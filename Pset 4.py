################################################################################
#
# States are represented by 3-tuples of integers in the range 0, ..., k.
#
# Transitions are 2-tuples of states (start_state, end_state), where start_state
# is the start of the transition and end_state is the end of the transition.
#
# Reachable states should be represented by a 3-tuple (state, length, previous)
# where state is the reachable state, length is the length of the path to get
# there, and previous is the previous state. For the 0 length path to the start,
# that would be (start, 0, start).
#
################################################################################

# start is a state, a 3-tuple (x, y, z) where 0 <= x, y, z <= k
# transitions is a list of 2-tuples of 3-tuples (x, y, z)
#   where 0 <= x, y, z <= k.
# Note that the start state is reachable through a path of length 0.
def reachable_states(start, transitions):
    # TODO: Implement part a.
    d = dict()
    for t in transitions:
    	a = t[0]
    	b = t[1]
    	if a not in d:
    		d[a] = [b]
    	else:
    		if b not in d[a]:
	    		d[a] = d[a]+[b]
    visited = set()
    reach = []
    queue = [(start,0,start)]
    while queue:
    	current = queue.pop(0)
    	if current[2] not in visited:
    		visited.add(current[2])
    		reach.append((current[2],current[1],current[0]))
    	if current[2] in d:
	    	for n in d[current[2]]:
	    		if n not in visited:
	    			queue.append((current[2],current[1]+1,n))
    return reach

# Returns either a path as a list of reachable states if the target is
# reachable or False if the target isn't reachable.
def simple_machine(k, start, target):
    # TODO: Implement part b.

    if not target[1]-start[1] == target[2]-start[2]:
    	return False
    else: 
    	queue = [(start,[start])]
    	visited = set()
    	while queue:
    		(current,path) = queue.pop(0)
    		if current == target:
    			return path
    		if current not in visited:
    			visited.add(current)
    			trans=[(current[0]+1,current[1]+1,current[2]+1),(current[0]-1,current[1]-1,current[2]-1),(current[0]+1,current[1],current[2]),(current[0]-1,current[1],current[2])]
    			for t in trans:
    				if t not in visited:
    					queue.append((t,path+[t]))
    	return path

# Returns either False if the mutual exclusion property is satisfied or
# a minimum-length counterexample as a list of reachable states.
def mutual_exclusion_1():
    # TODO: Implement part c.
    queue = [(0,0,1)]
    visited = set()
    transitions = set()
    while queue:
    	current = queue.pop(0)
    	if current[0]==0:
    		trans = (1,current[1],1)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==0:
    		trans = (current[0],1,2)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==1 and current[1]==0:
    		trans = (3,0,current[2])
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[0]==0 and current[1]==1:
    		trans = (0,3,current[2])
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==1 and current[2]==2:
    		trans = (3,current[1],2)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==1 and current[2]==1:
    		trans = (current[0],3,1)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==3:
    		trans = (0,current[1],current[2])
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==3:
    		trans = (current[0],3,current[2])
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    print sorted(list(transitions))
    return exclusionProp((0,0,1),transitions)

def exclusionProp(start,transitions):
    # TODO: Implement part a.
    d = dict()
    for t in transitions:
    	a = t[0]
    	b = t[1]
    	if a not in d:
    		d[a] = [b]
    	else:
    		if b not in d[a]:
	    		d[a] = d[a]+[b]
    #print d

    visited = set()
    queue = [(start,[start])]
    while queue:
    	(current,path) = queue.pop(0)
    	if current[0]==3 and current[1]==3:
    		return path
    	visited.add(current)
    	if current in d:
	    	for n in d[current]:
	    		if n not in visited:
	    			queue.append((n, path+[n]))
    return False

# Returns either False if the mutual exclusion property is satisfied or
# a minimum-length counterexample as a list of reachable states.
def mutual_exclusion_2():
    # TODO: Implement part d.
    queue = [(0,0,0)]
    visited = set()
    transitions = set()
    while queue:
    	current = queue.pop(0)
    	if current[0]==0 and current[2]==0:
    		trans = (1,current[1],0)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==0 and current[2]==0:
    		trans = (current[0],1,0)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==1:
    		trans = (2,current[1],1)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==1:
    		trans = (current[0],2,2)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==2 and current[2]==1:
    		trans = (3,current[1],1)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==2 and current[2]==2:
    		trans = (current[0],3,2)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==2 and not current[2]==1:
    		trans = (0,current[1],current[2])
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==2 and not current[2]==2:
    		trans = (current[0],2,current[2])
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)

    	if current[0]==3:
    		trans = (0,current[1],0)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
    			visited.add(trans)
    	if current[1]==3:
    		trans = (current[0],0,0)
    		transitions.add((current,trans))
    		if trans not in visited:
    			queue.append(trans)
				visited.add(trans)

    #print sorted(list(transitions))
    return exclusionProp((0,0,0),transitions)

trans = [((2,1,1),(2,0,0)),((1,0,2),(2,2,1)),((2,1,0),(0,2,2))]
print reachable_states(0,trans)
#print len(simple_machine(10,(2,3,3),(10,7,7)))
#print mutual_exclusion_2()

