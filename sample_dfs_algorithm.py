from copy import deepcopy

# Define the goal state
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, ""]]

def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == "":
                return i, j

def is_goal(state):
    return state == GOAL_STATE

def swap(state, pos1, pos2):
    new_state = deepcopy(state)
    new_state[pos1[0]][pos1[1]], new_state[pos2[0]][pos2[1]] = new_state[pos2[0]][pos2[1]], new_state[pos1[0]][pos1[1]]
    return new_state

def get_neighbors(state):
    neighbors = []
    x, y = get_blank_position(state)
    
    # Define the possible moves in URDL order
    moves = [
        ((x-1, y), (x, y), "D"),  # Up (move blank down)
        ((x, y+1), (x, y), "L"),  # Right (move blank left)
        ((x+1, y), (x, y), "U"),  # Down (move blank up)
        ((x, y-1), (x, y), "R")   # Left (move blank right)
    ]
    
    for (new_x, new_y), (blank_x, blank_y), direction in moves:
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = swap(state, (blank_x, blank_y), (new_x, new_y))
            neighbors.append((new_state, direction))
    
    return neighbors

def solve_puzzle(start_state):
    visited = set()
    stack = [(start_state, [])]  # Stack stores tuples of (state, path)
    
    while stack:
        state, path = stack.pop()
        
        if is_goal(state):
            return path
        
        visited.add(str(state))
        
        for neighbor, direction in get_neighbors(state):
            if str(neighbor) not in visited:
                stack.append((neighbor, path + [direction]))
    
    return None  # Return None if no solution is found

def visualize_solution(start_state, solution):
    state = deepcopy(start_state)
    for move in solution:
        print("Move:", move)
        print_state(state)
        x, y = get_blank_position(state)
        if move == "U" and x > 0:
            state = swap(state, (x, y), (x-1, y))
        elif move == "R" and y < 2:
            state = swap(state, (x, y), (x, y+1))
        elif move == "D" and x < 2:
            state = swap(state, (x, y), (x+1, y))
        elif move == "L" and y > 0:
            state = swap(state, (x, y), (x, y-1))
        else:
            print(f"Invalid move {move} at position ({x}, {y})")
    print("Final state:")
    print_state(state)

def print_state(state):
    for row in state:
        print(row)
    print()

# Example usage
start_state = [[1, 2, 3], [4, 5, 6], [7, "", 8]]
solution = solve_puzzle(start_state)
print("Solution path:", solution)
