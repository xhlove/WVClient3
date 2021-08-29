import re
import sys
import base64
import requests
from pathlib import Path
from argparse import ArgumentParser
from urllib.request import getproxies
from pywidevine.decrypt.wvdecrypt import WvDecrypt

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'


class CmdArgs:

    def __init__(self):
        self.pssh = None # type: str
        self.init_path = None # type: str
        self.init_url = None # type: str
        self.mpd_url = None # type: str
        self.license_url = None # type: str


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
            r = requests.get(url, headers={'user-agnet': USER_AGENT}, proxies=self.proxies, timeout=5)
            offset = r.content.rfind(b'pssh')
            pssh = r.content[offset - 4:offset - 4 + r.content[offset - 1]]
        except Exception:
            pass
        return pssh

    def read_from_mpd_url(self, url: str):
        pssh = None
        try:
            r = requests.get(url, headers={'user-agnet': USER_AGENT}, proxies=self.proxies, timeout=5)
            results = re.findall(r'ed.+\n.+(pssh.+)<', r.content.decode('utf-8'), re.M | re.I)
            pssh = base64.b64decode(results[0].split('>')[1].split('<')[0])
        except Exception:
            pass
        return pssh


class Headers:
    def __init__(self):
        self.headers = {}

    def get(self, args: CmdArgs) -> dict:
        self.__generate(args)
        return self.headers

    def __generate(self, args: CmdArgs):
        '''
        - 不指定user-agent 使用默认值
        - 指定user-agent 使用指定值 如果为"" 那么user-agent就是""
        '''
        if args.headers != '':
            self.__add_headers(args.headers)

    def __add_headers(self, text: str):
        text = text.strip()
        for one_header in text.split('|'):
            data = one_header.strip().split(':', maxsplit=1)
            if len(data) == '':
                continue
            if len(data) == 1:
                self.headers[data[0]] = ''
            else:
                self.headers[data[0]] = data[1]


def check_pssh(pssh_b64: str):
    WV_SYSTEM_ID = [237, 239, 139, 169, 121, 214, 74, 206, 163, 200, 39, 220, 213, 29, 33, 237]
    pssh = base64.b64decode(pssh_b64)
    if not pssh[12:28] == bytes(WV_SYSTEM_ID):
        new_pssh = bytearray([0, 0, 0])
        new_pssh.append(32 + len(pssh))
        new_pssh[4:] = bytearray(b"pssh")
        new_pssh[8:] = [0, 0, 0, 0]
        new_pssh[13:] = WV_SYSTEM_ID
        new_pssh[29:] = [0, 0, 0, 0]
        new_pssh[31] = len(pssh)
        new_pssh[32:] = pssh
        return base64.b64encode(new_pssh)
    else:
        return base64.b64decode(pssh_b64)


def command_handler(args: CmdArgs):
    '''
    检查命令参数
    '''
    if args.license_url is None:
        assert 1 == 0, 'must set --license-url option'
    args.headers = Headers().get(args)


def main(args: CmdArgs):
    if args.pssh:
        if len(args.pssh) % 4 != 0:
            args.pssh += '=' * (4 - len(args.pssh) % 4)
        # pssh = base64.b64decode(args.pssh)
        pssh = check_pssh(args.pssh)
    elif args.init_path:
        pssh = PSSH().read_from_file(args.init_path)
    elif args.init_url:
        pssh = PSSH().read_from_init_url(args.init_url)
    elif args.mpd_url:
        pssh = PSSH().read_from_mpd_url(args.mpd_url)
    else:
        sys.exit('at least specific one of them: --pssh, --init-path, --init-url, --mpd-url')
    if not pssh:
        sys.exit('can not get pssh')

    pssh = base64.b64encode(pssh).decode('utf-8')

    cert = requests.post(args.license_url, b'\x08\x04').content
    wvdecrypt = WvDecrypt(pssh)
    wvdecrypt.set_certificate(base64.b64encode(cert))
    challenge = wvdecrypt.get_challenge()
    license = requests.post(args.license_url, challenge, headers=args.headers).content
    wvdecrypt.update_license(base64.b64encode(license))
    keys = wvdecrypt.start_process()

    for k in keys:
        print(k)


if __name__ == '__main__':
    command = ArgumentParser(
        prog='wvclient3 v1.3@xhlove',
        description=('origin author is T3rry7f, this is a python3 version.')
    )
    command.add_argument('--pssh', help='pssh which is base64 format')
    command.add_argument('--init-path', help='init.mp4 file path')
    command.add_argument('--init-url', help='init.mp4 segment url')
    command.add_argument('--mpd-url', help='mpd url')
    command.add_argument('--license-url', help='widevine license server url')
    command.add_argument('--headers', help='set custom headers for request, separators is |, e.g. "header1:value1|header2:value2"')
    args = command.parse_args()
    command_handler(args)
    main(args)