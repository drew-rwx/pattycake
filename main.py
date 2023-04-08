# imports
import copy
import random
import math
import datetime
import os
import sys


#
# Fitness key functions
#
# Need to redefine these functions outside the class for the sort function
#
def fitness_pattern_match(organism):
    return organism.fitness_pattern_match()


def fitness_pattern_match_2_color(organism):
    return organism.fitness_pattern_match_2_color()


#
# PATSApproximator
#
class PATS_Approximator:
    def __init__(self, pattern, population_size):
        # class variables
        self.id = datetime.datetime.now()
        self.id = (
            str(self.id.date())
            + "-"
            + f"{self.id.hour:02}"
            + f"{self.id.minute:02}"
            + f"{self.id.second:02}"
        )
        self.mutation_rate = 0.25
        self.pattern = pattern
        self.pattern_size = int(math.sqrt(len(pattern)))
        self.population_size = population_size
        self.generation = 0
        self.random_seed = random.randrange(sys.maxsize)
        random.seed(self.random_seed)
        self.write_info()
        self.population = [Organism(self.pattern, self.mutation_rate)
                           for _ in range(self.population_size)]
        self.population.sort(key=fitness_pattern_match, reverse=True)
        self.best_score = self.population[0].score
        self.write_population()

    def new_population(self):
        # top ten of population
        top_ten_index = int(len(self.population) * 0.1)
        top_ten = []
        for i in range(top_ten_index):
            top_ten.append(self.population[i])

        # selection and mutate
        next_population = []
        next_population.extend(top_ten)
        while len(next_population) < self.population_size:
            # select random from best
            random_index = random.randint(0, top_ten_index - 1)
            # mutate and add
            next_population.append(top_ten[random_index].mutate())

        return next_population

    def run_generation(self):
        self.generation += 1

        # score and sort
        self.population.sort(key=fitness_pattern_match_2_color, reverse=True)

        # update best score
        if self.population[0].score > self.best_score:
            self.best_score = self.population[0].score
            # write to file
            self.write_population()

        # select and mutate
        self.population = self.new_population()

    def print_best(self):
        print(f"*** Generation {self.generation} ***")
        print(self.population[0])

    def write_info(self):
        path = os.path.join("runs", str(self.id), "_info.txt")

        # make dir, write info in file
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(f"ID: {self.id}\n")
            f.write(f"Random seed: {self.random_seed}\n")
            f.write(f"Population size: {self.population_size}\n")
            f.write(f"Mutation rate: {self.mutation_rate}\n\n")

            f.write(f"Pattern:\n")
            for r in range(self.pattern_size):
                for c in range(self.pattern_size):
                    f.write(self.pattern[(r * self.pattern_size) + c] + " ")
                f.write("\n")

    def write_population(self):
        path = os.path.join("runs", str(
            self.id), "score_" + f"{self.best_score:03}" + "_population.txt")

        # make dir, write info in file
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(f"*** Generation {self.generation} ***\n\n")
            f.write("--- Best Organism ---\n")
            f.write(str(self.population[0]))
            for i in range(1, self.population_size):
                f.write(f"\n--- Population {i:03} ---\n")
                f.write(str(self.population[i]))
                f.write("\n")


#
# Tile
#
class Tile:
    def __init__(self, north=0, east=0, south=0, west=0):
        # class variables
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def __eq__(self, o):
        if isinstance(o, Tile):
            res = self.north == o.north and self.east == o.east
            res = res and self.south == o.south and self.west == o.west
            return res
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.north, self.east, self.south, self.west))

    def __str__(self):
        result = ""

        # Separator string
        separator = "--------"

        # Top separator
        result += separator + "\n"

        # Glues
        line = "|  {:^3} |".format(self.north)
        result += line + "\n"
        line = "|{:^3}{:^3}|".format(self.west, self.east)
        result += line + "\n"
        line = "|  {:^3} |".format(self.south)
        result += line + "\n"

        # Bottom separator
        result += separator

        return result


