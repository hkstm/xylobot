import random
import math

#initializing matricies for use with Markov chain
number_of_notes = 8
transition_frequencies = [[0 for i in range(number_of_notes)] for j in range(number_of_notes)]
transition_probabilities = [[0 for i in range(number_of_notes)] for j in range(number_of_notes)]

#Methods to be called from dictionary for updating Marvok chain transition matrix
def lowc_to_lowc():
	transition_frequencies[0][0] = transition_frequencies[0][0] + 1
def d_to_lowc():
	transition_frequencies[1][0] = transition_frequencies[1][0] + 1
def e_to_lowc():
	transition_frequencies[2][0] = transition_frequencies[2][0] + 1
def f_to_lowc():
	transition_frequencies[3][0] = transition_frequencies[3][0] + 1
def g_to_lowc():
	transition_frequencies[4][0] = transition_frequencies[4][0] + 1
def a_to_lowc():
	transition_frequencies[5][0] = transition_frequencies[5][0] + 1
def b_to_lowc():
	transition_frequencies[6][0] = transition_frequencies[6][0] + 1
def highc_to_lowc():
	transition_frequencies[7][0] = transition_frequencies[7][0] + 1
def lowc_to_d():
	transition_frequencies[0][1] = transition_frequencies[0][1] + 1
def d_to_d():
	transition_frequencies[1][1] = transition_frequencies[1][1] + 1
def e_to_d():
	transition_frequencies[2][1] = transition_frequencies[2][1] + 1
def f_to_d():
	transition_frequencies[3][1] = transition_frequencies[3][1] + 1
def g_to_d():
	transition_frequencies[4][1] = transition_frequencies[4][1] + 1
def a_to_d():
	transition_frequencies[5][1] = transition_frequencies[5][1] + 1
def b_to_d():
	transition_frequencies[6][1] = transition_frequencies[6][1] + 1
def highc_to_d():
	transition_frequencies[7][1] = transition_frequencies[7][1] + 1
def lowc_to_e():
	transition_frequencies[0][2] = transition_frequencies[0][2] + 1
def d_to_e():
	transition_frequencies[1][2] = transition_frequencies[1][2] + 1
def e_to_e():
	transition_frequencies[2][2] = transition_frequencies[2][2] + 1
def f_to_e():
	transition_frequencies[3][2] = transition_frequencies[3][2] + 1
def g_to_e():
	transition_frequencies[4][2] = transition_frequencies[4][2] + 1
def a_to_e():
	transition_frequencies[5][2] = transition_frequencies[5][2] + 1
def b_to_e():
	transition_frequencies[6][2] = transition_frequencies[6][2] + 1
def highc_to_e():
	transition_frequencies[7][2] = transition_frequencies[7][2] + 1
def lowc_to_f():
	transition_frequencies[0][3] = transition_frequencies[0][3] + 1
def d_to_f():
	transition_frequencies[1][3] = transition_frequencies[1][3] + 1
def e_to_f():
	transition_frequencies[2][3] = transition_frequencies[2][3] + 1
def f_to_f():
	transition_frequencies[3][3] = transition_frequencies[3][3] + 1
def g_to_f():
	transition_frequencies[4][3] = transition_frequencies[4][3] + 1
def a_to_f():
	transition_frequencies[5][3] = transition_frequencies[5][3] + 1
def b_to_f():
	transition_frequencies[6][3] = transition_frequencies[6][3] + 1
def highc_to_f():
	transition_frequencies[7][3] = transition_frequencies[7][3] + 1
def lowc_to_g():
	transition_frequencies[0][4] = transition_frequencies[0][4] + 1
def d_to_g():
	transition_frequencies[1][4] = transition_frequencies[1][4] + 1
def e_to_g():
	transition_frequencies[2][4] = transition_frequencies[2][4] + 1
def f_to_g():
	transition_frequencies[3][4] = transition_frequencies[3][4] + 1
def g_to_g():
	transition_frequencies[4][4] = transition_frequencies[4][4] + 1
def a_to_g():
	transition_frequencies[5][4] = transition_frequencies[5][4] + 1
def b_to_g():
	transition_frequencies[6][4] = transition_frequencies[6][4] + 1
def highc_to_g():
	transition_frequencies[7][4] = transition_frequencies[7][4] + 1
def lowc_to_a():
	transition_frequencies[0][5] = transition_frequencies[0][5] + 1
def d_to_a():
	transition_frequencies[1][5] = transition_frequencies[1][5] + 1
def e_to_a():
	transition_frequencies[2][5] = transition_frequencies[2][5] + 1
def f_to_a():
	transition_frequencies[3][5] = transition_frequencies[3][5] + 1
