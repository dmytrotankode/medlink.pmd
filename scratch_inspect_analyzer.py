# -*- coding: utf-8 -*-
with open('c:/__MEDLINK___/PMG/downloaded_js/js_nszu-analyzer-compiled.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re

print("Length:", len(code))

# Find all occurrences of upload / xhr / fetch / action
for m in re.finditer(r'(xhr|upload|fetch|action|endpoint|server|ajax|\.post)', code, re.I):
    start = max(0, m.start() - 60)
    end = min(len(code), m.end() + 100)
    snippet = code[start:end].replace('\n', ' ')
    if any(k in snippet.lower() for k in ['url', 'send', 'open', 'action', 'api', 'http', 'php']):
        print("MATCH:", snippet)

