


abort;
and(
back;
bounce;
chat x
defuse x
flank x
force x
globe 
inst x
inst info(
in 
load(
neg 
not(
plant(
perim(
pos 


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
                    tokens.append(("flank_token", char))
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
                    tokens.append(("load_token", char))
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

    def token_operator(self, input_string, i):
        """Handles assignment operators, operators, and comparison operators."""
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

        elif char == '-':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
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

        elif char == '=':
            tokens.append(("assignment_operator", "="))

        elif char == '!':
            if i + 1 < len(input_string) and input_string[i + 1] == '=':
                tokens.append(("not_equal_to_operator", "!="))
                i += 1  # Skip the next '=' character

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
