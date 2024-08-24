import random
import re
import os
import base64
import json
import urllib.parse

import cherrypy
import jinja2
import pymongo
import requests

from . import tasks, seeds

import FreeEnt

RANDOM_SEED_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789'
ACTIVITY_SPRITES = [
    'dkcecil', 'kain', 'crydia', 'tellah', 'edward', 'rosa', 'yang',
    'palom', 'porom', 'pcecil', 'cid', 'arydia', 'edge', 'fusoya', 
    'pig', 'toad', 'mini'
    ]
CHECKSUM_IMAGES = {}

def _json_escape_str(string):
    return json.dumps(string)[1:-1]

class Server:
    def __init__(self, db, task_queue):
        self._db = db
        self._task_store = tasks.TaskStore(db)
        self._seed_store = seeds.SeedStore(db)

        self._task_store.create_indices()
        self._seed_store.create_indices()

        db['api_keys'].create_index('key')

        self._task_queue = task_queue

    def verify_api_key(self, api_key):
        doc = self._db['api_keys'].find_one({'key' : api_key})
        return (doc is not None)

    def generate(self, flags, seed=None, metaconfig=None, api_key=None):
        try:
            flagset = FreeEnt.FlagSet(flags)
        except Exception as e:
            return {'error' : f'Flag string error: {str(e)} (flags: {flags})'}

        if metaconfig:
            if type(metaconfig) is str:
                try:
                    metaconfig = json.loads(metaconfig)
                except json.decoder.JSONDecodeError:
                    return {'error' : f'Metaconfiguration format error'}
            elif type(metaconfig) is not dict:
                return {'error' : f'Metaconfiguration format error - unexpectede type {type(metaconfig)}'}

        rnd = random.Random()
        if seed is None:
            seed = ''

        # sanitize seed string
        seed = re.sub(r'[^A-Z0-9]', '', seed.upper())[:10]
        if not seed:
            seed = ''.join([rnd.choice(RANDOM_SEED_CHARS) for x in range(10)])

        # check if seed already exists
        if not metaconfig:
            existing_seed_id = self._seed_store.lookup(flagset.to_binary(), seed)
            if existing_seed_id is not None:
                return {'seed_id' : existing_seed_id}

        # kick off generator process and return status page
        metadata = {}
        if api_key:
            metadata['api_key'] = api_key
        task_id = self._task_store.create(flags, seed, metaconfig, **metadata)

        self._task_queue.put(task_id)

        return { 'task_id' : task_id }

    def get_task_status(self, task_id):
        return self._task_store.get_status_report(task_id)

    def get_cached_seed(self, seed_id):
        return self._seed_store.get(seed_id)

    def set_cached_seed_metadata(self, seed_id, **metadata):
        self._seed_store.set_metadata(seed_id, **metadata)

class Admin:
    def __init__(self, server):
        self._server = server

    @cherrypy.expose
    def index(self):
        return "eyyyy"

class Api:
    def __init__(self, server):
        self._server = server

    @cherrypy.expose
    def doc(self):
        cherrypy.response.headers['Content-Type'] = "text/plain"
        with open(os.path.join(os.path.dirname(__file__), 'api_doc.txt'), 'r') as infile:
            return infile.read()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out()
    def generate(self, key, flags=None, seed=None):
        if cherrypy.request.app.config['FreeEnt']['require_api_key'] and not self._server.verify_api_key(key):
            return {'status' : 'error', 'error' : 'Invalid API key.'}

        try:
            body_params = json.loads(cherrypy.request.body.read())
        except json.decoder.JSONDecodeError:
            body_params = {}

        flags = body_params.get('flags', flags)
        seed = body_params.get('seed', seed)
        metaconfig = body_params.get('metaconfig', None)

        if flags is None:
            return {'status' : 'error', 'error' : 'No flags specified.'}

        generate_result = self._server.generate(flags, seed, metaconfig, api_key=key)

        if 'seed_id' in generate_result:
            return {'status' : 'exists', 'seed_id' : generate_result['seed_id'] }

        if 'task_id' in generate_result:
            return {'status' : 'ok', 'task_id' : generate_result['task_id'] }

        if 'error' in generate_result:
            error_msg = generate_result['error']
        else:
            error_msg = 'Unhandled generation request result.'

        return {'status' : 'error', 'error' : error_msg }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def task(self, key, id):
        if cherrypy.request.app.config['FreeEnt']['require_api_key'] and not self._server.verify_api_key(key):
            return {'status' : 'error', 'error' : 'Invalid API key.'}

        report = self._server.get_task_status(id)
        if 'result' in report:
            report['seed_id'] = report['result']
            del report['result']
        return report

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def seed(self, key, id):
        if cherrypy.request.app.config['FreeEnt']['require_api_key'] and not self._server.verify_api_key(key):
            return {'status' : 'error', 'error' : 'Invalid API key.'}

        cached_seed = self._server.get_cached_seed(id)
        if cached_seed is None:
            return {'status' : 'error', 'error' : 'Seed not found.'}

        site_root = cherrypy.request.app.config['FreeEnt']['site_root']
        return {
            'status' : 'ok',
            'version' : cached_seed.version,
            'seed' : cached_seed.seed,
            'flags' : cached_seed.flags,
            'verification' : '/'.join([t[0].upper() + t[1:] for t in cached_seed.verification]),
            'url' : f"{site_root}/get?id={id}"
        }

