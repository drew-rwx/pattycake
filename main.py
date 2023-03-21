# imports
import copy
import random


#
# PATSApproximator
#
class PATS_Approximator:
    def __init__(self, pattern, population_size):
        # class variables
        self.pattern_size = len(pattern) / 2
        self.population_size = population_size
        self.generation = 0
        self.population = [Organism(self.pattern_size)
                           for _ in range(self.population_size)]

    def run_generation(self):
        self.generation += 1


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

                print("west", west_glue, "south", south_glue)

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
    def __init__(self, pattern_size):
        # class variables
        self.pattern_size = pattern_size
        self.max_tiles = self.pattern_size ** 2
        self.max_glues = self.max_tiles * 2
        self.gluetable = GlueTable(self.max_glues)

        # Seed assembly
        seed_tiles = [random.randint(1, self.max_glues)
                      for _ in range(self.pattern_size * 2)]
        self.seed_assembly = Assembly(seed_tiles)


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

    pats = PATS_Approximator()
