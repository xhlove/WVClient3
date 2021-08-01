# 说明

原项目是[NoDRM](https://github.com/T3rry7f/NoDRM)（WVClient续作，适配2209版本），感谢原作者。

这里改成了python3版本，并附上具体使用方法。

# 使用

运行`WideVineProxy.exe`

执行脚本

**示例**
```bash
python wvclient.py -path binary/init.mp4
```

**帮助**
```bash
usage: wvclient3 v1.2@xhlove [-h] [-path INIT_PATH] [-pssh PSSH]
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