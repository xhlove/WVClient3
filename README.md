# 说明

原项目是[WVClient](https://github.com/T3rry7f/WVClient)，感谢原作者。

这里改成了python3版本，并附上具体使用方法。

# 使用

首先将`widevinecdm.dll`放到本目录（我用的是1679版本），然后在这里开cmd，并运行`license_proxy.exe`，然后弹窗提示点确定。

![示意图](/binary/Snipaste_2020-11-05_21-10-11.png)

**示例**
```bash
python wvclient.py -path binary/init.mp4
```

![运行示意图](/binary/Snipaste_2020-11-05_22-18-29.png)

**帮助**
```bash
usage: wvclient3 v1.0@xhlove [-h] [-path INIT_PATH] [-pssh PSSH]
                             [-url LICENSE_URL]

origin author is T3rry7f, this is a python3 version.

optional arguments:
  -h, --help            show this help message and exit
  -path INIT_PATH, --init-path INIT_PATH
                        init.mp4 file path
  -pssh PSSH, --pssh PSSH
                        pssh which is base64 format
  -url LICENSE_URL, --license-url LICENSE_URL
                        widevine license server url
```

以上。