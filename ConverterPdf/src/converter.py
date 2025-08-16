import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
import fitz  


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ModernPdfToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

       
        self.title("Super Ferramenta PDF v1.2")
        self.geometry("1000x750")
        self.resizable(True, True)

      
        self.tab_view = ctk.CTkTabview(self, width=950, height=700)
        self.tab_view.pack(pady=20, padx=20, fill="both", expand=True)

        self.tab_converter = self.tab_view.add("🖼️ Converter Imagens")
        self.tab_merger = self.tab_view.add("📚 Juntar PDFs")
        self.tab_unlocker = self.tab_view.add("🔓 Desbloquear PDF")
        self.tab_extractor = self.tab_view.add("📄 Extrair Páginas")

        
        self.merger_items = [] 
        self.selected_merger_index = None
        
        self.extractor_pdf_path = None
        self.extractor_page_vars = []
        self.extractor_page_widgets = []

        # --- Inicialização das abas ---
        self.setup_converter_tab()
        self.setup_merger_tab()
        self.setup_unlocker_tab()
        self.setup_extractor_tab()

    def log_message(self, textbox, message):
        """Adiciona uma mensagem a uma caixa de texto de status."""
        textbox.configure(state="normal")
        textbox.insert("end", message + "\n")
        textbox.configure(state="disabled")
        textbox.see("end")

    # =================================================================================
    # --- ABA 1: CONVERSOR DE IMAGENS 
    # =================================================================================
    def setup_converter_tab(self):
       
        self.tab_converter.grid_columnconfigure(0, weight=1)
        self.tab_converter.grid_rowconfigure(2, weight=1)

        
        select_frame = ctk.CTkFrame(self.tab_converter)
        select_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        select_frame.grid_columnconfigure(1, weight=1)

        self.converter_path_var = ctk.StringVar(value="Nenhuma pasta selecionada.")
        select_btn = ctk.CTkButton(select_frame, text="Selecionar Pasta", width=150, command=self.select_folder_for_conversion)
        select_btn.grid(row=0, column=0, padx=10, pady=10)
        path_label = ctk.CTkLabel(select_frame, textvariable=self.converter_path_var, anchor="w")
        path_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

       
        self.delete_images_var = ctk.StringVar(value="off")
        delete_checkbox = ctk.CTkCheckBox(select_frame, text="Excluir imagens após conversão", variable=self.delete_images_var, onvalue="on", offvalue="off")
        delete_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

       
        self.converter_start_btn = ctk.CTkButton(self.tab_converter, text="Converter Imagens para PDF", height=40, command=self.start_conversion_thread)
        self.converter_start_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

       
        self.converter_status_box = ctk.CTkTextbox(self.tab_converter, state="disabled", font=("Consolas", 12))
        self.converter_status_box.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

    def select_folder_for_conversion(self):
        directory = filedialog.askdirectory()
        if directory:
            self.converter_path_var.set(directory)
            self.log_message(self.converter_status_box, f"Pasta selecionada: {directory}")

    def start_conversion_thread(self):
        dir_path = self.converter_path_var.get()
        if not os.path.isdir(dir_path):
            messagebox.showerror("Erro", "Por favor, selecione uma pasta válida.")
            return
        delete_images = self.delete_images_var.get() == "on"
        threading.Thread(target=self.process_conversion, args=(dir_path, delete_images), daemon=True).start()

    def process_conversion(self, directory_path, delete_images=False):
        self.log_message(self.converter_status_box, "Iniciando conversão...")
        self.converter_start_btn.configure(state="disabled")
        
        image_files = sorted([f for f in os.listdir(directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
        if not image_files:
            self.log_message(self.converter_status_box, "Nenhuma imagem encontrada na pasta.")
            self.converter_start_btn.configure(state="normal")
            return

        try:
            output_filename = os.path.join(directory_path, "convertido.pdf")
            
            first_image_path = os.path.join(directory_path, image_files[0])
            first_image = Image.open(first_image_path).convert("RGB")
            
            other_images = []
            for i in range(1, len(image_files)):
                img_path = os.path.join(directory_path, image_files[i])
                img = Image.open(img_path).convert("RGB")
                other_images.append(img)

            first_image.save(output_filename, save_all=True, append_images=other_images)
            self.log_message(self.converter_status_box, f"PDF '{os.path.basename(output_filename)}' criado com sucesso com {len(image_files)} imagens.")

            if delete_images:
                self.log_message(self.converter_status_box, "Excluindo imagens originais...")
                for filename in image_files:
                    os.remove(os.path.join(directory_path, filename))
                self.log_message(self.converter_status_box, "Imagens excluídas.")

        except Exception as e:
            self.log_message(self.converter_status_box, f"ERRO na conversão: {e}")

        self.log_message(self.converter_status_box, "Conversão concluída.")
        self.converter_start_btn.configure(state="normal")

    # =================================================================================
    # --- ABA 2: JUNTAR PDFS
    # =================================================================================
    def setup_merger_tab(self):
        self.tab_merger.grid_columnconfigure(0, weight=1)
        self.tab_merger.grid_rowconfigure(1, weight=1)

       
        merger_action_frame = ctk.CTkFrame(self.tab_merger)
        merger_action_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        select_files_btn = ctk.CTkButton(merger_action_frame, text="Adicionar PDFs", command=self.select_files_for_merger)
        select_files_btn.pack(side="left", padx=10, pady=10)

        self.merger_up_btn = ctk.CTkButton(merger_action_frame, text="▲ Mover para Cima", width=140, command=lambda: self.move_merger_item(-1), state="disabled")
        self.merger_up_btn.pack(side="left", padx=5, pady=10)

        self.merger_down_btn = ctk.CTkButton(merger_action_frame, text="▼ Mover para Baixo", width=140, command=lambda: self.move_merger_item(1), state="disabled")
        self.merger_down_btn.pack(side="left", padx=5, pady=10)

        self.merger_remove_btn = ctk.CTkButton(merger_action_frame, text="Remover", command=self.remove_merger_item, state="disabled")
        self.merger_remove_btn.pack(side="left", padx=5, pady=10)

        clear_list_btn = ctk.CTkButton(merger_action_frame, text="Limpar Lista", command=self.clear_merger_list)
        clear_list_btn.pack(side="right", padx=10, pady=10)

      
        self.merger_scrollable_frame = ctk.CTkScrollableFrame(self.tab_merger, label_text="Arraste e organize os PDFs para juntar")
        self.merger_scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

       
        self.merge_btn = ctk.CTkButton(self.tab_merger, text="Juntar PDFs", height=40, command=self.merge_pdfs, state="disabled")
        self.merge_btn.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

    def select_files_for_merger(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if files:
           
            threading.Thread(target=self.load_merger_files, args=(files,), daemon=True).start()

    def load_merger_files(self, files):
        for file_path in files:
            if any(item['path'] == file_path for item in self.merger_items):
                continue 

            try:
                doc = fitz.open(file_path)
                page_count = len(doc)
                
                
                page = doc.load_page(0)
                pix = page.get_pixmap(dpi=72)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail((120, 170), Image.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                doc.close()

                
                item_data = {'path': file_path, 'thumbnail': ctk_img, 'page_count': page_count}
                self.merger_items.append(item_data)
                
            except Exception as e:
                print(f"Erro ao carregar {os.path.basename(file_path)}: {e}")
        
 
        self.after(0, self.update_merger_display)

    def update_merger_display(self):
        
        for item in self.merger_items:
            if 'frame' in item and item['frame'].winfo_exists():
                item['frame'].destroy()

        
        for i, item_data in enumerate(self.merger_items):
            frame = ctk.CTkFrame(self.merger_scrollable_frame)
            
           
            columns = 5
            row = i // columns
            col = i % columns
            frame.grid(row=row, column=col, padx=10, pady=10)

           
            thumb_label = ctk.CTkLabel(frame, image=item_data['thumbnail'], text="")
            thumb_label.pack(padx=5, pady=5)

           
            filename = os.path.basename(item_data['path'])
            if len(filename) > 20:
                filename = filename[:17] + "..."
            name_label = ctk.CTkLabel(frame, text=filename, font=("", 10))
            name_label.pack(padx=5)

            
            pages_label = ctk.CTkLabel(frame, text=f"{item_data['page_count']} páginas", font=("", 9), text_color="gray")
            pages_label.pack(padx=5, pady=(0, 5))

           
            item_data['frame'] = frame
            
            
            frame.bind("<Button-1>", lambda event, index=i: self.select_merger_item(index))
            thumb_label.bind("<Button-1>", lambda event, index=i: self.select_merger_item(index))
            name_label.bind("<Button-1>", lambda event, index=i: self.select_merger_item(index))
            pages_label.bind("<Button-1>", lambda event, index=i: self.select_merger_item(index))

        
        self.update_merger_buttons()
        if self.selected_merger_index is not None and self.selected_merger_index < len(self.merger_items):
             self.select_merger_item(self.selected_merger_index) 
        else:
            self.clear_merger_selection()

    def select_merger_item(self, index):
        
        if self.selected_merger_index is not None and self.selected_merger_index < len(self.merger_items):
            self.merger_items[self.selected_merger_index]['frame'].configure(border_width=0)

        
        self.selected_merger_index = index
        if self.selected_merger_index is not None:
            selected_frame = self.merger_items[self.selected_merger_index]['frame']
            selected_frame.configure(border_width=2, border_color="dodgerblue")
        
        self.update_merger_buttons()

    def update_merger_buttons(self):
        has_selection = self.selected_merger_index is not None
        item_count = len(self.merger_items)

        self.merger_remove_btn.configure(state="normal" if has_selection else "disabled")
        self.merger_up_btn.configure(state="normal" if has_selection and self.selected_merger_index > 0 else "disabled")
        self.merger_down_btn.configure(state="normal" if has_selection and self.selected_merger_index < item_count - 1 else "disabled")
        self.merge_btn.configure(state="normal" if item_count > 1 else "disabled")

    def clear_merger_selection(self):
        if self.selected_merger_index is not None and self.selected_merger_index < len(self.merger_items):
            self.merger_items[self.selected_merger_index]['frame'].configure(border_width=0)
        self.selected_merger_index = None
        self.update_merger_buttons()

    def move_merger_item(self, direction):
        if self.selected_merger_index is None: return
        
        idx = self.selected_merger_index
        new_idx = idx + direction
        
        if 0 <= new_idx < len(self.merger_items):
           
            item = self.merger_items.pop(idx)
            self.merger_items.insert(new_idx, item)
            
            
            self.selected_merger_index = new_idx
            self.update_merger_display()

    def remove_merger_item(self):
        if self.selected_merger_index is None: return
        
        item_to_remove = self.merger_items.pop(self.selected_merger_index)
        if 'frame' in item_to_remove and item_to_remove['frame'].winfo_exists():
            item_to_remove['frame'].destroy()
        
       
        self.clear_merger_selection()
        self.update_merger_display()
    
    def clear_merger_list(self):
        for item in self.merger_items:
            if 'frame' in item and item['frame'].winfo_exists():
                item['frame'].destroy()
        self.merger_items.clear()
        self.clear_merger_selection()
        self.update_merger_display()
    
    def merge_pdfs(self):
        if len(self.merger_items) < 2:
            messagebox.showwarning("Aviso", "Adicione pelo menos dois PDFs para juntar.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path: return

        merger = PdfWriter()
        try:
            pdf_paths = [item['path'] for item in self.merger_items]
            for pdf_path in pdf_paths:
                merger.append(pdf_path)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Sucesso", f"PDFs juntados com sucesso em:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os PDFs:\n{e}")

  
    # ABA 3: DESBLOQUEAR PDF
    def setup_unlocker_tab(self):
        self.tab_unlocker.grid_columnconfigure(0, weight=1)
        self.tab_unlocker.grid_rowconfigure(2, weight=1)

        unlocker_frame = ctk.CTkFrame(self.tab_unlocker)
        unlocker_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.unlocker_files_var = ctk.StringVar(value="Nenhum arquivo selecionado.")
        select_btn = ctk.CTkButton(unlocker_frame, text="Selecionar Arquivos", command=self.select_files_for_unlocking)
        select_btn.pack(side="left", padx=10, pady=10)
        
        self.delete_originals_var = ctk.StringVar(value="off")
        delete_checkbox = ctk.CTkCheckBox(unlocker_frame, text="Excluir originais após desbloqueio", variable=self.delete_originals_var, onvalue="on", offvalue="off")
        delete_checkbox.pack(side="left", padx=20, pady=10)

        self.unlocker_start_btn = ctk.CTkButton(self.tab_unlocker, text="Desbloquear PDFs", height=40, command=self.start_unlock_thread)
        self.unlocker_start_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.unlocker_status_box = ctk.CTkTextbox(self.tab_unlocker, state="disabled", font=("Consolas", 12))
        self.unlocker_status_box.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        
        self.unlocker_input_paths = []

    def select_files_for_unlocking(self):
        files = filedialog.askopenfilenames(title="Selecione os PDFs para desbloquear", filetypes=[("PDF files", "*.pdf")])
        if files:
            self.unlocker_input_paths = files
            self.log_message(self.unlocker_status_box, f"{len(files)} arquivo(s) selecionado(s) para desbloqueio.")

    def start_unlock_thread(self):
        if not self.unlocker_input_paths:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
            return
        delete_originals = self.delete_originals_var.get() == "on"
        threading.Thread(target=self.process_unlocking, args=(self.unlocker_input_paths, delete_originals), daemon=True).start()

    def process_unlocking(self, input_paths, delete_originals):
        self.unlocker_start_btn.configure(state="disabled")
        self.log_message(self.unlocker_status_box, "Iniciando processo de desbloqueio...")
        sucessos, erros = 0, 0

        for input_path in input_paths:
            filename = os.path.basename(input_path)
            self.log_message(self.unlocker_status_box, f"Processando '{filename}'...")
            try:
                reader = PdfReader(input_path)
                writer = PdfWriter()

                if reader.is_encrypted:
                    
                    if reader.decrypt('') != 1:
                        self.log_message(self.unlocker_status_box, f"  ❌ ERRO: Falha ao descriptografar '{filename}'. Senha incorreta ou arquivo corrompido.")
                        erros += 1
                        continue
                
                for page in reader.pages:
                    writer.add_page(page)

                base, ext = os.path.splitext(input_path)
                output_path = f"{base}_desbloqueado.pdf"
                
                with open(output_path, "wb") as out_file:
                    writer.write(out_file)
                
                self.log_message(self.unlocker_status_box, f"  ✅ SUCESSO: '{filename}' salvo como '{os.path.basename(output_path)}'.")
                sucessos += 1

                if delete_originals:
                    os.remove(input_path)
                    self.log_message(self.unlocker_status_box, f"  - Original '{filename}' excluído.")

            except Exception as e:
                self.log_message(self.unlocker_status_box, f"  ❌ ERRO Inesperado com '{filename}': {e}")
                erros += 1
        
        self.log_message(self.unlocker_status_box, f"\nProcesso finalizado. Sucessos: {sucessos}, Erros: {erros}.")
        self.unlocker_start_btn.configure(state="normal")
        self.unlocker_input_paths = []

    
    # ABA 4: EXTRAIR PÁGINAS
    def setup_extractor_tab(self):
        self.tab_extractor.grid_columnconfigure(0, weight=1)
        self.tab_extractor.grid_rowconfigure(1, weight=1)

        
        top_frame = ctk.CTkFrame(self.tab_extractor)
        top_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        select_btn = ctk.CTkButton(top_frame, text="Selecionar PDF", command=self.select_pdf_for_extraction)
        select_btn.pack(side="left", padx=10, pady=10)

        self.extractor_filename_label = ctk.CTkLabel(top_frame, text="Nenhum PDF selecionado.", anchor="w")
        self.extractor_filename_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)

       
        self.scrollable_frame = ctk.CTkScrollableFrame(self.tab_extractor, label_text="Páginas do PDF")
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
       
        bottom_frame = ctk.CTkFrame(self.tab_extractor)
        bottom_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.extract_btn = ctk.CTkButton(bottom_frame, text="Extrair Páginas Selecionadas", height=40, command=self.extract_selected_pages, state="disabled")
        self.extract_btn.pack(pady=10, fill="x", expand=True)

    def select_pdf_for_extraction(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not filepath:
            return

        self.extractor_pdf_path = filepath
        self.extractor_filename_label.configure(text=os.path.basename(filepath))
        self.extract_btn.configure(state="disabled") 
        
        for widget in self.extractor_page_widgets:
            widget.destroy()
        self.extractor_page_widgets = []
        self.extractor_page_vars = []

        threading.Thread(target=self.load_and_display_thumbnails, daemon=True).start()

    def load_and_display_thumbnails(self):
        try:
            doc = fitz.open(self.extractor_pdf_path)
            
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=72)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail((100, 141), Image.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                self.after(0, self.create_page_widget, i, ctk_img)

            doc.close()
            self.after(0, lambda: self.extract_btn.configure(state="normal"))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erro", f"Não foi possível carregar o PDF: {e}"))
            self.after(0, lambda: self.extractor_filename_label.configure(text="Falha ao carregar PDF."))

    def create_page_widget(self, page_index, ctk_image):
        page_frame = ctk.CTkFrame(self.scrollable_frame)
        
        columns = 6 
        row = len(self.extractor_page_widgets) // columns
        col = len(self.extractor_page_widgets) % columns
        page_frame.grid(row=row, column=col, padx=5, pady=5)

        page_label = ctk.CTkLabel(page_frame, image=ctk_image, text="")
        page_label.pack(padx=5, pady=5)

        check_var = ctk.StringVar(value="off")
        checkbox = ctk.CTkCheckBox(page_frame, text=f"Pág. {page_index + 1}", variable=check_var, onvalue="on", offvalue="off")
        checkbox.pack(padx=5, pady=(0, 5))

        self.extractor_page_vars.append(check_var)
        self.extractor_page_widgets.append(page_frame)

    def extract_selected_pages(self):
        selected_pages = [i for i, var in enumerate(self.extractor_page_vars) if var.get() == "on"]

        if not selected_pages:
            messagebox.showwarning("Aviso", "Nenhuma página selecionada para extração.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{os.path.splitext(os.path.basename(self.extractor_pdf_path))[0]}_extraido.pdf"
        )

        if not output_path:
            return

        try:
            reader = PdfReader(self.extractor_pdf_path)
            writer = PdfWriter()
            for page_num in selected_pages:
                writer.add_page(reader.pages[page_num])
            
            with open(output_path, "wb") as f:
                writer.write(f)
            
            messagebox.showinfo("Sucesso", f"Páginas extraídas com sucesso para:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a extração:\n{e}")


if __name__ == "__main__":
    app = ModernPdfToolApp()
    app.mainloop()