from Evolver import Evolver

if __name__ == '__main__':
     testEvo = Evolver(target_pic="target_pic_sm.png")
     print("Pop 0: " + str(len(testEvo.population)))
     for x in range(3):
        testEvo.iterate_evo()
        print("Pop " + str(x+1) + ": " + str(len(testEvo.population)))
