class DEDOSLexicalAnalyzer:
    def __init__(self):
        self.reserved_words = ['abort', 'and']  # Define reserved words
        self.literals = {
            'literal1': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],  # alpha
            'literal2': ['0'],  # zero
            'literal3': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],  # digits
            'literal4': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],  # num (combination of zero and digits)
            'literal5': ['null'],  # null
            'literal6': ['λ'],  # lambda
            'literal7': ['.'],  # dot
            'literal8': [','],  # comma
            'literal9': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],  # alphanum (alpha + digits)
            'literal10': ['@', '#', '?', '&', '{', '.', ';', '>', '^', ']', '~', '*', '+', '}', '$', '[', '<', '!', ':', ',', '%', '/', ')', '_', '(', '\\', '=', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '-', '`', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']  # ascii
        }

        self.delimiters = {
            'delim1': ['{'],
            'delim2': ['~'],
            'delim3': [' '],
            'delim4': ['('],
            'delim5': [' ', '('],
            'delim6': [' ', '^', ';', '}', '\n', '\0'],
            'delim7': ['=', ' '],
            'delim8': [' ', '=', ')', '\0', '!'],
            'delim9': [' ', 'num', "'", '(', '_', 'alpha', '"'],
            'delim10': ['num', "'", '"', 'alpha', '[', '[', ']'],
            'delim11': [' ', '\0', '\n'],
            'delim12': [';'],
            'delim13': [' ', 'num', '"', 'alpha', '(', "'", 'and'],
            'delim14': [' ', 'num', '(', '_'],
            'delim15': [' ', 'num', '(', '_', '"'],
            'delim16': ['^', ' ', '\0', '\n', '~'],
            'delim17': [' ', '\0', 'num', 'alpha', '"', '(', "'", ')'],
            'delim18': [' ', '\0', '\n', 'alpha', '+', '-', '*', '/', '%', '!', '=', '<', '>', ',', '}', ')', '{'],
            'delim19': ['=', '*', ')', ' ', '\0', '+', ']', '%', ',', '}', '/', '<', '[', '>', '\n', '!', '-'],
            'delim20': [' ', '+', '=', '!', ',', '^', ')', '}', '\n', '\0', ']'],
            'delim21': ['\0', '}', ' ', '\n', '^'],
            'delim22': ['\n', '\0', '^'],
            'delim23': [']', '%', '>', '+', '}', '\0', ',', '<', '/', '=', '^', '*', ' ', '!', '-', '\n', ')'],
            'delim24': [')', ']', '+', '=', '}', '*', '\0', ',', '/', '[', '<', '>', '-', ' ', '%', '(', '\n', '!'],
            'delim25': [' ', '='],
            'delim26': [',', '+', '-', '*', '/', '%', '=', '<', '>', '!', '^', '\n', '\0', '}', ']', ' ', ',', ')'],
            'delim27': [' ', '=', '!', ',', '^', ')', '}', '\n', '\0', ']'],
        }

    def a_token(self, token):
        i = 0  # Index of current character
        length = len(token)
        self.state = 0  # Start in the initial state

        while i < length:
            char = token[i]

            # State 0: Start state, checking for 'abort' or 'and'
            if self.state == 0:
                if char == 'a':  # First character of 'abort' or 'and'
                    self.state = 1  # Transition to state 1
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' but got '{char}' at position {i + 1}")

            # State 1: After 'a', checking for 'b' in 'abort' or 'n' in 'and'
            elif self.state == 1:
                if char == 'b':  # Second character of 'abort'
                    self.state = 2  # Transition to state 2
                elif char == 'n':  # Second character of 'and'
                    self.state = 4  # Transition to state 4 (checking for 'd' in 'and')
                else:
                    raise ValueError(f"Lexical Error: Expected 'b' or 'n' but got '{char}' at position {i + 1}")

            # State 2: After 'ab', checking for 'o' in 'abort'
            elif self.state == 2:
                if char == 'o':  # Third character of 'abort'
                    self.state = 3  # Transition to state 3
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' but got '{char}' at position {i + 1}")

            # State 3: After 'abo', checking for 'r' in 'abort'
            elif self.state == 3:
                if char == 'r':  # Fourth character of 'abort'
                    self.state = 4  # Transition to state 4
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' but got '{char}' at position {i + 1}")

            # State 4: After 'abor', checking for 't' in 'abort' or checking for 'd' in 'and'
            elif self.state == 4:
                if char == 't':  # Fifth character of 'abort'
                    self.state = 5  # Transition to state 5 (final state for 'abort')
                elif char == 'd':  # Second character of 'and', after 'n'
                    self.state = 6  # Transition to state 6 (final state for 'and')
                else:
                    raise ValueError(f"Lexical Error: Expected 't' or 'd' but got '{char}' at position {i + 1}")

            # State 5: After 'abort', check for delimiter ';'
            elif self.state == 5:
                if char == ';':  # After 'abort', check for ';'
                    return "abort_token"  # Valid 'abort;' token
                else:
                    raise ValueError(f"Lexical Error: Missing delimiter ';' after 'abort' at position {i + 1}")

            # State 6: After 'and', check for space or '(' using delim5
            elif self.state == 6:
                if char == ' ':  # Check for space before '('
                    self.state = 7  # Transition to state 7 (looking for '(' after space)
                elif char == '(':  # 'and(' without space is invalid
                    raise ValueError(f"Lexical Error: Missing space before '(' after 'and' at position {i + 1}")
                else:
                    raise ValueError(f"Lexical Error: Expected space or '(' after 'and' at position {i + 1}")

            # State 7: After space, check for '('
            elif self.state == 7:
                if char == '(':  # After space, check for '('
                    return "and_token"  # Valid 'and (' token
                else:
                    raise ValueError(f"Lexical Error: Expected '(' after 'and ' at position {i + 1}")

            i += 1  # Move to the next character

        # If the loop ends and we haven't reached a valid final state, raise an error
        raise ValueError("Lexical Error: Invalid token.")


    def b_token(self, token):
        i = 0  # Index of current character
        length = len(token)
        self.state = 0  # Start in the initial state

        while i < length:
            char = token[i]

            # State 0: Initial state, looking for 'b'
            if self.state == 0:
                if char == 'b':  # First character of 'b_token'
                    self.state = 10  # Transition to state 10
                else:
                    raise ValueError(f"Lexical Error: Expected 'b' but got '{char}' at position {i + 1}")

            # State 10: After 'b', checking for 'a'
            elif self.state == 10:
                if char == 'a':
                    self.state = 11  # Transition to state 11
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' but got '{char}' at position {i + 1}")

            # State 11: After 'ba', checking for 'c'
            elif self.state == 11:
                if char == 'c':
                    self.state = 12  # Transition to state 12
                else:
                    raise ValueError(f"Lexical Error: Expected 'c' but got '{char}' at position {i + 1}")

            # State 12: After 'bac', checking for 'k'
            elif self.state == 12:
                if char == 'k':
                    self.state = 13  # Transition to state 13
                else:
                    raise ValueError(f"Lexical Error: Expected 'k' but got '{char}' at position {i + 1}")

            # State 13: After 'back', checking for space (delim 4) or '('
            elif self.state == 13:
                if char == ' ':  # After 'back', we expect a space (delim 4)
                    self.state = 14  # Transition to state 14 (lookahead for '(')
                elif char == '(':  # If no space, '(' is immediately valid as well
                    self.state = 14  # Transition to state 14
                else:
                    raise ValueError(f"Lexical Error: Expected space or '(' but got '{char}' at position {i + 1}")

            # State 14: After 'back ', looking for '('
            elif self.state == 14:
                if char == '(':
                    self.state = 15  # Transition to state 15 (valid token ends here)
                else:
                    raise ValueError(f"Lexical Error: Expected '(' but got '{char}' at position {i + 1}")

            i += 1  # Move to the next character

        # Valid token is 'back (' with space
        if self.state == 14:
            return "back_token"  # Valid 'back' (delim 4)

        # Invalid state if any other sequence
        raise ValueError("Lexical Error: Invalid token.")
    
    def c_token(self, token):
        i = 0  # Index of current character
        length = len(token)
        self.state = 0  # Start in the initial state

        while i < length:
            char = token[i]

            # State 0: Initial state, looking for 'c'
            if self.state == 0:
                if char == 'c':  # First character of 'c_token'
                    self.state = 21  # Transition to state 21
                else:
                    raise ValueError(f"Lexical Error: Expected 'c' but got '{char}' at position {i + 1}")

            # State 21: After 'c', checking for 'h'
            elif self.state == 21:
                if char == 'h':  # Second character of 'ch'
                    self.state = 22  # Transition to state 22
                else:
                    raise ValueError(f"Lexical Error: Expected 'h' but got '{char}' at position {i + 1}")

            # State 22: After 'ch', checking for 'a'
            elif self.state == 22:
                if char == 'a':  # Third character of 'cha'
                    self.state = 23  # Transition to state 23
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' but got '{char}' at position {i + 1}")

            # State 23: After 'cha', checking for 't'
            elif self.state == 23:
                if char == 't':  # Fourth character of 'chat'
                    self.state = 24  # Transition to state 24
                else:
                    raise ValueError(f"Lexical Error: Expected 't' but got '{char}' at position {i + 1}")

            # State 24: After 'chat', looking for delimiter (delim3 - space)
            elif self.state == 24:
                if char == ' ':  # Space after 'chat'
                    self.state = 25  # Transition to state 25 (valid token ends here)
                elif char == '(':  # '(' immediately after 'chat' could also be valid
                    self.state = 25  # Transition to state 25
                else:
                    raise ValueError(f"Lexical Error: Expected space or '(' after 'chat' but got '{char}' at position {i + 1}")

            # State 25: After 'chat' and space or '(', valid token
            elif self.state == 25:
                return "c_token"  # Valid 'chat (' or 'chat' with space

            i += 1  # Move to the next character

        # Invalid state if any other sequence
        raise ValueError("Lexical Error: Invalid token.")

    def d_token(self, token):
        i = 0  # Index of current character
        length = len(token)
        self.state = 0  # Start in the initial state

        while i < length:
            char = token[i]

            # State 0: Looking for 'd'
            if self.state == 0:
                if char == 'd':  # First character of 'd_token'
                    self.state = 26  # Transition to state 26
                else:
                    raise ValueError(f"Lexical Error: Expected 'd' but got '{char}' at position {i + 1}")

            # State 26: After 'd', looking for 'e'
            elif self.state == 26:
                if char == 'e':  # Second character of 'de'
                    self.state = 27  # Transition to state 27
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' but got '{char}' at position {i + 1}")

            # State 27: After 'de', looking for 'f'
            elif self.state == 27:
                if char == 'f':  # Third character of 'def'
                    self.state = 28  # Transition to state 28
                else:
                    raise ValueError(f"Lexical Error: Expected 'f' but got '{char}' at position {i + 1}")

            # State 28: After 'def', looking for 'u'
            elif self.state == 28:
                if char == 'u':  # Fourth character of 'defu'
                    self.state = 29  # Transition to state 29
                else:
                    raise ValueError(f"Lexical Error: Expected 'u' but got '{char}' at position {i + 1}")

            # State 29: After 'defu', looking for 's'
            elif self.state == 29:
                if char == 's':  # Fifth character of 'defus'
                    self.state = 30  # Transition to state 30
                else:
                    raise ValueError(f"Lexical Error: Expected 's' but got '{char}' at position {i + 1}")

            # State 30: After 'defus', looking for 'e'
            elif self.state == 30:
                if char == 'e':  # Sixth character of 'defuse'
                    self.state = 31  # Transition to state 31
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' but got '{char}' at position {i + 1}")

            # State 31: After 'defuse', look for delimiter (delim3 - space or other)
            elif self.state == 31:
                if char == ' ':  # Space after 'defuse'
                    self.state = 32  # Valid token ends here
                elif char == '(':  # '(' immediately after 'defuse' could also be valid
                    self.state = 32  # Transition to state 32
                else:
                    raise ValueError(f"Lexical Error: Expected space or '(' after 'defuse' but got '{char}' at position {i + 1}")

            # State 32: After 'defuse' and space or '(', valid token
            elif self.state == 32:
                return "d_token"  # Valid 'defuse' with space or '('

            i += 1  # Move to the next character

        # Invalid state if any other sequence
        raise ValueError("Lexical Error: Invalid token.")

    def f_token(self, token):
        i = 0  # Index of current character
        length = len(token)
        self.state = 0  # Start in the initial state

        while i < length:
            char = token[i]

            # State 0: Initial state, looking for 'f'
            if self.state == 0:
                if char == 'f':  # First character of 'f_token' (either 'flank' or 'force')
                    self.state = 33  # Transition to state 33
                else:
                    raise ValueError(f"Lexical Error: Expected 'f' but got '{char}' at position {i + 1}")

            # State 33: After 'f', checking for 'l' (for 'flank' or 'force')
            elif self.state == 33:
                if char == 'l':  # Second character of 'flank' or 'force'
                    self.state = 34  # Transition to state 34
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' but got '{char}' at position {i + 1}")

            # State 34: After 'fl', checking for 'a' (for 'flank')
            elif self.state == 34:
                if char == 'a':  # Third character of 'flank'
                    self.state = 35  # Transition to state 35
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' but got '{char}' at position {i + 1}")

            # State 35: After 'fla', checking for 'n' (for 'flank')
            elif self.state == 35:
                if char == 'n':  # Fourth character of 'flank'
                    self.state = 36  # Transition to state 36
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' but got '{char}' at position {i + 1}")

            # State 36: After 'flan', checking for 'k' (for 'flank')
            elif self.state == 36:
                if char == 'k':  # Fifth character of 'flank'
                    self.state = 37  # Transition to state 37
                else:
                    raise ValueError(f"Lexical Error: Expected 'k' but got '{char}' at position {i + 1}")

            # State 37: After 'flank', looking for space (delim3)
            elif self.state == 37:
                if char == ' ':  # Space after 'flank'
                    self.state = 38  # Transition to state 38 (valid token ends here)
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'flank' but got '{char}' at position {i + 1}")

            # State 38: After 'flank' and space, valid token
            elif self.state == 38:
                return "f_token"  # Valid 'flank' with space (delim3)

            # State 39: After 'f', checking for 'o' (for 'force')
            elif self.state == 39:
                if char == 'o':  # Second character of 'force'
                    self.state = 40  # Transition to state 40
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' but got '{char}' at position {i + 1}")

            # State 40: After 'fo', checking for 'r' (for 'force')
            elif self.state == 40:
                if char == 'r':  # Third character of 'force'
                    self.state = 41  # Transition to state 41
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' but got '{char}' at position {i + 1}")

            # State 41: After 'for', checking for 'c' (for 'force')
            elif self.state == 41:
                if char == 'c':  # Fourth character of 'force'
                    self.state = 42  # Transition to state 42
                else:
                    raise ValueError(f"Lexical Error: Expected 'c' but got '{char}' at position {i + 1}")

            # State 42: After 'forc', checking for 'e' (for 'force')
            elif self.state == 42:
                if char == 'e':  # Fifth character of 'force'
                    self.state = 43  # Transition to state 43
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' but got '{char}' at position {i + 1}")

            # State 43: After 'force', looking for space (delim3)
            elif self.state == 43:
                if char == ' ':  # Space after 'force'
                    self.state = 44  # Transition to state 44 (valid token ends here)
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'force' but got '{char}' at position {i + 1}")

            # State 44: After 'force' and space, valid token
            elif self.state == 44:
                return "f_token"  # Valid 'force' with space (delim3)

            i += 1  # Move to the next character

        # Invalid state if any other sequence
        raise ValueError("Lexical Error: Invalid token.")

    def g_token(self, token):
        i = 0  # Index of current character
        length = len(token)
        self.state = 0  # Start in the initial state

        while i < length:
            char = token[i]

            # State 0: Initial state, looking for 'g'
            if self.state == 0:
                if char == 'g':  # First character of 'g_token'
                    self.state = 44  # Transition to state 44
                else:
                    raise ValueError(f"Lexical Error: Expected 'g' but got '{char}' at position {i + 1}")

            # State 44: After 'g', looking for 'l'
            elif self.state == 44:
                if char == 'l':  # Second character of 'gl'
                    self.state = 45  # Transition to state 45
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' but got '{char}' at position {i + 1}")

            # State 45: After 'gl', looking for 'o'
            elif self.state == 45:
                if char == 'o':  # Third character of 'glo'
                    self.state = 46  # Transition to state 46
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' but got '{char}' at position {i + 1}")

            # State 46: After 'glo', looking for 'b'
            elif self.state == 46:
                if char == 'b':  # Fourth character of 'glob'
                    self.state = 47  # Transition to state 47
                else:
                    raise ValueError(f"Lexical Error: Expected 'b' but got '{char}' at position {i + 1}")

            # State 47: After 'glob', looking for 'e'
            elif self.state == 47:
                if char == 'e':  # Fifth character of 'globe'
                    self.state = 48  # Transition to state 48
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' but got '{char}' at position {i + 1}")

            # State 48: After 'globe', looking for space (delim3)
            elif self.state == 48:
                if char == ' ':  # Space after 'globe'
                    self.state = 49  # Transition to state 49 (valid token ends here)
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'globe' but got '{char}' at position {i + 1}")

            # State 49: After 'globe' and space, valid token
            elif self.state == 49:
                return "g_token"  # Valid 'globe' followed by space

            i += 1  # Move to the next character

        # Invalid state if any other sequence
        raise ValueError("Lexical Error: Invalid token.")



    def i_token(self, token):
        i = 0
        length = len(token)
        self.state = 50  # Start with state 50 for 'in', 'inst', 'info'

        while i < length:
            char = token[i]

            if self.state == 50:  # Looking for 'i'
                if char == 'i':
                    self.state = 51
                else:
                    raise ValueError(f"Lexical Error: Expected 'i' but got '{char}' at position {i + 1}")

            elif self.state == 51:  # Looking for 'n'
                if char == 'n':
                    self.state = 52
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' but got '{char}' at position {i + 1}")

            elif self.state == 52:  # Looking for 's' (for 'inst')
                if char == 's':
                    self.state = 53  # Transition to 'inst'
                else:
                    self.state = 56  # Transition to 'info'

            elif self.state == 53:  # Looking for 't' (for 'inst')
                if char == 't':
                    self.state = 54
                else:
                    raise ValueError(f"Lexical Error: Expected 't' but got '{char}' at position {i + 1}")

            elif self.state == 54:  # After 'inst', check for space (delim3)
                if char == ' ':
                    self.state = 55
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'inst' but got '{char}' at position {i + 1}")

            elif self.state == 55:  # Valid 'inst' followed by space
                return "inst_token"

            elif self.state == 56:  # After 'in', looking for 'f' (for 'info')
                if char == 'f':
                    self.state = 57
                else:
                    raise ValueError(f"Lexical Error: Expected 'f' after 'in' but got '{char}' at position {i + 1}")

            elif self.state == 57:  # After 'inf', looking for 'o' (for 'info')
                if char == 'o':
                    self.state = 58
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' after 'inf' but got '{char}' at position {i + 1}")

            elif self.state == 58:  # After 'info', check for space (delim4)
                if char == ' ':
                    self.state = 59
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'info' but got '{char}' at position {i + 1}")

            elif self.state == 59:  # Valid 'info' followed by space
                return "info_token"

            i += 1  # Move to the next character
        
        # If we didn't complete the expected word
        raise ValueError(f"Lexical Error: Invalid token.")

    def l_token(self, token):
        i = 0
        length = len(token)
        self.state = 59  # Start with state 59 for 'l' (start of 'load')

        while i < length:
            char = token[i]

            if self.state == 59:  # Looking for 'l'
                if char == 'l':
                    self.state = 60
                else:
                    raise ValueError(f"Lexical Error: Expected 'l' but got '{char}' at position {i + 1}")

            elif self.state == 60:  # Looking for 'o'
                if char == 'o':
                    self.state = 61
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' but got '{char}' at position {i + 1}")

            elif self.state == 61:  # Looking for 'a'
                if char == 'a':
                    self.state = 62
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' but got '{char}' at position {i + 1}")

            elif self.state == 62:  # Looking for 'd'
                if char == 'd':
                    self.state = 63  # Transition to check for delimiter
                else:
                    raise ValueError(f"Lexical Error: Expected 'd' but got '{char}' at position {i + 1}")

            elif self.state == 63:  # After 'load', check for delimiter (delim4 - space or other)
                if char == ' ':
                    self.state = 64
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'load' but got '{char}' at position {i + 1}")

            elif self.state == 64:  # Valid 'load' followed by space (delim4)
                return "l_token"  # Successfully identified the 'load' token followed by a space

            i += 1  # Move to the next character

        # If we didn't complete the expected word
        raise ValueError(f"Lexical Error: Invalid token.")

    def n_token(self, token):
        i = 0
        length = len(token)
        self.state = 64  # Start with state 64 for 'n' (start of 'neg' or 'not')

        while i < length:
            char = token[i]

            if self.state == 64:  # Looking for 'n' (start of 'neg' or 'not')
                if char == 'n':
                    self.state = 65
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' but got '{char}' at position {i + 1}")

            elif self.state == 65:  # Looking for 'e'
                if char == 'e':
                    self.state = 66
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' but got '{char}' at position {i + 1}")

            elif self.state == 66:  # Looking for 'g' (for 'neg')
                if char == 'g':
                    self.state = 67
                else:
                    self.state = 70  # If not 'g', it could be 'not', transition to 'not'

            elif self.state == 67:  # Finished with 'neg', check for delim8
                if char in [' ', '=', ')', '\0', '!']:  # Delim8
                    self.state = 68
                else:
                    raise ValueError(f"Lexical Error: Expected one of delimiters in 'delim8' after 'neg' but got '{char}' at position {i + 1}")

            elif self.state == 68:  # Valid 'neg' followed by a delimiter
                return "neg_token"

            elif self.state == 70:  # Looking for 'o' for 'not'
                if char == 'o':
                    self.state = 71
                else:
                    raise ValueError(f"Lexical Error: Expected 'o' after 'n' but got '{char}' at position {i + 1}")

            elif self.state == 71:  # Looking for 't' for 'not'
                if char == 't':
                    self.state = 72
                else:
                    raise ValueError(f"Lexical Error: Expected 't' after 'no' but got '{char}' at position {i + 1}")

            elif self.state == 72:  # Finished with 'not', check for delim4
                if char == '(':  # Delim4
                    self.state = 73
                else:
                    raise ValueError(f"Lexical Error: Expected '(' after 'not' but got '{char}' at position {i + 1}")

            elif self.state == 73:  # Valid 'not' followed by '('
                return "not_token"

            i += 1  # Move to the next character
            
        # If we didn't complete the expected word
        raise ValueError(f"Lexical Error: Invalid token.")
    
















    def p_token(self, token):
        i = 0  # Index of the current character
        length = len(token)
        self.state = 74  # Start at state 74, corresponding to 'p'

        while i < length:
            char = token[i]

            # State 74: Start state, checking for 'p'
            if self.state == 74:
                if char == 'p':
                    self.state = 75  # Transition to state 75 (for 'e')
                else:
                    raise ValueError(f"Lexical Error: Expected 'p' but got '{char}' at position {i + 1}")

            # State 75: After 'p', checking for 'e' (Reserved word: 'perim')
            elif self.state == 75:
                if char == 'e':
                    self.state = 76  # Transition to state 76 (for 'r')
                else:
                    raise ValueError(f"Lexical Error: Expected 'e' but got '{char}' at position {i + 1}")

            # State 76: After 'pe', checking for 'r' (Reserved word: 'perim')
            elif self.state == 76:
                if char == 'r':
                    self.state = 77  # Transition to state 77 (for 'i')
                else:
                    raise ValueError(f"Lexical Error: Expected 'r' but got '{char}' at position {i + 1}")

            # State 77: After 'per', checking for 'i' (Reserved word: 'perim')
            elif self.state == 77:
                if char == 'i':
                    self.state = 78  # Transition to state 78 (for 'm')
                else:
                    raise ValueError(f"Lexical Error: Expected 'i' but got '{char}' at position {i + 1}")

            # State 78: After 'peri', checking for 'm' (Reserved word: 'perim')
            elif self.state == 78:
                if char == 'm':
                    self.state = 79  # Transition to state 79 (end of 'perim')
                elif char == 'l':  # Check for 'l' (Reserved word: 'plant')
                    self.state = 80  # Transition to state 80 (for 'a')
                else:
                    raise ValueError(f"Lexical Error: Expected 'm' or 'l' but got '{char}' at position {i + 1}")

            # State 79: End of 'perim', check for delimiter or other token
            elif self.state == 79:
                return "perim_token"  # Successfully recognized 'perim'

            # State 80: After 'pl', checking for 'a' (Reserved word: 'plant')
            elif self.state == 80:
                if char == 'a':
                    self.state = 81  # Transition to state 81 (for 'n')
                else:
                    raise ValueError(f"Lexical Error: Expected 'a' but got '{char}' at position {i + 1}")

            # State 81: After 'pla', checking for 'n' (Reserved word: 'plant')
            elif self.state == 81:
                if char == 'n':
                    self.state = 82  # Transition to state 82 (for 't')
                else:
                    raise ValueError(f"Lexical Error: Expected 'n' but got '{char}' at position {i + 1}")

            # State 82: After 'plan', checking for 't' (Reserved word: 'plant')
            elif self.state == 82:
                if char == 't':
                    self.state = 83  # Transition to state 83 (delimiters)
                else:
                    raise ValueError(f"Lexical Error: Expected 't' but got '{char}' at position {i + 1}")

            # State 83: End of 'plant', check for delimiter
            elif self.state == 83:
                return "plant_token"  # Successfully recognized 'plant'

            # State 86: After 'p', checking for 'u' (Reserved word: 'push')
            elif self.state == 86:
                if char == 'u':
                    self.state = 87  # Transition to state 87 (for 's')
                else:
                    raise ValueError(f"Lexical Error: Expected 'u' but got '{char}' at position {i + 1}")

            # State 87: After 'pu', checking for 's' (Reserved word: 'push')
            elif self.state == 87:
                if char == 's':
                    self.state = 88  # Transition to state 88 (for 'h')
                else:
                    raise ValueError(f"Lexical Error: Expected 's' but got '{char}' at position {i + 1}")

            # State 88: After 'pus', checking for 'h' (Reserved word: 'push')
            elif self.state == 88:
                if char == 'h':
                    self.state = 91  # Transition to state 91 (end of 'push')
                else:
                    raise ValueError(f"Lexical Error: Expected 'h' but got '{char}' at position {i + 1}")

            # State 91: End of 'push', check for delimiter
            elif self.state == 91:
                return "push_token"  # Successfully recognized 'push'

            i += 1  # Move to the next character

        raise ValueError("Lexical Error: Invalid token.")






















    def classify_token(self, token):
        # Check against literals
        for literal_key, literal_values in self.literals.items():
            if token in literal_values:
                return f"{literal_key}_token"
        
        # If it's not a literal, check if it's a reserved word
        if token in self.reserved_words:
            return f"{token}_token"
        
        # Otherwise, classify as an identifier
        return "identifier_token"


    def tokenize(self, input_string):
        """Tokenizes the input string based on predefined rules using delimiters from delim1 to delim27."""
        tokens = []
        i = 0
        length = len(input_string)

        while i < length:
            char = input_string[i]
            
            # Handle delimiters from delim1 to delim27
            found_delim = False
            for delim_key, delim_chars in self.delimiters.items():
                if char in delim_chars:
                    tokens.append((char, delim_key))  # Tokenize the delimiter and record its key
                    i += 1  # Move to the next character
                    found_delim = True
                    break  # Exit the loop once the delimiter is found and processed
            
            if not found_delim:
                # Handle whitespace (optional)
                if char.isspace():
                    i += 1
                    continue

                # Handle specific keywords like 'back', 'bounce', 'and', 'chat'
                if char.isalpha():
                    start = i
                    while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        i += 1
                    token = input_string[start:i]

                    # Handle the reserved word 'abort' and check for ';' delimiter
                    if token == "abort":
                        tokens.append(("abort_token", "abort"))
                        
                        # Check for ';' delimiter after 'abort'
                        if i < length and input_string[i] == ";":
                            tokens.append((input_string[i], input_string[i]))
                            i += 1  # Move past the ';'
                            
                            # Now lookahead for delim27 after ';' (checking for '\n' and '}')
                            if i < length and input_string[i] in ['\n', '}']:
                                tokens.append((input_string[i], input_string[i]))
                                i += 1  # Move past the delimiter

                        else:
                            raise ValueError(f"Lexical Error: Missing delimiter ';' after 'abort' at position {i}")
                                        
                # Handle the reserved word 'and' and check for space or '(' delimiter using delim5
                    elif token == "and":
                        tokens.append(("and_token", "and"))

                        # Check if the next character is either a space or '(' using delim5
                        if i < length and input_string[i] in [" ", "("]:
                            delimiters = []

                            # Check for space
                            if input_string[i] == " ":
                                delimiters.append("SPACE")
                                i += 1  # move to the next character after space
                            
                            # Check for opening parenthesis
                            elif input_string[i] == "(":
                                delimiters.append("(")
                                i += 1  # move to the next character after '('

                            # Add token for delim5 with the delimiters
                            tokens.append(("delim5", ", ".join(delimiters)))

                        else:
                            # Raise error if neither space nor '(' follows 'and'
                            raise ValueError(f"Lexical Error: Missing space or '(' after 'and' at position {i}")


                        # Lookahead for delim17 (characters after 'and')
                        if i < length and input_string[i] in ['\0', 'num', 'alpha', '(', ')', ',']:
                            # Check for a specific set of delimiters defined in delim17
                            tokens.append(("delim17", input_string[i]))
                            i += 1
                        else:
                            raise ValueError(f"Lexical Error: Missing valid delimiter after 'and' at position {i}")
                        
                    # Now lookahead for delim18 after encountering ')'
                        if i < length and input_string[i] in [' ', '\0', '\n', 'alpha', '+', '-', '*', '/', '%', '!', '=', '<', '>', ',', '}', ')', '{', ';']:
                            # Check if the character is part of delim18
                            tokens.append(("delim18", input_string[i]))
                            i += 1
                        else:
                            raise ValueError(f"Lexical Error: Missing valid delimiter after ')' at position {i}")





                    # Handle the reserved word 'back' and check for delimiters
                    elif token == "back":
                        tokens.append(("back_token", "back"))
                        
                        # Check if the next character is either a space or '(' using delim5
                        if i < length and input_string[i] in ["("]:
                            delimiters = []

                            # Check for opening parenthesis
                            if input_string[i] == "(":
                                delimiters.append("(")
                                i += 1  # move to the next character after '('

                            # Add token for delim5 with the delimiters
                            tokens.append(("delim4", ", ".join(delimiters)))

                        else:
                            # Raise error if neither space nor '(' follows 'and'
                            raise ValueError(f"Lexical Error: Missing space or '(' after 'and' at position {i}")


                        # Lookahead for delim17 (characters after 'and')
                        if i < length and input_string[i] in ['\0', 'num', 'alpha', '(', ')', ',']:
                            # Check for a specific set of delimiters defined in delim17
                            tokens.append(("delim17", input_string[i]))
                            i += 1
                        else:
                            raise ValueError(f"Lexical Error: Missing valid delimiter after 'and' at position {i}")
                        
                        # Now lookahead for delim18 after encountering ')'
                        if i < length and input_string[i] in [' ', '\0', '\n', 'alpha', '+', '-', '*', '/', '%', '!', '=', '<', '>', ',', '}', ')', '{', ';']:
                            # Check if the character is part of delim18
                            tokens.append(("delim18", input_string[i]))
                            i += 1
                        else:
                            raise ValueError(f"Lexical Error: Missing valid delimiter after ')' at position {i}")


                    
                    # Updated lexer logic to handle \n correctly
                    elif token == "bounce":
                        tokens.append(("bounce_token", "bounce"))

                        if i < length and input_string[i] == " ":
                            raise ValueError(f"Lexical Error: Invalid space between 'bounce' and ';' at position {i}")
                        
                        elif i < length and input_string[i] == ";":
                            tokens.append((";", ";"))
                            i += 1
                            
                            # Check for newline or closing brace as valid delimiters after the semicolon
                            if i < length and input_string[i] in ['\n', '}']:
                                tokens.append(("delim27", input_string[i]))  # Handle the newline or closing brace
                                i += 1
                            else:
                                raise ValueError(f"Lexical Error: Missing valid delimiter ('\\n' or '}}') after ';' at position {i}")


                    # Handle the reserved word 'chat'
                    elif token == "chat":
                        if i < length and input_string[i] == " ":
                            tokens.append(("c_token", "chat"))
                            tokens.append(("SPACE", "SPACE"))
                            i += 1
                            
                            # Extract identifier after "chat"
                            identifier = ''
                            while i < length and (
                                ('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z')
                            ):
                                identifier += input_string[i]
                                i += 1

                            if identifier:
                                tokens.append(("IDENTIFIER", identifier))
                            else:
                                raise ValueError(f"Lexical Error: Expected identifier after 'chat' at position {i}")

                            # Expect space after identifier
                            if i < length and input_string[i] == " ":
                                tokens.append(("SPACE", "SPACE"))
                                i += 1
                            else:
                                raise ValueError(f"Lexical Error: Expected space after identifier at position {i}")

                            # Lookahead for `=` after space
                            if i < length and input_string[i] == "=":
                                tokens.append(("EQUALS", "="))
                                i += 1
                            else:
                                raise ValueError(f"Lexical Error: Expected '=' after space at position {i}")

                            # Expect space after `=`
                            if i < length and input_string[i] == " ":
                                tokens.append(("SPACE", "SPACE"))
                                i += 1
                            else:
                                raise ValueError(f"Lexical Error: Expected space after '=' at position {i}")

                            # Handle assignment value inside single quotes
                            if i < length and input_string[i] == "'":
                                tokens.append(("SINGLE_QUOTE", "'"))
                                i += 1

                                # Extract character inside quotes
                                if i < length and (
                                    ('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z')
                                ):
                                    tokens.append(("CHAR_LITERAL", input_string[i]))
                                    i += 1
                                else:
                                    raise ValueError(f"Lexical Error: Expected character after '=' at position {i}")

                                # Expect closing single quote
                                if i < length and input_string[i] == "'":
                                    tokens.append(("SINGLE_QUOTE", "'"))
                                    i += 1
                                else:
                                    raise ValueError(f"Lexical Error: Missing closing single quote at position {i}")

                                # Expect semicolon
                                if i < length and input_string[i] == ";":
                                    tokens.append(("SEMICOLON", ";"))
                                    i += 1
                                else:
                                    raise ValueError(f"Lexical Error: Missing ';' after assignment at position {i}")
                            else:
                                raise ValueError(f"Lexical Error: Expected single quote after '=' at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: 'chat' must be followed by a space at position {i}")
                                



                    # Handle the reserved word 'defuse'
                    elif token == "defuse":
                        if i < length and input_string[i] == " ":
                            tokens.append(("d_token", "defuse"))
                            tokens.append(("SPACE", "SPACE"))
                            i += 1  # Move past the space

                            # Expect an identifier after the space
                            if i < length and (
                                ('a' <= input_string[i] <= 'z') or 
                                ('A' <= input_string[i] <= 'Z')
                            ):
                                identifier = ""
                                while i < length and (
                                    ('a' <= input_string[i] <= 'z') or 
                                    ('A' <= input_string[i] <= 'Z') or 
                                    ('0' <= input_string[i] <= '9')
                                ):
                                    identifier += input_string[i]
                                    i += 1
                                tokens.append(("identifier_token", identifier))

                                # Check for space after the identifier
                                if i < length and input_string[i] == " ":
                                    tokens.append(("SPACE", "SPACE"))
                                    i += 1

                                    # Check for assignment operator '='
                                    if i < length and input_string[i] == "=":
                                        tokens.append(("assign_op", "="))
                                        i += 1

                                        # Check for space after '='
                                        if i < length and input_string[i] == " ":
                                            tokens.append(("SPACE", "SPACE"))
                                            i += 1

                                            # Lookahead for valid `delim13`
                                            if i < length and (
                                                ('a' <= input_string[i] <= 'z') or 
                                                ('A' <= input_string[i] <= 'Z') or 
                                                ('0' <= input_string[i] <= '9') or 
                                                input_string[i] in ['"', "'", '(']
                                            ):
                                                tokens.append(("delim13", input_string[i]))
                                                i += 1
                                            else:
                                                raise ValueError(f"Lexical Error: Expected valid value after '=' at position {i}")
                                        else:
                                            raise ValueError(f"Lexical Error: Expected space after '=' at position {i}")
                                    else:
                                        raise ValueError(f"Lexical Error: Expected '=' after identifier at position {i}")
                                else:
                                    raise ValueError(f"Lexical Error: Expected space after identifier at position {i}")
                            else:
                                raise ValueError(f"Lexical Error: Expected identifier after 'defuse ' at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: 'defuse' must be followed by a space at position {i}")

                    # Handle the reserved word 'flank' (f_token) and check for space (delim3)
                    elif token == "flank":
                        if i < length and input_string[i] == " ":
                            tokens.append(("f_token", "flank"))
                            tokens.append(("SPACE", "SPACE"))  # Add the space as delim3
                            i += 1  # Move past the space

                            # Handle the lookahead for the next tokens (expect space before identifier)
                            if i < length and ('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z'):
                                # Handle identifier token (e.g., var1)
                                identifier = input_string[i]
                                i += 1
                                while i < length and (('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z') or ('0' <= input_string[i] <= '9')):
                                    identifier += input_string[i]
                                    i += 1
                                tokens.append(("identifier_token", identifier))

                            # Expecting a space after the identifier before '='
                            if i < length and input_string[i] == " ":
                                tokens.append(("SPACE", "SPACE"))
                                i += 1  # Move past the space
                                
                                # Expecting '=' (delim13) now
                                if i < length and input_string[i] == "=":
                                    tokens.append(("delim13", "="))
                                    i += 1  # Move past '='

                                    # Expecting a space after '=' before continuing
                                    if i < length and input_string[i] == " ":
                                        tokens.append(("SPACE", "SPACE"))
                                        i += 1  # Move past the space

                                        # After the space, expect a number or identifier or other valid tokens
                                        if i < length and ('0' <= input_string[i] <= '9'):
                                            # Handle number token (e.g., 1.23)
                                            num = input_string[i]
                                            i += 1
                                            while i < length and ('0' <= input_string[i] <= '9' or input_string[i] == '.'):
                                                num += input_string[i]
                                                i += 1
                                            tokens.append(("num_token", num))

                                        # Expecting a semicolon or another valid token after the number
                                        if i < length and input_string[i] == ";":
                                            tokens.append(("delim25", ";"))
                                            i += 1
                                    else:
                                        raise ValueError(f"Lexical Error: Expected space after '=' at position {i}")

                                else:
                                    raise ValueError(f"Lexical Error: Expected '=' after identifier at position {i}")
                            else:
                                raise ValueError(f"Lexical Error: Expected space after identifier at position {i}")


                    # Handling for the "force" token
                    elif token == "force":
                        if i < length and input_string[i] == " ":
                            tokens.append(("f_token", "force"))  # Tokenize 'force'
                            tokens.append(("SPACE", "SPACE"))  # Space token
                            i += 1  # Move past the space

                            # Lookahead for an identifier after 'force'
                            if i < length and (
                                ('a' <= input_string[i] <= 'z') or
                                ('A' <= input_string[i] <= 'Z') or
                                input_string[i] == '_'):  # Valid identifier characters
                                identifier = input_string[i]
                                i += 1
                                while i < length and (('a' <= input_string[i] <= 'z') or
                                                    ('A' <= input_string[i] <= 'Z') or
                                                    ('0' <= input_string[i] <= '9') or
                                                    input_string[i] == '_'):
                                    identifier += input_string[i]
                                    i += 1
                                tokens.append(("identifier_token", identifier))  # Tokenize identifier

                                # After identifier, lookahead for the 'in' token (with optional space before it)
                                if i < length and input_string[i] == " ":
                                    tokens.append(("SPACE", "SPACE"))  # Add space after identifier
                                    i += 1  # Move past the space

                                if i < length and input_string[i:i+2] == "in":
                                    tokens.append(("in_token", "in"))  # Tokenize 'in'
                                    i += 2  # Move past 'in'

                                    # Lookahead for space after 'in'
                                    if i < length and input_string[i] == " ":
                                        tokens.append(("SPACE", "SPACE"))  # Add space after 'in'
                                        i += 1  # Move past the space

                                        # Now check if 'perim' follows after space
                                        if i < length and input_string[i:i+5] == "perim":
                                            tokens.append(("perim_token", "perim"))  # Tokenize 'perim' as p_token
                                            i += 5  # Move past the 'perim'

                                            # Ensure space after 'perim' before checking for '('
                                            if i < length and input_string[i] == " ":
                                                tokens.append(("SPACE", "SPACE"))  # Add space after 'perim'
                                                i += 1  # Move past the space

                                                # Lookahead for delimiters (delim25)
                                                if i < length and (input_string[i] == "(" or 
                                                                    ('0' <= input_string[i] <= '9') or  # Numbers
                                                                    ('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z') or  # Letters
                                                                    input_string[i] in ['(', "'", '"', '=', '+', '-', '*', '/', '%', ' ', '>', '<', '!', '^']):
                                                    if input_string[i] == "(":
                                                        tokens.append(("delim_paren", "("))  # Tokenize the opening parenthesis
                                                        i += 1  # Move past the '('
                                                    else:
                                                        # Handle other delim25 cases (e.g., number, symbols, alpha)
                                                        tokens.append(("delim25", input_string[i]))  # Tokenize as delim25
                                                        i += 1  # Move past the current character
                                                else:
                                                    raise ValueError(f"Lexical Error: Invalid token following 'perim' at position {i}. Expected delim25 token after '('.")


                                                # Lookahead for closing parenthesis ')'
                                                if i < length and input_string[i] == ")":
                                                    tokens.append(("delim_paren", ")"))  # Tokenize the closing parenthesis
                                                    i += 1  # Move past the ')'

                                                # Lookahead for semicolon
                                                if i < length and input_string[i] == ";":
                                                    tokens.append(("delim_semicolon", ";"))  # Tokenize semicolon
                                                    i += 1  # Move past the semicolon
                                            else:
                                                raise ValueError(f"Lexical Error: Expected space after 'perim' at position {i}")
                                        else:
                                            raise ValueError(f"Lexical Error: Expected 'perim' after 'in' at position {i}")
                                    else:
                                        raise ValueError(f"Lexical Error: Expected space after 'in' at position {i}")
                                else:
                                    raise ValueError(f"Lexical Error: Expected 'in' after identifier at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: 'force' must be followed by a space at position {i}")

                    # Handling for the "in" token
                    elif token == "in":
                        if i < length and input_string[i] == " ":
                            tokens.append(("i_token", "in"))  # Tokenize 'in'
                            tokens.append(("SPACE", "SPACE"))  # Space token
                            i += 1  # Move past the space

                            # Lookahead for valid next token after "in"
                            if i < length:
                                next_char = input_string[i]
                                if (
                                    ('a' <= next_char <= 'z') or
                                    ('A' <= next_char <= 'Z') or
                                    ('0' <= next_char <= '9') or
                                    next_char in ['(', "'", '"', '=', '+', '-', '*', '/', '%', ',', '>', '<', '!', '^']
                                ):
                                    # Handle different valid tokens after "in"
                                    if ('a' <= next_char <= 'z') or ('A' <= next_char <= 'Z') or next_char == '_':  # Handle identifiers
                                        start = i
                                        while i < length and (
                                            ('a' <= input_string[i] <= 'z') or
                                            ('A' <= input_string[i] <= 'Z') or
                                            ('0' <= input_string[i] <= '9') or
                                            input_string[i] == '_'):
                                            i += 1
                                        tokens.append(("identifier_token", input_string[start:i]))  # Tokenize the identifier
                                    elif '0' <= next_char <= '9':  # Handle numbers
                                        start = i
                                        while i < length and '0' <= input_string[i] <= '9':
                                            i += 1
                                        tokens.append(("number_token", input_string[start:i]))  # Tokenize the number
                                    elif next_char in ['(', "'", '"', '=', '+', '-', '*', '/', '%', ',', '>', '<', '!', '^']:  # Handle operators
                                        tokens.append(("operator_token", next_char))  # Tokenize the operator
                                        i += 1  # Move past the operator
                                    else:
                                        raise ValueError(f"Lexical Error: Unexpected character after 'in' at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: Expected space after 'in' at position {i}")


                    # Handling for the "perim" token
                    elif token == "perim":
                        if i < length and input_string[i] == " ":
                            tokens.append(("p_token", "perim"))  # Tokenize 'perim'
                            tokens.append(("SPACE", "SPACE"))  # Space token
                            i += 1  # Move past the space

                            # Lookahead for opening parenthesis '(' after the space
                            if i < length and input_string[i] == "(":
                                tokens.append(("delim_paren", "("))  # Tokenize the opening parenthesis
                                i += 1  # Move past the '('

                                # Now process the content inside the parentheses
                                while i < length and input_string[i] != ")":
                                    # Handle string literals
                                    if input_string[i] == '"':  # String literal
                                        start = i
                                        i += 1
                                        while i < length and input_string[i] != '"':
                                            i += 1
                                        if i < length and input_string[i] == '"':
                                            tokens.append(("char_literal", input_string[start:i+1]))  # Tokenize the string literal
                                            i += 1  # Move past the closing quote

                                    # Handle character literals
                                    elif input_string[i] == "'":  # Character literal
                                        start = i
                                        i += 1
                                        while i < length and input_string[i] != "'":
                                            i += 1
                                        if i < length and input_string[i] == "'":
                                            tokens.append(("char_literal", input_string[start:i+1]))  # Tokenize the character literal
                                            i += 1  # Move past the closing quote

                                    # Handle numbers
                                    elif '0' <= input_string[i] <= '9':
                                        start = i
                                        while i < length and '0' <= input_string[i] <= '9':
                                            i += 1
                                        tokens.append(("num_literal", input_string[start:i]))  # Tokenize the number

                                    # Handle operators or other symbols
                                    elif input_string[i] in ['+', '-', '=', '*', '/', '%', '>', '<', '!', '^']:
                                        tokens.append(("operator_token", input_string[i]))  # Tokenize operators
                                        i += 1  # Move past the operator

                                    # Handle spaces (to skip and continue tokenizing)
                                    elif input_string[i] == " ":
                                        tokens.append(("SPACE", "SPACE"))
                                        i += 1

                                    # Handle identifier or variable names
                                    elif ('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z'):
                                        start = i
                                        while i < length and (('a' <= input_string[i] <= 'z') or ('A' <= input_string[i] <= 'Z') or ('0' <= input_string[i] <= '9') or input_string[i] == '_'):
                                            i += 1
                                        tokens.append(("identifier_token", input_string[start:i]))  # Tokenize identifier

                                    # Skip any other characters (error handling can be added)
                                    else:
                                        i += 1

                                # Ensure closing parenthesis
                                if i < length and input_string[i] == ")":
                                    tokens.append(("delim_paren", ")"))  # Tokenize the closing parenthesis
                                    i += 1  # Move past the ')'
                                else:
                                    raise ValueError(f"Lexical Error: Expected closing parenthesis ')' after expression inside 'perim' at position {i}")
                            else:
                                raise ValueError(f"Lexical Error: Expected '(' after space following 'perim' at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: Expected space after 'perim' at position {i}")


                                        # Handle the reserved word 'info' (delim4 - '(')
                    elif token == "info":
                        if i < length and input_string[i] == "(":
                            tokens.append(("i_token", "info"))
                            tokens.append(("(", "("))  # Add '(' as delim4
                            i += 1  # Move past the '('
                        else:
                            # Raise an error if space is not found after 'globe'
                            raise ValueError(f"Lexical Error: 'info' must be followed by a space and '(' at position {i}")
                        
                    # Handle the reserved word 'inst' (delim3 - space)
                    elif token == "inst":
                        if i < length and input_string[i] == " ":
                            tokens.append(("i_token", "inst"))
                            tokens.append(("SPACE", "SPACE"))  # Add space as delim3
                            i += 1  # Move past the space
                        else:
                            # Raise an error if space is not found after 'globe'
                            raise ValueError(f"Lexical Error: 'inst' must be followed by a space at position {i}")
                        
                                    # Handle the reserved word 'load' (l_token) followed by '(' (delim4)
                    elif token == "load":
                        if i < length and input_string[i] == "{":
                            tokens.append(("l_token", "load"))
                            tokens.append(("{", "{"))  # Add '(' as delim1
                            i += 1  # Move past the '('
                        else:
                            # Raise an error if space is not found after 'globe'
                            raise ValueError(f"Lexical Error: 'load' must be followed by a '(' at position {i}")
                        
                    # Handle the reserved word 'neg' (delim8 - space, '=', ')', '\0', '!')
                    elif token == "neg":
                        tokens.append(("neg_token", "neg"))
                        
                        if i < length:
                            next_char = input_string[i]  # Capture the next character after 'neg'
                            if next_char in [' ', '=', ')', '\0', '!']:
                                tokens.append(("delim8", next_char))  # Correctly append the delimiter lexeme
                                i += 1  # Move past the delimiter
                            else:
                                raise ValueError(f"Lexical Error: Invalid delimiter '{next_char}' after 'neg' at position {i}.")
                        else:
                            raise ValueError("Lexical Error: Expected a delimiter after 'neg' but reached end of input.")

                    # Handle the reserved word 'not' (delim4 - '(')
                    elif token == "not":
                        if i < length and input_string[i] == "(":
                            tokens.append(("not_token", "not"))
                            tokens.append(("(", "("))  # Add '(' as delim4
                            i += 1  # Move past the '('
                        else:
                            raise ValueError(f"Lexical Error: Expected '(' after 'not' at position {i}")

                    # Handle the reserved word 'load' (l_token) followed by '(' (delim4)
                    elif token == "load":
                        if i < length and input_string[i] == "(":
                            tokens.append(("l_token", "load"))
                            tokens.append(("(", "("))  # Add '(' as delim4
                            i += 1  # Move past the '('
                        else:
                            raise ValueError(f"Lexical Error: 'load' must be followed by '(' at position {i}")

                    else:
                        # For other identifiers, classify normally
                        token_type = self.classify_token(token)
                        tokens.append((token_type, token))
                        # Handle the reserved word 'globe' (g_token) and check for space (delim3)

                    return tokens



