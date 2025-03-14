import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from lexer import DEDOSLexicalAnalyzer
from Syntax import DEDOSParser  # Import your PLY-based parser
import Semantic
import speech_recognition as sr  # Import the speech recognition module

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


        analyzer_button_frame = tk.Frame(master, bg="#3c3f59")
        analyzer_button_frame.grid(row=3, column=0, columnspan=5, padx=0, pady=10, sticky="ew")


        self.lexical_button = self.create_rounded_button(analyzer_button_frame, "Run Lexical Analyzer", self.analyze_code, "#fb5421", "white", ("Helvetica", 10))
        self.lexical_button.pack(side=tk.LEFT, padx=5)

        self.syntax_button = self.create_rounded_button(analyzer_button_frame, "Run Syntax Analyzer", self.analyze_syntax, "#fb5421", "white", ("Helvetica", 10))
        self.syntax_button.pack(side=tk.LEFT, padx=0)
        self.syntax_button.configure(state="disabled")


        self.semantic_button = self.create_rounded_button(analyzer_button_frame, "Run Semantic Analyzer", self.analyze_semantic, "#fb5421", "white", ("Helvetica", 10))
        self.semantic_button.pack(side=tk.LEFT, padx=5)
        self.semantic_button.configure(state="disabled")

        self.import_button = self.create_rounded_button(analyzer_button_frame, "Import File", self.import_file, "#fb5421", "white", ("Helvetica", 10))
        self.import_button.pack(side=tk.LEFT, padx=5)

        self.export_button = self.create_rounded_button(analyzer_button_frame, "Export Results", self.export_file, "#fb5421", "white", ("Helvetica", 10))
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.help_button = self.create_rounded_button(analyzer_button_frame, "Help", self.show_help, "#fb5421", "white", ("Helvetica", 10))
        self.help_button.pack(side=tk.LEFT, padx=5)

        
        # Input Code Frame (first instance)
        input_frame = tk.Frame(master, bg="#3c3f59")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        # (This instance will be overridden later by the final code input widget)
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#161527", fg="#fbb200",
                                                     insertbackground="#fbb200", font=("Helvetica", 12))
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Error Output with scrollbar
        error_frame = tk.Frame(master, bg="#161527")
        error_frame.grid(row=2, column=0, columnspan=5, padx=6, pady=5, sticky="nsew")
        self.errors_list = tk.Listbox(error_frame, bg="#161527", fg="#fbb200", font=("Consolas", 10))
        scrollbar_errors = tk.Scrollbar(error_frame, orient=tk.VERTICAL, command=self.errors_list.yview)
        self.errors_list.config(yscrollcommand=scrollbar_errors.set)
        self.errors_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_errors.pack(side=tk.RIGHT, fill=tk.Y)



        # Tokens Panel with scrollbar
        tokens_frame = ttk.LabelFrame(master, text="Tokens")
        tokens_frame.grid(row=1, column=3, padx=0, pady=5, sticky="nsew")
        self.tokens_list = tk.Listbox(tokens_frame, width=40)
        scrollbar_tokens = tk.Scrollbar(tokens_frame, orient=tk.VERTICAL, command=self.tokens_list.yview)
        self.tokens_list.config(yscrollcommand=scrollbar_tokens.set)
        self.tokens_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_tokens.pack(side=tk.RIGHT, fill=tk.Y)

        # Lexemes Panel with scrollbar
        lexemes_frame = ttk.LabelFrame(master, text="Lexemes")
        lexemes_frame.grid(row=1, column=4, padx=0, pady=5, sticky="nsew")
        self.lexemes_list = tk.Listbox(lexemes_frame, width=40)
        scrollbar_lexemes = tk.Scrollbar(lexemes_frame, orient=tk.VERTICAL, command=self.lexemes_list.yview)
        self.lexemes_list.config(yscrollcommand=scrollbar_lexemes.set)
        self.lexemes_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_lexemes.pack(side=tk.RIGHT, fill=tk.Y)

        # Apply Dark Mode by Default
        self.apply_dark_mode()

        # Bind Ctrl+F to the find_text function and Esc to close the find bar
        self.master.bind("<Control-f>", self.show_find_bar)
        self.master.bind("<Escape>", self.hide_find_bar)

        # Find bar frame (hidden by default)
        self.find_frame = None

        # --- Input Frame with Line Numbers ---
        input_frame = tk.Frame(master, bg="#3c3f59")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
        self.line_numbers = tk.Text(input_frame, width=4, padx=5, bg="#161527",
                                     fg="white", state="disabled", font=("Helvetica", 13))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        # Create the final code input widget (this one will be used)
        self.code_input = scrolledtext.ScrolledText(input_frame, bg="#161527", fg="#fbb200",
                                                      insertbackground="#fbb200", font=("Helvetica", 13))
        self.code_input.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # Add status bar at the top
        self.status_frame = tk.Frame(master, bg="#2c2c2c", height=20)
        self.status_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=0, pady=0)
        self.status_label = tk.Label(self.status_frame, text="Ready", bg="#2c2c2c", fg="#5cb85c", anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=2)
        # Configure hover help for elements
        self.setup_hover_help()

        # Bind events to update line numbers and sync scrolling
        self.code_input.bind("<KeyRelease>", self.update_line_numbers)
        self.code_input.bind("<MouseWheel>", self.sync_scroll)
        self.code_input.bind("<Configure>", self.update_line_numbers)
        self.code_input.bind("<KeyRelease>", self.highlight_words, add="+")
        # Add this line where the code_input is created (inside __init__)
        self.code_input.bind("<Tab>", self.handle_tab)
        
                # Within the __init__ method, after creating other buttons
        self.help_button = self.create_rounded_button(analyzer_button_frame, "Help", self.show_help, "#fb5421", "white", ("Helvetica", 10))
        self.help_button.pack(side=tk.LEFT, padx=5)

        # Add the Voice Button to capture speech input
        self.voice_button = self.create_rounded_button(
            analyzer_button_frame,
            "Speak",
            self.voice_to_text,
            "#fb5421",
            "white",
            ("Helvetica", 10)
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)

    def show_help(self):
        """Show help window with input field instructions"""
        help_text = """DEDOS Input Field Guide:
        
        1. Basic Syntax:
        - Use indentation (4 spaces) for code blocks
        - start statements with ~ and end statements with ~
        - Example:
            ~
            inst #x = 10
            plant(#x)
            ~
        
        2. Shortcuts:
        - Ctrl+F: Find text
        - Tab: Insert 4 spaces
        - Mouse hover: See element descriptions above
        
        3. Special Symbols:
        - ~ : Code of Block 
        - +-*/ : Arithmetic operators
        - () : Parameter grouping
        - "" : String delimiters
        
        4. Code Examples:
        Variable declaration:
            inst ammo = 30 
        Conditional statement:
            re(ammo < 10){
                plant("the ammo is greater than 10")
            }
            reload{
                plant("The ammo is less than 10")
            }
        Function call:
            defuse bomb_siteb(){
                }"""
        
        help_window = tk.Toplevel(self.master)
        help_window.title("Input Field Help")
        help_window.geometry("600x400")
        
        text_area = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=("Consolas", 11))
        text_area.insert(tk.INSERT, help_text)
        text_area.configure(state='disabled', bg="#161527", fg="#fbb200")
        text_area.pack(fill=tk.BOTH, expand=True)

    def voice_to_text(self):
        """Capture voice input and insert recognized text into the code input field,
        replacing spoken commands with symbols."""
        recognizer = sr.Recognizer()
        # Mapping spoken words to symbols
        mapping = {
            "equals": "=",
            "plus": "+",
            "minus": "-",
            "slash": "/",
            "double equals": "==",
            "minus equals": "-=",
            "plus equals": "+=",
            "not equals": "!=",
            "tilde": "~",
            "open parenthesis": "(",
            "close parenthesis": ")",
            "open brace": "{",
            "close brace": "}",
        }
        
        try:
            with sr.Microphone() as source:
                self.status_label.config(text="Listening...")
                self.master.update()  # Update the UI to show listening status
                audio = recognizer.listen(source, timeout=5)
                # Get the recognized text in lowercase for consistency.
                text = recognizer.recognize_google(audio).lower()

                # Replace spoken phrases with corresponding symbols.
                for word, symbol in mapping.items():
                    # Add spaces around word to avoid partial matches
                    text = text.replace(" " + word + " ", " " + symbol + " ")
                
                # Optionally, you can print or log the transformed text.
                self.code_input.insert(tk.INSERT, text)
                self.status_label.config(text="Voice input added!")
        except sr.WaitTimeoutError:
            self.status_label.config(text="No speech detected. Please try again.")
        except sr.UnknownValueError:
            self.status_label.config(text="Could not understand audio.")
        except sr.RequestError:
            self.status_label.config(text="Speech service unavailable.")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def setup_hover_help(self):
        """Configure hover help messages for UI elements"""
        hover_help = {
            self.code_input: "Enter your DEDOS code here | Use Ctrl+F to find text | Tab for 4 spaces",
            self.tokens_list: "Displays identified tokens from lexical analysis",
            self.lexemes_list: "Shows corresponding lexeme values for tokens",
            self.errors_list: "Displays compilation errors and warnings",
            self.syntax_button: "Check code structure and syntax rules compliance",
            self.lexical_button: "Analyze code for valid tokens and lexemes",
            self.semantic_button: "Verify semantic rules and type checking",
            self.import_button: "Import code from .dedos files",
            self.export_button: "Export code and analysis results"
        }

        for widget, message in hover_help.items():
            self.add_hover_help(widget, message)

    def add_hover_help(self, widget, message):
        """Add hover help functionality to a widget"""
        widget.bind("<Enter>", lambda e, m=message: self.status_label.config(text=m))
        widget.bind("<Leave>", lambda e: self.status_label.config(text="Ready"))
        
    def handle_tab(self, event):
        """Insert 4 spaces when Tab is pressed"""
        event.widget.insert(tk.INSERT, "    ")  # 4 spaces
        return "break"  # Prevents default Tab behavior
        
    def highlight_words(self, event=None):
        """Highlight multiple groups of words in different colors."""
        highlight_groups = {
            "group1": (["defuse", "in", "not"], "#F93827"),
            "group2": (["inst", "flank", "chat", "strike"], "#5cffe4"),
            "group3": (["abort", "back", "push", "perim"], "#aeac95"),
            "group4": (["plant", "info"], "#FFD65A"),
            "group5": (["re", "reload", "load"], "#ff1377"),
            "group6": (["force"], "#F3CFC6"),
            "group7": (["+", "-", "/", "*", "="], "#ffffff"),
            "group8": ("numbers", "#d6fa51"),  # Special handling for numbers
            "group9": (["~"], "#16C47F"),
            "group10": (["(", ")", "[", "{", "}", "]"], "white"),
            "group11": ("quoted_text", "#FFEB00")  # Color for text inside quotes
        }

        # Remove old highlights and set colors
        for tag, (words, color) in highlight_groups.items():
            self.code_input.tag_remove(tag, "1.0", tk.END)
            self.code_input.tag_config(tag, foreground=color)

            if words == "numbers":
                # Special handling for full numbers
                start_pos = "1.0"
                while True:
                    start_pos = self.code_input.search("0", start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    # Expand to capture the full number Sequence
                    end_pos = start_pos
                    while True:
                        next_char = self.code_input.get(end_pos)
                        if not next_char.isdigit():
                            break
                        end_pos = f"{end_pos}+1c"
                    before = self.code_input.get(f"{start_pos}-1c", start_pos)
                    after = self.code_input.get(end_pos, f"{end_pos}+1c")
                    if (before.isspace() or before in "{}[]();.,") and (after.isspace() or after in "{}[]();.,"):
                        self.code_input.tag_add(tag, start_pos, end_pos)
                    start_pos = end_pos

            elif words == "quoted_text":
                # Search for text inside quotes (single and double)
                for quote in ["'", '"']:
                    start_pos = "1.0"
                    while True:
                        start_pos = self.code_input.search(quote, start_pos, stopindex=tk.END)
                        if not start_pos:
                            break
                        end_pos = f"{start_pos}+1c"
                        while True:
                            next_char = self.code_input.get(end_pos)
                            if next_char == quote:
                                end_pos = f"{end_pos}+1c"
                                break
                            elif next_char == "":
                                break
                            end_pos = f"{end_pos}+1c"
                        self.code_input.tag_add(tag, start_pos, end_pos)
                        start_pos = end_pos

            else:
                # Standard word highlighting
                for word in words:
                    start_pos = "1.0"
                    while True:
                        start_pos = self.code_input.search(word, start_pos, stopindex=tk.END)
                        if not start_pos:
                            break
                        before = self.code_input.get(f"{start_pos}-1c", start_pos)
                        after = self.code_input.get(f"{start_pos}+{len(word)}c", f"{start_pos}+{len(word) + 1}c")
                        if (before.isspace() or before in "{}[]();.,") and (after.isspace() or after in "{}[]();.,"):
                            end_pos = f"{start_pos}+{len(word)}c"
                            self.code_input.tag_add(tag, start_pos, end_pos)
                        start_pos = f"{start_pos}+{len(word)}c"


    def create_rounded_button(self, parent, text, command, bg, fg, font):
        """Creates a rounded button with a hover effect."""
        button = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            command=command,
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=12,
            highlightthickness=0,
            bd=0,
            activebackground=bg,
            activeforeground=fg
        )
        button.config(
            highlightthickness=0,
            relief="solid",
        )
        def on_enter(e):
            button.config(bg="#303358", fg="#fbb200")
        def on_leave(e):
            button.config(bg=bg, fg=fg)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        return button

    def update_line_numbers(self, event=None):
        """Update line numbers dynamically."""
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        line_count = self.code_input.get("1.0", tk.END).count("\n")
        line_numbers_str = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_numbers_str)
        self.line_numbers.config(state="disabled")

    def sync_scroll(self, event):
        """Sync scrolling between code input and line numbers."""
        self.line_numbers.yview_moveto(self.code_input.yview()[0])

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
            self.find_entry.focus_set()
            return
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
        self.find_entry.bind("<Return>", lambda e: self.find_text())
        self.find_entry.focus_set()

    def hide_find_bar(self, event=None):
        """Close the find bar."""
        if self.find_frame and self.find_frame.winfo_exists():
            self.find_frame.destroy()

    def find_text(self):
        """Find text in the input field."""
        search_text = self.find_entry.get()
        if not search_text:
            return
        self.code_input.tag_remove("highlight", "1.0", tk.END)
        start_pos = '1.0'
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
            self.errors_list.delete(0, tk.END)
            self.errors_list.insert(tk.END, "Error: Please enter some code to analyze!")
            return

        self.lexer = DEDOSLexicalAnalyzer(code)
        self.lexer.getNextTokens()
        current_line = 1
        for token in self.lexer.tokens:
            if " : " in token:
                token_type, lexeme_value = token.split(" : ", 1)
                self.tokens_list.insert(tk.END, f"{current_line}. {token_type}")
                self.lexemes_list.insert(tk.END, f"{current_line}. {lexeme_value}")
            else:
                self.tokens_list.insert(tk.END, f"{current_line}. {token}")
                self.lexemes_list.insert(tk.END, f"{current_line}. {token}")
            if " : " in token:
                if "\n" in lexeme_value:
                    current_line += lexeme_value.count("\n")
                else:
                    current_line += 1
            else:
                current_line += 1

        if self.lexer.tokensForUnknown:
            for error in self.lexer.tokensForUnknown:
                self.errors_list.insert(tk.END, f" 💥 {error}")
            self.syntax_button.configure(state="disabled")
        else:
            self.errors_list.insert(tk.END, "-" * 180)
            self.errors_list.insert(tk.END, "----------------------------------------------------------------------LEXICAL COMPILE SUCCESSFULLY AGENT!---------------------------------------------------------------------------")
            self.errors_list.insert(tk.END, "-" * 180)
            self.syntax_button.configure(state="normal")


    def analyze_syntax(self):
        """Run Syntax Analysis"""
        self.errors_list.delete(0, tk.END)
        # Create the parser instance using tokens from the lexer.
        print("Tokens received for syntax analysis:", self.lexer.tokens)  # Debugging
        self.parser = DEDOSParser(self.lexer.tokens)
        self.parser.ListToDict()
        self.parser.GetNextTerminal()
        
        syntaxErrors = self.parser.SyntaxErrors
        print("Raw Syntax Errors:", syntaxErrors)  # Debugging
        
        # Display only the first syntax error in the GUI (if available).
        if syntaxErrors:
            self.errors_list.insert(tk.END, syntaxErrors[0])
        
        # Check for success
        if syntaxErrors and "SYNTAX COMPILE SUCCESSFUL" in syntaxErrors[0]:
            print("Syntax analysis succeeded, enabling semantic analysis.")
            self.semantic_button.configure(state="normal")  # Enable semantic button
            self.analyze_semantic()
        else:
            print("Syntax analysis failed or did not return the expected compilation.")
            self.semantic_button.configure(state="disabled")  # Ensure semantic button is disabled

        # Clear syntax errors for subsequent runs.
        self.parser.SyntaxErrors = []



    def enteringErrorsOfSyntax(self, syntaxErrors):
        # For a Listbox widget, use numeric indices.
        self.errors_list.delete(0, tk.END)
        for err in syntaxErrors:
            self.errors_list.insert(tk.END, err)


    def analyze_semantic(self):
        
        # Check if the parser and its outputs are available.
        if not hasattr(self, 'parser') or not self.parser:
            self.errors_list.delete(0, tk.END)
            self.errors_list.insert(tk.END, "Syntax analysis has not been run yet.")
            return

        if self.parser.SyntaxErrors:
            print("Syntax Errors:", self.parser.SyntaxErrors)  # Debugging
            return

        Terminals = getattr(self.parser, 'Terminals', [])
        Sequence = getattr(self.parser, 'SemanticSequence', None) or getattr(self.parser, 'Sequence', []) or Terminals

        if not Terminals or not Sequence:
            self.errors_list.delete(0, tk.END)
            self.errors_list.insert(tk.END, "Required syntax analysis outputs are missing!")
            return

        print("Running Semantic Analysis with Terminals:", Terminals)
        print("Running Semantic Analysis with Sequence:", Sequence)

        # Create the semantic analyzer instance.
        sem = Semantic.DEDOSSemantic(Terminals, Sequence)
        
        # Run semantic processing.
        sem.keyval_fix()
        sem.token_type()
        
        # Ensure output is a list
        output = sem.Output if sem.Output is not None else []
        
        # Retrieve only errors
        errors = [item.replace("|||", "") for item in output 
                if isinstance(item, str) and ('|||Semantic Error' in item or '|||Runtime Error' in item)]
        
        # Clear previous output
        self.errors_list.delete(0, tk.END)
        
        # Display errors if found, else show completion message
        if errors:
            for line in errors:
                self.errors_list.insert(tk.END, line)
        else:
            self.errors_list.insert(tk.END, "-------------------------------------------------------------SEMANTIC COMPILE SUCCESSFUL\n-------------------------------------------------------------")



    def import_file(self):
        """Open a file dialog to import a code file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.dedos"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.code_input.delete(1.0, tk.END)
                self.code_input.insert(tk.END, code)


    def export_file(self):
        """Export the code from the input box to a text file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dedos", 
            filetypes=[("Text Files", "*.dedos"), ("All Files", "*.*")]
        )
        if file_path:
            code = self.code_input.get("1.0", tk.END)
            with open(file_path, "w") as file:
                file.write(code)


