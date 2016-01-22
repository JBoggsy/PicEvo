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

    def __init__(self, target_pic="target_pic.png"):
        """
        Create the initial population of pictures randomly.
        :param grid_size: Number of pixels on a side of the picture. It's
                          important that this number be evenly divisible
                          by 100, 50, 20, and 10. A multiple of 100 is
                          ideal.
        :param target_pic: Filename of the target picture. Defaults to
                           "target_pic.png" in the PicEvo folder.
        """
        self.population = []
        self.target_pic = cv2.imread(target_pic)
        self.grid_size = len(self.target_pic)
        for i in range(POPULATION_SIZE):
            print(i)
            self.population.append(Picture(grid_size=self.grid_size))

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

    def compare_pics(self, evo_pic):
        """
        Compare two Pictures by subtracting the evo pic from the target
        picture and taking the sum of the resultant matrix. The smaller the
        result, the closer the two images are. Should work... right?
        :param evo_pic: Picture object generated during evolution
        :return: An integer where lower is better
        """
        assert isinstance(evo_pic, Picture), "evo_pic is not a Picture"
        assert evo_pic.grid_size == self.grid_size, "evo_pic is not the right size"

        evo_matrix = evo_pic.render_picture()  # evo_matrix is for testing ops
        result_matrix = evo_matrix - self.target_pic
        result = result_matrix.sum()
        return result
