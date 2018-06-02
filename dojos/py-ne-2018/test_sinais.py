import pytest
import io
from sinais import analisar_linha, analisar_documento, buscar
from sinais import formatar, main


@pytest.fixture
def documento():
    return io.StringIO('0041;LATIN CAPITAL LETTER A;Lu;0;L;;;;;N;;;;0061;\n'
                       '0042;LATIN CAPITAL LETTER B;Lu;0;L;;;;;N;;;;0062;\n')

def test_analisar_documento(documento):
    resultado = analisar_documento(documento)
    assert resultado == [('0041', 'LATIN CAPITAL LETTER A'),
                         ('0042', 'LATIN CAPITAL LETTER B')]

def test_analisar_linha():
    linha = '0041;LATIN CAPITAL LETTER A;Lu;0;L;;;;;N;;;;0061;'
    codigo, nome = analisar_linha(linha)
    assert codigo == '0041'
    assert nome == 'LATIN CAPITAL LETTER A'

def test_buscar_latin(documento):
    busca = buscar('LATIN', analisar_documento(documento))
    assert busca == [('0041', 'LATIN CAPITAL LETTER A'),
                     ('0042', 'LATIN CAPITAL LETTER B')]

def test_buscar_B(documento):
    busca = buscar('B', analisar_documento(documento))
    assert busca == [('0042', 'LATIN CAPITAL LETTER B')]

def test_buscar_b(documento):
    busca = buscar('b', analisar_documento(documento))
    assert busca == [('0042', 'LATIN CAPITAL LETTER B')]

def test_buscar_a(documento):
    busca = buscar('a', analisar_documento(documento))
    assert busca == [('0041', 'LATIN CAPITAL LETTER A')]

def test_buscar_string_vazia(documento):
    busca = buscar('', analisar_documento(documento))
    assert busca == []

def test_buscar_varias(documento):
    busca = buscar('B LETTER', analisar_documento(documento))
    assert busca == [('0042', 'LATIN CAPITAL LETTER B')]

def test_formatar_resultado():
    esperado = ['U+0041\tA\tLATIN CAPITAL LETTER A']
    assert esperado == formatar([('0041', 'LATIN CAPITAL LETTER A')])

def test_formatar_resutado_varios():
    esperado = ['U+0041\tA\tLATIN CAPITAL LETTER A',
                'U+0042\tB\tLATIN CAPITAL LETTER B']
    assert esperado == formatar([('0041', 'LATIN CAPITAL LETTER A'),
                                 ('0042', 'LATIN CAPITAL LETTER B')])

def test_main(capsys):
    main(['registered'])
    captured = capsys.readouterr()
    assert captured.out == "U+00AE\t®\tREGISTERED SIGN\n"
