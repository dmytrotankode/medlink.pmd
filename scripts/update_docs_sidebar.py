import re, glob

files = [
    r'c:\__MEDLINK___\PMG\docs_html\01_database_schema.html',
    r'c:\__MEDLINK___\PMG\docs_html\02_api_endpoints.html',
    r'c:\__MEDLINK___\PMG\docs_html\03_business_logic_and_math.html',
    r'c:\__MEDLINK___\PMG\docs_html\04_openxml_processor.html',
    r'c:\__MEDLINK___\PMG\docs_html\05_frontend_integration_guide.html',
    r'c:\__MEDLINK___\PMG\docs_html\06_pmg_dictionaries_catalog.html'
]

pattern = r'(<a href="06_pmg_dictionaries_catalog\.html">[\s\S]*?</a>\s*</li>)'

replacement = r'''\1
      <li class="nav-item">
        <a href="07_nszu_file_analysis_literal_compliance.html"><i class="material-icons">verified</i> 7. Аудит відповідності (info-pmg)</a>
      </li>'''

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    if '07_nszu_file_analysis_literal_compliance.html' not in content:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('Successfully updated:', fp)
        else:
            print('No match for:', fp)
    else:
        print('Already present in:', fp)
