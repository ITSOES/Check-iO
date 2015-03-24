import itertools as it, operator as op, re, string


def subchr(text1, text2, alphabet=string.ascii_uppercase):
    seq1, seq2=[map(alphabet.index, t) for t in (text1, text2)]
    return ''.join(alphabet[i] for i in map(op.sub, seq1, it.cycle(seq2)))


def decode_vigenere(old_decrypted, old_encrypted, new_encrypted):
    keyword=subchr(old_encrypted, old_decrypted)
    match=re.match(r'(?P<repeat>.+)(?P=repeat)|(?P<whole>.+)', keyword)
    return subchr(new_encrypted, match.group('repeat') or match.group('whole'))


# import itertools as it, operator as op, re, string
# ​
# def subchr(text1, text2, alphabet=string.ascii_uppercase):
#     seq1, seq2=[map(alphabet.index, t) for t in (text1, text2)]
#     return ''.join(alphabet[i] for i in map(op.sub, seq1, it.cycle(seq2)))
#
# ​
# def decode_vigenere(old_decrypted, old_encrypted, new_encrypted):
#     keyword=subchr(old_encrypted, old_decrypted)
#     match=re.match(r'(?P.+)(?P=repeat)|(?P.+)', keyword)
#     return subchr(new_encrypted, match.group('repeat') or match.group('whole'))
if __name__ == '__main__':
    assert decode_vigenere('DONTWORRYBEHAPPY',
                           'FVRVGWFTFFGRIDRF',
                           'DLLCZXMFVRVGWFTF') == "BEHAPPYDONTWORRY", "CHECKIO"
    assert decode_vigenere('HELLO', 'OIWWC', 'ICP') == "BYE", "HELLO"
    assert decode_vigenere('LOREMIPSUM',
                           'OCCSDQJEXA',
                           'OCCSDQJEXA') == "LOREMIPSUM", "DOLORIUM"
print(decode_vigenere('DONTWORRYBEHAPPY',
                      'FVRVGWFTFFGRIDRF',
                      'DLLCZXMFVRVGWFTF'))
print(decode_vigenere(
    "DOESNOTWORKINALLCASES",
    "RVSZBVLKQFYTBHZSQHKSU",
    "VLFLOUWLCADWSVTHPYGYGBQLGL"))