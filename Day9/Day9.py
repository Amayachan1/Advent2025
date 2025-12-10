# Input handling

with open("Day9_input.txt", 'r') as input_file:
    input_raw = input_file.read().split('\n')


# List of red tiles
list_of_red_tiles = []

for tile in input_raw:
    x,y = tile.split(',')
    list_of_red_tiles.append((int(x), int(y)))



sorted_list_of_red_tiles = sorted(list_of_red_tiles, key=lambda tile: tile[0])
# print(sorted_list_of_red_tiles)



valid_pairs = [(tile1, tile2) for i, tile1 in enumerate(sorted_list_of_red_tiles) for tile2 in sorted_list_of_red_tiles[i+1:] if (tile1[0] != tile2[0]) and (tile1[1] != tile2[1])]


def rect_area(pair_of_tiles):
    dx = abs(pair_of_tiles[0][0] - pair_of_tiles[1][0])+1
    dy = abs(pair_of_tiles[0][1] - pair_of_tiles[1][1])+1
    return dx*dy


sorted_valid_pairs = sorted(valid_pairs, key=lambda pair: rect_area(pair), reverse=True)
# print(sorted_valid_pairs)


largest_area = rect_area(sorted_valid_pairs[0])
print('Part 1')
print(f'Largest possible area is {largest_area} between {sorted_valid_pairs[0][0]} and {sorted_valid_pairs[0][1]}')


# Part 2 By myself (in progress)

def are_any_points_inside_or_crossing(pair, shape):
    xs = [pair[0][0], pair[1][0]]
    ys = [pair[0][1], pair[1][1]]
    
    for i, point in enumerate(shape):

        if all([(point[0] in xs), (point[1] in ys)]):
            continue

        # Is inside?
        x_inside = (point[0] > min(xs)) and (point[0] < max(xs))
        y_inside = (point[1] > min(ys)) and (point[1] < max(ys))

        if all([x_inside, y_inside]):
            return True
        
        if i == len(shape):
            next_i = 0
        else:
            next_i = i

        # Is crossing?
        next_point = shape[next_i]

        # x direction
        if (point[1] == next_point[1]) and y_inside:

            minx = min([point[0], next_point[0]])
            maxx = max([point[0], next_point[0]])

            for tile_x in range(minx, maxx+1):
                if (tile_x > min(xs)) and (tile_x < max(xs)):
                    return True

        # y direction
        elif (point[0] == next_point[0]) and x_inside:

            miny = min([point[1], next_point[1]])
            maxy = max([point[1], next_point[1]])

            for tile_y in range(miny, maxy+1):
                if (tile_y > min(ys)) and (tile_y < max(ys)):
                    return True

    return False


for pair in sorted_valid_pairs:
    if not are_any_points_inside_or_crossing(pair, list_of_red_tiles):
        largest_rect_pair = pair
        largest_area = rect_area(pair)
        break

print('Part 2')
print(f'Largest possible area is {largest_area} between {largest_rect_pair[0]} and {largest_rect_pair[1]}')

# Visual
from matplotlib import pyplot as plt

fig, ax = plt.subplots()

all_xs = [point[0] for point in list_of_red_tiles] + [list_of_red_tiles[0][0]]
all_ys = [point[1] for point in list_of_red_tiles] + [list_of_red_tiles[0][1]]
all_ys = [-y for y in all_ys]

ax.plot(all_xs, all_ys)

# Plot points for the largest rectangle
point1 = largest_rect_pair[0]
point2 = largest_rect_pair[1]

ax.plot(point1[0], -point1[1], marker='o', markersize=10, color='red')
ax.plot(point2[0], -point2[1], marker='o', markersize=10, color='red')

plt.show()


# Part 2 Shapely

from shapely.geometry import box
from shapely.geometry.polygon import Polygon

shape = Polygon(list_of_red_tiles)

for pair in sorted_valid_pairs:
    xs = [pair[0][0], pair[1][0]]
    ys = [pair[0][1], pair[1][1]]
    
    rectangle = box(min(xs), min(ys), max(xs), max(ys))

    if shape.contains(rectangle):
        largest_rect_pair = pair
        largest_area = rect_area(pair)
        break

print('Part 2 with shapely')
print(f'Largest possible area is {largest_area} between {largest_rect_pair[0]} and {largest_rect_pair[1]}')


