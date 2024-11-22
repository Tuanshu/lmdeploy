# Copyright (c) OpenMMLab. All rights reserved.
import os
import sys

from .cli import CLI
from .lite import SubCliLite
from .serve import SubCliServe


def run():
    print(('[dev] entrypoint run called'))
    """The entry point of running LMDeploy CLI."""
    args = sys.argv[1:]
    CLI.add_parsers()
    SubCliServe.add_parsers()
    SubCliLite.add_parsers()
    parser = CLI.parser
    args = parser.parse_args()
    print((f'[dev] args={args}'))

    if hasattr(args, 'model_name'):
        # if `model_name` is not specified, use the model_path instead. The
        # 'model_path' could be a a local path, or a repo id from hub
        args.model_name = args.model_name if args.model_name else \
            args.model_path

    if 'run' in dir(args):
        print((f'[dev] run in arg'))

        from lmdeploy.utils import get_model
        model_path = getattr(args, 'model_path', None)
        revision = getattr(args, 'revision', None)
        download_dir = getattr(args, 'download_dir', None)
        if model_path is not None and not os.path.exists(args.model_path):
            print(f'[dev] about to get_model with model_path={args.model_path}, download_dir={download_dir}, revision={revision}')

            args.model_path = get_model(args.model_path,
                                        download_dir=download_dir,
                                        revision=revision)
        model_path_or_server = getattr(args, 'model_path_or_server', None)
        if model_path_or_server is not None and (
                ':' not in model_path_or_server
                and not os.path.exists(model_path_or_server)):
            args.model_path_or_server = get_model(args.model_path_or_server,
                                                  download_dir=download_dir,
                                                  revision=revision)
        print(f'[dev] about to run with args={args}')
        args.run(args)
    else:
        print((f'[dev] run NOT in arg'))
        try:
            args.print_help()
        except AttributeError:
            command = args.command
            if command == 'serve':
                SubCliServe.parser.print_help()
            elif command == 'lite':
                SubCliLite.parser.print_help()
            else:
                parser.print_help()
