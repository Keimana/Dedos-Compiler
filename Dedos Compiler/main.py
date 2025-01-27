import tkinter as tk
from tkinter import scrolledtext, messagebox
import traceback
from lexer import DEDOSLexicalAnalyzer, readTokens

def analyze_code():
    """Run the lexical analyzer on the input code."""
    input_text = code_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some code to analyze!")
        return

    lexer = DEDOSLexicalAnalyzer()
    try:
        tokens = readTokens(input_text, lexer)

        # Clear previous results
        lexeme_list.delete(0, tk.END)
        token_list.delete(0, tk.END)
        error_output.config(state=tk.NORMAL)
        error_output.delete("1.0", tk.END)

        error_output.insert(tk.END, "Lexemes and Tokens:\n")
        error_output.insert(tk.END, "-" * 30 + "\n")

        for token_type, lexeme in tokens:
            if token_type == "\\n":
                lexeme_list.insert(tk.END, "\\n")
                token_list.insert(tk.END, "newline_token")
                error_output.insert(tk.END, f"Lexeme: \\n\tToken: newline_token\n")
            else:
                lexeme_list.insert(tk.END, lexeme)
                token_list.insert(tk.END, token_type)
                error_output.insert(tk.END, f"Lexeme: {lexeme}\tToken: {token_type}\n")

        error_output.insert(tk.END, "-" * 30 + "\n")
        error_output.insert(tk.END, "Lexical analysis completed successfully!\n")

    except ValueError as e:
        error_output.config(state=tk.NORMAL)
        error_output.insert(tk.END, f"ValueError: {str(e)}\n")
        error_output.insert(tk.END, f"Traceback:\n{traceback.format_exc()}\n")
        error_output.config(state=tk.DISABLED)

    except Exception as e:
        error_output.config(state=tk.NORMAL)
        error_output.insert(tk.END, f"Unexpected Error: {str(e)}\n")
        error_output.insert(tk.END, f"Traceback:\n{traceback.format_exc()}\n")
        error_output.config(state=tk.DISABLED)


def update_line_numbers(event=None):
    """Update the line numbers in the text widget."""
    code = code_input.get("1.0", tk.END).strip()
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete("1.0", tk.END)
    for i, _ in enumerate(code.split("\n"), start=1):
        line_numbers.insert(tk.END, f"{i}\n")
    line_numbers.config(state=tk.DISABLED)


# Main window setup
root = tk.Tk()
root.title("DEDOS Analyzer")
root.configure(bg="#333333")

# Responsive layout
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)



# Function to create rounded buttons
def create_rounded_button(parent, text, command, bg, fg, font):
    """Creates a rounded button with a hover effect."""
    button = tk.Label(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        font=font,
        padx=10,
        pady=5,
        relief="flat",
        cursor="hand2",
        borderwidth=0
    )

    def on_enter(e):
        button.config(bg="#005f8c", fg="white")  # Hover color

    def on_leave(e):
        button.config(bg=bg, fg=fg)  # Default color

    # Bind hover effects
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<Button-1>", lambda e: command())  # Click event

    return button


# Analyzer Buttons Frame
analyzer_button_frame = tk.Frame(root, bg="#333333")
analyzer_button_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

# Lexical Analyzer Button
lexical_button = create_rounded_button(
    analyzer_button_frame,
    text="Lexical Analyzer",
    command=analyze_code,  # Replace with actual lexical analysis function
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
lexical_button.pack(side=tk.LEFT, padx=10)

# Syntax Analyzer Button
def analyze_syntax():
    """Placeholder function for syntax analyzer."""
    messagebox.showinfo("Syntax Analyzer", "Syntax analyzer function triggered!")

syntax_button = create_rounded_button(
    analyzer_button_frame,
    text="Syntax Analyzer",
    command=analyze_syntax,  # Replace with actual syntax analysis function
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
syntax_button.pack(side=tk.LEFT, padx=10)

# Semantic Analyzer Button
def analyze_semantics():
    """Placeholder function for semantic analyzer."""
    messagebox.showinfo("Semantic Analyzer", "Semantic analyzer function triggered!")

semantic_button = create_rounded_button(
    analyzer_button_frame,
    text="Semantic Analyzer",
    command=analyze_semantics,  # Replace with actual semantic analysis function
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
semantic_button.pack(side=tk.LEFT, padx=10)


# Top Buttons: Run Tokenization
button_frame = tk.Frame(root, bg="#333333")
button_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

# Status Message and Run Button Frame
run_button_frame = tk.Frame(root, bg="#333333")
run_button_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

run_button = create_rounded_button(
    run_button_frame,
    text="Run Tokenization",
    command=analyze_code,  # This will trigger the analyze_code function
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
run_button.pack(side=tk.LEFT, padx=10)

completion_message = tk.Label(
    run_button_frame, text="", bg="#333333", fg="white", font=("Arial", 12)
)
completion_message.pack(side=tk.LEFT, padx=10)

# Input Frame for Code
input_frame = tk.Frame(root, bg="#333333")
input_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

line_numbers = tk.Text(input_frame, width=4, bg="#1e1e1e", fg="white", font=("Arial", 12), bd=0, height=10)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)
line_numbers.config(state=tk.DISABLED)

code_input = scrolledtext.ScrolledText(input_frame, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
code_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
code_input.bind("<KeyRelease>", update_line_numbers)

# Lexeme Listbox with Scrollbar
lexeme_frame = tk.Frame(root, bg="#333333")  # Frame to hold the listbox and scrollbar
lexeme_frame.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")

lexeme_scroll = tk.Scrollbar(lexeme_frame, orient=tk.VERTICAL)  # Vertical scrollbar for Lexeme
lexeme_scroll.pack(side=tk.RIGHT, fill=tk.Y)

lexeme_list = tk.Listbox(lexeme_frame, bg="#1e1e1e", fg="white", font=("Arial", 10), yscrollcommand=lexeme_scroll.set)
lexeme_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

lexeme_scroll.config(command=lexeme_list.yview)  # Connect the scrollbar to the listbox

# Token Listbox with Scrollbar
token_frame = tk.Frame(root, bg="#333333")  # Frame to hold the listbox and scrollbar
token_frame.grid(row=1, column=4, padx=10, pady=5, sticky="nsew")

token_scroll = tk.Scrollbar(token_frame, orient=tk.VERTICAL)  # Vertical scrollbar for Token
token_scroll.pack(side=tk.RIGHT, fill=tk.Y)

token_list = tk.Listbox(token_frame, bg="#1e1e1e", fg="white", font=("Arial", 10), yscrollcommand=token_scroll.set)
token_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

token_scroll.config(command=token_list.yview)  # Connect the scrollbar to the listbox


# Status Message
completion_message = tk.Label(root, text="", bg="#333333", fg="white", font=("Arial", 12))
completion_message.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Error Output (Terminal-like behavior)
error_output = tk.Text(root, bg="#1e1e1e", fg="white", font=("Consolas", 10), height=10, wrap=tk.WORD, bd=0)
error_output.grid(row=3, column=0, columnspan=5, padx=6, pady=5, sticky="nsew")
error_output.config(state=tk.DISABLED)

root.mainloop()  # Start the Tkinter event loop
