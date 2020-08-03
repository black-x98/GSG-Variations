import random
from entities_UR import entities
import g_var_UR

class agent(entities):

    agent_counter = 0
    agent_color = "green"


    def __init__(self,_canvas,_root,_agent_pos,_cell_resources,_target_pos,_round_marking,_drone_signal):
        self.canvas = _canvas
        self.root = _root
        self.agent_pos = _agent_pos
        self.cell_resource = _cell_resources
        self.target_pos = _target_pos
        self.round_marking = _round_marking
        self.drone_signal = _drone_signal

        while True:
            pair = self.round_marking[random.randint(0,len(self.round_marking)-1)]
            self.cur_x_agent = pair[1]
            self.cur_y_agent = pair[0]
            if self.agent_pos[self.cur_x_agent][self.cur_y_agent]==0:
                break
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 1
        self.prev_y = -1
        self.prev_x = -1
        self.prev2_y = -1
        self.prev2_x = -1


        self.my_target = _target_pos[random.randint(0,len(_target_pos)-1)]
        ##print "my target : " + str(self.my_target)

        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 1
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)

        ##print "Placed an agent at the position: " + self.cur_x_agent.__str__() + " mmmm " + self.cur_y_agent.__str__()

    def move_agent(self):

        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR.bg_color, outline=g_var_UR.bg_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 0
        lower_limit_x = -1
        lower_limit_y = -1
        upper_limit_x = 1
        upper_limit_y = 1

        if self.cur_x_agent<1:
            lower_limit_x = 0
        if self.cur_y_agent<1:
            lower_limit_y = 0
        if self.cur_x_agent>g_var_UR.dimension-2:
            upper_limit_x=0
        if self.cur_y_agent>g_var_UR.dimension-2:
            upper_limit_y=0

        move_x =  random.randint(lower_limit_x,upper_limit_x)
        move_y =  random.randint(lower_limit_y,upper_limit_y)
        self.cur_x_agent = self.cur_x_agent + move_x
        self.cur_y_agent = self.cur_y_agent + move_y
        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size

        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 1

        self.agent_counter += 1
        if move_x != 0 or move_y != 0:
            g_var_UR.distance_travelled += 1

        if self.agent_counter < g_var_UR.movement_limit:
            self.root.after(g_var_UR.turn_gap_time, self.move_agent)

    def check_resource(self):

        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR.bg_color, outline=g_var_UR.bg_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 0


        ##print "Agent " + self.agent_id.__str__() + " moved to " + self.cur_x_agent.__str__() + "," + self.cur_y_agent.__str__()
        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 1

        self.agent_counter += 1

        g_var_UR.distance_travelled += 1

        if self.agent_counter < g_var_UR.movement_limit:
            self.root.after(g_var_UR.turn_gap_time, self.check_resource)
            
    def move_spec_guard(self):
        ##print "inside move_spec**************"
        ##print " checking for drone signal nearby "
        for i in range(5):
            for j in range(5):
                temp_y = self.cur_y_agent-1+i
                temp_x = self.cur_x_agent-1+j
                if temp_y>=0 and temp_y<=g_var_UR.dimension-1 and temp_x>=0 and temp_x<=g_var_UR.dimension-1:
                    if self.drone_signal[temp_y][temp_x] == 1:
                        self.my_target = (temp_y,temp_x)
                        #print "AGENT DETECTED A DRONE SIGNAL!!!"
                        #print "Agent heading to " + str(self.my_target) + " from " + str(self.cur_y_agent) + "," + str(self.cur_x_agent)
                        break
        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR.bg_color, outline=g_var_UR.bg_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 0

        offset_y = self.my_target[0] - self.cur_y_agent
        offset_x = self.my_target[1] - self.cur_x_agent

        if offset_x==0 and offset_y==0:
            temp = self.target_pos[random.randint(0,len(self.target_pos)-1)]
            self.my_target= temp
            ##print "New target of spec guard at " + str(self.my_target[0]) + "," + str(self.my_target[1])

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
        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size

        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 1

        self.agent_counter += 1
        if move_x != 0 or move_y != 0:
            g_var_UR.distance_travelled += 1

        if self.agent_counter < g_var_UR.movement_limit:
            self.root.after(g_var_UR.turn_gap_time, self.move_spec_guard)

    def agent_go_round(self):

        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.canvas.create_polygon(x_cor + 15, y_cor + 20, x_cor + 15, y_cor + 35, x_cor + 30, y_cor + 35, x_cor + 30, y_cor + 20, fill=g_var_UR.bg_color, outline=g_var_UR.bg_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 0

        got_it = False
        for i in range(3):
            for j in range(3):
                if i==1 and j==1 or i<0 or j<0:
                    continue
                if i==self.cur_y_agent and j==self.cur_x_agent:
                    continue
                if self.cur_y_agent-1+i > g_var_UR.dimension-2 or self.cur_x_agent > g_var_UR.dimension-2:
                    continue

                if self.cell_resource[self.cur_y_agent-1+i][self.cur_x_agent-1+j]==-1:
                    if self.prev_y == self.cur_y_agent-1+i and self.prev_x == self.cur_x_agent-1+j:
                        continue
                    if self.prev2_y == self.cur_y_agent-1+i and self.prev2_x == self.cur_x_agent-1+j:
                        continue
                    self.prev_x = self.cur_x_agent
                    self.prev_y = self.cur_y_agent
                    self.cur_x_agent = self.cur_x_agent-1+j
                    self.cur_y_agent = self.cur_y_agent-1+i

                    got_it = True
                    break
            if got_it:
                break
        ##print "Agent " + self.agent_id.__str__() + " moved to " + self.cur_x_agent.__str__() + "," + self.cur_y_agent.__str__()
        x_cor = self.cur_x_agent * g_var_UR.block_size
        y_cor = self.cur_y_agent * g_var_UR.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.agent_color)
        self.agent_pos[self.cur_x_agent][self.cur_y_agent] = 1

        self.agent_counter += 1

        g_var_UR.distance_travelled += 1

        if self.agent_counter < g_var_UR.movement_limit:
            self.root.after(g_var_UR.turn_gap_time, self.agent_go_round)

