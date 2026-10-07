import fitz # PyMuPDF
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"c:\__MEDLINK___\PMG\extracted_data\normative_docs"
files = ["pmg-2026.pdf", "Додаток-1.pdf", "Додаток-2.pdf"]

for fn in files:
    path = os.path.join(pdf_dir, fn)
    if not os.path.exists(path):
        continue
    doc = fitz.open(path)
    print(f"\n=======================================================")
    print(f"PDF DOCUMENT: {fn} (Pages: {len(doc)})")
    print(f"=======================================================")
    
    # Print first 2 pages text
    for page_num in range(min(3, len(doc))):
        page = doc[page_num]
        txt = page.get_text()
        print(f"\n--- Page {page_num + 1} ---")
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        for l in lines[:15]:
            print(" ", l)

    # Search for titles, orders, decrees in the document
    toc = doc.get_toc()
    if toc:
        print("\nTable of Contents (sample):")
        for item in toc[:10]:
            print(" ", item)
