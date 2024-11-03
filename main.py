import sys

#ROTEIRO 9 - funcao e scope de variavel



class Node():
    def __init__(self, value, type, symbol_table_func):
        self.value = value
        self.type = type
        self.children = []
        self.symbol_table_func = symbol_table_func
 
class UnOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)
        self.children = []

    def evaluate(self, symbol_table_local):
        if self.value == '+':
            filho = self.children[0].evaluate(symbol_table_local)
            if filho[1] != 'int':
                raise ValueError('Tipo inválido: ' + filho[1])
            return filho
        elif self.value == '-':
            filho = self.children[0].evaluate(symbol_table_local)
            if filho[1] != 'int':
                raise ValueError('Tipo inválido: ' + filho[1])

            return (-filho[0], filho[1])

class BinOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)
        self.children = []

    def evaluate(self, symbol_table_local):
        if self.value == '+':
                num1 = self.children[0].evaluate(symbol_table_local)
                num2 = self.children[1].evaluate(symbol_table_local)
                if num1[1] != 'int' or num2[1] != 'int':
                    raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
                
                return (int(num1[0] + num2[0]), 'int')
            
        elif self.value == '-':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] - num2[0]), 'int')
        
        elif self.value == '*':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] * num2[0]), 'int')
        elif self.value == '/':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] // num2[0]), 'int')

class IntVal(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)
    
    def evaluate(self, symbol_table_local):
        return (int(self.value), 'int')
    
class strVal(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)
    
    def evaluate(self, symbol_table_local):
        return (self.value, 'str')

class NoOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        return
    
class Block(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'BLOCK':
            for child in self.children:
                if(child.type == 'RETURN'):
                    return child.evaluate(symbol_table_local)
                else:
                    child.evaluate(symbol_table_local)

class  UnBool(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.value == '!':
                num1 = self.children[0].evaluate(symbol_table_local)
                if num1[1] != 'int':
                    raise ValueError('Tipo inválido: ' + num1[1])
                return (int(not num1[0]), 'int')

class BinBool(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local): 
        if self.value == '<':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] < num2[0])  , 'int')
        elif self.value == '>':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] > num2[0])  , 'int')
        elif self.value == '==':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != num2[1]:
                raise ValueError('Tipo diferentes: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] == num2[0]), num1[1])
        elif self.value == '&&':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] and num2[0])  , 'int')
        elif self.value == '||':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            if num1[1] != 'int' or num2[1] != 'int':
                raise ValueError('Tipo inválido: ' + num1[1] + ' ' + num2[1])
            return (int(num1[0] or num2[0])  , 'int')
        
