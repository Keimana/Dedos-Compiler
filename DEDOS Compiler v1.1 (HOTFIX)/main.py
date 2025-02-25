import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from lexer import DEDOSLexicalAnalyzer
from Syntax import DEDOSParser  # Import your PLY-based parser
import Semantic
class LexerGUI:
    def __init__(self, master):
        self.master = master
        master.geometry("1280x800")
        master.title("DEDOS Compiler")  # Window title
        master.iconbitmap("counterstrikeconditionzero_11724.ico")  # Window icon
        master.resizable(False, False)
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

        # Analyzer Button Frame and buttons (unchanged)...
        analyzer_button_frame = tk.Frame(master, bg="#3c3f59")
        analyzer_button_frame.grid(row=12, column=2, columnspan=5, padx=0, pady=10, sticky="ew")
        self.syntax_button = self.create_rounded_button(analyzer_button_frame, "Run Syntax Analyzer", self.analyze_syntax, "#fb5421", "white", ("Helvetica", 10))
        self.syntax_button.pack(side=tk.LEFT, padx=0)
        self.syntax_button.configure(state="disabled")
        lexical_button = self.create_rounded_button(analyzer_button_frame, "Run Lexical Analyzer", self.analyze_code, "#fb5421", "white", ("Helvetica", 10))
        lexical_button.pack(side=tk.LEFT, padx=5)
        import_button = self.create_rounded_button(analyzer_button_frame, "Import File", self.import_file, "#fb5421", "white", ("Helvetica", 10))
        import_button.pack(side=tk.LEFT, padx=5)
        export_button = self.create_rounded_button(analyzer_button_frame, "Export Results", self.export_file, "#fb5421", "white", ("Helvetica", 10))
        export_button.pack(side=tk.LEFT, padx=5)

        # Input Code Frame (first instance)
        input_frame = tk.Frame(master, bg="#3c3f59")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#161527", fg="#fbb200",
                                                      insertbackground="#fbb200", font=("Helvetica", 12))
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Code Input Box
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#161527", fg="#fbb200", insertbackground="#fbb200", font=("Helvetica", 10))
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Error Output
        self.errors_list = tk.Listbox(master, bg="#161527", fg="#fbb200", font=("Consolas", 10), height=20)
        self.errors_list.grid(row=2, column=0, columnspan=5, padx=6, pady=5, sticky="nsew")

        # Tokens Panel
        tokens_frame = ttk.LabelFrame(master, text="Tokens")
        tokens_frame.grid(row=1, column=3, padx=0, pady=5, sticky="nsew")
        self.tokens_list = tk.Listbox(tokens_frame, width=40)
        self.tokens_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Lexemes Panel
        lexemes_frame = ttk.LabelFrame(master, text="Lexemes")
        lexemes_frame.grid(row=1, column=4, padx=0, pady=5, sticky="nsew")
        self.lexemes_list = tk.Listbox(lexemes_frame, width=40)
        self.lexemes_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Apply Dark Mode by Default
        self.apply_dark_mode()

        # Bind Ctrl+F to the find_text function
        self.master.bind("<Control-f>", self.show_find_bar)
        # Bind Esc to close the find bar if it's open
        self.master.bind("<Escape>", self.hide_find_bar)

        # Find bar frame (hidden by default)
        self.find_frame = None
        # --- Input Frame with Line Numbers ---
        input_frame = tk.Frame(master, bg="#3c3f59")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
        self.line_numbers = tk.Text(input_frame, width=3, padx=5, bg="#161527",
                                     fg="#fbb200", state="disabled", font=("Helvetica", 14))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        # Create the final code input widget (this one will be used)
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#161527", fg="#fbb200",
                                                      insertbackground="#fbb200", font=("Helvetica", 14))
        self.code_input.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Bind events to update line numbers and sync scrolling
        self.code_input.bind("<KeyRelease>", self.update_line_numbers)
        self.code_input.bind("<MouseWheel>", self.sync_scroll)
        self.code_input.bind("<Configure>", self.update_line_numbers)
        self.code_input.bind("<KeyRelease>", self.highlight_words, add="+")


    def highlight_words(self, event=None):
        """Highlight multiple groups of words in different colors."""
        # Define groups: each key is a tag name, and each value is (list of words, color)
        highlight_groups = {
            "group1": (["defuse", "in", "not"], "#F93827"),
            "group2": (["inst", "flank", "chat", "strike"], "#5cffe4"),
            "group3": (["abort", "back", "push", "perim"], "#aeac95"),
            "group4": (["plant", "info"], "#FFD65A"),
            "group5": (["re", "reload", "load"], "#ff1377"),
            "group6": (["force"], "#F3CFC6"),
            "group7": (["+", "-", "/", "*", "="], "#ffffff"),
            "group8": (["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], "#d6fa51"),
            "group9": (["~"], "#16C47F"),
            "group10": (["(", ")", "[", "{", "}", "]", "'", '"'], "white")
        }
        # For each group, remove old highlights and configure the tag
        for tag, (words, color) in highlight_groups.items():
            self.code_input.tag_remove(tag, "1.0", tk.END)
            self.code_input.tag_config(tag, foreground=color)
            # For each word, search and add the tag
            for word in words:
                start_pos = "1.0"
                while True:
                    start_pos = self.code_input.search(word, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(word)}c"
                    self.code_input.tag_add(tag, start_pos, end_pos)
                    start_pos = end_pos

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
            button.config(bg="#303358", fg="#fbb200")  # Hover color

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
        self.master.config(bg="#3c3f59")
        self.code_input.config(bg="#161527", fg="#fbb200", insertbackground="#fbb200")
        self.errors_list.config(bg="#161527", fg="#fbb200")
        self.tokens_list.config(bg="#161527", fg="#fbb200")
        self.lexemes_list.config(bg="#161527", fg="#fbb200")

    def show_find_bar(self, event=None):
        """Display the find bar at the top like in VS Code."""
        if self.find_frame and self.find_frame.winfo_exists():
            # If already open, bring focus to the entry
            self.find_entry.focus_set()
            return

        # Create the find bar frame using grid (since master uses grid)
        self.find_frame = tk.Frame(self.master, bg="#2c2c2c")
        self.find_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=5, pady=5)

        label = tk.Label(self.find_frame, text="Find:", bg="#2c2c2c", fg="white", font=("Helvetica", 12))
        label.pack(side=tk.LEFT, padx=5, pady=5)

        self.find_entry = tk.Entry(self.find_frame, font=("Helvetica", 12))
        self.find_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        search_button = tk.Button(self.find_frame, text="Find", command=self.find_text)
        search_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self.find_frame, text="X", command=self.hide_find_bar)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Bind Enter key to trigger search
        self.find_entry.bind("<Return>", lambda e: self.find_text())

        self.find_entry.focus_set()  # Set focus to the find entry

    def hide_find_bar(self, event=None):
        """Close the find bar."""
        if self.find_frame and self.find_frame.winfo_exists():
            self.find_frame.destroy()

    def find_text(self):
        """Find text in the input field."""
        search_text = self.find_entry.get()
        if not search_text:
            return

        # Remove previous highlights in the code input area
        self.code_input.tag_remove("highlight", "1.0", tk.END)
        
        start_pos = '1.0'
        while True:
            start_pos = self.code_input.search(search_text, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_text)}c"
            self.code_input.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos  # Move to next occurrence

        # Configure the highlight appearance
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
                self.errors_list.insert(tk.END, f" 💥 {error}")
            self.syntax_button.configure(state="disabled")
        else:
            self.errors_list.insert(tk.END, "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            self.errors_list.insert(tk.END, " ")

            self.errors_list.insert(tk.END, "----------------------------------------------------------------------LEXICAL COMPILE SUCCESSFULLY AGENT!---------------------------------------------------------------------------")
            self.errors_list.insert(tk.END, " ")

            self.errors_list.insert(tk.END, "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            self.syntax_button.configure(state="normal")  # Enable syntax analysis



    def import_file(self):
        """Open a file dialog to import a code file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.dedos"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.code_input.delete(1.0, tk.END)  # Clear existing input
                self.code_input.insert(tk.END, code)  # Insert imported code into the input field

    def export_file(self):
        """Export the results to a text file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".dedos", filetypes=[("Text Files", "*.dedos"), ("All Files", "*.*")])
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
        self.errors_list.delete(0, tk.END)  # Clear previous errors

        # Run Syntax Analysis
        self.parser = DEDOSParser(self.lexer.tokens)
        self.parser.ListToDict()
        self.parser.GetNextTerminal()

        syntaxErrors = self.parser.SyntaxErrors  # Get syntax errors
        print("Syntax Errors:", syntaxErrors)  # Debugging

        # 🛠️ Ignore Success Messages in Error List
        if syntaxErrors and not any("Syntax Compile Successfully" in err for err in syntaxErrors):
            for error in syntaxErrors:
                line_number = self.parser.lineCounter
                self.errors_list.insert(tk.END, f" {error}")  # Show line numbers
        else:
            self.errors_list.insert(tk.END, "Syntax Compile Successfully")



# ===================== Run GUI Without Choose Analysis =====================
def main():
    root = tk.Tk()
    app = LexerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
