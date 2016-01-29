import operator

import cv2
from VisualObjects import Picture
from GUI import display_pic

SURVIVAL_SIZE = 2
CHILD_AMOUNT = SURVIVAL_SIZE**2
POPULATION_SIZE = 2*CHILD_AMOUNT + SURVIVAL_SIZE #(10)

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
        self.population = {}
        self.target_pic = cv2.imread(target_pic)
        self.grid_size = len(self.target_pic)
        for i in range(POPULATION_SIZE):
            print(i)
            new_pic = Picture(grid_size=self.grid_size)
            self.population[new_pic.pic_id] = new_pic
        self.iteration = 0

    @property
    def pop_size(self):
        """
        :return: Size of the population.
        """
        return POPULATION_SIZE

    def get_pic_at(self, pic_id):
        """
        :param index: pic_id of the population member to be examined.
        :return: The picture with the pic_id specified in the current
                population.
        """
        return self.population[pic_id]

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

    def iterate_evo(self, iter_show_step):
        """
        Complete one iteration of the evolutionary process by comparing
        every Picture in the population with the target picture and selecting
        the top x for survival. Then replace the remaining 2x^2 with
        Pictures created from one or two parents of the survivng x. 1/2
        of the new Pictures will be generated by merging two parents, and
        1/2 will be generated from mutating one parent. See the docs of
        Picture.generate_merge_parents() and Picture.generate_mutate_parent().
        Where x = SURVIVAL_SIZE
        :return: Lowest fitness value
        """
        # get fitness values for every picture in the population
        self.iteration += 1
        fitness_vals = {}
        for pic_id in self.population:
            test_pic = self.population[pic_id]
            fitness_val = self.compare_pics(test_pic)
            fitness_vals[pic_id] = fitness_val

        # select the top x for survival and create new population
        sorted_fit_vals = sorted(fitness_vals.items(),
                                 key=operator.itemgetter(1))
        surviving_ids = [pair[0] for pair in sorted_fit_vals[:SURVIVAL_SIZE]]
        surviving_pics = [(surv_id, self.population[surv_id])
                          for surv_id in surviving_ids]
        if self.iteration % iter_show_step == 0:
            for pic_id in surviving_ids:
                img_name = 'img_{}.png'.format(pic_id)
                cv2.imwrite(img_name,
                            self.population[pic_id].render_picture()
                            )
        new_population = dict(surviving_pics)
        new_pop_holder = new_population.copy()

        # generate the rest new population from surviving parents
        for parent1_id in new_pop_holder:
            for parent2_id in new_pop_holder:
                parent1 = new_population[parent1_id]
                parent2 = new_population[parent2_id]
                new_pic_merge = Picture(parent1, parent2)
                new_pic_mutate = Picture(parent1)
                new_population[new_pic_merge.pic_id] = new_pic_merge
                new_population[new_pic_mutate.pic_id] = new_pic_mutate

        self.population = new_population
        return sorted_fit_vals[0]
