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
