import heapq

grid_size = 6
truck_position = (-1, -1)  # truck is outside the grid

# grid with 2 empty rows at the top for temporary storage
initial_grid = [
    ["0", "0", "0", "0", "0", "0"],  # empty row for temporary storage
    ["0", "0", "0", "0", "0", "0"],  # empty row for temporary storage
    ["C01", "C02", "C03", "C04", "C05", "C06"],
    ["C07", "C08", "C09", "C10", "C11", "C12"],
    ["C13", "C14", "C15", "C16", "C17", "C18"],
    ["C19", "C20", "C21", "C22", "C23", "C24"],
    ["C25", "C26", "C27", "C28", "C29", "C30"],
    ["C31", "C32", "C33", "C34", "C35", "C36"]
]

def find_container(grid, container):
    # find the pos of a container in the grid
    for i, row in enumerate(grid):
        if container in row:
            return (i, row.index(container))
    return None

def get_blocking_containers(grid, target_pos):
    # find containers blocking the target container vertically
    row, col = target_pos
    return [(r, col, grid[r][col]) for r in range(row) if grid[r][col] != "0"]

def find_path(grid, target_container, goal):
    # find the optimal moves to transport the target container to the truck
    start_pos = find_container(grid, target_container)
    if not start_pos:
        return None

    blocking = get_blocking_containers(grid, start_pos)
    moves = []

    target_col = start_pos[1]
    temp_cols = [col for col in [target_col - 1, target_col + 1] if 0 <= col < len(grid[0])]
    temp_stack_heights = {col: 1 for col in temp_cols}

    for i, (row, col, container) in enumerate(blocking):
        temp_col = temp_cols[i % len(temp_cols)]
        temp_row = temp_stack_heights[temp_col]
        if temp_row > 1:
            temp_row = 0  
        moves.append(('temp_stack', container, (temp_row, temp_col)))
        temp_stack_heights[temp_col] = 0  
        
    moves.append(('move', target_container, truck_position))

    # return blocking containers to original positions
    for row, col, container in reversed(blocking):
        moves.append(('return', container, (row, col)))

    return moves

def print_grid(grid):
    # print the current grid state
    for row in grid:
        print(row)
    print()

def simulate_moves(grid, moves):
    # sim the moves and print the grid after each move
    current_grid = [row[:] for row in grid]

    for i, (action, container, pos) in enumerate(moves, 1):
        old_row, old_col = find_container(current_grid, container)
        current_grid[old_row][old_col] = "0"
        if action != 'move':
            new_row, new_col = pos
            current_grid[new_row][new_col] = container

        print(f"Step {i}: {action.title()} {container} to {pos}")
        print_grid(current_grid)

if __name__ == "__main__":
    print("Initial grid:")
    print_grid(initial_grid)

    path = find_path(initial_grid, "C15", truck_position)

    if path:
        print("\nPath found! Simulating moves:")
        simulate_moves(initial_grid, path)
    else:
        print("\nNo path found!")