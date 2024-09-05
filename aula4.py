# AULA 4 - parenteses e sinais

import sys

def limpa_coment2(text):
    i=0
    while i < (len(text)-1):
        if text[i] == "*" and text[i+1] == "/":
            raise ValueError("Comentário não aberto")
        if text[i] == "/" and text[i+1] == "*":
            inicio = i
            while text[i] != "*" or text[i+1] != "/":
                if i == len(text)-1:
                    raise ValueError("Comentário não fechado")
                i+=1
            if text[i] == "*" and text[i+1] == "/":
                fim = i+2
                text = text[:inicio] + text[fim:]
                i=0 
        i+=1
    return text

def balanceamento_parn(text):
    pilha = []
    for caractere in text:
        if caractere == '(':
            pilha.append(caractere)
        elif caractere == ')':
            if pilha == []:
                return False
            pilha.pop()

    if pilha != []:
        return False
    return True

class Token():
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
class Tokenizer():
    def __init__(self, source):
        
        self.source = limpa_coment2(source) #codigo fonte
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
        elif self.source[self.position] == '*':
            self.position += 1
            self.next = Token('MULT', '*')
            return self.next
        elif self.source[self.position] == '/':
            self.position += 1
            self.next = Token('DIV', '/')
            return self.next
        elif self.source[self.position] == '(':
            self.position += 1
            self.next = Token('LPAREN', '(')
            return self.next
        elif self.source[self.position] == ')':
            self.position += 1
            self.next = Token('RPAREN', ')')
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

    def parseFactor(self):
        token = self.tokenizer.selectNext()
        # if token.tipo == 'INT':
        #     return token.valor
        if token.tipo == 'INT':
            return token.valor
        elif token.tipo == 'MINUS':
            return -self.parseFactor()
        elif token.tipo == 'PLUS':
            return self.parseFactor()
        elif token.tipo == 'LPAREN':
            resultado = self.parseExpression()
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            return resultado
        else:
            raise ValueError('Token inválido: ' + token.tipo)
        
    def parseTerm(self):
        self.resultado = self.parseFactor()
        token = self.tokenizer.selectNext()
        if token.tipo == "INT":
            raise ValueError('Token inválido: ' + token.tipo)
        while token.tipo == 'MULT' or token.tipo == 'DIV':
            if token.tipo == 'MULT':
                self.resultado *= self.parseFactor()
                
                
            elif token.tipo == 'DIV':
                self.resultado //= self.parseFactor()
            token = self.tokenizer.selectNext()  
        return self.resultado

        
        
        
    def parseExpression(self):
        resultado = self.parseTerm()
        token = self.tokenizer.next

        while token.tipo == 'PLUS' or token.tipo == 'MINUS':
            if token.tipo == 'PLUS':
                resultado += self.parseTerm()
            elif token.tipo == 'MINUS':
                resultado -= self.parseTerm()
            token = self.tokenizer.next
        return int(resultado)



    def run(self, code):
        tokenizador = Tokenizer(code)
        self.tokenizer = tokenizador
        if not balanceamento_parn(code):
            raise ValueError("Parenteses inválidos")
        resultado = self.parseExpression()
        token = self.tokenizer.selectNext()
        if token.tipo != 'EOF':
            raise ValueError('Token inválido: ' + self.tokenizer.next.tipo)
        return resultado

    

code = sys.argv[1]
# code = "(3+3)/2"

parser = Parser()
resultado = parser.run(code)

print(resultado)