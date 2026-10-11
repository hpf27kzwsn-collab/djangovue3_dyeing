"""为 Kombu 5.6.2 的 Redis extra 更新依赖声明；不修改传输实现。"""
import base64
import csv
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
metadata = json.load(urllib.request.urlopen('https://pypi.org/pypi/kombu/5.6.2/json'))
wheel = next(item for item in metadata['urls'] if item['filename'].endswith('.whl'))
original = urllib.request.urlopen(wheel['url']).read()
archive = zipfile.ZipFile(io.BytesIO(original))
files = {}
for name in archive.namelist():
    new_name = name.replace('kombu-5.6.2.dist-info/', 'kombu-5.6.2+dvadmin.1.dist-info/')
    files[new_name] = archive.read(name)
meta_name = 'kombu-5.6.2+dvadmin.1.dist-info/METADATA'
content = files[meta_name].decode()
content = content.replace('Version: 5.6.2\n', 'Version: 5.6.2+dvadmin.1\n')
lines = content.splitlines()
index = next(i for i, line in enumerate(lines) if line.startswith('Requires-Dist: redis') and 'extra == "redis"' in line)
lines[index] = 'Requires-Dist: redis==8.1.0; extra == "redis"'
files[meta_name] = ('\n'.join(lines)+'\n').encode()
record_name = 'kombu-5.6.2+dvadmin.1.dist-info/RECORD'
record = io.StringIO(newline='')
writer = csv.writer(record)
for name, content in files.items():
    if name != record_name:
        digest=base64.urlsafe_b64encode(hashlib.sha256(content).digest()).rstrip(b'=').decode()
        writer.writerow([name,'sha256='+digest,len(content)])
writer.writerow([record_name,'',''])
files[record_name]=record.getvalue().encode()
output = root/'wheels'/'kombu-5.6.2+dvadmin.1-py3-none-any.whl'
output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as patched:
    for name, content in files.items():patched.writestr(name, content)
print(output)
