import sys

#ROTEIRO 7 - string e tipagem



class Node():
    def __init__(self, value, type, symbol_table):
        self.value = value
        self.type = type
        self.children = []
        self.symbol_table = symbol_table
 
class UnOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
        self.children = []

    def evaluate(self):
        if self.value == '+':
            filho = self.children[0].evaluate()
            if filho[1] != 'int':
                raise ValueError('Tipo inválido: ' + filho[1])
            return filho
        elif self.value == '-':
            filho = self.children[0].evaluate()
            if filho[1] != 'int':
                raise ValueError('Tipo inválido: ' + filho[1])

            return (-filho[0], filho[1])

class BinOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
        self.children = []

    def evaluate(self):
        if self.value == '+':
                num1 = self.children[0].evaluate()
                num2 = self.children[1].evaluate()
                if num1[1] != 'int' or num2[1] != 'int':
                    raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
                
                return (int(num1[0] + num2[0]), 'int')
            
        elif self.value == '-':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] - num2[0]), 'int')
        
        elif self.value == '*':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] * num2[0]), 'int')
        elif self.value == '/':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] // num2[0]), 'int')
 
 

class IntVal(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
    
    def evaluate(self):
        return (int(self.value), 'int')
    
class strVal(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
    
    def evaluate(self):
        return (self.value, 'str')

class NoOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        return
    
class Block(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'BLOCK':
            for child in self.children:
                child.evaluate()

class  UnBool(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.value == '!':
                num1 = self.children[0].evaluate()
                if num1[1] != 'int':
                    raise ValueError('Tipo inválido: ' + num1[1])
                return (int(not num1[0]), 'int')

class BinBool(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self): 
        if self.value == '<':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] < num2[0])  , 'int')
        elif self.value == '>':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] > num2[0])  , 'int')
        elif self.value == '==':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != num2[1]:
                raise ValueError('Tipo diferentes: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] == num2[0]), num1[1])
        elif self.value == '&&':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] and num2[0])  , 'int')
        elif self.value == '||':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] or num2[0])  , 'int')
        

