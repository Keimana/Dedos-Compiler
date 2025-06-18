import re
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

        analyzer_button_frame = tk.Frame(master, bg="#3c3f59")
        analyzer_button_frame.grid(row=3, column=0, columnspan=5, padx=0, pady=10, sticky="ew")

        self.lexical_button = self.create_rounded_button(
            analyzer_button_frame, "Run Lexical Analyzer", self.analyze_code,
            "#fb5421", "white", ("Consolas", 12)
        )
        self.lexical_button.pack(side=tk.LEFT, padx=5)

        self.syntax_button = self.create_rounded_button(
            analyzer_button_frame, "Run Syntax Analyzer", self.analyze_syntax,
            "#fb5421", "white", ("Consolas", 12)
        )
        self.syntax_button.pack(side=tk.LEFT, padx=0)
        self.syntax_button.configure(state="disabled")

        self.codegen_button = self.create_rounded_button(
            analyzer_button_frame, "Execute!", self.generate_code,
            "#fb5421", "white", ("Consolas", 12)
        )
        self.codegen_button.pack(side=tk.LEFT, padx=5)
        self.codegen_button.configure(state="disabled")

        self.import_button = self.create_rounded_button(
            analyzer_button_frame, "Import File", self.import_file,
            "#fb5421", "white", ("Consolas", 12)
        )
        self.import_button.pack(side=tk.LEFT, padx=5)

        self.export_button = self.create_rounded_button(
            analyzer_button_frame, "Export File", self.export_file,
            "#fb5421", "white", ("Consolas", 12)
        )

        self.export_button.pack(side=tk.LEFT, padx=5)

        self.help_button = self.create_rounded_button(
            analyzer_button_frame, "Help", self.show_help,
            "#fb5421", "white", ("Consolas", 12)
        )
        self.help_button.pack(side=tk.LEFT, padx=5)


        # Input Code Frame (first instance)
        input_frame = tk.Frame(master, bg="#3c3f59")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        # (This instance will be overridden later by the final code input widget)
        self.code_input = scrolledtext.ScrolledText(
            input_frame, bg="#161527", fg="#fbb200",
            insertbackground="#fbb200", font=("Consolas", 12)
        )
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Error Output with scrollbar
        error_frame = tk.Frame(master, bg="#161527")
        error_frame.grid(row=2, column=0, columnspan=5, padx=6, pady=5, sticky="nsew")
        self.errors_list = tk.Listbox(
            error_frame, bg="#161527", fg="#fbb200", font=("Consolas", 12)
        )
        scrollbar_errors = tk.Scrollbar(
            error_frame, orient=tk.VERTICAL, command=self.errors_list.yview
        )
        self.errors_list.config(yscrollcommand=scrollbar_errors.set)
        self.errors_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_errors.pack(side=tk.RIGHT, fill=tk.Y)

        # ——————————————————————————————————————————
        # Lexemes & Tokens Panels (swapped)
        # ——————————————————————————————————————————
        # Lexemes container (left)
        tokens_frame = ttk.LabelFrame(master, text="Lexemes")
        tokens_frame.grid(row=1, column=3, padx=0, pady=5, sticky="nsew")
        # Tokens container (right)
        lexemes_frame = ttk.LabelFrame(master, text="Tokens")
        lexemes_frame.grid(row=1, column=4, padx=0, pady=5, sticky="nsew")

        # 1) Create your two listboxes
        self.tokens_list = tk.Listbox(
            tokens_frame, width=40, bg="#161527", fg="#fbb200"
        )
        self.lexemes_list = tk.Listbox(
            lexemes_frame, width=40, bg="#161527", fg="#fbb200"
        )

        # 2) One Scrollbar instance for *both*
        self._tl_scrollbar = tk.Scrollbar(
            tokens_frame, orient=tk.VERTICAL, command=self._on_tl_scroll
        )
        # (We pack it in the Lexemes frame; both listboxes obey its command.)

        # 3) Configure both listboxes to send their “slider‐moves” back to that scrollbar
        self.tokens_list.config(yscrollcommand=self._on_tl_yscroll)
        self.lexemes_list.config(yscrollcommand=self._on_tl_yscroll)

        # 4) Layout
        self.tokens_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._tl_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.lexemes_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 5) Mouse-wheel on either box scrolls *both*
        for w in (self.tokens_list, self.lexemes_list):
            w.bind("<MouseWheel>", self._on_tl_mousewheel)
            w.bind("<Button-4>", self._on_tl_mousewheel)   # Linux wheel up
            w.bind("<Button-5>", self._on_tl_mousewheel)   # Linux wheel down

        # Apply Dark Mode by Default
        self.apply_dark_mode()

        # Bind Ctrl+F to the find_text function and Esc to close the find bar
        self.master.bind("<Control-f>", self.show_find_bar)
        self.master.bind("<Escape>", self.hide_find_bar)
        self.master.bind("<Control-BackSpace>", self.handle_ctrl_backspace)
        # Find bar frame (hidden by default)
        self.find_frame = None

        # --- Input Frame with Line Numbers & a Shared Scrollbar ---
        input_frame = tk.Frame(master, bg="#3c3f59")
        input_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        # 1) One vertical scrollbar
        text_scrollbar = tk.Scrollbar(input_frame, orient=tk.VERTICAL)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2) Gutter: no scrollbar binding, disabled state so user can't scroll it
        self.line_numbers = tk.Text(
            input_frame,
            width=4,
            padx=5,
            bg="#161527",
            fg="white",
            state="disabled",
            font=("Consolas", 13)
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.line_numbers.bind("<MouseWheel>", lambda e: "break")
        self.line_numbers.bind("<Button-4>",   lambda e: "break")
        self.line_numbers.bind("<Button-5>",   lambda e: "break")

        # 3) Code pane: *this* is the only widget hooked to the scrollbar
        self.code_input = tk.Text(
            input_frame,
            bg="#161527",
            fg="#fbb200",
            insertbackground="#fbb200",
            font=("Consolas", 13),
            yscrollcommand=text_scrollbar.set
        )
        self.code_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 4) Scrollbar drives *both* widgets, but is only connected to code_input
        text_scrollbar.config(command=self._on_scrollbar)

        # 5) Mouse-wheel on code_input scrolls both
        self.code_input.bind("<MouseWheel>", self._on_mousewheel)
        self.code_input.bind("<Button-4>",   self._on_mousewheel)
        self.code_input.bind("<Button-5>",   self._on_mousewheel)

        # Add status bar at the top
        self.status_frame = tk.Frame(master, bg="#2c2c2c", height=20)
        self.status_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=0, pady=0)
        self.status_label = tk.Label(
            self.status_frame, text="Ready", bg="#2c2c2c",
            fg="#5cb85c", font=("Segoe UI", 12), anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=2)

        # Configure hover help for elements
        self.setup_hover_help()

        # Bind events to update line numbers and sync scrolling
        self.code_input.bind("<KeyRelease>", self.update_line_numbers)
        self.code_input.bind("<MouseWheel>", self.sync_scroll)
        self.code_input.bind("<Configure>",   self.update_line_numbers)
        self.code_input.bind("<KeyRelease>", self.highlight_words, add="+")
        self.code_input.bind("<Tab>",         self.handle_tab)





    def start_codegen_button_animation(self):
        self.codegen_colors = [
            "#004a99",  # deep blue
            "#005fbf",  # medium blue
            "#0073e6",  # bright blue
            "#008080",  # teal
            "#009966",  # jade green
            "#007a3d",  # dark green
            "#005f33",  # forest green
            "#004d26"   # deep forest green
        ]    
        self.codegen_color_index = 0
        self.animate_codegen_button()


    def animate_codegen_button(self):
        if self.codegen_button["state"] == "normal":
            color = self.codegen_colors[self.codegen_color_index]
            self.codegen_button.configure(bg=color)
            self.codegen_color_index = (self.codegen_color_index + 1) % len(self.codegen_colors)
            self.master.after(75, self.animate_codegen_button)

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
    inst #ammo = 30 
