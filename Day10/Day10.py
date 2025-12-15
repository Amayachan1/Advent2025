# Input handling

with open("Day10_input.txt", 'r') as input_file:
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

    machine_buttons_bool = []

    for machine_button in machine_buttons:
        machine_button_bool = [light in machine_button for light in range(len(light_indicators[machine]))]
        machine_buttons_bool.append(machine_button_bool)

    all_buttons[machine] = machine_buttons_bool


def press_buttons_on_a_machine(machine_num, buttons_num_list):
    # Get machine info
    machine_goal_lights = light_indicators[machine_num]
    machine_lights = [False for i in range(len(machine_goal_lights))]
    machine_buttons = all_buttons[machine_num]

    # Initialise resulting light sequence
    result_lights = machine_lights
    lights_string = ''.join(['#' if light else '.' for light in result_lights])

    # Press buttons
    for button in buttons_num_list:
        result_lights = [result_lights[i] ^ machine_buttons[button][i] for i in range(len(result_lights))]
        lights_string = ''.join(['#' if light else '.' for light in result_lights])
        # print(f'Pressed button #{button}: {machine_buttons[button]} - lights are {lights_string}')
    
    # Check if matching the goal
    matched = result_lights == machine_goal_lights

    return matched, result_lights, lights_string


# Try writing a BFS for a single machine

from collections import deque

def BFS_single_machine(machine_num):
    machine_buttons = all_buttons[machine_num]
    num_of_buttons = len(machine_buttons)

    tried_combinations = []

    matched = False

    combinations_to_try = deque([[]])

    while not matched:
        
        buttons_to_press = combinations_to_try.popleft()

        # print(buttons_to_press)
        if set(buttons_to_press) not in tried_combinations:
            tried_combinations.append(set(buttons_to_press))
        # Add next level nodes from here to the queue
            next_level = [buttons_to_press + [button] for button in range(num_of_buttons)]
            combinations_to_try.extend(next_level)

            matched, result_lights, lights_string = press_buttons_on_a_machine(machine_num, buttons_to_press)
            # print(f'Result on machine {machine_num} is : {lights_string} {'Goal achived!' if matched else 'Not matching'}')

    button_num_string = ' '.join(['#'+str(button_num) for button_num in buttons_to_press])
    num_of_presses = len(buttons_to_press)
    
    print(f'End result on machine {machine_num} is : {lights_string} {'Goal achived!' if matched else 'Not matching'}')
    print(f'Pressed {num_of_presses} buttons: {button_num_string}')
    return num_of_presses


# Try all machines

total_presses = 0

for machine in range(len(light_indicators)):
    num_of_presses = BFS_single_machine(machine)
    total_presses += num_of_presses

print(f'Total number of buttons pressed is {total_presses}')


