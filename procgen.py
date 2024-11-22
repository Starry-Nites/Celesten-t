import random


# Establish what types of blocks are going to be generated
def randomizeBlocks():
    finTiles = ""
    nonSpaceCounter = 0
    for i in range(15):
        tile = random.randint(1, 13)

        # If the randint was 1-4, make a block with empty space directly after it.
        # The addition of the empty space along with the theoretical probability of this option being chosen
        # means that it will be extremely unlikely that the player will be trapped on a floor.
        if tile == 1 or tile == 2 or tile == 3 or tile == 4:
            finTiles += "X "

        # If the randint was 5-7, make a regular block with no space after it. This is the second most probable option.
        elif tile == 5 or tile == 6 or tile == 7:
            finTiles += "X"
            nonSpaceCounter += 1

        # If the randint was 8-10, an empty space will be placed. This is tied as the second most probable option.
        elif tile == 8 or tile == 9 or tile == 10:
            finTiles += " "

        # If the randint was 11 or 12, spawn a trap.
        elif tile == 11 or tile == 12:
            finTiles += "t"
            nonSpaceCounter += 1

        # If the randint was 11, spawn a coin. Will very rarely happen (1/11 odds)
        elif tile == 13:
            finTiles += "C"

    if len(finTiles) > 15:
        finTiles = finTiles[0:15]

    finTiles = finTiles.replace(finTiles[0], "X")
    finTiles = finTiles.replace(finTiles[-1], "X")
    if nonSpaceCounter >= 12:
        finTiles = finTiles.replace(finTiles[0], " ")

    return finTiles

