from random import gauss, randint, choice
import numpy as np
from math import floor

class RandRGB(object):
    """
    Object used to generate a random RGB 3-tuple. Generates each number
    for Red, Green, and Blue in a range 0-256 by using a skewed
    gaussian random number generation. This object provides a mu and
    sigma for generating each number randomly. A Gene object is made up
    of a matrix of RandRGB.
    """
    def __init__(self, r_mu=128, r_sig=16,
                 g_mu=128, g_sig=16,
                 b_mu=128, b_sig=16):
        self.r_mu = r_mu
        self.r_sig = r_sig
        self.g_mu = g_mu
        self.g_sig = g_sig
        self.b_mu = b_mu
        self.b_sig = b_sig

    @property
    def gauss_vector(self):
        """
        :return: A vector containing the mu and sigma for each color
         to use when called random.gauss.
        """
        return (self.r_mu, self.r_sig,
                self.g_mu, self.g_sig,
                self.b_mu, self.b_sig)

    @property
    def rgb_vector(self):
        """
        :return: a vector of a red, green, and blue values between 0 and
         256.
        """
        red_val = int(round(gauss(self.r_mu, self.r_sig))) % 256
        grn_val = int(round(gauss(self.g_mu, self.g_sig))) % 256
        blu_val = int(round(gauss(self.b_mu, self.b_sig))) % 256
        return red_val, grn_val, blu_val

    @property
    def rgb_string(self):
        """
        :return: A string representation of a random color generated
          from by random.gauss and the mu/sigma of each color.
        """
        rgb_vec = self.rgb_vector
        rgb_hex_string = '#'
        for x in range(3):
            rgb_hex_string += str(hex(rgb_vec[x])).ljust(4, '0')[2:]
        # print(rgb_hex_string)
        return rgb_hex_string

    def load_vector(self, temp_vec_form):
        """
        Recreate an RandRGB from a vector containing its mus and sigmas
        :param temp_vec_form: Vector with color mus and sigmas
        :return: True if successful
        """
        self.r_mu = int(temp_vec_form[0])
        self.r_sig = int(temp_vec_form[1])
        self.g_mu = int(temp_vec_form[2])
        self.g_sig = int(temp_vec_form[3])
        self.b_mu = int(temp_vec_form[4])
        self.b_sig = int(temp_vec_form[5])

    def mutate(self):
        """
        Adjust the mu of each color by -64 through +64 and the sigma
        of each color by a random amount -16 through +16, including 0.
        :return: True if successful
        """
        self.r_mu += randint(-64, 64)
        self.g_mu += randint(-64, 64)
        self.b_mu += randint(-64, 64)
        self.r_sig += randint(-16, 16)
        self.g_sig += randint(-16, 16)
        self.b_sig += randint(-16, 16)


class Gene(object):
    """
    Represents a gene in a picture. A gene is a square of RandRGB pixels
    in a Picture object. Any RandRGB pixel in a Picture is a member of
    exactly one gene. The size of a gene can vary, but is always 1, 2,
    5, or 10% of the Picture. A gene is used to abstract the mutation,
    therefore the Gene class has a function to mutate it. A genetic code
    is made up of a matrix of genes. A gene is never generated in an
    original way, rather Genes are instantiated from already existing
    Pictures.
    """
    def __init__(self, pixel_matrix=None):
        """
        Create a gene from a matrix of RandRGB pixels in a Picture.
        :param pixel_matrix: A matrix of pixels from the Picture.
        Should be a Numpy ndarray
        """
        assert isinstance(pixel_matrix, np.ndarray)
        self.matrix = pixel_matrix
        self.size = len(pixel_matrix)

    def mutate(self):
        """
        Mutate this gene randomly. Note that this method CHANGES THE GENE.
        :return: True if successful.
        """
        for row in range(self.size):
            for col in range(self.size):
                self.matrix[row, col].mutate()

    def __getitem__(self, item):
        """
        Get a specific pixel in the gene
        :param item: coordinate of the pixel
        :return: A RandRGB pixel
        """
        return self.matrix[item]


