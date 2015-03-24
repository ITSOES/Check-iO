from pprint import pprint
from collections import Counter, OrderedDict
from random import shuffle
from functools import reduce
from itertools import permutations as perms, combinations as combos, cycle

class SpanningTree:
    def __init__(self, segments):
        self.count=count=Counter()
        self._segments=segments
        self.forest=forest={}
        self.ego=[]
        self.all=len(segments)
        for s in segments:
            x1, y1, x2, y2=s
            count[x1, y1]+=1
            count[x2, y2]+=1
        for s in segments:
            forest[(s,)]=set((x,) for x in segments if x != s and self.can_mate(s, x))
        self.paths=set((x,) for x in count if count[x]%2) or set((x,) for x in count)
        # print('forest', len(forest), forest)
        # print(count)
        for point in count:
            result = (point,)
            while any(self.spanned(result).values()):
                print(len(segments),len(result),result)
                print(self.spanned(result))
                g = list(filter(lambda x: self.is_legal(self.tuplify(result+(x,))), count))
                print(g)

                result+=(max(g, key=self.spanned(result).get),)

            if result:
                self.ego = result
        # print('recurse', self.recurse(segments))
        # i = int(self.all/2)
        # while i>0:
        #     i-=1
        #     for s in combos(segments, i):
        #         # print(s)
        #         egg = reduce(self.tie_ends, s)
        #         if egg:
        #             for n in perms([x for x in segments if x not in s]):
        #                 print(s, 'n', n)
        #                 self.ego = reduce(self.tie_ends, s)
        #                 print(self.ego)
        #                 if self.ego: return
        # l=next(forest[s])
        # print('s', s, 'next',self.tie_ends(s,next(forest[s])))

    def recurse(self,segments, cache={}):
        seg = None
        # print(segments)
        for seg in segments:
            next_segs =tuple(sorted(x for x in segments if x != seg))
            result = cache.get(next_segs) or cache.setdefault(next_segs, self.recurse(next_segs))
            # print(result)
            if result: return self.tie_ends(seg,result)
        return seg
    def has_line(self,line,path):
        a, b=line[:2], line[2:]
        for p in range(1, len(path)):
            if path[p-1:p+1] in ((a, b), (b, a)):
                return True
        return False
    def dfs(self, line, explored=[]):
        if len(self._segments)==1: self.ego=self.tuplify(line)
        if self.ego: return
        # k =list(filter(lambda x: self.can_mate(line,x), self.forest))
        # print(k,'k', line)
        # k = sorted(k,key=lambda x: self.spanned(line)[x[0][:2]],reverse=True)
        # if len(k)>1:shuffle(k)
        i=0
        k = [x for x in self.forest]
        c = cycle([max,min])
        while k:
        # try:
        #     k.sort(key=len,reverse=next(c))
            line = k.pop(k.index(next(c)(k,key=len)))
            # print(len(self.forest), 'length of forest', i)
            i=len(self.forest)
            last = []
            for x in (self.forest[line]):
                    e=()
                    # print('x',line+x, self.can_mate(line,x), self.can_mate(x,x))
                    if len(line)+len(x)>=self.all: self.ego = self.tie_ends(line,x);return
                    if self.ego:return
                    # print(list(reduce(self.tie_ends, line+x)))
                    # print('x',x,'some line', line)
                    if self.tuplify(x+line):
                        e=x+line
                        # print(e)
                        # self.tuplify(e)
                        # except: e=line+x
                    else:
                        if e and len(e)>2: print('EEEEEEE', e)
                        e=line+x

                    if (e not in self.forest and e[::-1] not in self.forest):
                        # print(self.can_mate(x,line),x, 'ejtjt', e)
                        # amend = set(j for j in self.forest if j not in self.forest[line] and self.can_mate(j, e))
                        # amend=set(j for j in self.forest if j not in self.forest[line] and self.can_mate(j, e))
                        amend = set()
                        for j in self.forest:
                            if j not in self.forest[line] and self.can_mate(j, e) and j+e not in self.forest and e+j not in self.forest:
                                # print('len(j+e)', len(j+e))
                                j_e = len(j+e)
                                if j_e==self.all:
                                    self.ego=self.tie_ends(j,e)
                                    return
                                else: #if j_e <= (self.all+1)/2:
                                    amend.add(j)
                        if amend:
                            self.forest[e] = amend
                            # self.forest[line].discard(x)
                            # amend.
                            # print('the e', len(e), len(k), self.all, e)
                            # print(self.tuplify(line))
                            # line = e


                            if e not in k and e[::-1] not in k: k.append(e)
                            if len(e) <= (self.all+1)/2:
                                pass
                                # k.insert(0,line)
                                # break
            del self.forest[line]
                                # if e in self.forest: line = e
                                # except: pass
    def get_ends(self, path, with_paths=False):
        ends=[]
        path=self.tuplify(path)
        for x in self._segments:
            a, b=x[:2], x[2:]
            if not self.has_line(x, path):
                if with_paths:
                    if path[-1] == a:
                        ends.append(path+(b,))
                    elif path[-1] == b:
                        ends.append(path+(a,))
                    elif path[0] == a:
                        ends.append((b,)+path)
                    elif path[0] == b:
                        ends.append((a,)+path)
                elif path[-1] == a:
                    ends.append([b])
                elif path[-1] == b:
                    ends.append([a])
                elif path[0] == a:
                    ends.append([b])
                elif path[0] == b:
                    ends.append([a])
        return ends

    def add_ends(self, path):
        for y in self.get_ends(path, True):
            if y[::-1] not in self.paths:
                self.paths.add(y)
            for x in set(self.paths):
                if self.can_mate(y, x):
                    h=self.tie_ends(y, x)
                    # print('Heey', h)
                    # print(self.paths)
                    if h[::-1] not in self.paths:
                        # print('MAAN')
                        self.paths.add(h)

                        # print(self.paths)


    def spanned(self, path, cache={}):
        count=self.count
        path=self.tuplify(path)
        if path in cache:
            return cache[path]
        new_count=dict(count)
        new_count.update({x: count[x]-(2*path.count(x)) for x in set(path)})
        new_count[path[-1]]+=1
        new_count[path[0]]+=1
        # print(path, new_count, count)
        return cache.setdefault(path, new_count)

    def can_mate(self, path1, path2):
        # print(path1,path2)
        if path1==path2 or None in (path1,path2):
            return False
        try:
            if path1 in self.forest.get(path2) or path2 in self.forest.get(path1):
                # print('some path1',path1, self.forest.get(path2))
                return True
        except:pass
        # w = (self.tuplify(path2))
        # if not w:
        #     print('MORE ERROR', w)
        #     raise StopIteration
        # print(path1,'Where it be?', path2)
        path1=self.tuplify(path1)
        path2=self.tuplify(path2)
        p2set = self.into_set(path2)
        p1set = self.into_set(path1)
        legal = self.is_legal(path1) and self.is_legal(path2)
        if None in (path1, path2) or False in (p1set,p2set): print('THERE IS A NONE', path1,path2, p1set, p2set)
        # print('sets',p1set, p2set)
        if not legal or p1set & p2set or path1 == path2 or None in (path1, path2): return False
        try:
            pass
            # print('Hello', path1, path2)
            # print('HI', path1, path2)
            # print('testing')
            # print('test', self.tie_ends(path1, path2))
            if path2 == None: print('SHIT'); raise StopIteration
            if path1 == None: print('THIS'); raise StopIteration
        except:
            print('ERROR in can_mate', path1, path2)
            return False
        # if not all([p1set,p2set]):
        #     # print('Here', path1,path2)
        #     return False
        # print('path1', path1, 'path2', path2)
        # print(path1)
        return self.tie_ends(path1,path2) and \
               not any([True for x in self.spanned(self.tie_ends(path1, path2)).values() if x < 0])
        # return True
        # return False

    def is_legal(self,fmtd_path):
        if not fmtd_path: return False
        hold = self.into_set(fmtd_path)
        l = len(fmtd_path)
        # print('l',hold)
        # print(2*)
        return hold and l-1 == len(hold)

    def into_set(self,fmtd_path):
        hold=set()
        l=len(fmtd_path)
        # print('l',l)
        for i in range(1, l):
            # print(fmtd_path, i)
            x, y=fmtd_path[i-1:i+1]
            # print(x,y)
            if x == y: return False
            if (x+y) in self._segments:
                hold.add((x+y))
            elif (y+x) in self._segments:
                hold.add(y+x)
            else:
                # print('fmtd_path', x, y, fmtd_path)
                return False
        return hold

    def tie_ends(self, p1, p2, cache={}):
        # print(p1,p2)
        if not (p1 and p2): return ()
        p1=self.tuplify(p1)
        p2=self.tuplify(p2)
        # if (p1,p2) in cache or (p2,p1) in cache:
        #     return cache.get((p1,p2)) or cache.get((p2, p1))
        # print('tie ends', p1, p2, p1[::-1]+p2[-2::-1])
        if p1[-1] == p2[0]: return p1[:-1]+p2
        if p1[-1] == p2[-1]: return p1[:-1]+p2[::-1]
        # if p1[0] == p2[-1]: return  p2[:-1]+p1
        if p1[0] == p2[-1]: return p1[::-1]+p2[-2::-1]
        if p1[0] == p2[0]: return p1[::-1]+p2[1:]
        return ()

    def tuplify(self,path):
        i=0
        # if not path: return ()
        # print(path)
        # if len(path)>4:
            # print('THE PATH', path)
        if path in self._segments:i=1
        if isinstance(path[0], tuple) and len(path[0])>2:
            if i:print('iiii', i)
            if len(path) == 1: return self.tuplify(path[0])
            result = self.tie_ends(*path[:2])
            # print(result, 'resere', path)
            if len(path) == 2 or not result: return result
            for p in path[2:]:
                p = self.tuplify(p)
                # print('tupe',result, p)
                if p[0] == result[-1]: result += (p[1],)
                elif p[1] == result[-1]: result += (p[0],)
                else: return ()
            if not self.is_legal(result): print('R', path, 'RESULT', result)
            return result
            # print(path, 'reduce?', reduce(self.tie_ends, path))
            # return reduce(self.tie_ends, path) if len(path)>1 else self.tuplify(path[0])
        return path if isinstance(path[0], tuple) else tuple(zip(path[::2], path[1::2]))

