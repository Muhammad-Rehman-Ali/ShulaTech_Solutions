import os
from tkinter import Tk, filedialog, Button, Label, messagebox, Frame
from PyPDF2 import PdfReader, PdfWriter

class PDFTool:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger & Splitter")
        self.root.geometry("400x250")
        self.root.configure(bg="#2C3E50")

        # Frame for buttons
        self.frame = Frame(root, bg="#2C3E50")
        self.frame.pack(pady=20)

        # Merge Button
        self.merge_button = Button(self.frame, text="Merge PDFs", command=self.merge_pdfs, width=20, bg="#3498DB", fg="white", font=("Arial", 12, "bold"))
        self.merge_button.pack(pady=10)

        # Split Button
        self.split_button = Button(self.frame, text="Split PDF", command=self.split_pdf, width=20, bg="#E74C3C", fg="white", font=("Arial", 12, "bold"))
        self.split_button.pack(pady=10)

        # Label for feedback
        self.label = Label(root, text="Select an action above to proceed", bg="#2C3E50", fg="white", font=("Arial", 12))
        self.label.pack(pady=20)

    def merge_pdfs(self):
        file_paths = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF files", "*.pdf")])
        if not file_paths:
            return

        pdf_writer = PdfWriter()
        for path in file_paths:
            try:
                pdf_reader = PdfReader(path)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file: {path}\n{e}")
                return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                 title="Save Merged PDF")
        if save_path:
            with open(save_path, "wb") as output_file:
                pdf_writer.write(output_file)
            messagebox.showinfo("Success", "PDFs merged successfully!")

    def split_pdf(self):
        file_path = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        try:
            pdf_reader = PdfReader(file_path)
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if not output_dir:
                return

            for i, page in enumerate(pdf_reader.pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                output_file_path = os.path.join(output_dir, f"Page_{i + 1}.pdf")
                with open(output_file_path, "wb") as output_file:
                    pdf_writer.write(output_file)

            messagebox.showinfo("Success", "PDF split successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error splitting PDF: {e}")

if __name__ == "__main__":
    root = Tk()
    app = PDFTool(root)
    root.mainloop()
