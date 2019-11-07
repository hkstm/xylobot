from tkinter import *
import math
import time

class Window(Frame):
    def init_window(self):
        direction = 0
        type = "backwards"
        lower_joint_angle = 160
        upper_joint_angle = 210
        base_length = 20
        lower_arm_length = 16
        upper_arm_length = 14.5
        distance = 20
        multiplier = 20
        sleep_time = 0.01
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()/2
        xylophone_height = 10 
        keywidth = multiplier*2
        birds_eye_view = Canvas(self, width = width, height = height, background = "black")
        side_view = Canvas(self, width = width, height = height, background = "black")
        birds_eye_view.grid(row = 1, column = 0)
        side_view.grid(row = 0, column = 0)
        self.pack(fill=BOTH, expand=1)
        division = multiplier*1
        top = height/2-multiplier*5.53
        bottom = height/2+multiplier*5.53
        left = width/2-multiplier*11-division/2
        c = 0.4714
        birds_eye_view.create_rectangle(left+0*(keywidth+division), top+0*c, left+0*(keywidth+division)+keywidth, bottom-0*c, fill = "blue")
        birds_eye_view.create_rectangle(left+1*(keywidth+division), top+1*c, left+1*(keywidth+division)+keywidth, bottom-1*c, fill = "green")
        birds_eye_view.create_rectangle(left+2*(keywidth+division), top+2*c, left+2*(keywidth+division)+keywidth, bottom-2*c, fill = "yellow")
        birds_eye_view.create_rectangle(left+3*(keywidth+division), top+3*c, left+3*(keywidth+division)+keywidth, bottom-3*c, fill = "orange")
        birds_eye_view.create_rectangle(left+4*(keywidth+division), top+4*c, left+4*(keywidth+division)+keywidth, bottom-4*c, fill = "red")
        birds_eye_view.create_rectangle(left+5*(keywidth+division), top+5*c, left+5*(keywidth+division)+keywidth, bottom-5*c, fill = "purple")
        birds_eye_view.create_rectangle(left+6*(keywidth+division), top+6*c, left+6*(keywidth+division)+keywidth, bottom-6*c, fill = "white")
        birds_eye_view.create_rectangle(left+7*(keywidth+division), top+7*c, left+7*(keywidth+division)+keywidth, bottom-7*c, fill = "darkblue")
        side_view.create_rectangle(width/2-multiplier*5.53, height+100-multiplier*xylophone_height, width/2+multiplier*5.53, height+100, fill="blue")
        base = bottom+multiplier*distance -110.6 
        b_line = birds_eye_view.create_line(width/2, base, 
                                                    width/2, base,
                                                    width/2+multiplier*lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction)),
                                                    base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                                    width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
                                                                        upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))),
                                                    base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                     upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
                                                    fill = "grey", width = 10, joinstyle = ROUND)
        s_line = side_view.create_line(width/2+multiplier*(distance), height+100,
                                               width/2+multiplier*(distance), height+100-multiplier*base_length,
                                               width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                               height+100-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))),
                                               width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                            upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
                                               height+100-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
                                                                                  upper_arm_length*math.sin(math.radians(upper_joint_angle))),
                                               fill = "grey", width = 10, joinstyle = ROUND)
        if(type == "forwards"):
            directions = [-30, -15, 0, 15, 30, 0]
            lower_angles = [160, 185, 160, 185, 160, 170]
            upper_angles = [180, 260, 180, 260, 180, 200]
            i = 0
            while(i < len(directions)):
                goal_direction = directions[i]
                goal_lower_joint_angle = lower_angles[i]
                goal_upper_joint_angle = upper_angles[i]
                done = False
                while(not done):
                    done = True
                    if(direction < goal_direction):
                        direction += 1
                        done = False
                    elif(direction > goal_direction):
                        direction -= 1
                        done = False
                    if(lower_joint_angle < goal_lower_joint_angle):
                        lower_joint_angle += 1
                        done = False
                    elif(lower_joint_angle > goal_lower_joint_angle):
                        lower_joint_angle -= 1
                        done = False
                    if(upper_joint_angle < goal_upper_joint_angle):
                    	upper_joint_angle += 1
                    	done = False
                    elif(upper_joint_angle > goal_upper_joint_angle):
                        upper_joint_angle -= 1
                        done = False
                    birds_eye_view.coords(b_line, width/2, base,     
                                                  width/2, base,
                                                  width/2+multiplier*lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction)),
                                                  base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                                  width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
                                                                      upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))),
                                                  base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                   upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))))
                    side_view.coords(s_line, width/2+multiplier*(distance), height,
                                             width/2+multiplier*(distance), height-multiplier*base_length,
                                             width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                             height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))),
                                             width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                          upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
                                             height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
                                                                            upper_arm_length*math.sin(math.radians(upper_joint_angle))))
                    time.sleep(sleep_time)
                    if((width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                     upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))) >= width/2-multiplier*5.3) &
                       (width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                     upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))) <= width/2+multiplier*5.3) &
                       (height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
                                                       upper_arm_length*math.sin(math.radians(upper_joint_angle))) >= height+100-multiplier*xylophone_height)):
                        done = True
                    side_view.update_idletasks()
                    birds_eye_view.update_idletasks()
                time.sleep(1)
                i+=1
        elif(type == "backwards"):
            note = "blue"
            xGoal = 0.0
            yGoal = top+multiplier*11.6/2
            if(note == "blue"):
                xGoal = left+0*(keywidth+division)+keywidth/2
            elif(note == "green"):
            	xGoal = left+1*(keywidth+division)+keywidth/2
            elif(note == "yellow"):
                xGoal = left+2*(keywidth+division)+keywidth/2
            elif(note == "orange"):
                xGoal = left+3*(keywidth+division)+keywidth/2
            elif(note == "red"):
                xGoal = left+4*(keywidth+division)+keywidth/2
            elif(note == "purple"):
                xGoal = left+5*(keywidth+division)+keywidth/2
            elif(note == "white"):
                xGoal = left+6*(keywidth+division)+keywidth/2
            elif(note == "darkblue"):
                xGoal = left+7*(keywidth+division)+keywidth/2
            xLeg = xGoal-width/2
            yLeg = base-yGoal
            goal_direction = int(math.degrees(math.atan2(yLeg, xLeg)))-90
            done = False
            while(not done):
                done = True
                if(direction < goal_direction):
                    direction += 1
		    done = False
                elif(direction > goal_direction):
                    direction -= 1
                    done = False
                birds_eye_view.coords(b_line, width/2, base, 
                                              width/2, base,
                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction)),
                                              base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
                                                                  upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))),
                                              base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                               upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))))
                side_view.coords(s_line, width/2+multiplier*(distance), height,
                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))),
                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                      upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
                                                                        upper_arm_length*math.sin(math.radians(upper_joint_angle))))
                side_view.update_idletasks()
                birds_eye_view.update_idletasks()
                time.sleep(sleep_time)
            completed = False
            x = 0
            y = 0
            while(not completed):
                done = False
                xLeg = (width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))))-(width/2)
                yLeg = (height+100-multiplier*xylophone_height)-(height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))))
                goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg)))+180
                fabrik = side_view.create_line(width/2, height+100-multiplier*xylophone_height, width/2,
                                               height+100-multiplier*xylophone_height, fill="grey", width=10,
                                               joinstyle=ROUND)
                time.sleep(1)
                while(not done):
                    done = True
                    if(upper_joint_angle < goal_upper_joint_angle):
                    	upper_joint_angle += 1
                    	done = False
                    elif(upper_joint_angle > goal_upper_joint_angle):
                    	upper_joint_angle -= 1
                    	done = False
                    side_view.coords(s_line, width/2+multiplier*(distance), height,
                                             width/2+multiplier*(distance), height-multiplier*base_length,
                                             width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                             height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))))
                    endpoint_lower_x = width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction)))
                    endpoint_lower_y = height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle)))
                    endpoint_upper_x = width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                    upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction)))
                    endpoint_upper_y = height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
                                                               upper_arm_length*math.sin(math.radians(upper_joint_angle)))
                    xDifference = endpoint_lower_x-endpoint_upper_x
                    yDifference = endpoint_lower_y-endpoint_upper_y
                    side_view.coords(fabrik, width/2, height+100-multiplier*xylophone_height,
                                             width/2+xDifference, height+100-multiplier*xylophone_height+yDifference)
                    side_view.update_idletasks()
                    birds_eye_view.update_idletasks()
                    time.sleep(sleep_time)
                done = False
                xLeg = (width/2+multiplier*(distance))-(width/2+xDifference)
                yLeg = (height+100-multiplier*xylophone_height+yDifference)-(height-multiplier*base_length)
                goal_lower_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg)))+180
                time.sleep(1)
                while(not done):
                    done = True
                    if(lower_joint_angle < goal_lower_joint_angle):
                    	lower_joint_angle += 1
                    	done = False
                    elif(lower_joint_angle > goal_lower_joint_angle):
                    	lower_joint_angle -= 1
                        done = False
                    side_view.coords(s_line, width/2+multiplier*(distance), height,
                                             width/2+multiplier*(distance), height-multiplier*base_length)
                    endpoint_base_x = width/2+multiplier*(distance)
                    endpoint_base_y = height-multiplier*base_length
                    endpoint_lower_x = width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction)))
                    endpoint_lower_y = height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle)))
                    xDifference2 = endpoint_base_x-endpoint_lower_x
                    yDifference2 = endpoint_base_y-endpoint_lower_y
                    side_view.coords(fabrik, width/2, height+100-multiplier*xylophone_height,
                                             width/2+xDifference, height+100-multiplier*xylophone_height+yDifference,
                                             width/2+xDifference+xDifference2, height+100-multiplier*xylophone_height+yDifference+yDifference2)
                    side_view.update_idletasks()
                    birds_eye_view.update_idletasks()
                    time.sleep(sleep_time)
                done = False
                xLeg = (width/2+multiplier*(distance))-(width/2+xDifference)
                yLeg = (height+100-multiplier*xylophone_height+yDifference)-(height-multiplier*base_length) 
                goal_lower_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg)))+180
                time.sleep(1)
                while(not done):
                    done = True
                    if(lower_joint_angle < goal_lower_joint_angle):
                    	lower_joint_angle += 1
                    	done = False
                    elif(lower_joint_angle > goal_lower_joint_angle):
                    	lower_joint_angle -= 1
                        done = False
                    side_view.coords(s_line, width/2+multiplier*(distance), height,
                                             width/2+multiplier*(distance), height-multiplier*base_length,
                                             width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                             height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))))
                    side_view.coords(fabrik, width/2, height+100-multiplier*xylophone_height,
                                             width/2+xDifference, height+100-multiplier*xylophone_height+yDifference)
                    side_view.update_idletasks()
                    birds_eye_view.update_idletasks()
                    time.sleep(sleep_time)
                done = False
                xLeg = (width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))))-(width/2)
                yLeg = (height+100-multiplier*xylophone_height)-(height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))))  
                goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg)))+180
                time.sleep(1)
                while(not done):
                    done = True
                    if(upper_joint_angle < goal_upper_joint_angle):
                    	upper_joint_angle += 1
                        done = False
                    elif(upper_joint_angle > goal_upper_joint_angle):
                    	upper_joint_angle -= 1
                        done = False
                    side_view.coords(s_line, width/2+multiplier*(distance), height,
                                             width/2+multiplier*(distance), height-multiplier*base_length,
                                             width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
                                             height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))),
                                             width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
                                                                          upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
                                             height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
                                                                            upper_arm_length*math.sin(math.radians(upper_joint_angle))))
                    side_view.coords(fabrik, width/2, height+100-multiplier*xylophone_height,
                                             width/2, height+100-multiplier*xylophone_height)
                    side_view.update_idletasks()
                    birds_eye_view.update_idletasks()
                    time.sleep(sleep_time)
                if(x == goal_lower_joint_angle and y == goal_upper_joint_angle):
                    completed = True
                    print(lower_joint_angle)
                    print(upper_joint_angle)
                x = goal_lower_joint_angle
                y = goal_upper_joint_angle
    def __init__(self, master = None):
            Frame.__init__(self, master)
            self.master = master
            self.master.title("Simulation")
            self.update()
            self.init_window()
def main():
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    app = Window(root)
    root.mainloop()
main()
