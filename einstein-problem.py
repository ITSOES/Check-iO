D = {
    "number": ['1', '2', '3', '4', '5'],
    "color": ['blue', 'green', 'red', 'white', 'yellow'],
    "nationality":  ['Brit', 'Dane', 'German', 'Norwegian', 'Swede'],
    "beverage":  ['beer', 'coffee', 'milk', 'tea', 'water'],
    "cigarettes":  ['Rothmans', 'Dunhill', 'Pall Mall', 'Winfield', 'Marlboro'],
    "pet": ['cat', 'bird', 'dog', 'fish', 'horse']
}

def get_type(name):
    return next(x for x in D if name in D[x])

def answer(relations, question):
    have, find = question.split('-')
    people = [{x:set(y) for x,y in D.items()} for _ in xrange(5)]
    for p, name in zip(people,D[find]):
        p[find] = {name}
    relations = set(frozenset((get_type(x),x) for x in s.split('-')) for s in relations)
    l = 0
    while l <100:
        l += 1
        for x, y in relations:
            for i, p in enumerate(people):
                if len(p[x[0]])==1 and x[1] in p[x[0]] or len(p[y[0]])==1 and y[1] in p[y[0]]:
                    p[x[0]] &= {x[1]}
                    p[y[0]] &= {y[1]}
                    for pp in people[:i] + people[i+1:]:
                        pp[x[0]] -= {x[1]}
                        pp[y[0]] -= {y[1]}
                if x[1] not in p[x[0]] or y[1] not in p[y[0]]:
                    p[y[0]] -= {y[1]}
                    p[x[0]] -= {x[1]}
    return [x[find].pop() for x in people for y in x if have in x[y]][0]
from itertools import product

NUMBERS = ['1', '2', '3', '4', '5']
COLORS = ['blue', 'green', 'red', 'white', 'yellow']
NATIONALITY = ['Brit', 'Dane', 'German', 'Norwegian', 'Swede']
BEVERAGES = ['beer', 'coffee', 'milk', 'tea', 'water']
CIGARETTES = ['Rothmans', 'Dunhill', 'Pall Mall', 'Winfield', 'Marlboro']
PETS = ['cat', 'bird', 'dog', 'fish', 'horse']

ATTRS = [NUMBERS, COLORS, NATIONALITY, BEVERAGES, CIGARETTES, PETS]
QUESTIONS = ["number", "color", "nationality", "beverage", "cigarettes", "pet"]


def answer(relations, question):
    relations = [set(r.split('-')) for r in relations]
    all_patterns = product(*ATTRS)
    houses = (house for house in all_patterns if all(len(set(house) & r) != 1 for r in relations))
    val, name = question.split('-')
    return next(house[QUESTIONS.index(name)]
    for house in houses
        if val in house
             )


if __name__ != '__main__':
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'fish-color') == 'green'  # What is the color of the house where the Fish lives?
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'tea-number') == '2'  # What is the number of the house where tea is favorite beverage?
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'Norwegian-beverage') == 'water'  # What is the favorite beverage of the Norwegian man?
