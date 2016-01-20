import cv2
from VisualObjects import Picture

POPULATION_SIZE = 10

class Evolver(object):
    """
    Class to evolve the pictures. Creates POPULATION_SIZE members in each
    population. Generates 2/5 from two parents, 2/5 from one parent, and
    1/5 from the last generation.

    Evaluates members in a population against a base picture using the
    Mean Squared Error and Structural Similarity Indexing. The top 1/5
    of the population "lives" on into the next population, and the
    remaining 4/5 of the next population are developed from a parent or
    parents in the top 1/5.
    """

    def __init__(self, grid_size):
        """
        Create the initial population of pictures randomly.
        :param grid_size: Number of pixels on a side of the picture. It's
                          important that this number be evenly divisible
                          by 100, 50, 20, and 10. A multiple of 100 is
                          ideal.
        """
        self.population = []
        self.grid_size = grid_size

        for i in range(POPULATION_SIZE):
            print(i)
            self.population.append(Picture(grid_size=grid_size))

    @property
    def pop_size(self):
        """
        :return: Size of the population.
        """
        return POPULATION_SIZE

    def get_pic_at(self, index):
        """
        :param index: Number of the population member to be examined.
        :return: The picture at the location specified in the current
                population.
        """
        return self.population[index]

    def compare_pics(self, evo_pic, tgt_pic):
        """
        Compare two Pictures using Mean Squared Error and Structural
        Similarity Indexing methods. Return a number which represents the
        SIMILARITY between the two, which means a higher numbers is more
        of a match, and therefore better.
        :param evo_pic: Picture object generated during evolution
        :param tgt_pic: Target Picture to compare evolved pics to
        :return: A float 0-10, where higher is better
        """
