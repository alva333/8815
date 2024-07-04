import fitz  # PyMuPDF

def get_pdf_page_count(pdf_document):
    return len(pdf_document)

def get_pdf_page_size(pdf_document, page_number):
    page = pdf_document.load_page(page_number)
    return page.get_pixmap().width, page.get_pixmap().height