#!/usr/bin/python3

import sys
from flask import Flask, jsonify
from invalidUsage import InvalidUsage

__author__ = 'Gabriel Cantu'


MAX_NUMBER = 99999
ONES = ['', 'um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez',
        'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove']
TWENTIES = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa']
HUNDREDS = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos']


app = Flask(__name__)

#------------------------------------------------------------------------
@app.route('/<path:path>', methods=['GET'])
def extensionNumber(path):

    word = num2word(path)
    print ('FINAL WORD: {}'.format(word))
    return jsonify ({'extenso': word})

#---------------------------------------------------------
def isNegative (number):

    if number < 0: return True
    return False


#---------------------------------------------------------
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

    print ('CANTU 3 - WORD MILS: {}'.format(word))
    return word

#---------------------------------------------------------
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

    print ('CANTU 4 - WORD CENTENAS: {}'.format(word))
    return word

#------------------------------------------------------------------------
def num2word(number):

    try:
        intNumber = int(number)
    except:
        raise InvalidUsage ('Erro ao converter o path recebido para inteiro.')

    if intNumber == 0:
        return 'Zero'

    negative = False
    if isNegative(intNumber):
        negative = True
        intNumber = -intNumber

    if intNumber > MAX_NUMBER:
        raise InvalidUsage ('Numero fora dos limites aceitos.')

    print ('CANTU 0 - NUMERO: {}'.format(intNumber))

    hundreds  = intNumber % 1000
    thousands = (intNumber % 100000) - hundreds

    print ('CANTU 1 - CENTENA: {}'.format(hundreds))
    print ('CANTU 2 - MILHARES: {}'.format(thousands))

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
        finalNumber = 'Menos ' + finalNumber

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

