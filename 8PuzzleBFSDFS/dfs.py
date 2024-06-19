def DFSearch(initial_state, goal_test, actions, result, depth_limit):
    frontier = [(initial_state, [], 0)]  # Include depth in the tuple
    explored = set()
    
    while frontier:
        current_state, actions_taken, depth = frontier.pop()
        
        if goal_test(current_state):
            return actions_taken
        
        state_tuple = tuple(tuple(row) for row in current_state)
        if state_tuple not in explored and depth < depth_limit:
            explored.add(state_tuple)
            
            for action in actions(current_state):
                new_state = result(current_state, action)
                new_actions_taken = actions_taken + [action]
                frontier.append((new_state, new_actions_taken, depth + 1))
    
    return None  # Return None if no solution is found

# Define the goal test function
def goal_test(state):
    return state == [[1, 2, 3], [4, 5, 6], [7, 8, ""]]

# Define the actions function
def actions(state):
    # Find the position of the empty cell
    empty_pos = None
    for i in range(3):
        for j in range(3):
            if state[i][j] == "":
                empty_pos = (i, j)
                break
        if empty_pos:
            break
    
    # Define the possible actions based on the empty cell's position
    possible_actions = []
    i, j = empty_pos
    
    if i > 0:  # Can move Up
        possible_actions.append("U")
    if j < 2:  # Can move Right
        possible_actions.append("R")
    if i < 2:  # Can move Down
        possible_actions.append("D")
    if j > 0:  # Can move Left
        possible_actions.append("L")
    
    
    return possible_actions

# Define the result function
def result(state, action):
    import copy
    new_state = copy.deepcopy(state)
    i, j = [(index, row.index("")) for index, row in enumerate(state) if "" in row][0]

    if action == "U":
        new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
    elif action == "R":
        new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
    elif action == "D":
        new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
    elif action == "L":
        new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
    
    
    return new_state

# # Initial state
# initial_state = [[1, 2, 3], [4, 5, ""], [7, 8, 6]]

# # Perform DFS
# solution = DFSearch(initial_state, goal_test, actions, result)
# print("Solution:", solution)

