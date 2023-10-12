import fitz  # Import PyMuPDF

def print_pdf_outline(pdf_path):
    pdf_document = fitz.open(pdf_path)
    outline = pdf_document.getToC(simple=False)  # Get the document outline (Table of Contents)
    pdf_document.close()

    for item in outline:
        level, title, page, dest = item
        print(f'Level: {level}, Title: {title}, Page: {page}')


pdf_path = '/Users/davidallan/Desktop/Lund/böcker/Ralph-Stair-George-Reynolds-Thomas-Chesney-Principles-of-Business-Information-Systems-2020-Cengage-Learning-EMEA-libgen.li_compressed-1.pdf'
print_pdf_outline(pdf_path)
