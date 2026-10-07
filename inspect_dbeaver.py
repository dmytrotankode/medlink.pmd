import json

path = r'C:\Users\tanko\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver\data-sources.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in data.get('connections', {}).items():
    cfg = v.get('configuration', {})
    host = cfg.get('host')
    dbname = cfg.get('database')
    user = cfg.get('user')
    print(f"ID: {k} | Name: {v.get('name')} | Host: {host} | DB: {dbname} | User: {user}")