def draw(segments):
    count=Counter()
    print(segments)
    for s in segments:
        x1, y1, x2, y2=s
        count[x1, y1]+=1
        count[x2, y2]+=1
        # print(s, count)
    spanner={}

    def spanned(paths):
        for y in paths:
            print('y', y)
        ref={x: count[x]-paths.count(x) for y in paths for z in y for x in z}
        return ref

    print('edge', sorted(count, key=lambda x: count[x]))
    print(count)
    # segments = sorted(segments, key=lambda x: count[x[:2]])
    paths=[]
    for point in sorted(count, key=lambda x: count[x]):
        heap=[]
        if count[point]%2:
            heap.append([point, [], []])
        while heap:
            # print(heap)
            # heap = sorted(heap,key=lambda x: len(x[2]))
            print('paths', paths, spanned(paths))
            next, explored, path=heap.pop()
            if len(path) >= len(segments):
                print('path', path+[next])
                return path+[next]
            ff=filter(lambda x: x not in explored, sorted(segments, key=lambda x: count[x[:2]]))
            ss=set()
            for s in ff:
                a, b=s[:2], s[2:]
                if a == next and [path+[next]+[b]] not in paths:
                    count[a]-=1
                    heap.append([b, explored+[s], path+[next]])
                    paths.append([path+[next]+[b]])
                    # break
                elif b == next and [path+[next]+[a]] not in paths:
                    count[b]-=1
                    heap.append([a, explored+[s], path+[next]])
                    paths.append([path+[next]+[a]])
                    # break
    return []


