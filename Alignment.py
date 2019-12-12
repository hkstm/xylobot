import math

#an array containing the note and the arrival time of that note as a 2d array, will need a method to generate this based on what can be retrieved from signal processing
test_array = [[1, 2, 3, 4, 5], [0, 0.7, 1.4, 1.6, 2.6]]

#a method finding the minimum intercal between notes played
def find_interval(note_info):
	array_length = len(note_info[0])
	i = 0
	minimum = 99
	while(i < array_length-1):
		current_interval = note_info[1][i+1]-note_info[1][i]
		if(current_interval < minimum):
			minimum = current_interval 
		i+=1
	return round(minimum, 5)

#a method to align notes based on the interval calculated in findInterval
def align_notes(note_info, interval):
	num_time_stamps = math.ceil(note_info[1][len(note_info[0])-1]/interval)
	time_stamps = [0]*(num_time_stamps+1)
	i = 1
	while(i < len(time_stamps)):
		time_stamps[i] = round((i)*interval, 5)
		i = i+1
	i = 0
	while(i < len(note_info[1])): 
		closest = 999
		current_best_timing = note_info[1][i]
		j = 0
		while(j < len(time_stamps)):
			if(abs(note_info[1][i]-time_stamps[j])  < closest):
				closest = abs(note_info[1][i]-time_stamps[j])
				current_best_timing = time_stamps[j]
			j = j+1
		note_info[1][i] = current_best_timing
		i = i+1
	return note_info	

def full_align(array):
	return align_notes(array, find_interval(array))
#print("Note Info: {}".format(test_array))
#print("Shortest Interval: {}".format(find_interval(test_array)))
#print("Alignment: {}".format(allign_notes(test_array, find_interval(test_array))))
