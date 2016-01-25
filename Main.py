import sys

from Evolver import Evolver

if __name__ == '__main__':
    args = sys.argv
    generations = args[1]
    display_step =args[2]
    testEvo = Evolver(target_pic="target_pic_sm.png")
    print("Pop 0: " + str(len(testEvo.population)))
    for x in range(generations):
        testEvo.iterate_evo(display_step)
        print("Pop " + str(x+1) + ": " + str(len(testEvo.population)))