class Site:
    def __init__(self, server):
        self._server = server
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            )

    def _check_hibernation_mode(self):
        if cherrypy.request.app.config['FreeEnt']['hibernation_mode']:
            raise cherrypy.HTTPError(status=403, message="This site is now in hiberation mode; please visit the main page at http://ff4fe.com/")

    def _check_beta_redirect(self):
        if cherrypy.request.app.config['FreeEnt']['beta']:
            raise cherrypy.HTTPRedirect("/make")

    @cherrypy.expose
    def index(self, flags=None, seed=None):
        self._check_hibernation_mode()
        self._check_beta_redirect()
        return self._env.get_template('home.html').render()

    @cherrypy.expose
    def make(self, flags=None, seed=None):
        if cherrypy.request.app.config['FreeEnt']['beta']:
            with open(os.path.join(os.path.dirname(__file__), 'content', 'beta_changelog.txt'), 'r') as infile:
                beta_changelog = infile.read()
        else:
            beta_changelog = None

        return self._env.get_template('make_react.html').render(
            version=FreeEnt.VERSION_STR,
            production=(not cherrypy.request.app.config['FreeEnt']['debug']),
            initial_flags = (_json_escape_str(flags) if flags else ''),
            initial_seed = (seed if seed else ''),
            beta_changelog = beta_changelog
            )

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def generate(self, flags, seed=None, metaconfig=None, **kwargs):
        self._check_hibernation_mode()

        if not cherrypy.request.app.config['FreeEnt'].get('skip_captcha', False):
            if ('g-recaptcha-response' not in kwargs) or not kwargs['g-recaptcha-response']:
                return self._env.get_template("pregenerate.html").render(
                    flags = flags,
                    seed = (seed if seed else ''),
                    metaconfig = metaconfig,
                    recaptcha_site_key = cherrypy.request.app.config['FreeEnt']['recaptcha_site_key']
                    )
            else:
                remote_ip = cherrypy.request.remote.ip
                
                if 'X_FORWARDED_FOR' in cherrypy.request.headers and cherrypy.request.headers['X_FORWARDED_FOR']:
                    remote_ip = cherrypy.request.headers['X_FORWARDED_FOR']
                
                r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                    data = {
                        'secret' : cherrypy.request.app.config['FreeEnt']['recaptcha_secret_key'],
                        'response' : kwargs['g-recaptcha-response'],
                        'remoteip' : remote_ip
                    }
                    )

                if r.status_code != 200 or not r.json()['success']:
                    return self._env.get_template("seed_error.html").render(
                        title = "Verification error",
                        message = f"Error: There was a problem verifying your request. Please try again later."
                        )

        if not seed:
            seed = None

        generate_result = self._server.generate(flags, seed, metaconfig)

        if 'seed_id' in generate_result:
            raise cherrypy.HTTPRedirect(f"/get?id={generate_result['seed_id']}")

        if 'task_id' in generate_result:
            raise cherrypy.HTTPRedirect(f"/generating?task_id={generate_result['task_id']}")

        if 'error' in generate_result:
            error_msg = generate_result['error']
        else:
            error_msg = 'Unhandled generation request result.'

        return self._env.get_template("seed_error.html").render(
            title = "Generation error",
            message = f"Error: {error_msg}"
            )


    @cherrypy.expose
    def generating(self, task_id):
        rnd = random.Random()
        return self._env.get_template('generating.html').render(
            task_id = task_id,
            sprite = rnd.choice(ACTIVITY_SPRITES)
            )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status(self, id):
        return self._server.get_task_status(id)

    @cherrypy.expose
    def get(self, id):
        cached_seed = self._server.get_cached_seed(id)
        if cached_seed is None:
            return self._env.get_template("seed_error.html").render(seed_id = id)

        checksum_images = []
        for tile in cached_seed.verification:
            if tile not in CHECKSUM_IMAGES:
                with open(os.path.join(os.path.dirname(__file__), 'static', f'checksum-{tile}.png'), 'rb') as infile:
                    CHECKSUM_IMAGES[tile] = base64.b64encode(infile.read()).decode('utf-8')
            checksum_images.append(CHECKSUM_IMAGES[tile])

        try:
            metaconfig = cached_seed.metaconfig
        except AttributeError:
            metaconfig = None

        if metaconfig and metaconfig.get('hide_flags', False):
            encoded_flags = None
        elif cherrypy.request.app.config['FreeEnt']['beta']:
            encoded_flags = urllib.parse.quote(cached_seed.flags)
        else:
            encoded_flags = cached_seed.binary_flags

        public_spoiler = None
        try:
            public_spoiler = cached_seed.public_spoiler
        except AttributeError:
            # support for legacy spoiler format
            try:
                spoiler_access = cached_seed.spoiler_access
                if spoiler_access:
                    public_spoiler = cached_seed.spoiler
            except AttributeError:
                pass


        site_root = cherrypy.request.app.config['FreeEnt']['site_root']
        return self._env.get_template("seed_get.html").render(
            seed_url = f"{site_root}/get?id={id}",
            seed = cached_seed,
            patch = base64.b64encode(cached_seed.patch).decode('utf-8'),
            seed_key = id,
            flags_url = f'{site_root}/make?flags={encoded_flags}',
            checksum_images = checksum_images,
            hide_flags = (metaconfig and metaconfig.get('hide_flags', False)),
            test_settings = (json.dumps(metaconfig['test_settings']) if (metaconfig and metaconfig.get('test_settings', None)) else None),
            spoiler = (base64.b64encode(public_spoiler).decode('utf-8') if public_spoiler else None)
            )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def presets(self):
        with open(os.path.join(os.path.dirname(__file__), 'presets.json'), "r") as infile:
            presets = json.load(infile)
        
        processed_presets = []
        for item in presets:
            if 'href' in item:
                try:
                    r = requests.get(item['href'])
                    if r.status_code >= 200 and r.status_code < 300:
                        external_data = r.json()
                        for external_item in external_data:
                            external_item['external'] = True
                            processed_presets.append(external_item)
                except Exception as e:
                    # in all error cases, just skip this HREF
                    pass
            else:
                processed_presets.append(item)

        return processed_presets

