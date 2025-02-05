
currentChar = ""  # Current character being processed
errorChar = []  # Define error characters
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't','u', 'v', 'w', 'x', 'y', 'z']
num = list('0123456789')  # Convert string to list of characters
delim1 = ['{']
delim2 = ['~']
delim3 = [' ']
delim4 = ['(']
delim5 = [' ', '(', ')', ';']
delim6 = [' ', '^', ';', '}', '\n', '\0']  + num + alpha
delim7 = ['=', ' ']
delim8 = [' ', '=', ')', '\0', '!']
delim9 = [' ', 'num', "'", '(', '_', 'alpha', '"']
delim10 = ['num', "'", '"', 'alpha', '[', ']'] + num + alpha
delim11 = [' ', '\0', '\n']
delim12 = [';']  # Semicolon delimiter
delim13 = [' ', '"', '(', "'"] + num + alpha
delim14 = [' ', 'num', '(', '_']
delim15 = [' ', 'num', '(', '_', '"']
delim16 = [' ', '\0', '\n', '~', '$', '`']
delim17 = [' ', '\0', '"', '(', "'", ')'] + num + alpha
delim18 = [' ', '\0', '\n', '+', '-', '*', '/', '%', '!', '=', '<', '>', ',', '}', ')', '{', ';'] + alpha
delim19 = ['=', '*', ')', ' ', '\0', '+', ']', '%', ',', '}', '/', '<', '[', '>', '\n', '!', '-', ';']
delim20 = [' ', '+', '=', '!', ',', '^', ')', '}', '\n', '\0', ']', ';', '$', '`']
delim21 = ['\0', '}', ' ', '\n', '^']
delim22 = ['^', ']', '%', '>', '+', '}', '\0', ',', '<', '/', '=', '*', ' ', '!', '-', ';', ')', '\n', '\0', '$', '`']
delim23 = [' ', '\0', '\n', '"', '(', '-', "'", ')', '#'] + num + alpha
delim24 = [')', ']', '+', '=', '}', '*', '\0', ',', '/', '[', '<', '>', '-', ' ', '%', '(', '\n', '!']
delim25 = [' ', '=', '(', ')', '\'', '"', '+', '-', '*', '/', '%', '>', '<', '!', '^', 'alpha', 'num', '[', ']', '$', '`'] 
delim26 = [',', '+', '-', '*', '/', '%', '=', '<', '>', '!', '^', '\n', '\0', '}', ']', ' ', ',', ')']
delim27 = [' ', '\n', '\0', '}']
delim28 = [' ', ';', '\n', '\0']
zero = '0'
errorChar = ['!', '@', '%', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ':', "'", '"', ',', '.', '<', '>', '/', '?', '~']
unknownCharacters = ['@',  '&', '_', '?', '|', ';', '-', '|', '\\', ':', ';', 'e', 'h', 'j', 'k', 'm', 'q', 'u', 'v', 'x', 'y', 'z', '.', "'"] + [chr(ord('A') + i) for i in range(26)]
reservedkeywords = ["abort", "and", "back", "bounce", "chat", "defuse", "flank", "force", "in", "inst", "info","load", "neg", "not", "or", "perim", "plant", "push", "re", "reload", "strike", "tool", "watch"]