class BinStr(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.value == '.':
            num1 = self.children[0].evaluate(symbol_table_local)
            num2 = self.children[1].evaluate(symbol_table_local)
            return (str(num1[0]) + str(num2[0]), 'str')
        
class PrintOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'PRINTF':
            print(self.children[0].evaluate(symbol_table_local)[0])

class ScanfOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'SCANF':
            num1 = input()
            return (int(num1), 'int')

class IfOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'IF':
            if (self.children[0].evaluate(symbol_table_local)[0]>0):
                self.children[1].evaluate(symbol_table_local)
            elif len(self.children) == 3:
                self.children[2].evaluate(symbol_table_local)

class WhileOp(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'WHILE':
            while (self.children[0].evaluate(symbol_table_local)[0]>0):
                self.children[1].evaluate(symbol_table_local)

class AssingOP(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'ASSIGN':
            var = self.children[0].value
            value = self.children[1].evaluate(symbol_table_local)
            symbol_table_local.set(var, value[0], value[1])

class Var(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'VAR':
            return (symbol_table_local.get(self.value).value, symbol_table_local.get(self.value).type)

class type(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)
 
    def evaluate(self, symbol_table_local):
        if self.type == 'TYPE':
            for child in self.children:
                name = child.value
                symbol_table_local.create(name, self.value)

class Fdec(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self):
        nome = self.value
        tipo = self.type
        args = self.children[0]
        comando = self.children[1]
        self.symbol_table_func.create(nome, tipo, args, comando)

class returnNode(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        return self.children[0].evaluate(symbol_table_local)

class argDec(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        args = []
        for child in self.children:
            args.append(child.evaluate(symbol_table_local))
        return args

class FCall(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self, symbol_table_local):
        if self.type == 'FCALL':
            func = self.symbol_table_func.get(self.value)
            args = []
            args_value = []
            args_type = []
            for child in self.children:
                args.append(child)
            if len(args) != len(func.args.children):
                raise ValueError('Número de argumentos inválido: ' + str(len(args)) + ' ' + str(len(func.args)))
            for i in range(len(args)):
                if args[i].type == 'VAR':
                    args_type.append(symbol_table_local.get(args[i].value).type)
                    if args_type[i] != func.args.children[i].value:
                        raise ValueError('Tipo de argumento inválido: ' + symbol_table_local.get(args[i].value).type + ' ' + func.args.children[i].value)
                    args_value.append(symbol_table_local.get(args[i].value).value)
                else:
                    args_type.append(args[i].evaluate(symbol_table_local)[1])
                    args_value.append(args[i].evaluate(symbol_table_local)[0])
            symbol_table_local = SymbolTable()
            for i in range(len(args)):
                symbol_table_local.create(func.args.children[i].children[0].value, args_type[i])
                symbol_table_local.set(func.args.children[i].children[0].value, args_value[i], args_type[i])
                
            return func.comands.evaluate(symbol_table_local)

class astNode(Node):
    def __init__(self, value, type, symbol_table_func):
        super().__init__(value, type, symbol_table_func)

    def evaluate(self):
        symbol_table_local = SymbolTable()
        for i in range(len(self.children)-1):
            self.children[i].evaluate()
        self.children[len(self.children)-1].evaluate(symbol_table_local)
class indentifier():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class idFuncao():
    def __init__(self, ret, args, comands):
        self.ret = ret
        self.args = args
        self.comands = comands


class symbolTableFunc():
    def __init__(self):
        self.symbol_table_func = {}

    def create(self, key, ret, args, comands):
        if key in self.symbol_table_func:
            raise ValueError('Função já declarada: ' + key)
        self.symbol_table_func[key]= idFuncao(ret, args, comands)

    def get (self, key):
        if key not in self.symbol_table_func:
            raise ValueError('Função não declarada: ' + key)
        return self.symbol_table_func[key]
        

class SymbolTable():
    def __init__(self):
        self.symbol_table_local = {}

    def get (self, key):
        if key not in self.symbol_table_local:
            raise ValueError('Variável não declarada: ' + str(key))
        if self.symbol_table_local[key].value == None:
            raise ValueError('Variável não inicializada: ' + str(key))
        return self.symbol_table_local[key]
    def create(self, key, type):
        if key in self.symbol_table_local:
            raise ValueError('Variável já declarada: ' + key)
        self.symbol_table_local[key]= indentifier(type, None)

    def set (self, key, value,type):
        if key not in self.symbol_table_local:
            raise ValueError('Variável não declarada: ' + key)
        if self.symbol_table_local[key].type != type:
            raise ValueError('Tipo inválido: ' + self.symbol_table_local[key].type)
        self.symbol_table_local[key]= indentifier(type, value)
    
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
        elif self.source[self.position] == ',':
            self.position += 1
            self.next = Token('COMMA', ',')
            return self.next
        
    
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
            elif (self.source[start:self.position] == 'void'):
                self.next = Token('TYPE', self.source[start:self.position])
            elif (self.source[start:self.position] == 'return'):
                self.next = Token('RETURN', self.source[start:self.position])
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

    def BlockAst(self):
        token = self.tokenizer.next
        no = astNode("AST", "AST", self.symbol_table_func)
        while(token.tipo != 'EOF'):
            no.children.append(self.funcDefBlock())
            self.tokenizer.selectNext()
            token = self.tokenizer.next
        node = FCall("main", "FCALL", self.symbol_table_func)
        no.children.append(node)

        return no
        

    def funcDefBlock(self):

        token = self.tokenizer.next
        if token.tipo == "TYPE":
            tipo = token.valor
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != "VAR":
                raise ValueError('Token inválido: ' + token.tipo)
            func = Fdec(token.valor, tipo, self.symbol_table_func)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != "LPAREN":
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            arg = argDec(func.value, tipo , self.symbol_table_func)
            while token.tipo != "RPAREN":
                if token.tipo == 'EOF':
                    raise ValueError('Token inválido: ' + token.tipo)
                
                if token.tipo != 'TYPE':
                    raise ValueError('Token inválido: ' + token.tipo)
                no = type(token.valor, token.tipo, self.symbol_table_func)

                self.tokenizer.selectNext()
                token = self.tokenizer.next
                if token.tipo != 'VAR':
                    raise ValueError('Token inválido: ' + token.tipo)
                no.children.append(Var(token.valor, token.tipo, self.symbol_table_func))
                arg.children.append(no)

                self.tokenizer.selectNext()
                token = self.tokenizer.next
                if token.tipo == 'COMMA':
                    self.tokenizer.selectNext()
                    token = self.tokenizer.next
            func.children.append(arg)
            self.tokenizer.selectNext()      
            func.children.append(self.parserCommand())
            return func

   
    def parserBlock(self):
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'LBRACE':
            token = self.tokenizer.next
            node = Block("{", "BLOCK", self.symbol_table_func)
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
            if token.tipo == 'ASSIGN':
                
                self.tokenizer.selectNext()
                no = AssingOP(token.valor, token.tipo, self.symbol_table_func)
                no.children.append(Var(var, token.tipo, self.symbol_table_func))
                no.children.append(self.orExpr())
                token = self.tokenizer.next
                if token.tipo != 'SEMICOLON':
                    raise ValueError('Token inválido: ' + token.tipo)
                self.tokenizer.selectNext()
                return no
            elif token.tipo == 'LPAREN':
                self.tokenizer.selectNext()
                no = FCall(var, 'FCALL', self.symbol_table_func)
                token = self.tokenizer.next
                while token.tipo != 'RPAREN':
                    no.children.append(self.orExpr())
                    token = self.tokenizer.next
                    if token.tipo == 'COMMA':
                        self.tokenizer.selectNext()
                        token = self.tokenizer.next
                self.tokenizer.selectNext()
                token = self.tokenizer.next
                if token.tipo != 'SEMICOLON':
                    raise ValueError('Token inválido: ' + token.tipo)
                self.tokenizer.selectNext()
                return no
            else:
                raise ValueError('Token inválido: ' + token.tipo)
        if token.tipo == 'TYPE':
            self.tokenizer.selectNext()
            no = type(token.valor, token.tipo, self.symbol_table_func)
            token = self.tokenizer.next
            if token.tipo != 'VAR':
                raise ValueError('Token inválido: ' + token.tipo)
            no.children.append(Var(token.valor, token.tipo, self.symbol_table_func))
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            while token.tipo == 'COMMA':
                self.tokenizer.selectNext()
                token = self.tokenizer.next
                if token.tipo != 'VAR':
                    raise ValueError('Token inválido: ' + token.tipo)
                no.children.append(Var(token.valor, token.tipo, self.symbol_table_func))
                self.tokenizer.selectNext()
                token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            return no
        elif token.tipo == 'LBRACE':
            return self.parserBlock()
        elif token.tipo == 'SEMICOLON':
            self.tokenizer.selectNext()
            return NoOp(";", "SEMICOLON", self.symbol_table_func)
        elif token.tipo == 'PRINTF':
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            no = PrintOp("printf","PRINTF", self.symbol_table_func)    
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
            no = IfOp("if","IF", self.symbol_table_func)
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
            no = WhileOp("while","WHILE", self.symbol_table_func)
            no.children.append(self.orExpr())
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            no.children.append(self.parserCommand())
            token = self.tokenizer.next
            return no         
        elif token.tipo == 'RETURN':
            self.tokenizer.selectNext()
            no = returnNode("return","RETURN", self.symbol_table_func)
            no.children.append(self.orExpr())
            token = self.tokenizer.next
            if token.tipo != 'SEMICOLON':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return no

        else:
            raise ValueError('Token inválido: ' + token.tipo)
        


    def parseFactor(self):
        token = self.tokenizer.next
        self.tokenizer.selectNext()
        if token.tipo == 'INT':
            return IntVal(token.valor, token.tipo, self.symbol_table_func)
        elif token.tipo == 'MINUS' or token.tipo == 'PLUS':
            no = UnOp(token.valor, token.tipo, self.symbol_table_func)
            no.children.append(self.parseFactor())
            return no
        elif token.tipo == 'NOT':
            no = UnBool(token.valor, token.tipo, self.symbol_table_func)
            no.children.append(self.parseFactor())
            return no
        elif token.tipo == 'VAR':
            no = Var(token.valor, token.tipo, self.symbol_table_func)
            no2 = FCall(token.valor, 'FCALL', self.symbol_table_func)
            token = self.tokenizer.next
            if token.tipo == 'LPAREN':
                self.tokenizer.selectNext()
                token = self.tokenizer.next
                while token.tipo != 'RPAREN':
                    no2.children.append(self.orExpr())
                    token = self.tokenizer.next
                    if token.tipo == 'COMMA':
                        self.tokenizer.selectNext()
                        token = self.tokenizer.next
                self.tokenizer.selectNext()
                return no2
            return no
        elif token.tipo == 'SCANF':
            token = self.tokenizer.next
            if token.tipo != 'LPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            token = self.tokenizer.next
            if token.tipo != 'RPAREN':
                raise ValueError('Token inválido: ' + token.tipo)
            self.tokenizer.selectNext()
            return ScanfOp("scanf", "SCANF", self.symbol_table_func)
        elif token.tipo == 'STR':
            return strVal(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinOp(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinStr(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinOp(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinBool(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinBool(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinBool(token.valor, token.tipo, self.symbol_table_func)
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
            op = BinBool(token.valor, token.tipo, self.symbol_table_func)
            op.children.append(node)
            node = op
            node.children.append(self.andExpr())
            token = self.tokenizer.next
        return node
    
    

    def run(self, code):
        tokenizador = Tokenizer(code)
        self.tokenizer = tokenizador
        self.symbol_table_func = symbolTableFunc()
        self.tokenizer.selectNext()

        node = self.BlockAst()
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
# """

    parser = Parser()

    resultado = parser.run(code)
    resultado.evaluate()
