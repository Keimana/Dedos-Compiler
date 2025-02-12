class DEDOSParser:
    def __init__(self, LexemeTokens):
        self.LexemeTokens = LexemeTokens
        self.DictLexemeTokens = {}
        self.Terminals = []  # Initialize self.Terminals as an empty list
        self.currentTerminal = None  # Initialize currentTerminal as None
        self.position = 0
        self.currentkeys = None
        self.currentvalues = None
        self.SyntaxErrors = []
        self.lineCounter = 1
        self.SemanticSequence = []
        self.keys = []
        self.values = []

    def ListToDict(self):  # Splitting all whitespace terminals and putting them in dictionaries
        for item in self.LexemeTokens:
            if " : " in item:  # Ensure token is properly formatted
                key, value = item.split(" : ", 1)
                if key in ['SPACE_TOKEN', 'COMMENT'] or value == '"\\t"':
                    continue  # Skip spaces/comments
                self.DictLexemeTokens[key] = value
                self.Terminals.append({key: value})  # Append dictionary to self.Terminals
            else:
                print(f"WARNING: Skipping malformed token -> {item}")  # Debugging output

        if self.Terminals:
            self.currentTerminal = self.Terminals[0]
            self.keys = list(self.currentTerminal.keys())
            self.values = list(self.currentTerminal.values())
            self.currentkeys = self.keys[0]
            self.currentvalues = self.values[0]
        else:
            print("ERROR: No valid tokens found!")  # Handle empty token list


    def next(self):  # character next function
        self.position += 1
        if self.position >= len(self.Terminals):  # Adjust the condition here
            self.currentTerminal = '\0'
        else:
            self.currentTerminal = self.Terminals[self.position]
            self.keys = list(self.currentTerminal.keys())
            self.values = list(self.currentTerminal.values())
            self.currentkeys = self.keys[0]
            self.currentvalues = self.values[0]
            if self.currentkeys == '"NEWLINE"':
                self.lineCounter += 1
                self.next()

    def prev(self):  # character prev function
        self.position -= 1
        if self.position < 0:
            self.currentTerminal = '\0'
        else:
            self.currentTerminal = self.Terminals[self.position]
            self.keys = list(self.currentTerminal.keys())
            self.values = list(self.currentTerminal.values())
            self.currentkeys = self.keys[0]
            self.currentvalues = self.values[0]
            if self.currentkeys == '"NEWLINE"':
                self.lineCounter -= 1
                self.prev()

    def ter_program_start(self):  #<program>

        if self.currentkeys == '~':
            self.next()  # Expected: self.currentkeys = first set of <var_dec> and <body>
            self.SemanticSequence.insert(len(self.SemanticSequence),{"<Program+>": self.position})

            if self.currentkeys in ['inst', 'flank', 'chat','defuse', 'strike', 're', 'load', 'watch', 'force', 'tool','plant', '~', '~'] or 'Identifier' in self.currentkeys:
                pass

            else:
                print("Syntax Error 1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "inst", "defuse", "flank", "chat", "strike", "re", "watch", "load", "force", "tool", "plant", "~", "}}", "Identifier"')  # put Error in a list for viewing in GUI
        else:
            print("Syntax Error 1.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~"')  # put Error in a list for viewing in GUI

    def ter_prog_end(self):  # <program>
        self.next()  # Move to next token

        # Handle unexpected tokens before ~
        while self.currentkeys in ["strike", "flank", "watch", "chat", "inst"]:  # Add more if needed
            print(f"WARNING: Skipping unexpected token {self.currentkeys} at {self.position}")
            self.next()  # Skip to next token

        if self.currentkeys == ';':  
            self.next()  # Skip semicolon and check the next token
        
        if self.currentkeys == '~':  # Ensure ~ is accepted at the program's end
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<Program->": self.position-1})
        else:
            print("Syntax Error 2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: \"{self.currentvalues}\" \n\nExpected: \"~\"')


    def ter_var_declaration(self):  # <var_dec>
        if self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<var_dec+>": self.position})
            self.ter_data_type()
            self.ter_id_or_array()
            self.ter_declare_and_initialize()
            self.ter_var_declaration()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank', 'strike',
                                    'chat', 'tool', 'bounce', '}', 'back', ';'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                  'strike', 'chat', 'tool', 'bounce', '}', 'back', ';'] or 'Identifier' in self.currentkeys:
            pass # NULL <declaration>
        else:
            print("SYNTAX ERROR 3.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected ⏵ "inst", "flank", "strike", "tool", "chat", "plant", "re", "force", "watch", "defuse", "~", "globe", "bounce", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI

    def ter_data_type(self):  # <data type>
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<data_type>": self.position})
        if self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat']:
            self.next()  # Expected: self.currentkeys = follow set <data type>
            if 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected ⏵ "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 4.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected ⏵ "inst", "flank", "strike", "tool", "chat"')  # put error in a list for viewing in GUI

    def ter_id_or_array(self):  # <id or array>
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<id or array+>": self.position})
        if 'Identifier' in self.currentkeys:
            self.ter_id()
            self.ter_index()
            if self.currentkeys in ['=', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                    'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', ']', 'COMMA', ')', '+',
                                    '-', '*', '/', '%', 'abort', 'push', '}', '<', '>', '<=', '>=', '==', '!=', 'and',
                                    'or',
                                    '+=', '-=', '*=', '/=', '%=', ';'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<id or array->": self.position-1})
            else:
                print("SYNTAX ERROR 5: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "]", "COMMA", ")", "+", "-", "*", "/", "%", "abort", "push", "}}", "<", ">", "<=", ">=", "==", "!=", "and", "or", "+=", "-=", "*=", "/=", "%=", "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 5.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "Identifier"')  # put error in a list for viewing in GUI

    def ter_id(self):  # <id>
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<id>": self.position})
        if 'Identifier' in self.currentkeys:
            self.next()  # Expected: self.currentkeys = follow set <id>
            if (self.currentkeys in ['[', '=', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst',
                                     'flank', 'strike', 'chat', 'tool', 'bounce', 'back', ']', 'COMMA', ')', '+', '-',
                                     '*', '/', '%', 'abort', 'push', '}', '<', '>', '<=', '>=', '==', '!=', 'and', 'or',
                                     '+=', '-=', '*=', '/=', '%=', '(', 'in'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 6: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "[", "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "]", "COMMA", ")", "+", "-", "*", "/", "%", "abort", "push", "}}", "<", ">", "<=", ">=", "==", "!=", "and", "or", "+=", "-=", "*=", "/=", "%=", "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 6.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "Identifier"')  # put error in a list for viewing in GUI

    def ter_index(self):  # <index>
        if self.currentkeys == '[':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<index+>": self.position})
            self.next()  # Expected: self.currentkeys = first set <inst or id value>
            self.ter_inst_or_id_value()
            if self.currentkeys == ']':
                self.next()  # Expected: self.currentkeys = first set <2d array> or follow set <index>
                if (self.currentkeys in ['=', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst',
                                         'flank', 'strike', 'chat', 'tool', 'bounce', 'back', ']', 'COMMA', ')', '+',
                                         '-', '*', '/', '%', 'abort', 'push', '}', '<', '>', '<=', '>=', '==', '!=',
                                         'and', 'or', '+=', '-=', '*=', '/=',
                                         '%=', ';'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<index->": self.position-1})
                else:
                    print("SYNTAX ERROR 7: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "]", "COMMA", ")", "+", "-", "*", "/", "%", "abort", "push", "}}", "<", ">", "<=", ">=", "==", "!=", "and", "or", "+=", "-=", "*=", "/=", "%=", "Identifier"')  # put error in a list for viewing in GUI
            else:
                print("SYNTAX ERROR 7.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "]"')  # put error in a list for viewing in GUI
        elif (self.currentkeys in ['=', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst',
                                   'flank', 'strike', 'chat', 'tool', 'bounce', 'back', ']', 'COMMA', ')', '+',
                                   '-', '*', '/', '%', 'abort', 'push', '}', '<', '>', '<=', '>=', '==', '!=',
                                   'and', 'or', '+=', '-=', '*=', '/=',
                                   '%=', ';'] or 'Identifier' in self.currentkeys):
            pass  # NULL <index>
        else:
            print("SYNTAX ERROR 7.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "[", "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "]", "COMMA", ")", "+", "-", "*", "/", "%", "abort", "push", "}}", "<", ">", "<=", ">=", "==", "!=", "and", "or", "+=", "-=", "*=", "/=", "%=", "Identifier"')  # put error in a list for viewing in GUI

    def ter_inst_or_id_value(self):  # <inst or id value>
        if self.currentkeys == 'INSTLIT':  # Handle integer literals
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<intlit>": self.position})
            self.next()  # Consume INSTLIT

            # Expect valid delimiters: ; (delim25), ] (array close), , (separator), or )
            if self.currentkeys in [']', 'COMMA', ')']:
                return  # Valid follow-up, exit function
            elif self.currentkeys == 'delim25' and self.currentvalues == ';':  
                self.next()  # Consume `;` and move forward
            else:
                print("SYNTAX ERROR 8: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\n'
                    f'Expected ⏵ "]", "COMMA", ")", ";"')

        elif self.currentkeys == 'Identifier':  # Handle variable identifiers
            self.ter_id_or_array()

            if self.currentkeys in [']', 'COMMA', ')']:  
                return  # Valid follow-up, exit function
            elif self.currentkeys == 'delim25' and self.currentvalues == ';':  
                self.next()  # Consume `;`
            else:
                print("SYNTAX ERROR 8.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\n'
                    f'Expected ⏵ "]", "COMMA", ")", ";"')

        else:
            print("SYNTAX ERROR 8.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\n'
                f'Expected ⏵ "INSTLIT", "Identifier"')

    def ter_declare_and_initialize(self):  # <declare and initialize>
        if self.currentkeys == '=':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<assignment operator>": self.position})
            self.next()  # Expected: self.currentkeys = first set <allowed value>
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value+>": self.position})
            self.ter_allowed_value()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank', 'strike',
                                     'chat', 'tool', 'bounce', 'back', '}', ';'] or 'Identifier' in self.currentkeys):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value->": self.position-1})
            else:
                print("SYNTAX ERROR 10: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI
        elif (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank', 'strike',
                                   'chat', 'tool', 'bounce', 'back', '}', ';'] or 'Identifier' in self.currentkeys):
            pass
        else:
            print("SYNTAX ERROR 10.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI

    def ter_allowed_value(self):  # <allowed value>
        if self.currentkeys == 'INSTLIT':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<intlit>": self.position})
            self.next()  # Consume INSTLIT
            
            # Ensure that the next token is a delimiter (';')
            if self.currentkeys == ';':
                self.next()  # Consume ';' and move forward
            else:
                print("SYNTAX ERROR 11.8: Missing ';' after integer literal", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f"LINE #{self.lineCounter} : Missing ';' after integer literal"
                )  # Put error in a list for viewing in GUI
            return

        if self.currentkeys == 'info':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<input+>": self.position})
            self.next()  # Expected: self.currentkeys = first set <parameter>
            if self.currentkeys == '(':
                self.next()  # Expected: self.currentkeys = first set <return value>
                self.ter_back_value()
                if self.currentkeys == ')':
                    self.next()  # Expected: self.currentkeys = follow set <allowed value>
                    if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                             'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                             'push', '}', ';'] or 'Identifier' in self.currentkeys):
                        self.SemanticSequence.insert(len(self.SemanticSequence), {"<input->": self.position-1})
                    else:
                        print("SYNTAX ERROR 11: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}", "Identifier"')  # put error in a list for viewing in GUI
                else:
                    print("SYNTAX ERROR 11.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI
            else:
                print("SYNTAX ERROR 11.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI
        elif self.currentkeys == '[':
            self.ter_array_value()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}', ';'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys == 'CHATLIT':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<CHATLIT>": self.position})
            
            self.next()  # Expected: self.currentkeys = follow set <allowed value>
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}', ';'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['neg', 'pos']:
            self.ter_tool_value()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}', ';'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.5: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['(', 'INSTLIT', 'FLANKLIT', 'STRIKELIT'] or 'Identifier' in self.currentkeys:
            self.ter_math_expression()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}', ';'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.6: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 11.7: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI
        if "NEWLINE" in self.currentkeys:
            self.lineCounter += 1
            self.next()

    def ter_back_value(self):
        if (self.currentkeys in ['[', 'CHATLIT', 'neg', 'pos', '(', 'INSTLIT', 'FLANKLIT',
                                 'STRIKELIT'] or 'Identifier' in self.currentkeys):
            self.ter_data_value()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 12: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI
        elif self.currentkeys == ')':
            pass  # NULL <return value>
        else:
            print("SYNTAX ERROR 12.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier", ")"')  # put error in a list for viewing in GUI

    def ter_data_value(self):
        if self.currentkeys in ['FLANKLIT', 'INSTLIT', 'STRIKELIT', 'CHATLIT', 'neg',
                                '(','pos'] or 'Identifier' in self.currentkeys:
            self.ter_data_value_no_array()
            if self.currentkeys in [')', 'COMMA', ']']:
                pass
            else:
                print("SYNTAX ERROR 13: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "COMMA", "]"')  # put error in a list for viewing in GUI
        elif self.currentkeys == '[':
            self.ter_array_value()
            if self.currentkeys in [')', 'COMMA', ']']:
                pass
            else:
                print("SYNTAX ERROR 13.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "COMMA", "]"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 13.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "FLANKLIT", "INSTLIT", "STRIKELIT", "CHATLIT", "neg", "pos", "Identifier", "["')  # put error in a list for viewing in GUI

    def ter_data_value_no_array(self):
        if self.currentkeys in ['neg', 'pos']:
            self.ter_tool_value()
            if (self.currentkeys in [')', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']):
                pass
            else:
                print("SYNTAX ERROR 14: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or"')  # put error in a list for viewing in GUI
        elif self.currentkeys == 'CHATLIT':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<CHATLIT+>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <data value no array>
            if (self.currentkeys in [')', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<CHATLIT->": self.position-1})
            else:
                print("SYNTAX ERROR 14.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['(', 'FLANKLIT', 'INSTLIT', 'STRIKELIT'] or 'Identifier' in self.currentkeys:
            self.ter_math_expression()
            if (self.currentkeys in [')', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']):
                pass
            else:
                print("SYNTAX ERROR 14.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 14.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "neg", "pos", "CHATLIT", "(", "FLANKLIT", "INSTLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI

    def ter_tool_value(self):
        if self.currentkeys in ['neg', 'pos']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<tool value>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <tool value>
            if (self.currentkeys in [')', 'COMMA', ']', '==', '!=', 'and', 'or', 'inst', 'strike', 'chat', 'tool',
                                     'flank', '}', '~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce', 'abort',
                                     'push'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 15: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "COMMA", "]", "==", "!=", "and", "or", "inst", "strike", "chat", "tool", "flank", "}}", "~", "plant", "re", "force", "watch", "defuse", "bounce", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI

        else:
            print("SYNTAX ERROR 15.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "neg", "pos"')  # put error in a list for viewing in GUI


    def ter_math_expression(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression+>": self.position})
        if self.currentkeys == '(':
            self.next()  # Expected: self.currentkeys = first set <math expression>
            self.ter_math_expression()
            if self.currentkeys == ')':
                self.next()  # Expected: self.currentkeys = first set <arithmetic tail> or follow set <math expression>
                self.ter_arithmetic_tail()
                if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                         'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                         'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or',
                                         '}'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
                else:
                    print("SYNTAX ERROR 16: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
            else:
                print("SYNTAX ERROR 16.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['INSTLIT', 'FLANKLIT']:
            self.ter_number_value()
            self.ter_arithmetic_tail()
            if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                     'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                     'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                     'or', '}'] or 'Identifier' in self.currentkeys):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
            else:
                print("SYNTAX ERROR 16.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys == 'STRIKELIT':
            self.next()  # Expected: self.currentkeys = first set <arithmetic tail> or follow set <math expression>
            if self.currentkeys == '+':
                self.ter_arithmetic_tail()
                if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                         'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                         'COMMA', ']', '==', '!=', 'and',
                                         'or', '}'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
                else:
                    print("SYNTAX ERROR 16.3: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
            elif (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                       'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                       'COMMA', ']', '==', '!=', 'and',
                                       'or', '}'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
            else:
                print("SYNTAX ERROR 16.3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "==", "!=", "and", "or", "}}", "Identifier", "+"')  # put error in a list for viewing in GUI

        elif 'Identifier' in self.currentkeys:
            self.ter_id_or_array()
            self.ter_arithmetic_tail()
            if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                     'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                     'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                     'or', '}'] or 'Identifier' in self.currentkeys):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
            else:
                print("SYNTAX ERROR 16.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}" "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 16.5: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI

    def ter_arithmetic_tail(self):
        if self.currentkeys in ['+', '-', '*', '/', '%']:
            self.ter_arithmetic()
            self.ter_math_expression()
            if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                     'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                     'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                     'or', '}'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 17: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
        elif (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                   'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                   'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                   'or', '}'] or 'Identifier' in self.currentkeys):
            pass  # NULL <arithmetic tail>
        else:
            print("SYNTAX ERROR 17.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "+", "-", "*", "/", "%", ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI

    def ter_arithmetic(self):
        if self.currentkeys in ['+', '-', '*', '/', '%']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<arithmetic>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <arithmetic>
            if self.currentkeys in ['(', 'INSTLIT', 'FLANKLIT', 'STRIKELIT'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 17.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 17.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "+", "-", "*", "/", "%"')  # put error in a list for viewing in GUI:

    def ter_number_value(self):
        if self.currentkeys in ['FLANKLIT', 'INSTLIT']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<number value>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <number value>
            if self.currentkeys in ['+', '-', '*', '/', '%', ')', 'plant', 're', 'force', 'watch', 'defuse',
                                    '~', 'globe', 'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back',
                                    'abort', 'push', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 18: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "+", "-", "*", "/", "%", ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "Identifier", "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 18.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "FLANKLIT", "INSTLIT"')  # put error in a list for viewing in GUI:

    def ter_array_value(self):
        if self.currentkeys == '[':
            self.next()  # Expected: self.currentkeys = first set <parameter values>
            self.ter_array_parameter_values()
            if self.currentkeys == ']':
                self.next()  # Expected: self.currentkeys = follow set <array value>
                if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst',
                                        'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push', ')',
                                        'COMMA', ']', '}', ';'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 19: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", ")", "COMMA", "]", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 19.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "]"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 19.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "["')  # put error in a list for viewing in GUI:

    def ter_array_parameter_values(self):
        if self.currentkeys in ['[', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT',
                                'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.ter_array_data_value()
            self.ter_array_parameter_tail()
            if self.currentkeys == ']':
                pass
            else:
                print("SYNTAX ERROR 20: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "]"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 20.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "[", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT"')  # put error in a list for viewing in GUI:

    def ter_array_data_value(self):
        if self.currentkeys in ['neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.ter_data_value()
            if self.currentkeys in ['COMMA', ']']:
                pass
            else:
                print("SYNTAX ERROR 21: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", "]"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 21.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier", "["')  # put error in a list for viewing in GUI:

    def ter_data_value_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.ter_data_value_no_array()
            self.ter_data_value_tail()
            if self.currentkeys == ']':
                pass
            else:
                print("SYNTAX ERROR 23: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "]"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ']':
            pass  # NULL <data value tail>
        else:
            print("SYNTAX ERROR 23.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", "]"')  # put error in a list for viewing in GUI:

    def ter_array_parameter_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.ter_array_data_value()
            self.ter_array_parameter_tail()
            if self.currentkeys == ']':
                pass
            else:
                print("SYNTAX ERROR 24: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "]"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ']':
            pass  # NULL <array parameter tail>
        else:
            print("SYNTAX ERROR 24.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", "]"')  # put error in a list for viewing in GUI:

    def ter_body(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse'] or 'Identifier' in self.currentkeys:
            self.ter_statement()
            if self.currentkeys == '~':
                pass
            else:
                print("SYNTAX ERROR 25: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ~')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '~':
            pass  # NULL <body>
        else:
            print("SYNTAX ERROR 25.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_statement(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch'] or 'Identifier' in self.currentkeys:
            self.ter_body_no_defuse()
            self.ter_statement()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 26: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'defuse':
            self.ter_function()
            self.ter_statement()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 26.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <statement>
        else:
            print("SYNTAX ERROR 26.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "Identifier", "defuse", "~"')  # put error in a list for viewing in GUI:

    def ter_body_no_defuse(self):
        if self.currentkeys in ['plant', 'force', 'watch'] or 'Identifier' in self.currentkeys:
            self.ter_body_no_if_defuse()
            if self.currentkeys in ['bounce', 'plant', 're', 'force', 'watch', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 27: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "plant", "re", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 're':
            self.ter_condition_statement()
            if self.currentkeys in ['bounce', 'plant', 're', 'force', 'watch', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 27.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "plant", "re", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['bounce', 'plant', 're', 'force', 'watch', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <body no defuse>
        else:
            print("SYNTAX ERROR 27.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "plant", "re", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_body_no_if_defuse(self):
        if self.currentkeys == 'plant' or 'Identifier' in self.currentkeys:
            if self.currentkeys == 'plant':
                self.ter_body_no_if_loop_defuse()
                if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                        '}', '~'] or 'Identifier' in self.currentkeys:
                    pass
            elif 'Identifier' in self.currentkeys:
                self.next()  # Expected: self.currentkeys = '(' if in <function call statement>
                if self.currentkeys == '(':
                    self.prev()
                    self.ter_function_call_statement()
                    if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                            '}', '~'] or 'Identifier' in self.currentkeys:
                        pass
                    else:
                        print("SYNTAX ERROR 29: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
                else:
                    self.prev()  # if Identifier but not for <function call statement>
                    self.ter_body_no_if_loop_defuse()
                    if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                            '}', '~'] or 'Identifier' in self.currentkeys:
                        pass
                    else:
                        print("SYNTAX ERROR 29.1: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:

            else:
                print("SYNTAX ERROR 28: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch']:
            self.ter_loop_statement()
            if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 28.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <body no if-defuse>
        else:
            print("SYNTAX ERROR 28.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_body_no_if_loop_defuse(self):
        if 'Identifier' in self.currentkeys:
            self.ter_initialization_statement()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 29.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'plant':
            self.ter_output_statement()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 29.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <body no if-loop-defuse>
        else:
            print("SYNTAX ERROR 29.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_call_statement(self):
        if 'Identifier' in self.currentkeys:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function call statement+>": self.position})
            self.ter_id()
            self.ter_parameter()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function call statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 29.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 29.5: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "Identifier"')  # put error in a list for viewing in GUI:

    def ter_parameter(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<parameter+>": self.position})
        if self.currentkeys == '(':
            self.next()
            self.ter_parameter_values()
            if self.currentkeys == ')':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<parameter->": self.position})
                self.next()
                if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                        'plant', 'defuse', '}', ';'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 30: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 30.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 30.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI:

    def ter_parameter_values(self):
        if self.currentkeys in ['FLANKLIT', 'INSTLIT', 'STRIKELIT', 'CHATLIT', 'neg', 'pos',
                                '(','['] or 'Identifier' in self.currentkeys:
            self.ter_data_value()
            self.ter_parameter_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 31: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <parameter values>
        else:
            print("SYNTAX ERROR 31.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "FLANKLIT", "INSTLIT", "STRIKELIT", "CHATLIT", "neg", "pos", "[", "Identifier", ")"')  # put error in a list for viewing in GUI:

    def ter_parameter_tail(self):
        if self.currentkeys == 'COMMA':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<comma>": self.position})
            self.next()
            self.ter_parameter_values()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 32: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass
        else:
            print("SYNTAX ERROR 32.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", ")"')  # put error in a list for viewing in GUI:

    def ter_output_statement(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<output statement+>": self.position})
        
        if self.currentkeys == 'plant':
            self.next()
            self.ter_parameter()

            # Check if a semicolon is present after the parameter
            if self.currentkeys == ';':
                self.next()  # Move past the semicolon
                print(f"DEBUG: After semicolon, next token is '{self.currentkeys}' on line {self.lineCounter}")


            else:
                print("SYNTAX ERROR 34: Missing semicolon", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Missing semicolon ⏵ Expected ";" at the end of the output statement'
                )

        else:
            print("SYNTAX ERROR 33.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant"'
            )



    def ter_initialization_statement(self):
        if 'Identifier' in self.currentkeys:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<initialization statement+>": self.position})
            self.ter_id_or_array()
            self.ter_assignment_operator()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value+>": self.position})
            self.ter_allowed_value_initialize()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value->": self.position-1})
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<initialization statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 34: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 34.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "Identifier"')  # put error in a list for viewing in GUI:

    def ter_assignment_operator(self):
        if self.currentkeys in ['=', '+=', '-=', '*=', '/=', '%=']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<assignment operator>": self.position})
            self.next()
            if self.currentkeys in ['info', '[', 'CHATLIT', 'neg', 'pos', '(', 'INSTLIT', 'STRIKELIT',
                                    'FLANKLIT'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 35: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "STRIKELIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 35.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "=", "+=", "-=", "*=", "/=", "%="')  # put error in a list for viewing in GUI:

    def ter_allowed_value_initialize(self):
        if 'Identifier' in self.currentkeys:
            self.next()  # Expected: self.currentkeys = '(' if in <function call statement>
            if self.currentkeys == '(':
                self.prev()
                self.ter_function_call_statement()
            else:
                self.prev()  # if Identifier but not for <function call statement>
                if 'Identifier' in self.currentkeys:
                    self.ter_allowed_value()
                    if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push',
                                            'plant', 'defuse', '}', '~'] or 'Identifier' in self.currentkeys:
                        pass
                    else:
                        print("SYNTAX ERROR 36: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "plant", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['info', '[', 'CHATLIT', 'neg', 'pos', '(', 'INSTLIT', 'FLANKLIT', 'STRIKELIT']:
            self.ter_allowed_value()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push',
                                    'plant', 'defuse', '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 36.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "abort", "push", "plant", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 36.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "Identifier", "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "FLANKLIT", "STRIKELIT"')  # put error in a list for viewing in GUI:
        if "NEWLINE" in self.currentkeys:
            self.lineCounter += 1
            self.next()

    def ter_loop_statement(self):
        if self.currentkeys == 'force':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<force loop+>": self.position})
            self.ter_for()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body+>": self.position})
            self.ter_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body->": self.position - 1})
            if self.currentkeys in ['~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce', 'back', '}',
                                    'abort', 'push'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<force loop->": self.position-1})
            else:
                print("SYNTAX ERROR 37: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "~", "plant", "re", "force", "watch", "defuse", "bounce", "back", "}}", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'watch':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<watch loop+>": self.position})
            self.ter_watch()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body+>": self.position})
            self.ter_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body->": self.position - 1})
            if self.currentkeys in ['~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce', 'back', '}',
                                    'abort', 'push'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<watch loop->": self.position - 1})
            else:
                print("SYNTAX ERROR 37.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "~", "plant", "re", "force", "watch", "defuse", "bounce", "back", "}}", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 37.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch"')  # put error in a list for viewing in GUI:

    def ter_for(self):
        if self.currentkeys == 'force':
            self.next()
            self.ter_id()
            if self.currentkeys == 'in':
                self.next()
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<perim+>": self.position})
                if self.currentkeys == 'perim':
                    self.next()
                    if self.currentkeys == '(':
                        self.next()
                        self.ter_inst_or_id_value()
                        self.ter_perim()
                        if self.currentkeys == ')':
                            self.SemanticSequence.insert(len(self.SemanticSequence), {"<perim->": self.position})
                            self.next()
                            if self.currentkeys == '{':
                                pass
                            else:
                                print("SYNTAX ERROR 38: Unexpected", self.currentvalues, self.lineCounter)
                                self.SyntaxErrors.append(
                                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:
                        else:
                            print("SYNTAX ERROR 38.1: Unexpected", self.currentvalues, self.lineCounter)
                            self.SyntaxErrors.append(
                                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
                    else:
                        print("SYNTAX ERROR 38.2: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 38.3: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "perim"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 38.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "in"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 38.5: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force"')  # put error in a list for viewing in GUI:

    def ter_perim(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.ter_inst_or_id_value()
            self.ter_perim_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 39: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <perim>
        else:
            print("SYNTAX ERROR 39.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", ")"')  # put error in a list for viewing in GUI:

    def ter_perim_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.ter_inst_or_id_value()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 40: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <perim tail>
        else:
            print("SYNTAX ERROR 40.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", ")"')  # put error in a list for viewing in GUI:

    def ter_loop_body(self):
        if self.currentkeys == '{':
            self.next()
            self.ter_loop_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                        'defuse', '}', '~', 'reload', 'load'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 41: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "reload", "load", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 41.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 41.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:

    def ter_loop_content(self):
        if self.currentkeys in ['force', 'watch', 'plant', 're', 'bounce', 'abort',
                                'push'] or 'Identifier' in self.currentkeys:
            self.ter_body_no_if_defuse()
            self.ter_loop_condition()
            self.ter_control_flow()
            self.ter_loop_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 42: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass
        else:
            print("SYNTAX ERROR 42.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch", "plant", "re", "bounce", "abort", "push", "Identifier", "}}"')  # put error in a list for viewing in GUI:

    def ter_loop_condition(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop condition+>": self.position})
            self.ter_loop_re()
            self.ter_loop_reload()
            self.ter_loop_load()
            if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop condition->": self.position-1})
            else:
                print("SYNTAX ERROR 43: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "bounce", "abort", "push", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <loop condition>
        else:
            print("SYNTAX ERROR 43.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "bounce", "abort", "push", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_loop_re(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop if+>": self.position})
            self.ter_re()
            self.ter_loop_body()
            if self.currentkeys in ['reload', 'load', 're', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop if->": self.position-1})
            else:
                print("SYNTAX ERROR 44: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "re", "bounce", "abort", "push", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 44.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re"')  # put error in a list for viewing in GUI:

    def ter_re(self):
        if self.currentkeys == 're':
            self.next()
            self.ter_condition()
            if self.currentkeys == '{':
                pass
            else:
                print("SYNTAX ERROR 45: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 45.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re"')  # put error in a list for viewing in GUI:

    def ter_condition(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition+>": self.position})
        if self.currentkeys == '(':
            self.next()
            self.ter_logical_expression()
            if self.currentkeys == ')':
                self.next()
                if self.currentkeys == '{':
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition->": self.position-1})
                else:
                    print("SYNTAX ERROR 46: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 46.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 46.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI:

    def ter_logical_expression(self):
        if self.currentkeys == '(':
            self.next()
            self.ter_logical_expression()
            if self.currentkeys == ')':
                self.next()
                self.ter_logic_or_relational_tail()
                if self.currentkeys == ')':
                    pass
                else:
                    print("SYNTAX ERROR 47: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 47.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'not':
            self.ter_not_logic()
            self.ter_logic_or_relational_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 47.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT',
                                  'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.ter_relational_expression()
            self.ter_logic_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 47.3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 47.4: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "(", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_logic_tail(self):
        if self.currentkeys in ['and', 'or']:
            self.ter_logical_operator()
            self.ter_logical_expression()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 48: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <logic tail>
        else:
            print("SYNTAX ERROR 48.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "and", "or", ")"')  # put error in a list for viewing in GUI:

    def ter_logical_operator(self):
        if self.currentkeys in ['and', 'or']:
            self.next()
            if self.currentkeys in ['(', 'not', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT',
                                    ] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 49: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "(", "not", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 49.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "and", "or"')  # put error in a list for viewing in GUI:

    def ter_not_logic(self):
        if self.currentkeys == 'not':
            self.next()
            if self.currentkeys == '(':
                self.next()
                self.ter_logical_expression()
                if self.currentkeys == ')':
                    self.next()
                    if self.currentkeys in ['and', 'or', '==', '!=', ')']:
                        pass
                    else:
                        print("SYNTAX ERROR 50: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "and", "or", "==", "!="')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 50.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 50.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 50.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "not"')  # put error in a list for viewing in GUI:

    def ter_logic_or_relational_tail(self):
        if self.currentkeys in ['and', 'or']:
            self.ter_logic_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 51: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['<', '>', '<=', '>=', '==', '!=']:
            self.ter_relational_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 51.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass
        elif self.currentkeys in ['(', 'not', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT',
                                    ] or 'Identifier' in self.currentkeys:
            self.ter_logical_expression() #NOTSURE PA HERE EXPERIMENT LANG
        else:
            print("SYNTAX ERROR 51.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "and", "or", "==", "!=", ")"')  # put error in a list for viewing in GUI:

    def ter_relational_expression(self):
        if self.currentkeys == '(':
            self.next()
            self.ter_logic_or_relational_tail()
            if self.currentkeys == ')':
                self.next()
                if self.currentkeys in [')', 'and', 'or']:
                    pass
                else:
                    print("SYNTAX ERROR 52: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "and", "or"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 52.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT',
                                  'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.ter_data_value_no_array()
            self.ter_logic_or_relational_tail()
            if self.currentkeys in [')', 'and', 'or']:
                pass
            else:
                print("SYNTAX ERROR 52.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "and", "or"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 52.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "(", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_relational_tail(self):
        if self.currentkeys in ['<', '>', '<=', '>=', '==', '!=']:
            self.ter_relational_operator()
            self.ter_relational_expression()
            if self.currentkeys in [')', 'and', 'or']:
                pass
            else:
                print("SYNTAX ERROR 53: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")", "and", "or"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in [')', 'and', 'or']:
            pass  # NULL <relational tail>
        else:
            print("SYNTAX ERROR 53.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "<", ">", "<=", ">=", "==", "!=", ")", "and", "or"')  # put error in a list for viewing in GUI:

    def ter_relational_operator(self):
        if self.currentkeys in ['<', '>', '<=', '>=', '==', '!=']:
            self.next()
            if self.currentkeys in ['(', 'not', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT',
                                    ] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 54: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "(", "not", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 54.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "<", ">", "<=", ">=", "==", "!="')  # put error in a list for viewing in GUI:

    def ter_loop_reload(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop elif+>": self.position})
            self.ter_reload()
            self.ter_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop elif->": self.position - 1})
            self.ter_loop_reload()
            if self.currentkeys in ['load', 'bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 55: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <loop elif>
        else:
            print("SYNTAX ERROR 55.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_reload(self):
        if self.currentkeys == 'reload':
            self.next()
            self.ter_condition()
            if self.currentkeys == '{':
                pass
            else:
                print("SYNTAX ERROR 56: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 56.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload"')  # put error in a list for viewing in GUI:

    def ter_loop_load(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop else+>": self.position})
            self.next()
            self.ter_loop_body()
            if self.currentkeys in ['bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop else->": self.position-1})
            else:
                print("SYNTAX ERROR 57: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <loop else>
        else:
            print("SYNTAX ERROR 57.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "load", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_control_flow(self):
        if self.currentkeys in ['bounce', 'abort', 'push']:
            if self.currentvalues == 'bounce':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<pass>": self.position})
            elif self.currentvalues == 'abort':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<break>": self.position})
            elif self.currentvalues == 'push':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<continue>": self.position})
            self.next()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'abort', 'push',
                                    '}', 'back'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 58: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "bounce", "abort", "push", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'abort', 'push',
                                  '}', 'back'] or 'Identifier' in self.currentkeys:
            pass  # NULL <control flow>
        else:
            print("SYNTAX ERROR 58.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "bounce", "abort", "push", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_watch(self):
        if self.currentkeys == 'watch':
            self.next()
            self.ter_condition()
            if self.currentkeys == '{':
                pass
            else:
                print("SYNTAX ERROR 59: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 59.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "watch"')  # put error in a list for viewing in GUI:

    def ter_condition_statement(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition statement+>": self.position})
            self.ter_re_with_body()
            self.ter_reload_with_body()
            self.ter_load_with_body()
            if self.currentkeys in ['~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce',
                                    '}', 'back', 'abort', 'push'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 60: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "~", "plant", "re", "force", "watch", "defuse", "bounce", "}}", "back", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 60.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re"')  # put error in a list for viewing in GUI:

    def ter_re_with_body(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<if with body+>": self.position})
        if self.currentkeys == 're':
            self.ter_re()
            self.ter_condition_body()
            if self.currentkeys in ['reload', 'load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<if with body->": self.position - 1})
            else:
                print("SYNTAX ERROR 61: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 61.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re"')  # put error in a list for viewing in GUI:

    def ter_condition_body(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition body+>": self.position})
        if self.currentkeys == '{':
            self.next()
            self.ter_condition_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['reload', 'load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                        '}', '~'] or 'Identifier' in self.currentkeys:
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition body->": self.position -1})
                else:
                    print("SYNTAX ERROR 62: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 62.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 62.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:

    def ter_condition_content(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce'] or 'Identifier' in self.currentkeys:
            self.ter_body_no_defuse()
            self.ter_pass()
            self.ter_condition_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 63: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass  # NULL <condition content>
        else:
            print("SYNTAX ERROR 63.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "bounce", "Identifier", "}}"')  # put error in a list for viewing in GUI:

    def ter_pass(self):
        if self.currentkeys == 'bounce':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<pass>": self.position})
            self.next()
            if self.currentkeys in ['plant', 're', 'watch', 'force', 'bounce', 'back',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 64: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "watch", "force", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'watch', 'force', 'bounce',
                                  'back', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <pass>
        else:
            print("SYNTAX ERROR 64.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "plant", "re", "watch", "force", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_reload_with_body(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<elif with body+>": self.position})
            self.ter_reload()
            self.ter_condition_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<elif with body->": self.position - 1})
            self.ter_reload_with_body()
            if self.currentkeys in ['load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 65: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <elif with body>
        else:
            print("SYNTAX ERROR 65.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_load_with_body(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<else with body+>": self.position})
            self.next()
            self.ter_condition_body()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<else with body->": self.position-1})
            else:
                print("SYNTAX ERROR 66: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <else with body>
        else:
            print("SYNTAX ERROR 66.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<function+>": self.position})
        if self.currentkeys == 'defuse':
            self.next()
            self.ter_id()
            if self.currentkeys == '(':
                self.next()
                self.ter_function_parameter()
                if self.currentkeys == ')':
                    self.next()
                    self.ter_function_body()
                    if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                            '~'] or 'Identifier' in self.currentkeys:
                        self.SemanticSequence.insert(len(self.SemanticSequence), {"<function->": self.position-1})
                    else:
                        print("SYNTAX ERROR 67: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "bounce", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 67.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 67.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 67.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "defuse"')  # put error in a list for viewing in GUI:

    def ter_function_parameter(self):
        if 'Identifier' in self.currentkeys:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function parameter+>": self.position})
            self.ter_id()
            self.ter_id_tail()
            if self.currentkeys == ')':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function parameter->": self.position-1})
            else:
                print("SYNTAX ERROR 68: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <function parameter>
        else:
            print("SYNTAX ERROR 68.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "Identifier", ")"')  # put error in a list for viewing in GUI:

    def ter_id_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.ter_function_parameter()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 69: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <id tail>
        else:
            print("SYNTAX ERROR 69.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "COMMA", ")"')  # put error in a list for viewing in GUI:

    def ter_function_body(self):
        if self.currentkeys == '{':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function body+>": self.position})
            self.next()
            self.ter_function_declaration()
            self.ter_function_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse',
                                        '~'] or 'Identifier' in self.currentkeys:
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<function body->": self.position-1})
                else:
                    print("SYNTAX ERROR 70: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 70.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:

    def ter_function_declaration(self):
        if self.currentkeys == 'universal':
            self.ter_globe()
            self.ter_function_declaration()
            if self.currentkeys in ['plant', 're', 'force', 'watch', '}', 'bounce',
                                    'back'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 71: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['inst', 'flank', 'strike', 'chat', 'tool']:
            self.ter_var_declaration()
            self.ter_function_declaration()
            if self.currentkeys in ['plant', 're', 'force', 'watch', '}', 'back'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 71.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "plant", "re", "force", "watch", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', '}', 'bounce',
                                  'back'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function declaration>
        else:
            print("SYNTAX ERROR 71.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "universal", "inst", "flank", "strike", "chat", "tool", "plant", "re", "force", "watch", "}}" , "Identifier"')  # put error in a list for viewing in GUI:

    def ter_globe(self):
        if self.currentkeys == 'universal':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<universal+>": self.position})
            self.next()
            self.ter_data_type()
            self.ter_id_or_array()
            if self.currentkeys in ['universal', 'inst', 'flank', 'strike', 'chat', 'tool', 'plant', 're',
                                    'force', 'watch', '}', 'bounce'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<universal->": self.position})
            else:
                print("SYNTAX ERROR 72: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "universal", "inst", "flank", "strike", "chat", "tool", "plant", "re", "force", "watch", "}}", "bounce", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['universal', 'inst', 'flank', 'strike', 'chat', 'tool', 'plant', 're',
                                  'force', 'watch', '}', 'bounce'] or 'Identifier' in self.currentkeys:
            pass  # NULL <universal>
        else:
            print("SYNTAX ERROR 72.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "universal", "inst", "flank", "strike", "chat", "tool", "plant", "re", "force", "watch", "}}", "bounce", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_content(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce',
                                'back'] or 'Identifier' in self.currentkeys:
            self.ter_body_no_if_loop_defuse()
            self.ter_function_condition()
            self.ter_function_loop()
            self.ter_pass()
            self.ter_back()
            self.ter_function_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 73: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass  # NULL <function content>
        else:
            print("SYNTAX ERROR 73.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "plant", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_condition(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition+>": self.position})
            self.ter_function_re()
            self.ter_function_reload()
            self.ter_function_load()
            if self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition->": self.position})
            else:
                print("SYNTAX ERROR 74: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "plant", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        if self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function condition>
        else:
            print("SYNTAX ERROR 74.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "back", "plant", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_re(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function if+>": self.position})
            self.ter_re()
            self.ter_function_condition_body()
            if self.currentkeys in ['reload', 'load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function if->": self.position-1})
            else:
                print("SYNTAX ERROR 75: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 75.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re"')  # put error in a list for viewing in GUI:

    def ter_function_condition_body(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition body+>": self.position})
        if self.currentkeys == '{':
            self.next()
            self.ter_function_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['reload', 'load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                        '}'] or 'Identifier' in self.currentkeys:
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition body->": self.position - 1})
                else:
                    print("SYNTAX ERROR 76: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 76.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 76.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:

    def ter_function_reload(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function elif+>": self.position})
            self.ter_reload()
            self.ter_function_condition_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function elif->": self.position - 1})
            self.ter_function_reload()
            if self.currentkeys in ['load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 77: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function elif>
        else:
            print("SYNTAX ERROR 77.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", ')  # put error in a list for viewing in GUI:

    def ter_function_load(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function else+>": self.position})
            self.next()
            self.ter_function_condition_body()
            if self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function else->": self.position - 1})
            else:
                print("SYNTAX ERROR 78: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function else>
        else:
            print("SYNTAX ERROR 78.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_loop(self):
        if self.currentkeys == 'force':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function force loop+>": self.position})
            self.ter_for()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body+>": self.position})
            self.ter_function_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body->": self.position - 1})
            if self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force', 'watch',
                                    're'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function force loop->": self.position - 1})
            else:
                print("SYNTAX ERROR 79: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'watch':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function watch loop+>": self.position})
            self.ter_watch()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body+>": self.position})
            self.ter_function_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body->": self.position - 1})
            if self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force', 'watch',
                                    're'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function watch loop->": self.position - 1})
            else:
                print("SYNTAX ERROR 79.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force', 'watch',
                                  're'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop>
        else:
            print("SYNTAX ERROR 79.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch", "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_loop_body(self):
        if self.currentkeys == '{':
            self.next()
            self.ter_function_loop_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force',
                                        'watch', 're', 'reload', 'load'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 80: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "reload", "load", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 80.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 80.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "{{"')  # put error in a list for viewing in GUI:

    def ter_function_loop_content(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'abort', 'push',
                                'back'] or 'Identifier' in self.currentkeys:
            self.ter_body_no_if_loop_defuse()
            self.ter_function_loop_condition()
            self.ter_function_loop()
            self.ter_control_flow()
            self.ter_back()
            self.ter_function_loop_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 81: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass  # NULL <function loop content>
        else:
            print("SYNTAX ERROR 81.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_loop_condition(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop condition+>": self.position})
            self.ter_function_loop_re()
            self.ter_function_loop_reload()
            self.ter_function_loop_load()
            if self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop condition->": self.position-1})
            else:
                print("SYNTAX ERROR 82: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop condition>
        else:
            print("SYNTAX ERROR 82.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_loop_re(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop if+>": self.position})
            self.ter_re()
            self.ter_function_loop_body()
            if self.currentkeys in ['reload', 'load', 'force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop if->": self.position-1})
            else:
                print("SYNTAX ERROR 83: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 83.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "re"')  # put error in a list for viewing in GUI:

    def ter_function_loop_reload(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop elif+>": self.position})
            self.ter_reload()
            self.ter_function_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop elif->": self.position - 1})
            self.ter_function_loop_reload()
            if self.currentkeys in ['load', 'force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 84: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop elif>
        else:
            print("SYNTAX ERROR 84.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "reload", "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_function_loop_else(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop else+>": self.position})
            self.next()
            self.ter_function_loop_body()
            if self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop else->": self.position-1})
            else:
                print("SYNTAX ERROR 85: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop else>
        else:
            print("SYNTAX ERROR 85.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def ter_back(self):
        if self.currentkeys == 'back':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<return+>": self.position})
            self.next()
            if self.currentkeys == '(':
                self.next()
                self.ter_back_value()
                if self.currentkeys == ')':
                    self.next()
                    if self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                            're', '}'] or 'Identifier' in self.currentkeys:
                        self.SemanticSequence.insert(len(self.SemanticSequence), {"<return->": self.position-1})
                    else:
                        print("SYNTAX ERROR 86: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 86.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 86.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "("')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <return>
        else:
            print("SYNTAX ERROR 86.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}" \n\nExpected ⏵ "back", "force", "watch", "bounce", "abort", "push", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    # =====================================The STRUCTURE CODE============================================================#

    def GetNextTerminal(self):  # <program> and <program content>
        terminator = 0
        ctr = 0
        if self.currentkeys == '"NEWLINE"':
            print("SYNTAX ERROR 87: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~}}"')  # put error in a list for viewing in GUI #
        if self.currentkeys == '~':
            terminator += 1
        self.ter_program_start()
        while self.position < len(self.Terminals) and ctr != len(self.Terminals) and terminator != 0:
            if self.currentkeys == ';':
                break
            if self.currentkeys == '~':
                break
            elif self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat']:
                self.ter_var_declaration()
            elif self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse'] or "Identifier" in self.currentkeys:
                self.ter_body()
            else:
                print("SYNTAX ERROR X:", self.currentvalues)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected ⏵ "{self.currentvalues}"')  # put error in a list for viewing in GUI
                break
            ctr += 1
        self.ter_prog_end()
        if len(self.SyntaxErrors) == 0:
            print("SYNTAX COMPILE SUCCESSFUL", self.lineCounter)
            self.SyntaxErrors.append("-------------------------------------------------------------SYNTAX COMPILE SUCCESSFUL\n-------------------------------------------------------------\n\n")  # put in a list for viewing in GUI
            print(self.SemanticSequence)
        else:
            print("ERRORS FOUND", self.lineCounter)
        return self.SyntaxErrors

