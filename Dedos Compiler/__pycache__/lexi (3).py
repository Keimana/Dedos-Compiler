class DEDOSLexicalAnalyzer:
    def __init__(self):
        self.delimiters = {' ', ',', '(', ')', '{', '}', '[', ']', ';'}
        self.reserved_words = {
            "if": "IF_TOKEN",
            "else": "ELSE_TOKEN",
            "while": "WHILE_TOKEN",
            "for": "FOR_TOKEN",
            "return": "RETURN_TOKEN",
            "function": "FUNCTION_TOKEN",
            "var": "VAR_TOKEN",
            "let": "LET_TOKEN",
            "const": "CONST_TOKEN",
            "true": "TRUE_TOKEN",
            "false": "FALSE_TOKEN",
            "null": "NULL_TOKEN",
            "undefined": "UNDEFINED_TOKEN",
            "break": "BREAK_TOKEN",
            "continue": "CONTINUE_TOKEN",
            "switch": "SWITCH_TOKEN",
            "case": "CASE_TOKEN",
            "default": "DEFAULT_TOKEN",
            "try": "TRY_TOKEN",
            "catch": "CATCH_TOKEN",
            "finally": "FINALLY_TOKEN",
            "throw": "THROW_TOKEN",
            "class": "CLASS_TOKEN",
            "extends": "EXTENDS_TOKEN",
            "super": "SUPER_TOKEN",
            "import": "IMPORT_TOKEN",
            "export": "EXPORT_TOKEN",
            "from": "FROM_TOKEN",
            "as": "AS_TOKEN",
            "async": "ASYNC_TOKEN",
            "await": "AWAIT_TOKEN",
            "static": "STATIC_TOKEN",
            "this": "THIS_TOKEN",
            "new": "NEW_TOKEN",
            "delete": "DELETE_TOKEN",
            "in": "IN_TOKEN",
            "of": "OF_TOKEN",
            "instanceof": "INSTANCEOF_TOKEN",
            "with": "WITH_TOKEN",
            "do": "DO_TOKEN"
        }

    def tokenize(self, input_string):
        tokens = []
        current_token = ""
        line_number = 1
        column_number = 1
        errors = []

        for char in input_string:
            if char in self.delimiters:
                if current_token:
                    if current_token in self.reserved_words:
                        tokens.append((self.reserved_words[current_token], line_number, column_number))
                    else:
                        tokens.append(("IDENTIFIER", line_number, column_number, current_token))
                    current_token = ""
                if char == "\n":
                    line_number += 1
                    column_number = 1
                else:
                    column_number += 1
                if char != " ":
                    tokens.append(("DELIMITER", line_number, column_number, char))
            elif char.isalnum() or char == '_':  # Allow alphanumeric characters and underscores
                current_token += char
                column_number += 1
            else:
                # Log an error for invalid characters
                errors.append(f"Lexical Error: Invalid character '{char}' at line {line_number}, column {column_number}.")
                column_number += 1  # Move to the next character

        if current_token:
            if current_token in self.reserved_words:
                tokens.append((self.reserved_words[current_token], line_number, column_number))
            else:
                tokens.append(("IDENTIFIER", line_number, column_number, current_token))

        return tokens, errors

        # Operators
        self.operators = {"+", "-", "*", "/", "%", "**", "//", "=", "==", "!=", ">", "<", ">=", "<="}
        self.delimiters = {"~{", "}~", "{", "}", "(", ")", "[", "]", ";", ","}


    
    def a_token(self, token):
        # Ensure the token is exactly "abort" and not anything shorter or incomplete
        if token != "abort":
            raise ValueError(f"Lexical Error: Invalid token '{token}', expected 'abort'.")

        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            # Handle state transitions based on characters
            if state == 0:
                if char == 'a':
                    state = 1  # Transition to state 1 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 1:
                if char == 'b':
                    state = 2  # Transition to state 2 after 'b'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 2:
                if char == 'o':
                    state = 3  # Transition to state 3 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 3:
                if char == 'r':
                    state = 4  # Transition to state 4 after 'r'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 4:
                if char == 't':
                    state = 5  # Transition to state 5 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 5:
                # Lookahead for delimiter `;` or space or opening parenthesis `(`
                if i + 1 < len(token):
                    next_char = token[i + 1]

                    if next_char == ';':
                        state = 6  # Transition to final state after 'abort;' token
                        return "A_TOKEN_WITH_DELIMITER"  # Successfully identified "abort;" with delimiter
                    elif next_char in " \t\n\r(":
                        # If space or parenthesis, stay in state 5 and continue
                        state = 5
                    else:
                        raise ValueError(f"Lexical Error: Expected ';' or space after 'abort', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected ';' or space after 'abort', but no more characters found.")

            i += 1  # Move to the next character

        # If the loop finishes and no valid transition occurred
        raise ValueError(f"Lexical Error: Expected ';' or space after 'abort', but no delimiter found.")


    def b_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]
            
            # Handle state transitions based on characters
            if state == 0:
                if char == 'b':
                    state = 10  # Transition to state 10 after 'b'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 10:
                if char == 'a':
                    state = 11  # Transition to state 11 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 11:
                if char == 'c':
                    state = 12  # Transition to state 12 after 'c'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 12:
                if char == 'k':
                    state = 13  # Transition to state 13 after 'k'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 13:
                # Lookahead for '(' delimiter
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char == '(':
                        state = 14  # Transition to state 14 after 'back(' token
                        return "BACK_TOKEN"
                    else:
                        raise ValueError(f"Lexical Error: Expected '(' after 'back', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected '(' after 'back', but no more characters found.")
            
            elif state == 14:
                if char == 'o':
                    state = 15  # Transition to state 15 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 15:
                if char == 'u':
                    state = 16  # Transition to state 16 after 'u'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 16:
                if char == 'n':
                    state = 17  # Transition to state 17 after 'n'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 17:
                if char == 'c':
                    state = 18  # Transition to state 18 after 'c'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 18:
                if char == 'e':
                    state = 19  # Transition to state 19 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 19:
                # Lookahead for delimiters (space, tab, newline, or semicolon)
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char in " \t\n\r;":
                        state = 20  # Final state after 'bounce' with a valid delimiter
                        return "BOUNCE_TOKEN"  # Successfully identified the 'bounce' token
                    else:
                        raise ValueError(f"Lexical Error: Expected a delimiter (space, tab, newline, or ';') after 'bounce', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected a delimiter after 'bounce', but no more characters found.")

            i += 1  # Move to the next character

        # If the loop finishes and no valid transition occurred
        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")


    def c_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]
            
            # Handle state transitions based on characters
            if state == 0:
                if char == 'c':
                    state = 21  # Transition to state 21 after 'c'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 21:
                if char == 'h':
                    state = 22  # Transition to state 22 after 'h'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 22:
                if char == 'a':
                    state = 23  # Transition to state 23 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 23:
                if char == 't':
                    state = 24  # Transition to state 24 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 24:
                # Lookahead for space (delim3)
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char in " \t\n\r":  # Space or tab or newline (delim3)
                        state = 25  # Transition to final state 25 after the space
                        return "CHAT_TOKEN"  # Successfully identified 'chat' followed by space
                    else:
                        raise ValueError(f"Lexical Error: Expected space after 'chat', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'chat', but no more characters found.")

            i += 1  # Move to the next character

        # If the loop finishes and no valid transition occurred
        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")
    
    def d_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]
            
            # Handle state transitions based on characters
            if state == 0:
                if char == 'd':
                    state = 26  # Transition to state 26 after 'd'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 26:
                if char == 'e':
                    state = 27  # Transition to state 27 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 27:
                if char == 'f':
                    state = 28  # Transition to state 28 after 'f'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 28:
                if char == 'u':
                    state = 29  # Transition to state 29 after 'u'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 29:
                if char == 's':
                    state = 30  # Transition to state 30 after 's'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 30:
                if char == 'e':
                    state = 31  # Transition to state 31 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 31:
                # Lookahead for space (delim3)
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char in " \t\n\r":  # Space or tab or newline (delim3)
                        state = 32  # Transition to final state 32 after the space
                        return "DEFUSE_TOKEN"  # Successfully identified 'defuse' followed by space
                    else:
                        raise ValueError(f"Lexical Error: Expected space after 'defuse', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'defuse', but no more characters found.")

            i += 1  # Move to the next character

        # If the loop finishes and no valid transition occurred
        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")
    
    def f_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]
            
            # Handle state transitions based on characters
            if state == 0:
                if char == 'f':
                    state = 33  # Transition to state 33 after 'f'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 33:
                if char == 'l':
                    state = 34  # Transition to state 34 after 'l'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 34:
                if char == 'a':
                    state = 35  # Transition to state 35 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 35:
                if char == 'n':
                    state = 36  # Transition to state 36 after 'n'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 36:
                if char == 'k':
                    state = 37  # Transition to state 37 after 'k'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 37:
                # Lookahead for space (delim3)
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char in " \t\n\r":  # Space or tab or newline (delim3)
                        state = 38  # Transition to final state 38 after space
                        return "FLANK_TOKEN"  # Successfully identified 'flank' followed by space
                    else:
                        raise ValueError(f"Lexical Error: Expected space after 'flank', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'flank', but no more characters found.")

            elif state == 33:
                if char == 'o':
                    state = 39  # Transition to state 39 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 39:
                if char == 'r':
                    state = 40  # Transition to state 40 after 'r'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 40:
                if char == 'c':
                    state = 41  # Transition to state 41 after 'c'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 41:
                if char == 'e':
                    state = 42  # Transition to state 42 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 42:
                # Lookahead for space (delim3)
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char in " \t\n\r":  # Space or tab or newline (delim3)
                        state = 43  # Transition to final state 43 after space
                        return "FORCE_TOKEN"  # Successfully identified 'force' followed by space
                    else:
                        raise ValueError(f"Lexical Error: Expected space after 'force', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'force', but no more characters found.")

            i += 1  # Move to the next character

        # If the loop finishes and no valid transition occurred
        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def g_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]
            
            # Handle state transitions based on characters
            if state == 0:
                if char == 'g':
                    state = 44  # Transition to state 44 after 'g'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 44:
                if char == 'l':
                    state = 45  # Transition to state 45 after 'l'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 45:
                if char == 'o':
                    state = 46  # Transition to state 46 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 46:
                if char == 'b':
                    state = 47  # Transition to state 47 after 'b'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 47:
                if char == 'e':
                    state = 48  # Transition to state 48 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 48:
                # Lookahead for space (delim3)
                if i + 1 < len(token):
                    next_char = token[i + 1]
                    
                    if next_char in " \t\n\r":  # Space or tab or newline (delim3)
                        state = 49  # Transition to final state 49 after the space
                        return "GLOBE_TOKEN"  # Successfully identified 'globe' followed by space
                    else:
                        raise ValueError(f"Lexical Error: Expected space after 'globe', but found '{next_char}' at position {i + 2}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'globe', but no more characters found.")

            i += 1  # Move to the next character

        # If the loop finishes and no valid transition occurred
        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")
    

    def i_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'i':
                    state = 50  # Transition to state 50 after 'i'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 50:
                if char == 'n':
                    state = 51  # Transition to state 51 after 'n'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 51:
                # Lookahead for space or other delimiters (space, parentheses, etc.)
                if i + 1 < len(token) and token[i + 1] == ' ':
                    state = 52  # Transition to state 52 after 'in' followed by space
                    return "IN_TOKEN"  # Successfully identified "in" followed by space

                # Check for the next character as 'info' token
                elif i + 1 < len(token) and token[i + 1] == 'f':
                    state = 53  # Transition to state 53 after 'f' (checking for 'info')

                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 53:
                if char == 'o':
                    state = 54  # Transition to state 54 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 54:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    state = 55  # Transition to final state after 'info(' token
                    return "INFO_TOKEN"  # Successfully identified "info("

            elif state == 55:
                if char == 's':
                    state = 56  # Transition to state 56 after 's'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 56:
                if char == 't':
                    state = 57  # Transition to state 57 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 57:
                # Lookahead for space or other delimiters
                if i + 1 < len(token) and token[i + 1] == ' ':
                    state = 58  # Transition to final state after 'st' followed by space
                    return "INFO_ST_TOKEN"  # Successfully identified "st" token after space

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def l_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'l':
                    state = 59  # Transition to state 59 after 'l'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 59:
                if char == 'o':
                    state = 60  # Transition to state 60 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 60:
                if char == 'a':
                    state = 61  # Transition to state 61 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 61:
                if char == 'd':
                    state = 62  # Transition to state 62 after 'd'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 62:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    state = 63  # Transition to final state after 'load(' token
                    return "LOAD_TOKEN"  # Successfully identified "load("

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")


    def n_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'n':
                    state = 64  # Transition to state 64 after 'n'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 64:
                if char == 'e':
                    state = 65  # Transition to state 65 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 65:
                if char == 'g':
                    state = 66  # Transition to state 66 after 'g'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 66:
                # Lookahead for delimiters: space, '=', ',', ')', null, '!', '}'
                if i + 1 < len(token) and token[i + 1] in " \t\n\r=,!){}":
                    state = 67  # Transition to final state after valid delimiter
                    return "NEG_TOKEN"  # Successfully identified "neg" token

            elif state == 67:
                # If the next character is 'o', proceed to 'o'
                if char == 'o':
                    state = 68  # Transition to state 68 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 68:
                if char == 't':
                    state = 69  # Transition to state 69 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 69:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    state = 70  # Transition to final state after 'not(' token
                    return "NOT_TOKEN"  # Successfully identified "not(" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def o_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'o':
                    state = 71  # Transition to state 71 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 71:
                if char == 'r':
                    state = 72  # Transition to state 72 after 'r'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 72:
                # Lookahead for delimiters: space, '('
                if i + 1 < len(token) and token[i + 1] in " \t\n\r(":
                    state = 73  # Transition to final state 73 after valid delimiter
                    return "OR_TOKEN"  # Successfully identified "or" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def p_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'p':
                    state = 74  # Transition to state 74 after 'p'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 74:
                if char == 'e':
                    state = 75  # Transition to state 75 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 75:
                if char == 'r':
                    state = 76  # Transition to state 76 after 'r'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 76:
                if char == 'i':
                    state = 77  # Transition to state 77 after 'i'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 77:
                if char == 'm':
                    state = 78  # Transition to state 78 after 'm'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 78:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    state = 79  # Transition to final state 79 after valid '(' delimiter
                    return "PERM_TOKEN"  # Successfully identified "perm(" token

                # Transition for "plant" token
                elif i + 1 < len(token) and token[i + 1] == 'l':
                    state = 80  # Transition to state 80 after 'l'

            elif state == 80:
                if char == 'a':
                    state = 81  # Transition to state 81 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 81:
                if char == 'n':
                    state = 82  # Transition to state 82 after 'n'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 82:
                if char == 't':
                    state = 83  # Transition to state 83 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 83:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    state = 84  # Transition to final state 84 after valid '(' delimiter
                    return "PLANT_TOKEN"  # Successfully identified "plant(" token

                # Transition for "or" token
                elif i + 1 < len(token) and token[i + 1] == 'o':
                    state = 85  # Transition to state 85 after 'o'

            elif state == 85:
                if char == 's':
                    state = 86  # Transition to state 86 after 's'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 86:
                # Lookahead for delimiters: space, '=', ',', ')', null, '!', '}'
                if i + 1 < len(token) and token[i + 1] in " \t\n\r=,!){}":
                    state = 87  # Transition to final state 87 after valid delimiter
                    return "OS_TOKEN"  # Successfully identified "os" token

            elif state == 87:
                # Lookahead for ';' delimiter
                if i + 1 < len(token) and token[i + 1] == ';':
                    state = 92  # Transition to final state 92 after ';'
                    return "USH_TOKEN"  # Successfully identified "ush;" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def r_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'r':
                    state = 92  # Transition to state 92 after 'r'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")
            
            elif state == 92:
                if char == 'e':
                    state = 93  # Transition to state 93 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 93:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    state = 94  # Transition to final state 94 after valid '(' delimiter
                    return "READ_TOKEN"  # Successfully identified "read(" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def s_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 's':
                    state = 100  # Transition to state 100 after 's'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 100:
                if char == 't':
                    state = 101  # Transition to state 101 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 101:
                if char == 'r':
                    state = 102  # Transition to state 102 after 'r'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 102:
                if char == 'i':
                    state = 103  # Transition to state 103 after 'i'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 103:
                if char == 'k':
                    state = 104  # Transition to state 104 after 'k'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 104:
                if char == 'e':
                    state = 105  # Transition to state 105 after 'e'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 105:
                # Lookahead for space delimiter
                if i + 1 < len(token) and token[i + 1] == ' ':
                    state = 106  # Transition to final state 106 after space
                    return "STRIKE_TOKEN"  # Successfully identified "strike" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def t_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 't':
                    state = 107  # Transition to state 107 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 107:
                if char == 'o':
                    state = 108  # Transition to state 108 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 108:
                if char == 'o':
                    state = 109  # Transition to state 109 after 'o'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 109:
                if char == 'l':
                    state = 110  # Transition to state 110 after 'l'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 110:
                # Lookahead for space delimiter
                if i + 1 < len(token) and token[i + 1] == ' ':
                    state = 111  # Transition to final state 111 after space
                    return "TOOL_TOKEN"  # Successfully identified "tool" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")

    def w_token(self, token):
        state = 0  # Initial state
        i = 0  # Index of current character

        while i < len(token):
            char = token[i]

            if state == 0:
                if char == 'w':
                    state = 112  # Transition to state 112 after 'w'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 112:
                if char == 'a':
                    state = 113  # Transition to state 113 after 'a'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 113:
                if char == 't':
                    state = 114  # Transition to state 114 after 't'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 114:
                if char == 'c':
                    state = 115  # Transition to state 115 after 'c'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 115:
                if char == 'h':
                    state = 116  # Transition to state 116 after 'h'
                else:
                    raise ValueError(f"Lexical Error: Invalid character '{char}' at position {i + 1}")

            elif state == 116:
                # Lookahead for '(' delimiter
                if i + 1 < len(token) and token[i + 1] == '(':
                    return "WATCH_TOKEN"  # Successfully identified "watch(" token

            i += 1  # Move to the next character

        raise ValueError(f"Lexical Error: Token '{token}' is not valid.")


    def operator_token(self, token):
        description = ""  # To store the description of the operator

        # Check for invalid tokens like '===' or '+++'
        if len(token) > 2:  
            return (f"Invalid token: {token}", "LEXICAL_ERROR")

        # Handle multi-character operators (e.g., '-=', '+=', '==', '>=', etc.)
        if len(token) == 2:
            if token == "==":
                description = "EQUALITY_TOKEN"
                return (description, "==")
            elif token == "+=":
                description = "PLUSEQUALS_TOKEN"
                return (description, "+=")
            elif token == "-=":
                description = "MINUSEQUALS_TOKEN"
                return (description, "-=")
            elif token == "!=":
                description = "NOTEQUAL_TOKEN"
                return (description, "!=")
            elif token == ">=":
                description = "GREATEREQUAL_TOKEN"
                return (description, ">=")
            elif token == "<=":
                description = "LESSEQUAL_TOKEN"
                return (description, "<=")
            elif token == "/=":
                description = "DIVISIONEQUAL_TOKEN"
                return (description, "/=")
            elif token == "%=":
                description = "MODULOEQUAL_TOKEN"
                return (description, "%=")

        # Handle special multi-character operators (e.g., '**' and '//')
        if len(token) == 2:
            if token == "**":
                description = "EXPONENTIAL_TOKEN"
                return (description, "**")
            elif token == "//":
                description = "FLOOR_TOKEN"
                return (description, "//")

        # Handle single-character operators with exact length matching
        if len(token) == 1:
            if token == "=":
                description = "EQUAL_TOKEN"
                return (description, "=")
            elif token == ">":
                description = "GREATER_TOKEN"
                return (description, ">")
            elif token == "<":
                description = "LESS_TOKEN"
                return (description, "<")
            elif token == "+":
                description = "PLUS_TOKEN"
                return (description, "+")
            elif token == "-":
                description = "MINUS_TOKEN"
                return (description, "-")
            elif token == "*":
                description = "MULTIPLY_TOKEN"
                return (description, "*")
            elif token == "/":
                description = "DIVISION_TOKEN"
                return (description, "/")
            elif token == "%":
                description = "MODULO_TOKEN"
                return (description, "%")

        # Return error for any other invalid operator
        return (f"Invalid token: {token}", "LEXICAL_ERROR")
    

    def identifier_token(self, token):
        # Generic identifier handler
        return "IDENTIFIER"

    def classify_token(self, token):
        # Handle multi-character operators first
        if token in {"==", "!=", ">=", "<=", "-=", "+=", "*=", "/=", "%="}:
            return self.operator_token(token)

        # Handle single-character operators
        if token in {"+", "-", "*", "/", "%", "**", "//"}:
            return self.operator_token(token)
        elif token in {"=", ">", "<"}:
            return self.operator_token(token)

        # Handle spaces (Optional)
        if token == " ":
            return None  # Space should typically be ignored

        # Handle alphabetic tokens (keywords or identifiers)
        if token.isalpha():
            # Depending on the starting letter, you can route it to specific functions
            first_char = token[0]
            
            # Match based on the first letter (you can generalize this list as needed)
            if first_char == 'a':
                return self.a_token(token)
            elif first_char == 'b':
                return self.b_token(token)
            elif first_char == 'c':
                return self.c_token(token)
            elif first_char == 'd':
                return self.d_token(token)
            elif first_char == 'f':
                return self.f_token(token)
            elif first_char == 'g':
                return self.g_token(token)
            elif first_char == 'i':
                return self.i_token(token)
            elif first_char == 'l':
                return self.l_token(token)
            elif first_char == 'n':
                return self.n_token(token)
            elif first_char == 'o':
                return self.o_token(token)
            elif first_char == 'p':
                return self.p_token(token)
            elif first_char == 'r':
                return self.r_token(token)
            elif first_char == 's':
                return self.s_token(token)
            elif first_char == 't':
                return self.t_token(token)
            elif first_char == 'w':
                return self.w_token(token)
            elif first_char == 'z':
                return self.identifier_token(token)

            # If token does not match any prefix rule, treat it as an identifier
            return self.identifier_token(token)

        # Handle numbers (integer or float, including negative)
        if token.isdigit() or (token[0] == "-" and (token[1:].isdigit() or token[1] == ".")):
            return self.number_token(token)

        # Handle unknown tokens (if no other rules match)
        return "UNKNOWN"

    def tokenize(self, input_string):
        """Tokenizes the input string based on predefined rules using alphabetically split functions."""
        tokens = []
        i = 0
        length = len(input_string)

        while i < length:
            char = input_string[i]

            # Handle multi-character delimiter "~{" and "}~"
            if i + 1 < length and input_string[i:i+2] == "~{":
                tokens.append(("~{", "~{"))
                i += 2  # Skip the next character
                continue
            elif i + 1 < length and input_string[i:i+2] == "}~":
                tokens.append(("}~", "}~"))
                i += 2  # Skip the next character
                continue

            # Handle delimiters, including the comma specifically
            if char in self.delimiters:
                if char == ",":
                    tokens.append(("Comma", ","))
                else:
                    tokens.append((char, char))
                i += 1
                continue

            # Handle whitespace
            if char.isspace():
                tokens.append(("SPACE", "\n"))
                i += 1
                continue

            # Handle multi-character operators (e.g., '+=', '-=', '/=')
            if char in {'-', '+', '/', '%'} and i + 1 < length and input_string[i + 1] == '=':
                operator_token = self.operator_token(input_string[i:i + 2])
                tokens.append(operator_token)
                i += 2
                continue

            # Handle multi-character operators (e.g., '**', '//')
            if char == '*' and i + 1 < length and input_string[i + 1] == '*':
                operator_token = self.operator_token("**")
                tokens.append(operator_token)
                i += 2
                continue
            elif char == '/' and i + 1 < length and input_string[i + 1] == '/':
                operator_token = self.operator_token("//")
                tokens.append(operator_token)
                i += 2
                continue
            elif char == '=' and i + 1 < length and input_string[i + 1] == '=':
                operator_token = self.operator_token("==")
                tokens.append(operator_token)
                i += 2
                continue

            # Handle single-character operators (e.g., '-', '+', '*', '/', '%')
            if char in {'-', '+', '*', '/', '%'}:
                if char == "-" and i + 1 < length:
                    next_char = input_string[i + 1]

                    # Handle negative numbers (integers or floats)
                    if next_char.isdigit() or next_char == '.':  # Negative number case
                        start = i
                        i += 1  # Skip the minus sign and include it with the number
                        while i < length and (input_string[i].isdigit() or input_string[i] == '.'):
                            i += 1
                        # Ensure the token is identified correctly as a float or integer
                        if '.' in input_string[start:i]:
                            tokens.append(("FLOAT_LITERAL", input_string[start:i]))  # Add the full float literal
                        else:
                            tokens.append(("INST_LITERAL", input_string[start:i]))  # Add the full integer literal
                        continue

                operator_token = self.operator_token(input_string[i:i + 1])
                tokens.append(operator_token)
                i += 1
                continue

            # Handle comparison operators (e.g., '=', '>', '<')
            if char in {'=', '>', '<'}:
                operator_token = self.operator_token(input_string[i:i + 1])
                tokens.append(operator_token)
                i += 1
                continue

            # Handle identifiers or reserved words
            if char.isalpha():
                start = i
                while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                    i += 1
                token = input_string[start:i]

                # Check for reserved words explicitly
                if token in self.reserved_words:
                    tokens.append((self.reserved_words[token], token))  # Add token type and lexeme
                else:
                    # For identifiers, classify normally
                    token_type = self.classify_token(token)
                    tokens.append((token_type, token))
                continue

            # Handle numbers (integer or float, including negative)
            if char.isdigit() or (char == "-" and i + 1 < length and (input_string[i + 1].isdigit() or input_string[i + 1] == ".")):
                start = i
                if char == "-":
                    i += 1  # Skip the minus sign and include it with the number

                # Handle digits of the number
                while i < length and input_string[i].isdigit():
                    i += 1

                # Handle decimal point for float (check if decimal point exists after digits)
                if i < length and input_string[i] == ".":
                    i += 1  # Skip the decimal point
                    # If digits follow the decimal point, continue parsing
                    while i < length and input_string[i].isdigit():
                        i += 1
                    tokens.append(("FLOAT_LITERAL", input_string[start:i]))  # Add the full float literal
                else:
                    tokens.append(("INST_LITERAL", input_string[start:i]))  # Add the full integer literal
                continue

            # Handle multi-line comments
            if input_string[i:i + 3] == "^^^":
                start = i
                i += 3  # Skip the opening ^^^
                while i < length and input_string[i:i + 3] != "^^^":
                    i += 1
                if i < length and input_string[i:i + 3] == "^^^":
                    i += 3  # Skip the closing ^^^
                    tokens.append(("MULTI_LINE_COMMENT_TOKEN", input_string[start:i]))
                else:
                    tokens.append(("ERROR", "Unterminated multi-line comment"))
                continue

            # Handle single-line comments
            if input_string[i:i + 2] == "^^":
                start = i
                i += 2  # Skip the opening ^^
                while i < length and input_string[i:i + 2] != "^^":
                    i += 1
                if i < length and input_string[i:i + 2] == "^^":
                    i += 2  # Skip the closing ^^
                    tokens.append(("SINGLE_LINE_COMMENT_TOKEN", input_string[start:i]))
                else:
                    tokens.append(("ERROR", "Unterminated single-line comment"))
                continue

            # Handle string literals
            if char == '"':
                start = i
                i += 1
                while i < length and input_string[i] != '"':
                    i += 1
                if i < length:
                    i += 1
                    tokens.append(("STRIKE_LITERAL", input_string[start:i]))
                else:
                    tokens.append(("ERROR", "Unterminated string literal"))
                continue

            if char == "'":
                start = i
                i += 1
                while i < length and input_string[i] != "'":
                    i += 1
                if i < length:
                    i += 1
                    tokens.append(("CHAT_LITERAL", input_string[start:i]))
                else:
                    tokens.append(("ERROR", "Unterminated string literal"))
                continue

            # Handle unknown characters and transition to the next state
            tokens.append(("UNKNOWN", char))
            i += 1

        return tokens
