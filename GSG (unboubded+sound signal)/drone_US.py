import random
from entities_US import entities
import g_var_US

class drone(entities):

    drone_counter = 0
    drone_color = "#ffff66"

    def __init__(self,_canvas,_root, _drone_pos, _drone_signal, _adv_pos):
        self.canvas = _canvas
        self.root = _root
        self.drone_pos = _drone_pos
        self.drone_signal = _drone_signal
        self.adv_pos = _adv_pos
        self.cur_x_drone = random.randint(0, g_var_US.dimension - 2)
        self.cur_y_drone = random.randint(0, g_var_US.dimension - 2)

        x_cor = self.cur_x_drone * g_var_US.block_size
        y_cor = self.cur_y_drone * g_var_US.block_size
        self.drone_pos[self.cur_x_drone][self.cur_y_drone] = 1
        self.canvas.create_oval(x_cor + 22, y_cor + 10, x_cor + 37, y_cor + 25, fill=self.drone_color, outline=g_var_US.bg_color)

    def move_drone(self):

        x_cor = self.cur_x_drone * g_var_US.block_size
        y_cor = self.cur_y_drone * g_var_US.block_size
        self.drone_pos[self.cur_x_drone][self.cur_y_drone] = 0
        self.canvas.create_oval(x_cor + 22, y_cor + 10, x_cor + 37, y_cor + 25, fill=g_var_US.bg_color, outline=g_var_US.bg_color)
        self.drone_signal[self.cur_y_drone][self.cur_x_drone] = 0 # erasing the signal, if any that is!!!

        lower_limit_x = -1
        lower_limit_y = -1
        upper_limit_x = 1
        upper_limit_y = 1
        if self.cur_x_drone<1:
            lower_limit_x = 0
        if self.cur_y_drone<1:
            lower_limit_y = 0
        if self.cur_x_drone>g_var_US.dimension-2:
            upper_limit_x=0
        if self.cur_y_drone>g_var_US.dimension-2:
            upper_limit_y=0

        self.cur_x_drone = (self.cur_x_drone + random.randint(lower_limit_x,upper_limit_x))
        self.cur_y_drone = (self.cur_y_drone + random.randint(lower_limit_y,upper_limit_y))


        x_cor = self.cur_x_drone * g_var_US.block_size
        y_cor = self.cur_y_drone * g_var_US.block_size
        self.drone_pos[self.cur_x_drone][self.cur_y_drone] = 1 # Marking Drone Position
        self.canvas.create_oval(x_cor + 22, y_cor + 10, x_cor + 37, y_cor + 25, fill=self.drone_color, outline=g_var_US.bg_color)
        if self.adv_pos[self.cur_y_drone][self.cur_x_drone] == 1:
            self.drone_signal[self.cur_y_drone][self.cur_x_drone] = 1
            #print "Drone sending signal!!! BEEP BEEP BEEP!! at " + self.cur_y_drone.__str__() + "," + self.cur_x_drone.__str__()

        self.drone_counter += 1

        if self.drone_counter < g_var_US.movement_limit:
            self.root.after(g_var_US.turn_gap_time, self.move_drone)