def g_to_a():
	transition_frequencies[4][5] = transition_frequencies[4][5] + 1
def a_to_a():
	transition_frequencies[5][5] = transition_frequencies[5][5] + 1
def b_to_a():
	transition_frequencies[6][5] = transition_frequencies[6][5] + 1
def highc_to_a():
	transition_frequencies[7][5] = transition_frequencies[7][5] + 1
def lowc_to_b():
	transition_frequencies[0][6] = transition_frequencies[0][6] + 1
def d_to_b():
	transition_frequencies[1][6] = transition_frequencies[1][6] + 1
def e_to_b():
	transition_frequencies[2][6] = transition_frequencies[2][6] + 1
def f_to_b():
	transition_frequencies[3][6] = transition_frequencies[3][6] + 1
def g_to_b():
	transition_frequencies[4][6] = transition_frequencies[4][6] + 1
def a_to_b():
	transition_frequencies[5][6] = transition_frequencies[5][6] + 1
def b_to_b():
	transition_frequencies[6][6] = transition_frequencies[6][6] + 1
def highc_to_b():
	transition_frequencies[7][6] = transition_frequencies[7][6] + 1
def lowc_to_highc():
	transition_frequencies[0][7] = transition_frequencies[0][7] + 1
def d_to_highc():
	transition_frequencies[1][7] = transition_frequencies[1][7] + 1
def e_to_highc():
	transition_frequencies[2][7] = transition_frequencies[2][7] + 1
def f_to_highc():
	transition_frequencies[3][7] = transition_frequencies[3][7] + 1
def g_to_highc():
	transition_frequencies[4][7] = transition_frequencies[4][7] + 1
def a_to_highc():
	transition_frequencies[5][7] = transition_frequencies[5][7] + 1
def b_to_highc():
	transition_frequencies[6][7] = transition_frequencies[6][7] + 1
def highc_to_highc():
	transition_frequencies[7][7] = transition_frequencies[7][7] + 1

#dictionary used to generating index for the transition matrix
index_dictionary = {'c6': lambda x: 0,
					'd6': lambda x: 1,
					'e6': lambda x: 2,
					'f6': lambda x: 3,
					'g6': lambda x: 4,
					'a6': lambda x: 5,
					'b6': lambda x: 6,
					'c7': lambda x: 7}

#dictionary used for updating transition matrix based on input sequence
key_dictionary = {
	'c6': {'c6': lowc_to_lowc, 'd6': d_to_lowc, 'e6': e_to_lowc, 'f6': f_to_lowc, 'g6': g_to_lowc, 'a6': a_to_lowc,
		   'b6': b_to_lowc, 'c7': highc_to_lowc},
	'd6': {'c6': lowc_to_d, 'd6': d_to_d, 'e6': e_to_d, 'f6': f_to_d, 'g6': g_to_d, 'e6': a_to_d, 'f6': b_to_d,
		   'c7': highc_to_d},
	'e6': {'c6': lowc_to_e, 'd6': d_to_e, 'e6': e_to_e, 'f6': f_to_e, 'g6': g_to_e, 'a6': a_to_e, 'b6': b_to_e,
		   'c7': highc_to_e},
	'f6': {'c6': lowc_to_f, 'd6': d_to_f, 'e6': e_to_f, 'f6': f_to_f, 'g6': g_to_f, 'a6': a_to_f, 'b6': b_to_f,
		   'c7': highc_to_f},
	'g6': {'c6': lowc_to_g, 'd6': d_to_g, 'e6': e_to_g, 'f6': f_to_g, 'g6': g_to_g, 'a6': a_to_g, 'b6': b_to_g,
		   'c7': highc_to_g},
	'a6': {'c6': lowc_to_a, 'd6': d_to_a, 'e6': e_to_a, 'f6': f_to_a, 'g6': g_to_a, 'a6': a_to_a, 'b6': b_to_a,
		   'c7': highc_to_a},
	'b6': {'c6': lowc_to_b, 'd6': d_to_b, 'e6': e_to_b, 'f6': f_to_b, 'g6': g_to_b, 'a6': a_to_b, 'b6': b_to_b,
		   'c7': highc_to_b},
	'c7': {'c6': lowc_to_highc, 'd6': d_to_highc, 'e6': e_to_highc, 'f6': f_to_highc, 'g6': g_to_highc,
		   'a6': a_to_highc, 'b6': b_to_highc, 'c7': highc_to_highc}}

