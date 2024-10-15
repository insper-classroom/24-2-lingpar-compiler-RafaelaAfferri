import sys

#ROTEIRO 4 - Arvore Sintática

class Node():
    def __init__(self, value):
        self.value = value
        self.children = []

    def evaluate(self):
        if self.value == '+':
            if len(self.children)>1:
                num1 = self.children[0].evaluate()
                num2 = self.children[1].evaluate()
                return int(num1 + num2)
            else:
                return self.children[0].evaluate()
        elif self.value == '-':
            if len(self.children)>1:
                num1 = self.children[0].evaluate()
                num2 = self.children[1].evaluate()
                return int(num1 - num2)
            else:
                return -self.children[0].evaluate()
        elif self.value == '*':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            return int(num1 * num2)
        elif self.value == '/':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            return int(num1 // num2)
        else:
            return int(self.value)
        
            



class UnOp(Node):
    def __init__(self, value):
        super().__init__(value)
        self.children = []

class BinOp(Node):
    def __init__(self, value):
        super().__init__(value)
        self.children = []

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

class NoOp(Node):
    def __init__(self, value):
        super().__init__(value)


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
            self.next = Token('EOF', None)
            return self.next
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
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'INT':
            return IntVal(token.valor)
        elif token.tipo == 'MINUS' or token.tipo == 'PLUS':
            no = UnOp(token.valor)
            no.children.append(self.parseFactor())
            return no
        elif token.tipo == 'LPAREN':
            resultado = self.parseExpression()
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return resultado
        else:
            raise ValueError('Token inválido: ' + token.tipo)
        
    def parseTerm(self):
        node = self.parseFactor()
        token = self.tokenizer.next
        while token.tipo == 'MULT' or token.tipo == 'DIV':
            self.tokenizer.selectNext()
            op = BinOp(token.valor)
            op.children.append(node)
            node = op
            node.children.append(self.parseFactor())
            token = self.tokenizer.next 
        return node

    def parseExpression(self):
        node = self.parseTerm()
        token = self.tokenizer.next
        while token.tipo == 'PLUS' or token.tipo == 'MINUS':
            self.tokenizer.selectNext()
            op = BinOp(token.valor)
            op.children.append(node)
            node = op
            node.children.append(self.parseTerm())
            token = self.tokenizer.next
        return node



    def run(self, code):
        tokenizador = Tokenizer(code)
        self.tokenizer = tokenizador
        # if not balanceamento_parn(code):
        #     raise ValueError("Parenteses inválidos")
        self.tokenizer.selectNext()
        node = self.parseExpression()
        token = self.tokenizer.next
        if token.tipo != 'EOF':
            raise ValueError('Token inválido: ' + self.tokenizer.next.tipo)
        return node

    

# code = sys.argv[1]
# filecode = sys.argv[1]
# with open(filecode, 'r') as file:
#     code = file.read()
code = "3*(2+4)"

parser = Parser()
resultado = parser.run(code)
print(resultado.evaluate())