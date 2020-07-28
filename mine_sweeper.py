import tkinter as tk
import random
import time
from PIL import Image, ImageTk
from Button import Button

class Mine_Sweeper(tk.Frame):

    game_size = {'easy': (8,10),
                 'medium': (14,18),
                 'hard': (20,24)}

    bomb_max = {'easy': 10, 'medium': 40, 'hard': 99}

    def __init__(self, root, image_dict, game_mode='easy'):
        super().__init__()

        self.root = root

        # Get the grid size based on the chosen game-mode
        self.grid_size = self.game_size[game_mode]

        # Get the maximum no. of bombs for the specified gamemode
        self.num_of_bombs = self.bomb_max[game_mode]

        # Contains a list to contain all the bomb locations
        self.bomb_location_list = []

        # Contains a dictionary of all the assets. 
        self.image_dict = image_dict

        self.mid_frame = tk.LabelFrame(root, bd=6)
        self.mid_frame.grid(row=1, columnspan=self.grid_size[1], rowspan=self.grid_size[0])

        self.bottom_frame = self.bottom_frame(root)

        # Assemble the game
        self.main()


    def main(self):
        """ Initialize the game """
        self.create_grid()
        self.create_bombs()
        self.update_button_scores()
        #self.set_images()
        #self.show_all_nums()

    
    def create_grid(self):
        """ Creates the object's grid filled with button objects """
        x_max, y_max = self.grid_size

        # A grid filled with button objects
        self.grid = []

        cls_ref = self

        for x_cord in range(x_max):
            small_list = []
            for y_cord in range(y_max):
                button = Button(root = self.mid_frame, x_cord = x_cord, y_cord = y_cord, val=0, class_ref=cls_ref, isPressed = False, image_dict=self.image_dict, image=self.image_dict[0], relief='raised', bd=3)
                button.configure(command = button.button_click)
                button.bind("<Button-3>", button.right_click)
                button.grid(row=x_cord, column=y_cord)
                small_list.append(button)
            self.grid.append(small_list)

    def create_bombs(self):
        """ Updates the object's grid with bombs """
        
        for i in range(self.num_of_bombs):
            # Update the button's value to indicate bomb
            x_cord, y_cord = self.get_random_coord()
            self.grid[x_cord][y_cord].Value = -1

            # Add the bomb locations to bomb locations list
            self.bomb_location_list.append((x_cord, y_cord))

    def get_random_coord(self):
        max_idx = self.grid_size[0]-1
        while True:
            random_x = random.randint(0, max_idx)
            random_y = random.randint(0, max_idx)

            coord = (random_x, random_y)

            if coord not in self.bomb_location_list:
                return coord
            else:
                continue

    def update_button_scores(self):
        for bomb_location in self.bomb_location_list:
            #print('===================BOMB at location ({}) finished ======================'.format(bomb_location))
            x_cord, y_cord = bomb_location
            for x in range(x_cord-1, x_cord+2):
                for y in range(y_cord-1, y_cord+2):
                    try:
                        assert 0 <= x and x < self.grid_size[0]
                        assert 0 <= y and y < self.grid_size[1]

                        val = self.grid[x][y].Value
                        if val != -1:
                            self.grid[x][y].Value += 1
                            #print('Button at ( {}, {} ) had value changed from {} to {}'.format(x, y, val, self.grid[x][y].Value))
                    except:
                        continue


    def flood_fill(self, button):
        x,y = button.x_cord,button.y_cord
        #print(x, y)
        for i in range(4):
            if i == 0:
                try:
                    new_x, new_y = x-1, y
                    assert (new_x >= 0 and new_x < self.grid_size[0])
                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    elif val != -1:
                        new_button.button_side_click()
                except:
                    continue

            if i == 1:
                # Look on the y- side of tile
                try:
                    new_x, new_y = x+1, y
                    assert (0 <= new_x < self.grid_size[0])

                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    elif val != -1:
                        new_button.button_side_click()
                except:
                    continue

            if i == 2:
                # Look on the x+ side of tile
                try:
                    new_x, new_y = x, y+1
                    assert (0 <= new_y < self.grid_size[1])

                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    elif val != -1:
                        new_button.button_side_click()
                except:
                    continue

            if i == 3:
                # Look on the x- side of tile
                try:
                    new_x, new_y = x, y-1
                    assert (0 <= new_y < self.grid_size[1])

                    new_button = self.grid[new_x][new_y]
                    val = new_button.Value

                    if val == 0:
                        new_button.button_click()
                        #self.flood_fill(new_button)
                    elif val != -1:
                        new_button.button_side_click()
                except:
                    continue

    def show_all_nums(self):
        for smal_list in self.grid:
            for button in smal_list:
                if button.Value != 0:
                    button.configure(text=str(button.Value))

    def bottom_frame(self, root):
        frame = tk.LabelFrame(root, bd=4)

        solve_button = tk.Button(frame, text='SOLVE', bd=3, relief='raised')
        solve_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=1, pady=3)

        retry_button = tk.Button(frame, text='RETRY', bd=3, relief='raised', command=self.reset_game)
        retry_button.pack(side=tk.RIGHT, padx=10, ipadx=10, ipady=1, pady=3)

        frame.grid(row=self.grid_size[0]+1,ipady=0,columnspan=self.grid_size[1], ipadx=self.grid_size[1]*5) #columnspan=self.grid_size[1], ipady=5, ipadx=self.grid_size[1]*8)

    def reset_game(self):
        for smal_list in self.grid:
            for button in smal_list:
                button.Value = 0
        self.main()



