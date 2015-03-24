def checkio(n,f=''):
    for x in range(9,1,-1):
        while n%x<1:
            f+=str(x)
            n/=x
    return int(n==1and f[::-1])


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    print(checkio(20))
    print(checkio(9973))
    assert checkio(20) == 45, "1st example"
    assert checkio(21) == 37, "2nd example"
    assert checkio(17) == 0, "3rd example"
    assert checkio(33) == 0, "4th example"
    assert checkio(3125) == 55555, "5th example"
    assert checkio(9973) == 0, "6th example"