def draw(segments):
    count=Counter()
    i=0
    for s in segments:
        x1, y1, x2, y2=s
        count[x1, y1]+=1
        count[x2, y2]+=1
    paths=list((x,) for x in count if count[x]%2) or list([(x,) for x in count][:1])
    print('paths', paths)
    length = len(segments)
    def spanned(path, cache={}):
        if path in cache:
            return cache[path]
        new_count=dict(count)
        new_count.update({x: count[x]-(2*path.count(x)) for i, x in enumerate(path)})
        new_count[path[-1]]+=1
        new_count[path[0]]+=1
        return cache.setdefault(path, new_count)

    j=0
    explored=set()
    while paths:
        i=len(paths)
        # add_to_paths=set()
        y = paths.pop()[::-1]
        print(length, 'i', i, len(y), len(explored), paths)
        # for y in list(paths): # sorted(paths, key=lambda x: len(x), reverse=True):
            # print('e')
            # paths.remove(y)
        if y in explored or y[::-1] in explored or y in paths or y[::-1] in paths:
            # print('the y',y, explored, len(paths))
            continue
        if len(y) == length+1: # and not any(sp.values()):
            print('y', y)
            return y
        # print(len(y), len(paths), max(paths, key=lambda x: len(x)), 'y', y)
        j+=1
        # print('y and j', paths, y,j)

        for x in segments:
            # print('spanned', spanned(y), y[-1] == b, spanned(y)[a])
            a, b=x[:2], x[2:]
            sp=spanned(y)
            # if len(y)>len(segments)+1:
            # break
            # if any(filter(lambda x: x<0, sp.values())):
            #     print('sp',sp)
            #     return
            for p in range(1, len(y)):
                if y[p-1:p+1] in ((a, b), (b, a)):
                    # print('Happer', (a,b))
                    break
            else:
                if y[-1] == a and sp[b] != 0:
                    # print('Hi')
                    paths.append(y+(b,))

                elif y[-1] == b and sp[a] != 0:
                    # print('Hey', y+(a,))
                    # print(paths)
                    paths.append(y+(a,))
                elif y[0] == b and sp[a] != 0:
                    # print('Hey', y+(a,))
                    # print(paths)
                    paths.append((a,)+y)
                elif y[0] == a and sp[b] != 0:
                    paths.append((b,)+y)
        # explored.add(y[::-1])
        explored.add(y)
        # break
        #     if len(paths)!=i:
        #         break
        # paths|=add_to_paths
        # print('add to path', add_to_paths, spanned(y), b)
        # paths-=explored
        # for path in paths:
        # print (path)f
        #     print(spanned(path))
    # print(paths)
    print('count', count)
    return []