#creates the transition matrix for the markov model
def create_transition_matrix(sequence):
	for i in range(len(sequence) - 1):
		key_dictionary[sequence[i][0]][sequence[i + 1][0]]()
	column_totals = [0 for i in range(number_of_notes)]
	for i in range(len(transition_frequencies)):
		total = 0
		for j in range(len(transition_frequencies[i])):
			total = total + transition_frequencies[j][i]
		column_totals[i] = total
	for i in range(number_of_notes):
		column_total = column_totals[i]
		for j in range(number_of_notes):
			transition_probabilities[i][j] = (transition_frequencies[j][i] + 1) / (column_total + number_of_notes)
	print("matrix")
	print(transition_probabilities)

#generates one note based on the previous note played by consulting the index dictionary and then transition matrix
def generate_note(previous_note):
	index = index_dictionary[previous_note](None)
	rand = random.random()
	probability_counter = transition_probabilities[index][0]
	if rand < probability_counter:
		return 'c6'
	probability_counter = probability_counter + transition_probabilities[index][1]
	if rand < probability_counter:
		return 'd6'
	probability_counter = probability_counter + transition_probabilities[index][2]
	if rand < probability_counter:
		return 'e6'
	probability_counter = probability_counter + transition_probabilities[index][3]
	if rand < probability_counter:
		return 'f6'
	probability_counter = probability_counter + transition_probabilities[index][4]
	if rand < probability_counter:
		return 'g6'
	probability_counter = probability_counter + transition_probabilities[index][5]
	if rand < probability_counter:
		return 'a6'
	probability_counter = probability_counter + transition_probabilities[index][6]
	if rand < probability_counter:
		return 'b6'
	else:
		return 'c7'

#finds the shortest interval between two consecutive notes in the input sequence
def find_shortest_interval(note_info):
	array_length = len(note_info)
	i = 0
	minimum = 99
	while i < array_length - 1:
		current_interval = note_info[i + 1][1] - note_info[i][1]
		if current_interval < minimum:
			minimum = current_interval
		i += 1
	return round(minimum, 5)

#finds the longest interval between two consecutive in the input sequence
def find_longest_interval(note_info):
	array_length = len(note_info)
	i = 0
	maximum = 0
	while i < array_length - 1:
		current_interval = note_info[i + 1][1] - note_info[i][1]
		if current_interval > maximum:
			maximum = current_interval
		i += 1
	return round(maximum, 5)

#quantizes the notes so that they fit onto a discrete timeline
def align_notes(note_info_tuples, interval):
	note_info = []
	for i in range(len(note_info_tuples)):
		temp_tuple = note_info_tuples[i]
		temp_list = list(temp_tuple)
		note_info.append(temp_list)
	num_time_stamps = math.ceil(note_info[len(note_info[0]) - 1][1] / interval)
	time_stamps = [0] * (num_time_stamps + 1)
	i = 1
	while i < len(time_stamps):
		time_stamps[i] = round((i) * interval, 5)
		i = i + 1
	i = 0
	while i < len(note_info[1]):
		closest = 999
		current_best_timing = note_info[i][1]
		j = 0
		while j < len(time_stamps):
			if abs(note_info[i][1] - time_stamps[j]) < closest:
				closest = abs(note_info[i][1] - time_stamps[j])
				current_best_timing = time_stamps[j]
			j = j + 1
		note_info[i][1] = current_best_timing
		i = i + 1
	formatted_note_info = []
	for i in range(len(note_info)):
		temp_list = note_info[i]
		temp_tuple = tuple(temp_list)
		formatted_note_info.append(temp_tuple)
	return formatted_note_info

#calculates the probability of time delays occuring in the improvised sequence based on time delays in the input sequence
def generate_timings(sequence):
	aligned_sequence = align_notes(sequence, find_shortest_interval(sequence))
	shortest_interval = find_shortest_interval(aligned_sequence)
	longest_interval = find_longest_interval(aligned_sequence)
	number_of_timings = int(longest_interval / shortest_interval)
	time_values = [0 for i in range(number_of_timings)]
	time_frequencies = [0 for i in range(number_of_timings)]
	time_values[0] = shortest_interval
	time_values[len(time_values) - 1] = longest_interval
	i = 1
	while i < number_of_timings - 1:
		time_values[i] = time_values[i - 1] + shortest_interval
		i = i + 1
	for j in range(len(aligned_sequence) - 1):
		for k in range(len(time_values)):
			if ((aligned_sequence[j + 1][1] - aligned_sequence[j][1] >= time_values[k] - (shortest_interval / 2)) & (
					aligned_sequence[j + 1][1] - aligned_sequence[j][1] <= time_values[k] + (
					shortest_interval / 2))):  # problem with this equality check!! (check within a range and then make a check foe when total is zero)
				time_frequencies[k] = time_frequencies[k] + 1
	raw_probabilities = [0 for j in range(len(time_frequencies))]
	ptotal = 0
	for j in time_frequencies:
		ptotal = ptotal + j
	for j in range(len(raw_probabilities)):
		raw_probabilities[j] = time_frequencies[j] / ptotal
	return raw_probabilities, time_values

