def is_solvable(puzzle):
    # Convert 3x3 puzzle into a 1D list
    one_d_puzzle = [tile for row in puzzle for tile in row]
    
    # Count inversions
    inversions = 0
    for i in range(len(one_d_puzzle)):
        for j in range(i + 1, len(one_d_puzzle)):
            if one_d_puzzle[i] > one_d_puzzle[j] and one_d_puzzle[i] != 0 and one_d_puzzle[j] != 0:
                inversions += 1
    
    # Find the row of the blank space (0) from the bottom
    blank_row_from_bottom = 3 - (one_d_puzzle.index(0) // 3)
    
    # Determine solvability
    if inversions % 2 == 0:
        print("Solvable")
        return "Solvable"
    else:
        print("Not Solvable")
        return "Not Solvable"

# # Example usage
# puzzle1 = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, ""]
# ]

# puzzle2 = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [8, 7, 0]
# ]
