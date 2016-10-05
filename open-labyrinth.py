#Your code here
#You can import some modules or create additional functions


"""def checkio(map)
    closedset = [] #the empty set    #// The set of nodes already evaluated.
    openset = map    # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = [] #the empty map    #// The map of navigated nodes.
 
    start = (1,1)
    goal = (10,10)
 
    g_score[start] = 0   # // Cost from start along best known path.
    #// Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal)
 
    while openset is not empty
        current = start #the node in openset having the lowest f_score[] value
        if current = goal
            return reconstruct_path(came_from, goal)
 
        remove current from openset
        add current to closedset
        for each neighbor in neighbor_nodes(current)
            if neighbor in closedset
                continue
            tentative_g_score := g_score[current] + dist_between(current,neighbor)
 
            if neighbor not in openset or tentative_g_score < g_score[neighbor] 
                came_from[neighbor] := current
                g_score[neighbor] := tentative_g_score
                f_score[neighbor] := g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                if neighbor not in openset
                    add neighbor to openset
 
    return failure"""
    
longest_path = {}
   
start = (1,1)

def checkio(map, path='', current=start):
    end = (10,10)
    if current==start:
        longest_path["Found"] = "Can't get there!"  #Apparently I can't assume dictionary keys will always return to default values automatically 
    if current == end and (len(longest_path["Found"])*(longest_path["Found"] == "Can't get there!") > len(path) or longest_path["Found"] == "Can't get there!" ):
        print("FOND", path)
        longest_path["Found"] = path
        return path

    map[current[0]][current[1]] = 1

    MOVE = {"S": (1, 0), "N": (-1, 0), "W": (0, -1), "E": (0, 1)}


    
    for x in MOVE:

        test = MOVE.get(x, None)
        move = (current[0]+test[0], current[1]+test[1])

        if map[move[0]][move[1]] == 0:  #If the next space is empty:
            checkio(map, path + x, move)

       


    return longest_path["Found"]
 
"""function reconstruct_path(came_from, current_node)
    if current_node in came_from
        p := reconstruct_path(came_from, came_from[current_node])
        return (p + current_node)
    else
        return current_node"""
    
#print(check_route(maze_map))


from collections import deque

def checkio(maze_map):
    q = deque([(1, 1)])
    path = [[''] * 12 for y in range(0, 12)]
    MOVE = {"S": (1, 0), "N": (-1, 0), "W": (0, -1), "E": (0, 1)}
    while q:
        x, y = q.popleft()
        for dir, (dy, dx) in MOVE.items():
            (nx, ny) = (x + dx, y + dy)
            if maze_map[ny][nx] == 0 and not path[ny][nx]:
                path[ny][nx] = path[y][x] + dir
                q.append((nx, ny))
    print(path)
    return path[10][10]