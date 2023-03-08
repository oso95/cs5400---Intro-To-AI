import sys
from collections import deque


# read in files and store it in a list
# ignore the first line of the input file
def read_file(filename):
    f = open(filename, "r")
    farm = []
    for i, line in enumerate(f):
        if i == 0:
            continue
        farm.append([c for c in line.strip()])
    return farm


# write to the output file
def write_file(output_file, farm, score):
    with open(output_file, "w") as f:
        size = len(farm)
        f.write(str(size))
        f.write("\n")
        for row in farm:
            f.write("".join(row))
            f.write("\n")
        f.write(str(score))


# print out the farm
def print_farm(farm):
    for row in farm:
        print("".join(row))


# get the position of all the grass's coordinate in the farm (grass is represented by '.')
def get_grass(farm):
    grass = []
    for i in range(len(farm)):
        for j in range(len(farm[i])):
            if farm[i][j] == ".":
                grass.append((i, j))
    return grass


# calculate the score of the cow placement
# if a cow is horizontally or vertically adjacent to a haystack, the score is +1
# if a cow is horinzontally or vertically adjacent to both a haystack and water pond, the score is +2
# if a cow is next to another cow (horizontally or vertically or diagonally), the score is -3
# water pond is represented by '#'
# the size of the farm is in the first line of the input file, when calculating the score, we need to exclude the first line
# if the cow is at the edge of the farm, we need to avoid to read index out of range
def calculate_score(farm):
    score = 0
    rows, cols = len(farm), len(farm[0])

    for x in range(cols):
        for y in range(rows):
            if farm[x][y] == "C":
                # print("cow at", x, y, "cow_score = 0")
                waterPond_ctr = 0
                cow_score = 0
                haystack_ctr = 0
                adjacent_positions = [
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                ]
                for adj_x, adj_y in adjacent_positions:
                    # not valid location
                    if adj_x < 0 or adj_y < 0 or adj_x >= rows or adj_y >= cols:
                        continue
                    else:
                        if farm[adj_x][adj_y] == "@":
                            haystack_ctr += 1
                        if farm[adj_x][adj_y] == "#":
                            waterPond_ctr += 1
                if haystack_ctr:
                    if waterPond_ctr:
                        cow_score += 3
                    else:
                        cow_score += 1
                diagonally_adjacent_positions = [
                    (x - 1, y - 1),
                    (x + 1, y - 1),
                    (x - 1, y + 1),
                    (x + 1, y + 1),
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                ]
                for adj_x, adj_y in diagonally_adjacent_positions:
                    if adj_x < 0 or adj_y < 0 or adj_x >= rows or adj_y >= cols:
                        continue
                    else:
                        if farm[adj_x][adj_y] == "C":
                            cow_score -= 3
                score += cow_score
    return score


def bfs(initial_farm):
    """
    Breadth-first search algorithm.

    We use a queue to store the nodes that we need to explore and a set to store the states that we have already explored.
    Visited states are stored in a dictionary, where the key is the hash of the state and the value is True.
    
    VARIABLES:
        - frontier: a queue that stores the nodes that we need to explore, each node is a tuple of the state and the actions
        - visited_states: a set that stores the states that we have already explored
        - state: the state of the current node
        - actions: the actions that we have taken to get to the current state
        - valid_actions: the valid actions that can be applied to the current state
        - new_state: the new state that is created by applying the action to the current state
        - new_actions: the new actions that are created by appending the action to the current actions
        - new_node: the new node that is created by appending the new state and new actions to the current node
        - score: the score of the current state
        - goal: the goal state of the puzzle

    while the queue is not empty:
        - Get the first node in the frontier queue and remove it from the queue, this is the current node

        - Check if the state of the current node has already been visited, if so, continue to the next iteration of the loop,
            otherwise, add the state to the visited states dictionary

        - Check if the state of the current node is the goal state, if so, return the state and the score

        - Expand the current node by getting all the valid actions that can be applied to the current state

        - For each valid action, create a new state by applying the action to the current state

        - Add the new state and the new actions to the frontier queue as a new node (append to the end of the queue)
    """

    frontier = deque([(tuple(map(tuple, initial_farm)), [])])
    visited_states = set()

    while frontier:
        state, actions = frontier.popleft()

        # Check if state has already been visited
        if state in visited_states:
            continue

        # Mark state as visited
        visited_states.add(state)

        # Check if state is the goal state
        if goal(state):
            return state, calculate_score(state)

        # Expand the node
        valid_actions = get_valid_actions(state, visited_states)
        for action in valid_actions:
            new_state = apply_action(state, action)
            new_actions = actions + [action]
            frontier.append((new_state, new_actions))

    return None

# Create a new state by applying the action to the current state
def apply_action(state, action):
    new_state = [list(row) for row in state]
    new_state[action[0]][action[1]] = "C"
    return tuple(map(tuple, new_state))

# Return a list of valid actions that can be applied to the current state
def get_valid_actions(state, visited_states):
    actions = get_grass(state)
    valid_actions = []
    for action in actions:
        new_state = apply_action(state, action)
        if new_state not in visited_states:
            valid_actions.append(action)
    return valid_actions

# Return True if the state is the goal state, otherwise return False
def goal(state):
    score = calculate_score(state)
    if score >= 7:
        return True
    return False


# main function
if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    farm, score = bfs(read_file(input_file))
    write_file(output_file, farm, score)
