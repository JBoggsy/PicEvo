from random import gauss, randint, choice
from math import floor, sqrt

class RandRGB(object):
    """
    Object used to generate a random RGB 3-tuple. Generates each number
    for Red, Green, and Blue in a range 0-256 by using a skewed
    gaussian random number generation. This object provides a mu and
    sigma for generating each number randomly. A single RandRGB makes
    up a pixel in
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
        return (self.r_mu, self.r_sig,
                self.g_mu, self.g_sig,
                self.b_mu, self.b_sig)

    @property
    def rgb_vector(self):
        red_val = int(round(gauss(self.r_mu, self.r_sig))) % 256
        grn_val = int(round(gauss(self.g_mu, self.g_sig))) % 256
        blu_val = int(round(gauss(self.b_mu, self.b_sig))) % 256
        return (red_val, grn_val, blu_val)

    @property
    def rgb_string(self):
        rgb_vec = self.rgb_vector
        rgb_hex_string = '#'
        for x in range(3):
            rgb_hex_string += str(hex(rgb_vec[x])).ljust(4, '0')[2:]
        # print(rgb_hex_string)
        return rgb_hex_string

    def load_vector(self, temp_vec_form):
        self.r_mu = int(temp_vec_form[0])
        self.r_sig = int(temp_vec_form[1])
        self.g_mu = int(temp_vec_form[2])
        self.g_sig = int(temp_vec_form[3])
        self.b_mu = int(temp_vec_form[4])
        self.b_sig = int(temp_vec_form[5])


class Gene(object):
    """
    Represents a gene in a picture. A gene is a square of RandRGB pixels
    in a Picture object. Any RandRGB pixel in a Picture is a member of
    exactly one gene. The size of a gene can vary, but is always 1, 2,
    5, or 10% of the Picture. A gene is used to abstract the mutation,
    therefore the Gene class has a function to mutate it.
    """
    def __init__(self):
        pass


class Picture(object):
    """
    An object to contain a grid of Rand_RGB objects which generates a
    random but somewhat similar image.
    """
    def __init__(self, parent1=None, parent2=None, grid_size=400):
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
        adjusting the mu of each color by -64 through + 64 and the sigma
        of each color by a random amount -16 through +16, including 0.

        :param parent: Picture to be mutated
        """
        # choose a gene size
        gene_size = choice((0.01, 0.02, 0.05, 0.1))*self.grid_size
        # get the genes from the parent
        p_genes = parent.get_genes(gene_size)
        #for

    def generate_no_parents(self):
        """
        Generate a grid of Rand_RGB cells fresh.
        """
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                row.append(RandRGB(r_mu=randint(0, 256), r_sig=randint(1, 10),
                                   g_mu=randint(0, 256), g_sig=randint(1, 10),
                                   b_mu=randint(0, 256), b_sig=randint(1, 10)))
            self.grid.append(row)

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
        :return: A matrix of genes
        """
        gene_size = int(gene_size)
        gene_num = int(self.grid_size/gene_size)
        genetic_code = []
        # iterate through the Picture to the top-left pixel of each gene
        for row in range(gene_num):
            gc_row = [] # row in the genetic code
            for col in range(gene_num):
                # iterate through each pixel in each gene
                # get the top-left coordinates
                gene_head = [row*gene_size, col*gene_size]
                # create the gene array
                gene=[]
                for y in range(gene_size):
                    # create a new row
                    gene_row = []
                    for x in range(gene_size):
                        # add each pixel to the new row
                        pxl_loc = [gene_head[0]+y, gene_head[1]+x]
                        gene_row.append(self.grid[pxl_loc[0]][pxl_loc[1]])
                    gene.append(gene_row)
                gc_row.append(gene)
            genetic_code.append(gc_row)
        return genetic_code

    def build_from_genes(self, genes):
        """
        Create the grid of this picture from a genetic code.
        :param genes: List of genes
        :return: None
        """
        gene_size = len(genes[0][0][0]) # dimension of a gene
        new_grid = [] # blank grid for filling
        for row in range(self.grid_size):
            new_row = [] # blank row for filling
            for col in range(self.grid_size):
                # following lines find the next RandRGB pixel
                gene_row = int(floor(row/gene_size)) # which gene
                pixel_row = row % (gene_size-1) # row of the pixel in the gene
                gene_col = int(floor(col/gene_size))
                pixel_col = col % (gene_size-1)
                pixel = genes[gene_row][gene_col][pixel_row][pixel_col]
                new_row.append(pixel)
            new_grid.append(new_row)
        self.grid = new_grid
