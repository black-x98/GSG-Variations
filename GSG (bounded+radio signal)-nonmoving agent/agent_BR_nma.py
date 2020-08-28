import random
from entities_BR_nma import entities
import g_var_BR_nma

class agent(entities):


    agent_color = "#00FF00"#"green"

    def __init__(self,_canvas,_root,_agent_pos,_cell_resources,_target_pos,_round_marking,_drone_signal,_subarea_y,_subarea_x,_sub_y,_sub_x, _adv_pos, _subarea_signal):
        self.canvas = _canvas
        self.root = _root
        self.agent_pos = _agent_pos
        self.cell_resource = _cell_resources
        self.target_pos = _target_pos
        self.round_marking = _round_marking
        self.drone_signal = _drone_signal
        self.subarea_y = _subarea_y
        self.subarea_x = _subarea_x
        self.sub_y = _sub_y
        self.sub_x = _sub_x
        self.adv_pos = _adv_pos
        self.agent_counter = 0
        self.subarea_signal = _subarea_signal
        self.active_target = False
        self.move_skip = 0
        #print "The mult y's are: " + str(_subarea_y[self.sub_y][0]) + ","+ str(_subarea_y[self.sub_y][1])

        # move_spec initilization
        self.cur_y_agent = random.randint(round(g_var_BR_nma.dimension * self.subarea_y[self.sub_y][0]), round(g_var_BR_nma.dimension * self.subarea_y[self.sub_y][1]) - 1)
        self.cur_x_agent = random.randint(round(g_var_BR_nma.dimension * self.subarea_x[self.sub_x][0]), round(g_var_BR_nma.dimension * self.subarea_x[self.sub_x][1]) - 1)

        self.my_target = _target_pos[random.randint(0,len(_target_pos)-1)]

        x_cor = self.cur_x_agent * g_var_BR_nma.block_size
        y_cor = self.cur_y_agent * g_var_BR_nma.block_size
        self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)


    def move_agent(self):

        # detected drone signal
        if self.subarea_signal[self.sub_y][self.sub_x] != []:
            self.my_target = self.subarea_signal[self.sub_y][self.sub_x].pop()
            self.active_target = True
            #print "DETECTED a subarea signal at " + str(self.my_target)
            #print "After popping a subarea signal, length of list is: " + len(self.subarea_signal).__str__()
        self.move_skip = (self.move_skip + 1) % g_var_BR_nma.move_skip_toggle

        if self.active_target==True:
            #print "going to drone signalled place <- " + str(self.my_target[0]) + "," + str(self.my_target[1]) + " ->"
            x_cor = self.cur_x_agent * g_var_BR_nma.block_size
            y_cor = self.cur_y_agent * g_var_BR_nma.block_size
            self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_BR_nma.bg_color, outline=g_var_BR_nma.bg_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0

            x_offset = self.my_target[1] - self.cur_x_agent
            y_offset = self.my_target[0] - self.cur_y_agent

            if x_offset == 0 and y_offset == 0:
                #print "Reached the Radio signalled spot, setting active target FALSE" + str(self.my_target)
                self.active_target=False

            move_x, move_y = 0,0
            if x_offset>0 and self.cur_x_agent<g_var_BR_nma.dimension-1: move_x = +1
            elif x_offset<0 and self.cur_x_agent>0 : move_x=-1
            if y_offset>0 and self.cur_y_agent<g_var_BR_nma.dimension-1: move_y = +1
            elif y_offset<0 and self.cur_y_agent>0 : move_y=-1

            self.cur_x_agent += move_x
            self.cur_y_agent += move_y

            #print "drawing agent at " + str(self.my_target[0]) + "," + str(self.my_target[1]) + " "
            x_cor = self.cur_x_agent * g_var_BR_nma.block_size
            y_cor = self.cur_y_agent * g_var_BR_nma.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 3

            '''if self.adv_pos[self.cur_y_agent][self.cur_x_agent] == 1: # jawar pore 
                print "Shabbash drone er baccha!!! Signal shune dhoira falaisi poacher re at: ",
                print self.cur_y_agent, self.cur_x_agent'''

            self.agent_counter += 1
            g_var_BR_nma.distance_travelled += 1

            '''
        elif self.move_skip==0:
            x_cor = self.cur_x_agent * g_var_BR_nm.block_size
            y_cor = self.cur_y_agent * g_var_BR_nm.block_size
            # earsing agent
            self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_BR_nm.bg_color, outline=g_var_BR_nm.bg_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0
            lower_limit_x = -1
            lower_limit_y = -1
            upper_limit_x = 1
            upper_limit_y = 1

            if self.cur_x_agent<=g_var_BR_nm.dimension*self.subarea_x[self.sub_x][0]:
                lower_limit_x = 0
            elif self.cur_x_agent>=g_var_BR_nm.dimension*self.subarea_x[self.sub_x][1]-1:
                upper_limit_x = 0
            if self.cur_y_agent<=g_var_BR_nm.dimension*self.subarea_y[self.sub_y][0]:
                lower_limit_y = 0
            elif self.cur_y_agent>=g_var_BR_nm.dimension*self.subarea_y[self.sub_y][1]-1:
                upper_limit_y = 0

            move_x =  random.randint(round(lower_limit_x),round(upper_limit_x))
            move_y =  random.randint(round(lower_limit_y),round(upper_limit_y))
            
            self.cur_x_agent = self.cur_x_agent + move_x
            self.cur_y_agent = self.cur_y_agent + move_y
            x_cor = self.cur_x_agent * g_var_BR_nm.block_size
            y_cor = self.cur_y_agent * g_var_BR_nm.block_size

            # drawing agent
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1

            self.agent_counter += 1
            if move_x != 0 or move_y != 0:
                g_var_BR_nm.distance_travelled += 1
            '''
        else:
            x_cor = self.cur_x_agent * g_var_BR_nma.block_size
            y_cor = self.cur_y_agent * g_var_BR_nma.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)

        if self.agent_counter < g_var_BR_nma.movement_limit:
            self.root.after(g_var_BR_nma.turn_gap_time, self.move_agent)


