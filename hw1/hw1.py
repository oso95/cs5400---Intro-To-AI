import sys
import random


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


# calculate amount of haystack in the farm (haystack is represented by '@')
def count_haystack(farm):
    count = 0
    for row in farm:
        for c in row:
            if c == "@":
                count += 1
    return count


# get the position of all the grass's coordinate in the farm (grass is represented by '.')
def get_grass(farm):
    grass = []
    for i in range(len(farm)):
        for j in range(len(farm[i])):
            if farm[i][j] == ".":
                grass.append((i, j))
    return grass


# randomly chose the cordinate of the grass and place the cow there
# the amount of cow is equal to the amount of haystack, which is calculated by count_haystack function
# the cow is represented by 'C'
# print out the farm after placing the cow
def place_cow(farm):
    grass = get_grass(farm)
    for i in range(count_haystack(farm)):
        random_grass = random.choice(grass)
        farm[random_grass[0]][random_grass[1]] = "C"
        grass.remove(random_grass)


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
                # calculate the score of the cow based on how many haystack and water pond it is adjacent to
                if haystack_ctr:
                    if waterPond_ctr:
                        cow_score += 3
                    else:
                        cow_score += 1
                        
                # diagonally and adjacent positions for the cow
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
                # not valid location
                for adj_x, adj_y in diagonally_adjacent_positions:
                    if adj_x < 0 or adj_y < 0 or adj_x >= rows or adj_y >= cols:
                        continue
                    else:
                        # if the cow is next to another cow, the score is -3
                        if farm[adj_x][adj_y] == "C":
                            cow_score -= 3
                score += cow_score
    return score


# write to the output file
def write_file(output_file, farm, score):
    with open(output_file, "w") as f:
        size = len(farm)
        f.write(str(size) + "\n")
        for row in farm:
            f.write("".join(row))
            f.write("\n")
        f.write(str(score))


# main function
if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    farm = read_file(input_file)
    place_cow(farm)
    write_file(output_file, farm, calculate_score(farm))
