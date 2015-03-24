from pprint import pprint
from collections import Counter, defaultdict
from random import shuffle


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
        print('forest', len(forest), forest)

        # print('recurse', self.recurse(segments))
        # l=next(forest[s])
        # print('s', s, 'next',self.tie_ends(s,next(forest[s])))

    def recurse(self, segments, cache={}):
        seg=None
        # print(segments)
        for seg in segments:
            next_segs=tuple(x for x in segments if x != seg)
            result=cache.get(next_segs) or cache.setdefault(next_segs, self.recurse(next_segs))
            print(result)
            if result: return self.tie_ends(seg, result)
        return seg

    def has_line(self, line, path):
        a, b=line[:2], line[2:]
        for p in range(1, len(path)):
            if path[p-1:p+1] in ((a, b), (b, a)):
                return True
        return False

    def dfs(self, line, explored=[]):
        # print(line,self.forest[line])
        # ego2 =reduce(self.tie_ends, explored) if len(explored)>1 else self.tuplify(*explored[0])
        # print('eego2',ego2, explored)
        # if not self.get_ends(ego2):return
        # if len(ego2)==self.all:self.ego=self.get_ends(ego2,True)[0];return
        # print(self.get_ends(ego2),'ttttt',ego2)
        if line[::-1] in self.forest:
            print('line', line)
        if self.ego: return
        # k =list(filter(lambda x: self.can_mate(line,x), self.forest))
        # print(k,'k', line)
        # k = sorted(k,key=lambda x: self.spanned(line)[x[0][:2]],reverse=True)
        # if len(k)>1:shuffle(k)
        i=0
        while len(self.forest) > i:
            # try:
            print(len(self.forest), 'length of forest', i)
            i=len(self.forest)
            for x in self.forest[line]:
                e=()
                # print('x',line+x, self.can_mate(line,x), self.can_mate(x,x))
                if len(line)+len(x) >= self.all: self.ego=self.tie_ends(line, x)
                if self.ego: return
                # print(list(reduce(self.tie_ends, line+x)))
                if self.can_mate(x, line[0]):
                    e=x+line
                    try: self.tuplify(e)
                    except: e=line+x
                else:
                    if e and len(e) > 2: print('EEEEEEE', e)
                    e=line+x
                if (e not in self.forest and e[::-1] not in self.forest):
                    # print(self.can_mate(x,line),x, 'ejtjt', e)
                    # amend = set(j for j in self.forest if j not in self.forest[line] and self.can_mate(j, e))
                    amend=set(j for j in self.forest if j not in self.forest[line] and self.can_mate(j, e))
                    if amend:
                        self.forest[e]=self.forest[line]=amend
                        print('the e', len(e), self.all, e)
                        line=e
                        # if e in self.forest: line = e
                        # except: pass

    def get_ends(self, path, with_paths=False):
        ends=[]
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
        new_count.update({x: count[x]-(2*path.count(x)) for i, x in enumerate(path)})
        new_count[path[-1]]+=1
        new_count[path[0]]+=1
        # print(path, new_count, count)
        return cache.setdefault(path, new_count)

    def can_mate(self, path1, path2):
        # print(path1,path2)
        if path1 == path2 or None in (path1, path2):
            return False
        try:
            if path1 in self.forest.get(path2) or path2 in self.forest.get(path1):
                # print('some path1',path1, self.forest.get(path2))
                return True
        except: pass
        # print(path1,'Where it be?', path2)
        try:
            path1=self.tuplify(path1)
            # print('Hello', path1, path2)
            path2=self.tuplify(path2)
            # print('HI', path1, path2)
            legal=self.is_legal(path1) and self.is_legal(path2)
            p1set=self.into_set(path1)
            p2set=self.into_set(path2)
            if p1set & p2set or not legal or path1 == path2 or None in (path1, path2): return False
            # print('testing')
            # print('test', self.tie_ends(path1, path2))
        except:
            print('ERROR in can_mate', path1, path2)
            if path2 == None: print('SHIT'); raise StopIteration
            if path1 == None: print('THIS'); raise StopIteration
            return False
        # if not all([p1set,p2set]):
        # # print('Here', path1,path2)
        #     return False
        # print('path1', path1, 'path2', path2)
        # print(path1)
        return self.tie_ends(path1, path2) and \
               not any([True for x in self.spanned(self.tie_ends(path1, path2)).values() if x < 0])
        # return True
        # return False

    def is_legal(self, fmtd_path):
        if not fmtd_path: return False
        hold=self.into_set(fmtd_path)
        l=len(fmtd_path)
        # print('l',hold)
        # print(2*)
        return hold and l-1 == len(hold)

    def into_set(self, fmtd_path):
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
            else: return False
        return hold

    def tie_ends(self, p1, p2, cache={}):
        # print(p1,p2)
        p1=self.tuplify(p1)
        p2=self.tuplify(p2)
        # if (p1,p2) in cache or (p2,p1) in cache:
        # return cache.get((p1,p2)) or cache.get((p2, p1))
        if p1[-1] == p2[0]: return p1[:-1]+p2
        if p1[-1] == p2[-1]: return p1[:-1]+p2[::-1]
        if p1[0] == p2[0]: return p1[::-1]+p2[1:]
        if p1[0] == p2[-1]: return p2[:-1]+p1

    def tuplify(self, path):
        i=0
        # print(path)
        # if len(path)>4:
        # print('THE PATH', path)
        if path in self._segments:
            # print('something',path)
            i=1
        if isinstance(path[0], tuple) and len(path[0]) > 2:
            # print(path, '???', path[0])
            if i: print('iiii', i)
            # print(path, 'reduce?', reduce(self.tie_ends, path))
            return reduce(self.tie_ends, path) if len(path) > 1 else self.tuplify(path[0])
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