def draw(segments):
    x = list(segments)[0]
    tree=SpanningTree(segments)
    tuplify = tree.tuplify
    if len(segments)==3:return tuplify(tuple(segments))
    if len(list(filter(lambda x: x%2,tree.count.values())))>2: return ()
    if tree.ego: return tree.ego

    # for x in list(tree.forest):
    #     tree.dfs(x, [x])
    #     if tree.ego: break
    result = tree.dfs(x,[x])
    # print('segments', segments)
    # print('the forest', len(tree.forest), tree.forest)
    # print(len(segments), 'nothing', tree.ego)
    # print('TUPE', tree.tuplify(((4,7,7,5), (4,7,7,5))), tree.is_legal(tuplify(((4,7,7,5),(4,7,7,5)))))
    if False:
        for path in tree.forest:
            print(path)
            print(tree.tuplify(path))
    return tree.ego

import collections
from itertools import chain
class Tree(collections.MutableMapping, dict):
    def __init__(self, segments, head=()):
        # print('seg and heads', segments, head)
        self.store = {}
        self._segs = segments
        self._head = head
        self.count = Counter(chain.from_iterable(segments)) #[p for s in self._segs for p in s])
        # print(self.count)
        if head and head[-1] in self.count: self.count.pop(head[-1])
    def __iter__(self):
        for p in self.count:
            self[p]
            yield p

    def __getitem__(self, item):
        print('iiiiiihu',self._head, item)
        if item in self.store: return self.store[item]

        elif item in self.count:
            h=(self._head+(item,))
            h1=h[-2:]
            next_segs =self._segs-{h1, h1[::-1]}
            if len(next_segs)<len(self._segs) or not self._head:
                # self.__dict__[item]=
                self[item]=j=Tree(self._segs-{h1, h1[::-1]}, h)
                # print('li',self.store)

                # self.__setitem__(item,j)
                return j
                # return self[item]
            print('h1', h1)
            if h1 in self._segs:
                return Tree(self._segs - {h1, h1[::-1]}, h)
            # return self[item]
        # else: return self._head

    def __repr__(self): return 'TREE' + str(self.store)

    def __setitem__(self, key, value):
        self.store[key] = value
    # def __repr__(self):
    #     return 'Tree.head( '+str(self._head or 'start') +' )'



