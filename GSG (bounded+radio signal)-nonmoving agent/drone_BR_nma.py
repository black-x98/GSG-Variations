import random
from entities_BR_nma import entities
import g_var_BR_nma

class drone(entities):


    drone_color = "#ffff66"

    def __init__(self,_canvas,_root, _drone_pos, _drone_signal, _adv_pos,_subarea_y,_subarea_x,_sub_y,_sub_x,_subarea_signal):
        self.canvas = _canvas
        self.root = _root
        self.drone_pos = _drone_pos
        self.drone_signal = _drone_signal
        self.adv_pos = _adv_pos
        self.subarea_y = _subarea_y
        self.subarea_x = _subarea_x
        self.sub_y = _sub_y
        self.sub_x = _sub_x
        self.subarea_signal = _subarea_signal
        self.drone_counter = 0

        g_var_BR_nma.drone_placement_array[_sub_y][_sub_x] += 1

        self.cur_y_drone = random.randint(round(g_var_BR_nma.dimension * self.subarea_y[self.sub_y][0]), round(g_var_BR_nma.dimension * self.subarea_y[self.sub_y][1]) - 1)
        self.cur_x_drone = random.randint(round(g_var_BR_nma.dimension * self.subarea_x[self.sub_x][0]), round(g_var_BR_nma.dimension * self.subarea_x[self.sub_x][1]) - 1)

        #unbounded drone placement:
        '''self.cur_x_drone = random.randint(0,g_var.dimension-2)
        self.cur_y_drone = random.randint(0,g_var.dimension-2)'''

        x_cor = self.cur_x_drone * g_var_BR_nma.block_size
        y_cor = self.cur_y_drone * g_var_BR_nma.block_size
        self.drone_pos[self.cur_y_drone][self.cur_x_drone] = 1
        self.canvas.create_oval(x_cor + 22, y_cor + 10, x_cor + 37, y_cor + 25, fill=self.drone_color, outline=g_var_BR_nma.bg_color)

    def move_drone(self):

        self.drone_signal[self.cur_y_drone][self.cur_x_drone] = 0
        '''print "erasing drone signal at ",
        print self.cur_y_drone,
        print ",",
        print self.cur_x_drone'''
        x_cor = self.cur_x_drone * g_var_BR_nma.block_size
        y_cor = self.cur_y_drone * g_var_BR_nma.block_size
        self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_BR_nma.bg_color, outline=g_var_BR_nma.bg_color)
        self.drone_pos[self.cur_y_drone][self.cur_x_drone] = 0
        lower_limit_x = -1
        lower_limit_y = -1
        upper_limit_x = 1
        upper_limit_y = 1
        self.canvas.create_oval(x_cor + 22, y_cor + 10, x_cor + 37, y_cor + 25, fill=g_var_BR_nma.bg_color, outline=g_var_BR_nma.bg_color)
        if self.cur_x_drone<=g_var_BR_nma.dimension*self.subarea_x[self.sub_x][0]:
                lower_limit_x = 0
        elif self.cur_x_drone>=g_var_BR_nma.dimension*self.subarea_x[self.sub_x][1]-1:
            upper_limit_x = 0
        if self.cur_y_drone<=g_var_BR_nma.dimension*self.subarea_y[self.sub_y][0]:
            lower_limit_y = 0
        elif self.cur_y_drone>=g_var_BR_nma.dimension*self.subarea_y[self.sub_y][1]-1:
            upper_limit_y = 0

        move_x =  random.randint(round(lower_limit_x),round(upper_limit_x))
        move_y =  random.randint(round(lower_limit_y),round(upper_limit_y))

        self.cur_x_drone = self.cur_x_drone + move_x
        self.cur_y_drone = self.cur_y_drone + move_y
        x_cor = self.cur_x_drone * g_var_BR_nma.block_size
        y_cor = self.cur_y_drone * g_var_BR_nma.block_size

        self.drone_pos[self.cur_y_drone][self.cur_x_drone] = 1 # Marking Drone Position
        self.canvas.create_oval(x_cor + 22, y_cor + 10, x_cor + 37, y_cor + 25, fill=self.drone_color, outline=g_var_BR_nma.bg_color)
        #if self.adv_pos[self.cur_y_drone][self.cur_x_drone] == 1:
        #if random.randint(0,1) == 1:
        if self.adv_pos[self.cur_y_drone][self.cur_x_drone] == 1:
            #self.drone_signal[self.cur_y_drone][self.cur_x_drone] = 1
            self.subarea_signal[self.sub_y][self.sub_x].append((self.cur_y_drone,self.cur_x_drone))
            #print "placed a subarea signal at " + str(self.cur_y_drone) + str(self.cur_x_drone)
            #print self.subarea_signal
            '''print "placed drone signal at (",
            print self.cur_y_drone,
            print ",",
            print self.cur_x_drone,
            print ")"'''
            #print "Drone sending signal!!! BEEP BEEP BEEP!! at " + self.cur_y_drone.__str__() + "," + self.cur_x_drone.__str__()

        self.drone_counter += 1

        if self.drone_counter < g_var_BR_nma.movement_limit:
            self.root.after(g_var_BR_nma.turn_gap_time, self.move_drone)
