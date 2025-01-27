import tkinter as tk
from tkinter import scrolledtext, messagebox
import traceback

# Lexer with newline handling
class DEDOSLexicalAnalyzer:
    def newline_token(self, input_string, i):
        """Handles newline characters as tokens."""
        tokens = []
        if input_string[i] == '\n':  # Check for a newline character
            tokens.append(("newline_token", "\\n"))  # Add the newline token
            i += 1  # Move to the next character
        else:
            raise ValueError(f"Lexical Error: Expected newline at position {i}, but got '{input_string[i]}' instead.")
        return tokens, i

    def identifier_token(self, input_string, i):
        """Handles identifiers and keywords."""
        tokens = []
        start_index = i
        while i < len(input_string) and input_string[i].isalnum():  # Allow only alphanumeric characters
            i += 1

        token = input_string[start_index:i]

        # Add the token to the list
        tokens.append(("identifier", token))
        
        return tokens, i


# Tokenizer function
def readTokens(input_string, tokenizer):
    try:
        tokens = []
        i = 0
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Skip whitespace characters (spaces, tabs, carriage returns)
            if char in [' ', '\t', '\r']:
                i += 1
                continue

            # Handle newline characters
            elif char == '\n':
                token, i = tokenizer.newline_token(input_string, i)
                tokens.extend(token)  # Add the newline token to the list
                continue  # Skip to the next character

            # Handle identifiers
            elif char.isalpha():
                token, i = tokenizer.identifier_token(input_string, i)
                tokens.extend(token)  # Add the identifier or keyword to the list

            else:
                raise ValueError(f"Lexical Error: Unknown character at position {i}")

        return tokens

    except ValueError as e:
        print(f"Error: {str(e)}")
        return []


# GUI to display tokens
def analyze_code():
    """Run the lexical analyzer on the input code."""
    input_text = code_input.get("1.0", tk.END)  # Get the code from the ScrolledText widget, no strip to preserve newlines
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some code to analyze!")
        return

    lexer = DEDOSLexicalAnalyzer()  # Create a lexer instance
    try:
        # Ensure readTokens processes the input correctly
        tokens = readTokens(input_text, lexer)

        # Clear previous results
        lexeme_list.delete(0, tk.END)
        token_list.delete(0, tk.END)
        error_output.config(state=tk.NORMAL)
        error_output.delete("1.0", tk.END)

        if isinstance(tokens, list):
            # Display tokens and lexemes in the listboxes
            for token_type, lexeme in tokens:
                # Handle newline token and display it as "\\n"
                if token_type == "newline_token":
                    lexeme_list.insert(tk.END, "\\n")  # Display the newline visually
                    token_list.insert(tk.END, token_type)  # Display the token type
                else:
                    lexeme_list.insert(tk.END, lexeme)
                    token_list.insert(tk.END, token_type)

            completion_message.config(text="Lexical analysis completed successfully!", fg="green")
        else:
            # Handle error messages from readTokens
            completion_message.config(text=tokens, fg="red")
            error_output.insert(tk.END, tokens)

        error_output.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("Error", str(e))  # Show a simple error message
        # Capture and display the full traceback in the debug output section
        error_output.config(state=tk.NORMAL)
        error_output.insert(tk.END, f"Error: {str(e)}\n")
        error_output.insert(tk.END, f"Traceback: {traceback.format_exc()}")  # Display full error traceback
        error_output.config(state=tk.DISABLED)


# GUI setup
root = tk.Tk()
root.title("DEDOS Lexical Analyzer")
root.configure(bg="#333333")

# Responsive layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=2)

# Input Frame for Code
input_frame = tk.Frame(root, bg="#333333")
input_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

line_numbers = tk.Text(input_frame, width=4, bg="#1e1e1e", fg="white", font=("Arial", 12), bd=0, height=10)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)
line_numbers.config(state=tk.DISABLED)

code_input = scrolledtext.ScrolledText(input_frame, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
code_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Lexeme and Token Lists
lexeme_label = tk.Label(root, text="Lexeme", bg="#333333", fg="white", font=("Arial", 12))
lexeme_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

token_label = tk.Label(root, text="Token", bg="#333333", fg="white", font=("Arial", 12))
token_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lexeme_list = tk.Listbox(root, bg="#1e1e1e", fg="white", font=("Arial", 10))
lexeme_list.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

token_list = tk.Listbox(root, bg="#1e1e1e", fg="white", font=("Arial", 10))
token_list.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

# Status Message
completion_message = tk.Label(root, text="", bg="#333333", fg="white", font=("Arial", 12))
completion_message.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Error Output (Terminal-like behavior)
error_output = tk.Text(root, bg="#1e1e1e", fg="white", font=("Consolas", 10), height=10, wrap=tk.WORD, bd=0)
error_output.grid(row=4, column=0, columnspan=2, padx=6, pady=5, sticky="nsew")
error_output.config(state=tk.DISABLED)

# Run Button
run_button = tk.Button(root, text="Run Tokenization", command=analyze_code, bg="#007acc", fg="white", font=("Arial", 12))
run_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

root.mainloop()  # Start the Tkinter event loop
