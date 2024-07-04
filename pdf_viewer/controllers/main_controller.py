from models.pdf_viewer import PDFViewer

class MainController:
    def __init__(self, master):
        self.pdf_viewer = PDFViewer(master)
