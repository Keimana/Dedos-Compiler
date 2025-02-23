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

    def ListToDict(self):
        for item in self.LexemeTokens:
            if " : " in item:
                key, value = item.split(" : ", 1)
                if key in ['SPACE_TOKEN', 'COMMENT'] or value == '"\\t"':
                    pass
                else:
                    self.DictLexemeTokens[key] = value
                    self.Terminals.append({key: value})  # Keep the token

            elif item == "NEWLINE":
                self.Terminals.append({"NEWLINE": "NEWLINE"})  # Ensure newline is stored properly

        if self.Terminals:
            self.currentTerminal = self.Terminals[0]
            self.keys = list(self.currentTerminal.keys())
            self.values = list(self.currentTerminal.values())
            self.currentkeys = self.keys[0]
            self.currentvalues = self.values[0]


    def next(self):
        self.position += 1
        if self.position >= len(self.Terminals):
            self.currentTerminal = '\0'
        else:
            self.currentTerminal = self.Terminals[self.position]
            self.keys = list(self.currentTerminal.keys())
            self.values = list(self.currentTerminal.values())
            self.currentkeys = self.keys[0]
            self.currentvalues = self.values[0]
            
            # Fix: Correctly check for "NEWLINE" and update lineCounter
            if self.currentkeys == "NEWLINE":  
                self.lineCounter += 1
                self.next()  # Move to the next token after newline


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

    # =====================================terminal_he Sterminal_RUCterminal_URE CODE============================================================#

    def terminal_program_start(self):  # <program>
        if self.currentkeys == '~':
            self.SemanticSequence.insert(len(self.SemanticSequence),{"<Prog_start+>": self.position})
            self.next()  # Expected: self.currentkeys = first set of <declaration> and <body>
            if self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat', 'plant', 're', 'force', 'watch',
                                    'defuse', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "inst", "flank", "strike", "tool", "chat", "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 1.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~"')  # put error in a list for viewing in GUI

    def terminal_program_end(self):  # <program>
        self.next()  # Expected: self.currentkeys = NULL
        if self.position == len(self.Terminals) and self.currentkeys == '~':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<Program->": self.position-1})
        else:
            print("SYNTAX ERROR 2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "NULL"')  # put error in a list for viewing in GUI

    def terminal_declaration(self):  # <declaration>
        if self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<declaration+>": self.position})
            self.terminal_data_type()
            self.terminal_id_or_array()
            self.terminal_declare_and_initialize()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<declaration->": self.position - 1})
            self.terminal_declaration()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank', 'strike',
                                    'chat', 'tool', 'bounce', '}', 'back'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                  'strike', 'chat', 'tool', 'bounce', '}', 'back'] or 'Identifier' in self.currentkeys:
            pass # NULL <declaration>
        else:
            print("SYNTAX ERROR 3.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "inst", "flank", "strike", "tool", "chat", "plant", "re", "force", "watch", "defuse", "~", "globe", "bounce", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI

    def terminal_data_type(self):  # <data type>
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<data type>": self.position})
        if self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat']:
            self.next()  # Expected: self.currentkeys = follow set <data type>
            if 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 4.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "inst", "flank", "strike", "tool", "chat"')  # put error in a list for viewing in GUI

    def terminal_id_or_array(self):  # <id or array>
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<id+>": self.position})
        if 'Identifier' in self.currentkeys:
            self.terminal_id()
            if self.currentkeys in ['=', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                    'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', ']', 'COMMA', ')', '+',
                                    '-', '*', '/', '%', 'abort', 'push', '}', '<', '>', '<=', '>=', '==', '!=', 'and',
                                    'or',
                                    '+=', '-=', '*=', '/=', '%='] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<id->": self.position-1})
            else:
                print("SYNTAX ERROR 5: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "]", "COMMA", ")", "+", "-", "*", "/", "%", "abort", "push", "}}", "<", ">", "<=", ">=", "==", "!=", "and", "or", "+=", "-=", "*=", "/=", "%=", "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 5.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier"')  # put error in a list for viewing in GUI

    def terminal_id(self):  # <id>
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
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "[", "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "]", "COMMA", ")", "+", "-", "*", "/", "%", "abort", "push", "}}", "<", ">", "<=", ">=", "==", "!=", "and", "or", "+=", "-=", "*=", "/=", "%=", "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 6.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier"')  # put error in a list for viewing in GUI


    def terminal_inst_or_id_value(self):  # <inst or id value>
        if self.currentkeys == 'INSTLIT':
            self.next()  # Expected: self.currentkeys = follow set <inst or id value>
            if self.currentkeys in [']', 'COMMA', ')']:
                pass
            else:
                print("SYNTAX ERROR 8: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "]", "COMMA", ")"')  # put error in a list for viewing in GUI
        elif "Identifier" in self.currentkeys:
            self.terminal_id_or_array()
            if self.currentkeys in [']', 'COMMA', ')']:
                pass
            else:
                print("SYNTAX ERROR 8.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "]", "COMMA", ")"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 8.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "INSTLIT", "Identifier"')  # put error in a list for viewing in GUI

    def terminal_declare_and_initialize(self):  # <declare and initialize>
        if self.currentkeys == '=':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<assignment operator>": self.position})
            self.next()  # Expected: self.currentkeys = first set <allowed value>
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value+>": self.position})
            self.terminal_allowed_value()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank', 'strike',
                                     'chat', 'tool', 'bounce', 'back', '}'] or 'Identifier' in self.currentkeys):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value->": self.position-1})
            else:
                print("SYNTAX ERROR 10: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI
        elif (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank', 'strike',
                                   'chat', 'tool', 'bounce', 'back', '}'] or 'Identifier' in self.currentkeys):
            pass
        else:
            print("SYNTAX ERROR 10.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "=", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI

    def terminal_allowed_value(self):  # <allowed value>
        if self.currentkeys == 'info':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<input+>": self.position})
            self.next()  # Expected: self.currentkeys = first set <parameter>
            if self.currentkeys == '(':
                self.next()  # Expected: self.currentkeys = first set <return value>
                self.terminal_return_value()
                if self.currentkeys == ')':
                    self.next()  # Expected: self.currentkeys = follow set <allowed value>
                    if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                             'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                             'push', '}'] or 'Identifier' in self.currentkeys):
                        self.SemanticSequence.insert(len(self.SemanticSequence), {"<input->": self.position-1})
                    else:
                        print("SYNTAX ERROR 11: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}", "Identifier"')  # put error in a list for viewing in GUI
                else:
                    print("SYNTAX ERROR 11.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI
            else:
                print("SYNTAX ERROR 11.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI
        elif self.currentkeys == '[':
            self.terminal_array_value()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys == 'CHATLIT':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<CHATLIT>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <allowed value>
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['neg', 'pos']:
            self.terminal_bully_value()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.5: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['(', 'FLANKLIT', 'INSTLIT', 'STRIKELIT'] or 'Identifier' in self.currentkeys:
            self.terminal_math_expression()
            if (self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst', 'flank',
                                     'strike', 'chat', 'tool', 'bounce', 'back', 'abort',
                                     'push', '}'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 11.6: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "}}",  "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 11.7: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI
        if "NEWLINE" in self.currentkeys:
            self.lineCounter += 1
            self.next()

    def terminal_return_value(self):
        if (self.currentkeys in ['[', 'CHATLIT', 'neg', 'pos', '(', 'INSTLIT', 'FLANKLIT',
                                 'STRIKELIT'] or 'Identifier' in self.currentkeys):
            self.terminal_data_value()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 12: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI
        elif self.currentkeys == ')':
            pass  # NULL <return value>
        else:
            print("SYNTAX ERROR 12.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier", ")"')  # put error in a list for viewing in GUI

    def terminal_data_value(self):
        if self.currentkeys in ['FLANKLIT', 'INSTLIT', 'STRIKELIT', 'CHATLIT', 'neg',
                                '(','pos'] or 'Identifier' in self.currentkeys:
            self.terminal_data_value_no_array()
            if self.currentkeys in [')', 'COMMA', ']']:
                pass
            else:
                print("SYNTAX ERROR 13: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "COMMA", "]"')  # put error in a list for viewing in GUI
        elif self.currentkeys == '[':
            self.terminal_array_value()
            if self.currentkeys in [')', 'COMMA', ']']:
                pass
            else:
                print("SYNTAX ERROR 13.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "COMMA", "]"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 13.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "FLANKLIT", "INSTLIT", "STRIKELIT", "CHATLIT", "neg", "pos", "Identifier", "["')  # put error in a list for viewing in GUI

    def terminal_data_value_no_array(self):
        if self.currentkeys in ['neg', 'pos']:
            self.terminal_bully_value()
            if (self.currentkeys in [')', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']):
                pass
            else:
                print("SYNTAX ERROR 14: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or"')  # put error in a list for viewing in GUI
        elif self.currentkeys == 'CHATLIT':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<CHATLIT+>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <data value no array>
            if (self.currentkeys in [')', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<CHATLIT->": self.position-1})
            else:
                print("SYNTAX ERROR 14.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['(', 'FLANKLIT', 'INSTLIT', 'STRIKELIT'] or 'Identifier' in self.currentkeys:
            self.terminal_math_expression()
            if (self.currentkeys in [')', 'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']):
                pass
            else:
                print("SYNTAX ERROR 14.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 14.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "neg", "pos", "CHATLIT", "(", "FLANKLIT", "INSTLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI

    def terminal_bully_value(self):
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
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "COMMA", "]", "==", "!=", "and", "or", "inst", "strike", "chat", "tool", "flank", "}}", "~", "plant", "re", "force", "watch", "defuse", "bounce", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI

        else:
            print("SYNTAX ERROR 15.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "neg", "pos"')  # put error in a list for viewing in GUI

    def terminal_math_expression(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression+>": self.position})
        if self.currentkeys == '(':
            self.next()  # Expected: self.currentkeys = first set <math expression>
            self.terminal_math_expression()
            if self.currentkeys == ')':
                self.next()  # Expected: self.currentkeys = first set <arithmetic tail> or follow set <math expression>
                self.terminal_arithmetic_tail()
                if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                         'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                         'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and', 'or',
                                         '}'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
                else:
                    print("SYNTAX ERROR 16: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
            else:
                print("SYNTAX ERROR 16.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI
        elif self.currentkeys in ['INSTLIT', 'FLANKLIT']:
            self.terminal_number_value()
            self.terminal_arithmetic_tail()
            if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                     'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                     'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                     'or', '}'] or 'Identifier' in self.currentkeys):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
            else:
                print("SYNTAX ERROR 16.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
        elif self.currentkeys == 'STRIKELIT':
            self.next()  # Expected: self.currentkeys = first set <arithmetic tail> or follow set <math expression>
            if self.currentkeys == '+':
                self.terminal_arithmetic_tail()
                if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                         'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                         'COMMA', ']', '==', '!=', 'and',
                                         'or', '}'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
                else:
                    print("SYNTAX ERROR 16.3: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
            elif (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                       'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                       'COMMA', ']', '==', '!=', 'and',
                                       'or', '}'] or 'Identifier' in self.currentkeys):
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
            else:
                print("SYNTAX ERROR 16.3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "==", "!=", "and", "or", "}}", "Identifier", "+"')  # put error in a list for viewing in GUI

        elif 'Identifier' in self.currentkeys:
            self.terminal_id_or_array()
            self.terminal_arithmetic_tail()
            if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                     'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                     'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                     'or', '}'] or 'Identifier' in self.currentkeys):
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<math expression->": self.position-1})
            else:
                print("SYNTAX ERROR 16.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}" "Identifier"')  # put error in a list for viewing in GUI
        else:
            print("SYNTAX ERROR 16.5: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI

    def terminal_arithmetic_tail(self):
        if self.currentkeys in ['+', '-', '*', '/', '%']:
            self.terminal_arithmetic()
            self.terminal_math_expression()
            if (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                     'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                     'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                     'or', '}'] or 'Identifier' in self.currentkeys):
                pass
            else:
                print("SYNTAX ERROR 17: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI
        elif (self.currentkeys in [')', 'plant', 're', 'force', 'watch', 'defuse', '~', 'globe',
                                   'inst', 'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push',
                                   'COMMA', ']', '<', '>', '<=', '>=', '==', '!=', 'and',
                                   'or', '}'] or 'Identifier' in self.currentkeys):
            pass  # NULL <arithmetic tail>
        else:
            print("SYNTAX ERROR 17.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "+", "-", "*", "/", "%", ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "}}", "Identifier"')  # put error in a list for viewing in GUI

    def terminal_arithmetic(self):
        if self.currentkeys in ['+', '-', '*', '/', '%']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<arithmetic>": self.position})
            self.next()  # Expected: self.currentkeys = follow set <arithmetic>
            if self.currentkeys in ['(', 'INSTLIT', 'FLANKLIT', 'STRIKELIT'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 17.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "(", "INSTLIT", "FLANKLIT", "STRIKELIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 17.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "+", "-", "*", "/", "%"')  # put error in a list for viewing in GUI:

    def terminal_number_value(self):
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
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "+", "-", "*", "/", "%", ")", "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", "COMMA", "]", "<", ">", "<=", ">=", "==", "!=", "and", "or", "Identifier", "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 18.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "FLANKLIT", "INSTLIT"')  # put error in a list for viewing in GUI:

    def terminal_array_value(self):
        if self.currentkeys == '[':
            self.next()  # Expected: self.currentkeys = first set <parameter values>
            self.terminal_array_parameter_values()
            if self.currentkeys == ']':
                self.next()  # Expected: self.currentkeys = follow set <array value>
                if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~', 'globe', 'inst',
                                        'flank', 'strike', 'chat', 'tool', 'bounce', 'back', 'abort', 'push', ')',
                                        'COMMA', ']', '}'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 19: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "globe", "inst", "flank", "strike", "chat", "tool", "bounce", "back", "abort", "push", ")", "COMMA", "]", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 19.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "]"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 19.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "["')  # put error in a list for viewing in GUI:

    def terminal_array_parameter_values(self):
        if self.currentkeys in ['[', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT',
                                'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.terminal_array_data_value()
            self.terminal_array_parameter_tail()
            if self.currentkeys == ']':
                pass
            else:
                print("SYNTAX ERROR 20: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "]"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 20.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "[", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT"')  # put error in a list for viewing in GUI:

    def terminal_array_data_value(self):
        if self.currentkeys in ['neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.terminal_data_value()
            if self.currentkeys in ['COMMA', ']']:
                pass
            else:
                print("SYNTAX ERROR 21: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", "]"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 21.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier", "["')  # put error in a list for viewing in GUI:

    def terminal_data_value_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.terminal_data_value_no_array()
            self.terminal_data_value_tail()
            if self.currentkeys == ']':
                pass
            else:
                print("SYNTAX ERROR 23: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "]"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ']':
            pass  # NULL <data value tail>
        else:
            print("SYNTAX ERROR 23.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", "]"')  # put error in a list for viewing in GUI:

    def terminal_array_parameter_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.terminal_array_data_value()
            self.terminal_array_parameter_tail()
            if self.currentkeys == ']':
                pass
            else:
                print("SYNTAX ERROR 24: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "]"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ']':
            pass  # NULL <array parameter tail>
        else:
            print("SYNTAX ERROR 24.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", "]"')  # put error in a list for viewing in GUI:

    def terminal_body(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse'] or 'Identifier' in self.currentkeys:
            self.terminal_statement()
            if self.currentkeys == '~':
                pass
            else:
                print("SYNTAX ERROR 25: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ~')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '~':
            pass  # NULL <body>
        else:
            print("SYNTAX ERROR 25.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_statement(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch'] or 'Identifier' in self.currentkeys:
            self.terminal_body_no_task()
            self.terminal_statement()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 26: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'defuse':
            self.terminal_function()
            self.terminal_statement()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 26.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <statement>
        else:
            print("SYNTAX ERROR 26.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "Identifier", "defuse", "~"')  # put error in a list for viewing in GUI:

    def terminal_body_no_task(self):
        if self.currentkeys in ['plant', 'force', 'watch'] or 'Identifier' in self.currentkeys:
            self.terminal_body_no_if_task()
            if self.currentkeys in ['bounce', 'plant', 're', 'force', 'watch', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 27: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "plant", "re", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 're':
            self.terminal_condition_statement()
            if self.currentkeys in ['bounce', 'plant', 're', 'force', 'watch', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 27.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "plant", "re", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['bounce', 'plant', 're', 'force', 'watch', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <body no defuse>
        else:
            print("SYNTAX ERROR 27.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "plant", "re", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_body_no_if_task(self):
        if self.currentkeys == 'plant' or 'Identifier' in self.currentkeys:
            if self.currentkeys == 'plant':
                self.terminal_body_no_if_loop_task()
                if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                        '}', '~'] or 'Identifier' in self.currentkeys:
                    pass
            elif 'Identifier' in self.currentkeys:
                self.next()  # Expected: self.currentkeys = '(' if in <function call statement>
                if self.currentkeys == '(':
                    self.prev()
                    self.terminal_function_call_statement()
                    if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                            '}', '~'] or 'Identifier' in self.currentkeys:
                        pass
                    else:
                        print("SYNTAX ERROR 29: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
                else:
                    self.prev()  # if Identifier but not for <function call statement>
                    self.terminal_body_no_if_loop_task()
                    if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                            '}', '~'] or 'Identifier' in self.currentkeys:
                        pass
                    else:
                        print("SYNTAX ERROR 29.1: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:

            else:
                print("SYNTAX ERROR 28: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch']:
            self.terminal_loop_statement()
            if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 28.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <body no if-defuse>
        else:
            print("SYNTAX ERROR 28.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_body_no_if_loop_task(self):
        if 'Identifier' in self.currentkeys:
            self.terminal_initialization_statement()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 29.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'plant':
            self.terminal_output_statement()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 29.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <body no if-loop-defuse>
        else:
            print("SYNTAX ERROR 29.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_call_statement(self):
        if 'Identifier' in self.currentkeys:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function call statement+>": self.position})
            self.terminal_id()
            self.terminal_parameter()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function call statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 29.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 29.5: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_parameter(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<parameter+>": self.position})
        if self.currentkeys == '(':
            self.next()
            self.terminal_parameter_values()
            if self.currentkeys == ')':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<parameter->": self.position})
                self.next()
                if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                        'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 30: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 30.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 30.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI:

    def terminal_parameter_values(self):
        if self.currentkeys in ['FLANKLIT', 'INSTLIT', 'STRIKELIT', 'CHATLIT', 'neg', 'pos',
                                '(','['] or 'Identifier' in self.currentkeys:
            self.terminal_data_value()
            self.terminal_parameter_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 31: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <parameter values>
        else:
            print("SYNTAX ERROR 31.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "FLANKLIT", "INSTLIT", "STRIKELIT", "CHATLIT", "neg", "pos", "[", "Identifier", ")"')  # put error in a list for viewing in GUI:

    def terminal_parameter_tail(self):
        if self.currentkeys == 'COMMA':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<comma>": self.position})
            self.next()
            self.terminal_parameter_values()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 32: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass
        else:
            print("SYNTAX ERROR 32.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", ")"')  # put error in a list for viewing in GUI:

    def terminal_output_statement(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<output statement+>": self.position})
        if self.currentkeys == 'plant':
            self.next()
            self.terminal_parameter()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<output statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 33: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 33.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant"')  # put error in a list for viewing in GUI:

    def terminal_initialization_statement(self):
        if 'Identifier' in self.currentkeys:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<initialization statement+>": self.position})
            self.terminal_id_or_array()
            self.terminal_assignment_operator()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value+>": self.position})
            self.terminal_allowed_value_initialize()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push', '~',
                                    'plant', 'defuse', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<allowed value->": self.position-1})
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<initialization statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 34: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "~", "plant", "defuse", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 34.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_assignment_operator(self):
        if self.currentkeys in ['=', '+=', '-=', '*=', '/=', '%=']:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<assignment operator>": self.position})
            self.next()
            if self.currentkeys in ['info', '[', 'CHATLIT', 'neg', 'pos', '(', 'INSTLIT', 'STRIKELIT',
                                    'FLANKLIT'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 35: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "STRIKELIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 35.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "=", "+=", "-=", "*=", "/=", "%="')  # put error in a list for viewing in GUI:

    def terminal_allowed_value_initialize(self):
        if 'Identifier' in self.currentkeys:
            self.next()  # Expected: self.currentkeys = '(' if in <function call statement>
            if self.currentkeys == '(':
                self.prev()
                self.terminal_function_call_statement()
            else:
                self.prev()  # if Identifier but not for <function call statement>
                if 'Identifier' in self.currentkeys:
                    self.terminal_allowed_value()
                    if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push',
                                            'plant', 'defuse', '}', '~'] or 'Identifier' in self.currentkeys:
                        pass
                    else:
                        print("SYNTAX ERROR 36: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "plant", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['info', '[', 'CHATLIT', 'neg', 'pos', '(', 'INSTLIT', 'FLANKLIT', 'STRIKELIT']:
            self.terminal_allowed_value()
            if self.currentkeys in ['re', 'force', 'watch', 'bounce', 'back', 'abort', 'push',
                                    'plant', 'defuse', '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 36.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "abort", "push", "plant", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 36.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier", "info", "[", "CHATLIT", "neg", "pos", "(", "INSTLIT", "FLANKLIT", "STRIKELIT"')  # put error in a list for viewing in GUI:
        if "NEWLINE" in self.currentkeys:
            self.lineCounter += 1
            self.next()

    def terminal_loop_statement(self):
        if self.currentkeys == 'force':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<force loop+>": self.position})
            self.terminal_for()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body+>": self.position})
            self.terminal_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body->": self.position - 1})
            if self.currentkeys in ['~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce', 'back', '}',
                                    'abort', 'push'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<force loop->": self.position-1})
            else:
                print("SYNTAX ERROR 37: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~", "plant", "re", "force", "watch", "defuse", "bounce", "back", "}}", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'watch':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<watch loop+>": self.position})
            self.terminal_watch()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body+>": self.position})
            self.terminal_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop body->": self.position - 1})
            if self.currentkeys in ['~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce', 'back', '}',
                                    'abort', 'push'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<watch loop->": self.position - 1})
            else:
                print("SYNTAX ERROR 37.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~", "plant", "re", "force", "watch", "defuse", "bounce", "back", "}}", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 37.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch"')  # put error in a list for viewing in GUI:

    def terminal_for(self):
        if self.currentkeys == 'force':
            self.next()
            self.terminal_id()
            if self.currentkeys == 'in':
                self.next()
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<perim+>": self.position})
                if self.currentkeys == 'perim':
                    self.next()
                    if self.currentkeys == '(':
                        self.next()
                        self.terminal_inst_or_id_value()
                        self.terminal_range()
                        if self.currentkeys == ')':
                            self.SemanticSequence.insert(len(self.SemanticSequence), {"<perim->": self.position})
                            self.next()
                            if self.currentkeys == '{':
                                pass
                            else:
                                print("SYNTAX ERROR 38: Unexpected", self.currentvalues, self.lineCounter)
                                self.SyntaxErrors.append(
                                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:
                        else:
                            print("SYNTAX ERROR 38.1: Unexpected", self.currentvalues, self.lineCounter)
                            self.SyntaxErrors.append(
                                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
                    else:
                        print("SYNTAX ERROR 38.2: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 38.3: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "perim"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 38.4: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "in"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 38.5: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force"')  # put error in a list for viewing in GUI:

    def terminal_range(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.terminal_inst_or_id_value()
            self.terminal_range_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 39: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <perim>
        else:
            print("SYNTAX ERROR 39.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", ")"')  # put error in a list for viewing in GUI:

    def terminal_range_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.terminal_inst_or_id_value()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 40: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <perim tail>
        else:
            print("SYNTAX ERROR 40.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", ")"')  # put error in a list for viewing in GUI:

    def terminal_loop_body(self):
        if self.currentkeys == '{':
            self.next()
            self.terminal_loop_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                        'defuse', '}', '~', 'reload', 'load'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 41: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "bounce", "abort", "push", "plant", "force", "watch", "defuse", "}}", "~", "reload", "load", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 41.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 41.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:

    def terminal_loop_content(self):
        if self.currentkeys in ['force', 'watch', 'plant', 're', 'bounce', 'abort',
                                'push'] or 'Identifier' in self.currentkeys:
            self.terminal_body_no_if_task()
            self.terminal_loop_condition()
            self.terminal_control_flow()
            self.terminal_loop_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 42: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass
        else:
            print("SYNTAX ERROR 42.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch", "plant", "re", "bounce", "abort", "push", "Identifier", "}}"')  # put error in a list for viewing in GUI:

    def terminal_loop_condition(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop condition+>": self.position})
            self.terminal_loop_if()
            self.terminal_loop_elif()
            self.terminal_loop_else()
            if self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop condition->": self.position-1})
            else:
                print("SYNTAX ERROR 43: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "bounce", "abort", "push", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['re', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <loop condition>
        else:
            print("SYNTAX ERROR 43.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "bounce", "abort", "push", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_loop_if(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop if+>": self.position})
            self.terminal_if()
            self.terminal_loop_body()
            if self.currentkeys in ['reload', 'load', 're', 'bounce', 'abort', 'push', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop if->": self.position-1})
            else:
                print("SYNTAX ERROR 44: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "re", "bounce", "abort", "push", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 44.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re"')  # put error in a list for viewing in GUI:

    def terminal_if(self):
        if self.currentkeys == 're':
            self.next()
            self.terminal_condition()
            if self.currentkeys == '{':
                pass
            else:
                print("SYNTAX ERROR 45: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 45.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re"')  # put error in a list for viewing in GUI:

    def terminal_condition(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition+>": self.position})
        if self.currentkeys == '(':
            self.next()
            self.terminal_logical_expression()
            if self.currentkeys == ')':
                self.next()
                if self.currentkeys == '{':
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition->": self.position-1})
                else:
                    print("SYNTAX ERROR 46: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 46.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 46.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI:

    def terminal_logical_expression(self):
        if self.currentkeys == '(':
            self.next()
            self.terminal_logical_expression()
            if self.currentkeys == ')':
                self.next()
                self.terminal_logic_or_relational_tail()
                if self.currentkeys == ')':
                    pass
                else:
                    print("SYNTAX ERROR 47: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 47.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'not':
            self.terminal_not_logic()
            self.terminal_logic_or_relational_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 47.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT',
                                  'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.terminal_relational_expression()
            self.terminal_logic_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 47.3: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 47.4: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "(", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_logic_tail(self):
        if self.currentkeys in ['and', 'or']:
            self.terminal_logical_operator()
            self.terminal_logical_expression()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 48: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <logic tail>
        else:
            print("SYNTAX ERROR 48.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "and", "or", ")"')  # put error in a list for viewing in GUI:

    def terminal_logical_operator(self):
        if self.currentkeys in ['and', 'or']:
            self.next()
            if self.currentkeys in ['(', 'not', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT',
                                    ] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 49: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "(", "not", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 49.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "and", "or"')  # put error in a list for viewing in GUI:

    def terminal_not_logic(self):
        if self.currentkeys == 'not':
            self.next()
            if self.currentkeys == '(':
                self.next()
                self.terminal_logical_expression()
                if self.currentkeys == ')':
                    self.next()
                    if self.currentkeys in ['and', 'or', '==', '!=', ')']:
                        pass
                    else:
                        print("SYNTAX ERROR 50: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "and", "or", "==", "!="')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 50.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 50.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 50.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "not"')  # put error in a list for viewing in GUI:

    def terminal_logic_or_relational_tail(self):
        if self.currentkeys in ['and', 'or']:
            self.terminal_logic_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 51: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['<', '>', '<=', '>=', '==', '!=']:
            self.terminal_relational_tail()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 51.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass
        elif self.currentkeys in ['(', 'not', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT',
                                    ] or 'Identifier' in self.currentkeys:
            self.terminal_logical_expression() #NOterminal_SURE PA HERE EXPERIMENterminal_ LANG
        else:
            print("SYNTAX ERROR 51.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "and", "or", "==", "!=", ")"')  # put error in a list for viewing in GUI:

    def terminal_relational_expression(self):
        if self.currentkeys == '(':
            self.next()
            self.terminal_logic_or_relational_tail()
            if self.currentkeys == ')':
                self.next()
                if self.currentkeys in [')', 'and', 'or']:
                    pass
                else:
                    print("SYNTAX ERROR 52: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "and", "or"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 52.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT',
                                  'FLANKLIT'] or 'Identifier' in self.currentkeys:
            self.terminal_data_value_no_array()
            self.terminal_logic_or_relational_tail()
            if self.currentkeys in [')', 'and', 'or']:
                pass
            else:
                print("SYNTAX ERROR 52.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "and", "or"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 52.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "(", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_relational_tail(self):
        if self.currentkeys in ['<', '>', '<=', '>=', '==', '!=']:
            self.terminal_relational_operator()
            self.terminal_relational_expression()
            if self.currentkeys in [')', 'and', 'or']:
                pass
            else:
                print("SYNTAX ERROR 53: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")", "and", "or"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in [')', 'and', 'or']:
            pass  # NULL <relational tail>
        else:
            print("SYNTAX ERROR 53.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "<", ">", "<=", ">=", "==", "!=", ")", "and", "or"')  # put error in a list for viewing in GUI:

    def terminal_relational_operator(self):
        if self.currentkeys in ['<', '>', '<=', '>=', '==', '!=']:
            self.next()
            if self.currentkeys in ['(', 'not', 'neg', 'pos', 'CHATLIT', 'STRIKELIT', 'INSTLIT', 'FLANKLIT',
                                    ] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 54: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "(", "not", "neg", "pos", "CHATLIT", "STRIKELIT", "INSTLIT", "FLANKLIT", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 54.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "<", ">", "<=", ">=", "==", "!="')  # put error in a list for viewing in GUI:

    def terminal_loop_elif(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop elif+>": self.position})
            self.terminal_elif()
            self.terminal_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop elif->": self.position - 1})
            self.terminal_loop_elif()
            if self.currentkeys in ['load', 'bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 55: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <loop elif>
        else:
            print("SYNTAX ERROR 55.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_elif(self):
        if self.currentkeys == 'reload':
            self.next()
            self.terminal_condition()
            if self.currentkeys == '{':
                pass
            else:
                print("SYNTAX ERROR 56: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 56.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload"')  # put error in a list for viewing in GUI:

    def terminal_loop_else(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop else+>": self.position})
            self.next()
            self.terminal_loop_body()
            if self.currentkeys in ['bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<loop else->": self.position-1})
            else:
                print("SYNTAX ERROR 57: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['bounce', 'abort', 'push', 're', 'plant', 'force', 'watch',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <loop else>
        else:
            print("SYNTAX ERROR 57.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "abort", "push", "re", "plant", "force", "watch", "}}", "load", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_control_flow(self):
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
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "bounce", "abort", "push", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'abort', 'push',
                                  '}', 'back'] or 'Identifier' in self.currentkeys:
            pass  # NULL <control flow>
        else:
            print("SYNTAX ERROR 58.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "bounce", "abort", "push", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_watch(self):
        if self.currentkeys == 'watch':
            self.next()
            self.terminal_condition()
            if self.currentkeys == '{':
                pass
            else:
                print("SYNTAX ERROR 59: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 59.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "watch"')  # put error in a list for viewing in GUI:

    def terminal_condition_statement(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition statement+>": self.position})
            self.terminal_if_with_body()
            self.terminal_elif_with_body()
            self.terminal_else_with_body()
            if self.currentkeys in ['~', 'plant', 're', 'force', 'watch', 'defuse', 'bounce',
                                    '}', 'back', 'abort', 'push'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition statement->": self.position - 1})
            else:
                print("SYNTAX ERROR 60: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~", "plant", "re", "force", "watch", "defuse", "bounce", "}}", "back", "abort", "push", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 60.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re"')  # put error in a list for viewing in GUI:

    def terminal_if_with_body(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<if with body+>": self.position})
        if self.currentkeys == 're':
            self.terminal_if()
            self.terminal_condition_body()
            if self.currentkeys in ['reload', 'load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<if with body->": self.position - 1})
            else:
                print("SYNTAX ERROR 61: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 61.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re"')  # put error in a list for viewing in GUI:

    def terminal_condition_body(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition body+>": self.position})
        if self.currentkeys == '{':
            self.next()
            self.terminal_condition_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['reload', 'load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                        '}', '~'] or 'Identifier' in self.currentkeys:
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<condition body->": self.position -1})
                else:
                    print("SYNTAX ERROR 62: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 62.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 62.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:

    def terminal_condition_content(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce'] or 'Identifier' in self.currentkeys:
            self.terminal_body_no_task()
            self.terminal_pass()
            self.terminal_condition_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 63: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass  # NULL <condition content>
        else:
            print("SYNTAX ERROR 63.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "bounce", "Identifier", "}}"')  # put error in a list for viewing in GUI:

    def terminal_pass(self):
        if self.currentkeys == 'bounce':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<pass>": self.position})
            self.next()
            if self.currentkeys in ['plant', 're', 'watch', 'force', 'bounce', 'back',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 64: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "watch", "force", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'watch', 'force', 'bounce',
                                  'back', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <pass>
        else:
            print("SYNTAX ERROR 64.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "plant", "re", "watch", "force", "bounce", "back", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_elif_with_body(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<elif with body+>": self.position})
            self.terminal_elif()
            self.terminal_condition_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<elif with body->": self.position - 1})
            self.terminal_elif_with_body()
            if self.currentkeys in ['load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 65: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <elif with body>
        else:
            print("SYNTAX ERROR 65.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_else_with_body(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<else with body+>": self.position})
            self.next()
            self.terminal_condition_body()
            if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                    '}', '~'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<else with body->": self.position-1})
            else:
                print("SYNTAX ERROR 66: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                  '}', '~'] or 'Identifier' in self.currentkeys:
            pass  # NULL <else with body>
        else:
            print("SYNTAX ERROR 66.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "plant", "re", "force", "watch", "bounce", "defuse", "}}", "~", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<function+>": self.position})
        if self.currentkeys == 'defuse':
            self.next()
            self.terminal_id()
            if self.currentkeys == '(':
                self.next()
                self.terminal_function_parameter()
                if self.currentkeys == ')':
                    self.next()
                    self.terminal_function_body()
                    if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'defuse',
                                            '~'] or 'Identifier' in self.currentkeys:
                        self.SemanticSequence.insert(len(self.SemanticSequence), {"<function->": self.position-1})
                    else:
                        print("SYNTAX ERROR 67: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "bounce", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 67.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 67.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 67.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "defuse"')  # put error in a list for viewing in GUI:

    def terminal_function_parameter(self):
        if 'Identifier' in self.currentkeys:
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function parameter+>": self.position})
            self.terminal_id()
            self.terminal_id_tail()
            if self.currentkeys == ')':
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function parameter->": self.position-1})
            else:
                print("SYNTAX ERROR 68: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <function parameter>
        else:
            print("SYNTAX ERROR 68.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "Identifier", ")"')  # put error in a list for viewing in GUI:

    def terminal_id_tail(self):
        if self.currentkeys == 'COMMA':
            self.next()
            self.terminal_function_parameter()
            if self.currentkeys == ')':
                pass
            else:
                print("SYNTAX ERROR 69: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == ')':
            pass  # NULL <id tail>
        else:
            print("SYNTAX ERROR 69.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "COMMA", ")"')  # put error in a list for viewing in GUI:

    def terminal_function_body(self):
        if self.currentkeys == '{':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function body+>": self.position})
            self.next()
            self.terminal_function_declaration()
            self.terminal_function_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse',
                                        '~'] or 'Identifier' in self.currentkeys:
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<function body->": self.position-1})
                else:
                    print("SYNTAX ERROR 70: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "defuse", "~", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 70.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:

    def terminal_function_declaration(self):
        if self.currentkeys == 'globe':
            self.terminal_universal()
            self.terminal_function_declaration()
            if self.currentkeys in ['plant', 're', 'force', 'watch', '}', 'bounce',
                                    'back'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 71: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['inst', 'flank', 'strike', 'chat', 'tool']:
            self.terminal_declaration()
            self.terminal_function_declaration()
            if self.currentkeys in ['plant', 're', 'force', 'watch', '}', 'back'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 71.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "plant", "re", "force", "watch", "}}", "back", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['plant', 're', 'force', 'watch', '}', 'bounce',
                                  'back'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function declaration>
        else:
            print("SYNTAX ERROR 71.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "globe", "inst", "flank", "strike", "chat", "tool", "plant", "re", "force", "watch", "}}" , "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_universal(self):
        if self.currentkeys == 'globe':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<globe+>": self.position})
            self.next()
            self.terminal_data_type()
            self.terminal_id_or_array()
            if self.currentkeys in ['globe', 'inst', 'flank', 'strike', 'chat', 'tool', 'plant', 're',
                                    'force', 'watch', '}', 'bounce'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<globe->": self.position})
            else:
                print("SYNTAX ERROR 72: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "globe", "inst", "flank", "strike", "chat", "tool", "plant", "re", "force", "watch", "}}", "bounce", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['globe', 'inst', 'flank', 'strike', 'chat', 'tool', 'plant', 're',
                                  'force', 'watch', '}', 'bounce'] or 'Identifier' in self.currentkeys:
            pass  # NULL <globe>
        else:
            print("SYNTAX ERROR 72.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "globe", "inst", "flank", "strike", "chat", "tool", "plant", "re", "force", "watch", "}}", "bounce", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_content(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce',
                                'back'] or 'Identifier' in self.currentkeys:
            self.terminal_body_no_if_loop_task()
            self.terminal_function_condition()
            self.terminal_function_loop()
            self.terminal_pass()
            self.terminal_return()
            self.terminal_function_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 73: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass  # NULL <function content>
        else:
            print("SYNTAX ERROR 73.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "plant", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_condition(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition+>": self.position})
            self.terminal_function_if()
            self.terminal_function_elif()
            self.terminal_function_else()
            if self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition->": self.position})
            else:
                print("SYNTAX ERROR 74: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "plant", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        if self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function condition>
        else:
            print("SYNTAX ERROR 74.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "back", "plant", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_if(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function if+>": self.position})
            self.terminal_if()
            self.terminal_function_condition_body()
            if self.currentkeys in ['reload', 'load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function if->": self.position-1})
            else:
                print("SYNTAX ERROR 75: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 75.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re"')  # put error in a list for viewing in GUI:

    def terminal_function_condition_body(self):
        self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition body+>": self.position})
        if self.currentkeys == '{':
            self.next()
            self.terminal_function_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['reload', 'load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                        '}'] or 'Identifier' in self.currentkeys:
                    self.SemanticSequence.insert(len(self.SemanticSequence), {"<function condition body->": self.position - 1})
                else:
                    print("SYNTAX ERROR 76: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 76.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 76.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:

    def terminal_function_elif(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function elif+>": self.position})
            self.terminal_elif()
            self.terminal_function_condition_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function elif->": self.position - 1})
            self.terminal_function_elif()
            if self.currentkeys in ['load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 77: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'force', 'watch', 'bounce', 'back', 'plant', 're',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function elif>
        else:
            print("SYNTAX ERROR 77.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", ')  # put error in a list for viewing in GUI:

    def terminal_function_else(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function else+>": self.position})
            self.next()
            self.terminal_function_condition_body()
            if self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                    '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function else->": self.position - 1})
            else:
                print("SYNTAX ERROR 78: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'back', 'plant', 're',
                                  '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function else>
        else:
            print("SYNTAX ERROR 78.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "force", "watch", "bounce", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_loop(self):
        if self.currentkeys == 'force':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function force loop+>": self.position})
            self.terminal_for()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body+>": self.position})
            self.terminal_function_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body->": self.position - 1})
            if self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force', 'watch',
                                    're'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function force loop->": self.position - 1})
            else:
                print("SYNTAX ERROR 79: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == 'watch':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function watch loop+>": self.position})
            self.terminal_watch()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body+>": self.position})
            self.terminal_function_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop body->": self.position - 1})
            if self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force', 'watch',
                                    're'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function watch loop->": self.position - 1})
            else:
                print("SYNTAX ERROR 79.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force', 'watch',
                                  're'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop>
        else:
            print("SYNTAX ERROR 79.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch", "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_loop_body(self):
        if self.currentkeys == '{':
            self.next()
            self.terminal_function_loop_content()
            if self.currentkeys == '}':
                self.next()
                if self.currentkeys in ['bounce', 'back', 'plant', '}', 'abort', 'push', 'force',
                                        'watch', 're', 'reload', 'load'] or 'Identifier' in self.currentkeys:
                    pass
                else:
                    print("SYNTAX ERROR 80: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "bounce", "back", "plant", "}}", "abort", "push", "force", "watch", "re", "reload", "load", "Identifier"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 80.1: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 80.2: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "{{"')  # put error in a list for viewing in GUI:

    def terminal_function_loop_content(self):
        if self.currentkeys in ['plant', 're', 'force', 'watch', 'bounce', 'abort', 'push',
                                'back'] or 'Identifier' in self.currentkeys:
            self.terminal_body_no_if_loop_task()
            self.terminal_function_loop_condition()
            self.terminal_function_loop()
            self.terminal_control_flow()
            self.terminal_return()
            self.terminal_function_loop_content()
            if self.currentkeys == '}':
                pass
            else:
                print("SYNTAX ERROR 81: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "}}"')  # put error in a list for viewing in GUI:
        elif self.currentkeys == '}':
            pass  # NULL <function loop content>
        else:
            print("SYNTAX ERROR 81.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_loop_condition(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop condition+>": self.position})
            self.terminal_function_loop_if()
            self.terminal_function_loop_elif()
            self.terminal_function_loop_else()
            if self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop condition->": self.position-1})
            else:
                print("SYNTAX ERROR 82: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop condition>
        else:
            print("SYNTAX ERROR 82.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_loop_if(self):
        if self.currentkeys == 're':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop if+>": self.position})
            self.terminal_if()
            self.terminal_function_loop_body()
            if self.currentkeys in ['reload', 'load', 'force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop if->": self.position-1})
            else:
                print("SYNTAX ERROR 83: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        else:
            print("SYNTAX ERROR 83.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "re"')  # put error in a list for viewing in GUI:

    def terminal_function_loop_elif(self):
        if self.currentkeys == 'reload':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop elif+>": self.position})
            self.terminal_elif()
            self.terminal_function_loop_body()
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop elif->": self.position - 1})
            self.terminal_function_loop_elif()
            if self.currentkeys in ['load', 'force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                pass
            else:
                print("SYNTAX ERROR 84: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['load', 'force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop elif>
        else:
            print("SYNTAX ERROR 84.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "reload", "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_function_loop_else(self):
        if self.currentkeys == 'load':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop else+>": self.position})
            self.next()
            self.terminal_function_loop_body()
            if self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                    're', '}'] or 'Identifier' in self.currentkeys:
                self.SemanticSequence.insert(len(self.SemanticSequence), {"<function loop else->": self.position-1})
            else:
                print("SYNTAX ERROR 85: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <function loop else>
        else:
            print("SYNTAX ERROR 85.1: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "load", "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    def terminal_return(self):
        if self.currentkeys == 'back':
            self.SemanticSequence.insert(len(self.SemanticSequence), {"<return+>": self.position})
            self.next()
            if self.currentkeys == '(':
                self.next()
                self.terminal_return_value()
                if self.currentkeys == ')':
                    self.next()
                    if self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                            're', '}'] or 'Identifier' in self.currentkeys:
                        self.SemanticSequence.insert(len(self.SemanticSequence), {"<return->": self.position-1})
                    else:
                        print("SYNTAX ERROR 86: Unexpected", self.currentvalues, self.lineCounter)
                        self.SyntaxErrors.append(
                            f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "force", "watch", "bounce", "abort", "push", "back", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:
                else:
                    print("SYNTAX ERROR 86.1: Unexpected", self.currentvalues, self.lineCounter)
                    self.SyntaxErrors.append(
                        f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: ")"')  # put error in a list for viewing in GUI:
            else:
                print("SYNTAX ERROR 86.2: Unexpected", self.currentvalues, self.lineCounter)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "("')  # put error in a list for viewing in GUI:
        elif self.currentkeys in ['force', 'watch', 'bounce', 'abort', 'push', 'back', 'plant',
                                  're', '}'] or 'Identifier' in self.currentkeys:
            pass  # NULL <return>
        else:
            print("SYNTAX ERROR 86.3: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "back", "force", "watch", "bounce", "abort", "push", "plant", "re", "}}", "Identifier"')  # put error in a list for viewing in GUI:

    # =====================================terminal_he Sterminal_RUCterminal_URE CODE============================================================#

    def GetNextTerminal(self):  # <program> and <program content>
        terminator = 0
        ctr = 0
        if self.currentkeys == '"NEWLINE"':
            print("SYNTAX ERROR 87: Unexpected", self.currentvalues, self.lineCounter)
            self.SyntaxErrors.append(
                f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}" \n\nExpected: "~"')  # put error in a list for viewing in GUI #
        if self.currentkeys == '~':
            terminator += 1
        self.terminal_program_start()
        while self.position < len(self.Terminals) and ctr != len(self.Terminals) and terminator != 0:
            if self.currentkeys == '~':
                break
            elif self.currentkeys in ['inst', 'flank', 'strike', 'tool', 'chat']:
                self.terminal_declaration()
            elif self.currentkeys in ['plant', 're', 'force', 'watch', 'defuse'] or "Identifier" in self.currentkeys:
                self.terminal_body()
            else:
                print("SYNTAX ERROR X:", self.currentvalues)
                self.SyntaxErrors.append(
                    f'LINE #{self.lineCounter} : Unexpected: "{self.currentvalues}"')  # put error in a list for viewing in GUI
                break
            ctr += 1
        self.terminal_program_end()
        if len(self.SyntaxErrors) == 0:
            print("SYNTAX COMPILE SUCCESSFULLY", self.lineCounter)
            self.SyntaxErrors.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")  # put in a list for viewing in GUI
            self.SyntaxErrors.append(" ")  # put in a list for viewing in GUI

            self.SyntaxErrors.append("------------------------------------------------------------------------SYNTAX COMPILE SUCCESSFULLY--------------------------------------------------------------------------------")  # put in a list for viewing in GUI
            self.SyntaxErrors.append(" ")  # put in a list for viewing in GUI
            self.SyntaxErrors.append("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")  # put in a list for viewing in GUI

            print(self.SemanticSequence)
        else:
            print("ERRORS FOUND", self.lineCounter)
        return self.SyntaxErrors

