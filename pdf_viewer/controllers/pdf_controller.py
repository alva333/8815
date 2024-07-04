import fitz  # PyMuPDF

class PDFController:
    def __init__(self, filename):
        self.pdf_document = fitz.open(filename)

    def get_page_count(self):
        return len(self.pdf_document)

    def get_page(self, page_number):
        return self.pdf_document.load_page(page_number)