def gather_images():
    img_dict = {}
    image_size = (20,20)

    null_img = Image.open('assets/null.png')
    null_img = ImageTk.PhotoImage(null_img.resize(image_size, Image.ANTIALIAS))

    one_img = Image.open('assets/1.png')
    one_img = ImageTk.PhotoImage(one_img.resize(image_size, Image.ANTIALIAS))

    two_img = Image.open('assets/2.png')
    two_img = ImageTk.PhotoImage(two_img.resize(image_size, Image.ANTIALIAS))

    three_img = Image.open('assets/3.png')
    three_img = ImageTk.PhotoImage(three_img.resize(image_size, Image.ANTIALIAS))

    four_img = Image.open('assets/4.png')
    four_img = ImageTk.PhotoImage(four_img.resize(image_size, Image.ANTIALIAS))

    five_img = Image.open('assets/5.png')
    five_img = ImageTk.PhotoImage(five_img.resize(image_size, Image.ANTIALIAS))

    six_img = Image.open('assets/6.png')
    six_img = ImageTk.PhotoImage(six_img.resize(image_size, Image.ANTIALIAS))

    seven_img = Image.open('assets/7.png')
    seven_img = ImageTk.PhotoImage(seven_img.resize(image_size, Image.ANTIALIAS))

    eight_img = Image.open('assets/8.png')
    eight_img = ImageTk.PhotoImage(eight_img.resize(image_size, Image.ANTIALIAS))

    mine_img = Image.open('assets/-1.png')
    mine_img = ImageTk.PhotoImage(mine_img.resize(image_size, Image.ANTIALIAS))

    flag_img = Image.open('assets/flag.png')
    flag_img = ImageTk.PhotoImage(flag_img.resize(image_size, Image.ANTIALIAS))

    img_dict[0] = null_img
    img_dict[1] = one_img
    img_dict[2] = two_img
    img_dict[3] = three_img
    img_dict[4] = four_img
    img_dict[5] = five_img
    img_dict[6] = six_img
    img_dict[7] = seven_img
    img_dict[8] = eight_img     
    img_dict[-1] = mine_img
    img_dict[9] = flag_img
    
    return img_dict


root = tk.Tk()

img = gather_images()
mine = Mine_Sweeper(root, img, game_mode='easy')

mine.mainloop()