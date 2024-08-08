import sys

conta = sys.argv[1]


def calculadora(conta):
    res = 0
    num1 = ''
    num2 = ''
    posicao_sinal = []
    conta = conta.replace(" ", "")

    for i in range(len(conta)):
        if conta[i] == "+" or conta[i] == "-":
            posicao_sinal.append(i)

    
    if len(posicao_sinal)<2:
        raise ValueError("Conta inválida")
    for i in range(len(posicao_sinal)):
        if conta[posicao_sinal[i]] +1 == conta[posicao_sinal[i+1]]:
            raise ValueError("Conta inválida")

    for i in range(len(posicao_sinal)):
        if res == 0:
            num1 = conta[0:posicao_sinal[i]]
            if len(posicao_sinal) == i+1:
                num2 = conta[posicao_sinal[i]+1:]
            else:
                num2 = conta[posicao_sinal[i]+1:posicao_sinal[i+1]]
        else:
            num1 = res
            if len(posicao_sinal) == i+1:
                num2 = conta[posicao_sinal[i]+1:]
            else:
                num2 = conta[posicao_sinal[i]+1:posicao_sinal[i+1]]
        if conta[posicao_sinal[i]] == "+":
            res = int(num1) + int(num2)
        if conta[posicao_sinal[i]] == "-":
            res = int(num1) - int(num2)

        
    return res

print(calculadora(conta))