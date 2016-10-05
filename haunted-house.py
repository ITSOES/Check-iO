import collections, heapq

DIRS = {"N": -4, "S": 4, "E": 1, "W": -1}
Node = collections.namedtuple("Node", ["heuristic", 'gheuristic', "step", "tr", "pos", 'gpos', "prev", 'direction'])

def heuristic(pos, goal):
    
    return abs(((pos - 1) % 4) - ((goal - 1) % 4)) + abs((pos-1)//4 - (goal-1)//4)

def checkio(house, stephan, ghost, steps=30):
    
    #g_map = Node(heuristic(ghost, stephan), 30, 0, ghost, None)
    if stephan == 1:
        return "N"
    
    goal = 1
    
    s_map = [Node(heuristic(stephan, goal), -heuristic(ghost, stephan), 30, 0, stephan, ghost, None, None)]
    
    previous = []
    #s_node = []
    
    while s_map:
        
        s_node = heapq.heappop(s_map)
        moves = ''
        previous.append((s_node.pos, s_node.gpos, s_node.tr))
        #print(s_node)
        
        if s_node.pos == goal:
            print("This should execute")
            break
        if s_node.step == 10:
            continue
            
        if (len(house[s_node.pos - 1]) + s_node.pos % 4 == 3 or \
            len(house[s_node.pos - 1]) + (s_node.pos + 1) % 4 == 3) and \
            s_node.prev is not None:
            continue
        
        
        for direction in DIRS:
            
            
            
            move = s_node.pos + DIRS[direction]
            
            
            
            if direction in house[s_node.pos - 1]:   #Checks for walls
                continue
                
            
            elif ((direction == "W" and s_node.pos % 4 == 1) or (direction == "E" and s_node.pos % 4 == 0) or \
                (s_node.pos < 1) or (s_node.pos > 16)) or (direction == "N" and s_node.pos <= 4) or \
                (direction == "S" and s_node.pos >= 13):    #Checks out-of-bounds
                continue 
            
            
            
            ghost_moves = []   
            for gdir in DIRS:

                gmove = s_node.gpos + DIRS[gdir]
                
                """if heuristic(gmove, move) > s_node.gheuristic:
                    print("gmove gets farther", gdir)
                    continue
                
                if gmove == move:
                    continue"""
                
                if gdir in house[s_node.gpos - 1]:   #Checks for walls
                    continue
                    
                elif ((gdir == "W" and s_node.gpos % 4 == 1) or (gdir == "E" and s_node.gpos % 4 == 0) or \
                    (s_node.gpos < 1) or (s_node.gpos > 16)) or (gdir == "N" and s_node.gpos <= 4) or \
                    (gdir == "S" and s_node.gpos >= 13):    #Checks out-of-bounds
                    continue
                else: ghost_moves.append([heuristic(gmove, move), gmove])
                #print(direction, s_node.gpos)
            ghost_moves.sort()
            
            #print("Huh", direction, ghost_moves)
            if ghost_moves[0][1] == move: # and s_node.prev is None:
                continue
            #print("What", direction, gdir)
            if (move, ghost_moves[0][1], s_node.tr + 1) not in previous:
                new_s_node = Node(-(heuristic(move, goal) - ghost_moves[0][0]), -ghost_moves[0][0], s_node.step - 1, s_node.tr + 1, move, ghost_moves[0][1], s_node, direction)
                heapq.heappush(s_map, new_s_node)
            
            if len(ghost_moves) > 1:
                if ghost_moves[0][0] == ghost_moves[1][0] and (move, ghost_moves[1][1], s_node.tr + 1) not in previous:
                    new_s_node = Node(-(heuristic(move, goal) - ghost_moves[1][0]), -ghost_moves[1][0], s_node.step - 1, s_node.tr + 1, move, ghost_moves[1][1], s_node, direction)
    else:
        print("This shouldn't execute", previous)
            
        
        
    print(s_node, "Does it work?")
    
    
    while s_node.prev.prev is not None:
            
            print("Stephan:", s_node.pos, "Ghost", s_node.gpos) 
            s_node = s_node.prev
            #print(s_node.direction, 'direction')
            
    print("Stephan:", s_node.pos, "Ghost", s_node.gpos) 
    print("Stephan:", s_node.prev.pos, "Ghost", s_node.prev.gpos) 
            
    return s_node.direction
            
            
            
        
        

"""def reverse(direction):
    if direction == "N":
        return "S"
    if direction == "S":
        return "N"
    if direction == "E":
        return "W"
    if direction == "W":
        return "E"#"""

"""def heuristic(spaces, pos, goal, starting_value=16, house=[]):
        #print(len(house))
        if not house:
            house = [x*0 for x in range(len(spaces))]
        #print(pos, starting_value)
        house[pos-1] += starting_value*((house[pos-1] < starting_value)+(house[pos-1] >= starting_value))
        
        next_value = (starting_value**(1/2))//1
        
        #mover = ""
        #print (house)
        test = 0
        
        for direction in DIRS:
            
            test = DIRS[direction]
            move = pos + test
            if direction in spaces[pos - 1]:
                #print('pos ran into a closed door. It was hurt.')
                pass
                
            
            elif ((direction == "W" and pos % 4 == 1) or (direction == "E" and pos % 4 == 0) or
                (pos < 1) or (pos > 16)) or (direction == "N" and pos <= 4) or (direction == "S" and pos >= 13):
                pass 
                
            elif pos + test == goal:    #any(map(lambda s, g: s == g + DIRS[direction]*c for c in range(4), stephan, ghost)):
                #print("Goal Close by!")
                house = heuristic(spaces, goal, move, next_value*1.5, house)
                #print (house)
                #house = heuristic(spaces, move, goal, starting_value, house)
                pass
            elif starting_value > 2:
                #print(starting_value, pos)
                house = heuristic(spaces, move, goal, next_value, house)
        if starting_value > 16:        
            #print(house)  
            pass
        return house #heuristic(spaces, move, goal, next_value)
            

def checkio(house, stephan, ghost, steps=30):
        #print(heuristic(house, ghost, stephan))
        test = 0
        ghost_distance = heuristic(house, ghost, stephan, starting_value=320)
        house.extend(['','','','',''])
        house[ghost-1] = "NWSE"
        house[ghost-5] += "S"
        house[(ghost+3)] += "N"
        house[ghost] += "W"
        house[ghost-2] += "E"
        print(house)
        goalh = heuristic(house, 1, 16, starting_value=1280000000000000)
        
        gh = heuristic(house, stephan, 1, starting_value=32)
        influence = list(map((lambda x, y, z: x + y - z), gh, goalh, ghost_distance))
        meh = influence #list(zip([str(x) for x in range(1, len(house)+1)], influence))

        mover = ""
        moves = ("0", -1000)
        print(gh)#
        print("goalh", goalh)
        for direction in DIRS:
            
            test = DIRS[direction] + stephan
            if direction in house[stephan - 1]:
                #print('Stefan ran into a closed door. It was hurt.')
                continue
                
            elif stephan == 1:
                print('Stefan has escaped.')
                return "N"
            
            elif ((direction == "W" and stephan % 4 == 1) or (direction == "E" and stephan % 4 == 0) or
                (stephan < 1) or (stephan > 16)) or (direction == "N" and stephan <= 4) or (direction == "S" and stephan >= 13):
                pass    #print('Stefan has gone out into the darkness.', direction)
                #break
            elif test == ghost:    #any(map(lambda s, g: s == g + DIRS[direction]*c for c in range(4), stephan, ghost)):
                print("Ghost Close by!")
                pass
            elif moves[1] < influence[test-1]:
                mover += direction
                #print(mover, test, influence[test-1], moves, len(influence))
                moves = (direction, influence[test - 1])
        
        #print(moves)#sorted(moves, key= lambda x: x[1]), "sort")
        
        return moves[0]
                
        sx, sy = (stephan - 1) % 4, (stephan - 1) // 4
        ghost_dirs = [ch for ch in "NWES" if ch not in house[ghost - 1]]
        if ghost % 4 == 1 and "W" in ghost_dirs:
            ghost_dirs.remove("W")
        if not ghost % 4 and "E" in ghost_dirs:
            ghost_dirs.remove("E")
        if ghost <= 4 and "N" in ghost_dirs:
            ghost_dirs.remove("N")
        if ghost > 12 and "S" in ghost_dirs:
            ghost_dirs.remove("S")

        ghost_dir, ghost_dist = "", 1000
        for d in ghost_dirs:
                new_ghost = ghost + DIRS[d]
                gx, gy = (new_ghost - 1) % 4, (new_ghost - 1) // 4
                dist = (gx - sx) ** 2 + (gy - sy) ** 2
                if ghost_dist > dist:
                    ghost_dir, ghost_dist = d, dist
                elif ghost_dist == dist:
                    ghost_dir += d
            ghost_move = choice(ghost_dir)
            ghost += DIRS[ghost_move]
            if ghost == stephan:
                print('The ghost caught Stephan.')
                return False
        print("Too many moves.")
        return False#"""

 


if __name__ == '__main__':
    #This part is using only for self-checking and not necessary for auto-testing
    from random import choice

    DIRS = {"N": -4, "S": 4, "E": 1, "W": -1}

    def check_solution(func, house):
        stephan = 16
        ghost = 1
        for step in range(30):
            direction = func(house[:], stephan, ghost)
            if direction in house[stephan - 1]:
                print('Stefan ran into a closed door. It was hurt.')
                return False
            if stephan == 1 and direction == "N":
                print('Stefan has escaped.')
                return True
            stephan += DIRS[direction]
            if ((direction == "W" and stephan % 4 == 0) or (direction == "E" and stephan % 4 == 1) or
                    (stephan < 1) or (stephan > 16)):
                print('Stefan has gone out into the darkness.')
                return False
            sx, sy = (stephan - 1) % 4, (stephan - 1) // 4
            ghost_dirs = [ch for ch in "NWES" if ch not in house[ghost - 1]]
            if ghost % 4 == 1 and "W" in ghost_dirs:
                ghost_dirs.remove("W")
            if not ghost % 4 and "E" in ghost_dirs:
                ghost_dirs.remove("E")
            if ghost <= 4 and "N" in ghost_dirs:
                ghost_dirs.remove("N")
            if ghost > 12 and "S" in ghost_dirs:
                ghost_dirs.remove("S")

            ghost_dir, ghost_dist = "", 1000
            for d in ghost_dirs:
                new_ghost = ghost + DIRS[d]
                gx, gy = (new_ghost - 1) % 4, (new_ghost - 1) // 4
                dist = (gx - sx) ** 2 + (gy - sy) ** 2
                if ghost_dist > dist:
                    ghost_dir, ghost_dist = d, dist
                elif ghost_dist == dist:
                    ghost_dir += d
            ghost_move = choice(ghost_dir)
            ghost += DIRS[ghost_move]
            if ghost == stephan:
                print('The ghost caught Stephan.')
                return False
        print("Too many moves.")
        return False

    assert check_solution(checkio,
                          ["", "S", "S", "",
                           "E", "NW", "NS", "",
                           "E", "WS", "NS", "",
                           "", "N", "N", ""]), "1st example"
    assert check_solution(checkio,
                          ["", "", "", "",
                           "E", "ESW", "ESW", "W",
                           "E", "ENW", "ENW", "W",
                           "", "", "", ""]), "2nd example"
