import random
from entities import entities
import g_var

class agent(entities):


    agent_color = "green"

    def __init__(self,_canvas,_root,_agent_pos,_cell_resources,_target_pos,_round_marking,_drone_signal,_sub_mult_y,_sub_mult_x, _adv_pos):
        self.canvas = _canvas
        self.root = _root
        self.agent_pos = _agent_pos
        self.cell_resource = _cell_resources
        self.target_pos = _target_pos
        self.round_marking = _round_marking
        self.drone_signal = _drone_signal
        self.sub_mult_y =  _sub_mult_y
        self.sub_mult_x =  _sub_mult_x
        self.adv_pos = _adv_pos
        self.agent_counter = 0
        self.move_skip = 0
        self.active_target = False # flag indicating whether
        #print "The mult y's are: " + str(_sub_mult_y[0]) + ","+ str(_sub_mult_y[1])

        # move_spec initilization
        self.cur_y_agent = random.randint(round(g_var.dimension*self.sub_mult_y[0]),round(g_var.dimension*self.sub_mult_y[1])-1)
        self.cur_x_agent = random.randint(round(g_var.dimension*self.sub_mult_x[0]),round(g_var.dimension*self.sub_mult_x[1])-1)


        self.my_target = _target_pos[random.randint(0,len(_target_pos)-1)]

        x_cor = self.cur_x_agent * g_var.block_size
        y_cor = self.cur_y_agent * g_var.block_size
        self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)


    def move_agent(self):
        self.move_skip = (self.move_skip + 1) % g_var.move_skip_toggle
        # checking drone signal
        for i in range(3):
            for j in range(3):
                if i==1 and j==1:
                    continue
                temp_y = self.cur_y_agent-1+i
                temp_x = self.cur_x_agent-1+j
                if temp_y>=g_var.dimension*self.sub_mult_y[0] and temp_y<=g_var.dimension*self.sub_mult_y[1]-1 and temp_x>=g_var.dimension*self.sub_mult_x[0] and temp_x<=g_var.dimension*self.sub_mult_x[1]-1:
                    if self.drone_signal[temp_y][temp_x] == 1:
                        self.my_target = (temp_y,temp_x)
                        self.active_target = True
                        #print "AGENT DETECTED A DRONE SIGNAL!!!"
                        ##print "Agent heading to " + str(self.my_target) + " from " + str(self.cur_y_agent) + "," + str(self.cur_x_agent)
                        break

        if self.active_target==True:
            #erasing previous position
            #print "going to drone signalled place <- " + str(self.my_target[0]) + "," + str(self.my_target[1]) + " ->"
            x_cor = self.cur_x_agent * g_var.block_size
            y_cor = self.cur_y_agent * g_var.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=g_var.bg_color,outline=g_var.bg_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0

            self.cur_x_agent = self.my_target[1]
            self.cur_y_agent = self.my_target[0]
            x_cor = self.cur_x_agent * g_var.block_size
            y_cor = self.cur_y_agent * g_var.block_size

            #print "drawing agent at " + str(self.my_target[0]) + "," + str(self.my_target[1]) + " "
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 3

            '''if self.adv_pos[self.cur_y_agent][self.cur_x_agent] == 1: # jawar pore 
                print "Shabbash drone er baccha!!! Signal shune dhoira falaisi poacher re at: ",
                print self.cur_y_agent, self.cur_x_agent'''

            self.agent_counter += 1
            g_var.distance_travelled += 1

        elif self.move_skip==0:

            x_cor = self.cur_x_agent * g_var.block_size
            y_cor = self.cur_y_agent * g_var.block_size
            # earsing agent
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=g_var.bg_color,outline=g_var.bg_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0
            lower_limit_x = -1
            lower_limit_y = -1
            upper_limit_x = 1
            upper_limit_y = 1

            if self.cur_x_agent<=g_var.dimension*self.sub_mult_x[0]:
                lower_limit_x = 0
            elif self.cur_x_agent>=g_var.dimension*self.sub_mult_x[1]-1:
                upper_limit_x = 0
            if self.cur_y_agent<=g_var.dimension*self.sub_mult_y[0]:
                lower_limit_y = 0
            elif self.cur_y_agent>=g_var.dimension*self.sub_mult_y[1]-1:
                upper_limit_y = 0

            move_x =  random.randint(round(lower_limit_x),round(upper_limit_x))
            move_y =  random.randint(round(lower_limit_y),round(upper_limit_y))
            '''print "move added ",
            print move_x, move_y'''
            self.cur_x_agent = self.cur_x_agent + move_x
            self.cur_y_agent = self.cur_y_agent + move_y
            x_cor = self.cur_x_agent * g_var.block_size
            y_cor = self.cur_y_agent * g_var.block_size

            # drawing agent
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1

            self.agent_counter += 1
            if move_x != 0 or move_y != 0:
                g_var.distance_travelled += 1

        if self.agent_counter < g_var.movement_limit:
            self.root.after(g_var.turn_gap_time, self.move_agent)


