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
import requests, subprocess

def is_mailhog_running(mailhog_ip):
    url = f"http://{mailhog_ip}:8025/api/v2/messages"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

parser = ArgumentParser(
    description="Set Odoo instance to use Mailhog as an outgoing STMP mail server",
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument("-d", "--db", dest="db", required=True, help="Odoo database to orient to mailhog")
parser.add_argument("-u", "--url", dest="url", default=None, help="URL of the Odoo server")
parser.add_argument("-U", "--user", dest="username", default="admin", help="Login to connect with")
parser.add_argument("-p", "--password", dest="password", default="admin", help="Password to connect with")
parser.add_argument("-m", "--mailhog-url", dest="mailhog_url", default="0.0.0.0:1025", help="Mailhog URL under which STMP works (not HTTP)")
args = parser.parse_args()

mailhog_ip, mailhog_port = args.mailhog_url.split(":")

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
        "smtp_host": mailhog_ip,
        "smtp_port": mailhog_port,
        "smtp_debug": False,
        "smtp_user": False,
        "smtp_pass": False,
        "smtp_ssl_certificate": False,
        "smtp_ssl_private_key": False,
    }],
)

# Odoo set to use Mailhog, is Mailhog running ?
if not is_mailhog_running(mailhog_ip):
    print("Odoo set to use Mailhog, but Mailhog is NOT running")
