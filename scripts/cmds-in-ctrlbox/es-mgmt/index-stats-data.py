import requests
import sys
import os
import json
import subprocess
import time

curdir = os.getcwd()
rel_path = os.path.dirname(sys.argv[0])
if rel_path == '': rel_path = '.'

es_host = 'http://elasticsearch:9200'
disk_script_path = "%s/collect-disk-stats.sh" % (rel_path)

try:
    r = subprocess.check_output(disk_script_path, shell=True)
    disk_data = json.loads(r)
except Exception as e:
    print("failed to get disk usage info: %s" % e.message)
    sys.exit(1)

print("debug info: disk_data: %s" % (json.dumps(disk_data, indent=2)))

datestr = time.strftime("%Y.%m.%d", time.gmtime())
timestr = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

try:
    index_name = "healthcheck-%s" % datestr
    disk_data['timestamp'] = timestr
    r = requests.post(
        "%s/%s/_doc" % (es_host, index_name), 
        headers={"Content-Type": "application/json"},
        json=disk_data
    )
    print(r.json())
except Exception as e:
    print("failed to post doc to index %s: %s" % (index_name, e.message))
