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

    @property
    def target_hists(self):
        target_hists = []
        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            t_hist = cv2.calcHist([self.target_pic], [i],
                                  None, [256], [0, 256])
            target_hists.append(t_hist)
        return target_hists

    def get_pic_at(self, index):
        """
        :param index: Number of the population member to be examined.
        :return: The picture at the location specified in the current
                population.
        """
        return self.population[index]

    def compare_pics(self, evo_pic):
        """
        Compare two Pictures using Mean Squared Error and Structural
        Similarity Indexing methods. Return a number which represents the
        SIMILARITY between the two, which means a higher numbers is more
        of a match, and therefore better.
        :param evo_pic: Picture object generated during evolution
        :return: A float 0-10, where higher is better
        """
        assert isinstance(evo_pic, Picture), "evo_pic is not a Picture"
        assert evo_pic.grid_size == self.grid_size, "evo_pic is not the right size"

        evo_matrix = evo_pic.render_picture()  # evo_matrix is for testing ops
        evo_hists = []  # list of histograms [B, G, R]

        # get the evo_pic histograms
        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            t_hist = cv2.calcHist([evo_matrix], [i], None, [256], [0, 256])
            evo_hists.append(t_hist)
        # shorten the target hists
        tgt_hists = self.target_hists
        # get the compareHist results
        hist_comps = []  # list of the results fo compHist
        for i, col in enumerate(colors):
            t_hist_comp = cv2.compareHist(evo_hists[i], tgt_hists[i], 2)
            hist_comps.append(t_hist_comp)
        return sum(hist_comps)
