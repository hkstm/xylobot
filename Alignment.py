import math


# test_array = [('a', 0), ('b', 0.7), ('c', 1.4), ('d', 1.6), ('e', 2.6)]

# a method finding the minimum interval between notes played
def find_interval(note_info):
    array_length = len(note_info)
    i = 0
    minimum = 99
    while i < array_length - 1:
        current_interval = note_info[i + 1][1] - note_info[i][1]
        if current_interval < minimum:
            minimum = current_interval
        i += 1
    return round(minimum, 5)


# a method to align notes based on the interval calculated in findInterval
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


def full_align(array):
    return align_notes(array, find_interval(array))

# print("Note Info: {}".format(test_array))
# print("Shortest Interval: {}".format(find_interval(test_array)))
# print("Alignment: {}".format(align_notes(test_array, find_interval(test_array))))
