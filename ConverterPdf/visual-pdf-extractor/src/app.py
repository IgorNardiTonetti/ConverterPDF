from tkinter import Tk, Frame, Button, Label, filedialog, messagebox, Text
from core.pdf_utils import extract_pages, save_extracted_pdfs

class PDFExtractorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Visual PDF Extractor")
        self.master.geometry("600x400")

        self.frame = Frame(self.master)
        self.frame.pack(pady=20)

        self.label = Label(self.frame, text="Select a PDF file to extract pages:")
        self.label.pack(pady=10)

        self.select_button = Button(self.frame, text="Select PDF", command=self.select_pdf)
        self.select_button.pack(pady=10)

        self.page_input = Text(self.frame, height=5, width=50)
        self.page_input.pack(pady=10)

        self.extract_button = Button(self.frame, text="Extract Pages", command=self.extract_pages)
        self.extract_button.pack(pady=10)

        self.status_label = Label(self.frame, text="", fg="green")
        self.status_label.pack(pady=10)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.label.config(text=f"Selected: {self.pdf_path}")

    def extract_pages(self):
        pages = self.page_input.get("1.0", "end").strip()
        if not pages:
            messagebox.showerror("Error", "Please enter pages to extract.")
            return

        try:
            extracted_pdfs = extract_pages(self.pdf_path, pages)
            save_extracted_pdfs(extracted_pdfs)
            self.status_label.config(text="Extraction successful!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    app = PDFExtractorApp(root)
    root.mainloop()