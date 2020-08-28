import random
from entities_UR_nma import entities
import g_var_UR_nma

class agent(entities):

    agent_counter = 0
    agent_color = "green"


    def __init__(self,_canvas,_root,_agent_pos,_cell_resources,_drone_signal):
        self.canvas = _canvas
        self.root = _root
        self.agent_pos = _agent_pos
        self.cell_resource = _cell_resources
        self.drone_signal = _drone_signal
        self.move_skip = 0
        self.drone_signal_flag = False

        '''while True:
            pair = self.round_marking[random.randint(0,len(self.round_marking)-1)]
            self.cur_x_agent = pair[1]
            self.cur_y_agent = pair[0]
            if self.agent_pos[self.cur_y_agent][self.cur_x_agent]==0:
                break
        '''
        self.cur_y_agent= random.randint(1, g_var_UR_nma.dimension - 2)
        self.cur_x_agent= random.randint(1, g_var_UR_nma.dimension - 2)
        self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1
        self.prev_y = -1
        self.prev_x = -1
        self.prev2_y = -1
        self.prev2_x = -1


        '''while(True):
            self.my_target[0] = random.randint(0,g_var_UR.dimension-1)
            self.my_target[1] = random.randint(0,g_var_UR.dimension-1)
            if self.cell_resource[self.my_target[0]][self.my_target[1]] > 0:
                break'''


        x_cor = self.cur_x_agent * g_var_UR_nma.block_size
        y_cor = self.cur_y_agent * g_var_UR_nma.block_size
        self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)

        ##print "Placed an agent at the position: " + self.cur_x_agent.__str__() + " mmmm " + self.cur_y_agent.__str__()

    def move_agent(self):

        x_cor = self.cur_x_agent * g_var_UR_nma.block_size
        y_cor = self.cur_y_agent * g_var_UR_nma.block_size
        self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR_nma.bg_color, outline=g_var_UR_nma.bg_color)
        self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0
        lower_limit_x = -1
        lower_limit_y = -1
        upper_limit_x = 1
        upper_limit_y = 1

        if self.cur_x_agent<1:
            lower_limit_x = 0
        if self.cur_y_agent<1:
            lower_limit_y = 0
        if self.cur_x_agent>g_var_UR_nma.dimension-2:
            upper_limit_x=0
        if self.cur_y_agent>g_var_UR_nma.dimension-2:
            upper_limit_y=0

        move_x =  random.randint(lower_limit_x,upper_limit_x)
        move_y =  random.randint(lower_limit_y,upper_limit_y)
        self.cur_x_agent = self.cur_x_agent + move_x
        self.cur_y_agent = self.cur_y_agent + move_y
        x_cor = self.cur_x_agent * g_var_UR_nma.block_size
        y_cor = self.cur_y_agent * g_var_UR_nma.block_size

        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
        self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1

        self.agent_counter += 1
        if move_x != 0 or move_y != 0:
            g_var_UR_nma.distance_travelled += 1

        if self.agent_counter < g_var_UR_nma.movement_limit:
            self.root.after(g_var_UR_nma.turn_gap_time, self.move_agent)

            
    def move_spec_guard(self):

        self.move_skip = (self.move_skip + 1) % g_var_UR_nma.move_skip_toggle
        ##print "inside move_spec**************"
        ##print " checking for drone signal nearby "
        for i in range(3):
            for j in range(3):
                temp_y = self.cur_y_agent-1+i
                temp_x = self.cur_x_agent-1+j
                if temp_y>=0 and temp_y<=g_var_UR_nma.dimension-1 and temp_x>=0 and temp_x<=g_var_UR_nma.dimension-1:
                    if self.drone_signal[temp_y][temp_x] == 1:
                        self.my_target = (temp_y,temp_x)
                        self.drone_signal_flag = True
                        #print "AGENT DETECTED A DRONE SIGNAL!!!"
                        ##print "Agent heading to " + str(self.my_target) + " from " + str(self.cur_y_agent) + "," + str(self.cur_x_agent)
                        break
        #print self.move_skip, self.drone_signal_flag

        if self.drone_signal_flag==True:
            #print "inside DRONE SIG MODE"
            x_cor = self.cur_x_agent * g_var_UR_nma.block_size
            y_cor = self.cur_y_agent * g_var_UR_nma.block_size
            self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR_nma.bg_color, outline=g_var_UR_nma.bg_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0

            offset_y = self.my_target[0] - self.cur_y_agent
            offset_x = self.my_target[1] - self.cur_x_agent

            if offset_x==0 and offset_y==0:
                self.drone_signal_flag = False

            move_x = 0
            move_y = 0
            if offset_x>0:
                move_x = 1
            elif offset_x<0:
                move_x = -1
            if offset_y>0:
                move_y = 1
            elif offset_y<0:
                move_y = -1

            self.cur_x_agent = self.cur_x_agent + move_x
            self.cur_y_agent = self.cur_y_agent + move_y
            x_cor = self.cur_x_agent * g_var_UR_nma.block_size
            y_cor = self.cur_y_agent * g_var_UR_nma.block_size

            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1

            if offset_x!=0 or offset_y!=0:
                #print " increasing distance drone SIGNAL mode"
                g_var_UR_nma.distance_travelled += 1
            '''
        elif self.move_skip==0:
            #print "inside NORMAL MODE"
            x_cor = self.cur_x_agent * g_var_UR_nma.block_size
            y_cor = self.cur_y_agent * g_var_UR_nma.block_size
            self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR_nma.bg_color, outline=g_var_UR_nma.bg_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 0

            lower_limit_x = -1
            lower_limit_y = -1
            upper_limit_x = 1
            upper_limit_y = 1
            if self.cur_x_agent<1:
                lower_limit_x = 0
            if self.cur_y_agent<1:
                lower_limit_y = 0
            if self.cur_x_agent>g_var_UR_nma.dimension-2:
                upper_limit_x=0
            if self.cur_y_agent>g_var_UR_nma.dimension-2:
                upper_limit_y=0
            normal_move_x = random.randint(lower_limit_x,upper_limit_x)
            normal_move_y = random.randint(lower_limit_y,upper_limit_y)
            self.cur_x_agent = (self.cur_x_agent + normal_move_x)
            self.cur_y_agent = (self.cur_y_agent + normal_move_y)

            x_cor = self.cur_x_agent * g_var_UR_nma.block_size
            y_cor = self.cur_y_agent * g_var_UR_nma.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
            self.agent_pos[self.cur_y_agent][self.cur_x_agent] = 1

            if normal_move_x != 0 or normal_move_y != 0:
                g_var_UR_nma.distance_travelled += 1
                #print " inceasing distance normal toggle mode"
            '''
        else:
            x_cor = self.cur_x_agent * g_var_UR_nma.block_size
            y_cor = self.cur_y_agent * g_var_UR_nma.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)

        self.agent_counter += 1
        if self.agent_counter < g_var_UR_nma.movement_limit:
            self.root.after(g_var_UR_nma.turn_gap_time, self.move_spec_guard)