#
# Assembly
#
class Assembly:
    def __init__(self, seed_tiles):
        # class variables
        pattern_size = len(seed_tiles) // 2
        self.size = pattern_size + 1
        self.assembly = [Tile() for _ in range(self.size ** 2)]

        # init seed glues
        seed_tile_index = 0
        # reverse the rows
        for r in reversed(range(1, self.size)):
            self.update_at(r, 0, Tile(east=seed_tiles[seed_tile_index]))
            seed_tile_index += 1

        for c in range(1, self.size):
            self.update_at(0, c, Tile(north=seed_tiles[seed_tile_index]))
            seed_tile_index += 1

    def update_at(self, x, y, t):
        self.assembly[(x * self.size) + y] = t

    def tile_at(self, x, y):
        return self.assembly[(x * self.size) + y]

    def assemble(self, gluetable):
        result = copy.deepcopy(self)

        for r in range(1, result.size):
            for c in range(1, result.size):
                south_glue = result.tile_at(r - 1, c).north
                west_glue = result.tile_at(r, c - 1).east

                north_glue, east_glue = gluetable.glues_at(
                    south_glue, west_glue)

                t = Tile(north_glue, east_glue, south_glue, west_glue)
                result.update_at(r, c, t)

        return result

    def __str__(self):
        result = ""

        # Separator string
        separator = "-"
        for _ in range(0, self.size):
            separator += "-------"

        # Top separator
        result += separator + "\n"

        # Loop through each row, reversed
        for r in reversed(range(self.size)):
            # Loop through each col for the north glues
            line = "|"
            for c in range(self.size):
                line += "  {:^3} |".format(self.tile_at(r, c).north)
            result += line + "\n"

            # Loop through each col for the west and east glues
            line = "|"
            for c in range(self.size):
                line += "{:^3}{:^3}|".format(self.tile_at(r, c).west,
                                             self.tile_at(r, c).east)
            result += line + "\n"

            # Loop through each col for the south glues
            line = "|"
            for c in range(self.size):
                line += "  {:^3} |".format(self.tile_at(r, c).south)
            result += line + "\n"

            # Write the bottom separator
            result += separator + "\n"

        return result


