import tkinter as tk
from tkinter import filedialog, ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
from .menu_bar import MenuBar
from utils.pdf_utils import get_pdf_page_size
from controllers.pdf_controller import PDFController

class PDFViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Viewer")

        # Set the clam theme for ttk
        style = ttk.Style()
        style.theme_use('clam')

        # Create the menu bar
        self.menu_bar = MenuBar(master, self)

        # Open a PDF file
        self.filename = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])

        # Open the PDF document using PDFController
        self.pdf_controller = PDFController(self.filename)
        
        # Get the size of the first page
        width, height = get_pdf_page_size(self.pdf_controller.pdf_document, 0)

        # Set the initial window size to match the first page
        self.master.geometry(f"{width}x{height}")

        # Create a Frame to hold the PDF viewer and sidebar
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Create a sidebar frame for thumbnails
        self.sidebar_frame = ttk.Frame(self.main_frame, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a Canvas for the sidebar
        self.sidebar_canvas = tk.Canvas(self.sidebar_frame)
        self.sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create a Scrollbar for the sidebar
        self.sidebar_scrollbar = ttk.Scrollbar(self.sidebar_frame, orient=tk.VERTICAL, command=self.sidebar_canvas.yview)
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Canvas to use the Scrollbar
        self.sidebar_canvas.config(yscrollcommand=self.sidebar_scrollbar.set)
        self.sidebar_canvas.bind('<Configure>', lambda e: self.sidebar_canvas.config(scrollregion=self.sidebar_canvas.bbox('all')))

        # Create a Frame inside the Canvas to hold the thumbnails
        self.thumbnails_frame = ttk.Frame(self.sidebar_canvas)
        self.sidebar_canvas.create_window((0, 0), window=self.thumbnails_frame, anchor='nw')

        # Create a Frame to hold the PDF viewer
        self.viewer_frame = ttk.Frame(self.main_frame)
        self.viewer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create a Canvas to display the PDF pages
        self.canvas = tk.Canvas(self.viewer_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create a Scrollbar for the Canvas
        self.scrollbar = ttk.Scrollbar(self.viewer_frame, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Canvas to use the Scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.resize_canvas)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # For macOS
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # For macOS

        # Bind mouse wheel events for the sidebar
        self.sidebar_canvas.bind_all("<MouseWheel>", self._on_sidebar_mousewheel)
        self.sidebar_canvas.bind_all("<Button-4>", self._on_sidebar_mousewheel)  # For macOS
        self.sidebar_canvas.bind_all("<Button-5>", self._on_sidebar_mousewheel)  # For macOS

        # Display the first page of the PDF
        self.current_page = 0
        self.display_page()

        # Bind keys for navigation
        self.master.bind('<Left>', self.prev_page)
        self.master.bind('<Right>', self.next_page)

        # Generate thumbnails for the sidebar
        self.generate_thumbnails()

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _on_sidebar_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.sidebar_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.sidebar_canvas.yview_scroll(1, "units")

    def resize_canvas(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if event:
            self.canvas_width = event.width
            self.canvas_height = event.height
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)

    def display_page(self):
        page = self.pdf_controller.get_page(self.current_page)
        img = page.get_pixmap()
        img = Image.frombytes("RGB", [img.width, img.height], img.samples)
        img = ImageTk.PhotoImage(img)
        self.canvas_image = self.canvas.create_image(0, 0, anchor='nw', image=img)
        self.canvas.image = img  # To prevent garbage collection
        self.resize_canvas(None)  # Adjust canvas size

    def prev_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.canvas.delete('all')
            self.display_page()

    def next_page(self, event):
        if self.current_page < self.pdf_controller.get_page_count() - 1:
            self.current_page += 1
            self.canvas.delete('all')
            self.display_page()

    def generate_thumbnails(self):
        for i in range(self.pdf_controller.get_page_count()):
            page = self.pdf_controller.get_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))  # Create a smaller thumbnail
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = ImageTk.PhotoImage(img)
            thumbnail = ttk.Button(self.thumbnails_frame, image=img, command=lambda page=i: self.goto_page(page))
            thumbnail.image = img  # To prevent garbage collection
            thumbnail.pack(side=tk.TOP, fill=tk.X, expand=True)

    def goto_page(self, page):
        self.current_page = page
        self.canvas.delete('all')
        self.display_page()