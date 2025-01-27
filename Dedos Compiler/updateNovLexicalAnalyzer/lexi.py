class DEDOSLexicalAnalyzer:
    def __init__(self):
        # Reserved words to identify in the input
        self.reserved_words = ['abort', 'and']  
        # Dictionary for literals (e.g., numbers, strings)
        self.literals = {}  
        # Delimiters to track in the input (e.g., ;, :, etc.)
        self.delimiters = {
            ";": "SEMICOLON",
            ":": "COLON"
        }

    def tokenize(self, input_string):
        """Tokenizes the input string based on predefined rules using delimiters."""
        tokens = []
        i = 0
        length = len(input_string)

        # Initialize the block_stack to track open blocks
        block_stack = []  # Ensure block_stack is defined at the start

        while i < length:
            char = input_string[i]

            # Skip whitespace (space, tab, newline)
            if char in " \t\n":
                i += 1  # Increment i to move past the whitespace
                continue  # Skip this iteration to check the next character


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

            # Handle 'and' keyword
            elif i + 3 <= length and input_string[i:i+3] == "and":
                if i + 3 < length and input_string[i+3].islower():  # Ensure the next character is lowercase
                    j = i + 3
                    while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                        j += 1
                    identifier = input_string[i+3:j]

                    for idx, c in enumerate(identifier):
                        if c.isupper():
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'and' at position {i + 3 + idx}")

                    tokens.append(("identifier", identifier))  # Tokenize the identifier
                    i = j  # Move past the identifier
                else:
                    tokens.append(("and_token", "and"))
                    i += 3  # Move past 'and'

                    # Check for space or opening parenthesis
                    if i < length and input_string[i] == " ":
                        tokens.append(("SPACE", " "))
                        i += 1
                    elif i < length and input_string[i] == "(":
                        tokens.append(("(", "("))
                        i += 1
                    else:
                        raise ValueError(f"Lexical Error: 'and' must be followed by space or '(' at position {i}")

            # Handle 'abort' keyword
            elif i + 5 <= length and input_string[i:i+5] == "abort":
                if i + 5 < length and input_string[i+5].islower():  # Ensure the next character is lowercase
                    j = i + 5
                    while j < length and input_string[j].islower():
                        j += 1
                    identifier = input_string[i+5:j]

                    for idx, c in enumerate(identifier):
                        if c.isupper():
                            raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'abort' at position {i + 5 + idx}")

                    tokens.append(("identifier", identifier))  # Tokenize the identifier
                    i = j  # Move past the identifier
                else:
                    tokens.append(("abort_token", "abort"))
                    i += 5  # Move past 'abort'

                    if i < length and input_string[i] == ";":
                        tokens.append((";", ";"))
                        i += 1  # Move past the semicolon

                    # Check if there's another character after semicolon
                    if i < length and input_string[i] != " ":
                        raise ValueError(f"Lexical Error: Expected space after semicolon at position {i}")
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


            # Handle 'flank' token with space validation
            elif input_string[i:i+5] == "flank":
                tokens.append(("flank_token", "flank"))  # Append 'flank' token
                i += 5  # Move past 'flank'

                # Check if there is a space after 'flank'
                if i < length and input_string[i] != " ":
                    raise ValueError(f"Lexical Error: 'flank' must be followed by a space at position {i}")

                # Skip any leading spaces after 'flank'
                while i < length and input_string[i] == " ":
                    tokens.append(("SPACE", " "))  # Tokenize the space
                    i += 1  # Move past the space

                # Now expect an identifier after the space
                if i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                    start = i
                    while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        i += 1
                    tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier
                else:
                    raise ValueError(f"Lexical Error: Expected identifier after 'flank' at position {i}")

                # Check for space after identifier
                if i < length and input_string[i] != " ":
                    raise ValueError(f"Lexical Error: Identifier must be followed by a space at position {i}")

                # Skip spaces after the identifier
                while i < length and input_string[i] == " ":
                    tokens.append(("SPACE", " "))  # Tokenize the space
                    i += 1  # Move past the space

                # Check for '=' after the identifier
                if i < length and input_string[i] == "=":
                    tokens.append(("=", "="))  # Tokenize '='
                    i += 1

                    # Ensure there's a space after '='
                    if i < length and input_string[i] != " ":
                        raise ValueError(f"Lexical Error: '=' must be followed by a space at position {i}")

                    # Skip spaces after '='
                    while i < length and input_string[i] == " ":
                        tokens.append(("SPACE", " "))  # Tokenize the space
                        i += 1  # Move past the space

                    # Handle INST_LIT (number or literal) after '='
                    if i < length and (input_string[i].isdigit() or input_string[i] == "-" or input_string[i] == "."):
                        start = i
                        # Handle negative numbers
                        if input_string[i] == "-":
                            i += 1
                        while i < length and (input_string[i].isdigit() or input_string[i] == "." or input_string[i] == "-"):
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
                        tokens.append(("SPACE", " "))  # Tokenize the space after the literal
                        i += 1  # Move past the space

                    # Expect semicolon ';' at the end of the statement
                    if i < length and input_string[i] == ";":
                        tokens.append((";", ";"))  # Tokenize the semicolon
                        i += 1  # Move past the semicolon

                        if i < length and input_string[i] == " ":
                            tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                            i += 1  # Move past the space
                    else:
                        raise ValueError(f"Lexical Error: Expected ';' at position {i}")

                else:
                    raise ValueError(f"Lexical Error: Expected '=' after identifier at position {i}")


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
                        # Handle 'inst' followed by space (valid case)
            elif input_string[i:i+4] == "inst":
                tokens.append(("inst_token", "inst"))  # Append 'inst' token
                i += 4  # Move past 'inst'

                # Check if there is a space after 'inst'
                if i < length and input_string[i] != " ":
                    raise ValueError(f"Lexical Error: 'inst' must be followed by a space at position {i}")

                # Skip any leading spaces after 'inst'
                while i < length and input_string[i] == " ":
                    tokens.append(("SPACE", " "))  # Tokenize the space
                    i += 1  # Move past the space

                # Now expect an identifier after the space
                if i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                    start = i
                    while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        i += 1
                    tokens.append(("identifier", input_string[start:i]))  # Tokenize the identifier
                else:
                    raise ValueError(f"Lexical Error: Expected identifier after 'inst' at position {i}")

                # Check for space after identifier
                if i < length and input_string[i] != " ":
                    raise ValueError(f"Lexical Error: Identifier must be followed by a space at position {i}")

                # Skip spaces after the identifier
                while i < length and input_string[i] == " ":
                    tokens.append(("SPACE", " "))  # Tokenize the space
                    i += 1  # Move past the space

                # Check for '=' after the identifier
                if i < length and input_string[i] == "=":
                    tokens.append(("=", "="))  # Tokenize '='
                    i += 1

                    # Ensure there's a space after '='
                    if i < length and input_string[i] != " ":
                        raise ValueError(f"Lexical Error: '=' must be followed by a space at position {i}")

                    # Skip spaces after '='
                    while i < length and input_string[i] == " ":
                        tokens.append(("SPACE", " "))  # Tokenize the space
                        i += 1  # Move past the space

                    # Handle INST_LIT (number or literal) after '='
                    if i < length and (input_string[i].isdigit() or input_string[i] == "-" or input_string[i] == "."):
                        start = i
                        # Handle negative numbers
                        if input_string[i] == "-":
                            i += 1
                        while i < length and (input_string[i].isdigit() or input_string[i] == "." or input_string[i] == "-"):
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
                        tokens.append(("SPACE", " "))  # Tokenize the space after the literal
                        i += 1  # Move past the space

                    # Expect semicolon ';' at the end of the statement
                    if i < length and input_string[i] == ";":
                        tokens.append((";", ";"))  # Tokenize the semicolon
                        i += 1  # Move past the semicolon

                        if i < length and input_string[i] == " ":
                            tokens.append(("SPACE", " "))  # Tokenize the space as a separate token
                            i += 1  # Move past the space
                    else:
                        raise ValueError(f"Lexical Error: Expected ';' at position {i}")

                else:
                    raise ValueError(f"Lexical Error: Expected '=' after identifier at position {i}")


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
                elif j < length and input_string[j] in [";"]:
                    tokens.append(("pos_token", "pos"))  # Append 'pos' token
                    tokens.append((";", ";"))  # Tokenize space after 'pos'
                    i += 3  # Move past 'pos'

                else:
                    raise ValueError(f"Lexical Error: Expected space after 'pos' at position {i + 3}")

            # Handle 'neg' token
            elif input_string[i:i+3] == "neg":
                j = i + 3  # Start checking after 'neg'

                # If 'neg' is followed by a space, '=', ')', '!', or '}', treat it as valid
                if j < length and input_string[j] in [";"]:
                    tokens.append(("neg_token", "neg"))  # Append 'neg' token
                    if input_string[j] == ";":
                        tokens.append((";", ";"))  # Tokenize space after 'neg'
                        i += 4  # Move past 'neg' and the space
                    else:
                        i += 3  # Move past 'neg'
                else:
                    raise ValueError(f"Lexical Error: 'neg' must be followed by ';' at position {i + 3}")

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

                    # Now handle the content inside the parentheses (string literal or identifiers or concatenation)
                    while i < length and input_string[i] != ")":
                        # Skip any leading spaces inside parentheses
                        if input_string[i] == " ":
                            tokens.append(("SPACE", " "))  # Tokenize the space
                            i += 1  # Move past the space
                            continue

                        # Check if it's a string literal
                        if input_string[i] == '"':
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
                                tokens.append(("STRIKE_LIT", strike_content))

                            if i < length and input_string[i] == '"':  # Ensure closing quote is found
                                i += 1  # Move past the closing quote
                            else:
                                raise ValueError(f"Lexical Error: Missing closing quote for string literal at position {i}")

                        # Check for concatenation operator '+'
                        elif input_string[i] == "+":
                            tokens.append(("+", "+"))  # Tokenize the '+' operator
                            i += 1

                        # Handle identifiers (non-string) inside parentheses
                        elif input_string[i].isalnum() or input_string[i] == "_":
                            start = i
                            while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                                i += 1
                            tokens.append(("identifier", input_string[start:i]))  # Tokenize identifier

                        else:
                            # Handle the case where there's neither string literal nor identifier inside parentheses
                            raise ValueError(f"Lexical Error: Unexpected character '{input_string[i]}' inside parentheses at position {i}")

                        # Skip any spaces between elements
                        while i < length and input_string[i] == " ":
                            tokens.append(("SPACE", " "))  # Tokenize the space
                            i += 1  # Move past the space

                    # Now check for the closing parenthesis ')'
                    if i < length and input_string[i] == ")":
                        tokens.append((")", ")"))  # Tokenize closing parenthesis
                        i += 1  # Move past the closing parenthesis
                    else:
                        raise ValueError(f"Lexical Error: Expected closing parenthesis ')' after content inside parentheses at position {i}")

                    # Check for the semicolon ';' after the closing parenthesis
                    if i < length and input_string[i] == ";":
                        tokens.append((";", ";"))  # Tokenize semicolon
                        i += 1  # Move past the semicolon
                    else:
                        raise ValueError(f"Lexical Error: Expected semicolon ';' after closing parenthesis at position {i}")

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
                            elif input_string[i] == "<":
                                tokens.append(("<", "<"))
                                i += 1
                            elif input_string[i] == ">":
                                tokens.append((">", ">"))
                                i += 1
                            elif input_string[i] == "!=":
                                tokens.append(("!=", "!="))
                                i += 1                                

                            elif input_string[i:i+2] == "==":
                                tokens.append(("==", "=="))
                                i += 2

                            elif input_string[i:i+2] == "!=":
                                tokens.append(("!=", "!="))
                                i += 2
                            elif input_string[i:i+2] == "*=":
                                tokens.append(("*=", "*="))
                                i += 2
                            elif input_string[i:i+2] == "/=":
                                tokens.append(("/=", "/="))
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
                        start = i
                        while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            i += 1
                        identifier = input_string[start:i]  # Extract the identifier

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

                            # After '=' check for string literal (must be a string literal)
                            if i < length and input_string[i] == '"':
                                i += 1  # Move past the opening quote
                                literal = ""
                                while i < length and input_string[i] != '"':  # Continue until closing quote is found
                                    literal += input_string[i]
                                    i += 1

                                if i < length and input_string[i] == '"':  # Ensure closing quote is found
                                    tokens.append(("STRIKE_LIT", literal))  # Tokenize the string literal as 'STRIKE_LIT'
                                    i += 1  # Move past the closing quote

                                    # Tokenize the semicolon after the string literal
                                    if i < length and input_string[i] == ";":
                                        tokens.append((";", ";"))  # Tokenize the semicolon
                                        i += 1  # Move past the semicolon
                                    else:
                                        raise ValueError(f"Lexical Error: Missing semicolon after string literal at position {i}")
                                else:
                                    raise ValueError(f"Lexical Error: Missing closing double quote at position {i}")
                            else:
                                raise ValueError(f"Lexical Error: Expected string literal after '=' at position {i}")
                        else:
                            raise ValueError(f"Lexical Error: Expected '=' after identifier '{identifier}' at position {i}")
                    else:
                        raise ValueError(f"Lexical Error: Missing identifier after 'strike' at position {i}")
                else:
                    raise ValueError(f"Lexical Error: Expected space after 'strike' at position {i}")

            # Handle 'watch' token
            elif input_string[i:i+5] == "watch":
                tokens.append(("watch_token", "watch"))
                i += 5  # Move past 'watch'

                # After 'watch', expect a space
                if i < length and input_string[i] == " ":
                    i += 1  # Move past space

                # After space, expect '('
                if i < length and input_string[i] == "(":
                    tokens.append(("(", "("))
                    i += 1  # Move past '('

                    # Now handle the logical expression inside the parentheses
                    while i < length and input_string[i] != ")":
                        # Expect numeric literal (e.g., '22')
                        if i < length and input_string[i].isdigit():
                            start = i
                            while i < length and (input_string[i].isdigit() or input_string[i] == '.'):
                                i += 1
                            tokens.append(("INST_LIT", input_string[start:i]))  # Tokenize as number

                        # Expect identifier (e.g., 'x')
                        elif i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                            start = i
                            while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                                i += 1
                            tokens.append(("identifier", input_string[start:i]))  # Tokenize as identifier

                        # Handle 'instlit' (instlit can be a keyword or token type you define)
                        elif i < length and input_string[i:i+7] == "INST_LIT":
                            tokens.append(("INST_LIT", "INST_LIT"))  # Tokenize as instlit
                            i += 7  # Move past 'instlit'

                        # Handle 'or' operator
                        elif i < length and input_string[i:i+2] == "or":
                            tokens.append(("or", "or"))
                            i += 2  # Move past 'or'

                        # Handle '>' operator
                        elif i < length and input_string[i] == ">":
                            tokens.append((">", ">"))
                            i += 1  # Move past '>'

                        # Skip any spaces or newlines
                        elif i < length and (input_string[i] == " " or input_string[i] == "\n" or input_string[i] == "\t"):
                            i += 1

                        else:
                            raise ValueError(f"Lexical Error: Unexpected token at position {i}")

                    # After the condition inside parentheses, expect ')'
                    if i < length and input_string[i] == ")":
                        tokens.append((")", ")"))
                        i += 1  # Move past ')'

                    # After ')', expect '{'
                    if i < length and input_string[i] == "{":
                        tokens.append(("{", "{"))
                        i += 1  # Move past '{'

                        # Now we expect the block content inside the curly braces
                        # You can add your block handling logic here if needed
                    else:
                        raise ValueError(f"Lexical Error: Expected '{{' after ')' at position {i}")



            # Handle 'tool' token
            elif input_string[i:i+4] == "tool":
                tokens.append(("tool_keyword", "tool"))
                i += 4  # Move past 'tool'

                # After 'tool', expect a space
                if i < length and input_string[i] == " ":
                    i += 1  # Move past space

                # After space, expect identifier (e.g., 'andromeda' or 'milkeymouse')
                if i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                    start = i
                    while i < length and (input_string[i].isalnum() or input_string[i] == "_"):
                        i += 1
                    tokens.append(("identifier", input_string[start:i]))  # Tokenize as identifier

                # After identifier, expect a space
                if i < length and input_string[i] == " ":
                    i += 1  # Move past space

                # After space, expect '='
                if i < length and input_string[i] == "=":
                    tokens.append(("=", "="))
                    i += 1  # Move past '='

                # After '=', expect a space
                if i < length and input_string[i] == " ":
                    i += 1  # Move past space

                # After space, expect valid value ('neg' or 'pos')
                if i < length and input_string[i:i+3] == "neg":
                    tokens.append(("neg", "neg"))
                    i += 3  # Move past 'neg'
                elif i < length and input_string[i:i+3] == "pos":
                    tokens.append(("pos", "pos"))
                    i += 3  # Move past 'pos'
                else:
                    raise ValueError(f"Lexical Error: Expected 'neg' or 'pos' after '=' at position {i}")

                # After 'neg' or 'pos', expect a semicolon
                if i < length and input_string[i] == ";":
                    tokens.append((";", ";"))
                    i += 1  # Move past ';'










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
                            tokens.append(("STRIKE_LIT", literal))  # Tokenize the string literal
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






            # Handle general letters (identifier or other tokens)
            elif char.isalpha():  # If the character is a letter, start an identifier or keyword
                j = i
                while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
                    j += 1
                identifier = input_string[i:j]
                tokens.append(("identifier", identifier))  # Tokenize the identifier
                i = j  # Move past the identifier

            # Handle other characters if no match found
            else:
                raise ValueError(f"Lexical Error: Unexpected character '{char}' at position {i}")
        # After the loop, check if there are any unclosed blocks
        if block_stack:
            raise ValueError(f"Lexical Error: Block opened with '~{{' but not closed properly.")

        return tokens

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


    def process_identifier(input_string, i, length):
        # Start of the identifier after 'and'
        j = i + 3
        while j < length and (input_string[j].isalnum() or input_string[j] == "_"):
            j += 1
        identifier = input_string[i+3:j]

        # Check for uppercase letters in the identifier
        for idx, c in enumerate(identifier):
            if c.isupper():
                raise ValueError(f"Lexical Error: Identifier '{identifier}' contains uppercase letter '{c}' after 'and' at position {i + 3 + idx}")


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
