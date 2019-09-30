from tkinter import *
import math
import time

class Window(Frame):
	direction = 0
	goal_direction = 90
	lower_joint_angle = 90
	goal_lower_joint_angle = 180
	upper_joint_angle = 100
	goal_upper_joint_angle = 150
	def __init__(self, master=None):
		Frame.__init__(self, master)                  
		self.master = master
		self.master.title("Simulation")
		self.update()
		self.init_window()
	def init_window(self):  
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
		base_length = 10
		lower_arm_length = 10
		upper_arm_length = 10
		distance = 10
		multiplier = 10
		base = bottom_space+multiplier*distance
		b_line = birds_eye_view.create_line(width/2, base, 
                                                    width/2, base,
                                                    width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction)), 
				                    base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))),
                                                    width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
				                                        upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                    base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
                                                                     upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                    fill = "grey", width = 5, joinstyle = ROUND)
		s_line = side_view.create_line(width/2+multiplier*(distance), height,
                                               width/2+multiplier*(distance), height-multiplier*base_length,
                                               width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                               height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                               width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                            upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                               height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                              upper_arm_length*math.sin(math.radians(self.upper_joint_angle))),
                                               fill = "grey", width = 5, joinstyle = ROUND)
		done = False		
		sleep_time = 0.01
		while(not done):
			done = True
			if(self.direction < self.goal_direction):
				print("1")
				self.direction += 1	
				birds_eye_view.coords(b_line, width/2, base, 
                                                              width/2, base,
                                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction)), 
				                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))),
                                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
				                                                  upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                               upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))))
				side_view.coords(s_line, width/2+multiplier*(distance), height,
                                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                                      upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                                        upper_arm_length*math.sin(math.radians(self.upper_joint_angle))))
				done = False
				time.sleep(sleep_time)
			if(self.direction > self.goal_direction):
				print("2")
				self.direction -= 1
				birds_eye_view.coords(b_line, width/2, base, 
                                                              width/2, base,
                                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction)), 
				                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))),
                                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
				                                                  upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                               upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))))
				side_view.coords(s_line, width/2+multiplier*(distance), height,
                                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                                      upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                                        upper_arm_length*math.sin(math.radians(self.upper_joint_angle))))
				time.sleep(sleep_time)
				done = False
			if(self.lower_joint_angle < self.goal_lower_joint_angle):
				print("3")
				self.lower_joint_angle += 1
				birds_eye_view.coords(b_line, width/2, base, 
                                                              width/2, base,
                                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction)), 
				                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))),
                                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
				                                                  upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                               upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))))
				side_view.coords(s_line, width/2+multiplier*(distance), height,
                                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                                      upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                                        upper_arm_length*math.sin(math.radians(self.upper_joint_angle))))
				time.sleep(sleep_time)
				done = False
			if(self.lower_joint_angle > self.goal_lower_joint_angle):
				print("4")
				self.lower_joint_angle -= 1
				birds_eye_view.coords(b_line, width/2, base, 
                                                              width/2, base,
                                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction)), 
				                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))),
                                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
				                                                  upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                               upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))))
				side_view.coords(s_line, width/2+multiplier*(distance), height,
                                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                                      upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                                        upper_arm_length*math.sin(math.radians(self.upper_joint_angle))))
				time.sleep(sleep_time)
				done = False
			if(self.upper_joint_angle < self.goal_upper_joint_angle):
				print("5")
				self.upper_joint_angle += 1
				birds_eye_view.coords(b_line, width/2, base, 
                                                              width/2, base,
                                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction)), 
				                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))),
                                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
				                                                  upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                               upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))))
				side_view.coords(s_line, width/2+multiplier*(distance), height,
                                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                                      upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                                        upper_arm_length*math.sin(math.radians(self.upper_joint_angle))))
				time.sleep(sleep_time)
				done = False
			if(self.upper_joint_angle > self.goal_upper_joint_angle):
				print("6")
				self.upper_joint_angle -= 1
				birds_eye_view.coords(b_line, width/2, base, 
                                                              width/2, base,
                                                              width/2+multiplier*lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction)), 
				                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))),
                                                              width/2+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.sin(math.radians(self.direction))+
				                                                  upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.sin(math.radians(self.direction))),
                                                              base+multiplier*(lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                               upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))))
				side_view.coords(s_line, width/2+multiplier*(distance), height,
                                                         width/2+multiplier*(distance), height-multiplier*base_length,
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))), 
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))),
                                                         width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(self.lower_joint_angle))*math.cos(math.radians(self.direction))+
                                                                                      upper_arm_length*math.cos(math.radians(self.upper_joint_angle))*math.cos(math.radians(self.direction))),
                                                         height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(self.lower_joint_angle))+
                                                                                        upper_arm_length*math.sin(math.radians(self.upper_joint_angle))))
				time.sleep(sleep_time)
				done = False
			side_view.update_idletasks()
			birds_eye_view.update_idletasks()

	#add something to ensure modularity in angles below
	def turn(self, degrees):
		self.goal_direction += degrees
	def bend_lower_arm(self, degrees):
		self.goal_lower_arm_angle += degrees
	def bend_middle_arm(self, degrees):
		self.goal_middle_arm_angle += degrees
	def upper_arm_bend(self, degrees):
		self.goal_upper_arm_angle += degrees
	#def redraw():
	#	init_window()

def main():
	root = Tk()
	width = root.winfo_screenwidth()
	height = root.winfo_screenheight()
	root.geometry(f"{width}x{height}")
	app = Window(root)
	#app.turn(100)
	#app.init_window()
	root.mainloop()  

main()
