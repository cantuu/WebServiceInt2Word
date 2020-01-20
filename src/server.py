#!/usr/bin/python3

import sys
from flask import Flask, jsonify
from invalidUsage import *

__author__ = 'Gabriel Cantu'


MAX_NUMBER = 99999
ONES = ['', 'um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez',
        'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
TWENTIES = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
HUNDREDS = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']


app = Flask(__name__)

#------------------------------------------------------------------------
#----------------------   ERROR HANDLER   -------------------------------
#------------------------------------------------------------------------
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(Exception)
def unhandled_exception(error):
    logger.exception ('EXCECAO NAO TRATADA. ABORTANDO. ERRO: {}'.format(error))
    return "Excecao nao tratada!!", 500

#------------------------------------------------------------------------
#--------------------------   ROUTES   ----------------------------------
#------------------------------------------------------------------------
@app.route('/<path:path>', methods=['GET'])
def extensionNumber(path):

    word = num2word(path)
    print ('Numero extenso: {}'.format(word))
    return jsonify ({'extenso': word})

#---------------------------------------------------------
# Verifica se o numero eh negativo.
def isNegative (number):

    if number < 0: return True
    return False

#---------------------------------------------------------
# Funcao para tratar os numeros mais significantes.
# Nesse caso, trata as milhares e as dezenas de milhares.
def treatThousands (number):

    thousands = int((number%10000)/1000)
    tensOfThousands = int((number%100000 - thousands*1000)/10000)

    word = ''
    sumThousands = thousands + tensOfThousands*10
    if sumThousands < 20:
        word = ONES[sumThousands]
    else:
        word = TWENTIES[tensOfThousands]
        if thousands != 0:
            word = word + ' e ' + ONES[thousands]

    if word != '':
        if word == 'um':
            word = 'mil'
        else:
            word = word + ' mil'

    print ('[treatThousands] - Milhares em extenso: {}'.format(word))
    return word

#--------------------------------------------------------
# Funcao para tratar os numeros menos significantes.
# Trata centenas, dezenas e unidades.
def treatHundreds (number):

    unit=number%10
    tens=int((number%100 - unit)/10)
    hundreds=int((number%1000 - tens*10 - unit)/100)

    if hundreds == 1 and tens == 0 and unit == 0:
        return 'cem'

    wordHundred = ''
    wordHundred = HUNDREDS[hundreds]

    wordTens = ''
    sumTens = unit + tens*10
    if sumTens < 20:
        wordTens = ONES[sumTens]
    else:
        wordTens = TWENTIES[tens]
        if unit != 0:
            wordTens = wordTens + ' e ' + ONES[unit]

    word = ''
    if wordHundred != '':
        word = wordHundred
        if wordTens != '':
            word = word + ' e ' + wordTens
    else:
        if wordTens != '':
            word = wordTens

    print ('[treatHundreds] - Centenas em extenso: {}'.format(word))
    return word

#------------------------------------------------------------------------
# Funcao de conversao do numero inteiro para extenso.
# Verifica se o numero eh um inteiro e esta dentro dos limites estabelecidos
def num2word(number):

    try:
        intNumber = int(number)
    except:
        raise InvalidUsage ('Erro ao converter o path recebido para inteiro.', status_code=400)

    if intNumber == 0:
        return 'Zero'

    negative = False
    if isNegative(intNumber):
        negative = True
        intNumber = -intNumber

    if intNumber > MAX_NUMBER:
        raise InvalidUsage ('Numero fora dos limites aceitos.', status_code=400)

    print ('[num2word] - Numero recebido: {}'.format(intNumber))

    hundreds  = intNumber % 1000
    thousands = (intNumber % 100000) - hundreds

    print ('[num2word] - Centenas: {}'.format(hundreds))
    print ('[num2word] - Milhares: {}'.format(thousands))

    wordThousands = treatThousands(thousands)
    wordHundreds  = treatHundreds (hundreds)

    finalNumber = ''
    if wordThousands != '':
        finalNumber = wordThousands
        if wordHundreds != '':
            finalNumber = finalNumber + ' e ' + wordHundreds
    else:
        if wordHundreds != '':
            finalNumber = wordHundreds

    if negative:
        finalNumber = 'menos ' + finalNumber

    return finalNumber

#------------------------------------------------------------------------
def runFlask():
    print ("Server Online")
    app.run(host='0.0.0.0', port=3000)

#------------------------------------------------------------------------
#-----------------------      MAIN      ---------------------------------
#------------------------------------------------------------------------
if __name__ == '__main__':
    runFlask()

#[EOF]
