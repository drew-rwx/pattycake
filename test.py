import sys
from main import PATS_Approximator
from main import ff_line_match_first, ff_pattern_match_best, ff_pattern_match_first, ff_pattern_match_best_tile_limit, ff_pattern_match_first_tile_limit

#
# main
#
if __name__ == "__main__":

    # python3 test.py [PATTERN_FILE] [FF_NUMBER]
    if len(sys.argv) < 3:
        print("ERROR: Not enough arguments.")
        print("python3 test.py [PATTERN_FILE] [FF_NUMBER]")
        quit()

    generations = 10_000
    population_size = 250

    # pattern
    pattern = []
    with open(sys.argv[1], "r") as file:
        data = file.read()
        pattern = data.split()

    # fitness function
    ff_num = sys.argv[2]
    if ff_num == 1:
        ff = ff_pattern_match_first
    elif ff_num == 2:
        ff = ff_pattern_match_best
    elif ff_num == 3:
        ff = ff_pattern_match_first_tile_limit
    elif ff_num == 4:
        ff = ff_pattern_match_best_tile_limit
    elif ff_num == 5:
        ff = ff_line_match_first
    else:
        ff = ff_pattern_match_first

    pats = PATS_Approximator(pattern, population_size, ff)
    print(f"ID: {pats.id}")

    # run the algorithm
    for g in range(generations):
        pats.run_generation()
        if g % 100 == 0:
            print(f"Generation {g + 1} / {generations}")
