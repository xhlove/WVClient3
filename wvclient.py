import re
import sys
import base64
import socket
import binascii
import requests
from pathlib import Path
from Crypto.Hash import CMAC
from Crypto.Hash import SHA1
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from argparse import ArgumentParser
from urllib.request import getproxies
from utils import license_protocol_pb2


USER_AGNET = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

# rewrite from https://github.com/T3rry7f/NoDRM/tree/master/WVClient use python3
# example init.mp4 https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/video/1080_4800000/cenc_dash/init.mp4


class PSSH:

    def __init__(self, proxy_url: str = None):
        if proxy_url is None:
            self.proxies = getproxies()
        else:
            self.proxies = {'http': proxy_url, 'https': proxy_url}

    def read_from_file(self, file_path: str):
        raw = Path(file_path).read_bytes()
        offset = raw.rfind(b'pssh')
        return raw[offset - 4:offset - 4 + raw[offset - 1]]

    def read_from_init_url(self, url: str):
        pssh = None
        try:
            r = requests.get(url, headers={'user-agnet': USER_AGNET}, proxies=self.proxies, timeout=5)
            pssh = self.read_from_file(r.content)
        except Exception:
            pass
        return pssh

    def read_from_mpd_url(self, url: str):
        pssh = None
        try:
            r = requests.get(url, headers={'user-agnet': USER_AGNET}, proxies=self.proxies, timeout=5)
            content = r.content.decode('utf-8')
            results = re.findall(r'pssh.+<', content, re.M | re.I)
            pssh = base64.b64decode(results[0].split('>')[1].split('<')[0])
        except Exception:
            pass
        return pssh


class WidevineCDM:
    def __init__(self, license_url: str):
        self.public_key = binascii.a2b_hex(
            '30820122300d06092a864886f70d01010105000382010f003082010a0282010100bca83d793f493c49df558612e74c773198ab4901f20369bfaf1598d71e362ef13ab9be3b4d4d73c63'
            '378542d23beba56ad4d589c1e7f151e25cf6f7a38f8ff1ff491d5d2dfc971617b6d9559406e3a5127b2aebddea965e0dfcf4c50ae241caf9e87bfe33b0db619b5c395e3986e310a3278'
            'f990b4139a421af74b3e4e1548250dec8f1755b038e61069e2547983ed93878549b4a9f5faa1bef72a75a9929fa7240fb1e46b9587170ef993c29c35f1f145e55bfec0de85d2b9409d6'
            '599b1c348bf76dd441abd53033475e3267f91647c2584d974d3ad7b8c0c33711556d6c2cf23bf7905b17a68c622a0580a623c1af9f446294d5f2de50721d85eb5f49b70130203010001'
        )
        self.proxies = getproxies()
        self.license_url = license_url
        self.headers = {"Cookie": ""}
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def generateRequestData(self, pssh: bytes):
        self._socket.settimeout(3)
        self._socket.connect(("127.0.0.1", 8888))
        self._socket.send(pssh)
        recv = self._socket.recv(10240)
        return recv

    def getContentKey(self, license_request_data: bytes):
        licenseMessage = license_protocol_pb2.License()
        requestMessage = license_protocol_pb2.SignedMessage()
        responseMessage = license_protocol_pb2.SignedMessage()
        resp = requests.post(self.license_url, license_request_data, headers=self.headers)
        requestMessage.ParseFromString(license_request_data)
        responseMessage.ParseFromString(resp.content)

        pubkey = RSA.importKey(self.public_key)
        verifier = pss.new(pubkey)
        h = SHA1.new(requestMessage.msg)
        verifier.verify(h, requestMessage.signature)
        enc_session_key = responseMessage.session_key
        self._socket.send(enc_session_key.hex().encode('utf-8'))
        sessionKey = binascii.a2b_hex(self._socket.recv(1024))
        licenseMessage.ParseFromString(responseMessage.msg)
        context_enc = b'\x01ENCRYPTION\x00' + requestMessage.msg + b"\x00\x00\x00\x80"
        cobj = CMAC.new(sessionKey, ciphermod=AES)
        enc_cmac_key = cobj.update(context_enc).digest()

        for key in licenseMessage.key:
            if not key.id:
                continue
            cipher = AES.new(enc_cmac_key, AES.MODE_CBC, iv=key.iv[0:16])
            dkey = cipher.decrypt(key.key[0:16])
            print(f'KID:KEY {key.id.hex()}:{dkey.hex()}')

    def work(self, pssh: bytes):
        license_request_data = self.generateRequestData(pssh)
        if license_request_data is None:
            sys.exit("generate requests data failed.")
        self.getContentKey(license_request_data)


def main(args):
    if args.init_path is not None:
        pssh = PSSH().read_from_file(args.init_path)
    elif args.pssh is not None:
        if len(args.pssh) % 4 != 0:
            args.pssh += "=" * (4 - len(args.pssh) % 4)
        pssh = base64.b64decode(args.pssh)
    else:
        sys.exit("not possible exit from here")
    cdm = WidevineCDM(args.license_url)
    cdm.work(pssh)


if __name__ == "__main__":
    command = ArgumentParser(
        prog="wvclient3 v1.2@xhlove",
        description=("origin author is T3rry7f, this is a python3 version.")
    )
    command.add_argument("-path", "--init-path", help="init.mp4 file path")
    command.add_argument("-pssh", "--pssh", help="pssh which is base64 format")
    command.add_argument("-url", "--license-url", default="https://widevine-proxy.appspot.com/proxy", help="widevine license server url")
    args = command.parse_args()
    if args.init_path is None and args.pssh is None:
        sys.exit("must specific one of init file path and pssh data")
    if args.license_url is None:
        sys.exit("must specific license url")
    main(args)