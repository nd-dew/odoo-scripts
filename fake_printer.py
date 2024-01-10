import argparse
import base64
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from PIL import Image, ImageOps
import re

logging.basicConfig()
_logger = logging.getLogger(__name__)
_logger.setLevel('INFO')

EPOS_PATH = '/cgi-bin/epos/service.cgi?devid=local_printer'

parser = argparse.ArgumentParser(prog='PrinterSimulator', description='Simulate printer to use in Odoo PoS')
parser.add_argument('-c', '--callback', choices=['nothing', 'show', 'save'], default='show', help='Callback action when a request is received')
parser.add_argument('-p', '--port', default=9000, type=int, help='Port on which the simulated printer will be available')
parser.add_argument('-i', '--http-interface', default='127.0.0.1', help='IP address on which the HTTP server listens')

args = parser.parse_args()


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != EPOS_PATH:
            return

        # Handle ePoS simulation
        length = int(self.headers['content-length'])
        print_detail = self.rfile.read(length)

        width = int(re.search(b'width="(\d+)"', print_detail).group(1))
        height = int(re.search(b'height="(\d+)"', print_detail).group(1))
        image_content_base_64 = re.search(b'<image .*?>(.*)</image>', print_detail).group(1)

        # Reconvert the received data by something we can interpret
        decoded_string = base64.b64decode(image_content_base_64)
        binary_img = ''.join(format(byte, '08b') for byte in decoded_string)
        data = bytes([255 if b == '0' else 0 for b in binary_img])

        callback = args.callback
        if callback != 'nothing':
            # TODO: check if mode 1 can be used instead of 'L'
            #  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
            img = Image.frombuffer('L', (width, height), data)
            if callback == 'show':
                img.show()
            elif callback == 'save':
                img.save(f"receipt{args.http_interface}_{args.port}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")

        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'<response xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print" success="true" code="lse-dummy-simulated-epos-printer" />')


if __name__ == '__main__':
    http_interface, http_port = args.http_interface, args.port
    _logger.info(f'Open ePoS-simulator server on {http_interface}:{http_port}')
    server = HTTPServer((http_interface, http_port), RequestHandler)
    server.serve_forever()
