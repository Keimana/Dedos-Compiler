import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from lexer import DEDOSLexicalAnalyzer
from parser import DEDOSParser  # Import your PLY-based parser

class LexerGUI:
    def __init__(self, master, analysis_type):
        self.master = master
        self.analysis_type = analysis_type
        master.title(f"DEDOS {analysis_type} Analyzer")
        master.geometry("900x600")

        # Configure grid layout for responsiveness
        master.grid_columnconfigure(0, weight=2, uniform="equal")
        master.grid_columnconfigure(1, weight=3, uniform="equal")
        master.grid_columnconfigure(2, weight=2, uniform="equal")
        master.grid_columnconfigure(3, weight=3, uniform="equal")
        master.grid_columnconfigure(4, weight=2, uniform="equal")
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=3)
        master.grid_rowconfigure(2, weight=2)
        master.grid_rowconfigure(3, weight=1)

        # Buttons for different analyzers
        analyzer_button_frame = tk.Frame(master, bg="#333333")
        analyzer_button_frame.grid(row=12, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

        lexical_button = self.create_rounded_button(analyzer_button_frame, "Run Lexical Analyzer", self.analyze_code, "#007acc", "white", ("Arial", 10))
        lexical_button.pack(side=tk.LEFT, padx=10)

        syntax_button = self.create_rounded_button(analyzer_button_frame, "Run Syntax Analyzer", self.analyze_syntax, "#007acc", "white", ("Arial", 10))
        syntax_button.pack(side=tk.LEFT, padx=10)

        semantic_button = self.create_rounded_button(analyzer_button_frame, "Semantic Analyzer", self.analyze_semantics, "#007acc", "white", ("Arial", 10))
        semantic_button.pack(side=tk.LEFT, padx=10)

        # Buttons for file import/export
        import_button = self.create_rounded_button(analyzer_button_frame, "Import File", self.import_file, "#007acc", "white", ("Arial", 10))
        import_button.pack(side=tk.LEFT, padx=10)

        export_button = self.create_rounded_button(analyzer_button_frame, "Export Results", self.export_file, "#007acc", "white", ("Arial", 10))
        export_button.pack(side=tk.LEFT, padx=10)

        # Input Code Frame
        input_frame = tk.Frame(master, bg="#333333")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        # Code Input Box
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Error Output
        self.errors_list = tk.Listbox(master, bg="#1e1e1e", fg="white", font=("Consolas", 10), height=10)
        self.errors_list.grid(row=2, column=0, columnspan=5, padx=6, pady=5, sticky="nsew")

        # Tokens Panel
        tokens_frame = ttk.LabelFrame(master, text="Tokens")
        tokens_frame.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")
        self.tokens_list = tk.Listbox(tokens_frame, width=40)
        self.tokens_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Lexemes Panel
        lexemes_frame = ttk.LabelFrame(master, text="Lexemes")
        lexemes_frame.grid(row=1, column=4, padx=10, pady=5, sticky="nsew")
        self.lexemes_list = tk.Listbox(lexemes_frame, width=40)
        self.lexemes_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Apply Dark Mode by Default
        self.apply_dark_mode()

        # Bind Ctrl+F to the find_text function
        self.master.bind("<Control-f>", self.open_find_dialog)

    def create_rounded_button(self, parent, text, command, bg, fg, font):
        """Creates a rounded button with a hover effect."""
        button = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            command=command,
            relief="flat",  # Remove the border
            borderwidth=0,
            padx=20,
            pady=12,
            highlightthickness=0,
            bd=0,  # Remove the border thickness to make the button smoother
            activebackground=bg,  # Maintain background color when clicked
            activeforeground=fg   # Maintain foreground color when clicked
        )
        
        button.config(
            highlightthickness=0,  # Remove outline on click
            relief="solid",        # Set the border relief to solid for rounded look
        )

        def on_enter(e):
            button.config(bg="#005f8c", fg="white")  # Hover color

        def on_leave(e):
            button.config(bg=bg, fg=fg)  # Default color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def apply_dark_mode(self):
        """Apply dark mode theme."""
        self.master.config(bg="#333333")
        self.code_input.config(bg="#1e1e1e", fg="white", insertbackground="white")
        self.errors_list.config(bg="#1e1e1e", fg="white")
        self.tokens_list.config(bg="#1e1e1e", fg="white")
        self.lexemes_list.config(bg="#1e1e1e", fg="white")

    def open_find_dialog(self, event=None):
        """Open the Find text dialog."""
        find_dialog = tk.Toplevel(self.master)
        find_dialog.title("Find Text")
        find_dialog.geometry("400x100")
        
        # Add a label for the search term
        label = tk.Label(find_dialog, text="Find:")
        label.pack(padx=10, pady=5)
        
        # Add an entry field for user to type the text they want to find
        self.find_entry = tk.Entry(find_dialog, font=("Arial", 12))
        self.find_entry.pack(padx=10, pady=5)
        
        # Add a button to trigger the search
        search_button = tk.Button(find_dialog, text="Find", command=self.find_text)
        search_button.pack(pady=5)

        # Focus the entry field
        self.find_entry.focus_set()

    def find_text(self):
        """Find text in the input field."""
        search_text = self.find_entry.get()
        start_pos = '1.0'
        self.code_input.tag_remove("highlight", "1.0", "end")  # Remove previous highlights
        
        while True:
            start_pos = self.code_input.search(search_text, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_text)}c"
            self.code_input.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        self.code_input.tag_config("highlight", background="yellow", foreground="black")

    def run_analysis(self):
        """Run the selected analysis based on the mode chosen at startup."""
        if self.analysis_type == "Lexical":
            self.analyze_code()
        elif self.analysis_type == "Syntax":
            self.analyze_syntax()
        elif self.analysis_type == "Semantic":
            self.analyze_semantics()

    def analyze_code(self):
        """Run Lexical Analysis"""
        self.tokens_list.delete(0, tk.END)
        self.lexemes_list.delete(0, tk.END)
        self.errors_list.delete(0, tk.END)

        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Input Error", "Please enter some code to analyze!")
            return

        # Initialize the lexer
        lexer = DEDOSLexicalAnalyzer(code)
        lexer.getNextTokens()

        # Display tokens (types) in the "Tokens" list box
        for token in lexer.tokens:
            if " : " in token:  # Ensure token contains " : " before splitting
                token_type, token_value = token.split(" : ")
                self.tokens_list.insert(tk.END, token_type)  # Display token type in "Tokens"
                self.lexemes_list.insert(tk.END, token_value)  # Display token value (lexeme) in "Lexemes"
            else:
                # If the token doesn't have the expected format, display it as is
                self.tokens_list.insert(tk.END, token)
                self.lexemes_list.insert(tk.END, token)  # Display the same token for lexeme as fallback

        # Display errors in the "Errors" list box
        for error in lexer.tokensForUnknown:
            self.errors_list.insert(tk.END, error)

    def import_file(self):
        """Open a file dialog to import a code file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.code_input.delete(1.0, tk.END)  # Clear existing input
                self.code_input.insert(tk.END, code)  # Insert imported code into the input field

    def export_file(self):
        """Export the results to a text file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                # Collect tokens, lexemes, and errors
                output = ""
                for token in self.tokens_list.get(0, tk.END):
                    output += f"Token: {token}\n"
                for lexeme in self.lexemes_list.get(0, tk.END):
                    output += f"Lexeme: {lexeme}\n"
                for error in self.errors_list.get(0, tk.END):
                    output += f"Error: {error}\n"
                file.write(output)  # Write to the file

    def analyze_syntax(self):
        """Run Syntax Analysis and display errors in GUI."""
        self.errors_list.delete(0, tk.END)  # Clear previous errors

        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Input Error", "Please enter some code to analyze!")
            return

        lexer = DEDOSLexicalAnalyzer(code)
        lexer.getNextTokens()

        # Pass the lexer-generated tokens to the parser
        parser = DEDOSParser(lexer.tokens)
        parser.parse()

        # Display syntax errors in the GUI
        if parser.errors_list:
            for error in parser.errors_list:
                self.errors_list.insert(tk.END, error)
        else:
            self.errors_list.insert(tk.END, "No Syntax Errors Found ✅")

    def analyze_semantics(self):
        """Run Semantic Analysis (Placeholder)"""
        messagebox.showinfo("Semantic Analyzer", "Semantic Analysis is under development")

