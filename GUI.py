import cv2

from Evolver import Evolver

from Tkinter import Tk, RIGHT, BOTH, RAISED, Canvas, Frame, Button
#from tkinter import Tk, RIGHT, BOTH, RAISED, Canvas, Frame, Button

class EvoViewer(Frame):
    """
    GUI for basic testing of picture displaying.
    """
    def __init__(self, parent, evolver):
        """
        Create a new window.
        :param parent: tkinter root frame.
        """
        Frame.__init__(self, parent)

        self.pic_evo = evolver
        self.grid_size = evolver.grid_size
        self.parent = parent
        self.Init_UI()


    def Init_UI(self):
        """
        Create the UI including the window and buttons.
        """
        self.parent.title("Buttons")
        self.canvas = Canvas(self, relief=RAISED, borderwidth=1,
                             width=self.grid_size, height=self.grid_size,
                             background="white")
        self.canvas.pack()
        # self.canvas.bind("<Button-1>",self.Gen_Pic_Test)
        # self.canvas.create_rectangle(0,0,10,10,fill="black")
        self.pack(fill=BOTH, expand=True)
        nextButton = Button(self, text="Next", command=self.view_next)
        nextButton.pack(side=RIGHT)
        prevButton = Button(self, text="Prev", command=self.view_prev)
        prevButton.pack(side=RIGHT)
        refrButton = Button(self, text="Refresh", command=self.refr_view)
        refrButton.pack(side=RIGHT)
        strtButton = Button(self, text="Start", command=self.start_evo)
        strtButton.pack(side=RIGHT)

    def display_pic_tk(self, pic):
        """
        Fills the screen with pixels generated from a picture.
        :param pic: Picture to display a version of
        """
        test_grid = pic.render_picture()
        rects = []
        x,y = (0,0)
        for row in test_grid:
            y += 2
            x=0
            for cell in row:
                x += 2
                #print cell
                try:
                    rects.append(self.canvas.create_rectangle(x, y, x-2, y-2, fill=cell, width=0))
                except:
                    print(cell)
        self.parent.update_idletasks()

    def display_pic(self, pic):
        """
        Display a Picture using OpenCV methods
        :param pic: The Picture object to be displayed
        """
        img_matrix = pic.render_picture()
        cv2.imshow('Picture', img_matrix)
        k = cv2.waitKey(0) & 0xFF
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
        elif k == ord('s'): # wait for 's' key to save and exit
            img_name = 'img_{}.png'.format(pic.pic_id)
            cv2.imwrite(img_name, img_matrix)
            cv2.destroyAllWindows()

    def start_evo(self):
        """
        Displays the first picture in the picture evolver of this object.
        """
        self.evo_gen_size = self.pic_evo.pop_size
        self.evo_index=0
        self.display_pic(self.pic_evo.get_pic_at(self.evo_index))

    def view_next(self):
        """
        Display next picture in population.
        """
        self.evo_index = (self.evo_index + 1) % self.evo_gen_size
        self.display_pic(self.pic_evo.get_pic_at(self.evo_index))
        pass

    def view_prev(self):
        """
        Display previous picture in population.
        """
        self.evo_index = (self.evo_index - 1) % self.evo_gen_size
        self.display_pic(self.pic_evo.get_pic_at(self.evo_index))
        pass

    def refr_view(self):
        """
        Refresh the picture by creating a new render of the same picture.
        See Picture class.
        """
        self.display_pic(self.pic_evo.get_pic_at(self.evo_index))
        pass


class PictureViewer(Frame):
    """
    GUI for basic testing of picture displaying.
    """
    def __init__(self, parent, pic_list):
        """
        Create a new window.
        :param parent: tkinter root frame.
        :param pic_list: list of picturess of length > 0
        """
        Frame.__init__(self, parent)

        self.pic_list = pic_list
        self.grid_size = pic_list[0].grid_size
        self.parent = parent
        self.pic_index = 0
        self.Init_UI()


    def Init_UI(self):
        """
        Create the UI including the window and buttons.
        """
        self.parent.title("Buttons")
        self.canvas = Canvas(self, relief=RAISED, borderwidth=1,
                             width=self.grid_size, height=self.grid_size,
                             background="white")
        self.canvas.pack()
        # self.canvas.bind("<Button-1>",self.Gen_Pic_Test)
        # self.canvas.create_rectangle(0,0,10,10,fill="black")
        self.pack(fill=BOTH, expand=True)
        nextButton = Button(self, text="Next", command=self.view_next)
        nextButton.pack(side=RIGHT)
        prevButton = Button(self, text="Prev", command=self.view_prev)
        prevButton.pack(side=RIGHT)
        refrButton = Button(self, text="Refresh", command=self.refr_view)
        refrButton.pack(side=RIGHT)
        strtButton = Button(self, text="Start", command=self.start_viewing())
        strtButton.pack(side=RIGHT)

    def display_pic(self, pic):
        """
        Fills the screen with pixels generated from a picture.
        :param pic: Picture to display a version of
        """
        test_grid = pic.render_picture()
        rects = []
        x,y = (0,0)
        for row in test_grid:
            y += 2
            x=0
            for cell in row:
                rgb_hex_string = '#'
                for val in cell:
                    rgb_hex_string += str(hex(int(val))).ljust(4, '0')[2:]
                x += 2
                try:
                    rects.append(self.canvas.create_rectangle(x, y, x-2, y-2,
                                                              fill=rgb_hex_string,
                                                              width=0)

                                 )
                except:
                    print(rgb_hex_string)
        self.parent.update_idletasks()

    def start_viewing(self):
        """
        Displays the first picture in the picture evolver of this object.
        """
        self.pic_index=0
        self.display_pic(self.pic_list[self.pic_index])

    def view_next(self):
        """
        Display next picture in population.
        """
        self.pic_index = (self.pic_index + 1) % len(self.pic_list)
        self.display_pic(self.pic_list[self.pic_index])
        pass

    def view_prev(self):
        """
        Display previous picture in population.
        """
        self.pic_index = (self.pic_index - 1) % len(self.pic_list)
        self.display_pic(self.pic_list[self.pic_index])
        pass

    def refr_view(self):
        """
        Refresh the picture by creating a new render of the same picture.
        See Picture class.
        """
        self.display_pic(self.pic_list[self.pic_index])
        pass


def display_pic(pic):
    root = Tk()
    display = PictureViewer(root, pic)
    root.mainloop()


def main():
    """
    ... Come on, you know what this is.
    """
    root = Tk()
    pic_evo = Evolver(grid_size=300)
    app = EvoViewer(root, pic_evo)
    root.mainloop()


if __name__ == '__main__':
    main()

