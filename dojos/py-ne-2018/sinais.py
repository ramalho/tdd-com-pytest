#!/usr/bin/env python3

import sys


def analisar_documento(documento):
    res = []
    for linha in documento:
        res.append(analisar_linha(linha))
    return res


def analisar_linha(linha):
    codigo, nome = linha.split(';')[:2]
    return codigo, nome


def buscar(consulta, registros):
    achados = []
    consulta = set(consulta.upper().split(' '))
    for codigo, nome in registros:
        tokens = set(nome.split(' '))
        if consulta <= tokens:
            achados.append((codigo, nome))
    return achados


def formatar(resultados):
    formatados = [f'U+{codigo}\t{chr(int(codigo, 16))}\t{nome}'
                  for codigo, nome in resultados]
    return formatados


def main(args):
    text_busca = ' '.join(args)
    with open('UnicodeData.txt') as documento:
        resultados = formatar(buscar(text_busca,
                                     analisar_documento(documento)))

    print('\n'.join(resultados))


if __name__ == '__main__':
    main(sys.argv[1:])
