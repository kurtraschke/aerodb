import argparse
import sys
import logging

from aerodb import duplicate_report, duplicate_summary, test_lookup
from aerodb import apply_preferences, remove_orphans, fetch_aerodromes, export

parser = argparse.ArgumentParser(description='Management tool for aerodb.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--verbose', dest='verbose',
                    action='append_const', const=1)

subparsers = parser.add_subparsers(help='sub-command help')

fetch_parser = subparsers.add_parser('fetch', help='fetch help',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
fetch_parser.add_argument('--batch-size', '-b', type=int, default=1000,
                          help="Number of records to retrieve in each batch")
fetch_parser.add_argument('outfile', type=argparse.FileType('w'),
                          help="JSON output file")
fetch_parser.set_defaults(func=lambda args: fetch_aerodromes(args.batch_size,
                                                             args.outfile))

dr_parser = subparsers.add_parser('duplicate_report',
                                  help="Generate duplicate codes report")
dr_parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                               default=sys.stdin, help="JSON input file")
dr_parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'),
                               default=sys.stdout, help="CSV output file")
dr_parser.set_defaults(func=lambda args: duplicate_report(args.infile,
                                                          args.outfile))

ds_parser = subparsers.add_parser('duplicate_summary',
                                        help="Generate duplicate codes summary")
ds_parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                             default=sys.stdin, help="JSON input file")
ds_parser.set_defaults(func=lambda args: duplicate_summary(args.infile))

ap_parser = subparsers.add_parser('apply_preferences',
                                    help="Apply de-duplication preferences")
ap_parser.add_argument('-d', '--dry-run', action='store_true', default=False)
ap_parser.add_argument('preferences', type=argparse.FileType('r'),
                         help="CSV preferences file")
ap_parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                         default=sys.stdin, help="JSON input file")
ap_parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                         default=sys.stdout, help="JSON output file")
ap_parser.set_defaults(func=lambda args: apply_preferences(args.preferences,
                                                             args.infile,
                                                             args.outfile,
                                                             args.dry_run))

rmo_parser = subparsers.add_parser('remove_orphans',
                                   help="Remove orphaned entries")
rmo_parser.add_argument('-d', '--dry-run', action='store_true', default=False)
rmo_parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="JSON input file")
rmo_parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help="JSON output file")
rmo_parser.set_defaults(func=lambda args: remove_orphans(args.infile,
                                                         args.outfile,
                                                         args.dry_run))


lookup_parser = subparsers.add_parser('lookup', help="Perform test lookup")
lookup_parser.add_argument('infile', type=argparse.FileType('r'),
                           help="JSON input file")
lookup_parser.add_argument('code', help="Code to look up")
lookup_parser.add_argument('type', nargs='?',
                           choices=['icao', 'iata', 'faa', 'lid'],
                           help="Code type, defaults to any")
lookup_parser.set_defaults(func=lambda args: test_lookup(args.infile,
                                                         args.code,
                                                         args.type))

export_parser = subparsers.add_parser('export', help="Export aerodrome database")
export_parser.add_argument('infile', type=argparse.FileType('r'),
                           help="JSON input file")
export_parser.add_argument('outfile', type=argparse.FileType('wb'),
                           help="Output file")
export_parser.add_argument('--format', '-f',
                           choices=['kml', 'csv'],
                           default='kml',
                           help="Export file format")
export_parser.set_defaults(func=lambda args: export(args.infile, args.outfile,
                                                    args.format))


args = parser.parse_args()
loglevel = {0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG}.get(sum(args.verbose or [0]), logging.DEBUG)
logging.basicConfig(level=loglevel)
args.func(args)
