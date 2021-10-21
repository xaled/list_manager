#!/usr/bin/python3
import json
import sys
import time
import argparse
import uuid
from os.path import dirname, realpath, join, exists

WL_PATH = ""
DEFAULT_LIST = "default_list"
SCRIPT_DIR = dirname(realpath(__file__))
DB_PATH = join(SCRIPT_DIR, 'lists.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( "--list-dir", default=WL_PATH, help=f"target lists directory (default: {WL_PATH})")

    action = parser.add_subparsers(help='action', dest='action')
    parser_add = action.add_parser('add', help='add new entry')

    parser_add.add_argument("-v", "--validity", default=7, type=int, help="validity in days (default: 7)")
    parser_add.add_argument("-c", "--comment", default="no comment", help="entry comment")
    parser_add.add_argument("-l", "--list", default=DEFAULT_LIST, help=f"target list (default: {DEFAULT_LIST})")
    parser_add.add_argument("range", help="IP range")
    parser_remove = action.add_parser('remove', help='remove entry')
    parser_remove.add_argument("-l", "--list", default=DEFAULT_LIST, help=f"target list (default: {DEFAULT_LIST})")
    parser_remove.add_argument("range", help="IP range")
    parser_cron = action.add_parser('cron', help='run cron')
    args = parser.parse_args()

    if exists(DB_PATH):
        with open(DB_PATH) as fin:
            data = json.load(fin)
    else:
        data = {}
    if args.action == 'add':
        # _uuid = uuid.uuid4().hex
        if args.range != '':
            t0 = time.time()
            tf = t0 + args.validity * 86400
            if args.list not in data:
                data[args.list] = {}

            data[args.list][args.range] = {
                'created': t0,
                'expires': tf,
                'validity': args.validity,
                'comment': args.comment,
                'range': args.range,
            }
        else:
            print("provide an IP range")
            sys.exit(2)
    if args.action == 'remove':
        if args.list in data and args.range in data[args.list]:
            del data[args.list][args.range]
        else:
            print("List or range do not exists!")

    # Cron
    now = time.time()
    for l in data:
        to_delete = list()
        with open(join(args.list_dir, l), 'w') as fou:
            for u, e in data[l].items():
                if e['expires'] <= now and e['validity'] != -1:
                    to_delete.append(u)
                else:
                    fou.write("%s # %s - %s" % (e['range'], e['comment'],
                                                'never expires' if e['validity'] == -1 else
                                                'expires in %d days' % int((e['expires'] - now) / 86400)))
                    fou.write("\n")

        for u in to_delete:
            del data[l][u]

    with open(DB_PATH, 'w') as fou:
        json.dump(data, fou)
