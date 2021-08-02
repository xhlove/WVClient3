# instruction

The original project is [NoDRM](https://github.com/T3rry7f/NoDRM) (WVClient sequel, adapted to version 2209), thanks to the original author.

Here is changed to the python3 version, and the specific usage method is attached.

# ONLY WORK FOR PART WEBSITE

# Only applicable to some websites

# use

```bash
pip install -r requirements.txt
```

**Run & Run**

-`WideVineProxy.exe`

**Example & Usage**
```bash
python wvclient.py --init-path binary/init.mp4
python wvclient.py --pssh AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNzaioZmFysa
python wvclient.py --mpd-url https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/mpds/11331.mpd
python wvclient.py --init-url https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/video/1080_4800000/cenc_dash/init.mp4
```

**Attention && Attention**

-If you are not using the example command, please specify the `--license-url` option
-if you do not use example command, please specific `--license-url` option

![](/binary/Snipaste_2021-08-02_01-12-25.png)

**Help & HELP**
```bash
usage: wvclient3 v1.2@xhlove [-h] [--pssh PSSH] [--init-path INIT_PATH]
                             [--init-url INIT_URL] [--mpd-url MPD_URL]
                             [--license-url LICENSE_URL]

origin author is T3rry7f, this is a python3 version.

optional arguments:
  -h, --help show this help message and exit
  --pssh PSSH pssh which is base64 format
  --init-path INIT_PATH
                        init.mp4 file path
  --init-url INIT_URL init.mp4 segment url
  --mpd-url MPD_URL mpd url
  --license-url LICENSE_URL
                        widevine license server url
```
