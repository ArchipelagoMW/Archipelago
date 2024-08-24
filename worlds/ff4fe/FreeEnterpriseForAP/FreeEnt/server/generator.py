import time
import multiprocessing
import io
import os
import re
import traceback
import queue
import subprocess
import tempfile
import sys
import datetime
import zipfile
import uuid

import pymongo
import FreeEnt

from . import tasks, seeds

def _generate(config, task_doc, *args, **kwargs):
    db_client = pymongo.MongoClient(config.db_url)
    db = db_client[config.db_name]

    try:
        _generate_impl(config, db, task_doc, *args, **kwargs)
    except Exception as e:
        task_store = tasks.TaskStore(db)
        task_store.report_error(task_doc['task_id'], str(e), trace=traceback.format_exc())

    db_client.close()

def _generate_impl(config, db, task_doc, build_cache_dir_name):        
    task_store = tasks.TaskStore(db)
    task_store.report_status(task_doc['task_id'], tasks.STATUS_IN_PROGRESS)

    generator = FreeEnt.Generator()
    options = generator.options

    try:
        options.flags.load(task_doc['flags'])
    except Exception as e:
        task_store.report_error(task_doc['task_id'], f'Invalid flag string: {str(e)}')
        return

    options.seed = task_doc['seed']
    options.beta = config.beta

    if 'metaconfig' in task_doc:
        if task_doc['metaconfig'].get('hide_flags', False):
            options.hide_flags = True
        if 'test_settings' in task_doc['metaconfig']:
            options.test_settings.update(task_doc['metaconfig']['test_settings'])

    options.clean_cache = False
    if build_cache_dir_name is None:
        build_cache_dir_name = FreeEnt.VERSION_STR
    options.cache_path = os.path.join(os.path.dirname(__file__), '_build', build_cache_dir_name)

    source_rom_path = config.rom
    with open(source_rom_path, 'rb') as infile:
        source_rom = infile.read()

    source_buffer = io.BytesIO(source_rom)
    build_output = generator.generate(source_buffer)

    # generate BPS patch
    temp_handle, temp_dst_path = tempfile.mkstemp(text=False)
    os.close(temp_handle)

    with open(temp_dst_path, 'wb') as outfile:
        outfile.write(build_output.rom)

    temp_handle, temp_bps_path = tempfile.mkstemp()
    os.close(temp_handle)

    if sys.platform == 'darwin':
        flips_binary = 'flips-mac'
    elif sys.platform == 'win32':
        flips_binary = 'flips.exe'
    else:
        flips_binary = 'flips-linux'

    flips_path = os.path.join(os.path.dirname(__file__), 'bin', flips_binary)
    if not os.path.exists(flips_path):
        raise Exception("FLIPS binary not found")
    
    flips_args = (
        flips_path,
        '--create',
        '--bps',
        source_rom_path,
        temp_dst_path,
        temp_bps_path
        )
    subprocess.run(flips_args, capture_output=True)

    with open(temp_bps_path, 'rb') as infile:
        bps_patch = infile.read()
        if not bps_patch:
            raise Exception("BPS patch is empty; something went wrong when creating it?")

    os.unlink(temp_dst_path)
    os.unlink(temp_bps_path)

    seed_store = seeds.SeedStore(db)

    metadata = {
        'version' : build_output.version,
        'flags' : build_output.flags,
        'binary_flags' : build_output.binary_flags,
        'seed' : build_output.seed,
        'verification' : build_output.verification    
        }

    if 'metaconfig' in task_doc:
        metadata['metaconfig'] = task_doc['metaconfig']
        seed_id = f'u{uuid.uuid1().hex.upper()}'
    else:
        seed_id = f'{build_output.binary_flags}.{build_output.seed}'

    if build_output.public_spoiler is not None:
        public_spoiler = build_output.public_spoiler.encode('utf-8')
        metadata['public_spoiler'] = public_spoiler

    metadata['spoiler'] = build_output.private_spoiler.encode('utf-8')

    seed_store.put(seed_id, bps_patch, **metadata)

    task_store.report_done(task_doc['task_id'], seed_id)

def run(config, task_queue):
    if config.beta:
        build_cache_dir_name = 'beta'
    else:
        build_cache_dir_name = None

    db_client = pymongo.MongoClient(config.db_url)
    db = db_client[config.db_name]

    while True:
        task_id = task_queue.get()

        doc = db['tasks'].find_one({'task_id' : task_id})
        if doc is None:
            continue

        if doc['status'] != tasks.STATUS_PENDING:
            continue

        generate_process = multiprocessing.Process(
            target = _generate,
            args = (config, doc, build_cache_dir_name),
            daemon = True
            )
        generate_process.start()


