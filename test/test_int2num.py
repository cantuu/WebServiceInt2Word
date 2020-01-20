import sys
import json
import pytest

sys.path.append('../src')
from server import *

# Testa a funcao isNegative - Um simples tratamento para validar se o numero passado por parametro eh ou nao negativo
# Funcao eh invocada dentro da funcao num2word
@pytest.mark.parametrize("number,expected", [(-3,True), (98510, False), (-99999,True), (1,False), (0,False)])
def test_verify_number_negative(number, expected):
    assert isNegative(number) == expected

# Testa a funcao treatThousands - Pega os dois numeros mais significativos e trata (milhar e dezena de milhar)
# Funcao eh invocada dentro da funcao num2word
@pytest.mark.parametrize("number,expected", [(1000, "mil"), (100, ""), (0, ""), (99999, "noventa e nove mil"), (11987, "onze mil")])
def test_verify_thousands(number, expected):
    assert treatThousands(number) == expected

# Testa a funcao treatHundreds - Pega os tres numeros menos significativos e traduz (unidade, dezena e centena)
# Funcao eh invocada dentro da funcao num2word
@pytest.mark.parametrize("number,expected", [(100, "cem"), (15, "quinze"), (99541, "quinhentos e quarenta e um"), (10957, "novecentos e cinquenta e sete")])
def test_verify_hundreds(number, expected):
    assert treatHundreds(number) == expected

#---------------------------------------------------------------------------------------------------------
# Teste da funcao num2word - The main function
#---------------------------------------------------------------------------------------------------------

# Vai receber o numero atraves do path da url, e vai traduzir com a ajuda das funcoes testadas acima.
@pytest.mark.parametrize("number,expected", [(1, "um"), (-7, "menos sete"), (26, "vinte e seis"), (-84, "menos oitenta e quatro"),
                                            (657, "seiscentos e cinquenta e sete"), (-785, "menos setecentos e oitenta e cinco"),
                                            (5498, "cinco mil e quatrocentos e noventa e oito"), (-3210, "menos tres mil e duzentos e dez"),
                                            (35798, "trinta e cinco mil e setecentos e noventa e oito"), (-65321, "menos sessenta e cinco mil e trezentos e vinte e um")])
def test_complete_numbers_inside_limits(number, expected):
    assert num2word(number) == expected

# Recebe um numero fora dos limites estabelecidosm e verifica se lanca uma excecao.
@pytest.mark.parametrize("number", [100000, -980723, -100000])
def test_number_out_of_limits(number):
    with pytest.raises(Exception) as e:
        assert num2word(number)

# Recebe na url um path que nao pode ser convertido em inteiro. Verifica se lanca uma excecao.
@pytest.mark.parametrize("number", ["test", "invalidWord", "python"])
def test_number_out_of_limits(number):
    with pytest.raises(Exception) as e:
        assert num2word(number)
