import sys

class Token():
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
class Tokenizer():
    def __init__(self, source):
        self.source = source #codigo fonte
        self.position = 0 #posição atual
        self.next = None #ultimo token lido

    def selectNext(self):
        if self.position >= len(self.source):
            return Token('EOF', None)
        if self.source[self.position] == '+':
            self.position += 1
            self.next = Token('PLUS', '+')
            return self.next
        elif self.source[self.position] == '-':
            self.position += 1
            self.next = Token('MINUS', '-')
            return self.next
        elif self.source[self.position].isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.next = Token('INT', int(self.source[start:self.position]))
            return self.next
        elif self.source[self.position].isspace():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isspace():
                self.position += 1
            return self.selectNext()
        else:
            raise ValueError('Caracter inválido: ' + self.source[self.position])

class Parser():
    def __init__(self):
        self.tokenizer = None
        self.resultado = 0

    def parseExpression(self):
        
        token = self.tokenizer.selectNext()
        if token.tipo == 'INT':
            self.resultado += token.valor
            token = self.tokenizer.selectNext()
            if token.tipo == 'INT':
                raise ValueError('Token inválido: ' + token.tipo)
            while token.tipo == 'PLUS' or token.tipo == 'MINUS':
                if token.tipo == 'PLUS':
                    token = self.tokenizer.selectNext()
                    if token.tipo == 'INT':
                        self.resultado += token.valor
                    else:
                        raise ValueError('Token inválido: ' + token.tipo)
                elif token.tipo == 'MINUS':
                    token = self.tokenizer.selectNext()
                    if token.tipo == 'INT':
                        self.resultado -= token.valor
                    else:
                        raise ValueError('Token inválido: ' + token.tipo)
                token = self.tokenizer.selectNext()
            return self.resultado
        else:
            raise ValueError('Token inválido: ' + token.tipo)

            

    def run(self, code):
        tokenizador = Tokenizer(code)
        self.tokenizer = tokenizador
        return self.parseExpression()
    

code = sys.argv[1]

parser = Parser()
resultado = parser.run(code)

print(resultado)