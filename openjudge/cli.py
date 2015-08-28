import argparse
from . import config, slave


def get_parser():
    """
    Return a parser for the package
    """
    parser = argparse.ArgumentParser(description='''
    LAN programming judge.
    ''')
    return parser


def add_arguments(parser):
    """
    Add relevant arguments
    """
    parser.add_argument('-ll',
                        '--log-level',
                        help='Logging level',
                        type=int,
                        default=config.default_loglevel)
    parser.add_argument('-t',
                        '--timeout',
                        help='Code check timeout in seconds',
                        type=int,
                        default=config.timeout_limit)
    parser.add_argument('-d',
                        '--check-data-folder',
                        help='Data folder for check data storage',
                        default=config.check_data_folder)
    parser.add_argument('-w',
                        '--web-server',
                        help='Web server address',
                        default=config.webserver)
    parser.add_argument('-u',
                        '--detail-url',
                        help='Question and language detail url',
                        default=config.detail_url)
    parser.add_argument('-b',
                        '--bind',
                        help='Address to listen at',
                        default=config.listen_addr)
    parser.add_argument('-j',
                        '--job-list-prefix',
                        help='The name to use for job list prefix',
                        default=config.job_list_prefix)
    parser.add_argument('-p',
                        '--protocol',
                        help='Protocol of the webserver',
                        default=config.protocol_of_webserver)
    parser.add_argument('-l',
                        '--log-file',
                        help='Name of logfile to use',
                        default=config.logfile)
    return parser


def process_args_and_get_slave(args):  # pragma: no cover
    "Process the args"
    return slave.Slave(webserver=args.web_server,
                       detail_url=args.detail_url,
                       listen_addr=args.bind,
                       timeout_limit=args.timeout,
                       loglevel=args.log_level)


def main():  # pragma: no cover
    parser = get_parser()
    parser = add_arguments(parser)
    args = parser.parse_args()
    s = process_args_and_get_slave(args)
    s.run()
