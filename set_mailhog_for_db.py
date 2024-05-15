#!/usr/bin/env python3

"""
This tool is setting odoo instance to use Mailhog as an outgoing STMP mail server

Minimal Usage:
    python set_mailhog_for_db -d <db_name>
    python set_mailhog_for_db -d 17d
The above: sets odoo running on url "http://o17d:8069" and with db called "17d", to use Mailhog as an outgoing STMP mail server

            -d <database>>
            [-u <url> default:"http://localhost:8569"]
            [-U <user> default:"admin"]
            [-p <password> default:"admin"]
]


"""

import base64
import xmlrpc.client
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

parser = ArgumentParser(
    description="Set Odoo instance to use Mailhog as an outgoing STMP mail server",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument("-d", "--db", dest="db", required=True, help="Odoo database to orient to mailhog")
parser.add_argument("-u", "--url", dest="url", default=None, help="URL of the Odoo server")
parser.add_argument("-U", "--user", dest="username", default="admin", help="Login to connect with")
parser.add_argument("-p", "--password", dest="password", default="admin", help="Password to connect with")
args = parser.parse_args()

if not args.url:
    args.url = f"http://o{args.db}:8069"
    print(f'Infered url:"{args.url}"')

common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(args.url))
uid = common.authenticate(args.db, args.username, args.password, {})
models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(args.url))
models.execute_kw(
    args.db,
    uid,
    args.password,
    "ir.mail_server",
    "create",
    [{
        "name": "Mailhog",
        "from_filter": False,
        "smtp_host": "0.0.0.0",
        "smtp_port": 1025,
        "smtp_debug": False,
        "smtp_user": False,
        "smtp_pass": False,
        "smtp_ssl_certificate": False,
        "smtp_ssl_private_key": False,
    }],
)
