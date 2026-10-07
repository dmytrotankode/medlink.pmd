with open(r'c:\__MEDLINK___\PMG\prototype_medlink\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
v_else = re.findall(r'v-else-if="currentView === \'([^\']+)\'"', text)
print("v-else-if views:", v_else)
