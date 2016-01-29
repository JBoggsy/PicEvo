import sys
import json
from Evolver import Evolver

if __name__ == '__main__':
    args = sys.argv
    generations = int(args[1])
    display_step =int(args[2])
    testEvo = Evolver(target_pic="target_pic_sm.png")
    print("Pop 0: " + str(len(testEvo.population)))
    fit_vals = []
    for x in range(generations):
        fit_result = testEvo.iterate_evo(display_step)
        fit_vals.append(fit_result[1])
        print("Pop {pid}: {fit}".format(pid=x, fit=fit_result))
    with open('fit_log.txt','w') as f_log:
        print(fit_vals)


