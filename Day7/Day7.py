# Input handling

with open("Day7_input.txt", 'r') as input_file:
    input_raw = input_file.read().split('\n')

start_raw = input_raw[0]
maze_raw = input_raw[1:]

# Coordinates of the starting beam
start_beam = set([i for i, beam in enumerate(start_raw) if beam == 'S'])


# Maze processing
maze = []

for row_i, row in enumerate(maze_raw):
    maze_row = []
    for col_i, point in enumerate(row):
        if point == '^':
            maze_row.append(col_i)
    maze.append(maze_row)


def move_beam_single_row(beams, maze, row_number=0, collisions=0):

    new_beams = beams.copy()

    for beam in beams:
        if beam in maze[row_number]:
            # print(f'Beam at x {beam} encountered a splitter!')
            collisions += 1
            new_beams.remove(beam)
            new_beams.add(beam-1)
            new_beams.add(beam+1)
    
    return new_beams, collisions
    


def move_beam_through_maze(beam, maze, row_number=0, collisions=0):

    new_beam, collisions = move_beam_single_row(beam, maze, row_number, collisions)
    
    if row_number == len(maze)-1:
        return new_beam, collisions
    
    else:
        return move_beam_through_maze(new_beam, maze, row_number+1, collisions)



end_beam, total_collisions = move_beam_through_maze(start_beam, maze)

print(f'Part 1: We had {total_collisions} collisions')


# Input handling for Part 2

# Starting beam row as a dict, with possible paths there as a value
start_beam={}
for x, char in enumerate(start_raw):
    if char == 'S':
        start_beam[x] = 1
    else:
        start_beam[x] = 0



def trace_beam_single_row(beams, maze, row_number=0):

    new_beams = beams.copy()

    for beam in filter(lambda item: item[1]>0, beams.items()):
        x = beam[0]
        paths = beam[1]
        if x in maze[row_number]:
            # print(f'Beam at x {beam} encountered a splitter!')
            new_beams[x-1] = new_beams[x-1] + paths
            new_beams[x+1] = new_beams[x+1] + paths
            new_beams[x] = 0
    
    # print(list(new_beams.values()))
    
    return new_beams



def trace_beam_through_maze(beam, maze, row_number=0):

    new_beam = trace_beam_single_row(beam, maze, row_number)
    
    if row_number == len(maze)-1:
        return new_beam
    
    else:
        return trace_beam_through_maze(new_beam, maze, row_number+1)

new_beams = trace_beam_through_maze(start_beam, maze)



print(f'Part 2: Total paths number is {sum(list(new_beams.values()))}')


