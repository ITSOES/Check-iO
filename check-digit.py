def checkio(data):
    print data,  (sum( (ord(x)-48)*2 for x in data if x.isalnum()) )
    added = 0
    for i, c in enumerate(filter(str.isalnum, str(data))):
        if i%2:
            added += (ord(c) - 48)*2
        else:
            added += sum(map(int, str((ord(c)-48)*2)))
    #replace this for solution
    print added
    result = [str(10 - (added % 10)), added]
    print result
    return result

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ != '__main__':
    #assert (checkio(u"799 273 9871") == ["3", 67]), "First Test"
    assert (checkio(u"139-MT") == ["8", 52]), "Second Test"
    assert (checkio(u"123") == ["0", 10]), "Test for zero"
    assert (checkio(u"999_999") == ["6", 54]), "Third Test"
    assert (checkio(u"+61 820 9231 55") == ["3", 37]), "Fourth Test"
    assert (checkio(u"VQ/WEWF/NY/8U") == ["9", 201]), "Fifth Test"

    print("OK, done!")
