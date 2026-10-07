with open(r'c:\__MEDLINK___\PMG\prototype_medlink\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
views = re.findall(r'v-if="currentView === \'([^\']+)\'"', text)
print("Views in template:", views)
for v in views:
    idx = text.find(f"v-if=\"currentView === '{v}'\"")
    print(f"  View '{v}' starts at char {idx}")