def inputter(desc):
    if desc.startswith("("):
        desc = desc[1:]
    
    # Create a new Toplevel window for input
    top = tk.Toplevel()
    top.title("Input")
    top.configure(bg="#3c3f59")


    # Label for the description with specified font and color
    tk.Label(top, text=desc, font=("Helvetica", 14), bg="#3c3f59", fg="#fbb200",
             anchor='w', justify='left').pack(pady=10)
    
    # Entry widget for user input with specified font and color
    entry = tk.Entry(top, font=("Helvetica", 12), width=40, bg="#3c3f59", fg="#fbb200",
                     insertbackground="#fbb200")
    entry.pack(padx=20, pady=10)
    entry.focus_set()
    value = None

    def submit():
        nonlocal value
        # Capture the entry value (the replace is left as in the original)
        value = str(entry.get()).replace("-", "-")
        top.destroy()  # Close the input window

    # Submit button with specified design
    tk.Button(top, text="Submit", command=submit, font=("Helvetica", 12),
              bg="#fb5421", fg="#fbb200", padx=20, pady=5, relief="flat", borderwidth=0).pack(pady=10)
    
    top.wait_window()  # Wait for the input window to close
    try:
        if value in [True, False]:
            pass
        elif type(eval(value)) == int:
            pass
        elif type(eval(value)) == float:
            pass
    except:
        value = "\"" + value + "\""
    return value

def main():
    root = tk.Tk()
    app = LexerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
