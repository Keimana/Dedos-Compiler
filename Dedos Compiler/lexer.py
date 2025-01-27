class DEDOSLexicalAnalyzer:
    def __init__(self):
        # Define delimiters as instance variables
        self.delim1 = ['{']
        self.delim2 = ['~']
        self.delim3 = [' ']
        self.delim4 = ['(']
        self.delim5 = [' ', '(']
        self.delim6 = [' ', '^', ';', '}', '\n', '\0']
        self.delim7 = ['=', ' ']
        self.delim8 = [' ', '=', ')', '\0', '!']
        self.delim9 = [' ', 'num', "'", '(', '_', 'alpha', '"']
        self.delim10 = ['num', "'", '"', 'alpha', '[', '[', ']']
        self.delim11 = [' ', '\0', '\n']
        self.delim12 = [';']  # Semicolon delimiter
        self.delim13 = [' ', 'num', '"', 'alpha', '(', "'", 'and']
        self.delim14 = [' ', 'num', '(', '_']
        self.delim15 = [' ', 'num', '(', '_', '"']
        self.delim16 = ['^', ' ', '\0', '\n', '~']
        self.delim17 = [' ', '\0', 'num', 'alpha', '"', '(', "'", ')']
        self.delim18 = [' ', '\0', '\n', 'alpha', '+', '-', '*', '/', '%', '!', '=', '<', '>', ',', '}', ')', '{', ';']
        self.delim19 = ['=', '*', ')', ' ', '\0', '+', ']', '%', ',', '}', '/', '<', '[', '>', '\n', '!', '-']
        self.delim20 = [' ', '+', '=', '!', ',', '^', ')', '}', '\n', '\0', ']', ';']
        self.delim21 = ['\0', '}', ' ', '\n', '^']
        self.delim22 = ['\n', '\0', '^', ']', '%', '>', '+', '}', '\0', ',', '<', '/', '=', '*', ' ', '!', '-', ';', ')']
        self.delim23 = [']', '%', '>', '+', '}', '\0', ',', '<', '/', '=', '^', '*', ' ', '!', '-', '\n', ')']
        self.delim24 = [')', ']', '+', '=', '}', '*', '\0', ',', '/', '[', '<', '>', '-', ' ', '%', '(', '\n', '!']
        self.delim25 = [' ', '=', '(', ')', '\'', '"', '+', '-', '*', '/', '%', '>', '<', '!', '^', 'alpha', 'num', '[', ']'] 
        self.delim26 = [',', '+', '-', '*', '/', '%', '=', '<', '>', '!', '^', '\n', '\0', '}', ']', ' ', ',', ')']
        self.delim27 = [' ', '=', '!', ',', '^', ')', '}', '\n', '\0', ']']
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't','u', 'v', 'w', 'x', 'y', 'z']
        self.num = '0123456789'  # Digits for numeric literals
        self.zero = '0'


    def newline_token(self, input_string, i):
        """Handles newline characters as tokens."""
        tokens = []
        char = input_string[i]

        if char == '\n':  # Check for a newline character
            tokens.append(("newline_token", "\\n"))  # Add the newline token
            i += 1  # Move to the next character
        else:
            raise ValueError(f"Lexical Error: Expected newline at position {i}, but got '{char}' instead.")

        return tokens, i
    
    def parse_number(self, input_string, i, is_negative=False):
        """
        Parses whole numbers and floating-point numbers.
        Supports negative numbers when `is_negative=True`.
        """
        tokens = []
        start_index = i
        number_str = "-" if is_negative else ""  # Start with a negative sign if applicable
        lhs_digit_count = 0
        rhs_digit_count = 0
        decimal_point_seen = False

        while i < len(input_string) and (input_string[i].isdigit() or input_string[i] == '.'):
            if input_string[i] == '.':
                if decimal_point_seen:  # Ensure only one decimal point
                    raise ValueError(f"Lexical Error: Multiple decimal points in numeric literal at position {start_index}")
                decimal_point_seen = True
                number_str += '.'
            elif not decimal_point_seen:
                lhs_digit_count += 1
                if lhs_digit_count > 15:
                    raise ValueError(f"Lexical Error: Exceeds 15 digits in LHS at position {start_index}")
                number_str += input_string[i]
            else:
                rhs_digit_count += 1
                if rhs_digit_count > 15:
                    raise ValueError(f"Lexical Error: Exceeds 15 digits in RHS at position {start_index}")
                number_str += input_string[i]
            i += 1

        if decimal_point_seen:
            tokens.append(("flank_token", number_str))  # Floating-point literal
        else:
            tokens.append(("inst_lit", number_str))  # Whole number literal

        return tokens, i

    def handle_comments(self, input_string, i):
        """
        Determines whether the comment is a single-line (^^) or multi-line (^^^) comment and processes it.
        """
        if input_string[i:i + 2] == "^^":
            return self.handle_single_line_comment(input_string, i)
        elif input_string[i:i + 3] == "^^^":
            return self.handle_multi_line_comment(input_string, i)
        else:
            raise ValueError(f"Lexical Error: Invalid comment start at position {i} ({input_string[i]})")


    def handle_single_line_comment(self, input_string, i):
        """
        Handles single-line comments (^^...^^).
        """
        tokens = []
        start_index = i
        end_sequence = "^^"
        i += 2  # Move past the opening '^^'
        comment_content = ""

        while i < len(input_string):
            # Check for the closing sequence
            if input_string[i:i + len(end_sequence)] == end_sequence:
                i += len(end_sequence)  # Move past the closing sequence
                tokens.append(("single_line_comment", comment_content))
                return tokens, i  # Return the tokens and the updated index

            # Append the current character to the comment content
            comment_content += input_string[i]
            i += 1  # Increment the index

        # If we exit the loop without finding the closing sequence, raise an error
        raise ValueError(f"Lexical Error: Unclosed comment starting at position {start_index}")


    def handle_multi_line_comment(self, input_string, i):
        """
        Handles multi-line comments (^^^...^^^).
        """
        tokens = []
        start_index = i
        end_sequence = "^^^"
        i += 3  # Move past the opening '^^^'
        comment_content = ""

        while i < len(input_string):
            # Check for the closing sequence
            if input_string[i:i + len(end_sequence)] == end_sequence:
                i += len(end_sequence)  # Move past the closing sequence
                tokens.append(("multi_line_comment", comment_content))
                return tokens, i  # Return the tokens and the updated index

            # Append the current character to the comment content
            comment_content += input_string[i]
            i += 1  # Increment the index

        # If we exit the loop without finding the closing sequence, raise an error
        raise ValueError(f"Lexical Error: Unclosed comment starting at position {start_index}")


    def is_alpha(self, char):
        """Check if the character is alphabetic."""
        return char in self.alpha  # Check if char is in the alpha list

    def is_num(self, char):
        """Check if the character is numeric."""
        return char in self.num  # Check if char is in the num list

    def raise_unexpected_identifier(self, lexeme, position):
        """Raises a generalized error for unexpected identifiers."""
        raise ValueError(f"Lexical Error: Unexpected identifier '{lexeme}' at position {position}")

    def flank_token(self, input_string, i):
        """
        Handles numeric literals, ensuring the LHS and RHS lengths do not exceed specified limits.
        If no decimal point is encountered, the number is treated as an integer literal.
        Additionally, raises an error if a decimal point is not preceded or followed by digits (e.g., '1.x', 'x.1').
        """
        tokens = []
        start_index = i
        lhs_digit_count = 0  # Count digits on the left-hand side of the decimal point
        rhs_digit_count = 0  # Count digits on the right-hand side of the decimal point
        number_str = ""  # Accumulates the full number string
        decimal_point_seen = False  # Tracks if a decimal point has been encountered

        # Ensure the input starts with a digit (or raise an error)
        if not input_string[i].isdigit():
            raise ValueError(f"Lexical Error: Invalid numeric literal start at position {start_index} ({input_string[i]})")

        while i < len(input_string) and (input_string[i].isdigit() or (input_string[i] == '.' and not decimal_point_seen)):
            if input_string[i] == '.':
                decimal_point_seen = True  # Mark that a decimal point has been seen
                number_str += input_string[i]  # Add the decimal point to the number string
                i += 1  # Move past the decimal point

                # Raise an error if the decimal point is not followed by a digit
                if i >= len(input_string) or not input_string[i].isdigit():
                    raise ValueError(f"Lexical Error: Expected digits after decimal point at position {start_index}")

                continue

            # Count digits in LHS or RHS based on whether a decimal point has been seen
            if not decimal_point_seen:
                lhs_digit_count += 1
                if lhs_digit_count > 15:  # LHS cannot exceed 15 digits
                    raise ValueError(f"Lexical Error: Exceeds 15 digits at position {start_index}")
            else:
                rhs_digit_count += 1
                if rhs_digit_count > 15:  # RHS cannot exceed 15 digits
                    raise ValueError(f"Lexical Error: Exceeds 15 digits at position {start_index}")

            number_str += input_string[i]  # Append the digit to the number string
            i += 1

        # Ensure there is at least one digit in the LHS
        if lhs_digit_count == 0:
            raise ValueError(f"Lexical Error: Expected LHS numeric literal at position {start_index}")

        # Determine the token type based on whether a decimal point was seen
        if decimal_point_seen:
            tokens.append(("flank_token", number_str))  # Floating-point token
        else:
            tokens.append(("inst_lit", number_str))  # Integer literal token

        # Lookahead for valid delimiter (delim22)
        if i < len(input_string) and input_string[i] in self.delim22:
            tokens.append((input_string[i], input_string[i]))  # Add the delimiter token
            i += 1  # Move past the delimiter

        # Return the tokens and the updated index
        return tokens, i

    def chat_lit_token(self, input_string, i):
        """
        Handles string literals (chat literals) delimited by double quotes, allowing one or more characters inside.
        Ensures a valid delimiter follows the closing quote.
        """
        tokens = []
        start_index = i
        string_literal = ""  # To accumulate the characters inside the string literal

        # Move past the opening double quote
        i += 1

        # Collect characters inside the double quotes
        while i < len(input_string) and input_string[i] != '"':
            # Handle escape sequences (e.g., '\n', '\t', '\\', '\"', etc.)
            if input_string[i] == '\\' and i + 1 < len(input_string):
                # Handle common escape sequences
                if input_string[i + 1] in ['\\', '"', 'n', 't']:
                    string_literal += input_string[i + 1]  # Append the escaped character
                    i += 2  # Skip the escape character and the next character
                else:
                    string_literal += input_string[i]  # Add the backslash
                    i += 1
            else:
                string_literal += input_string[i]  # Regular character
                i += 1

        # Ensure we find the closing double quote
        if i < len(input_string) and input_string[i] == '"':
            tokens.append(("chat_lit", string_literal))  # Add the string literal as a token
            i += 1  # Move past the closing quote
        else:
            raise ValueError(f"Lexical Error: Missing closing double quote for string literal at position {start_index}")

        # Ensure a valid delimiter follows the closing double quote
        if i < len(input_string) and input_string[i] in self.delim20:  # Check for a valid delimiter
            tokens.append((input_string[i], input_string[i]))  # Add the delimiter token
            i += 1  # Move past the delimiter
        else:
            raise ValueError(f"Lexical Error: Missing delimiter after string literal at position {i}")

        return tokens, i

    def strike_token(self, input_string, i):
        """
        Handles string literals (strike literals) delimited by single quotes, allowing only one character.
        Ensures a valid delimiter follows the closing quote.
        """
        tokens = []
        start_index = i
        string_literal = ""  # To accumulate the characters inside the string literal

        # Move past the opening quote
        i += 1

        # Collect the single character inside the quotes
        if i < len(input_string) and input_string[i] != "'":  # Ensure there's a character before closing quote
            string_literal += input_string[i]  # Append the character to the string literal
            i += 1

        # Check if there's more than one character
        if len(string_literal) > 1:
            raise ValueError(f"Lexical Error: Only one character allowed in a string literal at position {start_index}")

        # Check if we encountered a closing quote
        if i < len(input_string) and input_string[i] == "'":
            tokens.append(("strike_lit", string_literal))  # Add the string literal as a token
            i += 1  # Move past the closing quote
        else:
            raise ValueError(f"Lexical Error: Unmatched quote at position {start_index}")

        # Ensure a valid delimiter follows the closing quote
        if i < len(input_string) and input_string[i] in self.delim20:  # Check for a valid delimiter
            tokens.append((input_string[i], input_string[i]))  # Add the delimiter token
            i += 1  # Move past the delimiter
        else:
            raise ValueError(f"Lexical Error: Missing delimiter after string literal at position {i}")

        return tokens, i

    def delimiterHandling(self, char, expected_delim, token_name):
        """Handles the check for the correct delimiter after a token."""
        if char not in expected_delim:
            raise ValueError(f"Lexical Error: Expected delimiter after '{token_name}' token, but got '{char}' instead.")
        return True

    def a_token(self, input_string, i):
        """Handles both 'abort' and 'and' tokens, ensuring they are followed by a valid delimiter."""
        try:
            tokens = []
            state = 0  # Initial state for 'a'
            length = len(input_string)
            lexeme = ""  # To accumulate the lexeme

            if input_string[i] != 'a':  # If the first character is not 'a', raise an error
                raise ValueError(f"Lexical Error: Expected 'a' at position {i}")

            while i < length:
                char = input_string[i]
                print(f"State: {state}, Char: {char}, Lexeme: {lexeme}")

                if state == 0:  # Expecting 'a'
                    if char == 'a':
                        lexeme += char
                        state = 1
                    else:
                        raise ValueError(f"Lexical Error: Unexpected character '{char}' after 'a' at position {i}")

                elif state == 1:  # After 'a', expecting 'b' for 'abort' or 'n' for 'and'
                    if char == 'b':  # Proceed to 'b' for 'abort'
                        lexeme += char
                        state = 2
                    elif char == 'n':  # Proceed to 'n' for 'and'
                        lexeme += char
                        state = 7
                    else:
                        raise ValueError(f"Lexical Error: Incomplete token 'a' at position {i}")

                elif state == 2:  # After 'b', expecting 'o' for 'abort'
                    if char == 'o':
                        lexeme += char
                        state = 3
                    else:
                        raise ValueError(f"Lexical Error: Incomplete 'abort' at position {i}")

                elif state == 3:  # After 'o', expecting 'r' for 'abort'
                    if char == 'r':
                        lexeme += char
                        state = 4
                    else:
                        raise ValueError(f"Lexical Error: Incomplete 'abort' at position {i}")

                elif state == 4:  # After 'r', expecting 't' for 'abort'
                    if char == 't':
                        lexeme += char
                        state = 5
                    else:
                        raise ValueError(f"Lexical Error: Incomplete 'abort' at position {i}")

                elif state == 5:  # After 't', check for delimiters
                    if self.delimiterHandling(char, self.delim12, "abort"):  # Handle valid delimiter
                        tokens.append(("abort_token", "abort"))  # Successfully identified 'abort'
                        tokens.append((";", ";"))
                        i += 1
                        break
                    else:
                        raise ValueError(f"Lexical Error: Expected delimiter after 'abort' at position {i + 1}")

                elif state == 7:  # After 'n', expecting 'd' for 'and'
                    if char == 'd':
                        lexeme += char
                        state = 8
                    else:
                        raise ValueError(f"Lexical Error: Incomplete 'and' at position {i}")

                elif state == 8:  # After 'd', check for delimiters
                    tokens.append(("and_token", "and"))  # Successfully identified 'and'
                    if char == ' ':  # Handle spaces
                        space_tokens, i = self.space_token(input_string, i)
                        tokens.extend(space_tokens)
                        break
                    elif self.delimiterHandling(char, self.delim5, "and"):  # Handle valid delimiter
                        tokens.append((char, char))
                        i += 1
                        break
                    else:
                        raise ValueError(f"Lexical Error: Expected delimiter after 'and' at position {i + 1}")

                i += 1  # Move to the next character

            # If we exit the loop without completing a token, raise an error
            if state in {1, 2, 3, 4, 7}:
                raise ValueError(f"Lexical Error: Incomplete token '{lexeme}' at end of input.")

            return tokens, i

        except ValueError as e:
            # Reraise the error to be handled in the analyze_code function
            raise ValueError(str(e)) from e

    def b_token(self, input_string, i):
        """Handles both 'back' and 'bounce' tokens, ensuring they are followed by a valid delimiter."""
        tokens = []
        state = 0  # Initial state for 'b'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 0:  # Expecting 'b'
                if char == 'b':
                    state = 1
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 1:  # After 'b', check for 'a' for 'back' or 'o' for 'bounce'
                if char == 'a':  # Proceed to 'a' for 'back'
                    state = 2
                elif char == 'o':  # Proceed to 'o' for 'bounce'
                    state = 5
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 2:  # After 'a', expecting 'c' for 'back'
                if char == 'c':
                    state = 3
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 3:  # After 'c', expecting 'k' for 'back'
                if char == 'k':
                    state = 4
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 4:  # After 'k', lookahead for delimiters (space or semicolon) for 'back'
                if char in self.delim4:  # Space or parentheses
                    tokens.append(("back_token", "back"))
                    tokens.append((char, char))  # Lookahead for space or parentheses
                    i += 1
                    break
                elif char in self.delim12:  # Semicolon
                    tokens.append(("back_token", "back"))
                    tokens.append((char, char))  # Lookahead for semicolon
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'back' at position {i}")

            elif state == 5:  # After 'o', expecting 'u' for 'bounce'
                if char == 'u':
                    state = 6
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 6:  # After 'u', expecting 'n' for 'bounce'
                if char == 'n':
                    state = 7
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 7:  # After 'n', expecting 'c' for 'bounce'
                if char == 'c':
                    state = 8
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 8:  # After 'c', expecting 'e' for 'bounce'
                if char == 'e':
                    state = 9
                else:
                    self.raise_unexpected_identifier(char, i)  # Handle unexpected identifier

            elif state == 9:  # After 'e', lookahead for delimiters (space or semicolon) for 'bounce'

                if char in self.delim12:  # Semicolon
                    tokens.append(("bounce_token", "bounce"))
                    tokens.append((char, char))  # Lookahead for semicolon
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'bounce' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def c_token(self, input_string, i):
        """Handles the 'chat' token."""
        tokens = []
        state = 21  # Initial state for 'chat'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 21:  # Expecting 'c'
                if char == 'c':
                    state = 22
                else:
                    raise ValueError(f"Lexical Error: Expected 'c' at position {i}")
            elif state == 22:  # After 'c', expecting 'h'
                if char == 'h':
                    state = 23
                else:
                    raise ValueError(f"Lexical Error: Expected 'h' at position {i}")
            elif state == 23:  # After 'h', expecting 'a'
                if char == 'a':
                    state = 24
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' at position {i}")
            elif state == 24:  # After 'a', expecting 't'
                if char == 't':
                    state = 25

                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")
            elif state == 25:  # After 't', lookahead for delimiter (space)
                if char in self.delim3:
                    tokens.append(("chat_token", "chat"))  # Lookahead for delimiter
                    tokens.append((char, char))  # Lookahead for delimiter
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'chat' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def d_token(self, input_string, i):
        """Handles the 'defuse' token."""
        tokens = []
        state = 26  # Initial state for 'defuse'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 26:  # Expecting 'd'
                if char == 'd':
                    state = 27
                else:
                    raise ValueError(f"Lexical Error: Expected 'd' at position {i}")
            elif state == 27:  # After 'd', expecting 'e'
                if char == 'e':
                    state = 28
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' at position {i}")
            elif state == 28:  # After 'e', expecting 'f'
                if char == 'f':
                    state = 29
                else:
                    raise ValueError(f"Lexical Error: Expected 'f' at position {i}")
            elif state == 29:  # After 'f', expecting 'u'
                if char == 'u':
                    state = 30
                else:
                    raise ValueError(f"Lexical Error: Expected 'u' at position {i}")
            elif state == 30:  # After 'u', expecting 's'
                if char == 's':
                    state = 31
                else:
                    raise ValueError(f"Lexical Error: Expected 's' at position {i}")
            elif state == 31:  # After 's', expecting 'e'
                if char == 'e':
                    state = 32
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' at position {i}")
            elif state == 32:  # After 'e', lookahead for delimiter (space)
                if char in self.delim3:
                    tokens.append(("defuse_token", "defuse"))  # Lookahead for delimiter

                    tokens.append((char, char))  # Lookahead for delimiter
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'defuse' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def f_token(self, input_string, i):
        """Handles both 'flank' and 'force' tokens."""
        tokens = []
        state = 33  # Initial state for 'f'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 33:  # Expecting 'f'
                if char == 'f':
                    state = 34
                else:
                    raise ValueError(f"Lexical Error: Expected 'f' at position {i}")

            elif state == 34:  # After 'f', expecting 'l' for 'flank'
                if char == 'l':
                    state = 35
                elif char == 'o':  # For 'force'
                    state = 39
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' or 'o' at position {i}")

            elif state == 35:  # After 'l', expecting 'a' for 'flank'
                if char == 'a':
                    state = 36
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' at position {i}")

            elif state == 36:  # After 'a', expecting 'n' for 'flank'
                if char == 'n':
                    state = 37
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' at position {i}")

            elif state == 37:  # After 'n', expecting 'k' for 'flank'
                if char == 'k':
                    state = 38
                else:
                    raise ValueError(f"Lexical Error: Expected 'k' at position {i}")

            elif state == 38:  # After 'k', lookahead for delimiter (space, newline, or semicolon) for 'flank'
                if char in self.delim3:  # Space, newline, or semicolon
                    tokens.append(("flank_token", "flank"))
                    tokens.append((char, char))  # Lookahead for delimiter
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'flank' at position {i}")

            elif state == 39:  # After 'o', expecting 'r' for 'force'
                if char == 'r':
                    state = 40
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' at position {i}")

            elif state == 40:  # After 'r', expecting 'c' for 'force'
                if char == 'c':
                    state = 41
                else:
                    raise ValueError(f"Lexical Error: Expected 'c' at position {i}")

            elif state == 41:  # After 'c', expecting 'e' for 'force'
                if char == 'e':
                    state = 42
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' at position {i}")

            elif state == 42:  # After 'e', lookahead for delimiter (space, newline, or semicolon) for 'force'
                if char in self.delim3:  # Space, newline, or semicolon
                    tokens.append(("force_token", "force"))
                    tokens.append((char, char))  # Lookahead for delimiter
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'force' at position {i}")

            i += 1  # Move to the next character

        return tokens, i
        
    def g_token(self, input_string, i):
        """Handles the 'globe' token."""
        tokens = []
        state = 44  # Initial state for 'g'
        length = len(input_string)
        lexeme = ""  # To accumulate the lexeme

        while i < length:
            char = input_string[i]

            if state == 44:  # Expecting 'g'
                if char == 'g':
                    lexeme += char  # Add to lexeme
                    state = 45
                else:
                    raise ValueError(f"Lexical Error: Expected 'g' at position {i}")

            elif state == 45:  # After 'g', expecting 'l'
                if char == 'l':
                    lexeme += char  # Add to lexeme
                    state = 46
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' at position {i}")

            elif state == 46:  # After 'l', expecting 'o'
                if char == 'o':
                    lexeme += char  # Add to lexeme
                    state = 47
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            elif state == 47:  # After 'o', expecting 'b'
                if char == 'b':
                    lexeme += char  # Add to lexeme
                    state = 48
                else:
                    raise ValueError(f"Lexical Error: Expected 'b' at position {i}")

            elif state == 48:  # After 'b', expecting 'e'
                if char == 'e':
                    lexeme += char  # Add to lexeme
                    state = 49
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' at position {i}")

            elif state == 49:  # After 'e', lookahead for delimiter
                if char in self.delim3:  # Valid delimiters: space, newline, or semicolon
                    tokens.append(("globe_token", lexeme))  # Append the globe token with lexeme
                    tokens.append((char, char))  # Append the delimiter as a token
                    i += 1  # Move past the delimiter
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'globe' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def i_token(self, input_string, i):
        """Handles the 'info', 'inst', and 'in' tokens."""
        tokens = []
        state = 50  # Initial state for 'i'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 50:  # Expecting 'i'
                if char == 'i':
                    state = 51
                else:
                    raise ValueError(f"Lexical Error: Expected 'i' at position {i}")

            elif state == 51:  # After 'i', expecting 'n'
                if char == 'n':
                    state = 52
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' at position {i}")

            elif state == 52:  # After 'n', lookahead for delimiter (delim3 for 'in') or 'f'/'s' for 'info'/'inst'
                if char in self.delim3:  # Delimiter after 'in'
                    tokens.append(("in_token", "in"))  # Recognized 'in'
                    tokens.append((char, char))  # Add the delimiter
                    i += 1
                    break
                elif char == 'f':  # Continue to 'f' for 'info'
                    state = 53
                elif char == 's':  # Continue to 's' for 'inst'
                    state = 56
                else:
                    raise ValueError(f"Lexical Error: Expected 'f', 's', or a delimiter after 'in' at position {i}")

            elif state == 53:  # After 'f', expecting 'o' for 'info'
                if char == 'o':
                    state = 54
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            elif state == 54:  # After 'o', lookahead for delimiters (delim4) for 'info'
                if char in self.delim4:  # Delimiter for 'info'
                    tokens.append(("info_token", "info"))  # Recognized 'info'
                    tokens.append((char, char))  # Add the delimiter
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'info' at position {i}")

            elif state == 56:  # After 's', expecting 't' for 'inst'
                if char == 't':
                    state = 57
                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")

            elif state == 57:  # After 't', lookahead for delimiters (delim3) for 'inst'
                if char in self.delim3:  # Delimiter for 'inst'
                    tokens.append(("inst_token", "inst"))  # Recognized 'inst'
                    tokens.append((char, char))  # Add the delimiter
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'inst' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def l_token(self, input_string, i):
        """Handles the 'load' token."""
        tokens = []
        state = 59  # Initial state for 'l'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 59:  # Expecting 'l'
                if char == 'l':
                    state = 60
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' at position {i}")

            elif state == 60:  # After 'l', expecting 'o'
                if char == 'o':
                    state = 61
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            elif state == 61:  # After 'o', expecting 'a'
                if char == 'a':
                    state = 62
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' at position {i}")

            elif state == 62:  # After 'a', expecting 'd'
                if char == 'd':
                    state = 63
                else:
                    raise ValueError(f"Lexical Error: Expected 'd' at position {i}")

            elif state == 63:  # After 'd', lookahead for delimiter (parentheses)
                if char in self.delim4:
                    tokens.append(("load_token", "load"))
                    tokens.append((char, char))  # Lookahead for parentheses
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected delimiter after 'load' at position {i}")

            i += 1  # Move to the next character

        return tokens, i
    
    def n_token(self, input_string, i):
        """Handles the 'neg' and 'not' tokens, ensuring invalid tokens like 'negot' are rejected."""
        tokens = []
        state = 64  # Initial state for 'n'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            if state == 64:  # Expecting 'n'
                if char == 'n':
                    state = 65
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' at position {i}")

            elif state == 65:  # After 'n', expecting 'e' for 'neg' or 'o' for 'not'
                if char == 'e':
                    state = 66
                elif char == 'o':
                    state = 68
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' or 'o' at position {i}")

            elif state == 66:  # After 'e', expecting 'g' for 'neg'
                if char == 'g':
                    state = 67
                else:
                    raise ValueError(f"Lexical Error: Expected 'g' at position {i}")

            elif state == 67:  # After 'g', expecting a valid delimiter (delim87)
                tokens.append(("neg_token", "neg"))  # Successfully identified 'neg'
                if char in self.delim8:  # Check for valid delimiter
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected a delimiter after 'neg' at position {i}")

            elif state == 68:  # After 'o', expecting 't' for 'not'
                if char == 't':
                    state = 69
                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")

            elif state == 69:  # After 't', expecting a valid delimiter (delim4)
                tokens.append(("not_token", "not"))  # Successfully identified 'not'
                if char in self.delim4:  # Check for valid delimiter
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Expected a delimiter after 'not' at position {i}")

            else:
                raise ValueError(f"Lexical Error: Invalid state at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def o_token(self, input_string, i):
        """Handles tokens starting with 'o', specifically 'or'."""
        tokens = []
        state = 71  # Initial state for 'o'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Initial state: Expecting 'o'
            if state == 71:
                if char == 'o':
                    state = 72
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            # After 'o', expecting 'r'
            elif state == 72:
                if char == 'r':
                    state = 73
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' at position {i}")

            # After 'or', expecting a lookahead delimiter (delim 5)
            elif state == 73:
                tokens.append(("or_token", "or"))
                if char in self.delim5:  # Lookahead for 'delim 5'
                    tokens.append((char, char))
                    i += 1  # Move past the delimiter
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'or' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def p_token(self, input_string, i):
        """Handles the 'plant', 'perim', 'pos', and 'push' tokens."""
        tokens = []
        state = 74  # Initial state for 'p'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Initial state: Expecting 'p'
            if state == 74:  # Expecting 'p' for all tokens
                if char == 'p':
                    state = 75
                else:
                    raise ValueError(f"Lexical Error: Expected 'p' at position {i}")

            # Determine the token type based on the next character
            elif state == 75:  # After 'p'
                if char == 'l':  # Start of 'plant'
                    state = 80
                elif char == 'e':  # Start of 'perim'
                    state = 76
                elif char == 'o':  # Start of 'pos'
                    state = 85
                elif char == 'u':  # Start of 'push'
                    state = 88
                else:
                    raise ValueError(f"Lexical Error: Expected 'l', 'e', 'o', or 'u' after 'p' at position {i}")

            # Handle 'perim'
            elif state == 76:  # After 'e', expecting 'r'
                if char == 'r':
                    state = 77
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' at position {i}")
            elif state == 77:  # After 'r', expecting 'i'
                if char == 'i':
                    state = 78
                else:
                    raise ValueError(f"Lexical Error: Expected 'i' at position {i}")
            elif state == 78:  # After 'i', expecting 'm'
                if char == 'm':
                    state = 79
                else:
                    raise ValueError(f"Lexical Error: Expected 'm' at position {i}")
            elif state == 79:  # After 'perim', lookahead for delimiters
                tokens.append(("perim_token", "perim"))
                if char in self.delim4:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'perim' at position {i}")

            # Handle 'plant'
            elif state == 80:  # After 'l', expecting 'a'
                if char == 'a':
                    state = 81
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' at position {i}")
            elif state == 81:  # After 'a', expecting 'n'
                if char == 'n':
                    state = 82
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' at position {i}")
            elif state == 82:  # After 'n', expecting 't'
                if char == 't':
                    state = 83
                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")
            elif state == 83:  # After 'plant', lookahead for delimiters
                tokens.append(("plant_token", "plant"))
                if char in self.delim4:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'plant' at position {i}")

            # Handle 'pos'
            elif state == 85:  # After 'o', expecting 's'
                if char == 's':
                    state = 86
                else:
                    raise ValueError(f"Lexical Error: Expected 's' at position {i}")
            elif state == 86:  # After 'pos', lookahead for delimiters
                tokens.append(("pos_token", "pos"))
                if char in self.delim8:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'pos' at position {i}")

            # Handle 'push'
            elif state == 88:  # After 'u', expecting 's'
                if char == 's':
                    state = 89
                else:
                    raise ValueError(f"Lexical Error: Expected 's' at position {i}")
            elif state == 89:  # After 's', expecting 'h'
                if char == 'h':
                    state = 90
                else:
                    raise ValueError(f"Lexical Error: Expected 'h' at position {i}")
            elif state == 90:  # After 'push', lookahead for delimiters
                tokens.append(("push_token", "push"))
                if char in self.delim12:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'push' at position {i}")

            i += 1  # Move to the next character

        return tokens, i

    def r_token(self, input_string, i):
        """Handles tokens starting with 'r', specifically 'reload'."""
        tokens = []
        state = 92  # Initial state for 'r'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Initial state: Expecting 'r'
            if state == 92:
                if char == 'r':
                    state = 93
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' at position {i}")

            # After 'r', expecting 'e'
            elif state == 93:
                if char == 'e':
                    state = 94
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' at position {i}")

            # After 're', expecting a lookahead delimiter (delim 4) or 'l' for 'reload'
            elif state == 94:
                if char in self.delim4:  # Lookahead delimiter
                    tokens.append(("re_token", "re"))
                    tokens.append((char, char))
                    i += 1
                    break
                elif char == 'l':  # Continue for 'reload'
                    state = 95
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 're' at position {i}")

            # After 'l', expecting 'o'
            elif state == 95:
                if char == 'o':
                    state = 96
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            # After 'o', expecting 'a'
            elif state == 96:
                if char == 'a':
                    state = 97
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' at position {i}")

            # After 'a', expecting 'd'
            elif state == 97:
                if char == 'd':
                    state = 98
                else:
                    raise ValueError(f"Lexical Error: Expected 'd' at position {i}")

            # After 'reload', expecting a lookahead delimiter (delim 1)
            elif state == 98:
                tokens.append(("reload_token", "reload"))
                if char in self.delim1:
                    tokens.append(("delim1", char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'reload' at position {i}")

            i += 1

        return tokens, i

    def s_token(self, input_string, i):
        """Handles tokens starting with 's', specifically 'strike'."""
        tokens = []
        state = 100  # Initial state for 's'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Initial state: Expecting 's'
            if state == 100:
                if char == 's':
                    state = 101
                else:
                    raise ValueError(f"Lexical Error: Expected 's' at position {i}")

            # After 's', expecting 't'
            elif state == 101:
                if char == 't':
                    state = 102
                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")

            # After 't', expecting 'r'
            elif state == 102:
                if char == 'r':
                    state = 103
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' at position {i}")

            # After 'r', expecting 'i'
            elif state == 103:
                if char == 'i':
                    state = 104
                else:
                    raise ValueError(f"Lexical Error: Expected 'i' at position {i}")

            # After 'i', expecting 'k'
            elif state == 104:
                if char == 'k':
                    state = 105
                else:
                    raise ValueError(f"Lexical Error: Expected 'k' at position {i}")

            # After 'k', expecting 'e'
            elif state == 105:
                if char == 'e':
                    state = 106
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' at position {i}")

            # After 'strike', expecting a lookahead delimiter (delim 3)
            elif state == 106:
                tokens.append(("strike_token", "strike"))
                if char in self.delim3:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'strike' at position {i}")

            i += 1

        return tokens, i

    def t_token(self, input_string, i):
        """Handles tokens starting with 't', specifically 'tool'."""
        tokens = []
        state = 107  # Initial state for 't'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Initial state: Expecting 't'
            if state == 107:
                if char == 't':
                    state = 108
                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")

            # After 't', expecting 'o'
            elif state == 108:
                if char == 'o':
                    state = 109
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            # After 'o', expecting 'o'
            elif state == 109:
                if char == 'o':
                    state = 110
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' at position {i}")

            # After 'o', expecting 'l'
            elif state == 110:
                if char == 'l':
                    state = 111
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' at position {i}")

            # After 'tool', expecting a lookahead delimiter (delim 3)
            elif state == 111:
                tokens.append(("tool_token", "tool"))
                if char in self.delim3:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'tool' at position {i}")

            i += 1

        return tokens, i

    def w_token(self, input_string, i):
        """Handles tokens starting with 'w', specifically 'watch'."""
        tokens = []
        state = 112  # Initial state for 'w'
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Initial state: Expecting 'w'
            if state == 112:
                if char == 'w':
                    state = 113
                else:
                    raise ValueError(f"Lexical Error: Expected 'w' at position {i}")

            # After 'w', expecting 'a'
            elif state == 113:
                if char == 'a':
                    state = 114
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' at position {i}")

            # After 'a', expecting 't'
            elif state == 114:
                if char == 't':
                    state = 115
                else:
                    raise ValueError(f"Lexical Error: Expected 't' at position {i}")

            # After 't', expecting 'c'
            elif state == 115:
                if char == 'c':
                    state = 116
                else:
                    raise ValueError(f"Lexical Error: Expected 'c' at position {i}")

            # After 'c', expecting 'h'
            elif state == 116:
                if char == 'h':
                    state = 117
                else:
                    raise ValueError(f"Lexical Error: Expected 'h' at position {i}")

            # After 'watch', expecting a lookahead delimiter (delim 4)
            elif state == 117:
                tokens.append(("watch_token", "watch"))
                if char in self.delim4:
                    tokens.append((char, char))
                    i += 1
                    break
                else:
                    raise ValueError(f"Lexical Error: Unexpected character after 'watch' at position {i}")

            i += 1

        return tokens, i

    def token_operator(self, input_string, i, prev_token=None):
        """
        Handles assignment operators, arithmetic operators, comparison operators, 
        and distinguishes between a subtraction operator and a negative sign.
        """
        tokens = []
        char = input_string[i]

        # Handle assignment operators
        if char == '=':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("equal_to_operator", "=="))
                i += 1  # Skip the next '=' character
            else:
                tokens.append(("assignment_operator", "="))

        # Handle addition, subtraction, multiplication, division, modulo
        elif char == '+':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("add_assignment_operator", "+="))
                i += 1  # Skip the '=' character
            else:
                tokens.append(("add_operator", "+"))

        # Handle addition, subtraction, and negative numbers
        elif char == '-':
            # Check context to determine if it's a negative number or subtraction
            if prev_token is None or prev_token in {'(', ',', '=', '+', '-', '*', '/', '%', '<', '>', '!'}:
                # If a valid preceding token suggests a negative number, parse the numeric literal
                i += 1  # Move past the negative sign
                if i < len(input_string) and (input_string[i].isdigit() or input_string[i] == '.'):
                    # Parse the number (whole or floating-point)
                    number_tokens, i = self.parse_number(input_string, i, is_negative=True)
                    tokens.extend(number_tokens)
                else:
                    raise ValueError(f"Lexical Error: Expected numeric literal after '-' at position {i - 1}")
            elif i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("subtract_assignment_operator", "-="))
                i += 1  # Skip the '=' character
            else:
                tokens.append(("minus_operator", "-"))

        elif char == '*':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("multiply_assignment_operator", "*="))
                i += 1  # Skip the '=' character
            elif i + 1 < len(input_string) and input_string[i + 1] == '*':
                tokens.append(("exponent_operator", "**"))
                i += 1  # Skip the next '*' character
            else:
                tokens.append(("multiply_operator", "*"))

        elif char == '/':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("divide_assignment_operator", "/="))
                i += 1  # Skip the '=' character
            elif i + 1 < len(input_string) and input_string[i + 1] == '/':
                tokens.append(("floor_div_operator", "//"))
                i += 1  # Skip the next '/' character
            else:
                tokens.append(("divide_operator", "/"))

        elif char == '%':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("mod_assignment_operator", "%="))
                i += 1  # Skip the '=' character
            else:
                tokens.append(("mod_operator", "%"))

        # Handle comparison operators
        elif char == '>':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("greater_than_or_equal_operator", ">="))
                i += 1  # Skip the next '=' character
            else:
                tokens.append(("greater_than_operator", ">"))

        elif char == '<':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("less_than_or_equal_operator", "<="))
                i += 1  # Skip the next '=' character
            else:
                tokens.append(("less_than_operator", "<"))

        elif char == '!':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("not_equal_to_operator", "!="))
                i += 1  # Skip the next '=' character
            else:
                raise ValueError(f"Lexical Error: Unexpected operator '{char}' at position {i}")

        else:
            raise ValueError(f"Lexical Error: Unexpected operator '{char}' at position {i}")

        return tokens, i + 1

    def space_token(self, input_string, i):
        """
        Handles space (' ') as a token, ensuring it is added to the tokens list.
        Also checks for valid delimiters (delim25) after spaces.
        """
        tokens = []
        state = 126  # State for processing space tokens

        while i < len(input_string) and input_string[i] == ' ':  # While the character is a space
            tokens.append(("space_token", " "))  # Add the space as a token
            i += 1  # Move to the next character

            # Check for delimiters in delim25 after processing spaces
            if i < len(input_string) and input_string[i] in self.delim25:  # Handle ' ' or '='
                tokens.append((input_string[i], input_string[i]))  # Add the delimiter as a token
                state = 127  # Transition to delimiter state
                i += 1  # Move past the delimiter
                break  # Exit after handling the delimiter

        return tokens, i

    def otherSymbols(self, input_string, i):
        """Handles tokens like `{`, `}`, `(`, `)`, spaces, and newlines with proper delimiter validation."""
        tokens = []
        state = None  # Tracks the current state
        char = input_string[i]

        # Handle `{` token
        if char == '{':
            state = 118
            tokens.append(("{", "{"))
            i += 1  # Move past the `{`

            # Check for delim11 after `{`
            if i < len(input_string) and input_string[i] in self.delim11:
                tokens.append(("delim11", input_string[i]))
                i += 1
            else:
                raise ValueError(f"Lexical Error: Expected delim11 after '{{' at position {i}")

        # Handle `}` token
        elif char == '}':
            state = 120
            tokens.append(("}", "}"))
            i += 1  # Move past the `}`

            # Check for delim16 after `}`
            if i < len(input_string) and input_string[i] in self.delim16:
                tokens.append(("delim16", input_string[i]))
                i += 1
            else:
                raise ValueError(f"Lexical Error: Expected delim16 after '}}' at position {i}")

            # Handle `(` token
            if char == '(':
                state = 122
                tokens.append(("(", "("))
                i += 1  # Move past the `(`

                # Lookahead: Ensure the next token is a valid delimiter from delim17
                if i < len(input_string):
                    next_char = input_string[i]  # Get the next character after `(`
                    
                    # Check if next_char is in delim17
                    if next_char in [' ', '\0'] or next_char.isdigit() or next_char.isalpha() or next_char in ['"', '(', "'", ')']:
                        tokens.append(("delim17", next_char))  # Add delimiter token to the list
                        i += 1  # Move past the delimiter
                    else:
                        raise ValueError(f"Lexical Error: Invalid token after '(' at position {i}, expected one of {self.delim17}")

            # Handle other cases (e.g., braces, parentheses, and other symbols) here
        # Handle `)` token
        elif char == ')':
            state = 124  # Update the state (if necessary, make sure 'state' is being used properly)
            tokens.append((")", ")"))  # Add the `)` token to the list
            i += 1  # Move past the `)`

            # Check if the next character is a valid delimiter from self.delim18
            if i < len(input_string) and input_string[i] in self.delim18:
                # If the next character is in delim18, append it as a token
                tokens.append(("delim18", input_string[i]))
                i += 1  # Move past the delimiter token
            else:
                # If no valid delimiter is found after `)`, raise an error
                raise ValueError(f"Lexical Error: Expected valid delimiter after ')' at position {i}")

        # Handle space token
        elif char == ' ':
            state = 126
            space_tokens, i = self.space_token(input_string, i)
            tokens.extend(space_tokens)

            # Check for delim25 after space
            if i < len(input_string) and input_string[i] in self.delim25:
                tokens.append(("delim25", input_string[i]))
                i += 1
            else:
                raise ValueError(f"Lexical Error: Expected delim25 after space at position {i}")

        # Handle newline token
        elif char == '\n':
            state = 128
            newline_tokens, i = self.newline_token(input_string, i)
            tokens.extend(newline_tokens)

            # Check for delim24 after newline
            if i < len(input_string) and input_string[i] in self.delim24:
                tokens.append(("delim24", input_string[i]))
                i += 1
            else:
                raise ValueError(f"Lexical Error: Expected delim24 after newline at position {i}")
            
        # Handle alpha (letters) token
        elif char in self.alpha:  # Check if the character is a letter
            tokens.append(("alpha_token", char))  # Add the alphabetic character as a token
            i += 1

        # Handle num (numeric) token
        elif char in self.num:  # Check if the character is numeric
            tokens.append(("num_token", char))  # Add the numeric character as a token
            i += 1

        # Handle any unexpected characters
        else:
            raise ValueError(f"Lexical Error: Unexpected character '{char}' at position {i}")

        return tokens, i

    def identifier_token(self, input_string, i):
        """Handles alphanumeric identifiers and keywords (inst, strike, flank, chat)."""
        tokens = []
        keyword_list = ["inst", "strike", "flank", "chat"]  # List of valid keywords

        # Start reading the identifier
        start_index = i
        while i < len(input_string) and (input_string[i].isalnum() or input_string[i] == '_'):  # Allow alphanumeric characters and underscores
            if input_string[i].isalpha() and not input_string[i].islower():  # Ensure identifiers are lowercase
                raise ValueError(f"Lexical Error: Identifier must be lowercase at position {i}")
            i += 1

        # Extract the token
        token = input_string[start_index:i]

        # Ensure the identifier is no longer than 15 characters
        if len(token) > 15:
            raise ValueError(f"Lexical Error: Identifier '{token}' exceeds 15 characters at position {start_index}")

        # Check if the token is a keyword (reserved word)
        if token in keyword_list:
            tokens.append((f"{token}_keyword", token))  # Handle keywords
        else:
            tokens.append(("identifier", token))  # Handle identifiers

        # Lookahead for valid space or delimiters in delim25 after the identifier
        if i < len(input_string):
            char = input_string[i]
            if char == ' ':  # Check if the next character is a space
                # Process the space token using the space_token method
                space_tokens, i = self.space_token(input_string, i)
                tokens.extend(space_tokens)  # Add space tokens to the token list

            # Now check if the next character is a valid delimiter (delim25)
            if i < len(input_string) and input_string[i] in self.delim25:  # Check if next char is in delim25 (space or '=')
                tokens.append((input_string[i], input_string[i]))  # Add the delimiter as a token
                i += 1  # Move past the delimiter

        return tokens, i

