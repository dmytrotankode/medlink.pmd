import sys
sys.path.append(r'c:\__MEDLINK___\PMG')
import scripts.build_pmg_catalog as b

for p in b.PACKAGES_DATA:
    if p['id'] in ['47', '54', '18']:
        print(f"PKG {p['id']}: name={repr(p['name'])}, cat={repr(p['category'])}")
