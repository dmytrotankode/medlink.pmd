import json

def update():
    with open(r'c:\__MEDLINK___\PMG\normative_packages\all_packages_manifest.json', 'r', encoding='utf-8') as f:
        all_pkgs = json.load(f)
    print(f"Loaded {len(all_pkgs)} packages from manifest")

    for file_path in [
        r'c:\__MEDLINK___\PMG\prototype_medlink\data.js',
        r'c:\__MEDLINK___\PMG\prototype\data.js'
    ]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            prefix = 'window.PROTOTYPE_DATA = '
            if content.startswith(prefix):
                json_str = content[len(prefix):].rstrip(';')
                data = json.loads(json_str)
                old_count = len(data.get('packages', []))
                data['packages'] = all_pkgs
                with open(file_path, 'w', encoding='utf-8') as fw:
                    fw.write(prefix + json.dumps(data, ensure_ascii=False) + ';\n')
                print(f"Updated {file_path}: from {old_count} to {len(all_pkgs)} packages.")
        except Exception as e:
            print(f"Error updating {file_path}: {e}")

if __name__ == '__main__':
    update()
