import tkinter as tk
from tkinter import scrolledtext
from lexi import DEDOSLexicalAnalyzer

# Function to update line numbers in the text area
def update_line_numbers(event):
    line_numbers.delete(1.0, tk.END)
    lines = code_input.get("1.0", tk.END).splitlines()
    for i, line in enumerate(lines, 1):
        line_numbers.insert(tk.END, f"{i}\n")

# Function to append messages to the terminal-like error output
def append_to_terminal(message):
    error_output.config(state=tk.NORMAL)
    error_output.insert(tk.END, f"{message}\n")  # Add message with a newline
    error_output.see(tk.END)  # Scroll to the latest message
    error_output.config(state=tk.DISABLED)

# Function to handle the Lexical Analyzer button
def analyze_code():
    input_string = code_input.get("1.0", tk.END).strip()

    tokenizer = DEDOSLexicalAnalyzer()  # Assuming you have a DEDOSLexicalAnalyzer class

    try:
        # Tokenize the input string
        tokens = tokenizer.tokenize(input_string)

        # Clear the lexeme and token lists
        lexeme_list.delete(0, tk.END)
        token_list.delete(0, tk.END)

        # Populate the lexeme and token lists
        for token_type, lexeme in tokens:
            lexeme_list.insert(tk.END, lexeme)
            token_list.insert(tk.END, token_type)

        # Log success message to the terminal
        append_to_terminal("Lexical analysis complete!")
        append_to_terminal(f"Tokens found: {len(tokens)}")

        # Update completion message
        completion_message.config(text="Lexical analysis complete!", fg="green")

    except ValueError as e:
        # Log error message to the terminal
        append_to_terminal(f"Error: {e}")
        
        # Display error message in completion label
        completion_message.config(text="Lexical analysis failed.", fg="red")

# Placeholder functions for syntax and semantic analyzers
def syntax_analyze():
    append_to_terminal("Syntax analyzer not implemented yet.")

def semantic_analyze():
    append_to_terminal("Semantic analyzer not implemented yet.")

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

# Top Buttons: Lexical, Syntax, and Semantic Analyzers
button_frame = tk.Frame(root, bg="#333333")
button_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

# Lexical Analyzer Button
lexical_button = create_rounded_button(
    button_frame,
    text="Lexical Analyzer",
    command=analyze_code,
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
lexical_button.pack(side=tk.LEFT, padx=10)

# Syntax Analyzer Button
syntax_button = create_rounded_button(
    button_frame,
    text="Syntax Analyzer",
    command=syntax_analyze,
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
syntax_button.pack(side=tk.LEFT, padx=10)

# Semantic Analyzer Button
semantic_button = create_rounded_button(
    button_frame,
    text="Semantic Analyzer",
    command=semantic_analyze,
    bg="#007acc",
    fg="white",
    font=("Arial", 10),
)
semantic_button.pack(side=tk.LEFT, padx=10)

# Input Frame for Code
input_frame = tk.Frame(root, bg="#333333")
input_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

input_frame.grid_columnconfigure(0, weight=0)
input_frame.grid_columnconfigure(1, weight=1)
input_frame.grid_rowconfigure(0, weight=1)

line_numbers = tk.Text(input_frame, width=4, bg="#1e1e1e", fg="white", font=("Arial", 12), bd=0, height=10)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

code_input = scrolledtext.ScrolledText(input_frame, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
code_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
code_input.bind("<KeyRelease>", update_line_numbers)

# Lexeme and Token Lists
lexeme_label = tk.Label(root, text="Lexeme", bg="#333333", fg="white", font=("Arial", 12))
lexeme_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

token_label = tk.Label(root, text="Token", bg="#333333", fg="white", font=("Arial", 12))
token_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

lexeme_list = tk.Listbox(root, bg="#1e1e1e", fg="white", font=("Arial", 10))
lexeme_list.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")

token_list = tk.Listbox(root, bg="#1e1e1e", fg="white", font=("Arial", 10))
token_list.grid(row=1, column=4, padx=10, pady=5, sticky="nsew")

# Add a message label below the input field for status updates
completion_message = tk.Label(root, text="", bg="#333333", fg="white", font=("Arial", 12))
completion_message.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Error Output (Terminal-like behavior)
error_output = tk.Text(root, bg="#1e1e1e", fg="white", font=("Consolas", 10), height=10, wrap=tk.WORD, bd=0)
error_output.grid(row=3, column=0, columnspan=5, padx=6, pady=5, sticky="nsew")
error_output.config(state=tk.DISABLED)

# Run the main loop
root.mainloop()
