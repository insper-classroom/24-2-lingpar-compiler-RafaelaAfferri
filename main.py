import sys

#AULA 6 - Variáveis, atribuições e blocos de comando



class Node():
    def __init__(self, value, type, symbol_table):
        self.value = value
        self.type = type
        self.children = []
        self.symbol_table = symbol_table

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
        elif self.type == 'PRINTF':
            print(self.children[0].evaluate())
        elif self.type == 'ASSIGN':
            var = self.children[0].value
            value = self.children[1].evaluate()
            self.symbol_table.set(var, value)
        elif self.type == 'VAR':
            if self.value in self.symbol_table.table:
                return  self.symbol_table.get(self.value)
            else:
                raise ValueError('Variável não declarada: ' + self.value)
        elif self.type == 'BLOCK':
            for child in self.children:
                child.evaluate()
            
        else:
            return int(self.value)
        
class UnOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
        self.children = []

class BinOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
        self.children = []

class IntVal(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

class NoOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

class MultOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

class SymbolTable():
    def __init__(self):
        self.table = {}

    def get (self, key):
        return self.table[key]
    
    def set (self, key, value):
        self.table[key] = value
    
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
        elif self.source[self.position] == '=':
            self.position += 1
            self.next = Token('ASSIGN', '=')
            return self.next
        elif self.source[self.position] == '{':
            self.position += 1
            self.next = Token('LBRACE', '{')
            return self.next
        elif self.source[self.position] == '}':
            self.position += 1
            self.next = Token('RBRACE', '}')
            return self.next
        elif self.source[self.position] == ';':
            self.position += 1
            self.next = Token('SEMICOLON', ';')
            return self.next
        elif self.source[self.position].isalpha():
            start = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            if (self.source[start:self.position] == 'printf'):
                self.next = Token('PRINTF', self.source[start:self.position])
            else:
                self.next = Token('VAR', self.source[start:self.position])
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

    def parserBlock(self):
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'LBRACE':
            token = self.tokenizer.next
            node = MultOp("{", "BLOCK", self.table)
            while token.tipo != 'RBRACE':
                if token.tipo == 'EOF':
                    raise ValueError('Token inválido: ' + token.tipo)
                res = self.parserCommand()
                if res != None:
                    node.children.append(res)
                token = self.tokenizer.next
            self.tokenizer.selectNext()
            return node

  

    def parserCommand(self):
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'VAR':
            var = token.valor
            token = self.tokenizer.next
            if token.tipo != 'ASSIGN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            no = BinOp(token.valor, token.tipo, self.table)
            no.children.append(NoOp(var, token.tipo, self.table))
            no.children.append(self.parseExpression())
            token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return no
        elif token.tipo == 'LBRACE':
            return self.parserBlock()
        elif token.tipo == 'SEMICOLON':
            return
        elif token.tipo == 'PRINTF':
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            no = UnOp("printf","PRINTF", self.table)    
            no.children.append(self.parseExpression())            
            # self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return no
        


    def parseFactor(self):
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'INT':
            return IntVal(token.valor, token.tipo, self.table)
        elif token.tipo == 'MINUS' or token.tipo == 'PLUS':
            no = UnOp(token.valor, token.tipo, self.table)
            no.children.append(self.parseFactor())
            return no
        elif token.tipo == 'VAR':
            return NoOp(token.valor, token.tipo, self.table)
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
            op = BinOp(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.parseFactor())
            # token = self.tokenizer.selectNext()  
            token = self.tokenizer.next
        return node

    def parseExpression(self):
        node = self.parseTerm()
        token = self.tokenizer.next
        while token.tipo == 'PLUS' or token.tipo == 'MINUS':
            self.tokenizer.selectNext()
            op = BinOp(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.parseTerm())
            token = self.tokenizer.next
        return node



    def run(self, code):
        tokenizador = Tokenizer(code)
        self.tokenizer = tokenizador
        self.table = SymbolTable()
        # if not balanceamento_parn(code):
        #     raise ValueError("Parenteses inválidos")
        self.tokenizer.selectNext()
        node = self.parserBlock()
        token = self.tokenizer.next
        if token.tipo != 'EOF':
            raise ValueError('Token inválido: ' + self.tokenizer.next.tipo)
        return node

    

code = sys.argv[1]
filecode = sys.argv[1]
with open(filecode, 'r') as file:
    code = file.read()
# code = """
# {
#   printf(3);}"""

parser = Parser()

resultado = parser.run(code)
resultado.evaluate()