# ((4, 2, 6, 8), (2, 6, 4, 2), (2, 6, 6, 2), (2, 4, 6, 2), (2, 4, 8, 6), (2, 6, 8, 6), (2, 6, 8, 4), (4, 8, 8, 4),
# (2, 6, 4, 8), (2, 4, 2, 6), (2, 4, 4, 2), (4, 2, 8, 6), (6, 2, 8, 6), (6, 8, 6, 2), (6, 8, 8, 6), (8, 4, 8, 6),
# (6, 2, 8, 4), (4, 8, 6, 2), (4, 8, 6, 8), (6, 8, 8, 4), (4, 2, 8, 4), (4, 2, 4, 8), (2, 4, 4, 8), (2, 4, 6, 8),
# (4, 2, 6, 2))

def draw(segments):
    count=Counter()
    i=0
    for s in segments:
        x1, y1, x2, y2=s
        count[x1, y1]+=1
        count[x2, y2]+=1
    paths=set((x,) for x in count if count[x]%2) or set([(x,) for x in count][:1])
    print('paths', paths)

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
        print('i', i, paths)
        add_to_paths=set()
        for y in sorted(paths, key=lambda x: len(x), reverse=True):
            # print('e')
            if y in explored:
                # print('the y',y, explored, len(paths))
                continue
            print(len(y), len(paths), max(paths, key=lambda x: len(x)), 'y', y)
            j+=1
            # print('y and j', paths, y,j)
            paths.remove(y)

            explored.add(y)
            explored.add(y[::-1])
            for x in segments:
                a, b=x[:2], x[2:]
                sp=spanned(y)
                # if len(y)>len(segments)+1:
                # break
                # if any(filter(lambda x: x<0, sp.values())):
                # print('sp',sp)
                #     return
                if len(y) == len(segments)+1 and not any(sp.values()):
                    print('y', y)
                    return y
                # print('spanned', spanned(y), y[-1] == b, spanned(y)[a])
                for p in range(1, len(y)):
                    if y[p-1:p+1] in ((a, b), (b, a)):
                        # print('Happer', (a,b))
                        break
                else:
                    if y[-1] == a and sp[b] != 0:
                        # print('Hi')
                        paths.add(y+(b,))

                    elif y[-1] == b and sp[a] != 0:
                        # print('Hey', y+(a,))
                        # print(paths)
                        paths.add(y+(a,))
                    elif y[0] == b and sp[a] != 0:
                        # print('Hey', y+(a,))
                        # print(paths)
                        paths.add((a,)+y)
                    elif y[0] == a and sp[b] != 0:
                        paths.add((b,)+y)
            break
            if len(paths) != i:
                break
        paths|=add_to_paths
        # print('add to path', add_to_paths, spanned(y), b)
        # paths-=explored
        # for path in paths:
        # print (path)
        # print(spanned(path))
    print(paths)
    print('count', count)
    return []


from functools import reduce