#
# Organism
#
class Organism:
    def __init__(self, pattern, mutation_rate):
        # class variables
        self.mutation_rate = mutation_rate
        self.pattern = pattern
        self.pattern_size = int(math.sqrt(len(pattern)))
        self.max_tiles = self.pattern_size ** 2
        self.max_glues = self.max_tiles * 2
        self.gluetable = GlueTable(self.max_glues)

        # seed assembly
        seed_tiles = [random.randint(1, self.max_glues)
                      for _ in range(self.pattern_size * 2)]
        self.seed_assembly = Assembly(seed_tiles)

        # init
        self.fitness_pattern_match()

    def __str__(self):
        res = ""

        # score
        res += f"Score: {self.score} / {self.perfect_score} \n"
        res += f"Incorrectly placed tiles: {self.incorrect} \n"

        # tileset map
        res += f"Tile set maping ({len(self.tile_color_map)} tiles):\n"
        for k in self.tile_color_map.keys():
            res += f"({k.north}, {k.east}, {k.south}, {k.west})" + \
                f": {self.tile_color_map[k]}\n"

        # assembly
        res += str(self.assembly)

        return res

    # Perfect score: every color correct + no tiles used
    # Subtract 1 for every incorrect color
    # Subtract 1 for every tile used
    def fitness_pattern_match(self):
        self.perfect_score = self.pattern_size ** 2 * 2
        self.score = self.pattern_size ** 2 * 2
        self.incorrect = 0
        self.tile_color_map = {}
        self.assembly = self.seed_assembly.assemble(self.gluetable)

        for r in range(1, self.assembly.size):
            for c in range(1, self.assembly.size):
                color = self.pattern[(
                    (self.pattern_size - r) * self.pattern_size) + (c - 1)]
                tile = self.assembly.tile_at(r, c)

                if tile not in self.tile_color_map:
                    self.tile_color_map[tile] = color
                elif self.tile_color_map[tile] != color:
                    self.incorrect += 1

        self.score -= self.incorrect
        self.score -= len(self.tile_color_map)
        return self.score

    # Perfect score: every color correct + no tiles used
    # Subtract 1 for every incorrect color
    # Subtract 1 for every tile used
    def fitness_pattern_match_2_color(self):
        self.perfect_score = self.pattern_size ** 2 * 2
        self.score = self.pattern_size ** 2 * 2
        self.incorrect = 0
        self.tile_color_map = {}
        self.assembly = self.seed_assembly.assemble(self.gluetable)

        for r in range(1, self.assembly.size):
            for c in range(1, self.assembly.size):
                color = self.pattern[(
                    (self.pattern_size - r) * self.pattern_size) + (c - 1)]
                tile = self.assembly.tile_at(r, c)

                if tile not in self.tile_color_map:
                    if color == 'b':
                        entry = (1, 0)
                    elif color == 'w':
                        entry = (0, 1)
                    else:
                        quit()

                    self.tile_color_map[tile] = entry
                else:
                    if color == 'b':
                        entry = self.tile_color_map[tile]
                        self.tile_color_map[tile] = (entry[0] + 1, entry[1])
                    elif color == 'w':
                        entry = self.tile_color_map[tile]
                        self.tile_color_map[tile] = (entry[0], entry[1] + 1)
                    else:
                        quit()

        for t in self.tile_color_map.keys():
            b_count, w_count = self.tile_color_map[t]

            if b_count >= w_count:
                self.tile_color_map[t] = 'b'
                self.incorrect += w_count
            else:
                self.tile_color_map[t] = 'w'
                self.incorrect += b_count

        self.score -= self.incorrect
        self.score -= len(self.tile_color_map)
        return self.score

    def mutate(self):
        result = copy.deepcopy(self)

        # mutate gluetable
        for s in range(1, result.gluetable.max_glues + 1):
            for w in range(1, result.gluetable.max_glues + 1):
                north, east = result.gluetable.glues_at(s, w)

                mutation_change = random.random()
                if mutation_change <= result.mutation_rate:
                    north = random.randint(1, result.gluetable.max_glues)
                mutation_change = random.random()
                if mutation_change <= result.mutation_rate:
                    east = random.randint(1, result.gluetable.max_glues)

                result.gluetable.set_glues_at(s, w, (north, east))

        # mutate seed
        for r in range(1, result.seed_assembly.size):
            mutation_change = random.random()
            if mutation_change <= result.mutation_rate:
                result.seed_assembly.update_at(r, 0, Tile(
                    east=random.randint(1, result.gluetable.max_glues)))

        for c in range(1, result.seed_assembly.size):
            mutation_change = random.random()
            if mutation_change <= result.mutation_rate:
                result.seed_assembly.update_at(0, c, Tile(
                    north=random.randint(1, result.gluetable.max_glues)))

        return result


#
# GlueTable
#
class GlueTable:
    def __init__(self, max_glues):
        self.max_glues = max_glues
        # Flattened 2D array, each entry is a tuple of glues (north, east)
        # Add 1 to max_glues to accommodate values [0, self.max_glues]
        self.gt = [(random.randint(1, self.max_glues),
                    random.randint(1, self.max_glues))
                   for _ in range((self.max_glues + 1) ** 2)]

    def glues_at(self, x, y):
        return self.gt[(x * self.max_glues) + y]

    def set_glues_at(self, x, y, g):
        self.gt[(x * self.max_glues) + y] = g


#
# main
#
if __name__ == "__main__":
    greeting = """
     ***  Pattycake ***

              (
              )
         __..---..__
     ,-='  /  |  \\  `=-.
    :--..___________..--;
     \\.,_____________,./
            """
    print(greeting)

    # default random pattern
    colors = ['b', 'w']
    pattern_size = 6
    pattern = [random.choice(colors) for _ in range(pattern_size ** 2)]

    # if pattern passed in, use that instead
    if len(sys.argv) > 2:
        pattern = []
        with open(sys.argv[2], "r") as file:
            data = file.read()
            pattern = data.split()

    pats = PATS_Approximator(pattern, 100)

    # number of generations
    generations = 25
    if len(sys.argv) > 1:
        generations = int(sys.argv[1])

    # run the algorithm
    pats.print_best()
    for g in range(generations):
        pats.run_generation()
        print(f"Generation {g + 1} / {generations}")
    print()
    pats.print_best()