#increases the probability of transitions between notes pairs in the transition matrix if those note pairs do not occur
#in the input sequence
def adjust(probabilities, frequencies, severity):
	for i in range(len(probabilities)):
		zero_counter = 0
		for j in range(len(probabilities[i])):
			if frequencies[i][j] == 0:
				zero_counter = zero_counter+1
		if zero_counter != len(probabilities):
			for j in range(len(probabilities[i])):
				if frequencies[i][j] == 0:
					probabilities[i][j] = probabilities[i][j]+severity
			decrease_by = (zero_counter*severity)/(len(probabilities)-zero_counter)
			for j in range(len(probabilities[i])):
				if frequencies[i][j] != 0:
					probabilities[i][j] = probabilities[i][j]-decrease_by
	for i in range(len(transition_probabilities)):
		for j in range(len(transition_probabilities[i])):
			transition_probabilities[i][j] = probabilities[i][j]

#calculates the similarity score between two melodies in the same key
def calculate_score(s1, s2):
	multiplier = len(s1)*len(s2)
	modified_s1 = translate(s1)
	modified_s2 = translate(s2)
	score = 0
	num_in_scale_1 = 0
	num_in_scale_2 = 0
	for i in modified_s1:
		if i == 1 | i == 5 | i == 8 | i == 13:
			num_in_scale_1 = num_in_scale_1+1
	for i in modified_s2:
		if i == 1 | i == 5 | i == 8 | i == 13:
			num_in_scale_2 = num_in_scale_2+1
	score = score-(multiplier*(abs(num_in_scale_1-num_in_scale_2)))
	for i in modified_s1:
		for j in modified_s2:
			score = score+(j-i)
	return score

#converts each element in a note sequence into a number equivelant for greater ease in calculate_score
def translate(s):
	number_equivalent = [0]*len(s)
	for i in range(len(s)):
		if s[i][0] == 'c6':
			number_equivalent[i] = 1
		elif s[i][0] == 'd6':
			number_equivalent[i] = 3
		elif s[i][0] == 'e6':
			number_equivalent[i] = 5
		elif s[i][0] == 'f6':
			number_equivalent[i] = 6
		elif s[i][0] == 'g6':
			number_equivalent[i] = 8
		elif s[i][0] == 'a6':
			number_equivalent[i] = 10
		elif s[i][0] == 'b6':
			number_equivalent[i] = 12
		elif s[i][0] == 'c7':
			number_equivalent[i] = 13
	return number_equivalent

#generates an interval between two notes in the improvised sequence based on the probability matrix
def generate_interval(timings):
	rand = random.random()
	probability_counter = timings[0][0]
	for i in range(len(timings)):
		if rand < probability_counter:
			return timings[1][i]
		if i < len(timings) - 1:
			probability_counter = probability_counter + timings[1][i + 1]
	#return[1][0] #in case of recording errors casued by a noisy environment

#creates an improvised sequence of specified length based on an input sequence
def improvise(note, improvisation_length, timings):
	improvised_notes = []
	current_time = generate_interval(timings)
	improvised_notes.append((generate_note(note), current_time))
	print(transition_probabilities)
	for i in range(improvisation_length - 1):
		current_time = current_time + generate_interval(timings)
		improvised_notes.append((generate_note(improvised_notes[i][0]), current_time))
	print("improised notes")
	print(improvised_notes)
	return improvised_notes

#appends the entire sequence to the end of the sequence to make it repeat twice to improve the transition probabilities
def double_sequence(sequence):
	new_sequence = []
	for i in range(len(sequence)):
		new_sequence.append(sequence[i])
	for i in range(len(sequence)):
		new_sequence.append((sequence[i][0], sequence[len(sequence)-1][1]+sequence[i][1]))
	return new_sequence

#calculates the similarity between two sequences after altering the probability by a severity factor to increase the
#number of rare note pairs appearing
def calculate_similarity(sequence, improvisation_length, severity):
	create_transition_matrix(sequence)
	adjust(transition_probabilities, transition_frequencies, severity)
	adjusted_improvised_sequence = improvise(sequence[len(sequence)-1][0], improvisation_length, generate_timings(sequence))
	score = calculate_score(sequence, adjusted_improvised_sequence)
	return score

#called by another class to return an improvised sequence
def create_music(sequence, improvisation_length):
	sequence = double_sequence(double_sequence(double_sequence(double_sequence(sequence))))
	create_transition_matrix(sequence)
	improvised_sequence = improvise(sequence[len(sequence) - 1][0], improvisation_length, generate_timings(sequence))
	return improvised_sequence
