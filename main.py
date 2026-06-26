import tkinter as tk
from tkinter import ttk, messagebox
import google.generativeai as genai
import threading

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Powered Multilingual Language Translation Tool")
        self.root.geometry("850x600")
        self.root.configure(bg="#f0f0f0")

        # Set up variables
        self.source_lang = tk.StringVar(value="Auto")
        self.target_lang = tk.StringVar(value="English")
        
        
        genai.configure(api_key="AQ.Ab8RN6KZ9aXJ15cy9eSQqJf8JIoWzdKSxD6PnwON0Q7TNaYLuQ")
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.languages = [
            "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chichewa", "Chinese (Simplified)", "Chinese (Traditional)", "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino", "Finnish", "French", "Frisian", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish (Kurmanji)", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar (Burmese)", "Nepali", "Norwegian", "Odia (Oriya)", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
        ]

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="AI Powered Multilingual Language Translation Tool", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        title_label.pack(pady=15)

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Configure columns
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.columnconfigure(2, weight=1)

        # Source Language
        source_frame = tk.Frame(main_frame, bg="#f0f0f0")
        source_frame.grid(row=0, column=0, sticky="nsew", padx=10)
        tk.Label(source_frame, text="Source Language:", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w")
        
        self.source_combo = ttk.Combobox(source_frame, textvariable=self.source_lang, values=["Auto"] + self.languages, state="readonly", font=("Helvetica", 11))
        self.source_combo.pack(fill=tk.X, pady=5)
        
        self.source_text = tk.Text(source_frame, height=15, font=("Helvetica", 12), wrap=tk.WORD, relief=tk.SOLID, borderwidth=1)
        self.source_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Buttons in the middle
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.grid(row=0, column=1, padx=10, pady=30)

        self.translate_btn = tk.Button(btn_frame, text="Translate ➔", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049", command=self.translate_text, width=12, height=2, cursor="hand2")
        self.translate_btn.pack(pady=20)

        self.clear_btn = tk.Button(btn_frame, text="Clear Fields", font=("Helvetica", 12), bg="#f44336", fg="white", activebackground="#e53935", command=self.clear_fields, width=12, cursor="hand2")
        self.clear_btn.pack(pady=10)

        # Target Language
        target_frame = tk.Frame(main_frame, bg="#f0f0f0")
        target_frame.grid(row=0, column=2, sticky="nsew", padx=10)
        tk.Label(target_frame, text="Target Language:", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w")

        self.target_combo = ttk.Combobox(target_frame, textvariable=self.target_lang, values=self.languages, state="readonly", font=("Helvetica", 11))
        self.target_combo.pack(fill=tk.X, pady=5)

        self.target_text = tk.Text(target_frame, height=15, font=("Helvetica", 12), wrap=tk.WORD, state=tk.DISABLED, relief=tk.SOLID, borderwidth=1, bg="#e8e8e8")
        self.target_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.copy_btn = tk.Button(target_frame, text="Copy Translated Text", font=("Helvetica", 11), bg="#2196F3", fg="white", activebackground="#1e88e5", command=self.copy_text, cursor="hand2")
        self.copy_btn.pack(anchor="e", pady=5)

    def translate_text(self):
        text_to_translate = self.source_text.get("1.0", tk.END).strip()
        source = self.source_lang.get()
        target = self.target_lang.get()

        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
            
        if not target:
            messagebox.showwarning("Input Error", "Please select a target language.")
            return

        self.translate_btn.config(text="Translating...", state=tk.DISABLED)
        
        # Run translation in a separate thread to keep UI responsive
        threading.Thread(target=self._perform_translation, args=(text_to_translate, source, target), daemon=True).start()

    def _perform_translation(self, text, source, target):
        try:
            prompt = f"Translate the following text from {source} to {target}. Only return the translated text without any conversational filler or quotes.\n\nText: {text}"
            response = self.model.generate_content(prompt)
            translated = response.text.strip()
            
            # Update UI from main thread
            self.root.after(0, self._update_target_text, translated)
        except Exception as e:
            self.root.after(0, self._handle_translation_error, str(e))
        finally:
            self.root.after(0, lambda: self.translate_btn.config(text="Translate ➔", state=tk.NORMAL))

    def _update_target_text(self, translated_text):
        self.target_text.config(state=tk.NORMAL)
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert(tk.END, translated_text)
        self.target_text.config(state=tk.DISABLED)

    def _handle_translation_error(self, error_msg):
        messagebox.showerror("Translation Error", f"An error occurred during translation:\n{error_msg}")

    def clear_fields(self):
        self.source_text.delete("1.0", tk.END)
        self.target_text.config(state=tk.NORMAL)
        self.target_text.delete("1.0", tk.END)
        self.target_text.config(state=tk.DISABLED)

    def copy_text(self):
        translated = self.target_text.get("1.0", tk.END).strip()
        if translated:
            self.root.clipboard_clear()
            self.root.clipboard_append(translated)
            self.root.update() # keep the clipboard updated
            messagebox.showinfo("Copied", "Translated text copied to clipboard!")
        else:
            messagebox.showwarning("Copy Error", "No translated text to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()