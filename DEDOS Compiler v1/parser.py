import ply.lex as lex

# Token definitions
tokens = (
    'OPENBLOCK',         # ~{
    'CLOSEBLOCK',         # }~
    'RBRACE',
    'LBRACE',
    'SEMICOLON',      # ;
    'EQUALS',         # =
    'LPAREN',         # (
    'RPAREN',         # )
    'NUMBER',         # Numeric values
    'STRING',         # String values
    'IDENTIFIER',     # Variable names and identifiers
    'HASH_IDENTIFIER',# Handle # identifier (e.g., #x)
    'DATA_TYPE',      # e.g., inst, flank, strike, tool, chat
    'SPACE',          # Space token
    'NEWLINE',        # Newline token
    'OPERATOR',       # +, -, *, /, %
    'REL_OP',         # Relational operators: <, >, <=, >=, ==, !=
    'COMMENT',        # Comment tokens
    'SEPARATOR',      # Commas or other separators
    'SPECIAL',        # Special symbols like brackets or braces (if not captured already)
    'IF',             # if (mapped from "re")
    'ELSE',           # else (mapped from "load")
    'ELSEIF'          # elseif (mapped from "reload")
)

# Regular expressions for tokens
t_OPENBLOCK    = r'~\{'      # Match opening brace ~{
t_CLOSEBLOCK   = r'\}~'      # Match closing brace }~
t_RBRACE    = r'\{'
t_LBRACE    = r'\}'
t_SEMICOLON = r';'
t_EQUALS    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

# Handle identifier with hash symbol
def t_HASH_IDENTIFIER(t):
    r'\#([a-zA-Z_][a-zA-Z_0-9]*)'
    t.type = 'IDENTIFIER'  # Treat #x as an identifier
    t.value = t.value[1:]  # Remove the '#' character
    return t

# Handle spaces (we ignore these by not returning them)
def t_SPACE(t):
    r'[ \t]+'
    pass

# Reserved words mapping
reserved = {
    're': 'IF',
    'load': 'ELSE',
    'reload': 'ELSEIF',
    'inst': 'DATA_TYPE',
    'flank': 'DATA_TYPE',
    'chat': 'DATA_TYPE',
    'strike': 'DATA_TYPE',  # Correctly map 'strike' to 'DATA_TYPE'
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check if it's a reserved word
    return t

def t_NUMBER(t):
    r'\d+'  # Numeric values
    t.value = int(t.value)
    return t

# Comment handling
def t_COMMENT(t):
    r'[`].*?[\$]'
    pass  # Ignore comments

# Handle newline
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()



class DEDOSParser:
    def __init__(self, tokens):
        self.tokens = tokens  # Token list from the lexer
        self.index = 0        # Current position in the tokens list
        self.current_token = None
        self.errors_list = []      # To store syntax errors
        self.advance()        # Load the first token

    def advance(self):
        """Advance to the next token, skipping SPACE and NEWLINE tokens."""
        while self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            if self.current_token in ["SPACE", "NEWLINE"]:
                self.index += 1
            else:
                self.index += 1
                break
        else:
            self.current_token = None  # End of tokens

    def parse(self):
        """Start parsing the program."""
        self.advance()  # Load the first token

        # Parse the program start token: ~{
        if self.current_token == "LBRACE":
            print("Found program start token: ~{")
            self.advance()  # Skip "~{"
            self.parse_program_content()
            if self.current_token == "RBRACE":
                print("Parsing successful!")
                return
            else:
                print("Syntax Error: Missing program end token (}~)")
        else:
            print("Syntax Error: Invalid program structure")

    def parse_program_content(self):
        """Parse the content within the program."""
        print(f"Parsing program content. Current token: {self.current_token}")
        if self.current_token == "DATA_TYPE":
            print("Found 'inst' token")
            self.parse_var_dec()
        elif self.current_token == "IDENTIFIER":
            print("Found identifier")
            self.parse_function_call()
        else:
            print("Syntax Error: Expected variable declaration or function call")

    def parse_var_dec(self):
        """Parse variable declarations"""
        print(f"Parsing variable declaration. Current token: {self.current_token}")
        if self.current_token == "DATA_TYPE":
            self.advance()
            if self.current_token == "IDENTIFIER":
                print(f"Found identifier: {self.current_token}")
                self.advance()
                self.parse_declaration_initialization()
                if self.current_token == "SEMICOLON":
                    self.advance()
                else:
                    print("Syntax Error: Missing semicolon after variable declaration")
                    return
            else:
                print("Syntax Error: Expected identifier after 'inst'")

    def parse_declaration_initialization(self):
        """Parse the initialization part of a declaration (e.g., = value)"""
        print(f"Parsing declaration initialization. Current token: {self.current_token}")
        if self.current_token == "EQUALS":
            self.advance()
            if self.current_token == "NUMBER":
                print(f"Assigned value: {self.current_token}")
                self.advance()
            else:
                print("Syntax Error: Expected a valid value after '='")

    def parse_function_call(self):
        """Parse function calls like 'plant(#x);'"""
        print(f"Parsing function call. Current token: {self.current_token}")
        if self.current_token == "IDENTIFIER":
            print("Parsing function call")
            self.advance()
            if self.current_token == "LPAREN":
                self.advance()
                if self.current_token == "IDENTIFIER":
                    print(f"Found parameter: {self.current_token}")
                    self.advance()
                    if self.current_token == "RPAREN":
                        self.advance()
                        if self.current_token == "SEMICOLON":
                            self.advance()
                        else:
                            print("Syntax Error: Missing semicolon after function call")
                            return
                    else:
                        print("Syntax Error: Missing closing parenthesis in function call")
                        return
                else:
                    print("Syntax Error: Expected identifier inside function call")
                    return
            else:
                print("Syntax Error: Expected opening parenthesis in function call")

def main():
    code = input("Enter DEDOS code: ")  # Get input from the terminal

    lexer.input(code)  # Pass input to lexer
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(token.type)

    print(f"Tokens: {tokens}")

    parser = DEDOSParser(tokens)  # Pass the token list to the parser
    parser.parse()  # Start the syntax analysis

if __name__ == '__main__':
    main()
