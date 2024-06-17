# from collections import deque

# class Algorithm:
#     @staticmethod
#     def is_puzzle_solved_state(grid):
#         # Check if the puzzle is in a solved state
#         win_pattern = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
#         return grid == win_pattern

#     @staticmethod
#     def get_possible_actions(grid):
#         # Determine possible actions: 'U' (Up), 'R' (Right), 'D' (Down), 'L' (Left)
#         actions = []
#         zero_row, zero_col = Algorithm.find_tile(grid, 0)
#         if zero_row > 0:
#             actions.append((-1, 0))  # Up
#         if zero_row < 2:
#             actions.append((1, 0))  # Down
#         if zero_col > 0:
#             actions.append((0, -1))  # Left
#         if zero_col < 2:
#             actions.append((0, 1))  # Right
#         return actions

#     @staticmethod
#     def find_tile(grid, tile_value):
#         # Find the coordinates of a specific tile value in the grid
#         for i in range(3):
#             for j in range(3):
#                 if grid[i][j] == tile_value:
#                     return i, j

#     @staticmethod
#     def result(grid, action):
#         # Move the empty tile in the given direction
#         new_grid = [row[:] for row in grid]
#         zero_row, zero_col = Algorithm.find_tile(new_grid, 0)
#         move_row, move_col = action
#         new_grid[zero_row][zero_col] = new_grid[zero_row + move_row][zero_col + move_col]
#         new_grid[zero_row + move_row][zero_col + move_col] = 0
#         return new_grid

#     @staticmethod
#     def get_movement_letter(action):
#         # Get the movement letter corresponding to the action
#         if action == (-1, 0):
#             return 'U'
#         elif action == (1, 0):
#             return 'D'
#         elif action == (0, -1):
#             return 'L'
#         elif action == (0, 1):
#             return 'R'

#     @staticmethod
#     def dfs_solution(initial_grid):
#         # Depth-First Search algorithm
#         class State:
#             def __init__(self, grid, actions=''):
#                 self.grid = grid
#                 self.actions = actions

#         frontier = [State(initial_grid)]  # Initialize frontier with the initial state
#         explored = set()  # Set to keep track of explored states

#         while frontier:
#             current_state = frontier.pop()  # Pop the last state (LIFO for DFS)

#             if Algorithm.is_puzzle_solved_state(current_state.grid):
#                 # Puzzle is solved, return the movement letters string
#                 return current_state.actions

#             explored.add(tuple(map(tuple, current_state.grid)))  # Add current state to explored

#             # Generate possible actions for the current state
#             for action in Algorithm.get_possible_actions(current_state.grid):
#                 new_grid = Algorithm.result(current_state.grid, action)
#                 if tuple(map(tuple, new_grid)) not in explored:
#                     # Add the new state to the frontier with the updated actions
#                     frontier.append(State(new_grid, current_state.actions + Algorithm.get_movement_letter(action)))

#         # If no solution found
#         return None

# # Test the DFS solution with the provided initial grid
# initial_grid = [[2, 3, 0], [1, 5, 6], [4, 7, 8]]
# print(Algorithm.dfs_solution(initial_grid))

def DFSearch(initial_state, goal_test, actions, result):
    frontier = [(initial_state, [])]
    explored = set()
    
    while frontier:
        current_state, actions_taken = frontier.pop()
        
        if goal_test(current_state):
            return actions_taken
        
        state_tuple = tuple(tuple(row) for row in current_state)
        if state_tuple not in explored:
            explored.add(state_tuple)
            
            for action in actions(current_state):
                new_state = result(current_state, action)
                new_actions_taken = actions_taken + [action]
                frontier.append((new_state, new_actions_taken))
    
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