class BinStr(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.value == '.':
            num1 = self.children[0].evaluate()
            num2 = self.children[1].evaluate()
            return (str(num1[0]) + str(num2[0]), 'str')
        
class PrintOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'PRINTF':
            print(self.children[0].evaluate()[0])

class ScanfOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'SCANF':
            num1 = input()
            return (int(num1), 'int')

class IfOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'IF':
            if (self.children[0].evaluate()[0]>0):
                self.children[1].evaluate()
            elif len(self.children) == 3:
                self.children[2].evaluate()

class WhileOp(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'WHILE':
            while (self.children[0].evaluate()[0]>0):
                self.children[1].evaluate()

class AssingOP(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'ASSIGN':
            var = self.children[0].value
            value = self.children[1].evaluate()
            self.symbol_table.set(var, value[0], value[1])

class Var(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)

    def evaluate(self):
        if self.type == 'VAR':
            return (self.symbol_table.get(self.value).value, self.symbol_table.get(self.value).type)

class type(Node):
    def __init__(self, value, type, symbol_table):
        super().__init__(value, type, symbol_table)
 
    def evaluate(self):
        if self.type == 'TYPE':
            name = self.children[0].value
            self.symbol_table.create(name, self.value)


class indentifier():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class SymbolTable():
    def __init__(self):
        self.table = {}

    def get (self, key):
        if key not in self.table:
            raise ValueError('Variável não declarada: ' + key)
        if self.table[key].value == None:
            raise ValueError('Variável não inicializada: ' + key)
        return self.table[key]
    def create(self, key, type):
        if key in self.table:
            raise ValueError('Variável já declarada: ' + key)
        self.table[key]= indentifier(type, None)

    def set (self, key, value,type):
        if key not in self.table:
            raise ValueError('Variável não declarada: ' + key)
        if self.table[key].type != type:
            raise ValueError('Tipo inválido: ' + self.table[key].type)
        self.table[key]= indentifier(type, value)
    
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
        elif self.source[self.position] == '.':
            self.position += 1
            self.next = Token('CONCAT', '.')
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
            if self.source[self.position + 1] == '=':
                self.position += 2
                self.next = Token('EQUAL', '==')
                return self.next
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
        elif self.source[self.position] == '<':
            self.position += 1
            self.next = Token('LESS', '<')
            return self.next
        elif self.source[self.position] == '>':
            self.position += 1
            self.next = Token('GREATER', '>')
            return self.next
        elif self.source[self.position] == '!':
            self.position += 1
            self.next = Token('NOT', '!')
            return self.next
        elif self.source[self.position] == '&':
            if self.source[self.position + 1] == '&':
                self.position += 2
                self.next = Token('AND', '&&')
                return self.next
            raise ValueError('Caracter inválido: ' + self.source[self.position])
        elif self.source[self.position] == '|':
            if self.source[self.position + 1] == '|':
                self.position += 2
                self.next = Token('OR', '||')
                return self.next
            raise ValueError('Caracter inválido: ' + self.source[self.position])
    
        elif self.source[self.position] == '"':
            self.position += 1
            start = self.position
            while self.position < len(self.source) and self.source[self.position] != '"':
                self.position += 1
            teste = self.source[self.position]
            if self.source[self.position] != '"':
                raise ValueError('Caracter inválido: ' + self.source[self.position])
            self.next = Token('STR', self.source[start:self.position])
            self.position += 1
            return self.next

        elif self.source[self.position].isalpha():
            start = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            if (self.source[start:self.position] == 'printf'):
                self.next = Token('PRINTF', self.source[start:self.position])
            elif (self.source[start:self.position] == 'scanf'):
                self.next = Token('SCANF', self.source[start:self.position])
            elif (self.source[start:self.position] == 'if'):
                self.next = Token('IF', self.source[start:self.position])
            elif (self.source[start:self.position] == 'else'):
                self.next = Token('ELSE', self.source[start:self.position])
            elif (self.source[start:self.position] == 'while'):
                self.next = Token('WHILE', self.source[start:self.position])
            elif (self.source[start:self.position] == 'int'):
                self.next = Token('TYPE', self.source[start:self.position])
            elif (self.source[start:self.position] == 'str'):
                self.next = Token('TYPE', self.source[start:self.position])
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
            node = Block("{", "BLOCK", self.table)
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
        if token.tipo == 'VAR':
            self.tokenizer.selectNext()
            var = token.valor
            token = self.tokenizer.next
            if token.tipo != 'ASSIGN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            no = AssingOP(token.valor, token.tipo, self.table)
            no.children.append(Var(var, token.tipo, self.table))
            no.children.append(self.orExpr())
            token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return no
        if token.tipo == 'TYPE':
            self.tokenizer.selectNext()
            no = type(token.valor, token.tipo, self.table)
            token = self.tokenizer.next
            if token.tipo != 'VAR':
                raise ValueError('Token inválido: ' + token.tipo)
            no.children.append(Var(token.valor, token.tipo, self.table))
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            return no
        elif token.tipo == 'LBRACE':
            return self.parserBlock()
        elif token.tipo == 'SEMICOLON':
            self.tokenizer.selectNext()
            return NoOp(";", "SEMICOLON", self.table)
        elif token.tipo == 'PRINTF':
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            no = PrintOp("printf","PRINTF", self.table)    
            no.children.append(self.orExpr())            
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return no
        elif token.tipo == 'IF':
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            no = IfOp("if","IF", self.table)
            no.children.append(self.orExpr())
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            no.children.append(self.parserCommand())
            token = self.tokenizer.next
            if token.tipo == 'ELSE':
                self.tokenizer.selectNext()
                no.children.append(self.parserCommand())
            return no
        elif token.tipo == 'WHILE':
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            no = WhileOp("while","WHILE", self.table)
            no.children.append(self.orExpr())
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            no.children.append(self.parserCommand())
            token = self.tokenizer.next
            return no         

        else:
            raise ValueError('Token inválido: ' + token.tipo)
        


    def parseFactor(self):
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'INT':
            return IntVal(token.valor, token.tipo, self.table)
        elif token.tipo == 'MINUS' or token.tipo == 'PLUS':
            no = UnOp(token.valor, token.tipo, self.table)
            no.children.append(self.parseFactor())
            return no
        elif token.tipo == 'NOT':
            no = UnBool(token.valor, token.tipo, self.table)
            no.children.append(self.parseFactor())
            return no
        elif token.tipo == 'VAR':
            return Var(token.valor, token.tipo, self.table)
        elif token.tipo == 'SCANF':
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return ScanfOp("scanf", "SCANF", self.table)
        elif token.tipo == 'STR':
            return strVal(token.valor, token.tipo, self.table)
        elif token.tipo == 'LPAREN':
            resultado = self.orExpr()
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
            token = self.tokenizer.next
        return node
    
    def parserConcat(self):
        node = self.parseExpression()
        token = self.tokenizer.next
        while token.tipo == 'CONCAT':
            self.tokenizer.selectNext()
            op = BinStr(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.parseTerm())
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

    def relExpr(self):
        node = self.parserConcat()
        token = self.tokenizer.next
        while token.tipo == 'LESS' or token.tipo == 'GREATER':
            self.tokenizer.selectNext()
            op = BinBool(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.parseExpression())
            token = self.tokenizer.next
        return node
    
    def eqExpr(self):
        node = self.relExpr()
        token = self.tokenizer.next
        while token.tipo == 'EQUAL':
            self.tokenizer.selectNext()
            op = BinBool(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.relExpr())
            token = self.tokenizer.next
        return node
    
    def andExpr(self):
        node = self.eqExpr()
        token = self.tokenizer.next
        while token.tipo == 'AND':
            self.tokenizer.selectNext()
            op = BinBool(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.eqExpr())
            token = self.tokenizer.next
        return node
    
    def orExpr(self):
        node = self.andExpr()
        token = self.tokenizer.next
        while token.tipo == 'OR':
            self.tokenizer.selectNext()
            op = BinBool(token.valor, token.tipo, self.table)
            op.children.append(node)
            node = op
            node.children.append(self.andExpr())
            token = self.tokenizer.next
        return node
    
    

    def run(self, code):
        tokenizador = Tokenizer(code)
        self.tokenizer = tokenizador
        self.table = SymbolTable()
        self.tokenizer.selectNext()
        node = self.parserBlock()
        token = self.tokenizer.next
        if token.tipo != 'EOF':
            raise ValueError('Token inválido: ' + self.tokenizer.next.tipo)
        return node

    
if __name__ == '__main__':
    code = sys.argv[1]
    filecode = sys.argv[1]
    with open(filecode, 'r') as file:
       code = file.read()
#     code = """
        
 
#   {
#     /* v2.2 testing */
#     int x_1;
    
#     x_1 = scanf();
#     if ((x_1 > 1) && !(x_1 < 1)) {
#         x_1 = 3;
#     }
#     else {
#         {
#         x_1 = (-20+30)*4*3/40;;;;; /* teste de comentario */
#         }
#     }
#     printf(x_1);
#     x_1 = scanf();
#     if ((x_1 > 1) && !(x_1 < 1))
#         x_1 = 3;
#     else
#         x_1 = (-20+30)*12/40;;;;;

#     printf(x_1);
#     while ((x_1 > 1) || (x_1 == 1)) {x_1 = x_1 - 1;printf(x_1);}}
#         """

    parser = Parser()

    resultado = parser.run(code)
    resultado.evaluate()