import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from lexer import DEDOSLexicalAnalyzer
from Syntax import DEDOSParser  # Import your PLY-based parser
import Semantic
class LexerGUI:
    def __init__(self, master):
        self.master = master
        master.geometry("1400x600")

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

        # ✅ First, define `analyzer_button_frame`
        analyzer_button_frame = tk.Frame(master, bg="#333333")
        analyzer_button_frame.grid(row=12, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

        # ✅ Now, define `self.syntax_button` after `analyzer_button_frame`
        self.syntax_button = self.create_rounded_button(analyzer_button_frame, "Run Syntax Analyzer", self.analyze_syntax, "#007acc", "white", ("Arial", 10))
        self.syntax_button.pack(side=tk.LEFT, padx=10)
        self.syntax_button.configure(state="disabled")  # Initially disabled

        self.semantic_button = self.create_rounded_button(analyzer_button_frame, "Semantic Analyzer", self.analyze_semantics, "#007acc", "white", ("Arial", 10))
        self.semantic_button.pack(side=tk.LEFT, padx=10)
        self.semantic_button.configure(state="disabled")  # Initially disabled

        # ✅ Now, define other buttons in `analyzer_button_frame`
        lexical_button = self.create_rounded_button(analyzer_button_frame, "Run Lexical Analyzer", self.analyze_code, "#007acc", "white", ("Arial", 10))
        lexical_button.pack(side=tk.LEFT, padx=10)

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
        # Input Frame with Line Numbers
        
        input_frame = tk.Frame(master, bg="#333333")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        # Line Number Panel
        self.line_numbers = tk.Text(input_frame, width=4, padx=5, bg="#1e1e1e", fg="white", state="disabled", font=("Arial", 12))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Code Input Box
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
        self.code_input.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Bind events to update line numbers
        self.code_input.bind("<KeyRelease>", self.update_line_numbers)
        self.code_input.bind("<MouseWheel>", self.sync_scroll)
        self.code_input.bind("<Configure>", self.update_line_numbers)


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
    
    def update_line_numbers(self, event=None):
        """Update line numbers dynamically."""
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        
        line_count = self.code_input.get("1.0", tk.END).count("\n")  # Count lines
        line_numbers_str = "\n".join(str(i) for i in range(1, line_count + 1))  # Generate numbers

        self.line_numbers.insert("1.0", line_numbers_str)
        self.line_numbers.config(state="disabled")  # Prevent user from modifying it

    def sync_scroll(self, event):
        """Sync scrolling between code input and line numbers."""
        self.line_numbers.yview_moveto(self.code_input.yview()[0])  # Move line numbers

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
        self.lexer = DEDOSLexicalAnalyzer(code)
        self.lexer.getNextTokens()

        # ✅ Correctly assign line numbers
        current_line = 1
        for token in self.lexer.tokens:
            if " : " in token:
                token_type, lexeme_value = token.split(" : ", 1)
                self.tokens_list.insert(tk.END, f"{current_line}. {token_type}")
                self.lexemes_list.insert(tk.END, f"{current_line}. {lexeme_value}")
            else:
                self.tokens_list.insert(tk.END, f"{current_line}. {token}")
                self.lexemes_list.insert(tk.END, f"{current_line}. {token}")

            # ✅ Count new lines based on token content
            if "\n" in lexeme_value:
                current_line += lexeme_value.count("\n")  # Increments based on actual lines
            else:
                current_line += 1  # Default: move to the next line

        # ✅ Display lexical errors properly
        if self.lexer.tokensForUnknown:
            for error in self.lexer.tokensForUnknown:
                self.errors_list.insert(tk.END, error)
            self.syntax_button.configure(state="disabled")
        else:
            self.errors_list.insert(tk.END, "LEXICAL COMPILE SUCCESSFUL ✅")
            self.syntax_button.configure(state="normal")  # Enable syntax analysis



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

        if not hasattr(self, "lexer") or not self.lexer.tokens:
            messagebox.showwarning("Syntax Error", "Run Lexical Analysis First!")
            return

        # Initialize Parser
        self.parser = DEDOSParser(self.lexer.tokens)
        self.parser.ListToDict()
        self.parser.GetNextTerminal()

        syntaxErrors = self.parser.SyntaxErrors

        # Display syntax errors
        if syntaxErrors:
            for error in syntaxErrors:
                self.errors_list.insert(tk.END, error)
            self.semantic_button.configure(state="disabled")
        else:
            self.errors_list.insert(tk.END, "SYNTAX COMPILE SUCCESSFUL ✅")
            self.semantic_button.configure(state="normal")  # Enable semantic analysis

            # Run Semantic Analysis
            self.analyze_semantics()

    def analyze_semantics(self):
        """Run Semantic Analysis"""
        if not hasattr(self, "parser") or not self.parser.SemanticSequence:
            messagebox.showwarning("Semantic Error", "Run Syntax Analysis First!")
            return

        # Initialize Semantic Analyzer
        self.semanticAnalyzer = Semantic.Sem(self.parser.Terminals, self.parser.SemanticSequence)
        self.semanticAnalyzer.keyval_fix()
        self.semanticAnalyzer.token_type()

        output = self.semanticAnalyzer.Output
        errorfound = any("Semantic Error" in item or "Runtime Error" in item for item in output)

        # Display results
        for line in output:
            self.errors_list.insert(tk.END, line)

        if not errorfound:
            self.errors_list.insert(tk.END, "\n✅ SEMANTIC COMPILE SUCCESSFUL")
        else:
            self.errors_list.insert(tk.END, "\n❌ ERRORS FOUND DURING SEMANTIC COMPILATION")


# ===================== Run GUI Without Choose Analysis =====================
def main():
    root = tk.Tk()
    app = LexerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()