class Picture(object):
    """
    An object to contain a grid of Rand_RGB objects which generates a
    random but somewhat similar image.
    """
    def __init__(self, parent1=None, parent2=None, grid_size=100):
        """
        Create a new picture object either through mutation other pictures
        or freshly generating it.

        :param parent1: Parent to mutate or mate with parent2
        :param parent2: Parent to mate with parent
        :param grid_size: Size of the picture produced
        """
        self.grid = []
        self.grid_size = grid_size
        if parent2:
            self.generate_merge_parents(parent1, parent2)
        elif parent1:
            self.generate_mutate_parent(parent1)
        else:
            self.generate_no_parents()

    def generate_merge_parents(self, parent1, parent2):
        """
        Mate two parent pictures to produce a new picture for the next
        population. Pictures are merged by first selecting a "gene size"
        and then copying fragments of each parent into a child. In detail:

        Gene size is 1,2,5, or 10% of the grid size, selected randomly.
        Ideally, the grid size will evenly split into all of these
        percentages. Every pixel in the picture will belong to exclusively
        one gene.

        The child picture will be composed of genes randomly selected from
        the parents by creating a grid of new genes of the same size and,
        for each child gene, a corresponding gene will come from a randomly
        selected parent.

        Note that the child Picture is this Picture object, so the final
        grid will become self.grid

        :param parent1: A Picture object to mate with parent2
        :param parent2: A Picture object to mate with parent1
        """

        # choose a gene size
        gene_size = choice((0.01, 0.02, 0.05, 0.1))*self.grid_size
        # get the genes from each parent
        p1_genes = parent1.get_genes(gene_size)
        p2_genes = parent2.get_genes(gene_size)
        gene_code_size = len(p1_genes)
        # put corresponding genes into pairs for selection later
        parent_gene_pairs = [(p1_genes[x], p2_genes[x])
                             for x in range(gene_code_size)]
        child_genes = []
        # iterate through each gene position and choose a parent gene
        for gene_index in range(gene_code_size):
                # select which parent that gene is coming from
                selected_gene = choice(parent_gene_pairs[gene_index])
                child_genes.append(selected_gene)
        # build child's grid from genes
        self.build_from_genes(child_genes)

    def generate_mutate_parent(self, parent):
        """
        Mutate a single parent Picture into a child picture by selecting
        random genes from a genetic code of the Picture and mutating them.
        Mutating a gene entails randomly adjusting the gaussian distributions
        in the pixels.

        Gene size is 1,2,5, or 10% of the grid size, selected randomly.
        Ideally, the grid size will evenly split into all of these
        percentages. Every pixel in the picture will belong to exclusively
        one gene.

        Mutating the gene means going through each pixel in the gene and
        adjusting the mu of each color by -64 through +64 and the sigma
        of each color by a random amount -16 through +16, including 0.

        :param parent: Picture to be mutated
        """
        assert isinstance(parent,Picture)
        # choose a gene size
        gene_size = choice((0.01, 0.02, 0.05, 0.1))*self.grid_size
        # get the genes from the parent
        p_genes = parent.get_genes(gene_size)
        #for

    def generate_no_parents(self):
        """
        Generate a grid of Rand_RGB cells fresh.
        """
        pre_matrix = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                pre_matrix.append(RandRGB(r_mu=randint(0, 256), r_sig=randint(1, 10),
                                   g_mu=randint(0, 256), g_sig=randint(1, 10),
                                   b_mu=randint(0, 256), b_sig=randint(1, 10)))
        self.grid = np.reshape(pre_matrix, (self.grid_size, self.grid_size))

    def render_picture(self):
        """
        Return a grid of hex strings which represent color at each point.
        """
        ret_grid = []
        for row in self.grid:
            ret_grid_row = []
            for cell in row:
                ret_grid_row.append(cell.rgb_string)
            ret_grid.append(ret_grid_row)
        return ret_grid

    def get_genes(self, gene_size):
        """
        Generate a genetic code from the picture by dividing the Picture's
        grid of RandRGB into genes of gene_size x gene_size pixels. The
        genetic code is a matrix of these genes.
        :param gene_size: Size of the side of a gene
        :return: A matrix of genes as a numpy ndarray
        """
        assert self.grid_size % gene_size == 0, "Gene size doesn't divide grid evenly"
        assert isinstance(gene_size, int), "gene_size needs to be an int"
        gene_num = int(self.grid_size / gene_size)
        genetic_code = []
        # iterate through the Picture to the top-left pixel of each gene
        for row in range(gene_num):
            for col in range(gene_num):
                # get the top-left coordinates
                head_row = row * gene_size
                head_col = col * gene_size
                # get the bottom right coordinates
                tail_row = head_row + gene_size
                tail_col = head_col + gene_size
                gene = Gene(self.grid[head_row:tail_row,
                                      head_col:tail_col]
                            )
                genetic_code.append(gene)
        return np.reshape(genetic_code, (gene_num, gene_num))

    def build_from_genes(self, genetic_code):
        """
        Create the grid of this picture from a genetic code.
        :param genes: List of Genes as a 2D numpy ndarray
        :return: None
        """
        gene_size = genetic_code[0, 0].size
        new_grid = []  # blank grid for filling
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # following lines find the next RandRGB pixel
                gene_row = floor(int(row/gene_size))
                gene_col = floor(int(col/gene_size))
                pix_row = row % gene_size
                pix_col = col % gene_size
                target_gene = genetic_code[gene_row, gene_col]
                pixel = target_gene[pix_row, pix_col]
                new_grid.append(pixel)
        self.grid = np.reshape(new_grid, (self.grid_size, self.grid_size))
