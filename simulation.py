import math
import time
import itertools
import SimuKey as Simukey
import SimuVector as SimuVector

arm_width = 20
base_length = 18.5
lower_arm_length = 10
upper_arm_length = 10
mallet_length = 5
distance = 20
multiplier = 20
xylophone_height = 10
c = 0.4714
direction = 0
lower_joint_angle = 0
upper_joint_angle = 0
division = multiplier*1
keywidth = multiplier*2



def updateXyloDrawing(xylo,birds_eye_view):
	keys = xylo.getKeys()
	for key in keys:
		color = key.getColor()
		print(color)
		thiskey = birds_eye_view.find_withtag(color)
		pts = key.getPoints()
		# for tuplee in pts:
		# 	for pt in tuplee:
		# 		print(pt)
		#birds_eye_view.coords(thiskey,(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1]),(pts[2][0],pts[2][1]),(pts[3][0],pts[3][1]))
		#np.print(flatten(pts))
		# newpts = flatten(pts)
		# for item in newpts:
		# 	print(item)

		birds_eye_view.coords(thiskey, *flatten(pts))
		#birds_eye_view.coords(thiskey, *newpts)

		print(key.getKeyMidpoint().y)
		print(key.getPoints()[0])
		birds_eye_view.update_idletasks()

		##TODO REMOVE THIS TESTER:
		print(xylo.getKeyLocation( 0, cm = True).x,"  ",xylo.getKeyLocation(0, cm = True).y)
		midpp = xylo.getXyloMidpoint()
		offsets = xylo.getConversions()
		birds_eye_view.create_line(midpp.x, midpp.y, offsets[1],offsets[2])

def flatten(list_of_lists):
	"""Flatten one level of nesting"""
	return itertools.chain.from_iterable(list_of_lists)

def fill_canvas(birds_eye_view, side_view, direction, lower_joint_angle, upper_joint_angle, goal_direction, goal_lower_joint_angle, goal_upper_joint_angle, xylo, seconds):
	sleep_time = seconds/abs(goal_direction-direction)
	width = birds_eye_view.winfo_screenwidth()/3
	height = birds_eye_view.winfo_screenheight()/2
	bottom = height/2+multiplier*5.53
	base = bottom+multiplier*distance-110.6
	left = width/2-multiplier*11-division/2
	s_line = side_view.find_withtag("s_line")
	b_line = birds_eye_view.find_withtag("b_line")
	s_mallet = side_view.find_withtag("s_mallet")
	b_mallet = birds_eye_view.find_withtag("b_mallet")

	keys = xylo.getKeys()
	for key in keys:
		color = key.getColor()
		thiskey = birds_eye_view.find_withtag(color)
		pts = key.getPoints()
		# for tuplee in pts:
		# 	for pt in tuplee:
		# 		print(pt)
		#birds_eye_view.coords(thiskey,(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1]),(pts[2][0],pts[2][1]),(pts[3][0],pts[3][1]))
		birds_eye_view.coords(thiskey,*flatten(pts))




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
		birds_eye_view.coords(b_mallet, width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
		                                                    upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))-
		                                                   (arm_width/(2*multiplier))*math.sin(math.radians(direction-90))),
		                                base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
	                                                         upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))-
		                                                (arm_width/(2*multiplier))*math.cos(math.radians(direction-90))),
		                                width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
		                                                   (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))-
		                                                   (arm_width/(2*multiplier))*math.sin(math.radians(direction-90))),
		                                base+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
		                                                (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))-
		                                                (arm_width/(2*multiplier))*math.cos(math.radians(direction-90))))
		side_view.coords(s_mallet, width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
		                                                        upper_arm_length*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))+
		                                                       (arm_width/(2*multiplier))*math.cos(math.radians(upper_joint_angle-90))),
		                           height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
		                                                          upper_arm_length*math.sin(math.radians(upper_joint_angle))+
		                                                         (arm_width/(2*multiplier))*math.sin(math.radians(upper_joint_angle-90))),
		                           width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
		                                                       (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))+
		                                                       (arm_width/(2*multiplier))*math.cos(math.radians(upper_joint_angle-90))),
		                           height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
		                                                         (upper_arm_length+mallet_length)*math.sin(math.radians(upper_joint_angle))+
		                                                         (arm_width/(2*multiplier))*math.sin(math.radians(upper_joint_angle-90))))
		time.sleep(sleep_time)
		if((width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
		                                (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))+
		                                (arm_width/(2*multiplier))*math.cos(math.radians(upper_joint_angle-90))) >= width/2-multiplier*5.53) &
		   (width/2+multiplier*(distance+lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.cos(math.radians(direction))+
		                                (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.cos(math.radians(direction))+
		                                (arm_width/(2*multiplier))*math.cos(math.radians(upper_joint_angle-90))) <= width/2+multiplier*5.53) &
		   (width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
		                       (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))-
		                       (arm_width/(2*multiplier))*math.sin(math.radians(direction-90))) <= left+7*(keywidth+division)+keywidth) &
		   (width/2+multiplier*(lower_arm_length*math.cos(math.radians(lower_joint_angle))*math.sin(math.radians(direction))+
		                       (upper_arm_length+mallet_length)*math.cos(math.radians(upper_joint_angle))*math.sin(math.radians(direction))-
		                       (arm_width/(2*multiplier))*math.sin(math.radians(direction-90))) >= left+0*(keywidth+division)) &
		   (height-multiplier*(base_length+lower_arm_length*math.sin(math.radians(lower_joint_angle))+
		                                  (upper_arm_length+mallet_length)*math.sin(math.radians(upper_joint_angle))+
		                                  (arm_width/(2*multiplier))*math.sin(math.radians(upper_joint_angle-90))) >= height-multiplier*xylophone_height)):
			done = True
		side_view.update_idletasks()
		birds_eye_view.update_idletasks()
	return(direction, lower_joint_angle, upper_joint_angle)


