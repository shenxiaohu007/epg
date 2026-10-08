#!/usr/bin/env python3
# get-epg.py —— 从公开 XMLTV 源下载 EPG，同时保存 epg.xml 和 epg.xml.gz
import urllib.request, gzip, os

SOURCES = [
    "http://epg.51zmt.top:8000/e.xml.gz",   # 主源：老张EPG 压缩版(.zg)
    "https://epg.zsdc.eu.org/t.xml.gz",        # 备用源
]
OUT = "epg.xml"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read()

def main():
    for url in SOURCES:
        try:
            data = fetch(url)
            # .zg 是 gzip 压缩格式，检测到魔数 \x1f\x8b 就解压成明文 XML
            if data[:2] == b'\x1f\x8b':
                data = gzip.decompress(data)
            # 保存明文版
            with open(OUT, "wb") as f:
                f.write(data)
            # 保存 gzip 压缩版
            with gzip.open(OUT + ".gz", "wb", compresslevel=9) as f:
                f.write(data)
            print(f"成功: {url} -> {OUT} ({len(data)} bytes), {OUT}.gz ({os.path.getsize(OUT + '.gz')} bytes)")
            return
        except Exception as e:
            print(f"失败: {url} -> {e}")
    raise SystemExit("所有数据源均失败")

if __name__ == "__main__":
    main()