def draw(segments):
    print()
    # print(segments)
    # tree = Tree(set((s[:2], s[2:])[::i] for s in segments for i in (-1, 1)))
    # list(tree)
    # print('treee', tree, tree.count)
    # walk=()
    # for x in tree.count:
    #     t=x
    #     break
    # # t=tree.count.most_common(1)[0][0]
    # print('t and tree', t, tree)
    # h = list(tree.count)
    # while len(walk)<=len(segments) and t:
    #     if not walk: t = h.pop()
    #     for x in tree[t]:
    #         walk=tree[x]._head
    #         print('x',x)
    #         t = x
    #         break
    #     print('nest tree', tree[t])
    #     break
    #
    # print('walker',t,'-',walk,'-',tree)
    #
    # return walk



    c = Counter #lambda x: Counter(list(x))
    count = c([(x, y) for s in segments for x, y in (s[:2], s[2:])])
    ends = {x:[] for x in count if count[x]%2}
    if len(ends)>2:return ()
    points = OrderedDict(ends)
    # while any(count.values()):
    print('count', count)
    print('ends', ends)

    _countit =lambda x: sum(count[y]%2 and count[y] for y in (x[:2], x[2:]))
    # something = sorted(something, key=lambda x: something.count(x))
    segments = sorted(segments, key=lambda x:x[2:])
    segments = sorted(segments, key=lambda x: any([y in ends for y in (x[:2], x[2:])]), reverse=True)
    if len([True for x in points if len(x) % 2])>2: return ()
    # for y in segments:
    #     print('y',y, _countit(y), count[y[:2]],count[y[2:]])
    # print('seggy', dict(map(lambda x: (x, count[x]),list([y for y in count if count[y]%2]))))
    butt = True
    result=list(ends.keys())
    for x,y,X,Y in segments:
        if (X, Y) in ends and butt or (x,y) in ends and not butt:
            x,y,X,Y=X,Y,x,y
            butt = False

        result.append(0)
        points.setdefault((x, y), []).append(((X, Y)))
        # if (x2,y2) not in points or (x1,y1) in points:
        #     points.setdefault((x1,y1),[]).append(((x1,y1),(x2,y2)))
        # else: points.setdefault((x2, y2), []).append(((x2,y2),(x1, y1)))
    print('New result', result)
    result = []
    # pprint((points))
    for edges in points.values():
        edges.sort(key=lambda x: x in points)
        # for
    print('points',)
    pprint(points)
    # print([x for y in points.values() for x in y])
    for x in points:
        points[x]=[t for e in points[x] for t in [e,x]][:-1]
        temp=[]
        # print('temp',temp)
        while points[x]:
            t2 =points[x].pop(0)
            temp.append(t2)
            # temp.append(x)
            # for d in points.get(t2,[]):
            #
            #     points[x].extend([points[t2].pop()])
            #     x=t2
            #     break
            #     # else: temp.append(x)
        result+=temp
        # print(x, len(points[x]))
    print(any(points.values()), points.values())
    print('result', len(segments), len(result),result)
    return result