Conditional statement:
    re(#ammo < 10){
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

    def _on_scrollbar(self, *args):
        """Scrollbar drag scrolls code and gutter in lock-step."""
        # move code
        self.code_input.yview(*args)
        # mirror to gutter
        self.line_numbers.yview(*args)

    def _on_mousewheel(self, event):
        """Wheel in code_input scrolls both; gutter ignores wheel."""
        # Windows/Mac
        if hasattr(event, "delta"):
            units = -1 * (event.delta // 120)
        else:
            # Linux (Button-4 up, Button-5 down)
            units = 1 if event.num == 5 else -1

        self.code_input.yview_scroll(units, "units")
        self.line_numbers.yview_scroll(units, "units")
        return "break"  # eat the event so gutter doesn’t respond


    def setup_hover_help(self):
        """Configure hover help messages for UI elements"""
        hover_help = {
            self.code_input: "Enter your DEDOS code here | Use Ctrl+F to find text | Tab for 4 spaces",
            self.tokens_list: "Displays identified tokens from lexical analysis",
            self.lexemes_list: "Shows corresponding lexeme values for tokens",
            self.errors_list: "Displays compilation errors and warnings and result of the evaluation",
            self.syntax_button: "Check code structure and syntax rules compliance",
            self.lexical_button: "Analyze code for valid tokens and lexemes",
            self.import_button: "Import code from .dedos files",
            self.export_button: "Export code and analysis results",
            self.codegen_button: "Generate target code from the analyzed input",
            self.help_button: "Helper button"
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
            "group2": (["inst", "flank", "chat", "strike", "tool"], "#5cffe4"),
            "group3": (["abort", "back", "push", "perim"], "#aeac95"),
            "group4": (["plant", "info"], "#FFD65A"),
            "group5": (["re", "reload", "load"], "#ff1377"),
            "group6": (["force"], "#F3CFC6"),
            "group7": (["+", "-", "/", "*", "="], "#ffffff"),
            "group8": ("numbers", "#d6fa51"),  # Special handling for numbers
            "group9": (["~"], "#16C47F"),
            "group10": (["(", ")", "[", "{", "}", "]"], "white"),
            "group11": ("quoted_text", "#FFEB00"),  # Color for text inside quotes
            "group12": ("comment", "#A9A9A9")  # Color for text inside comments
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
                        
            elif words == "comment":
                # Search for text inside comments marked with '$'
                for quote in ["$"]:
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



    def _on_tl_scroll(self, *args):
        """Scrollbar-thumb drag invokes this: scroll *both* lists."""
        self.tokens_list.yview(*args)
        self.lexemes_list.yview(*args)

    def _on_tl_yscroll(self, first, last):
        """
        Called when either listbox moves itself (e.g. via keyboard or .see()):
        update the scrollbar slider position.
        """
        self._tl_scrollbar.set(first, last)

    def _on_tl_mousewheel(self, event):
        """Wheel over either box scrolls both boxes together."""
        if hasattr(event, "delta"):
            amt = -1 * (event.delta // 120)
        else:
            amt = 1 if event.num == 5 else -1
        self.tokens_list.yview_scroll(amt, "units")
        self.lexemes_list.yview_scroll(amt, "units")
        return "break"


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
        label = tk.Label(self.find_frame, text="Find:", bg="#2c2c2c", fg="white", font=("Consolas", 12))
        label.pack(side=tk.LEFT, padx=5, pady=5)
        self.find_entry = tk.Entry(self.find_frame, font=("Consolas", 12))
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
        
    def handle_ctrl_backspace(self, event):
        # Get the current insertion index
        current_index = self.code_input.index("insert")
        # Get the start index of the current line
        line_start = self.code_input.index("insert linestart")
        # Retrieve the text from the beginning of the line to the current insertion point
        text_before = self.code_input.get(line_start, current_index)
        
        # Remove trailing spaces in case the cursor is after spaces
        stripped_text = text_before.rstrip()
        if not stripped_text:
            # Nothing to delete on this line, so let the default behavior occur
            return "break"
        
        # Calculate how many characters to delete:
        # Find the last space character in the stripped text. If none is found, delete from the beginning of the line.
        last_space = stripped_text.rfind(" ")
        if last_space == -1:
            delete_start = line_start
        else:
            # +1 to delete the space as well, so start from the character right after the last space.
            delete_start = f"{line_start}+{last_space + 1}c"
        
        # Delete from the calculated starting position to the current insertion point.
        self.code_input.delete(delete_start, current_index)
        
        return "break"  # Prevent any default behavior
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    def analyze_code(self):
        """Run Lexical Analysis (preserve valid tokens even if errors exist)"""
        # Clear previous results
        self.tokens_list.delete(0, tk.END)
        self.lexemes_list.delete(0, tk.END)
        self.errors_list.delete(0, tk.END)

        code = self.code_input.get("1.0", tk.END).strip()
        if not code:
            self.errors_list.insert(tk.END, "Error: Please enter some code to analyze!")
            return

        self.lexer = DEDOSLexicalAnalyzer(code)
        self.lexer.tokensForUnknown = []
        self.lexer.tokens = []  # Clear previous tokens if re-running

        self.lexer.getNextTokens()

        token_count = 1
        error_count = 1

        for token in self.lexer.tokens:
            if token == "ERROR" or token is None:
                continue  # Don't show SKIP in valid lists

            if " : " in token:
                token_type, lexeme_value = token.split(" : ", 1)

                if token_type == "ERROR":
                    self.errors_list.insert(tk.END, f"{error_count}. 💥 {lexeme_value}")
                    error_count += 1
                else:
                    self.lexemes_list.insert(tk.END, f"{token_count}. {token_type}")
                    self.tokens_list.insert(tk.END, f"{token_count}. {lexeme_value}")
                    token_count += 1
            else:
                # Fallback: unknown format but not SKIP
                self.lexemes_list.insert(tk.END, f"{token_count}. {token}")
                self.tokens_list.insert(tk.END, f"{token_count}. {token}")
                token_count += 1

        # Show all additional unknowns from tokensForUnknown
        for unknown in self.lexer.tokensForUnknown:
            self.errors_list.insert(tk.END, f"{error_count}. 💥 {unknown}")
            error_count += 1

        # Enable or disable syntax button based on errors
        if self.lexer.tokensForUnknown:
            self.syntax_button.configure(state="disabled")
        else:
            self.errors_list.insert(tk.END, "LEXICAL COMPILE SUCCESSFULLY AGENT!")
            self.syntax_button.configure(state="normal")



        
    def analyze_syntax(self):
        """Run Syntax Analysis"""
        # Clear previous errors in GUI
        self.errors_list.delete(0, tk.END)

        # Debug: show received tokens
        print("Tokens received for syntax analysis:", self.lexer.tokens)

        # Initialize parser
        self.parser = DEDOSParser(self.lexer.tokens)
        self.parser.ListToDict()

        # Attempt parsing, catching IndexError for unexpected end of tokens
        try:
            self.parser.GetNextTerminal()
        except IndexError as e:
            # Determine location of error from last processed token
            if self.parser.position > 0 and self.lexer.tokens:
                token = self.lexer.tokens[self.parser.position - 1]
                line = getattr(token, "line", "unknown")
                column = getattr(token, "column", "unknown")
            else:
                line = "unknown"
                column = "unknown"

            msg = str(e)
            error_message = f"Syntax Error at line {line}, column {column}: {msg}"
            self.parser.SyntaxErrors.append((error_message, line, column))
            print(error_message)

        # Capture errors
        syntax_errors = self.parser.SyntaxErrors
        print("Raw Syntax Errors:", syntax_errors)

        # Always show only the first syntax error
        if syntax_errors:
            err = syntax_errors[0]
            if isinstance(err, tuple) and len(err) == 3:
                message, ln, col = err
                display_text = f"Syntax Error at line {ln}, column {col}: {message}"
            else:
                display_text = str(err)

            self.errors_list.insert(tk.END, display_text)
            print(display_text)

            # Check that first error for a compile-success marker
            first_err_list = [syntax_errors[0]]
            if any(
                (isinstance(e, str) and "SYNTAX COMPILE SUCCESSFUL" in e)
                or (isinstance(e, tuple) and "SYNTAX COMPILE SUCCESSFUL" in e[0])
                for e in first_err_list
            ):
                print("Syntax analysis succeeded, enabling semantic analysis.")
                self.codegen_button.configure(state="normal")
                self.start_codegen_button_animation()
            else:
                print("Syntax analysis failed or did not return the expected compilation.")
                self.codegen_button.configure(state="disabled")
        else:
            # No errors: success
            print("Syntax analysis succeeded with no errors.")
            self.codegen_button.configure(state="normal")
            self.start_codegen_button_animation()

        # Reset errors for next run
        self.parser.SyntaxErrors.clear()






    def generate_code(self):
        """Generate target code by running semantic analysis and print the output in the error output box.
        If semantic errors are found, disable the Generate Code button."""
        # Ensure syntax analysis has been run
        if not hasattr(self, 'parser') or not self.parser:
            self.errors_list.delete(0, tk.END)
            self.errors_list.insert(tk.END, "Syntax analysis has not been run yet.")
            return

        if self.parser.SyntaxErrors:
            print("Syntax Errors:", self.parser.SyntaxErrors)  # Debugging
            return

        # Prepare terminals and sequence
        terminals = getattr(self.parser, 'Terminals', [])
        sequence = (getattr(self.parser, 'SemanticSequence', None)
                    or getattr(self.parser, 'Sequence', [])
                    or terminals)
        if not terminals or not sequence:
            self.errors_list.delete(0, tk.END)
            self.errors_list.insert(tk.END, "Required syntax analysis outputs are missing!")
            return

        # Semantic analysis
        sem = Semantic.DEDOSSemantic(terminals, sequence)
        sem.keyval_fix()
        sem.token_type()
        output = sem.Output

        # Clear previous output
        self.errors_list.delete(0, tk.END)

        # Normalize to list of lines
        lines = output if isinstance(output, list) else [output]

        # Check for semantic or runtime errors first
        error_lines = [line for line in lines
                       if isinstance(line, str)
                       and ("Semantic Error" in line or "Runtime Error" in line)]
        if error_lines:
            # Display only error messages
            for err in error_lines:
                self.errors_list.insert(tk.END, err)
            # Disable code generation
            self.codegen_button.configure(state="disabled")
            return

        for line in lines:
            formatted_line = line
            # Format floats
            if isinstance(line, str) and re.match(r'^[+-]?\d+\.\d+$', line):
                try:
                    num = float(line)
                    formatted_line = f"{round(num, 5):.5f}".rstrip('0').rstrip('.')
                except (ValueError, TypeError):
                    pass
            # Remove parentheses and brackets
            if isinstance(formatted_line, str):
                formatted_line = formatted_line.replace('(', '').replace(')', '')
                formatted_line = formatted_line.replace('[', '').replace(']', '')
            
            # Single insert after all formatting
            self.errors_list.insert(tk.END, formatted_line)

        # If no output at all
        if not lines:
            self.errors_list.insert(tk.END, "No output generated.")




    def import_file(self):
        """Open a file dialog to import a code file."""
        file_path = filedialog.askopenfilename(filetypes=[(".dedos", "*.dedos"), ("All Files", "*.*")])
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
    tk.Label(top, text=desc, font=("Consolas", 14), bg="#3c3f59", fg="#fbb200",
             anchor='w', justify='left').pack(pady=10)
    
    # Entry widget for user input with specified font and color
    entry = tk.Entry(top, font=("Consolas", 12), width=40, bg="#3c3f59", fg="#fbb200",
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
    tk.Button(top, text="Submit", command=submit, font=("Consolas", 12),
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