class DEDOSLexicalAnalyzer:
    def __init__(self, lexeme):
        self.lexeme = lexeme
        self.currentChar = lexeme[0] if lexeme else ''
        self.position = 0
        self.value_ = None
        self.type_ = None
        self.fullResult = None
        self.tokens = []
        self.counter = 0
        self.tokensForUnknown = []
        self.lineCounter = 1


    def next(self): #character next function
        self.position += 1
        if self.position > len(self.lexeme) - 1:
            self.currentChar = '\0'
        else:
            self.currentChar = self.lexeme[self.position]

    def prev(self): #character previous function
        self.position -= 1
        if self.position > len(self.lexeme) - 1:
            self.currentChar = '\0'
        else:
            self.currentChar = self.lexeme[self.position]
    
    def SpaceToken(self):
        result = '"'
        result += self.currentChar
        self.next()
        if self.currentChar != " ":
            pass
        return "SPACE_TOKEN", "SPACE"

    def digits(self):
        result = ""
        instctr = 0
        flankctr = 0

        while True:
            if self.currentChar == '0':
                result += self.currentChar
                instctr += 1
                self.next()
            elif self.currentChar in "123456789":
                result += self.currentChar
                instctr += 1
                self.next()
                while True:
                    if instctr > 9 or flankctr > 9:
                        return "UNKNOWN LEXEME", result
                    if self.currentChar in "0123456789":
                        result += self.currentChar
                        instctr += 1
                        self.next()
                    elif self.currentChar == '.':
                        result += self.currentChar
                        self.next()
                        while True:
                            if instctr > 6 or flankctr > 9:
                                return "UNKNOWN LEXEME", result
                            if self.currentChar in "0123456789":
                                result += self.currentChar
                                flankctr += 1
                                print(flankctr)
                                self.next()
                            elif self.currentChar in delim22:
                                # When a delimiter is found, return FLANKLIT token along with the value
                                return "FLANKLIT", result
                            elif self.currentChar in [x for x in set(errorChar) if x not in set(delim22)]:
                                return "UNKNOWN LEXEME", result
                            else:
                                break
                        break
                    elif self.currentChar in delim22:
                        # When a delimiter is found, return INSTLIT token along with the value
                        return "INSTLIT", result
                    elif self.currentChar in [x for x in set(errorChar) if x not in set(delim22)]:
                        return "UNKNOWN LEXEME", result
                    else:
                        break
            elif self.currentChar == '.':
                result += self.currentChar
                self.next()
                if self.currentChar == ' ' or self.currentChar == '\0' or self.currentChar == '\n':
                    return "UNKNOWN LEXEME", result
                while True:
                    if instctr > 9 or flankctr > 9:
                        return "UNKNOWN LEXEME", result
                    if self.currentChar in "0123456789":
                        result += self.currentChar
                        flankctr += 1
                        self.next()
                    elif self.currentChar in delim22:
                        # When a delimiter is found, return FLANKLIT token along with the value
                        return "FLANKLIT", result
                    elif self.currentChar in [x for x in set(errorChar) if x not in set(delim22)]:
                        return "UNKNOWN LEXEME", result
                    else:
                        break
            elif self.currentChar in delim22:
                # When a delimiter is found, return INSTLIT token along with the value
                return "INSTLIT", result
            elif self.currentChar in [x for x in set(errorChar) if x not in set(delim22)]:
                return "UNKNOWN LEXEME", result
            else:
                break

        return "UNKNOWN LEXEME", result

    def operatorToken(self):
        result = ""

        if self.currentChar == '+':
            result += self.currentChar
            self.next()  # Move to the next character

            # Check if the next character is '=' for '+='
            if self.currentChar == '=':
                result += self.currentChar
                self.next()  # Move past '='
                if self.currentChar in delim15:  # Ensure proper delimiter after operator
                    return "+=", result
                else:
                    return "UNKNOWN LEXEME", result

            # If it's a valid delimiter after '+', return '+'
            if self.currentChar in delim26:
                return "+", result

            return "UNKNOWN LEXEME", result  # Reject invalid operators


        if self.currentChar == '-':
            result += self.currentChar
            self.next()
            print(self.currentChar)
            instctr = 0
            flankctr = 0
            # Handling negative floating-point numbers
            if self.currentChar in "0123456789":
                print(self.currentChar)
                while self.currentChar in "0123456789" and self.currentChar != '\0':
                    if instctr > 9 or flankctr > 9:
                        return "UNKNOWN LEXEME", result
                    print(self.currentChar)
                    result += self.currentChar
                    instctr += 1
                    self.next()

                if self.currentChar == '.':
                    result += self.currentChar
                    self.next()

                    while self.currentChar in "0123456789" or self.currentChar == '\0':
                        if instctr > 9 or flankctr > 9:
                            return "UNKNOWN LEXEME", result
                        result += self.currentChar
                        flankctr += 1
                        self.next()
                        if self.currentChar in delim18:
                            return "FLANKLIT", result

                elif self.currentChar in delim18:
                    return "INSTLIT", result
                else:
                    return "UNKNOWN LEXEME", result

            if self.currentChar in delim23:
                return "-", result
            elif self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim12:
                    return "-=", result
                else:
                    return "UNKNOWN LEXEME", result


            if self.currentChar == '0':
                result += self.currentChar
                self.next()
                if self.currentChar == '.':
                    result += self.currentChar
                    self.next()
                    if self.currentChar == '0123456789':
                        while True:
                            if self.currentChar == '0123456789' or self.currentChar == '\0':
                                result += self.currentChar
                                self.next()
                            if self.currentChar in delim18:
                                return "FLANKLIT", result

            if self.currentChar == '123456789':
                result += self.currentChar
                self.next()
                while True:
                    if self.currentChar == '0123456789' or self.currentChar == '\0':
                        result += self.currentChar
                        self.next()
                        if self.currentChar in delim18:
                            return "INSTLIT", result
                        if self.currentChar == '.':
                            result += self.currentChar
                            self.next()
                            while True:
                                if self.currentChar == '0123456789' or self.currentChar == '\0':
                                    result += self.currentChar
                                    self.next()
                                if self.currentChar in delim18:
                                    return "FLANKLIT", result
            else:
                return "UNKNOWN LEXEME", result


        elif self.currentChar == '*':
            result += self.currentChar
            self.next()
            if self.currentChar in delim14:
                return "*", result
            if self.currentChar == '*':
                result += self.currentChar
                self.next()
                if self.currentChar in delim14:
                    return "**", result
                else:
                    return "UNKNOWN LEXEME", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim14:
                    return "*=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result

        elif self.currentChar == '/':
            result += self.currentChar
            self.next()
            if self.currentChar in delim14:
                return "/", result
            if self.currentChar == '/':
                result += self.currentChar
                self.next()
                if self.currentChar in delim14:
                    return "//", result
                else:
                    return "UNKNOWN LEXEME", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim14:
                    return "/=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result

        elif self.currentChar == '%':
            result += self.currentChar
            self.next()
            if self.currentChar in delim14:
                return "%", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim14:
                    return "%=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result
            
    def a_token(self):
        result = ""
        checker = ""  # advance
        checker += self.currentChar  # a
        self.next()  # self.currentChar = d
        checker += self.currentChar  # ad
        self.prev()  # self.currentChar = a

        # advance keyword
        if checker == "ab": #ajan
            for char in "abort":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim12)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim12:
                return "UNKNOWN LEXEME", result

            return "abort", result

        # and keyword
        elif checker == "an":
            for char in "and":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim5)]:
                    return "UNKNOWN LEXEME", result
            if self.currentChar not in delim5:
                    return "UNKNOWN LEXEME", result

            return "and", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result
    
    def b_token(self):
        result = ""
        checker = ""  # advance
        checker += self.currentChar  # a
        self.next()  # self.currentChar = d
        checker += self.currentChar  # ad
        self.prev()  # self.currentChar = a

        # advance keyword
        if checker == "ba": #ajan
            for char in "back":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim4:
                return "UNKNOWN LEXEME", result

            return "back", result

        # and keyword
        elif checker == "bo":
            for char in "bounce":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim12)]:
                    return "UNKNOWN LEXEME", result
            if self.currentChar not in delim12:
                    return "UNKNOWN LEXEME", result

            return "bounce", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result
    
    def c_token(self):
        result = ""


        for char in "chat":
            if self.currentChar != char:
                return "UNKNOWN LEXEME", result
            result += self.currentChar
            self.next()

        if self.currentChar in [x for x in set(errorChar) if x not in set(delim5)]:
            return "UNKNOWN LEXEME", result

        if self.currentChar not in delim3:
            return "UNKNOWN LEXEME", result

        return "chat", result
        
    def d_token(self):
        result = ""
        checker = ""  # elsa
        checker += self.currentChar  # e
        self.next()  # self.currentChar = e
        checker += self.currentChar  # el
        self.next()  # self.currentChar = e
        checker += self.currentChar  # el
        self.prev()  # self.currentChar = g
        self.prev()

        # ELIB keyword
        if checker == "def":
            for char in "defuse":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "defuse", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def f_token(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.prev()
        self.prev()

        if checker == "for":
            for char in "force":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "force", result

        elif checker == "fla":
            for char in "flank":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "flank", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def g_token(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.prev()
        self.prev()
        if checker == "glo":
            for char in "globe":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "globe", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def i_token(self):
        result = ""
        checker = ""  # genre
        checker += self.currentChar  # i
        self.next()  # self.currentChar = f
        checker += self.currentChar  # i
        self.prev()  # self.currentChar = i

        if checker == "in":
            for char in "in":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            # Check for 'inst'
            if self.currentChar == 's':  # Check for 'inst'
                result += "s"
                self.next()  # Move to next char
                if self.currentChar == 't':  # Check for 'inst'
                    result += "t"
                    self.next()  # Move to next char
                    if self.currentChar not in delim3:
                        return "UNKNOWN LEXEME", result
                    return "inst", result
            
            # Check for 'inst'
            if self.currentChar == 'f':  # Check for 'inst'
                result += "f"
                self.next()  # Move to next char
                if self.currentChar == 'o':  # Check for 'inst'
                    result += "o"
                    self.next()  # Move to next char
                    if self.currentChar not in delim5:
                        return "UNKNOWN LEXEME", result
                    return "info", result

            # After checking for 'inst' and 'info', if no match, return "in"
            if self.currentChar not in delim5:
                return "UNKNOWN LEXEME", result
            return "in", result  # Return "in" if no other tokens matched

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result
    
    def l_token(self):
        result = ""


        for char in "load":
            if self.currentChar != char:
                return "UNKNOWN LEXEME", result
            result += self.currentChar
            self.next()

        if self.currentChar in [x for x in set(errorChar) if x not in set(delim1)]:
            return "UNKNOWN LEXEME", result

        if self.currentChar not in delim1:
            return "UNKNOWN LEXEME", result

        return "load", result

    def n_token(self):  
        result = ""
        checker = ""  # genre
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()  # self.currentChar = g
        self.prev()

        if checker == "neg":
            for char in "neg":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim8)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim8:
                return "UNKNOWN LEXEME", result

            return "neg", result

        if checker == "not":
            for char in "not":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim5:
                return "UNKNOWN LEXEME", result

            return "not", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result
    
    def o_token(self):
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()
        if checker == "or":
            for char in "or":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim5)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim5:
                return "UNKNOWN LEXEME", result

            return "or", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result
    
    def p_token(self):  # pin = delim7 prom = delim3 poor = delim4 pout = delim7
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()  # self.currentChar = g
        self.prev()

        if checker == "pla":
            for char in "plant":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim24:
                return "UNKNOWN LEXEME", result

            return "plant", result

        if checker == "per":
            for char in "perim":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim4:
                return "UNKNOWN LEXEME", result
            return "perim", result

        if checker == "pos":
            for char in "pos":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim8)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim8:
                return "UNKNOWN LEXEME", result

            return "pos", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result
                
    def r_token(self):
        result = ""

        # Check for "r" at the beginning
        if self.currentChar == 'r':
            result += self.currentChar
            self.next()

            # Check for "e" following "r"
            if self.currentChar == 'e':
                result += self.currentChar
                self.next()

                # Now check if the next character is 'l' for "reload"
                if self.currentChar == 'l':
                    result += self.currentChar
                    self.next()

                    # Check for 'o'
                    if self.currentChar == 'o':
                        result += self.currentChar
                        self.next()

                        # Check for 'a'
                        if self.currentChar == 'a':
                            result += self.currentChar
                            self.next()

                            # Check for 'd'
                            if self.currentChar == 'd':
                                result += self.currentChar
                                self.next()

                                # Verify delimiter after "reload"
                                if self.currentChar in delim4:
                                    return "reload", result
                                else:
                                    # Invalid delimiter after "reload"
                                    return "UNKNOWN LEXEME", result
                            else:
                                # "d" not found after "reloa"
                                return "UNKNOWN LEXEME", result
                        else:
                            # "a" not found after "relo"
                            return "UNKNOWN LEXEME", result
                    else:
                        # "o" not found after "rel"
                        return "UNKNOWN LEXEME", result
                else:
                    # After "re", check if the current character is a valid delimiter for "re"
                    if self.currentChar in delim4:
                        return "re", result
                    else:
                        # "re" not followed by a valid delimiter
                        return "UNKNOWN LEXEME", result
            else:
                # "e" not found after "r"
                return "UNKNOWN LEXEME", result
        else:
            # Starting character is not 'r'
            return "UNKNOWN LEXEME", result

    def s_token(self):
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()
        if checker == "st":
            for char in "strike":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "strike", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def t_token(self):
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()

        if checker == "to":
            for char in "tool":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                    return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                    return "UNKNOWN LEXEME", result

            return "tool", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def w_token(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.prev()
        if checker == "wa":
            for char in "watch":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                    return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                    return "UNKNOWN LEXEME", result

            return "watch", result
        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def comment_token(self):
        result = ""  #SEAL#
        if self.currentChar == '`': 
            result += self.currentChar 
            while True:
                self.next() 
                result += self.currentChar 
                if self.currentChar == '`':
                    self.next()
                    if self.currentChar in delim28:
                        return "COMMENT", result
                    else:
                        break
                elif self.currentChar == '\0':
                    print("FLAG")
                    return "UNKNOWN LEXEME", result
            return "UNKNOWN LEXEME", result

        if self.currentChar == '$':  
            result += self.currentChar  
            while True:
                self.next() 
                result += self.currentChar  
                if self.currentChar == '$':
                    self.next()
                    if self.currentChar in delim28:
                        return "COMMENT", result
                    else:
                        break
                elif self.currentChar == '\0':
                    print("FLAG")
                    return "UNKNOWN LEXEME", result
            return "UNKNOWN LEXEME", result



    def rel_token(self):
        result = ""
        result += self.currentChar
        self.next()
        if result[0] == '<':
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim9:
                    return ("<=", result)
            if self.currentChar in delim9:
                return ("<", result)
        elif result[0] == '>':
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim9:
                    return (">=", result)
            if self.currentChar in delim9:
                return (">", result)
        elif result[0] == '=':
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim9:
                    return ("==", result)
            if self.currentChar in delim9:
                return ("=", result)
            
        elif result[0] == '!':
            if self.currentChar in delim5:  # Assuming delim5 is defined
                self.next()
                return ("!", result)
            
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim9:
                    return ("!=", result)
        return "UNKNOWN LEXEME", result
        
    def special_token(self):
        result = ""

        # Handle the sequence '~{'
        if self.currentChar == '~':
            result += self.currentChar
            self.next()  # Move to the next character
            if self.currentChar == '{':  # Check if the next character is '{'
                result += self.currentChar  # Append '{' to the result
                self.next()
                return "~{", result  # Return as opening block
            elif self.currentChar in delim1:  # If only ~, validate against delim1
                return "~", result
            else:
                return "UNKNOWN LEXEME", result

        # Handle the sequence '}~'
        elif self.currentChar == '}':
            result += self.currentChar
            self.next()  # Move to the next character
            if self.currentChar == '~':  # Check if the next character is '~'
                result += self.currentChar  # Append '~' to the result
                self.next()
                return "}~", result  # Return as closing block
            elif self.currentChar in delim16:  # If only }, validate against delim16
                return "}", result
            else:
                return "UNKNOWN LEXEME", result
            
        if self.currentChar == '~':
            result += self.currentChar
            self.next()
            if self.currentChar in delim1:
                return "~", result
            else:
                return "UNKNOWN LEXEME", result
            
        elif self.currentChar == '(':
            result += self.currentChar
            self.next()
            if self.currentChar in delim23:
                return "(", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == '[':
            result += self.currentChar
            self.next()
            if self.currentChar in delim10:
                return "[", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == '{':
            result += self.currentChar
            self.next()
            if self.currentChar in delim11:
                return "{", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == ')':
            result += self.currentChar
            self.next()
            if self.currentChar in delim18:
                return ")", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == ']':
            result += self.currentChar
            self.next()
            if self.currentChar in delim19:
                return "]", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == '}':
            result += self.currentChar
            self.next()
            if self.currentChar in delim11:
                return "}", result
            else:
                return "UNKNOWN LEXEME", result

        elif self.currentChar == ';':
            result += self.currentChar
            self.next()
            if self.currentChar in delim27:
                print(result)
                return ";", result
        return "UNKNOWN LEXEME", result
    
    def UnknownToken(self):
        result = ""
        result += self.currentChar
        self.next()
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter in result:
                return "UNKNOWN LEXEME", result
        return "UNKNOWN LEXEME", result + " "
    
    def strikelit_token(self):
        result = ""
        if self.currentChar == '"':
            while True:
                result += self.currentChar
                print(result, self.currentChar)

                self.next()
                if self.currentChar == '"':  # Closing quote found
                    result += self.currentChar
                    self.next()  # Move past the closing quote
                    print(result, self.currentChar)

                    if self.currentChar not in delim20:
                        return "UNKNOWN LEXEME", result
                    else:
                        return "STRIKELIT", result

                if self.currentChar == '\n' or self.currentChar == '\0' or self.currentChar == '':
                    return "UNKNOWN LEXEME", result  # Unterminated string literal

                if self.counter >= len(self.lexeme):  # Prevent infinite looping at EOF
                    return "UNKNOWN LEXEME", result

    def chatlit_token(self):
        result = ""
        if self.currentChar == "'":
            result += self.currentChar
            self.next()
            
            while self.counter < len(self.lexeme):  # Prevents infinite loops
                if self.currentChar == "'":  # Found closing quote
                    result += self.currentChar
                    self.next()

                    if self.currentChar in delim20:
                        return "CHATLIT", result
                    else:
                        return "UNKNOWN LEXEME", result

                elif self.currentChar in ['\n', '\0', '']:  # Unterminated string
                    return "UNKNOWN LEXEME", result

                else:
                    result += self.currentChar
                    self.next()

            return "UNKNOWN LEXEME", result  # Handles unterminated literals at EOF

        return "UNKNOWN LEXEME", result  # Not a string literal

    def seperator_token(self):
        result = ""
        result += self.currentChar
        self.next()
        if self.currentChar in delim22:
            return "COMMA", result
        return "UNKNOWN LEXEME", result

    def NewlineToken(self):
        result = ""
        if self.currentChar == "\\":
            self.next()
            if self.currentChar == "n":
                self.prev()
                while True:
                    result += self.currentChar # \n
                    if self.currentChar == "n": # X
                        self.next()
                        return "NEWLINE", "\n"
                    self.next() # current = n
        return "UNKNOWN LEXEME", result

    def unknown_token(self):
        result = ""
        result += self.currentChar
        self.next()
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter in result:
                return "UNKNOWN LEXEME", result
        return "UNKNOWN LEXEME", result + " "

    def IdentifierToken(self):
        result = "" 
        result += self.currentChar  # First character (assumed to be a letter or underscore)
        self.next()  # Move to the next character

        # Check if the current character is a valid starting character for an identifier
        if self.currentChar in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_" or "1234567890":  # Added support for underscore
            result += self.currentChar 
            self.next()  # Move to next character
            while (self.currentChar in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_") and self.currentChar not in delim19:  
                # Allow letters, digits, and underscores in the identifier, and break on invalid characters
                if self.currentChar in [x for x in set(errorChar) if x not in set(delim19)] or self.currentChar == "#" or self.currentChar in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    return "UNKNOWN LEXEME", result  # Return unknown lexeme if the character is invalid
                result += self.currentChar
                self.next()

                if self.currentChar == '\0':  # Stop at null character
                    break

            # If the next character is a delimiter
            if self.currentChar in delim19:
                self.counter += 1
                if len(result) <= 15:  # Identifier length should not exceed 16 characters
                    print(result)
                    if result[1:] not in reservedkeywords:  # Check if it's not a reserved keyword
                        return f"Identifier{self.counter}", result  # Valid identifier
                    else:
                        return "UNKNOWN LEXEME", result  # Reserved keyword, treated as unknown
                else:
                    return "UNKNOWN LEXEME", result  # Identifier exceeds the allowed length
        # If the first character is invalid (not a letter or underscore)
        elif self.currentChar in "0123456789" or self.currentChar in [x for x in set(errorChar) if x not in set(delim19)]:
            return "UNKNOWN LEXEME", result  # Return unknown lexeme for invalid identifiers
        return "UNKNOWN LEXEME", result  # Fallback for any other cases


    def getNextTokens(self):
        counter = 0
        error = "UNKNOWN LEXEME"
        while True:
            if counter >= len(self.lexeme):
                break
            if '0' <= self.currentChar <= '9' or self.currentChar == ".":
                self.type_, self.value_ = self.digits()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar in "+-*/%":
                self.type_, self.value_ = self.operatorToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'a':
                self.type_, self.value_ = self.a_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'b':
                self.type_, self.value_ = self.b_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'c':
                self.type_, self.value_ = self.c_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'd':
                self.type_, self.value_ = self.d_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'f':
                self.type_, self.value_ = self.f_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'g':
                self.type_, self.value_ = self.g_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'i':
                self.type_, self.value_ = self.i_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'l':
                self.type_, self.value_ = self.l_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'n':
                self.type_, self.value_ = self.n_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'o':
                self.type_, self.value_ = self.o_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'p':
                self.type_, self.value_ = self.p_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'r':
                self.type_, self.value_ = self.r_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 's':
                self.type_, self.value_ = self.s_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 't':
                self.type_, self.value_ = self.t_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'w':
                self.type_, self.value_ = self.w_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '#':
                self.type_, self.value_ = self.IdentifierToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '`' or self.currentChar == '$':
                self.type_, self.value_ = self.comment_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar in "({[)}];~}":
                self.type_, self.value_ = self.special_token()
                if self.type_ == "UNKNOWN LEXEME":
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '"':
                self.type_, self.value_ = self.strikelit_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == "'":
                self.type_, self.value_ = self.chatlit_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif (self.currentChar == '<' or self.currentChar == '>' or self.currentChar == '!' or self.currentChar == '='):
                self.type_, self.value_ = self.rel_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == ',':
                self.type_, self.value_ = self.seperator_token()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == ' ':
                self.type_, self.value_ = self.SpaceToken()
                self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            if self.currentChar == "\n":
                self.tokens.append(f'New line')
                self.lineCounter += 1
                self.next()
                continue
            elif self.currentChar in unknownCharacters:
                self.type_, self.value_ = self.UnknownToken()
                self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                continue

            counter += 1

        return self.tokens  # Return the complete list of tokens


def main():
    while True:
        lexeme = input("Enter lexeme: ")
        lexer = DEDOSLexicalAnalyzer(lexeme)
        print("Token: Lexeme")
        lexer.getNextTokens()
        print(lexer.tokens)
        print(lexer.tokensForUnknown)
        if lexeme == "|":
            break


if __name__ == "__main__":
    main()
