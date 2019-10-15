from tkinter import *
import math
import time
import argparse

parser = argparse.ArgumentParser(description = "provide parameters for forwards or backwards kinematics")
parser.add_argument("-t", "--type", help = "specify type using \"forwards\" or \"backwards\"")
parser.add_argument("-d", "--direction", help = "specify the direction")
parser.add_argument("-l", "--lower_joint_angle", help = "specify the lower joint angle")
parser.add_argument("-u", "--upper_joint_angle", help = "specify the upper joint angle")
parser.add_argument("-c", "--colour", help = "colour of the desired note")
args = parser.parse_args()

class Window(Frame):
	def init_window(self):  
		direction = 0
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
		xylophone_height = 10 #check this
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
		base = bottom+multiplier*distance-110.6 #correction term at the end
		b_line = birds_eye_view.create_line(width/2, base, # check base because something does not add up (print stuff)
       	                                            width/2, base,
       	                                            width/2+multiplier*lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction)), 
				        	    base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))),
       	                                            width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
					                                upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))),
       	                                            base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                             upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
       	                                            fill = "grey", width = 5, joinstyle = ROUND)
		s_line = side_view.create_line(width/2+multiplier*(distance), height+100,
       	                                       width/2+multiplier*(distance), height+100-multiplier*base_length,
       	                                       width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))), 
       	                                       height+100-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))),
       	                                       width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                                    upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))),
       	                                       height+100-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
       	                                                                      upper_arm_length*math.sin(math.radians(upper_joint_angle))),
       	                                       fill = "grey", width = 5, joinstyle = ROUND)
		print(top)
		print(base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                             upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))))
		if(args.type == "forwards"):
			goal_direction = int(args.direction)
			goal_lower_joint_angle = int(args.lower_joint_angle)
			goal_upper_joint_angle = int(args.upper_joint_angle)
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
				birds_eye_view.coords(b_line, width/2, base, # check base because something does not add up (print stuff)
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
       	                                                          upper_arm_length*math.sin(math.radians(upper_joint_angle))) >= height-multiplier*xylophone_height)):
					done = True
				side_view.update_idletasks()
				birds_eye_view.update_idletasks()
		elif(args.type == "backwards"):
			note = args.colour
			xGoal = 0.0
			yGoal = top+11.6/2
			if note == "blue":
				xGoal = left+0*(keywidth+division)+keywidth/2
			if note == "green":
				xGoal = left+1*(keywidth+division)+keywidth/2
			if note == "yellow":
				xGoal = left+2*(keywidth+division)+keywidth/2
			if note == "orange":
				xGoal = left+3*(keywidth+division)+keywidth/2
			if note == "red":
				xGoal = left+4*(keywidth+division)+keywidth/2
			if note == "purple":
				xGoal = left+5*(keywidth+division)+keywidth/2
			if note == "white":
				xGoal = left+6*(keywidth+division)+keywidth/2
			if note == "darkblue":
				xGoal = left+7*(keywidth+division)+keywidth/2
			xLeg = xGoal-width/2
			yLeg = base-yGoal
			goal_direction = int(math.degrees(math.atan2(yLeg,xLeg)))-90
			done = False
			while(not done):
				done = True
				if(direction < goal_direction):
					direction += 1	
					done = False
				elif(direction > goal_direction):
					direction -= 1
					done = False
				birds_eye_view.coords(b_line, width/2, base, # check base because something does not add up (print stuff)
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
			fabrik = side_view.create_line(xGoal, yGoal, xGoal, yGoal, fill = "grey", width = 5, joinstyle = ROUND)
			done = False
			xLeg = xGoal-(width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
       	                                                                 upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))))
			yLeg = yGoal-(height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
       	                                                             upper_arm_length*math.sin(math.radians(upper_joint_angle))))
			goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg,xLeg)))
			while(not done):
				done = True
				if(upper_joint_angle < goal_upper_joint_angle):
					upper_joint_angle += 1
					done = False
				elif(upper_joint_angle > goal_upper_joint_angle):
					upper_joint_angle -= 1
					done = False
				birds_eye_view.coords(b_line, width/2, base, # check base because something does not add up (print stuff)
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
       	                                                 height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))))
				side_view.coords(fabrik, xGoal, yGoal, upper_arm_length*math.sin(upper_joint_angle), upper_arm_length*math.cos(upper_joint_angle)) 
				time.sleep(sleep_time)
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
