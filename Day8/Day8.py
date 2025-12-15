# Input handling

with open("Day8_input.txt", 'r') as input_file:
    input_raw = input_file.read().split('\n')

# Make a list with boxes coordinates
list_of_boxes = [tuple(map(int, box.split(','))) for box in input_raw]

# Function to calculate distance between boxes

from math import sqrt
    
def calculate_distance(box1, box2):

    dx = box1[0] - box2[0]
    dy = box1[1] - box2[1]
    dz = box1[2] - box2[2]

    distance = sqrt(dx**2 + dy**2 + dz**2)

    return(distance)


# Set up a class for circuits

class Circuit:
    def __init__(self, coordinates):
        self.parent = self
        self.coordinates = coordinates

    def find_root(self):

        if self.parent == self:
            return self.parent
        
        else:
            # Updating parents to the root
            self.parent = self.parent.find_root()
            return self.parent
        
    def merge_circuits(self, other):

        root1 = self.find_root()
        root2 = other.find_root()

        if root1 == root2:
            # print(f'{self.coordinates} and {other.coordinates} are already in the same circuit')
            return
        
        else:
            root2.parent = self
            # print(f'Merged {self.coordinates} and {other.coordinates}')
            return
        
    def same_curcuit(self, other):
        root1 = self.find_root()
        root2 = other.find_root()

        if root1 == root2:
            return True
        else:
            return False
        
# Set up a class for a list of circuits

class Forest:
    def __init__(self, list_of_circuits):
        self.list_of_circuits = list_of_circuits


    def get_unique_roots(self):

        roots = set([circuit.find_root() for circuit in self.list_of_circuits])
        return roots


    def count_circuits(self):
        return len(self.get_unique_roots())


    def boxes_in_same_circuit(self, element):

        root = element.find_root()
        circuits_with_this_root = list(filter(lambda circuit: circuit.find_root() == root, self.list_of_circuits))

        return circuits_with_this_root
    
    
    def count_boxes_in_same_circuit(self, element):
        
        return len(self.boxes_in_same_circuit(element))
    

    def make_dict_of_circuit_lengths(self):

        result = {}

        roots = self.get_unique_roots()

        for root in roots:
            result[root.coordinates] = self.count_boxes_in_same_circuit(root)

        return result


    def print_circuits(self):

        roots = self.get_unique_roots()

        for root in roots:
            circuits_with_this_root = self.boxes_in_same_circuit(root)
            print(f'Circuit with root {root.coordinates} contains: {[box.coordinates for box in circuits_with_this_root]}')


# Part 1

# Initialise all circuits
list_of_circuits = []

for box in list_of_boxes:
    # box_circuit = Circuit(box)
    list_of_circuits.append(Circuit(box))

forest = Forest(list_of_circuits)

# Make a list of pairs
list_of_box_pairs = [(box1, box2) for i, box1 in enumerate(list_of_circuits) for box2 in list_of_circuits[i+1:]]

# Sort by distance, closest first
sorted_list_of_box_pairs = sorted(list_of_box_pairs, key=lambda pair: calculate_distance(pair[0].coordinates, pair[1].coordinates))

# Iterate 1000 times

i = 0

while i < 1000:
    
    box_pair = sorted_list_of_box_pairs[i]
    
    if not box_pair[0].same_curcuit(box_pair[1]):

        box_pair[0].merge_circuits(box_pair[1])

    i += 1

# Check all sizes and calculate the answer

list_of_sizes = forest.make_dict_of_circuit_lengths()

answer = 1

print(f'After merging 1000 times')

for root in sorted(list_of_sizes, key=lambda root: list_of_sizes[root], reverse=True)[:10]:
    print(f'Circuit with root {root} contains {list_of_sizes[root]} boxes')

for root in sorted(list_of_sizes, key=lambda root: list_of_sizes[root], reverse=True)[:3]:
    answer *= list_of_sizes[root]

print(f'Part 1: final result is {answer}')


# Part 2

# Initialise all circuits
list_of_circuits = []

for box in list_of_boxes:
    # box_circuit = Circuit(box)
    list_of_circuits.append(Circuit(box))

forest = Forest(list_of_circuits)


# Make a list of pairs
list_of_box_pairs = [(box1, box2) for i, box1 in enumerate(list_of_circuits) for box2 in list_of_circuits[i+1:]]

# Sort by distance, closest first
sorted_list_of_box_pairs = sorted(list_of_box_pairs, key=lambda pair: calculate_distance(pair[0].coordinates, pair[1].coordinates))


# Iterate until all boxes are in one circuit

i = -1

while forest.count_circuits() > 1:

    i += 1
    
    box_pair = sorted_list_of_box_pairs[i]
    
    if not box_pair[0].same_curcuit(box_pair[1]):

        box_pair[0].merge_circuits(box_pair[1])

last_pair = [box.coordinates for box in sorted_list_of_box_pairs[i]]

print(f'After iterating {i} times')

print(f'Last pair is {last_pair}')

# Calculate the answer
answer = last_pair[0][0] * last_pair[1][0]
print(f'Part 2: final result is {answer}')


