import sys
from main import PATS_Approximator
from main import ff_line_match_first, ff_pattern_match_best, ff_pattern_match_first, ff_pattern_match_best_tile_limit, ff_pattern_match_first_tile_limit

#
# main
#
if __name__ == "__main__":

    # python3 test.py [FF_NUMBER]
    if len(sys.argv) < 2:
        print("ERROR: Not enough arguments.")
        print("python3 test.py [FF_NUMBER]")
        quit()

    generations = 2_000
    population_size = 200

    # patterns to try
    pattern_files = ["patterns/checkerboard_4.txt",
                     "patterns/lines_4.txt",
                     "patterns/random_4.txt",
                     "patterns/random_5.txt"]

    # extract pattern
    patterns = []
    for pf in pattern_files:
        p = []
        with open(pf, "r") as f:
            data = f.read()
            p = data.split()
        patterns.append(p)

    # fitness function
    ff_num = int(sys.argv[1])
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

    for p in patterns:
        pats = PATS_Approximator(p, population_size, ff)
        print(f"ID: {pats.id}")

        # run the algorithm
        for g in range(generations):
            pats.run_generation()
            if g % 100 == 0:
                print(f"Generation {g + 1} / {generations}")
            if g % 10 == 0:
                pats.write_data()
