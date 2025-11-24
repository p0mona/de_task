from helpers import Parser

def test_parser():
    test_data = [
        {
            'city': "Warsaw",
            'street': "Pereca",
        },
        {
            'city': "Lublin",
            'street': "A. Mickiewicza"
        }
    ]

    result = [
        ('Warsaw', 'Pereca'),
        ('Lublin', 'A. Mickiewicza')
    ]

    parser = Parser()

    parser.cols = ['city', 'street']

    assert result == parser.parse(test_data)