def choose_analysis():
    """Prompt the user to select analysis type before launching the main GUI."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create a Toplevel window (modal dialog)
    dialog = tk.Toplevel(root)
    dialog.title("Choose Analysis Type")
    dialog.geometry("300x200")

    def select_lexical():
        selected_mode = "Lexical"
        dialog.destroy()  # Close the dialog
        main(selected_mode)

    def select_syntax():
        selected_mode = "Syntax"
        dialog.destroy()  # Close the dialog
        main(selected_mode)

    def select_semantic():
        selected_mode = "Semantic"
        dialog.destroy()  # Close the dialog
        main(selected_mode)

    # Add buttons for each analysis type
    lexical_button = tk.Button(dialog, text="Lexical Analysis", command=select_lexical, width=20)
    lexical_button.pack(pady=10)

    syntax_button = tk.Button(dialog, text="Syntax Analysis", command=select_syntax, width=20)
    syntax_button.pack(pady=10)

    semantic_button = tk.Button(dialog, text="Semantic Analysis", command=select_semantic, width=20)
    semantic_button.pack(pady=10)

    dialog.mainloop()

def main(selected_mode):
    """Launch the GUI with the selected analysis mode."""
    root = tk.Tk()
    app = LexerGUI(root, selected_mode)
    root.mainloop()

if __name__ == "__main__":
    choose_analysis()

def main(selected_mode):
    """Launch the GUI with the selected analysis mode."""
    root = tk.Tk()
    app = LexerGUI(root, selected_mode)
    root.mainloop()

if __name__ == "__main__":
    choose_analysis()
