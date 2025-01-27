# Constants
input_string = ""
position = 0
current_char = ''
delim1 = [' ', '#', '~', '\n', '\0']
delim2 = [' ', '(', '[', '{', '"']
delim3 = [' ']
delim4 = [' ', '(']
delim5 = [' ', ')', ']', '}', '#', '~', '=', '!', '<', '>', '+', '-', '/', '%', ',', ':', '\n', '\0']
delim6 = [' ', '{']
delim7 = ['(']
delim8 = [' ', '(', '{', '[', '"', '~', '#']
delim9 = ['`', ' ', '(', '"', '[', '{', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'c', 'n']
delim10 = [' ', '`', '(', '"', '[', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
delim11 = [' ', '`', '(', '[', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
delim12 = [' ', '`', '(', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
delim13 = [' ', '{', ',', '\0']
delim14 = [' ', '#', '~', '{', ']', '}', ')', ',', 'a', 'o', ':', '\0', '\n']
delim15 = [' ', '#', '~', '+', '-', '*', '%', '!', '=', '<', '>', ',', 'a', 'o', '(', '{', ']', '}', ')', ',', ':', '\0', '\n']
delim16 = [' ', '#', '~', '+', '!', '=', '>', '<', '[', ']', '}', ')', ',', 'a', 'o', ':', '\0', '\n']
delim17 = [' ', '+', '=', '!', '<', '>', ',', '#', '~', ']', ')', '}', ':', '\n', '\0']
delim18 = [' ', '+', '-', '*', '/', '%', '[', '(', '<', '>', '=', ':', ',', '!', '#', '~', ')', ']', '}', '\n', '\0']
delim19 = [' ', ',', '~', '#', '(', '[', '<', '>', '=', '!', '+', '-', '*', '/', '%', ')', ']', '}', '\n', '\0']
delim20 = ['\n']
delim21 = [' ', '\n', '\0']
delim22 = [' ', '`', '(', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '"', '[', '{', '(', 'c', 'n', '^']
delim23 = [' ', '(', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
delim24 = ['[', '(', '{', ']', ')', '}', '"', '`', ' ', '\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'c','n', '-', '\0']
delim25 = ['(', '}', ']', ']', '}', ')', '"', '#', '~', '`', ' ', '\n', '[', '{', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'c', 'e', 'f', 'g', 'h', 'i', 'l', 'n', 'p','r', 's', 'u', '-', '\0']
errorChar = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?', '~']
unknownCharacters = ['@', '$', '^', '&', '_', '?', '|', ';', '-', '|', '\\', ':', ';', 'q', 'd', 'j', 'k', 'm', 'w', 'v', 'x', 'y', 'z', '.', "'"] + [chr(ord('A') + i) for i in range(26)]
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
reservedKeywords = ["advance", "and", "bully", "cap", "checkif", "chill", "codex", "cut", "elba", "elsa", "flute", "genre", "goon", "hint", "if", "in", "lastly", "lift", "log", "nocap", "not", "poor", "pout", "range", "remit", "round", "say", "sayless", "size", "sort", "star", "task", "universal"]
IdentifierCTR = 0

class Lexer:
    def __init__(self, lexeme): #local declarations inside the class
        self.lexeme = lexeme
        self.currentChar = lexeme[0]
        self.position = 0
        self.value_ = None
        self.type_ = None
        self.fullResult = None
        self.tokens = []
        self.IDcounter = 0
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

    def digits(self):
        result = ""
        hintctr = 0
        flutectr = 0
        while True:
            if self.currentChar == '0':
                result += self.currentChar
                hintctr += 1
                self.next()
            elif self.currentChar in "123456789":
                result += self.currentChar
                hintctr += 1
                self.next()
                while True:
                    if hintctr > 9 or flutectr > 9:
                        return "UNKNOWN LEXEME", result
                    if self.currentChar in "0123456789":
                        result += self.currentChar
                        hintctr += 1
                        self.next()
                    elif self.currentChar == '.':
                        result += self.currentChar
                        self.next()
                        while True:
                            if hintctr > 9 or flutectr > 9:
                                return "UNKNOWN LEXEME", result
                            if self.currentChar in "0123456789":
                                result += self.currentChar
                                flutectr += 1
                                print(flutectr)
                                self.next()
                            elif self.currentChar in delim18:
                                return "FLUTELIT", result
                            elif self.currentChar in [x for x in set(errorChar) if x not in set(delim18)]:
                                return "UNKNOWN LEXEME", result
                            else:
                                break
                        break
                    elif self.currentChar in delim18:
                        return "HINTLIT", result
                    elif self.currentChar in [x for x in set(errorChar) if x not in set(delim18)]:
                        return "UNKNOWN LEXEME", result
                    else:
                        break
            elif self.currentChar == '.':
                result += self.currentChar
                self.next()
                if self.currentChar == ' ' or self.currentChar == '\0' or self.currentChar == '\n':
                    return "UNKNOWN LEXEME", result
                while True:
                    if hintctr > 9 or flutectr > 9:
                        return "UNKNOWN LEXEME", result
                    if self.currentChar in "0123456789":
                        result += self.currentChar
                        flutectr += 1
                        self.next()
                    elif self.currentChar in delim18:
                        return "FLUTELIT", result
                    elif self.currentChar in [x for x in set(errorChar) if x not in set(delim18)]:
                        return "UNKNOWN LEXEME", result
                    else:
                        break
            elif self.currentChar in delim18:
                return "HINTLIT", result
            elif self.currentChar in [x for x in set(errorChar) if x not in set(delim18)]:
                return "UNKNOWN LEXEME", result
            else:
                break

        return "UNKNOWN LEXEME", result

    def operatorToken(self):
        result = ""

        if self.currentChar == '+':
            result += self.currentChar
            self.next()
            if self.currentChar in delim10:
                return "+", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim11:
                    return "+=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result

        if self.currentChar == '-':
            result += self.currentChar
            self.next()
            print(self.currentChar)
            hintctr = 0
            flutectr = 0
            # Handling negative floating-point numbers
            if self.currentChar in "0123456789":
                print(self.currentChar)
                while self.currentChar in "0123456789" and self.currentChar != '\0':
                    if hintctr > 9 or flutectr > 9:
                        return "UNKNOWN LEXEME", result
                    print(self.currentChar)
                    result += self.currentChar
                    hintctr += 1
                    self.next()

                if self.currentChar == '.':
                    result += self.currentChar
                    self.next()

                    while self.currentChar in "0123456789" or self.currentChar == '\0':
                        if hintctr > 9 or flutectr > 9:
                            return "UNKNOWN LEXEME", result
                        result += self.currentChar
                        flutectr += 1
                        self.next()
                        if self.currentChar in delim18:
                            return "FLUTELIT", result

                elif self.currentChar in delim18:
                    return "HINTLIT", result
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

            # Dito hanggang ->
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
                                return "FLUTELIT", result

            if self.currentChar == '123456789':
                result += self.currentChar
                self.next()
                while True:
                    if self.currentChar == '0123456789' or self.currentChar == '\0':
                        result += self.currentChar
                        self.next()
                        if self.currentChar in delim18:
                            return "HINTLIT", result
                        if self.currentChar == '.':
                            result += self.currentChar
                            self.next()
                            while True:
                                if self.currentChar == '0123456789' or self.currentChar == '\0':
                                    result += self.currentChar
                                    self.next()
                                if self.currentChar in delim18:
                                    return "FLUTELIT", result
            else:
                return "UNKNOWN LEXEME", result


        elif self.currentChar == '*':
            result += self.currentChar
            self.next()
            if self.currentChar in delim12:
                return "*", result
            if self.currentChar == '*':
                result += self.currentChar
                self.next()
                if self.currentChar in delim12:
                    return "**", result
                else:
                    return "UNKNOWN LEXEME", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim12:
                    return "*=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result

        elif self.currentChar == '/':
            result += self.currentChar
            self.next()
            if self.currentChar in delim12:
                return "/", result
            if self.currentChar == '/':
                result += self.currentChar
                self.next()
                if self.currentChar in delim12:
                    return "//", result
                else:
                    return "UNKNOWN LEXEME", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim12:
                    return "/=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result

        elif self.currentChar == '%':
            result += self.currentChar
            self.next()
            if self.currentChar in delim12:
                return "%", result
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim12:
                    return "%=", result
                else:
                    return "UNKNOWN LEXEME", result
            else:
                return "UNKNOWN LEXEME", result




    def AToken(self):
        result = ""
        checker = ""  # advance
        checker += self.currentChar  # a
        self.next()  # self.currentChar = d
        checker += self.currentChar  # ad
        self.prev()  # self.currentChar = a

        # advance keyword
        if checker == "ad": #ajan
            for char in "advance":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim1)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim1:
                return "UNKNOWN LEXEME", result

            return "advance", result

        # and keyword
        elif checker == "an":
            for char in "and":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim2)]:
                    return "UNKNOWN LEXEME", result
            if self.currentChar not in delim2:
                    return "UNKNOWN LEXEME", result

            return "and", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def BToken(self):
        result = ""


        for char in "bully":
            if self.currentChar != char:
                return "UNKNOWN LEXEME", result
            result += self.currentChar
            self.next()

        if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
            return "UNKNOWN LEXEME", result

        if self.currentChar not in delim3:
            return "UNKNOWN LEXEME", result

        return "bully", result


    def CToken(self):
        result = ""
        checker = ""  # checkif
        checker += self.currentChar  # c
        self.next()  # self.currentChar = h
        checker += self.currentChar  # ch
        self.next()  # self.currentChar = e
        checker += self.currentChar  # che
        self.prev()  # self.currentChar = h
        self.prev()  # self.currentChar = c

        if checker == "cap":
            for char in "cap":
                if self.currentChar != char:
                    return "UNKOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim5)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim5:
                return "UNKNOWN LEXEME", result

            return "cap", result

        elif checker == "che":
            for char in "checkif":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim4:
                return "UNKNOWN LEXEME", result

            return "checkif", result

        elif checker == "chi":
            for char in "chill":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim1)]:
                        return "UNKNOWN LEXEME", result

            if self.currentChar not in delim1:
                        return "UNKNOWN LEXEME", result

            return "chill", result

        elif checker == "cod":
            for char in "codex":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                        return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                        return "UNKNOWN LEXEME", result

            return "codex", result

        elif checker == "cut":
            for char in "cut":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                        return "UNKNOWN LEXEME", result

            if self.currentChar not in delim4:
                        return "UNKNOWN LEXEME", result

            return "cut", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def EToken(self):
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
        if checker == "eli":
            for char in "elib":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim4:
                return "UNKNOWN LEXEME", result

            return "elib", result

        elif checker == "els":
            for char in "elsa":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim6)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim6:
                return "UNKNOWN LEXEME", result

            return "elsa", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def FToken(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.prev()
        self.prev()
        if checker == "flu":
            for char in "flute":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "elsa", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def GToken(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.prev()

        # Genre keyword
        if checker == "ge":
            for char in "genre":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "genre", result

        # goon keyword
        elif checker == "go":
            for char in "goon":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim1)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim1:
                return "UNKNOWN LEXEME", result

            return "goon", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def HToken(self):  # delim4
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()
        if checker == "hi":
            # Character by character checker
            for char in "hint":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
            # Error checker if current character is not in delim list
            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "hint", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def IToken(self):  # if - delim4, in-delim3
        result = ""
        checker = ""  # genre
        checker += self.currentChar  # i
        self.next()  # self.currentChar = f
        checker += self.currentChar  # if
        self.prev()  # self.currentChar = i

        if checker == "if":
            for char in "if":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim4:
                return "UNKNOWN LEXEME", result

            return "if", result

        # goon keyword
        elif checker == "in":
            for char in "in":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "in", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def LToken(self):  # Lastly = Delim6 Lift = Delim3 Log = Delim4
        result = ""
        checker = ""  # genre
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()  # self.currentChar = g

        if checker == "la":
            for char in "lastly":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim6)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim6:
                return "UNKNOWN LEXEME", result

            return "lastly", result

        if checker == "li":
            for char in "lift":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "lift", result

        if checker == "lo":
            for char in "log":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "log", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result



    def NToken(self):  # nocap = delim 5 not = delim2
        result = ""
        checker = ""  # genre
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()  # self.currentChar = g
        self.prev()

        if checker == "noc":
            for char in "nocap":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim5)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim5:
                return "UNKNOWN LEXEME", result

            return "nocap", result

        if checker == "not":
            for char in "not":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim2)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim2:
                return "UNKNOWN LEXEME", result

            return "not", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result




    def OToken(self):
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

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim2)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim2:
                return "UNKNOWN LEXEME", result

            return "or", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def PToken(self):  # pin = delim7 prom = delim3 poor = delim4 pout = delim7
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()  # self.currentChar = g
        self.prev()

        if checker == "pin":
            for char in "pin":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "pin", result

        if checker == "poo":
            for char in "poor":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim4)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim4:
                return "UNKNOWN LEXEME", result
            return "poor", result

        if checker == "pou":
            for char in "pout":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "pout", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def RToken(self):  # range = delim7 remit = delim8 round = delim7
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()  # self.currentChar = g

        if checker == "ra":
            for char in "range":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "range", result

        if checker == "re":
            for char in "remit":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim8)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim8:
                return "UNKNOWN LEXEME", result

            return "remit", result

        if checker == "ro":
            for char in "round":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "round", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def SToken(self):  # say = delim6 sayless = delim6 size = delim7 sort = delim7 star = delim4
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.next()  # self.currentChar = e
        self.prev()  # self.currentChar = g
        self.prev()  # self.currentChar = g
        self.prev()  # self.currentChar = g
        print(checker)
        if checker == "say":

            for char in "say":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar == 'l':

                for char in "less":
                    print(self.currentChar, char)

                    if self.currentChar != char:
                        return "UNKNOWN LEXEME", result
                    result += self.currentChar
                    self.next()

                if self.currentChar not in delim6:
                    return "UNKNOWN LEXEME", result

                return "sayless", result

            if self.currentChar not in delim6:
                return "UNKNOWN LEXEME", result

            return "say", result

        if checker == "siz":
            for char in "size":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "size", result

        if checker == "sor":
            for char in "sort":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim7)]:
                return "UNKNOWN LEXEME", result

            if self.currentChar not in delim7:
                return "UNKNOWN LEXEME", result

            return "sort", result

        if checker == "sta":
            for char in "star":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                return "UNKNOWN LEXEME", result
            if self.currentChar not in delim3:
                return "UNKNOWN LEXEME", result

            return "star", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result


    def TToken(self):
        result = ""
        checker = ""
        checker += self.currentChar  # g
        self.next()  # self.currentChar = e
        checker += self.currentChar  # ge
        self.prev()

        if checker == "ta":
            for char in "task":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                    return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                    return "UNKNOWN LEXEME", result

            return "task", result

        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def UToken(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()
        checker += self.currentChar
        self.prev()
        if checker == "un":
            for char in "universal":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar in [x for x in set(errorChar) if x not in set(delim3)]:
                    return "UNKNOWN LEXEME", result

            if self.currentChar not in delim3:
                    return "UNKNOWN LEXEME", result

            return "universal", result
        else:
            result += self.currentChar
            self.next()
            return "UNKNOWN LEXEME", result

    def IdentifierToken(self):
        result = ""  # `abc#
        result += self.currentChar  # `
        self.next()  # a
        if self.currentChar in "abcdefghijklmnopqrstuvwxyz":  # a
            result += self.currentChar  # `a
            self.next()  # b
            while (self.currentChar in "abcdefghijklmnopqrstuvwxyz" or self.currentChar in "0123456789") or self.currentChar not in delim19:  # `abc
                if self.currentChar in [x for x in set(errorChar) if x not in set(delim19)] or self.currentChar == "`" or self.currentChar in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()
                if self.currentChar == '\0':
                    break

            if self.currentChar in delim19:  #
                self.IDcounter += 1
                if len(result) <= 16:
                    print(result)
                    if result[1:] not in reservedKeywords:
                        return f"IDENTIFIER{self.IDcounter}", result
                    else:
                        return "UNKNOWN LEXEME", result
                else:
                    return "UNKNOWN LEXEME", result
        if self.currentChar in "0123456789" or self.currentChar in [x for x in set(errorChar) if x not in set(delim19)]:
            return "UNKNOWN LEXEME", result
        return "UNKNOWN LEXEME", result

    def ErrorHandlerToken(self):
        result = ""
        checker = ""
        checker += self.currentChar
        self.next()

        if self.currentChar == 'a':
            self.prev()

            for char in "^attributeerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^attributeerror", result

        if self.currentChar == 'f':
            self.prev()

            for char in "^floatingpointerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^floatingpointerror", result

        if self.currentChar == 's':
            self.prev()

            for char in "^syntaxerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^syntaxerror", result

        if self.currentChar == 't':
            self.prev()

            for char in "^typeerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^typeerror", result

        if self.currentChar == 'v':
            self.prev()

            for char in "^valueerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^valueerror", result

        if self.currentChar == 'k':
            self.prev()

            for char in "^keyboardinterrupt":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^keyboardinterrupt", result

        if self.currentChar == 'o':
            self.prev()

            for char in "^overflowerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^overflowerror", result

        if self.currentChar == 'n':
            self.prev()

            for char in "^nameerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^nameerror", result

        if self.currentChar == 'z':
            self.prev()

            for char in "^zerodivisionerror":
                if self.currentChar != char:
                    return "UNKNOWN LEXEME", result
                result += self.currentChar
                self.next()

            if self.currentChar not in delim13:
                return "UNKNOWN LEXEME", result
            else:
                return "^zerodivisionerror", result

        return "UNKNOWN LEXEME", checker

    def CommentToken(self):
        result = ""  #SEAL#
        if self.currentChar == '#':  # #
            result += self.currentChar  # #
            while True:
                self.next()  # S
                result += self.currentChar  # #SE
                if self.currentChar == '#':
                    self.next()
                    if self.currentChar in delim21:
                        return "COMMENT", result
                    else:
                        break
                elif self.currentChar == '\0':
                    print("FLAG")
                    return "UNKNOWN LEXEME", result
            return "UNKNOWN LEXEME", result

        if self.currentChar == '~':
            result += self.currentChar
            self.next()
            while self.currentChar not in delim20:
                result += self.currentChar
                self.next()
                if self.currentChar == '\0':
                    break
            return "COMMENT", result
        return "UNKNOWN LEXEME", result


    def SpecialToken(self):
        result = ""
        if self.currentChar == '(':
            result += self.currentChar
            self.next()
            if self.currentChar in delim24:
                return "(", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == '[':
            result += self.currentChar
            self.next()
            if self.currentChar in delim24:
                return "[", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == '{':
            result += self.currentChar
            self.next()
            if self.currentChar in delim25:
                return "{", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == ')':
            result += self.currentChar
            self.next()
            if self.currentChar in delim15:
                return ")", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == ']':
            result += self.currentChar
            self.next()
            if self.currentChar in delim16:
                return "]", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == '}':
            result += self.currentChar
            self.next()
            if self.currentChar in delim14:
                return "}", result
            else:
                return "UNKNOWN LEXEME", result
        elif self.currentChar == ':':
            result += self.currentChar
            self.next()
            if self.currentChar in delim22:
                print(result)
                return ":", result
        return "UNKNOWN LEXEME", result

    def SringLitToken(self):
        result = ""
        if self.currentChar == '"':
            while True:
                result += self.currentChar
                print(result, self.currentChar)
                self.next()
                if self.currentChar == '"':
                    result += self.currentChar
                    self.next() # "
                    print(result, self.currentChar)
                    if self.currentChar not in delim17:
                        return "UNKNOWN LEXEME", result
                    else:
                        return "STARLIT", result
                #if self.currentChar == "\\":
                #    self.next()
                #    if self.currentChar == "n":
                #        result += f"(NEWLINE-[\\n])"
                #    if self.currentChar == "t":
                #        result += f"(TAB-[\\t])"
                if self.currentChar == '\n' or self.currentChar == '\0':
                    return 'UNKNOWN LEXEME', result

    def RelationalToken(self):
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
            if self.currentChar == '=':
                result += self.currentChar
                self.next()
                if self.currentChar in delim9:
                    return ("!=", result)
        return "UNKNOWN LEXEME", result

    # [TOKEN:{, TOKEN: }]         input :
    def SpaceToken(self):
        result = '"'
        result += self.currentChar
        self.next()
        if self.currentChar != " ":
            pass
        return "SPACE", "[ ]"

    def SeperatorToken(self):
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

    def UnknownToken(self):
        result = ""
        result += self.currentChar
        self.next()
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter in result:
                return "UNKNOWN LEXEME", result
        return "UNKNOWN LEXEME", result + " "

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
                self.type_, self.value_ = self.AToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'b':
                self.type_, self.value_ = self.BToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'c':
                self.type_, self.value_ = self.CToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'e':
                self.type_, self.value_ = self.EToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'f':
                self.type_, self.value_ = self.FToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'g':
                self.type_, self.value_ = self.GToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'h':
                self.type_, self.value_ = self.HToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'i':
                self.type_, self.value_ = self.IToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'l':
                self.type_, self.value_ = self.LToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'n':
                self.type_, self.value_ = self.NToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'o':
                self.type_, self.value_ = self.OToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'p':
                self.type_, self.value_ = self.PToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'r':
                self.type_, self.value_ = self.RToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 's':
                self.type_, self.value_ = self.SToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 't':
                self.type_, self.value_ = self.TToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == 'u':
                self.type_, self.value_ = self.UToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '`':
                self.type_, self.value_ = self.IdentifierToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '^':
                self.type_, self.value_ = self.ErrorHandlerToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '~' or self.currentChar == '#':
                self.type_, self.value_ = self.CommentToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '(' or self.currentChar == '[' or self.currentChar == '{' or self.currentChar == ')' or self.currentChar == ']' or self.currentChar == '}' or self.currentChar == ':':
                self.type_, self.value_ = self.SpecialToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == '"':
                self.type_, self.value_ = self.SringLitToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif (self.currentChar == '<' or self.currentChar == '>' or self.currentChar == '!' or self.currentChar == '='):
                self.type_, self.value_ = self.RelationalToken()
                if self.type_ in error:
                    self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                else:
                    self.tokens.append(f'{self.type_} : {self.value_}')
                continue
            elif self.currentChar == ',':
                self.type_, self.value_ = self.SeperatorToken()
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
                self.tokens.append(f'"NEWLINE" : "\\n"')
                self.lineCounter += 1
                self.next()
                continue
            elif self.currentChar in unknownCharacters:
                self.type_, self.value_ = self.UnknownToken()
                self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : {self.value_}')
                continue
            # else:
            #     self.type_, self.value_ = self.UnknownToken()
            #     self.tokensForUnknown.append(f'line #{self.lineCounter} : {self.type_} : "{self.value_}"')
            #     continue
            counter += 1

def main():
    while True:
        lexeme = input("Enter lexeme: ")
        lexer = Lexer(lexeme)
        print("Token: Lexeme")
        lexer.getNextTokens()
        print(lexer.tokens)
        print(lexer.tokensForUnknown)
        if lexeme == "|":
            break


if __name__ == "__main__":
    main()
