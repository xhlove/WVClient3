```bash
__        ____     ______ _ _            _   _____ 
\ \      / /\ \   / / ___| (_) ___ _ __ | |_|___ / 
 \ \ /\ / /  \ \ / / |   | | |/ _ \ '_ \| __| |_ \ 
  \ V  V /    \ V /| |___| | |  __/ | | | |_ ___) |
   \_/\_/      \_/  \____|_|_|\___|_| |_|\__|____/ 
```

---

[ENGLISH README](README_ENG.md)

# WVClient3

原项目是[NoDRM](https://github.com/T3rry7f/NoDRM)（WVClient续作，适配2209版本），感谢原作者。

这里改成了python3版本，并附上具体使用方法。

**晚些时候更新为cdmapi版本并附上详细的编译过程**

# 使用

```bash
pip install -r requirements.txt
```

### 编译cdmapi & Compile cdmapi

- 进入`cdmapi-python-extension-src`文件夹
    ```bash
    cd cdmapi-python-extension-src
    ```
- 执行编译命令
    ```bash
    python setup.py build_ext --inplace
    ```

**示例 & Usage**
```bash
python wvclient.py --init-path binary/init.mp4
python wvclient.py --pssh AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNkZmFsa3IzaioCSEQyAA==
python wvclient.py --mpd-url https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/mpds/11331.mpd
python wvclient.py --init-url https://bitmovin-a.akamaihd.net/content/art-of-motion_drm/video/1080_4800000/cenc_dash/init.mp4
```

**注意 && Attention**

- 如果使用的不是示例命令，请指定`--license-url`选项
- if you do not use example command, please specific `--license-url` option

![](/binary/Snipaste_2021-08-02_01-12-25.png)

**帮助 & HELP**
```bash
usage: wvclient3 v1.2@xhlove [-h] [--pssh PSSH] [--init-path INIT_PATH]
                             [--init-url INIT_URL] [--mpd-url MPD_URL]
                             [--license-url LICENSE_URL]

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
```