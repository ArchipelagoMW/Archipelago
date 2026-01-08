import logging, os
from ..log.format import *
from .. import args

from .. import args as args
name, ext = os.path.splitext(args.output_file)
log_file = "{}{}".format(name, ".txt")
if args.stdout_log:
    import sys
    logging.basicConfig(stream = sys.stdout, filemode = 'w', level = logging.INFO, format = "%(message)s")
else:
    logging.basicConfig(filename = log_file, filemode = 'w', level = logging.INFO, format = "%(message)s")

hash = ', '.join([entry.name for entry in args.sprite_hash])
import time
from .. import version as version
log_msg =  f"Version   {version.__version__}\n"
log_msg += f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
log_msg += f"Input     {os.path.basename(args.input_file)}\n"
if args.ap_data:
    log_msg += f"AP Data   {os.path.basename(args.ap_data_path)}\n"
log_msg += f"Output    {os.path.basename(args.output_file)}\n"
log_msg += f"Log       {os.path.basename(log_file)}\n"
if args.website_url:
    log_msg += f"Website   {args.website_url}\n"
log_msg += f"Seed      {args.seed}\n"
if not args.hide_flags:
    log_msg += f"Flags     {args.flags}\n"
log_msg += f"Hash      {hash}"

if args.debug:
    log_msg += "\nDebug Mode"

logging.info(log_msg)

if not args.stdout_log:
    print(log_msg)

#if not args.hide_flags:
#    args.log()

if args.manifest_file:
    import json
    from ..api.get_manifest import get_manifest
    manifest = get_manifest(args.flags, hash, args.seed_id)
    with open(args.manifest_file, "wb") as output:
        output.write(json.dumps(manifest, indent=4).encode())
