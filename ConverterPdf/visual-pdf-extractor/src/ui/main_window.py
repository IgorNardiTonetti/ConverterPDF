from tkinter import Tk, Frame, Label, Button, Text, filedialog, messagebox
import threading
from core.pdf_utils import extract_pages 

class MainWindow:
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

        self.pages_text = Text(self.frame, height=10, width=50)
        self.pages_text.pack(pady=10)

        self.extract_button = Button(self.frame, text="Extract Pages", command=self.start_extraction_thread)
        self.extract_button.pack(pady=10)

        self.status_label = Label(self.frame, text="", fg="green")
        self.status_label.pack(pady=10)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.status_label.config(text=f"Selected: {self.pdf_path}")

    def start_extraction_thread(self):
        if not hasattr(self, 'pdf_path'):
            messagebox.showerror("Error", "Please select a PDF file first.")
            return

        self.extract_button.config(state="disabled", text="Extracting...")
        self.status_label.config(text="Extracting pages...")
        thread = threading.Thread(target=self.extract_pages)
        thread.start()

    def extract_pages(self):
        try:
            pages = extract_pages(self.pdf_path)  
            self.pages_text.delete("1.0", "end")
            for page in pages:
                self.pages_text.insert("end", f"{page}\n")
            self.status_label.config(text="Extraction completed!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.extract_button.config(state="normal", text="Extract Pages")

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()