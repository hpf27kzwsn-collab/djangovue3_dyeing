import json
import urllib.request
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
request = urllib.request.Request('https://api.github.com/repos/redis-windows/redis-windows/releases/latest', headers={'User-Agent':'djangovue3'})
release = json.load(urllib.request.urlopen(request))
asset = next(item for item in release['assets'] if item['name'].endswith('-cygwin.zip'))
destination = root / 'runtime' / 'downloads' / asset['name']
urllib.request.urlretrieve(asset['browser_download_url'], destination)
with zipfile.ZipFile(destination) as archive:
    archive.extractall(root / 'runtime' / 'redis')
print('Redis',release['tag_name'],asset['name'])
