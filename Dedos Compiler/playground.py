class DEDOSLexicalAnalyzer:
    def __init__(self):
        # Reserved words starting with specific characters
        self.reserved_words = {
            'a': ['abort', 'and'],
            'b': ['back', 'bounce'],
            'c': ['chat'],
            'd': ['define'],
            'f': ['function'],
            'g': ['glob'],
            'i': ['input', 'if'],
            'l': ['load'],
            'n': ['negate', 'note'],
            'o': ['output'],
            'p': ['print'],
            'r': ['read'],
            's': ['start'],
            't': ['token'],
            'w': ['watch']
        }
        
        self.delim12 = [';']  # Semicolon delimiter
        self.delim4 = [' ', '(', ')', '\n']  # Space and parentheses for 'and', 'abort', etc.
        self.delim3 = ['\n', ' ', ';']  # Newline and semicolon

    def tokenize(self, input_string):
        """Tokenizes the input string using an FSM approach."""
        tokens = []
        i = 0
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Skip whitespace
            if char in " \t\n":
                i += 1
                continue

            # Start FSM for the first letter
            if char == 'a':
                tokens.extend(self.a_token(input_string, i))
                i += 5  # Move past the word "abort" or "and"
                continue
            elif char == 'b':
                tokens.extend(self.b_token(input_string, i))
                i += 4  # Move past the word "back"
                continue
            elif char == 'c':
                tokens.extend(self.c_token(input_string, i))
                i += 4  # Move past the word "chat"
                continue
            elif char == 'd':
                tokens.extend(self.d_token(input_string, i))
                i += 6  # Move past the word "define"
                continue
            elif char == 'f':
                tokens.extend(self.f_token(input_string, i))
                i += 8  # Move past the word "function"
                continue
            elif char == 'g':
                tokens.extend(self.g_token(input_string, i))
                i += 4  # Move past the word "glob"
                continue
            elif char == 'i':
                tokens.extend(self.i_token(input_string, i))
                i += 5  # Move past the word "input"
                continue
            elif char == 'l':
                tokens.extend(self.l_token(input_string, i))
                i += 4  # Move past the word "load"
                continue
            elif char == 'n':
                tokens.extend(self.n_token(input_string, i))
                i += 7  # Move past the word "negate"
                continue
            elif char == 'o':
                tokens.extend(self.o_token(input_string, i))
                i += 6  # Move past the word "output"
                continue
            elif char == 'p':
                tokens.extend(self.p_token(input_string, i))
                i += 5  # Move past the word "print"
                continue
            elif char == 'r':
                tokens.extend(self.r_token(input_string, i))
                i += 4  # Move past the word "read"
                continue
            elif char == 's':
                tokens.extend(self.s_token(input_string, i))
                i += 5  # Move past the word "start"
                continue
            elif char == 't':
                tokens.extend(self.t_token(input_string, i))
                i += 5  # Move past the word "token"
                continue
            elif char == 'w':
                tokens.extend(self.w_token(input_string, i))
                i += 5  # Move past the word "watch"
                continue

            # Handle generic identifiers
            if char.isalpha():
                start = i
                while i < length and (input_string[i].isalnum() or input_string[i] == '_'):
                    i += 1
                identifier = input_string[start:i]
                tokens.append(("identifier", identifier))
                continue

            # Incomplete keyword handling
            if char in self.reserved_words:
                # Check for the start of a reserved word
                for keyword in self.reserved_words[char]:
                    # Check if the substring matches the keyword completely
                    if input_string[i:i+len(keyword)] != keyword:
                        # Error message indicating that a keyword is incomplete
                        raise ValueError(f"Lexical Error: Incomplete keyword '{input_string[i:i+len(keyword)]}' at position {i}, expected '{keyword}'")

            # Unrecognized character
            raise ValueError(f"Lexical Error: Unrecognized character '{char}' at position {i}")

        return tokens

            
    def a_token(self, input_string, i):
        """Handles the 'a' case for 'abort' and 'and' using FSM with reset."""
        tokens = []
        state = 0  # Start at state 0

        while i < len(input_string):
            char = input_string[i]

            if state == 0:
                if char == 'a':  # Start checking for either 'abort' or 'and'
                    state = 1
                else:
                    raise ValueError(f"Lexical Error: Unrecognized character '{char}' at position {i}")

            elif state == 1:
                if char == 'b':  # Checking for 'abort'
                    state = 2
                elif char == 'n':  # Checking for 'and'
                    state = 6
                else:
                    raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 'b' or 'n' after 'a'")

            elif state == 2:
                if char == 'o':  # Continue with 'abort'
                    state = 3
                else:
                    raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 'o' after 'ab'")

            elif state == 3:
                if char == 'r':  # Continue with 'abort'
                    state = 4
                else:
                    raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 'r' after 'abo'")

            elif state == 4:
                if char == 't':  # Final state for 'abort'
                    tokens.append(("abort_token", "abort"))
                    i += 4  # Move past "abort" (now i should point to the next character after "abort")
                    if i < len(input_string) and input_string[i] in self.delim12:
                        tokens.append(("delim12", input_string[i]))  # Lookahead for semicolon delimiter
                    state = 0
                    continue

                else:
                    raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 't' after 'abor'")

            elif state == 6:  # After "a", checking for "and"
                if char == 'n':  # Continue with "and"
                    state = 7
                else:
                    raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 'n' after 'a' in 'and'")

            elif state == 7:  # After "an", checking for "d" in "and"
                if char == 'd':  # Final state for "and"
                    tokens.append(("and_token", "and"))
                    i += 2  # Move past "and" (now i should point to the next character after "and")
                    if i < len(input_string) and input_string[i] in self.delim4:
                        tokens.append(("delim4", input_string[i]))  # Lookahead for delimiter
                    return tokens
                else:
                    raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 'd' after 'an'")

            i += 1  # Move to the next character if no transitions are made

        raise ValueError(f"Lexical Error: Incomplete keyword at position {i}, expected 'abort' or 'and'")


    def b_token(self, input_string, i):
        """Handles the 'b' case for 'back'."""
        tokens = []
        if input_string[i:i+4] == "back":
            tokens.append(("back_token", "back"))
            if i + 4 < len(input_string) and input_string[i + 4:i + 5] in self.delim4:
                tokens.append(("delim4", " "))
        if input_string[i:i+6] == "bounce":
            tokens.append(("bounce_token", "bounce"))
            if i + 6 < len(input_string) and input_string[i + 6:i + 7] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens
    
    def c_token(self, input_string, i):
        """Handles the 'c' case for 'chat'."""
        tokens = []
        if input_string[i:i+4] == "chat":
            tokens.append(("chat_token", "chat"))
            if i + 4 < len(input_string) and input_string[i + 4:i + 5] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def d_token(self, input_string, i):
        """Handles the 'd' case for 'define'."""
        tokens = []
        if input_string[i:i+6] == "define":
            tokens.append(("define_token", "define"))
            if i + 6 < len(input_string) and input_string[i + 6:i + 7] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def f_token(self, input_string, i):
        """Handles the 'f' case for 'function'."""
        tokens = []
        if input_string[i:i+8] == "function":
            tokens.append(("function_token", "function"))
            if i + 8 < len(input_string) and input_string[i + 8:i + 9] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def g_token(self, input_string, i):
        """Handles the 'g' case for 'glob'."""
        tokens = []
        if input_string[i:i+4] == "glob":
            tokens.append(("glob_token", "glob"))
            if i + 4 < len(input_string) and input_string[i + 4:i + 5] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def i_token(self, input_string, i):
        """Handles the 'i' case for 'input' or 'if'."""
        tokens = []
        if input_string[i:i+5] == "input":
            tokens.append(("input_token", "input"))
            if i + 5 < len(input_string) and input_string[i + 5:i + 6] in self.delim4:
                tokens.append(("delim4", " "))
        elif input_string[i:i+2] == "if":
            tokens.append(("if_token", "if"))
            if i + 2 < len(input_string) and input_string[i + 2:i + 3] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def l_token(self, input_string, i):
        """Handles the 'l' case for 'load'."""
        tokens = []
        if input_string[i:i+4] == "load":
            tokens.append(("load_token", "load"))
            if i + 4 < len(input_string) and input_string[i + 4:i + 5] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def n_token(self, input_string, i):
        """Handles the 'n' case for 'negate' or 'note'."""
        tokens = []
        if input_string[i:i+7] == "negate":
            tokens.append(("negate_token", "negate"))
            if i + 7 < len(input_string) and input_string[i + 7:i + 8] in self.delim4:
                tokens.append(("delim4", " "))
        elif input_string[i:i+4] == "note":
            tokens.append(("note_token", "note"))
            if i + 4 < len(input_string) and input_string[i + 4:i + 5] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def o_token(self, input_string, i):
        """Handles the 'o' case for 'output'."""
        tokens = []
        if input_string[i:i+6] == "output":
            tokens.append(("output_token", "output"))
            if i + 6 < len(input_string) and input_string[i + 6:i + 7] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def p_token(self, input_string, i):
        """Handles the 'p' case for 'print'."""
        tokens = []
        if input_string[i:i+5] == "print":
            tokens.append(("print_token", "print"))
            if i + 5 < len(input_string) and input_string[i + 5:i + 6] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def r_token(self, input_string, i):
        """Handles the 'r' case for 'read'."""
        tokens = []
        if input_string[i:i+4] == "read":
            tokens.append(("read_token", "read"))
            if i + 4 < len(input_string) and input_string[i + 4:i + 5] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def s_token(self, input_string, i):
        """Handles the 's' case for 'start'."""
        tokens = []
        if input_string[i:i+5] == "start":
            tokens.append(("start_token", "start"))
            if i + 5 < len(input_string) and input_string[i + 5:i + 6] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def t_token(self, input_string, i):
        """Handles the 't' case for 'token'."""
        tokens = []
        if input_string[i:i+5] == "token":
            tokens.append(("token_token", "token"))
            if i + 5 < len(input_string) and input_string[i + 5:i + 6] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens

    def w_token(self, input_string, i):
        """Handles the 'w' case for 'watch'."""
        tokens = []
        if input_string[i:i+5] == "watch":
            tokens.append(("watch_token", "watch"))
            if i + 5 < len(input_string) and input_string[i + 5:i + 6] in self.delim4:
                tokens.append(("delim4", " "))
        return tokens


# Main function
def main():
    # Prompt the user for input
    input_string = input("Enter a string to tokenize: ")
    tokenizer = DEDOSLexicalAnalyzer()

    try:
        # Tokenize the input string
        tokens = tokenizer.tokenize(input_string)

        # Print each token and lexeme
        for token_type, lexeme in tokens:
            print(f"Token: {token_type}, Lexeme: {lexeme}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