def main():
    # Prompt the user to input the string
    input_string = input("Enter a string to tokenize: ")

    tokenizer = DEDOSLexicalAnalyzer()
    try:
        # Tokenize the input string
        tokens = tokenizer.tokenize(input_string)

        # Print the token and lexeme for each token
        for token_type, lexeme in tokens:
            print(f"Token: {token_type}, Lexeme: {lexeme}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()









            # Handle delimiters
            found_delim = False
            for delim_key, delim_chars in self.delimiters.items():
                if char in delim_chars:
                    tokens.append((delim_key, char))  # Add token for delimiter
                    i += 1
                    found_delim = True
                    break
            
            if found_delim:
                continue  # Continue the loop if a delimiter was found

            # Handle specific reserved words (like 'and')
            elif i + 3 <= length and input_string[i:i+3] == "and":
                # Check if 'and' is followed by a valid token (space or opening parenthesis)
                if i + 3 < length and input_string[i+3].islower():  # Ensure the next character is lowercase
                    j = i + 3
                    # Consume only the lowercase letters or digits following 'and'
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    identifier = input_string[i+3:j]

                    # Check if the identifier contains any uppercase letters
                    for idx, c in enumerate(identifier):
                        if c.isupper():  # If any character is uppercase
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'and' at position {i + 3 + idx}")

                    tokens.append(("identifier", identifier))  # Tokenize the identifier
                    i = j  # Move past the identifier
                else:
                    tokens.append(("and_token", "and"))
                    i += 3  # Move past 'and'

                    # Check for space or opening parenthesis
                    if i < length and input_string[i] == " ":
                        tokens.append(("SPACE", " "))  # Tokenize space
                        i += 1
                    elif i < length and input_string[i] == "(":
                        tokens.append(("(", "("))  # Tokenize opening parenthesis
                        i += 1
                    else:
                        raise ValueError(f"Lexical Error: 'and' must be followed by space or '(' at position {i}")
            
        # Handle 'abort' keyword (with lowercase identifier check)
            elif input_string[i:i+5] == "abort":
                if i + 5 < length and input_string[i+5].islower():  # Ensure the next character is lowercase
                    j = i + 5
                    while j < length and input_string[j].islower():  # Only accept lowercase letters
                        j += 1
                    identifier = input_string[i:j]
                    
                    # Ensure identifier is fully lowercase
                    for idx, c in enumerate(identifier):
                        if c.isupper():  # If any character is uppercase
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' at position {i + idx}")
                    
                    tokens.append(("identifier", identifier))  # Tokenize the identifier
                    i = j  # Move past the identifier
                else:
                    tokens.append(("abort_token", "abort"))
                    i += 5  # Move past 'abort'

                    if i < length and input_string[i] == ";":
                        i += 1
                        tokens.append((";", ";"))

                    else:
                        raise ValueError(f"Lexical Error: Missing delimiter ';' after 'abort' at position {i}")

                    if i < length and input_string[i] == " ":
                        i += 1
                        tokens.append(("SPACE", " "))


            # Handle 'bounce' keyword
            elif input_string[i:i+6] == "bounce":
                # Check if the next character is alphanumeric (letter or number)
                if i + 6 < length and input_string[i+6].islower():  # Ensure the next character is lowercase
                    j = i + 6
                    # Consume alphanumeric characters following 'bounce'
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    identifier = input_string[i+6:j]

                    # Check if the identifier contains any uppercase letters
                    for idx, c in enumerate(identifier):
                        if c.isupper():  # If any character is uppercase
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'bounce' at position {i + 6 + idx}")

                    tokens.append(("identifier", identifier))  # Tokenize the alphanumeric identifier
                    i = j  # Move past the identifier

                else:
                    # Handle 'bounce' followed by a semicolon
                    if i + 6 < length and input_string[i+6] == ";":
                        tokens.append(("bounce_token", "bounce"))  # Append 'bounce' token
                        i += 7  # Move past 'bounce;'

                        # After semicolon, ensure there are no characters left
                        if i < length:  # Check if there are characters after the semicolon
                            next_char_after_semicolon = input_string[i]
                            raise ValueError(f"Lexical Error: Invalid character '{next_char_after_semicolon}' after ';' at position {i}")
                    else:
                        raise ValueError(f"Lexical Error: Expected ';' after 'bounce' at position {i + 6}")


            # Handle 'back' keyword
            elif input_string[i:i+4] == "back":
                if i + 4 < length:
                    next_char = input_string[i + 4]

                    # Check if 'back' is followed by a lowercase alphanumeric identifier
                    if next_char.islower():
                        j = i + 4
                        # Consume the alphanumeric characters following 'back'
                        while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                            j += 1

                        identifier = input_string[i+4:j]

                        # Check if the identifier contains any uppercase letters
                        for idx, c in enumerate(identifier):
                            if c.isupper():  # If any character is uppercase
                                raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'back' at position {i + 4 + idx}")

                        tokens.append(("identifier", identifier))  # Tokenize the alphanumeric identifier
                        i = j  # Move past the identifier

                    # Check if 'back' is followed by '('
                    elif next_char == "(":
                        tokens.append(("back_token", "back"))  # Append 'back' token
                        tokens.append(("(", "("))  # Append '(' as delimiter
                        i += 5  # Move past 'back('

                    else:
                        raise ValueError(f"Lexical Error: Expected '(' after 'back' at position {i + 4} (found '{next_char}')")
                else:
                    raise ValueError(f"Lexical Error: Expected '(' after 'back'")

            # Handle 'chat' keyword
            elif input_string[i:i+4] == "chat":
                j = i + 4  # Start checking after 'chat'

                # If 'chat' is followed by a lowercase alphanumeric character or '_', treat it as an identifier
                if j < length and input_string[j].islower():
                    start = i  # Include 'chat' in the identifier

                    # Consume the alphanumeric characters following 'chat'
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1

                    identifier = input_string[start:j]

                    # Check for uppercase letters in the identifier
                    for idx, c in enumerate(identifier):
                        if c.isupper():  # If any uppercase letter is found
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'chat' at position {start + idx}")

                    tokens.append(("identifier", identifier))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'chat' followed by a space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'chat' is followed by a space
                    tokens.append(("chat_token", "chat"))  # Append the valid 'chat' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 5  # Move past 'chat' and the space

                else:
                    # Handle 'chat' followed by invalid characters
                    raise ValueError(f"Lexical Error: 'chat' must be followed by a space at position {i}")

            # Handle 'defuse' keyword
            elif input_string[i:i+6] == "defuse":
                j = i + 6  # Start checking after 'defuse'

                # If 'defuse' is followed by a lowercase alphanumeric character or '_', treat it as an identifier
                if j < length and input_string[j].islower():
                    start = i  # Include 'defuse' in the identifier

                    # Consume the alphanumeric characters following 'defuse'
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1

                    identifier = input_string[start:j]

                    # Check for uppercase letters in the identifier
                    for idx, c in enumerate(identifier):
                        if c.isupper():  # If any uppercase letter is found
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' at position {start + idx}")

                    tokens.append(("identifier", identifier))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'defuse' followed by a space (valid case)
                elif j < length and input_string[j] == " ":
                    tokens.append(("defuse_token", "defuse"))  # Append the valid 'defuse' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 7  # Move past 'defuse' and the space

                # Handle 'defuse' followed by opening parenthesis '(' (valid case)
                elif j < length and input_string[j] == "(":
                    tokens.append(("defuse_token", "defuse"))  # Append the valid 'defuse' token
                    tokens.append(("(", "("))  # Tokenize the opening parenthesis
                    i += 7  # Move past 'defuse' and '('

                else:
                    # Handle 'defuse' followed by invalid characters
                    raise ValueError(f"Lexical Error: 'defuse' must be followed by a space or '(' at position {i}")


            elif input_string[i:i+5] == "flank":
                j = i + 5  # Start checking after 'flank'

                # If 'flank' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'flank' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier
                
                # Handle 'flank' followed by space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'flank' is followed by a space
                    tokens.append(("flank_token", "flank"))  # Append the valid 'flank' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 6  # Move past 'flank' and the space
                
                # Handle 'flank' followed by invalid opening parenthesis (raises an error)
                elif j < length and input_string[j] == "(":  # Check if 'flank' is followed by '('
                    raise ValueError(f"Lexical Error: 'flank' must be followed by space, found '(' at position {i}")
                
                # Handle any other invalid character after 'flank'
                else:
                    raise ValueError(f"Lexical Error: 'flank' must be followed by space  at position {i}")

            elif input_string[i:i+5] == "force":
                j = i + 5  # Start checking after 'force'

                # If 'force' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'force' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'force' followed by space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'force' is followed by a space
                    tokens.append(("f_token", "force"))  # Append the valid 'force' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 6  # Move past 'force' and the space

                # Handle invalid characters after 'force'
                else:
                    raise ValueError(f"Lexical Error: 'force' must be followed by space at position {i}")

            # Handle 'globe' token
            elif input_string[i:i+5] == "globe":
                j = i + 5  # Start checking after 'globe'

                # If 'globe' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'globe' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'globe' followed by space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'globe' is followed by a space
                    tokens.append(("g_token", "globe"))  # Append the valid 'globe' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 6  # Move past 'globe' and the space

                # Handle invalid characters after 'globe'
                else:
                    raise ValueError(f"Lexical Error: 'globe' must be followed by space at position {i}")
            # Handle 'inst' token
            # Handle 'inst' token
            elif input_string[i:i+4] == "inst":
                j = i + 4  # Start checking after 'inst'

                # If 'inst' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'inst' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'inst' followed by space (valid case)
                elif j < length and input_string[j] == " ":
                    tokens.append(("inst_token", "inst"))  # Append 'inst' token
                    i += 4  # Move past 'inst'

                    # Skip any leading spaces
                    while i < length and input_string[i] == " ":
                        i += 1

                    # Now expect the identifier after the space
                    if i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        start = i  # Start of the identifier
                        while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            i += 1
                        tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier
                    else:
                        raise ValueError(f"Lexical Error: Expected identifier after 'inst' at position {i}")

                    # Skip spaces after identifier
                    while i < length and input_string[i] == " ":
                        i += 1

                    # Expect '=' after identifier
                    if i < length and input_string[i] == "=":
                        tokens.append(("=", "="))  # Tokenize '='
                        i += 1
                    else:
                        raise ValueError(f"Lexical Error: Expected '=' after identifier at position {i}")

                    # Skip spaces after '='
                    while i < length and input_string[i] == " ":
                        i += 1

                    # Handle INST_LIT (number or literal) after '='
                    if i < length and (input_string[i].isdigit() or input_string[i] == "-" or input_string[i] == "."):
                        start = i
                        if input_string[i] == "-":  # Check for negative numbers
                            i += 1
                        while i < length and (input_string[i].isdigit() or input_string[i] == "."):
                            i += 1
                        token_value = input_string[start:i]
                        if "." in token_value:  # If it's a float, tokenize as FLANK_LIT
                            tokens.append(("FLANK_LIT", token_value))
                        else:  # Otherwise, it's an integer
                            tokens.append(("INST_LIT", token_value))
                    else:
                        raise ValueError(f"Lexical Error: Expected number or literal after '=' at position {i}")

                    # Skip spaces after the literal value
                    while i < length and input_string[i] == " ":
                        i += 1

                    # Expect semicolon ';' at the end of the statement
                    if i < length and input_string[i] == ";":
                        tokens.append((";", ";"))  # Tokenize the semicolon
                        i += 1  # Move past the semicolon

                        # After semicolon, check for newline or space
                        if i < length and input_string[i] == "\n":
                            tokens.append(("NEWLINE", "\n"))  # Tokenize newline as a separate token
                            i += 1  # Move past the newline
                        elif i < length and input_string[i] == " ":
                            tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                            i += 1  # Move past the space

                    else:
                        raise ValueError(f"Lexical Error: Expected ';' at position {i}")

                else:
                    raise ValueError(f"Lexical Error: Unexpected character '{input_string[i]}' at position {i}")


            # Handle 'info' token
            elif input_string[i:i+4] == "info":
                j = i + 4  # Start checking after 'info'

                # If 'info' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'info' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'info' followed by space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'info' is followed by a space
                    tokens.append(("info_token", "info"))  # Append the valid 'info' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 5  # Move past 'info' and the space

                # Handle invalid characters after 'info'
                else:
                    raise ValueError(f"Lexical Error: 'info' must be followed by space or valid identifier at position {i}")

            # Handle 'in' token
            elif input_string[i:i+2] == "in":
                j = i + 2  # Start checking after 'in'

                # If 'in' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'in' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'in' followed by space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'in' is followed by a space
                    tokens.append(("in_token", "in"))  # Append the valid 'in' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 2  # Move past 'in' and the space

                # Handle invalid characters after 'in'
                else:
                    raise ValueError(f"Lexical Error: 'in' must be followed by space at position {i}")


            # Handle 'pos' token
            elif input_string[i:i+3] == "pos":
                j = i + 3  # Start checking after 'pos'

                # If 'pos' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'pos' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # If 'pos' is followed by a valid character (like space or operators), treat it as valid
                elif j < length and input_string[j] in [" "]:
                    tokens.append(("pos_token", "pos"))  # Append 'pos' token
                    tokens.append(("SPACE", " "))  # Tokenize space after 'pos'
                    i += 3  # Move past 'pos'

                else:
                    raise ValueError(f"Lexical Error: Expected space after 'pos' at position {i + 3}")

            # Handle 'neg' token
            elif input_string[i:i+3] == "neg":
                j = i + 3  # Start checking after 'neg'

                # If 'neg' is followed by a space, '=', ')', '!', or '}', treat it as valid
                if j < length and input_string[j] in [" "]:
                    tokens.append(("neg_token", "neg"))  # Append 'neg' token
                    if input_string[j] == " ":
                        tokens.append(("SPACE", " "))  # Tokenize space after 'neg'
                        i += 4  # Move past 'neg' and the space
                    else:
                        i += 3  # Move past 'neg'
                else:
                    raise ValueError(f"Lexical Error: 'neg' must be followed by space at position {i + 3}")

            # Handle 'not' token
            elif input_string[i:i+3] == "not":
                j = i + 3  # Start checking after 'not'

                # If 'not' is followed by a space or '(' (valid cases)
                if j < length and (input_string[j] == " " or input_string[j] == "("):
                    tokens.append(("not_token", "not"))  # Append 'not' token
                    if input_string[j] == " ":
                        tokens.append(("SPACE", " "))  # Tokenize space
                        i += 4  # Move past 'not' and the space
                    elif input_string[j] == "(":
                        tokens.append(("(", "("))  # Tokenize opening parenthesis
                        i += 4  # Move past 'not' and '('
                else:
                    raise ValueError(f"Lexical Error: 'not' must be followed by a space or '(' at position {i + 3}")

            # Handle 'or' token
            elif input_string[i:i+2] == "or":
                j = i + 2  # Start checking after 'or'

                # If 'or' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'or' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # If 'or' is followed by a space, treat it as valid
                elif j < length and input_string[j] == " ":
                    tokens.append(("or_token", "or"))  # Append 'or' token
                    tokens.append(("SPACE", " "))  # Tokenize the space after 'or'
                    i += 3  # Move past 'or' and the space
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'or' at position {i + 2}")
                
            # Handle 'plant' token
            elif input_string[i:i+5] == "plant":
                j = i + 5  # Start checking after 'plant'

                # If 'plant' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'plant' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # If 'plant' is followed by an opening parenthesis, treat it as valid
                elif j < length and input_string[j] == "(":
                    tokens.append(("plant_token", "plant"))  # Append 'plant' token
                    tokens.append(("(", "("))  # Append opening parenthesis token
                    i += 6  # Move past 'plant' and the following '('

                    # Now handle the content inside the parentheses (string literal or identifiers)
                    # Check if there's a string literal
                    if i < length and input_string[i] == '"':
                        i += 1  # Skip the opening quote
                        strike_content = ""  # Store the string literal content

                        while i < length and input_string[i] != '"':  # Read until closing quote
                            if input_string[i] == '\\' and i + 1 < length:  # Handle escaped characters
                                if input_string[i + 1] == 'n':  # Check for escaped newline
                                    strike_content += '\\n'  # Add the escaped newline as part of literal
                                    i += 2  # Skip the escape sequence
                                else:
                                    strike_content += input_string[i]  # Append any other escape sequence
                                    i += 1
                            else:
                                strike_content += input_string[i]  # Append normal character
                                i += 1

                        # Add the last part of the string literal if not empty
                        if strike_content:
                            tokens.append(("string_lit", strike_content))

                        if i < length and input_string[i] == '"':  # Ensure closing quote is found
                            i += 1  # Move past the closing quote
                        else:
                            raise ValueError(f"Lexical Error: Missing closing quote for string literal at position {i}")

                    # Handle identifiers (non-string) inside parentheses
                    elif i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        start = i
                        while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            i += 1
                        tokens.append(("identifier", input_string[start:i]))  # Tokenize identifier
                        tokens.append((")", ")"))  # Tokenize identifier
                        tokens.append((";", ";"))  # Tokenize identifier

                    else:
                        # Handle the case where there's neither string literal nor identifier inside parentheses
                        raise ValueError(f"Lexical Error: Expected a string literal or identifier inside parentheses after 'plant' at position {i}")

                else:
                    # If 'plant' is followed by an invalid character
                    raise ValueError(f"Lexical Error: 'plant' must be followed by an identifier or '(' at position {i}")

            # Handle 'push' token
            elif input_string[i:i+4] == "push":
                j = i + 4  # Start checking after 'push'

                # If 'push' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'push' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # If 'push' is followed by a semicolon, treat it as valid
                elif j < length and input_string[j] == ";":
                    tokens.append(("push_token", "push"))  # Append 'push' token
                    tokens.append((";", ";"))  # Append semicolon token
                    i += 5  # Move past 'push' and the semicolon

                else:
                    raise ValueError(f"Lexical Error: Expected identifier or ';' after 'push' at position {i + 4}")

                    


            # Handle 'perim' token
            elif input_string[i:i+5] == "perim":
                j = i + 5  # Start checking after 'perim'

                # If 'perim' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'perim' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # If 'perim' is followed by '(', treat it as valid
                elif j < length and input_string[j] == "(":
                    tokens.append(("perim_token", "perim"))  # Append 'perim' token
                    tokens.append(("(", "("))  # Append opening parenthesis token
                    i += 6  # Move past 'perim('

                    # Tokenize the content inside the parentheses
                    while i < length and input_string[i] != ")":
                        next_char = input_string[i]

                        # Skip newline characters and continue parsing
                        if next_char == "\n":
                            i += 1  # Move past the newline
                            continue  # Skip to the next character (don't tokenize the newline)

                        # Tokenize numbers (both integers and floats, including negative)
                        if next_char.isdigit() or next_char == "-" or next_char == ".":
                            start = i
                            if input_string[i] == "-":  # If it's a negative number
                                i += 1
                            while i < length and (input_string[i].isdigit() or input_string[i] == "."):
                                i += 1
                            token_value = input_string[start:i]
                            if "." in token_value:  # If it's a float, tokenize as FLANK_LIT
                                tokens.append(("FLANK_LIT", token_value))
                            else:  # Otherwise, it's an integer
                                tokens.append(("INST_LIT", token_value))

                        # Tokenize commas inside the parentheses
                        elif input_string[i] == ",":
                            tokens.append((",", ","))  # Tokenize the comma
                            i += 1  # Move past the comma
                            # Skip spaces after the comma
                            while i < length and input_string[i] == " ":
                                i += 1

                        # Handle string literals (empty or non-empty) inside the parentheses
                        elif input_string[i] == '"':
                            start = i + 1  # Skip the opening quote
                            i += 1
                            strike_content = ""  # Store the string literal content

                            # Read the content until the closing quote or escaped characters
                            while i < length and input_string[i] != '"':
                                if input_string[i] == '\\' and i + 1 < length:  # Handle escaped characters
                                    if input_string[i + 1] == 'n':  # Check for escaped newline
                                        strike_content += '\n'  # Append actual newline
                                        i += 2  # Skip the 'n' in '\n'
                                    else:
                                        strike_content += input_string[i]  # Append any other escape sequence
                                        i += 1
                                else:
                                    strike_content += input_string[i]  # Append normal character
                                    i += 1

                            if i < length and input_string[i] == '"':  # Ensure closing quote is found
                                tokens.append(("strike_lit", strike_content))  # Tokenize the full string literal
                                i += 1  # Move past the closing quote
                            else:
                                raise ValueError(f"Lexical Error: Missing closing quote for string literal at position {i}")

                        else:
                            # Handle invalid character (optional error handling)
                            raise ValueError(f"Lexical Error: Unexpected character '{input_string[i]}' at position {i}")

                    # Finally, handle the closing parenthesis
                    if i < length and input_string[i] == ")":
                        tokens.append((")", ")"))  # Tokenize the closing parenthesis
                        i += 1  # Move past the ')'

                else:
                    raise ValueError(f"Lexical Error: Expected '(' after 'perim' at position {i + 5}")



            # Handle 'reload' token
            elif input_string[i:i+6] == "reload":
                if i + 6 < length:
                    next_char = input_string[i + 6]
                    
                    # Raise error if 'reload' is followed by a space or null character (end of string)
                    if next_char == " " or next_char == "":
                        raise ValueError(f"Lexical Error: Invalid character (space or end of string) after 'reload' at position {i + 6}")
                    
                    # Check if 'reload' is followed by '{'
                    elif next_char == "{":
                        tokens.append(("reload_token", "reload"))  # Append 'reload' token
                        tokens.append(("{", "{"))  # Append '{' as delimiter
                        i += 7  # Move past 'reload{'

                    # Handle case where 'reload' is followed by an identifier (alpha, num, or _)
                    elif next_char.isalnum() or next_char == "_":
                        start = i  # Include 'reload' in the identifier
                        while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            i += 1
                        tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier

                    else:
                        raise ValueError(f"Lexical Error: Invalid character after 'reload' at position {i + 6} (found '{next_char}')")
                else:
                    raise ValueError(f"Lexical Error: Expected character after 'reload' at position {i + 6}")


            # Handle 're' token
            elif input_string[i:i+2] == "re":
                if i + 2 < length:
                    next_char = input_string[i + 2]

                    # Skip whitespace after 're'
                    while next_char == " " and i + 2 < length:
                        i += 1
                        next_char = input_string[i + 2]

                    # Check if 're' is followed by '('
                    if next_char == "(":
                        tokens.append(("re_token", "re"))  # Append 're' token
                        tokens.append(("(", "("))  # Append '(' as delimiter
                        i += 3  # Move past 're('

                        # Parse content inside parentheses
                        start = i
                        while i < length and input_string[i] != ")":
                            # Handle numeric literals first
                            if input_string[i].isdigit():
                                start = i
                                while i < length and input_string[i].isdigit():
                                    i += 1
                                tokens.append(("inst_lit", input_string[start:i]))

                            # Handle identifiers
                            elif input_string[i].isalnum() or input_string[i] == "_":
                                start = i
                                while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                                    i += 1
                                tokens.append(("identifier", input_string[start:i]))

                            # Handle operators and punctuations like '%', '=='
                            elif input_string[i] == "%":
                                tokens.append(("%", "%"))
                                i += 1

                            elif input_string[i:i+2] == "==":
                                tokens.append(("==", "=="))
                                i += 2

                            else:
                                i += 1  # Skip invalid or unrecognized characters inside parentheses

                        if i < length and input_string[i] == ")":
                            tokens.append((")", ")"))  # Append closing ')'
                            i += 1  # Move past ')'

                            # Skip whitespace and check for semicolon
                            while i < length and input_string[i].isspace():
                                i += 1

                            if i < length and input_string[i] == ";":
                                tokens.append((";", ";"))
                                i += 1  # Move past the semicolon
                            else:
                                raise ValueError(f"Lexical Error: Missing semicolon after 're' at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: Missing closing ')' for 're' at position {i}")
            # Handle 'load' token
            elif input_string[i:i+4] == "load":
                j = i + 4  # Start checking after 'load'

                # If 'load' is followed by an alphanumeric character or '_', treat it as part of an identifier
                if j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    start = i  # Include 'load' in the identifier
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    tokens.append(("identifier", input_string[start:j]))  # Tokenize the identifier
                    i = j  # Move past the identifier

                # Handle 'load' followed by space (valid case)
                elif j < length and input_string[j] == " ":  # Check if 'load' is followed by a space
                    tokens.append(("load_token", "load"))  # Append the valid 'load' token
                    tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                    i += 5  # Move past 'load' and the space

                # Handle '{' after 'load'
                elif j < length and input_string[j] == "{":
                    tokens.append(("load_token", "load"))  # Append the valid 'load' token
                    tokens.append(("{", "{"))  # Tokenize '{' as a separate token
                    i += 5  # Move past 'load' and the '{'

                # Handle newline (\n) after 'load'
                elif j < length and input_string[j] == "\n":
                    tokens.append(("load_token", "load"))  # Append the valid 'load' token
                    tokens.append(("\n", "\n"))  # Tokenize newline as a separate token
                    i += 5  # Move past 'load' and the newline

                # Handle invalid characters after 'load'
                else:
                    raise ValueError(f"Lexical Error: 'load' must be followed by space, '{input_string[j]}' at position {i}")

            # Handle numeric literals outside parentheses
            elif input_string[i].isdigit():
                start = i
                while i < length and input_string[i].isdigit():
                    i += 1
                tokens.append(("inst_lit", input_string[start:i]))
            # Handle 'strike' token and '=' assignment
            elif input_string[i:i+6] == "strike":
                tokens.append(("strike_token", "strike"))  # Correctly append the token

                i += 6  # Move past 'strike'
                if i < length and (input_string[i] == " " or input_string[i] == "\n" or input_string[i] == "\t"):
                    # 'strike' followed by space/tab/newline, now expect an identifier
                    i += 1  # Move past the space/tab/newline

                    # Check if the next token is a valid identifier
                    if i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        # Handle identifier after 'strike'
                        start = i
                        while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            i += 1
                        tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier

                        # Check if there's any space between identifier and '='
                        if i < length and (input_string[i] == " " or input_string[i] == "\n" or input_string[i] == "\t"):
                            while i < length and (input_string[i] == " " or input_string[i] == "\n" or input_string[i] == "\t"):
                                i += 1  # Skip the space between identifier and '='

                        # Now check if it's followed by '='
                        if i < length and input_string[i] == "=":
                            tokens.append(("=", "="))  # Tokenize '='
                            i += 1  # Move past '='

                            # Check if there's any space after '='
                            while i < length and (input_string[i] == " " or input_string[i] == "\n" or input_string[i] == "\t"):
                                i += 1  # Skip space after '='

                            # Check if the assignment is followed by a valid value (string literal, number, etc.)
                            if i < length:
                                # Handle string literals with double quotes
                                if input_string[i] == '"':
                                    i += 1  # Move past the opening quote
                                    literal = ""
                                    while i < length and input_string[i] != '"':  # Continue until closing quote is found
                                        literal += input_string[i]
                                        i += 1

                                    if i < length and input_string[i] == '"':  # Ensure closing quote is found
                                        tokens.append(("string_lit", literal))  # Tokenize the string literal
                                        i += 1  # Move past the closing quote

                                        # Tokenize the semicolon after the string literal
                                        if i < length and input_string[i] == ";":
                                            tokens.append((";", ";"))  # Tokenize the semicolon
                                            i += 1  # Move past the semicolon
                                        else:
                                            raise ValueError(f"Lexical Error: Missing semicolon after string literal at position {i}")
                                    else:
                                        raise ValueError(f"Lexical Error: Missing closing double quote at position {i}")
                                # Handle numeric literals (integers or floats)
                                elif input_string[i].isdigit() or (input_string[i] == '.' and i + 1 < length and input_string[i + 1].isdigit()):
                                    start = i
                                    while i < length and (input_string[i].isdigit() or input_string[i] == '.'):
                                        i += 1
                                    tokens.append(("number", input_string[start:i]))  # Tokenize the number

                                    # Tokenize the semicolon after the string literal
                                    if i < length and input_string[i] == ";":
                                        tokens.append((";", ";"))
                                        i += 1  # Move past the semicolon

                                        # Check for newline '\n' after semicolon
                                        if i < length and input_string[i] == "\n":
                                            tokens.append(("newline", "\\n"))
                                            i += 1  # Move past the newline
                                        else:
                                            raise ValueError(f"Lexical Error: Missing newline after semicolon at position {i}")
                                    else:
                                        raise ValueError(f"Lexical Error: Missing semicolon after assignment at position {i}")

                            else:
                                # If there's no value after '=', we can just end the tokenization here without raising an error
                                pass
                        else:
                            raise ValueError(f"Lexical Error: Expected '=' after identifier '{input_string[start:i]}' at position {i}")
                    else:
                        raise ValueError(f"Lexical Error: Missing identifier after 'strike' at position {i}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'strike' at position {i}")
            # Handle case where there is an identifier or any alphanumeric sequence outside parentheses
            elif input_string[i].isalnum() or input_string[i] == "_":
                start = i
                while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                    i += 1
                tokens.append(("identifier", input_string[start:i]))
            # Handle operators and punctuations like '%', '=', etc.
            elif input_string[i] == "%":
                tokens.append(("%", "%"))
                i += 1
            elif input_string[i:i+2] == "==":
                tokens.append(("==", "=="))
                i += 2


            # Handle other tokens (braces, parentheses, etc.)
            elif input_string[i] == "}":
                tokens.append(("}", "}"))
                i += 1  # Move past the '}'

            elif input_string[i] == "{":
                tokens.append(("{", "{"))
                i += 1  # Move past the '{'



            # Handle relational operators like ">=" and "<="
            elif input_string[i:i+2] == ">=":
                tokens.append((">=", ">="))
                i += 2
                # Check if the next character is a valid token (like space or another operator)
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:  # Add valid next characters after relational operator
                        raise ValueError(f"Lexical Error: Invalid character after '>=' at position {i} (found '{next_char}')")

            elif input_string[i:i+2] == "<=":
                tokens.append(("<=", "<="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '<=' at position {i} (found '{next_char}')")
            elif input_string[i:i+2] == "==":
                tokens.append(("==", "=="))
                i += 2  # Move past '=='
                
                if i < length:
                    next_char = input_string[i]

                    # Skip spaces, tabs, or newlines
                    while i < length and (next_char == " " or next_char == "\n" or next_char == "\t"):
                        i += 1
                        next_char = input_string[i] if i < length else None

                    # After skipping white space, check if next character is a number (INST_LIT)
                    if next_char is not None:
                        if next_char.isdigit() or (next_char == '.' and i + 1 < length and input_string[i + 1].isdigit()):
                            # Handle numeric literals as INST_LIT (e.g., 5 or 5.0)
                            start = i
                            while i < length and (input_string[i].isdigit() or input_string[i] == '.'):
                                i += 1
                            tokens.append(("INST_LIT", input_string[start:i]))  # Tokenize the number as INST_LIT
                            tokens.append((";", ";"))  # Tokenize the number as INST_LIT
                        elif next_char.isalnum() or next_char == "_":
                            # Handle identifiers, if needed
                            start = i
                            while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                                i += 1
                            tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier
                        else:
                            raise ValueError(f"Lexical Error: Invalid character after '==' at position {i} (found '{next_char}')")

            # After '=': Handling spaces, numbers (positive/negative integers and floats), and string literals
            elif input_string[i:i+1] == "=":  # Check for '='
                tokens.append(("=", "="))  # Tokenize '='
                i += 1  # Move to the next character after '='

                if i < length:
                    next_char = input_string[i]

                    # Skip spaces and handle them as part of tokenization
                    if next_char == " ":
                        tokens.append(("SPACE", " "))  # Tokenize the space
                        i += 1  # Move past the space
                        if i < length:
                            next_char = input_string[i]

                    # Handle string literals enclosed in double quotes
                    elif next_char == '"':
                        i += 1  # Skip the opening quote
                        literal = ""
                        while i < length and input_string[i] != '"':  # Continue until closing quote is found
                            if input_string[i] == '\\' and i + 1 < length:  # Check for escape sequences
                                # Handle escape sequences like \n, \t, \" etc.
                                if input_string[i + 1] == 'n':
                                    literal += "\\n"  # Add newline as part of literal
                                    i += 2  # Skip the escape sequence (\n)
                                elif input_string[i + 1] == 't':
                                    literal += "\\t"  # Represent tab as part of literal
                                    i += 2  # Skip the escape sequence (\t)
                                elif input_string[i + 1] == '"':
                                    literal += '\\"'  # Represent escaped quote as part of literal
                                    i += 2  # Skip the escape sequence (\")
                                else:
                                    literal += input_string[i]  # Add the backslash as part of literal
                                    i += 1  # Skip the backslash
                            else:
                                literal += input_string[i]  # Add regular character to the literal content
                                i += 1

                        # After the loop, check for closing quote
                        if i < length and input_string[i] == '"':  # Ensure closing quote is found
                            tokens.append(("string_lit", literal))  # Tokenize the string literal
                            i += 1  # Move past the closing quote
                        else:
                            raise ValueError(f"Lexical Error: Missing closing double quote at position {i}")

                    # Handle numbers (integers or floats)
                    elif next_char.isdigit() or next_char == "-" or next_char == ".":
                        start = i
                        if input_string[i] == "-":  # Check for negative numbers
                            i += 1
                        while i < length and (input_string[i].isdigit() or input_string[i] == "."):
                            i += 1
                        token_value = input_string[start:i]
                        if "." in token_value:  # If it's a float, tokenize as FLANK_LIT
                            tokens.append(("FLANK_LIT", token_value))
                        else:  # Otherwise, it's an integer
                            tokens.append(("INST_LIT", token_value))

                    # Handle optional '[' and ']' (if valid syntax)
                    elif next_char == "[":
                        tokens.append(("[", "["))  # Tokenize the '['
                        i += 1  # Move past the '['
                    
                    elif next_char == "]":
                        tokens.append(("]", "]"))  # Tokenize the ']'
                        i += 1  # Move past the ']'

                    # Handle semicolon ';' (end of statement)
                    elif next_char == ";":
                        tokens.append((";", ";"))  # Tokenize the semicolon
                        i += 1  # Move past the semicolon
                    else:
                        raise ValueError(f"Lexical Error: Expected number, float, string literal, '[', ']', or ';' after '=' at position {i}")



            # Handle commas inside the list after '['
            elif input_string[i:i+1] == ",":
                tokens.append((",", ","))  # Tokenize the comma
                i += 1  # Move past the comma

            # Handle closing bracket ']'
            elif input_string[i:i+1] == "]":
                tokens.append(("]", "]"))  # Tokenize the closing bracket
                i += 1  # Move past the closing bracket


            # Handle square brackets "[" and "]"
            elif input_string[i] == "[":
                tokens.append(("[", "[")) 
                i += 1  # Move past the '['
            elif input_string[i] == "]":
                tokens.append(("]", "]"))
                i += 1  # Move past the ']'

            # Handle parentheses "(" and ")"
            elif input_string[i] == "(":
                tokens.append(("(", "("))  # Tokenize the opening parenthesis
                i += 1  # Move past the '('

                if i < length:
                    next_char = input_string[i]

                    # Loop to handle multiple numbers or literals inside parentheses
                    while i < length and (next_char.isdigit() or next_char == '.' or next_char == '-'):
                        start = i

                        if input_string[i] == '-':  # If it's a negative number, include the '-' sign
                            i += 1
                            next_char = input_string[i] if i < length else None  # Update next_char after '-'

                        # Now handle digits and decimal points
                        while i < length and (input_string[i].isdigit() or input_string[i] == '.'):
                            i += 1

                        # Tokenize the number as INST_LIT or FLANK_LIT
                        token_value = input_string[start:i]
                        if '.' in token_value:  # If it's a float, tokenize as FLANK_LIT
                            tokens.append(("FLANK_LIT", token_value))
                        else:  # Otherwise, it's an integer
                            tokens.append(("INST_LIT", token_value))

                        # After parsing the number, check for more tokens (like commas or closing parenthesis)
                        if i < length and input_string[i] == ",":
                            tokens.append((",", ","))  # Tokenize the comma
                            i += 1  # Move past the comma

                            # Skip any spaces after the comma to move to the next number
                            while i < length and input_string[i] == " ":
                                i += 1

                        # Update next_char after handling a number or a comma
                        if i < length:
                            next_char = input_string[i]

                    # Handle identifiers after numbers and commas (if needed)
                    while i < length and (next_char.isalnum() or next_char == "_"):
                        start = i
                        while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            i += 1
                        tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier

                # Tokenize the closing parenthesis if present
                if i < length and input_string[i] == ")":
                    tokens.append((")", ")"))  # Tokenize the closing parenthesis
                    i += 1  # Move past the ')'

            # Handle semicolons (end of statement) and whitespace including \n
            elif input_string[i] == ";":
                tokens.append((";", ";"))  # Tokenize the semicolon
                i += 1  # Move past the semicolon

            # Handle spaces or newlines as token separators
            elif input_string[i] == " " or input_string[i] == "\n":
                tokens.append(("SPACE", " "))  # Tokenize space
                i += 1  # Move past the space or newline



            # Handle negative numbers and floats (e.g., "-2" or "-2.2")
            elif input_string[i] == "-" and i + 1 < length and (input_string[i + 1].isdigit() or input_string[i + 1] == "."):
                start = i  # Start of negative number or float
                i += 1  # Skip the minus sign

                # Handle integer part of negative number or float
                while i < length and input_string[i].isdigit():
                    i += 1

                # Handle decimal part if present (for floats)
                if i < length and input_string[i] == ".":
                    i += 1  # Skip the decimal point
                    decimal_count = 0  # Counter for digits after decimal point
                    while i < length and input_string[i].isdigit():
                        decimal_count += 1
                        if decimal_count > 5:  # If there are more than 5 digits after the decimal point
                            raise ValueError(f"Lexical Error: Decimal part exceeds 5 digits at position {i}")
                        i += 1

                # Only add token if the index `i` has advanced
                if i > start:
                    if '.' in input_string[start:i]:  # Check if it's a float
                        tokens.append(("FLANK_LIT", input_string[start:i]))  # Add negative float token
                    else:  # It's an integer
                        tokens.append(("INST_LIT", input_string[start:i]))  # Add negative integer token
                continue  # Skip further checks for this number


            # Handle positive numbers and floats (e.g., "2" or "2.2")
            elif char.isdigit():
                start = i  # Start of number (could be integer or float)

                # Process integer part
                while i < length and input_string[i].isdigit():
                    i += 1

                # Handle decimal part if present (for floats)
                if i < length and input_string[i] == ".":
                    i += 1  # Skip the decimal point
                    decimal_count = 0  # Counter for digits after decimal point
                    while i < length and input_string[i].isdigit():
                        decimal_count += 1
                        if decimal_count > 5:  # If there are more than 5 digits after the decimal point
                            raise ValueError(f"Lexical Error: Decimal part exceeds 5 digits at position {i}")
                        i += 1

                # Only add token if the index `i` has advanced (i.e., a valid number was found)
                if i > start:
                    number_str = input_string[start:i]  # Extract the number substring
                    if '.' in number_str:  # Check if it's a float
                        tokens.append(("FLANK_LIT", number_str))  # Add positive float token
                    else:  # It's an integer
                        tokens.append(("INST_LIT", number_str))  # Add positive integer token
                continue  # Skip further checks for this number



            elif input_string[i:i+2] == "!=":
                tokens.append(("!=", "!="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '!=' at position {i} (found '{next_char}')")

            # Handle other operators like "**", "*=", "/=", etc.
            elif input_string[i:i+2] == "**":
                tokens.append(("**", "**"))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '**' at position {i} (found '{next_char}')")

            elif input_string[i:i+2] == "*=":
                tokens.append(("*=", "*="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '*=' at position {i} (found '{next_char}')")

            elif input_string[i:i+2] == "/=":
                tokens.append(("/=", "/="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '/=' at position {i} (found '{next_char}')")

            elif input_string[i:i+2] == "%=":
                tokens.append(("%=", "%="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '%=' at position {i} (found '{next_char}')")


            elif input_string[i:i+2] == "+=":
                tokens.append(("+=", "+="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '+=' at position {i} (found '{next_char}')")

            elif input_string[i:i+2] == "-=":
                tokens.append(("-=", "-="))
                i += 2
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '-=' at position {i} (found '{next_char}')")

            # Handle arithmetic operators like "+", "-", "*"
            elif input_string[i] == "+":
                tokens.append(("+", "+"))
                i += 1
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '+' at position {i} (found '{next_char}')")

            # Handling '-' for subtraction or negative numbers (with spaces between operators)
            elif input_string[i] == "-":
                tokens.append(("-", "-"))  # Tokenize the first '-' (could be subtraction or negative sign)
                i += 1  # Move past the '-'

                # Check if the next character is a space (indicating a space before a negative number)
                if i < length:
                    next_char = input_string[i]

                    # Case 1: If it's a space, move past it
                    if next_char == " ":
                        tokens.append(("SPACE", " "))  # Tokenize the space
                        i += 1  # Move past the space

                        # After the space, check for the second '-' (negative number)
                        if i < length and input_string[i] == "-":
                            i += 1  # Move past the second '-'

                            # Now look ahead to check if it's a valid number (e.g., -5.5)
                            if i < length and (input_string[i].isdigit() or input_string[i] == "."):
                                start = i  # Start of negative number

                                # Handle the number (positive or negative)
                                while i < length and (input_string[i].isdigit() or input_string[i] == "."):
                                    i += 1

                                # Handle decimal part if present (for floats)
                                if '.' in input_string[start:i]:  # If it's a float, add a specific token
                                    tokens.append(("FLANK_LIT", "-" + input_string[start:i]))  # Token for negative float
                                else:  # It's an integer
                                    tokens.append(("INST_LIT", "-" + input_string[start:i]))  # Token for negative integer

                            else:
                                raise ValueError(f"Lexical Error: Expected number after '-' at position {i}")

                        else:
                            raise ValueError(f"Lexical Error: Expected '-' after space at position {i}")

                    # Case 2: If it's a digit or a decimal, it's a subtraction operation (e.g., '5.1 - 5.5')
                    elif next_char.isdigit() or next_char == ".":
                        continue  # Move on to handle this later (subtraction or negative float)

                    else:
                        raise ValueError(f"Lexical Error: Invalid character after '-' at position {i} (found '{next_char}')")

                continue  # Skip further checks for this character


            elif input_string[i] == "*":
                tokens.append(("*", "*"))
                i += 1
                if i < length:
                    next_char = input_string[i]
                    if next_char not in [" ", "{", "}", "(", ")", ";"]:
                        raise ValueError(f"Lexical Error: Invalid character after '*' at position {i} (found '{next_char}')")

            # Handle modulus operator "%", division "/", and floor division "//"
            elif input_string[i] == "%":
                if i + 1 < length and input_string[i + 1] == "%":
                    raise ValueError(f"Lexical Error: Invalid '%%' sequence at position {i}")
                else:
                    tokens.append(("modulus", "%"))
                    i += 1
            elif input_string[i:i+2] == "//":
                tokens.append(("//", "//"))
                i += 2

            elif input_string[i] == "/":
                tokens.append(("/", "/"))
                i += 1



            # Handle single quotes for character literals (enclosed in single quotes)
            elif char == "'":
                start = i + 1
                i += 1
                while i < length and input_string[i] != "'":
                    i += 1
                if i < length:
                    char_literal_content = input_string[start:i]
                    if len(char_literal_content) == 1 and char_literal_content.isalnum():
                        tokens.append(("char_literal", char_literal_content))
                    else:
                        raise ValueError(f"Lexical Error: Invalid character literal '{char_literal_content}' at position {start}")
                    i += 1
                else:
                    raise ValueError(f"Lexical Error: Missing closing single quote at position {start}")

            # Handle comments with "^^^"
            elif input_string[i:i+3] == "^^^":  # Check for the start of a comment with "^^^"
                start = i
                i += 3  # Move past the initial "^^^"
                while i < length and input_string[i:i+3] != "^^^":  # Look for the closing "^^^"
                    i += 1
                if i < length and input_string[i:i+3] == "^^^":  # Check if the comment is closed with "^^^"
                    tokens.append(("multi_line_comment", input_string[start:i+3]))  # Append the comment token
                    i += 3  # Move past the closing "^^^"
                else:
                    raise ValueError(f"Lexical Error: Missing closing multi-line comment at position {start}")
                
            # Handle comments
            elif input_string[i:i+2] == "^^":  # Check for the start of a comment with "^^"
                start = i
                i += 2  # Move past the initial "^^"
                while i < length and input_string[i:i+2] != "^^":  # Look for the closing "^^"
                    i += 1
                if i < length and input_string[i:i+2] == "^^":  # Check if the comment is closed with "^^"
                    tokens.append(("single_line_comment", input_string[start:i+2]))  # Append the comment token
                    i += 2  # Move past the closing "^^"
                else:
                    raise ValueError(f"Lexical Error: Missing closing multi-line comment at position {start}")





