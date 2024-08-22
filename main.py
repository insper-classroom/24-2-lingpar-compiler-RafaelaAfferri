# AULA 1 
# 
# import sys

# conta = sys.argv[1]



# def calculadora(conta):
#     res = 0
#     num1 = ''
#     num2 = ''
#     posicao_sinal = []
#     conta = conta.replace(" ", "")

#     for i in range(len(conta)):
#         if conta[i] == "+" or conta[i] == "-":
#             posicao_sinal.append(i)


#     if len(posicao_sinal)<2:
#         raise ValueError("Conta inválida")
#     for i in range(len(posicao_sinal)-1):
#         if posicao_sinal[i]+1 == posicao_sinal[i+1]:
#             raise ValueError("Conta inválida")

#     for i in range(len(posicao_sinal)):
#         if res == 0:
#             num1 = conta[0:posicao_sinal[i]]
#             if len(posicao_sinal) == i+1:
#                 num2 = conta[posicao_sinal[i]+1:]
#             else:
#                 num2 = conta[posicao_sinal[i]+1:posicao_sinal[i+1]]
#         else:
#             num1 = res
#             if len(posicao_sinal) == i+1:
#                 num2 = conta[posicao_sinal[i]+1:]
#             else:
#                 num2 = conta[posicao_sinal[i]+1:posicao_sinal[i+1]]
#         if conta[posicao_sinal[i]] == "+":
#             res = int(num1) + int(num2)
#         if conta[posicao_sinal[i]] == "-":
#             res = int(num1) - int(num2)

        
#     return res

# print(calculadora(conta))


# AULA 2

# import sys

# class Token():
#     def __init__(self, tipo, valor):
#         self.tipo = tipo
#         self.valor = valor
    
# class Tokenizer():
#     def __init__(self, source):
#         self.source = source #codigo fonte
#         self.position = 0 #posição atual
#         self.next = None #ultimo token lido

#     def selectNext(self):
#         if self.position >= len(self.source):
#             return Token('EOF', None)
#         if self.source[self.position] == '+':
#             self.position += 1
#             self.next = Token('PLUS', '+')
#             return self.next
#         elif self.source[self.position] == '-':
#             self.position += 1
#             self.next = Token('MINUS', '-')
#             return self.next
#         elif self.source[self.position].isdigit():
#             start = self.position
#             while self.position < len(self.source) and self.source[self.position].isdigit():
#                 self.position += 1
#             self.next = Token('INT', int(self.source[start:self.position]))
#             return self.next
#         elif self.source[self.position].isspace():
#             start = self.position
#             while self.position < len(self.source) and self.source[self.position].isspace():
#                 self.position += 1
#             return self.selectNext()
#         else:
#             raise ValueError('Caracter inválido: ' + self.source[self.position])

# class Parser():
#     def __init__(self):
#         self.tokenizer = None
#         self.resultado = 0

#     def parseExpression(self):
        
#         token = self.tokenizer.selectNext()
#         if token.tipo == 'INT':
#             self.resultado += token.valor
#             token = self.tokenizer.selectNext()
#             if token.tipo == 'INT':
#                 raise ValueError('Token inválido: ' + token.tipo)
#             while token.tipo == 'PLUS' or token.tipo == 'MINUS':
#                 if token.tipo == 'PLUS':
#                     token = self.tokenizer.selectNext()
#                     if token.tipo == 'INT':
#                         self.resultado += token.valor
#                     else:
#                         raise ValueError('Token inválido: ' + token.tipo)
#                 elif token.tipo == 'MINUS':
#                     token = self.tokenizer.selectNext()
#                     if token.tipo == 'INT':
#                         self.resultado -= token.valor
#                     else:
#                         raise ValueError('Token inválido: ' + token.tipo)
#                 token = self.tokenizer.selectNext()
#             return self.resultado
#         else:
#             raise ValueError('Token inválido: ' + token.tipo)

            

#     def run(self, code):
#         tokenizador = Tokenizer(code)
#         self.tokenizer = tokenizador
#         return self.parseExpression()
    

# code = sys.argv[1]

# parser = Parser()
# resultado = parser.run(code)

# print(resultado)

#AULA 3 - mult e div

import sys
def limpa_coment2(text):
    i=0
    while i < (len(text)-1):
        if text[i] == "/" and text[i+1] == "*":
            inicio = i
            while text[i] != "*" or text[i+1] != "/":
                if i == len(text)-1:
                    raise ValueError("Comentário não fechado")
                i+=1
            if text[i] == "*" and text[i+1] == "/":
                fim = i+2
                text = text[:inicio] + text[fim:] 
                    
        if text[i] == "*" and text[i+1] == "/":
            raise ValueError("Comentário não aberto")
            
        i+=1
    return text

def limpa_coment(text):
    achou = True
    while achou:
        achou = False
        for i in range(len(text)-1):
            if text[i] == "/" and text[i+1] == "*":
                inicio = i
                for j in range(i+2,(len(text)-1)):
                    if text[j] == "*" and text[j+1] == "/":
                        fim = j+2
                        text = text[:inicio] + text[fim:] 
                        achou = True
                        break
                if not achou:
                    raise ValueError("Comentário não fechado")
            if achou:
                break
            if text[i] == "*" and text[i+1] == "/":
                raise ValueError("Comentário não aberto")
        
    
    return text

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

    def parseTerm(self):
        token = self.tokenizer.selectNext()
        if token.tipo == 'INT':
            self.resultado = token.valor
            token = self.tokenizer.selectNext()
            if token.tipo == 'INT':
                raise ValueError('Token inválido: ' + token.tipo)
            while token.tipo == 'MULT' or token.tipo == 'DIV':
                if token.tipo == 'MULT':
                    token = self.tokenizer.selectNext()
                    if token.tipo == 'INT':
                        self.resultado *= token.valor
                    else:
                        raise ValueError('Token inválido: ' + token.tipo)
                elif token.tipo == 'DIV':
                    token = self.tokenizer.selectNext()
                    if token.tipo == 'INT':
                        self.resultado /= token.valor
                    else:
                        raise ValueError('Token inválido: ' + token.tipo)
                token = self.tokenizer.selectNext()
            return self.resultado
        else:
            raise ValueError('Token inválido: ' + token.tipo)
        
    def parseExpression(self):

        
        resultado = self.parseTerm()
        token = self.tokenizer.next
        if token.tipo != 'EOF':

            while token.tipo == 'PLUS' or token.tipo == 'MINUS':
                if token.tipo == 'PLUS':
                    resultado += self.parseTerm()
                elif token.tipo == 'MINUS':
                    resultado -= self.parseTerm()
                token = self.tokenizer.next
            return int(resultado)
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