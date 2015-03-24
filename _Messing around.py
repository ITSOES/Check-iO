sadfsdfasdf='d'


class k:
    Help='jump'
    pass

# print(globals())
# print()
# print(dir(__builtins__))
# print()
# print(dir(k))
# print(__build_class__)

jump=k()
jump.fa='sd'
jump.Help='Yo'
# print(k.__dict__)
# print(jump.__dict__, dir(jump))



import re

PASS_RE=re.compile(r"^.{3,20}$")
valid_password=lambda password: PASS_RE.match(password)

print(valid_password('awe'), 'Help')

j=str('jump'
      'when'
      'you%s'%4+'want '
                'to. '
                'Okay?')
print(j)

print(not (False or True))

from itertools import cycle


def sieve(n):
    "Return all primes <= n."
    np1=n+1
    s=list(range(np1))  # leave off `list()` in Python 2
    s[1]=0
    sqrtn=int(round(n**0.5))
    for i in range(2, sqrtn+1):  # use `xrange()` in Python 2
        if s[i]:
            # next line:  use `xrange()` in Python 2
            s[i*i: np1: i]=[0]*len(range(i*i, np1, i))
    return [x for x in s if x]


i=lambda l=cycle([1, 1, -1, -1]): next(l)
r=0
print('here', sieve(100))
print(list(sieve(100)))
# for x in sieve(9000):
# r += 1/x*i()
#     print(x, r)
print()
from functools import reduce, partial;
from operator import xor
from itertools import zip_longest


def tobase(n, base=2):
    result=[]
    while n not in (0,-1):
        n, d=divmod(n, base)
        result.append(d)
    # print('n',n)
    return result+[n]


def basexor(a, b=0, base=2):
    """adds a and b arithmetically while omitting the carry in respect to base
    Doesn't work well with negative numbers.
    basexor(a,b,base) < max([a,b])*base """
    if base == 1: raise ValueError
    x, y=map(partial(tobase, base=base), (a, b))
    print(x,y,'x y')
    g=list(zip_longest(x, y, fillvalue=0 if a*b>0 else -1))
    h=list(map(lambda x: -1 in x and -1 or sum(x)%base, g))
    print('ggg',g[::-1], h,h[:-h.count(-1)+1])

    result=0
    for i, x in enumerate(h):
        result+=x*(base**i)
    return result

a,b=9,-254
print('basexor test:', tobase(-4)[::-1])
print('negative xor test:', basexor(a,b), a^b)
# print(divmod(-3,50))
# print(divmod(-7,5))
# print(divmod(-2, 5))
print()

# base=9
#
# xor10=partial(basexor, base=base)
# test=[900]*base+[23]+[10]*base+[4]
# ans=(reduce(xor10, test, 0))
# print(ans)
# print(tobase(27, base=base)[::-1], 27)
# print(tobase(18, base=base)[::-1], 18)
# print(tobase(23, base=base)[::-1], 23)
# print(tobase(4, base=base)[::-1], 4)
# print(basexor(-3, 4, base=base))

print(bin(reduce(xor, [-1, 1])))
print(bin(3), bin(-2), bin(-3))
print(-2 ^ 3)
print()

t = int('110000101001',2)
b = '{:b}'.format
xorit2 = lambda n: -(-~-n|n)^n
xorit = lambda n: 2**n.bit_length()-1-n
print('t ==',t)
print(b(t), 'ans=='+b(xorit(t)), b(xorit2(t)))
print()
print(b(60),-60-1, b(~60),~t, b((~-t|t)))
print(b(-~t),b((~-t|t)),~t)
print((~-t | t)^t)
print('end')

# y = 6*x+1
# y = 3*x + 1
# y = 2*x + 1
# y = 2*x - 1
# y =  2/3*x + 4/3
# y = x + 1

# y = 4*x + 1
# y = 2*x + 1
# y = 2*x - 1
# y = x + 1

# y = 2*x + 1
# y = x + 1

# y = x + 1
print()
print()
print()
print()
print()

def m_b(x1,y1,x2,y2):
    m = a_b(y1-y2,x1-x2) if x1-x2 else None
    b = a_b(y1)-m*x1 if m!=None else x1
    return m, b

def makeline(m, b=0):
    return '{}*x+{}'.format(m, b)

from fractions import gcd, Fraction as a_b
result = 1

l = 2
m = l**2
f1 = makeline(m,-m*l)
# for x in range(1+l,450,l):
x=1
# print('y='+f1.replace('x', ('('+str(x)+')'))+' == ', y)
# print(g)
def search(exp, x=1, step=1, upper=10,go=False):
    g=1
    print('y='+exp)
    while g == 1 or go:
        x += step
        y = eval(exp)
        g =gcd(y, x)
        print('gcd({},{}) == {}'.format(x,y, g))
        if upper and x > step*upper:
            break
    print()
search(f1, x,l)
# print(bool(a_b(1,1)),a_b(3,2),'slope_lines()', eval(makeline(*m_b(2,3,3,7))), a_b(.5))

kk =m_b(2, 3, 3, 7)
f2 = makeline(*kk)
search(f2,0,upper=5, go=True)
# print(kk)

# r = a_b(1)
# primes = sieve(100000)
# for x in sieve(20):#range(2,20):
#     # r += a_b(1,x)*(x%2or-1)
#     r-= r*a_b(1,x)
#     print(r, 'x=',x,abs(r.numerator) in primes)