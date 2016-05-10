# Note that infinity can be represented by float('inf') in Python.

################################################################################
# You do not need to implement anything in this section below.
import math

def dist(loc1, loc2):
    xdiff = loc1[0] - loc2[0]
    ydiff = loc1[1] - loc2[1]
    return math.sqrt(xdiff * xdiff + ydiff * ydiff)

import heapq
import itertools
# Borrowed heavily from https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.REMOVED = '<removed>'
        self.counter = itertools.count()
        self.num_elements = 0
        self.num_actions = 0

    def add(self, item, priority):
        if item in self.entry_finder:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)
        self.num_actions += 1
        self.num_elements += 1

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED
        self.num_elements -= 1

    def pop(self):
        self.num_actions += 1
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                self.num_elements -= 1
                del self.entry_finder[item]
                return item, priority
        raise KeyError('Pop from an empty priority queue')

    def head(self):
        priority, count, item = self.heap[0]
        return item, priority

    def empty(self):
        return self.num_elements == 0

# You do not need to implement anything in this section above.
################################################################################

# TODO: Implement both parts (a) and (b) with this function. If target is None,
# then return a list of tuples as described in part (a). If target is not None,
# then return a path as a list of states as described in part (b).
def dijkstra(n, edges, source, target=None):
    d = dict()
    queue = PriorityQueue()
    d[source] = (0, None)
    for s in edges[source]:
        d[s[0]] = (s[1],[source])
        queue.add(s[0],s[1])
    while not queue.empty():
        u = queue.pop()[0]
        if u == target:
            print queue.num_actions
            return (d[u][1]+[u],d[u][0])
        if u in edges:
            for v in edges[u]:
                if v[0] not in d:
                    w=d[u][0]+v[1]
                    d[v[0]]=(w,d[u][1]+[u])
                    queue.add(v[0],w)
                elif d[u][0]+v[1] < d[v[0]][0]:
                    w=d[u][0]+v[1]
                    d[v[0]]=(w,d[u][1]+[u])
                    queue.add(v[0],w)
    if target==None:
        a = []
        for e in d:
            if d[e][1] == None:
                tup = (e,d[e][0],d[e][1])
            else:
                tup = (e,d[e][0],d[e][1][-1])
            a.append(tup)
        print queue.num_actions
        return sorted(a, key = lambda x: x[1])
    
# TODO: Implement part (c).
def bidirectional(n, edges, source, target):
    q1 = PriorityQueue()
    q2 = PriorityQueue()
    d1 = dict()
    d2 = dict()
    v1 = []
    v2 = []
    short = ([],float('inf'))

    bedges = {}
    for a in edges:
        for b in edges[a]:
            if b[0] not in bedges:
                bedges[b[0]] = [(a,b[1])]
            else:
                bedges[b[0]] = bedges[b[0]]+[(a,b[1])]

    d1[source] = (source,0,[])
    d2[target] = (target,0,[])

    for s in edges[source]:
        d1[s[0]] = (s[0],s[1],[source])
        q1.add(s[0],s[1])
        v1.append(source)

    for t in bedges[target]:
        d2[t[0]]=(t[0],t[1],[target])
        q2.add(t[0],t[1])
        v2.append(target)

    while not q1.empty() and not q2.empty():
        if q1.head()[1]<=q2.head()[1]:
            u=q1.pop()[0]
            v1.append(u)
            if u in v2:
                print q1.num_actions+q2.num_actions
                return short
            if u in edges:
                for v in edges[u]:
                    if v[0] not in d1:
                        w=d1[u][1]+v[1]
                        d1[v[0]]=(v[0],w,d1[u][2]+[u])
                        q1.add(v[0],w)
                    elif d1[u][1]+v[1] < d1[v[0]][1]:
                        w=d1[u][1]+v[1]
                        d1[v[0]]=(v[0],w,d1[u][2]+[u])
                        q1.add(v[0],w)
                    if v[0] in v2:
                        n = d1[v[0]][1]+d2[v[0]][1]
                        if n < short[1]:
                            short = (d1[v[0]][2]+[v[0]]+d2[v[0]][2],n)
        else:
            u=q2.pop()[0]
            v2.append(u)
            if u in v1:
                print q1.num_actions+q2.num_actions
                return short
            if u in edges:
                for v in bedges[u]:
                    if v[0] not in d2:
                        w=d2[u][1]+v[1]
                        d2[v[0]]=(v[0],w,[u]+d2[u][2])
                        q2.add(v[0],w)
                    elif d2[u][1]+v[1] < d2[v[0]][1]:
                        w=d2[u][1]+v[1]
                        d2[v[0]]=(v[0],w,[u]+d2[u][2])
                        q2.add(v[0],w)
                    if v[0] in v1:
                        n = d1[v[0]][1]+d2[v[0]][1]
                        if n < short[1]:
                            short = (d1[v[0]][2]+[v[0]]+d2[v[0]][2],n)

# TODO: Implement part (d).
def astar(locs, edges, source, target):
    d = dict()
    q = PriorityQueue()
    d[source] = (0, None)
    for s in edges[source]:
        d[s] = (dist(locs[source],locs[s]),[source])
        q.add(s,dist(locs[s],locs[target]))
    while not q.empty():
        u = q.pop()[0]
        if u == target:
            print q.num_actions
            return (d[u][1]+[u],d[u][0])
        if u in edges:
            for v in edges[u]:
                w=d[u][0]+dist(locs[u],locs[v])
                if v not in d:
                    d[v]=(w,d[u][1]+[u])
                    q.add(v,d[v][0]+dist(locs[v],locs[target]))
                elif w < d[v][0]:
                    d[v]=(w,d[u][1]+[u])
                    q.add(v,d[v][0]+dist(locs[v],locs[target]))

'''
import csv
trans = dict()
with open('cases/26.in') as f:
    reader = csv.reader(f, delimiter=",")
    reader.next()
    reader.next()
    for x in range(0,10):  
        d=list(reader.next())
        k = int(d.pop(0))
        v = []
        for y in range(len(d)/2):
            v.append((int(d[2*y]),float(d[2*y+1])))
        trans[k]=v
'''

#print trans
#locs = [(0,0),(0,2),(2,0),(1,1),(2,2)]
#trans = {0:[1,2,3],1:[3,4],2:[3,4],3:[4]}
#print dijkstra(10,trans,0)
#print bidirectional(4094,trans,0,2047)
#print astar(locs,trans,0,4)

