import random
import math

# test_sequence = [('E', 0), ('D', 0.25), ('C', 0.5), ('D', 0.75), ('E', 1), ('E', 1.25), ('E', 1.5), ('D', 2.0),
#                 ('D', 2.25), ('D', 2.5), ('E', 3.0), ('G', 3.25), ('G', 3.5), ('E', 4.0), ('D', 4.25), ('C', 4.5),
#                 ('D', 4.75), ('E', 5.0), ('E', 5.25), ('E', 5.5), ('E', 5.75), ('D', 6.0), ('D', 6.25), ('E', 6.5),
#                 ('D', 6.75), ('C', 7.0)]
number_of_notes = 8
transition_frequencies = [[0 for i in range(number_of_notes)] for j in range(number_of_notes)]
transition_probabilities = [[0 for i in range(number_of_notes)] for j in range(number_of_notes)]


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


index_dictionary = {'c6': lambda x: 0,
					'd6': lambda x: 1,
					'e6': lambda x: 2,
					'f6': lambda x: 3,
					'g6': lambda x: 4,
					'a6': lambda x: 5,
					'b6': lambda x: 6,
					'c7': lambda x: 7}

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


def generate_interval(timings):
	rand = random.random()
	probability_counter = timings[0][0]
	for i in range(len(timings)):
		if rand < probability_counter:
			return timings[1][i]
		if i < len(timings) - 1:
			probability_counter = probability_counter + timings[1][i + 1]


def improvise(note, improvisation_length, timings):
	improvised_notes = []
	current_time = generate_interval(timings)
	improvised_notes.append((generate_note(note), current_time))
	for i in range(improvisation_length - 1):
		current_time = current_time + generate_interval(timings)
		improvised_notes.append((generate_note(improvised_notes[i][0]), current_time))
	return improvised_notes


def create_music(sequence, improvisation_length):
	create_transition_matrix(sequence)
	improvised_sequence = improvise(sequence[len(sequence) - 1][0], improvisation_length, generate_timings(sequence))
	print(improvised_sequence)
	return improvised_sequence