def run(config, task_queue):
    conf = {
        '/static' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : os.path.abspath(os.path.join(os.path.dirname(__file__), 'static')),
            'tools.expires.on' : True,
            'tools.expires.secs' : (24 * 60 * 60),  # 24 hours
        },
        '/script' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : os.path.abspath(os.path.join(os.path.dirname(__file__), 'script')),
            'tools.expires.on' : True,
            'tools.expires.secs' : 0,
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'favicon.ico'))
        },
        'FreeEnt' : {
            'beta' : config.beta,
            'hibernation_mode' : os.path.exists(os.path.join(os.path.dirname(__file__), 'hibernate')),
            'require_api_key' : (not config.local)
        },
    }

    if config.local:
        conf['FreeEnt']['site_root'] = 'http://127.0.0.1:8080'
        #conf['FreeEnt']['recaptcha_site_key'] = 'recaptcha_site_key_dev'
        #conf['FreeEnt']['recaptcha_secret_key'] = 'recaptcha_secret_key_dev'
        conf['FreeEnt']['skip_captcha'] = True
        conf['FreeEnt']['debug'] = True
    else:
        if config.beta:
            conf['FreeEnt']['site_root'] = os.getenv("FE_BETA_SITE_URL")
        else:
            conf['FreeEnt']['site_root'] = os.getenv("FE_SITE_URL")
        #conf['FreeEnt']['recaptcha_site_key'] = 'recaptcha_site_key'
        #conf['FreeEnt']['recaptcha_secret_key'] = 'recaptcha_secret_key'
        conf['FreeEnt']['debug'] = False

    # Force skip captcha by default in open-source codebase
    conf['FreeEnt']['skip_captcha'] = True

    if not config.local:
        try:
            with open(os.path.join(os.path.dirname(__file__), '.password'), 'r') as infile:
                admin_pass = infile.read().strip()
        except FileNotFoundError:
            admin_pass = (False, False, False) #ie. should never match string

        conf['/admin'] = {
           'tools.auth_basic.on': True,
           'tools.auth_basic.realm': 'localhost',
           'tools.auth_basic.checkpassword': (lambda realm, username, password: password == admin_pass),
           'tools.auth_basic.accept_charset': 'UTF-8',            
            }

    if config.password:
        conf.update({'/' : {
           'tools.auth_basic.on': True,
           'tools.auth_basic.realm': 'localhost',
           'tools.auth_basic.checkpassword': (lambda realm, username, password: password == config.password),
           'tools.auth_basic.accept_charset': 'UTF-8',        
            }})

    #if not config.local and not config.beta:
    #    cherrypy.config.update({'request.show_tracebacks': False})

    cherrypy.config.update({'server.socket_port' : config.port})
    if not config.local:
        cherrypy.config.update({
            'environment' : 'production',
            'show_tracebacks' : False
            })

    db_client = pymongo.MongoClient(config.db_url)
    db = db_client[config.db_name]

    server = Server(db, task_queue)
    website = Site(server)
    website.api = Api(server)
    website.admin = Admin(server)

    cherrypy.quickstart(website, '', conf)

