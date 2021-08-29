```bash
__        ____     ______ _ _            _   _____ 
\ \      / /\ \   / / ___| (_) ___ _ __ | |_|___ / 
 \ \ /\ / /  \ \ / / |   | | |/ _ \ '_ \| __| |_ \ 
  \ V  V /    \ V /| |___| | |  __/ | | | |_ ___) |
   \_/\_/      \_/  \____|_|_|\___|_| |_|\__|____/ 
```

---

# WVClient3

The original project is [NoDRM](https://github.com/T3rry7f/NoDRM), which is WVClient new version for widevinecdm 2209, thanks to T3rry7f.

WVClient3 is modified from it, with more detail guide.

# Usage

You can skip the next step if you are using python 3.7.4/3.7.10/3.8.5 with Windows System

## Compile cdmapi python binding library

**NOTE, must install Visual Studio first, its need cl.exe and link.exe to build library**

```bash
cd cdmapi-python-extension-src
python setup.py build_ext --inplace
```

After compiling successfully, move `cdmapi.cp38-win_amd64.pyd` to `pywidevine/cdm` and rename it to `cdmapi.pyd`

If you are not using Windows System, you should compile cryptopp library first

-  https://github.com/weidai11/cryptopp

Then move output static library to `cdmapi-python-extension-src` and modify `setup.py` **extra_objects**

If you are using python 3.7.10 and above, should compile `cryptopp` with `/MD` flag, which means multi thread dll

3.7.4 should compile `cryptopp` with `/MT` flag, which means multi thread

I havent tested others version, guess that all versions below 3.7.4 should use `/MT` flag, 3.7.4 - 3.7.10? Test is youself please.

## Install requirements.txt

```bash
pip install -r requirements.txt
```

## Command example

```bash
python wvclient.py --license-url "https://wv-keyos.licensekeyserver.com" --pssh "AAAAU3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADMIARIQMfrZEMw7Rnqy3TdKM7rd/BoLYnV5ZHJta2V5b3MiED5o9928RkXil+ELQ2BMelY=" --headers "customdata:PEtleU9TQXV0aGVudGljYXRpb25YTUw+PERhdGE+PEdlbmVyYXRpb25UaW1lPjIwMTYtMTEtMTkgMDk6MzQ6MDEuOTkyPC9HZW5lcmF0aW9uVGltZT48RXhwaXJhdGlvblRpbWU+MjAyNi0xMS0xOSAwOTozNDowMS45OTI8L0V4cGlyYXRpb25UaW1lPjxVbmlxdWVJZD4wZmZmMTk3YWQzMzQ0ZTMyOWU0MTA0OTIwMmQ5M2VlYzwvVW5pcXVlSWQ+PFJTQVB1YktleUlkPjdlMTE0MDBjN2RjY2QyOWQwMTc0YzY3NDM5N2Q5OWRkPC9SU0FQdWJLZXlJZD48V2lkZXZpbmVQb2xpY3kgZmxfQ2FuUGxheT0idHJ1ZSIgZmxfQ2FuUGVyc2lzdD0iZmFsc2UiIC8+PFdpZGV2aW5lQ29udGVudEtleVNwZWMgVHJhY2tUeXBlPSJIRCI+PFNlY3VyaXR5TGV2ZWw+MTwvU2VjdXJpdHlMZXZlbD48L1dpZGV2aW5lQ29udGVudEtleVNwZWM+PEZhaXJQbGF5UG9saWN5IC8+PExpY2Vuc2UgdHlwZT0ic2ltcGxlIiAvPjwvRGF0YT48U2lnbmF0dXJlPk1sNnhkcU5xc1VNalNuMDdicU8wME15bHhVZUZpeERXSHB5WjhLWElBYlAwOE9nN3dnRUFvMTlYK1c3MDJOdytRdmEzNFR0eDQydTlDUlJPU1NnREQzZTM4aXE1RHREcW9HelcwS2w2a0JLTWxHejhZZGRZOWhNWmpPTGJkNFVkRnJUbmxxU21raC9CWnNjSFljSmdaUm5DcUZIbGI1Y0p0cDU1QjN4QmtxMUREZUEydnJUNEVVcVJiM3YyV1NueUhGeVZqWDhCR3o0ZWFwZmVFeDlxSitKbWI3dUt3VjNqVXN2Y0Fab1ozSHh4QzU3WTlySzRqdk9Wc1I0QUd6UDlCc3pYSXhKd1ZSZEk3RXRoMjhZNXVEQUVZVi9hZXRxdWZiSXIrNVZOaE9yQ2JIVjhrR2praDhHRE43dC9nYWh6OWhVeUdOaXRqY2NCekJvZHRnaXdSUT09PC9TaWduYXR1cmU+PC9LZXlPU0F1dGhlbnRpY2F0aW9uWE1MPg=="
```

![](images/Snipaste_2021-08-29_18-40-47.png)

## HELP INFO

```bash
usage: wvclient3 v1.3@xhlove [-h] [--pssh PSSH] [--init-path INIT_PATH] [--init-url INIT_URL] [--mpd-url MPD_URL] [--license-url LICENSE_URL] [--headers HEADERS]

optional arguments:
  -h, --help            show this help message and exit
  --pssh PSSH           pssh which is base64 format
  --init-path INIT_PATH
                        init.mp4 file path
  --init-url INIT_URL   init.mp4 segment url
  --mpd-url MPD_URL     mpd url
  --license-url LICENSE_URL
                        widevine license server url
  --headers HEADERS     set custom headers for request, separators is |, e.g. "header1:value1|header2:value2"
```