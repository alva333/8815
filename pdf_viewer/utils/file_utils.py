import os

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

def is_pdf_file(filename):
    return get_file_extension(filename).lower() == '.pdf'