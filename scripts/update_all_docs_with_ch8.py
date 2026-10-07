import re, glob

files = glob.glob(r'c:\__MEDLINK___\PMG\docs_html\*.html')

ch8_link = """      <li class="nav-item">
        <a href="08_medlink_existing_ui_augmentation_guide.html"><i class="material-icons">extension</i> 8. Доповнення існуючих форм МІС</a>
      </li>"""

pattern = r'(<a href="07_nszu_file_analysis_literal_compliance\.html">[\s\S]*?</a>\s*</li>)'
replacement = r'\1\n' + ch8_link

for fp in files:
    if '08_medlink_existing_ui_augmentation_guide.html' in fp:
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    if '08_medlink_existing_ui_augmentation_guide.html' not in content:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Added Ch8 link to:", fp)
        else:
            print("Pattern not matched in:", fp)
    else:
        print("Already present in:", fp)