OrderedDict([((1, 2), [(7, 2), (1, 5)]), ((4, 7), [(7, 5)]), ((1, 5), [(4, 7)])])

from time import sleep, time
clock = time()
test1, test2, test3, test4 = [0],[0],[0],[0]
test1 = (draw({(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}))
test2 = (draw({(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5), (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2), (1, 5, 7,5)}))
test3 = (draw([(50, 40, 60, 40), (60, 10, 70, 20), (20, 40, 30, 40), (50, 10, 60, 10), (30, 10, 40, 25),(10, 30, 20, 40), (40, 25, 50, 10), (30, 40, 40, 25), (20, 10, 30, 10), (10, 20, 10, 30),(60, 40, 70, 30), (10, 20, 20, 10), (40, 25, 50, 40), (70, 30, 70, 20)]))
test4 =draw({(1, 1, 9, 9)})
# print(draw([(9,0,9,0)]))

# print(draw([(8, 4, 8, 6), (4, 8, 6, 2), (6, 8, 8, 6), (4, 8, 8, 6), (2, 6, 4, 2), (6, 2, 8, 4), (6, 8, 6, 2),(2, 6, 6, 2), (2, 4, 8, 4), (6, 8, 8, 4), (4, 2, 6, 2), (4, 2, 8, 6), (2, 4, 2, 6), (4, 2, 6, 8), (4, 2, 4, 8), (2, 4, 6, 2), (2, 4, 4, 8), (4, 8, 6, 8), (6, 2, 8, 6), (4, 8, 8, 4), (2, 6, 8, 6), (2, 6, 6, 8), (2, 4, 4, 2), (4, 2, 8, 4), (2, 4, 6, 8), (2, 6, 4, 8), (2, 6, 8, 4), (2, 4, 8, 6)]))

# print(draw({(4, 2, 6, 8), (2, 4, 6, 2), (4, 8, 6, 2), (2, 4, 6, 8), (6, 8, 6, 2), (6, 2, 8, 4), (4, 2, 8, 4), (2, 6, 4, 8),(2, 6, 6, 8), (2, 6, 4, 2), (4, 2, 4, 8), (2, 4, 4, 8), (4, 8, 6, 8), (2, 4, 4, 2), (2, 4, 8, 4), (6, 8, 8, 4),(2, 6, 6, 2), (2, 6, 8, 4), (4, 2, 6, 2), (4, 8, 8, 4), (2, 4, 2, 6)}))

# print(draw({(1, 1, 2, 2), (2, 1, 2, 2), (2, 1, 3, 2), (2, 1, 3, 1), (1, 1, 0, 2), (1, 1, 0, 0), (3, 2, 3, 1), (0, 0, 0, 2)}))
print('-------')
# print(draw({(1, 1, 1, 99), (99, 99, 1, 99), (99, 99, 99, 1), (99, 1, 1, 1)}))
print('test1', len(test1) - 1, test1)
print('test2', len(test2) - 1, test2)
print('test3', len(test3) - 1, test3)
print('test4', len(test4)-1, test4)


if __name__ == '__dmain__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    def checker(func, in_data, is_possible=True):
        user_result=func(in_data)
        sleep(.15)
        if not is_possible:
            if user_result:
                print("How did you draw this?")
                return False
            else:
                return True
        if len(user_result) < 2:
            print("More points please.")
            return False
        data=list(in_data)
        for i in range(len(user_result)-1):
            f, s=user_result[i], user_result[i+1]
            if (f+s) in data:
                data.remove(f+s)
            elif (s+f) in data:
                data.remove(s+f)
            else:
                print("The wrong segment {}.".format(f+s))
                return False
        if data:
            print("You forgot about {}.".format(data[0]))
            return False
        return True

    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}), "Example 1"
    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7),
                       (4, 7, 7, 5), (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2)},
                   False), "Example 2"
    assert checker(draw, {(97, 8, 3, 3), (3, 3, 50, 50), (50, 50, 97, 8)})
    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5),
                       (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2), (1, 5, 7, 5)}), "Example 3"
    assert checker(draw, ({(1, 1, 2, 2), (2, 1, 2, 2), (2, 1, 3, 2), (2, 1, 3, 1), (1, 1, 0, 2), (1, 1, 0, 0), (3, 2, 3, 1),(0, 0, 0, 2)}))
    assert checker(draw, ({(1, 1, 1, 99), (99, 99, 1, 99), (99, 99, 99, 1), (99, 1, 1, 1)}))
    # print(checker(draw, ([(8, 4, 8, 6), (4, 8, 6, 2), (6, 8, 8, 6), (4, 8, 8, 6), (2, 6, 4, 2), (6, 2, 8, 4), (6, 8, 6,
    # 2),
    #     (2, 6, 6, 2), (2, 4, 8, 4), (6, 8, 8, 4), (4, 2, 6, 2), (4, 2, 8, 6), (2, 4, 2, 6), (4, 2, 6, 8),
    #     (4, 2, 4, 8), (2, 4, 6, 2), (2, 4, 4, 8), (4, 8, 6, 8), (6, 2, 8, 6), (4, 8, 8, 4), (2, 6, 8, 6),
    #     (2, 6, 6, 8), (2, 4, 4, 2), (4, 2, 8, 4), (2, 4, 6, 8), (2, 6, 4, 8), (2, 6, 8, 4), (2, 4, 8, 6)])))
    print('Yatta!')

