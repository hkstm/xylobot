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
		base_length = 10
		lower_arm_length = 10
		upper_arm_length = 10
		distance = 10
		multiplier = 10
		width = self.winfo_screenwidth()
		height = self.winfo_screenheight()/2
		birds_eye_view = Canvas(self, width = width, height = height, background = "black")
		side_view = Canvas(self, width = width, height = height, background = "black")
		birds_eye_view.grid(row = 1, column = 0)
		side_view.grid(row = 0, column = 0)
		self.pack(fill=BOTH, expand=1)
		chunks = 12
		horozontal_division = width/120
		top_space = height/10
		bottom_space = height-height/3
		birds_eye_view.create_rectangle(2*width/chunks+horozontal_division, top_space, 3*width/chunks-horozontal_division, bottom_space, fill = "blue")
		birds_eye_view.create_rectangle(3*width/chunks+horozontal_division, top_space, 4*width/chunks-horozontal_division, bottom_space, fill = "green")
		birds_eye_view.create_rectangle(4*width/chunks+horozontal_division, top_space, 5*width/chunks-horozontal_division, bottom_space, fill = "yellow")
		birds_eye_view.create_rectangle(5*width/chunks+horozontal_division, top_space, 6*width/chunks-horozontal_division, bottom_space, fill = "orange")
		birds_eye_view.create_rectangle(6*width/chunks+horozontal_division, top_space, 7*width/chunks-horozontal_division, bottom_space, fill = "red")
		birds_eye_view.create_rectangle(7*width/chunks+horozontal_division, top_space, 8*width/chunks-horozontal_division, bottom_space, fill = "purple")
		birds_eye_view.create_rectangle(8*width/chunks+horozontal_division, top_space, 9*width/chunks-horozontal_division, bottom_space, fill = "white")
		birds_eye_view.create_rectangle(9*width/chunks+horozontal_division, top_space, 10*width/chunks-horozontal_division, bottom_space, fill = "darkblue")
		side_view.create_rectangle(width/3, height-height/10, width/2, height, outline="blue", fill="blue") 
		base = bottom_space+multiplier*distance
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
			sleep_time = 0.01
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
