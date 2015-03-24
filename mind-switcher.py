import itertools
from collections import deque, OrderedDict, defaultdict,ValuesView
from pprint import pprint


class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    # def __setitem__(self, key, value):
    #     if value in self:
    #         del self[value]
    #     OrderedDict.__setitem__(self, key, value)
    #     OrderedDict.__setitem__(self,value,key)
        # self.move_to_end(self.get(value,key), False)
def mind_switcher(journal):
    print(journal)
    # whos_who = OrderedDict()
    grps = defaultdict(OrderedDict)
    get_id = lambda swap, c=itertools.count(): next((gid for gid in grps if swap & set(grps[gid].keys())), None) or next(c)
    grp_id = get_id({})
    for x,y in journal:
        whos_who = grps[get_id({x, y})]
        whos_who[x],whos_who[y] = whos_who.get(y,y), whos_who.get(x, x)
        # print(swap, grps[grp_id], 'sset',swap-grps[grp_id])
        # print(set(whos_who.items() - dict(x for x in whos_who.items() if x[0] not in grps[grp_id]).items()))
        # grps[grp_id].update({x: whos_who[x],y:whos_who[y]})

    # print('next',whos_who)
    print('GROUPS from ',journal,':')
    pprint(grps)
    print()
    # if 'nikola' in grps[0]: return
    result = []
    g = {}
    for y in grps.values():
        g.update(y)
        a,b = next(iter(y.items()))
        # print(y)
        # print('testtt', a, y.pop(a))

        # sorted_grp=[y.popitem()]
        # while y:
        #     sorted_grp.append((sorted_grp[-1][1], y.pop(sorted_grp[-1][1])))
        a,b = y.popitem()
        print('the bees',y)
        result.append({'nikola',a})
        while y:
            result.extend([{'sophia',b},{'nikola',b}])
            a,b=b,y.pop(b)

            # if y:

            # print('item',y.popitem())
        result.append({'sophia', b})
        # result.append({'nikola', a})
        # print('the balls', sorted_grp)
        # print('sw', sorted_grp)
        # print('ss', list(zip(*sorted_grp)))
        # j,i=zip(*sorted_grp)
        #
        # print('j',j)
        # print('i',i)
        # pprint(OrderedDict(sorted_grp))
        # e=itertools.cycle([1,-1])
        # a1,b1=sorted_grp.pop(0)
        # result.append({a1,'nikola'})
        # for x,y in sorted_grp:
        #     result.extend([{x,'nikola'},{y,'nikola'}])
        #     result.extend([{x, 'sophia'}, {y, 'sophia'}])
        # print('the result',result)
            # print()
            # while sorted_grp:
            #     result.extend(zip(sorted_grp.pop(),('nikola','sophia')))
            # grps=defaultdict(OrderedDict)
            # for x, y in set((x,y) for x,y in journal)|set(g.items()):
            #     whos_who=grps[get_id({x, y})]
            #     whos_who[x], whos_who[y]=whos_who.get(y, y), whos_who.get(x, x)
            # mind_switcher(result)
            # print('grps2', pprint(grps))
            # print('sorted',sorted_grp)
    # whos_who = OrderedDict(sorted(whos_who.items(), key=lambda x: print(x) or next(id for id in grps if x[0] in grps[id])))
    print('g')
    pprint(g)
    # result = result[-1: ]+result[:-1]
    print('MAX  grps', max(grps))
    if len(grps)%2:result.append({'nikola', 'sophia'})
    j = list(zip(g.items()))
    pprint(print('whos_who') or grps)
    print('j',j)
    # print(list(zip(j.items())))
    print('result',result)
    return result
# test1 =({"scout", "super"},)
test3 =({'scout', 'driller'}, {'scout', 'lister'},
{'hater', 'digger'}, {'planer', 'lister'}, {'super', 'melter'})



# print(tuple({x,y} for x,y in test4))

# print(mind_switcher(test1))
print()
print('---------')
# print(mind_switcher(test3))
from time import sleep
if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    def check_solution(func, data):
        robots = {"nikola": "nikola", "sophia": "sophia"}
        switched = []
        for pair in data:
            switched.append(set(pair))
            r1, r2 = pair
            robots[r1], robots[r2] = robots.get(r2, r2), robots.get(r1, r1)

        result = func(data)
        sleep(.1)
        if not isinstance(result, (list, tuple)) or not all(isinstance(p, set) for p in result):
            print("The result should be a list/tuple of sets.")
            return False
        for pair in result:
            if len(pair) != 2:
                print(1, "Each pair should contain exactly two names.")
                return False
            r1, r2 = pair
            if not isinstance(r1, str) or not isinstance(r2, str):
                print("Names must be strings.")
                return False
            if r1 not in robots.keys():
                print("I don't know '{}'.".format(r1))
                return False
            if r2 not in robots.keys():
                print("I don't know '{}'.".format(r2))
                return False
            if set(pair) in switched:
                print("'{}' and '{}' already were switched.".format(r1, r2))
                return False
            switched.append(set(pair))
            robots[r1], robots[r2] = robots[r2], robots[r1]
        for body, mind in robots.items():
            if body != mind:
                print('<----->')
                pprint(robots)
                print("'{}' has '{}' mind.".format(body, mind))
                sleep(.2)
                return False
        return True

    assert check_solution(mind_switcher, ({"scout", "super"},))
    assert check_solution(mind_switcher, ({'hater', 'scout'}, {'planer', 'hater'}))
    # assert check_solution(mind_switcher, ({'scout', 'driller'}, {'scout', 'lister'},{'hater', 'digger'}, {'planer', 'lister'}, {'super', 'melter'}))
