# Input handling

with open("Day10_ex_input.txt", 'r') as input_file:
    input_raw = input_file.read().split('\n')


# Split input using regex

import re

light_indicators_re = re.compile("\\[.*?\\]")
joltages_re = re.compile("\\{.*?\\}")
buttons_re = re.compile("\\(.*?\\)")


# Get all light indicators as bool string put in a dict with machine # as index

light_indicators = {}
for machine, line in enumerate(input_raw):
    light_indicator = light_indicators_re.findall(line)[0][1:-1]
    light_indicator_bool = [light == '#' for light in light_indicator]
    light_indicators[machine] = light_indicator_bool


# Get all joltages as a dict

joltages = {}
for machine, line in enumerate(input_raw):
    joltage = joltages_re.findall(line)[0][1:-1]

    joltages[machine] = [int(number) for number in joltage.split(',')]


# Get all buttons, each button is a bool string, list for each machine in a dict

all_buttons = {}
for machine, line in enumerate(input_raw):
    machine_buttons_iterator = buttons_re.finditer(line)
    machine_buttons_raw = [button.group()[1:-1] for button in machine_buttons_iterator]
    machine_buttons = [tuple(map(int, button.split(','))) for button in machine_buttons_raw]

    # machine_buttons_bool = []

    # for machine_button in machine_buttons:
    #     machine_button_bool = [light in machine_button for light in range(len(light_indicators[machine]))]
    #     machine_buttons_bool.append(machine_button_bool)

    all_buttons[machine] = machine_buttons




def press_joltage_button(state, button):

    # Initialise resulting light sequence
    result_state = state.copy()

    # Press a button
    for joltage_change in button:
        result_state[joltage_change] += 1

    return result_state



from collections import deque

class MachineStates:
    def __init__(self, target, buttons):
        self.target = target

        self.root = ([0 for j in self.target], [])

        # self.paths = [self.root[1]]
        # self.visited_states = [self.root[0]]

        self.paths = []
        self.visited_states = []

        self.buttons = buttons

    def generate_states(self, id):
        children = []
        children_paths = []
        for button in self.buttons:
            child = press_joltage_button(self.visited_states[id], button)
            if child not in self.visited_states:
                children.append(child)
                children_paths.append(self.paths[id] + [button])

        return list(zip(children, children_paths))
    
    def BFS(self):

        matched = False
        states_to_try = deque([self.root])
        id=-1
        

        while not matched:
            current_state = states_to_try.popleft()

            if current_state[0] not in self.visited_states:
                id += 1
                # print(f'Reached state {current_state[0]}')
                self.visited_states.append(current_state[0])
                self.paths.append(current_state[1])

                if current_state[0] == self.target:
                    matched = True

                else:
                    states_to_try.extend(self.generate_states(id))
        
        path = current_state[1]
        button_presses = len(path)
        
        print(f'Reached target {self.target}, button presses: {button_presses}')

        return button_presses
                


# Try all machines

total_presses = 0

for machine in range(len(joltages)):
    print(f'Machine # {machine}')
    num_of_presses = MachineStates(joltages[machine], all_buttons[machine]).BFS()
    total_presses += num_of_presses

print(f'Total number of buttons pressed is {total_presses}')


