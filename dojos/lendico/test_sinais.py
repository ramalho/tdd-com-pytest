import pytest
from sinais import reader, search, main

@pytest.fixture
def data():
    return [
        ('U+00AE', '®', 'REGISTERED SIGN'),
        ('U+265D', '♝', 'BLACK CHESS BISHOP'),
        ('U+2657', '♗', 'WHITE CHESS BISHOP')
        ]


def test_registered(data):
    res = ['U+00AE\t®\tREGISTERED SIGN']
    assert list(search('registered', data)) == res


def test_multiple_results(data):
    res = ['U+265D\t♝\tBLACK CHESS BISHOP',
           'U+2657\t♗\tWHITE CHESS BISHOP']
    assert list(search('BISHOP', data)) == res


def test_multiple_words_query(data):
    res =  ['U+265D\t♝\tBLACK CHESS BISHOP',
           'U+2657\t♗\tWHITE CHESS BISHOP']
    assert list(search('BISHOP CHESS', data)) == res


def test_reads_file():
    result = list(reader())
    assert len(result) >= 10000
    expected = 'U+0041', 'A', 'LATIN CAPITAL LETTER A'
    assert expected in result


def test_main_single_result(capsys):
    main('REGISTERED')
    captured = capsys.readouterr()
    assert captured.out == 'U+00AE\t®\tREGISTERED SIGN\n'


def test_main_multiple_results(capsys):
    main('CHESS', 'BLACK')
    captured = capsys.readouterr()
    assert captured.out == '\n'.join([
        'U+265A\t♚\tBLACK CHESS KING',
        'U+265B\t♛\tBLACK CHESS QUEEN',
        'U+265C\t♜\tBLACK CHESS ROOK',
        'U+265D\t♝\tBLACK CHESS BISHOP',
        'U+265E\t♞\tBLACK CHESS KNIGHT',
        'U+265F\t♟\tBLACK CHESS PAWN',
    ]) + '\n'

def test_we_dont_have_result(capsys):
    main('batata')
    captured = capsys.readouterr()
    assert captured.err == 'No results\n'

def test_user_dont_input_anything(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.err == 'Please provide one word or more\n'