print('Total running time:', time()-clock)

from itertools import groupby
from pprint import pprint

items=[
    '3D/Axis',
    '3D/CameraTracker',

    'Color/Invert',
    'Color/Log2Lin',

    'Color/Math/Add',
    'Color/Math/Multiply',

    'Other/Group',
    'Other/NoOp',

    'Views/JoinViews',
    'Views/ShuffleViews',

    'Views/Stereo/Anaglyph',
    'Views/Stereo/ReConverge',
]

msg=lambda g: print(g) or g.lower()

def f(p, t, c):
    s=p.split('/');
    a=s[0];
    b=s[1:]
    if b:
        if a not in c: c[a]={}
        f('/'.join(b), t, c[a])
    else: c[a]=lambda: msg(t)

# menu={}
# for i in items: f(i, i, menu)

def fun(group, items, path):
    sep=lambda i: i.split('/', 1)
    head=[i for i in items if len(sep(i)) == 2]
    print('head', head)
    tail=[i for i in items if len(sep(i)) == 1]
    gv=groupby(sorted(head), lambda i: sep(i)[0])
    return group, dict([(i, path+i) for i in tail]+[fun(g, [sep(i)[1] for i in v], path+g+'/') for g, v in gv])


# menu=dict([fun('menu', items, '')])['menu']
# pprint(menu)
#
# assert menu['3D']['Axis']() == '3d/axis'
# assert menu['Color']['Invert']() == 'color/invert'
# assert menu['Color']['Math']['Add']() == 'color/math/add'
# assert menu['Views']['Stereo']['Anaglyph']() == 'views/stereo/anaglyph'