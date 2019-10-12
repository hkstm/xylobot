from tkinter import *
import math
import time
import argparse

parser = argparse.ArgumentParser(description = "provide parameters for forwards or backwards kinematics")
parser.add_argument("-t", "--type", help = "specify type using \"forwards\" or \"backwards\"")
parser.add_argument("-d", "--direction", help = "specify the direction")
parser.add_argument("-l", "--lower_joint_angle", help = "specify the lower joint angle")
parser.add_argument("-u", "--upper_joint_angle", help = "specify the upper joint angle")
args = parser.parse_args()

class Window(Frame):
	def init_window(self):  
		direction = 0
		goal_direction = int(args.direction)
		lower_joint_angle = 120
		goal_lower_joint_angle = int(args.lower_joint_angle)
		upper_joint_angle = 180
		goal_upper_joint_angle = int(args.upper_joint_angle)
		base_length = 20
		lower_arm_length = 16
		upper_arm_length = 14.5
		distance = 20
		multiplier = 20
		width = self.winfo_screenwidth()
		height = self.winfo_screenheight()/2 
		xylophone_height = 10 #check this
		keywidth = multiplier*2
		birds_eye_view = Canvas(self, width = width, height = height, background = "black")
		side_view = Canvas(self, width = width, height = height, background = "black")
		birds_eye_view.grid(row = 1, column = 0)
		side_view.grid(row = 0, column = 0)
		self.pack(fill=BOTH, expand=1)
		division = multiplier*1 
		top = height/2-multiplier*4.15
		bottom = height/2+multiplier*4.15
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
		side_view.create_rectangle(width/2-multiplier*5.3, height-multiplier*xylophone_height, width/2+multiplier*5.3, height, fill="blue") 
		base = bottom+multiplier*distance
		b_line = birds_eye_view.create_line(width/2, base, 
       	                                            width/2, base,
       	                                            width/2+multiplier*lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction)), 
				                    base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))),
       	                                            width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
				                                        upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
       	                                            base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
       	                                                             upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))),
       	                                            fill = "grey", width = 5, joinstyle = ROUND)
		s_line = side_view.create_line(width/2+multiplier*(distance), height,
       	                                       width/2+multiplier*(distance), height-multiplier*base_length,
       	                                       width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))), 
       	                                       height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))),
       	                                       width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                                    upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
                                               height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
       	                                                                      upper_arm_length*math.sin(math.radians(upper_joint_angle))),
       	                                       fill = "grey", width = 5, joinstyle = ROUND)
		if(args.type == "forwards"):
			done = False		
			sleep_time = 0.05
			while(not done):
				done = True
				if(direction < goal_direction):
					direction += 1	
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
					done = False
					time.sleep(sleep_time)
				if(direction > goal_direction):
					direction -= 1
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
					done = False
				if(lower_joint_angle < goal_lower_joint_angle):
					lower_joint_angle += 1
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
					done = False
				if(lower_joint_angle > goal_lower_joint_angle):
					lower_joint_angle -= 1
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
					done = False
				if(upper_joint_angle < goal_upper_joint_angle):
					upper_joint_angle += 1
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
					done = False
				if(upper_joint_angle > goal_upper_joint_angle):
					upper_joint_angle -= 1
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
					done = False
				if((width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                        upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))) >= width/2-multiplier*5.3) &
                                   (width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                        upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))) <= width/2+multiplier*5.3) &
				   (height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
       	                                                          upper_arm_length*math.sin(math.radians(upper_joint_angle))) >= height-multiplier*xylophone_height)):
					done = True
				side_view.update_idletasks()
				birds_eye_view.update_idletasks()
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