def draw(segments):
    tree=SpanningTree(segments)
    # print('yyo',tree.tuplify(
    # ((4, 2, 6, 8), (2, 6, 4, 2), (2, 6, 6, 2), (2, 4, 6, 2), (2, 4, 8, 6), (2, 6, 8, 6), (2, 6, 8, 4), (4, 8, 8, 4),
    #     (2, 6, 4, 8), (2, 4, 2, 6), (2, 4, 4, 2), (4, 2, 8, 6), (6, 2, 8, 6), (6, 8, 6, 2), (6, 8, 8, 6), (8, 4, 8, 6),
    #     (6, 2, 8, 4), (4, 8, 6, 2), (4, 8, 6, 8), (6, 8, 8, 4), (4, 2, 8, 4), (4, 2, 4, 8), (2, 4, 4, 8), (2, 4, 6, 8))))
    # ends=tree.get_ends
    # paths=tree.paths
    # print
    # print('can it blend?',tree.can_mate(((7, 5, 7, 2), (7, 5, 7, 2), (1, 5, 7, 5), (1, 2, 1, 5), (1, 2, 1, 5)), (1, 2, 1, 5)))
    for x in list(tree.forest):
        result=tree.dfs(x, [x])
        print('segments', segments)
        print('the forest', len(tree.forest), tree.forest)
        print(len(segments), 'nothing', tree.ego)
        return tree.ego
        # print('result', x)
        # if len(result)>=len(segments):
        #     print('path', result, segments)
    #     return result #reduce(tree.tie_ends,result)
    # pprint(tree.forest)
    # print('tuplifying', tree.tuplify((1, 2, 1, 5)), tree.tuplify(((4, 7, 7, 5), (1, 5, 4, 7))))
    # print(tree.can_mate((1, 2, 1, 5), ((4, 7, 7, 5), (1, 5, 4, 7))))
    return tree.ego
    # print(tree.count)
    # path_length =len(segments)+1
    # i=0
    # while len(paths)!=i and len(max(paths, key=len))!=path_length:
    #     i=len(paths)
    #     for path in set(tree.paths):
    #         tree.add_ends(path)
    #     print('path', path, 'ends', ends(path,True))
    # print(len(segments),max(paths, key=len),'p',paths)
    # return max(paths, key=len)


from time import sleep, time

clock=time()

# print(draw({(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}))
# print(draw({(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5), (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2), (1, 5, 7,5)}))
# print(draw([(50, 40, 60, 40), (60, 10, 70, 20), (20, 40, 30, 40), (50, 10, 60, 10), (30, 10, 40, 25),(10, 30, 20, 40), (40, 25, 50, 10), (30, 40, 40, 25), (20, 10, 30, 10), (10, 20, 10, 30),(60, 40, 70, 30), (10, 20, 20, 10), (40, 25, 50, 40), (70, 30, 70, 20)]))
# print(draw([(9,0,9,0)]))

print(draw([(8, 4, 8, 6), (4, 8, 6, 2), (6, 8, 8, 6), (4, 8, 8, 6), (2, 6, 4, 2), (6, 2, 8, 4), (6, 8, 6, 2),(2, 6, 6, 2), (2, 4, 8, 4), (6, 8, 8, 4), (4, 2, 6, 2), (4, 2, 8, 6), (2, 4, 2, 6), (4, 2, 6, 8),(4, 2, 4, 8), (2, 4, 6, 2), (2, 4, 4, 8), (4, 8, 6, 8), (6, 2, 8, 6), (4, 8, 8, 4), (2, 6, 8, 6), (2, 6, 6, 8), (2, 4, 4, 2), (4, 2, 8, 4), (2, 4, 6, 8), (2, 6, 4, 8), (2, 6, 8, 4), (2, 4, 8, 6)]))

# print(draw({(1, 1, 2, 2), (2, 1, 2, 2), (2, 1, 3, 2), (2, 1, 3, 1), (1, 1, 0, 2), (1, 1, 0, 0), (3, 2, 3, 1), (0, 0, 0, 2)}))
# print(draw({(1, 1, 1, 99), (99, 99, 1, 99), (99, 99, 99, 1), (99, 1, 1, 1)}))


if __name__ == '__main__':
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
    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5),
                       (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2), (1, 5, 7, 5)}), "Example 3"
    assert checker(draw, (
        {(1, 1, 2, 2), (2, 1, 2, 2), (2, 1, 3, 2), (2, 1, 3, 1), (1, 1, 0, 2), (1, 1, 0, 0), (3, 2, 3, 1), (0, 0, 0, 2)}))
    assert checker(draw, ({(1, 1, 1, 99), (99, 99, 1, 99), (99, 99, 99, 1), (99, 1, 1, 1)}))
    print('Yatta!')
    # print(checker(draw, ([(8, 4, 8, 6), (4, 8, 6, 2), (6, 8, 8, 6), (4, 8, 8, 6), (2, 6, 4, 2), (6, 2, 8, 4), (6, 8, 6,
    # 2),
    # (2, 6, 6, 2), (2, 4, 8, 4), (6, 8, 8, 4), (4, 2, 6, 2), (4, 2, 8, 6), (2, 4, 2, 6), (4, 2, 6, 8),
    #     (4, 2, 4, 8), (2, 4, 6, 2), (2, 4, 4, 8), (4, 8, 6, 8), (6, 2, 8, 6), (4, 8, 8, 4), (2, 6, 8, 6),
    #     (2, 6, 6, 8), (2, 4, 4, 2), (4, 2, 8, 4), (2, 4, 6, 8), (2, 6, 4, 8), (2, 6, 8, 4), (2, 4, 8, 6)])))

print('Total running time:', time()-clock)