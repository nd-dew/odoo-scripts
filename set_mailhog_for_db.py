#!/usr/bin/env python3

"""
This tool is sending mail to an Odoo instance (local or not).

Usage:
    send-mail.py <eml_file>
					<-d <database>>
					[-u <url> default:"http://localhost:8569"]
					[-U <user> default:"admin"]
					[-p <password> default:"admin"]
]

Commit odoo#ab70afb is removing the previously used route '/mail/receive'
Now we use the xmlrpc function to log to the db and the odoo's method message_process of mail.thread,
the first step on received emails.

Working version:
    8+
"""
import base64
import xmlrpc.client
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

parser = ArgumentParser(description="Send an email to Odoo databases", formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-u", "--url", dest="url", default="http://localhost:8569", help="URL of the Odoo server")
parser.add_argument("-d", "--db", dest="db", required=True, help="Odoo database to orient to mailhog")
parser.add_argument("-U", "--user", dest="username", default="admin", help="Login to connect with")
parser.add_argument("-p", "--password", dest="password", default="admin", help="Password to connect with")
args = parser.parse_args()

common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(args.url))
uid = common.authenticate(args.db, args.username, args.password, {})
models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(args.url))
models.execute_kw(
    args.db,
    uid,
    args.password,
    "ir.mail_server",
    "create",
    [{'name': 'Mailhog', 'from_filter': False, 'smtp_host': '0.0.0.0', 'smtp_port': 1025, 'smtp_debug': False,  'smtp_user': False, 'smtp_pass': False, 'smtp_ssl_certificate': False, 'smtp_ssl_private_key': False}],
)