def readTokens(input_string, tokenizer):
    """Tokenize the input string using the given tokenizer."""
    tokens = []
    i = 0
    length = len(input_string)

    try:
        while i < length:
            char = input_string[i]

            # Skip whitespace characters (but not newlines)
            if char in [' ', '\t', '\r']:
                i += 1
                continue
            
            # Handle comments (^^ for single-line, ^^^ for multi-line)
            if char == '^':
                comment_tokens, i = tokenizer.handle_comments(input_string, i)
                tokens.extend(comment_tokens)
                continue


            # Handle operators (including assignment, comparison, and arithmetic operators)
            elif char in ['+', '-', '*', '/', '%', '=', '>', '<', '!', '&']:
                operator_tokens, i = tokenizer.token_operator(input_string, i)
                tokens.extend(operator_tokens)  # Add the operator tokens



            # Handle float literals (flank_token)
            elif char.isdigit() or (char == '.' and i + 1 < length and input_string[i + 1].isdigit()):
                # If it's a digit or a decimal point followed by a digit
                float_literal_tokens, i = tokenizer.flank_token(input_string, i)
                tokens.extend(float_literal_tokens)

            # Handle integer literals (inst_token)
            elif char.isdigit():
                integer_literal_tokens, i = tokenizer.inst_token(input_string, i)
                tokens.extend(integer_literal_tokens)

            # Handle integer literals (inst_token)
            elif char in tokenizer.num:  # Only check tokenizer.num
                integer_literal_tokens, i = tokenizer.inst_token(input_string, i)
                tokens.extend(integer_literal_tokens)  # Add integer literal token

            # Handle specific keywords and identifiers
            elif input_string[i] == 'a':
                token, i = tokenizer.a_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'b':
                token, i = tokenizer.b_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'c':
                token, i = tokenizer.c_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'd':
                token, i = tokenizer.d_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'f':
                token, i = tokenizer.f_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'g':
                token, i = tokenizer.g_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'i':
                token, i = tokenizer.i_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'l':
                token, i = tokenizer.l_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'n':
                token, i = tokenizer.n_token(input_string, i)  # Call the n_token handler
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'o':
                token, i = tokenizer.o_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'p':
                token, i = tokenizer.p_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'r':
                token, i = tokenizer.r_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 's':
                token, i = tokenizer.s_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 't':
                token, i = tokenizer.t_token(input_string, i)
                tokens.extend(token)  # Add the token to the list
            elif input_string[i] == 'w':
                token, i = tokenizer.w_token(input_string, i)
                tokens.extend(token)  # Add the token to the list



            # Handle operators (including assignment, comparison, and arithmetic operators)
            elif char in ['+', '-', '*', '/', '%', '=', '>', '<', '!', '&']:
                operator_tokens, i = tokenizer.token_operator(input_string, i)
                tokens.extend(operator_tokens)  # Add the operator tokens

            # Handle string literals (single quotes for strings)
            elif char == "'":
                string_literal_tokens, i = tokenizer.strike_token(input_string, i)
                tokens.extend(string_literal_tokens)

            # Handle character literals (double quotes for characters)
            elif char == '"':
                char_literal_tokens, i = tokenizer.chat_lit_token(input_string, i)
                tokens.extend(char_literal_tokens)

            # Handle float literals (flank_token)
            elif char.isdigit():
                if i + 1 < length and input_string[i + 1] == '.':
                    float_literal_tokens, i = tokenizer.flank_token(input_string, i)
                    tokens.extend(float_literal_tokens)  # Add float literal token
                else:
                    integer_literal_tokens, i = tokenizer.inst_token(input_string, i)
                    tokens.extend(integer_literal_tokens)  # Add integer literal token

            # Handle specific keywords and identifiers
            elif char.isalpha():
                keyword_or_identifier_tokens, i = tokenizer.keyword_or_identifier_token(input_string, i)
                tokens.extend(keyword_or_identifier_tokens)  # Add keyword/identifier token

            # Handle newline characters explicitly
            elif char == '\n':
                newline_tokens, i = tokenizer.newline_token(input_string, i)
                tokens.extend(newline_tokens)

            # Handle symbols and operators
            elif char in ['{', '}', '(', ')', '~', '^', ';']:
                symbol_tokens, i = tokenizer.otherSymbols(input_string, i)
                tokens.extend(symbol_tokens)

            # Handle any unrecognized characters
            else:
                raise ValueError(f"Lexical Error: Unknown token start at position {i} ({char})")

            # Ensure we don't go out of bounds
            if i >= length:
                break

        return tokens

    except ValueError as e:
        # Reraise the error to be handled in the `analyze_code` function
        raise ValueError(str(e)) from e
