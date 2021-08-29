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
python wvclient.py --init-path binary/init.mp4
python wvclient.py --pssh AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNkZmFsa3IzaioCSEQyAA==
python wvclient.py --mpd-url https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/mpds/11331.mpd
python wvclient.py --init-url https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/video/1080_4800000/cenc_dash/init.mp4
```

## Attention

- if you do not use example command, please specific `--license-url` option

![](images/Snipaste_2021-08-29_18-40-47.png)

## HELP INFO

```bash
usage: wvclient3 v1.3@xhlove [-h] [--pssh PSSH] [--init-path INIT_PATH] [--init-url INIT_URL] [--mpd-url MPD_URL] [--license-url LICENSE_URL] [--headers HEADERS]

origin author is T3rry7f, this is a python3 version.

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