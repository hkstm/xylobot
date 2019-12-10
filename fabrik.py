from tkinter import *
import math
import time

multiplier = 20
division = multiplier * 1
keywidth = multiplier * 2
mallet_width = 5
distance = 20
lower_arm_length = 10
upper_arm_length = 10
mallet_length = 5
direction = 0
lower_joint_angle = 0
upper_joint_angle = 0
base_length = 18.5
xylophone_height = 10
sleep_time = 0.01
arm_width = 20


def calculate_and_draw(note, birds_eye_view, side_view, direction, lower_joint_angle, upper_joint_angle):
    width = birds_eye_view.winfo_screenwidth() / 3
    height = birds_eye_view.winfo_screenheight() / 2
    top = height / 2 - multiplier * 5.53
    left = width / 2 - multiplier * 11 - division / 2
    bottom = height / 2 + multiplier * 5.53
    base = bottom + multiplier * distance - 110.6
    xGoal = 0.0
    yGoal = top + multiplier * 11.6 / 2
    if (note == "blue"):
        xGoal = left + 0 * (keywidth + division) + keywidth / 2
    elif (note == "green"):
        xGoal = left + 1 * (keywidth + division) + keywidth / 2
    elif (note == "yellow"):
        xGoal = left + 2 * (keywidth + division) + keywidth / 2
    elif (note == "orange"):
        xGoal = left + 3 * (keywidth + division) + keywidth / 2
    elif (note == "red"):
        xGoal = left + 4 * (keywidth + division) + keywidth / 2
    elif (note == "purple"):
        xGoal = left + 5 * (keywidth + division) + keywidth / 2
    elif (note == "white"):
        xGoal = left + 6 * (keywidth + division) + keywidth / 2
    elif (note == "darkblue"):
        xGoal = left + 7 * (keywidth + division) + keywidth / 2
    xLeg = xGoal - width / 2
    yLeg = base - yGoal
    goal_direction = int(math.degrees(math.atan2(yLeg, xLeg))) - 90
    s_line = side_view.find_withtag("s_line")
    b_line = birds_eye_view.find_withtag("b_line")
    s_mallet = side_view.find_withtag("s_mallet")
    b_mallet = birds_eye_view.find_withtag("b_mallet")
    done = False
    while (not done):
        done = True
        if (direction < goal_direction):
            direction += 1
            done = False
        elif (direction > goal_direction):
            direction -= 1
            done = False
        birds_eye_view.coords(b_line, width / 2, base,
                              width / 2, base,
                              width / 2 + multiplier * lower_arm_length * math.cos(
                                  math.radians(lower_joint_angle)) * math.sin(math.radians(direction)),
                              base + multiplier * (
                                          lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                                      math.radians(direction))),
                              width / 2 + multiplier * (
                                          lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.sin(
                                      math.radians(direction)) +
                                          upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.sin(
                                      math.radians(direction))),
                              base + multiplier * (
                                          lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                                      math.radians(direction)) +
                                          upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                                      math.radians(direction))))
        side_view.coords(s_line, width / 2 + multiplier * (distance), height,
                         width / 2 + multiplier * (distance), height - multiplier * base_length,
                         width / 2 + multiplier * (
                                     distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                                 math.radians(direction))),
                         height - multiplier * (
                                     base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))),
                         width / 2 + multiplier * (
                                     distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                                 math.radians(direction)) +
                                     upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                                 math.radians(direction))),
                         height - multiplier * (
                                     base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                                     upper_arm_length * math.sin(math.radians(upper_joint_angle))))
        birds_eye_view.coords(b_mallet, width / 2 + multiplier * (
                    lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.sin(math.radians(direction)) +
                    upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.sin(math.radians(direction)) -
                    (arm_width / (2 * multiplier)) * math.sin(math.radians(direction - 90))),
                              base + multiplier * (
                                          lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                                      math.radians(direction)) +
                                          upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                                      math.radians(direction)) -
                                          (arm_width / (2 * multiplier)) * math.cos(math.radians(direction - 90))),
                              width / 2 + multiplier * (
                                          lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.sin(
                                      math.radians(direction)) +
                                          (upper_arm_length + mallet_length) * math.cos(
                                      math.radians(upper_joint_angle)) * math.sin(math.radians(direction)) -
                                          (arm_width / (2 * multiplier)) * math.sin(math.radians(direction - 90))),
                              base + multiplier * (
                                          lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                                      math.radians(direction)) +
                                          (upper_arm_length + mallet_length) * math.cos(
                                      math.radians(upper_joint_angle)) * math.cos(math.radians(direction)) -
                                          (arm_width / (2 * multiplier)) * math.cos(math.radians(direction - 90))))
        side_view.coords(s_mallet, 0, 0, 0, 0)
        side_view.update_idletasks()
        birds_eye_view.update_idletasks()
        time.sleep(sleep_time)
    completed = False
    x = 0
    y = 0
    while (not completed):
        done = False
        xLeg = (width / 2 + multiplier * (
                    distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                math.radians(direction)))) - (width / 2)
        yLeg = (height - multiplier * xylophone_height) - (
                    height - multiplier * (base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))))
        goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        fabrik = side_view.create_line(width / 2, height - multiplier * xylophone_height, width / 2,
                                       height - multiplier * xylophone_height, fill="green", width=arm_width,
                                       joinstyle=ROUND)
        time.sleep(1)
        while (not done):
            done = True
            if (upper_joint_angle < goal_upper_joint_angle):
                upper_joint_angle += 1
                done = False
            elif (upper_joint_angle > goal_upper_joint_angle):
                upper_joint_angle -= 1
                done = False
            side_view.coords(s_line, width / 2 + multiplier * (distance), height,
                             width / 2 + multiplier * (distance), height - multiplier * base_length,
                             width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                 math.radians(lower_joint_angle)) * math.cos(math.radians(direction))),
                             height - multiplier * (
                                         base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))))
            endpoint_lower_x = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_lower_y = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)))
            endpoint_upper_x_inclusive = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)) +
                        upper_arm_length + mallet_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_upper_y_inclusive = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                        upper_arm_length * math.sin(math.radians(upper_joint_angle)))
            endpoint_upper_x_inclusive = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)) +
                        (upper_arm_length + mallet_length) * math.cos(math.radians(upper_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_upper_y_inclusive = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                        (upper_arm_length + mallet_length) * math.sin(math.radians(upper_joint_angle)))
            endpoint_upper_x = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)) +
                        upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_upper_y = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                        upper_arm_length * math.sin(math.radians(upper_joint_angle)))
            xDifference_inclusive = endpoint_lower_x - endpoint_upper_x_inclusive
            yDifference_inclusive = endpoint_lower_y - endpoint_upper_y_inclusive
            xDifference = endpoint_lower_x - endpoint_upper_x
            yDifference = endpoint_lower_y - endpoint_upper_y
            side_view.coords(fabrik, width / 2, height - multiplier * xylophone_height,
                             width / 2 + xDifference, height - multiplier * xylophone_height + yDifference)
            side_view.update_idletasks()
            birds_eye_view.update_idletasks()
            time.sleep(sleep_time)
        done = False
        xLeg = (width / 2 + multiplier * (distance)) - (width / 2 + xDifference_inclusive)
        yLeg = (height - multiplier * xylophone_height + yDifference_inclusive) - (height - multiplier * base_length)
        goal_lower_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        time.sleep(1)
        while (not done):
            done = True
            if (lower_joint_angle < goal_lower_joint_angle):
                lower_joint_angle += 1
                done = False
            elif (lower_joint_angle > goal_lower_joint_angle):
                lower_joint_angle -= 1
                done = False
            side_view.coords(s_line, width / 2 + multiplier * (distance), height,
                             width / 2 + multiplier * (distance), height - multiplier * base_length)
            endpoint_base_x = width / 2 + multiplier * (distance)
            endpoint_base_y = height - multiplier * base_length
            endpoint_lower_x = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_lower_y = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)))
            xDifference2 = endpoint_base_x - endpoint_lower_x
            yDifference2 = endpoint_base_y - endpoint_lower_y
            side_view.coords(fabrik, width / 2, height - multiplier * xylophone_height,
                             width / 2 + xDifference, height - multiplier * xylophone_height + yDifference,
                             width / 2 + xDifference + xDifference2,
                             height - multiplier * xylophone_height + yDifference + yDifference2)
            side_view.update_idletasks()
            birds_eye_view.update_idletasks()
            time.sleep(sleep_time)
        done = False
        xLeg = (width / 2 + multiplier * (distance)) - (width / 2 + xDifference_inclusive)
        yLeg = (height - multiplier * xylophone_height + yDifference_inclusive) - (height - multiplier * base_length)
        goal_lower_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        time.sleep(1)
        while (not done):
            done = True
            if (lower_joint_angle < goal_lower_joint_angle):
                lower_joint_angle += 1
                done = False
            elif (lower_joint_angle > goal_lower_joint_angle):
                lower_joint_angle -= 1
                done = False
            side_view.coords(s_line, width / 2 + multiplier * (distance), height,
                             width / 2 + multiplier * (distance), height - multiplier * base_length,
                             width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                 math.radians(lower_joint_angle)) * math.cos(math.radians(direction))),
                             height - multiplier * (
                                         base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))))
            side_view.coords(fabrik, width / 2, height - multiplier * xylophone_height,
                             width / 2 + xDifference, height - multiplier * xylophone_height + yDifference)
            side_view.update_idletasks()
            birds_eye_view.update_idletasks()
            time.sleep(sleep_time)
        done = False
        xLeg = (width / 2 + multiplier * (
                    distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                math.radians(direction)))) - (width / 2)
        yLeg = (height - multiplier * xylophone_height) - (
                    height - multiplier * (base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))))
        goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        time.sleep(1)
        while (not done):
            done = True
            if (upper_joint_angle < goal_upper_joint_angle):
                upper_joint_angle += 1
                done = False
            elif (upper_joint_angle > goal_upper_joint_angle):
                upper_joint_angle -= 1
                done = False
            side_view.coords(s_line, width / 2 + multiplier * (distance), height,
                             width / 2 + multiplier * (distance), height - multiplier * base_length,
                             width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                 math.radians(lower_joint_angle)) * math.cos(math.radians(direction))),
                             height - multiplier * (
                                         base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))),
                             width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                 math.radians(lower_joint_angle)) * math.cos(math.radians(direction)) +
                                                       upper_arm_length * math.cos(
                                         math.radians(upper_joint_angle)) * math.cos(math.radians(direction))),
                             height - multiplier * (
                                         base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                                         upper_arm_length * math.sin(math.radians(upper_joint_angle))))
            side_view.coords(fabrik, width / 2, height - multiplier * xylophone_height,
                             width / 2, height - multiplier * xylophone_height)
            side_view.update_idletasks()
            birds_eye_view.update_idletasks()
            time.sleep(sleep_time)
        if (x == goal_lower_joint_angle and y == goal_upper_joint_angle):
            completed = True
        # print("direction: {}".format(direction))
        # print("lower joint angle: {}".format(lower_joint_angle))
        # print("upper joint angle: {}".format(upper_joint_angle))
        x = goal_lower_joint_angle
        y = goal_upper_joint_angle
    fabrik_s_mallet = side_view.create_line(width / 2 + multiplier * (
                distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
            math.radians(direction)) +
                upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(math.radians(direction)) +
                (arm_width / (2 * multiplier)) * math.cos(math.radians(upper_joint_angle - 90))),
                                            height - multiplier * (base_length + lower_arm_length * math.sin(
                                                math.radians(lower_joint_angle)) +
                                                                   upper_arm_length * math.sin(
                                                        math.radians(upper_joint_angle)) +
                                                                   (arm_width / (2 * multiplier)) * math.sin(
                                                        math.radians(upper_joint_angle - 90))),
                                            width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                                math.radians(lower_joint_angle)) * math.cos(math.radians(direction)) +
                                                                      (upper_arm_length + mallet_length) * math.cos(
                                                        math.radians(upper_joint_angle)) * math.cos(
                                                        math.radians(direction)) +
                                                                      (arm_width / (2 * multiplier)) * math.cos(
                                                        math.radians(upper_joint_angle - 90))),
                                            height - multiplier * (base_length + lower_arm_length * math.sin(
                                                math.radians(lower_joint_angle)) +
                                                                   (upper_arm_length + mallet_length) * math.sin(
                                                        math.radians(upper_joint_angle)) +
                                                                   (arm_width / (2 * multiplier)) * math.sin(
                                                        math.radians(upper_joint_angle - 90))),
                                            fill="grey", width=mallet_width, joinstyle=ROUND)
    birds_eye_view.coords(b_line, width / 2, base,
                          width / 2, base,
                          width / 2 + multiplier * lower_arm_length * math.cos(
                              math.radians(lower_joint_angle)) * math.sin(math.radians(direction)),
                          base + multiplier * (lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                              math.radians(direction))),
                          width / 2 + multiplier * (
                                      lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.sin(
                                  math.radians(direction)) +
                                      upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.sin(
                                  math.radians(direction))),
                          base + multiplier * (lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                              math.radians(direction)) +
                                               upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                                      math.radians(direction))))
    birds_eye_view.coords(b_mallet, width / 2 + multiplier * (
                lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.sin(math.radians(direction)) +
                upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.sin(math.radians(direction)) -
                (arm_width / (2 * multiplier)) * math.sin(math.radians(direction - 90))),
                          base + multiplier * (lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                              math.radians(direction)) +
                                               upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                                      math.radians(direction)) -
                                               (arm_width / (2 * multiplier)) * math.cos(math.radians(direction - 90))),
                          width / 2 + multiplier * (
                                      lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.sin(
                                  math.radians(direction)) +
                                      (upper_arm_length + mallet_length) * math.cos(
                                  math.radians(upper_joint_angle)) * math.sin(math.radians(direction)) -
                                      (arm_width / (2 * multiplier)) * math.sin(math.radians(direction - 90))),
                          base + multiplier * (lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                              math.radians(direction)) +
                                               (upper_arm_length + mallet_length) * math.cos(
                                      math.radians(upper_joint_angle)) * math.cos(math.radians(direction)) -
                                               (arm_width / (2 * multiplier)) * math.cos(math.radians(direction - 90))))
    side_view.update_idletasks()
    birds_eye_view.update_idletasks()
    time.sleep(sleep_time)
    return ([direction, lower_joint_angle, upper_joint_angle])


def calculate(note, birds_eye_view, direction, lower_joint_angle, upper_joint_angle):
    width = birds_eye_view.winfo_screenwidth() / 3
    height = birds_eye_view.winfo_screenheight() / 2
    top = height / 2 - multiplier * 5.53
    left = width / 2 - multiplier * 11 - division / 2
    bottom = height / 2 + multiplier * 5.53
    base = bottom + multiplier * distance - 110.6
    xGoal = 0.0
    yGoal = top + multiplier * 11.6 / 2
    if (note == "blue"):
        xGoal = left + 0 * (keywidth + division) + keywidth / 2
    elif (note == "green"):
        xGoal = left + 1 * (keywidth + division) + keywidth / 2
    elif (note == "yellow"):
        xGoal = left + 2 * (keywidth + division) + keywidth / 2
    elif (note == "orange"):
        xGoal = left + 3 * (keywidth + division) + keywidth / 2
    elif (note == "red"):
        xGoal = left + 4 * (keywidth + division) + keywidth / 2
    elif (note == "purple"):
        xGoal = left + 5 * (keywidth + division) + keywidth / 2
    elif (note == "white"):
        xGoal = left + 6 * (keywidth + division) + keywidth / 2
    elif (note == "darkblue"):
        xGoal = left + 7 * (keywidth + division) + keywidth / 2
    xLeg = xGoal - width / 2
    yLeg = base - yGoal
    goal_direction = int(math.degrees(math.atan2(yLeg, xLeg))) - 90
    done = False
    while (not done):
        done = True
        if (direction < goal_direction):
            direction += 1
            done = False
        elif (direction > goal_direction):
            direction -= 1
            done = False
    completed = False
    x = 0
    y = 0
    while (not completed):
        done = False
        xLeg = (width / 2 + multiplier * (
                    distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                math.radians(direction)))) - (width / 2)
        yLeg = (height - multiplier * xylophone_height) - (
                    height - multiplier * (base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))))
        goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        while (not done):
            done = True
            if (upper_joint_angle < goal_upper_joint_angle):
                upper_joint_angle += 1
                done = False
            elif (upper_joint_angle > goal_upper_joint_angle):
                upper_joint_angle -= 1
                done = False
            endpoint_lower_x = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_lower_y = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)))
            endpoint_upper_x_inclusive = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)) +
                        upper_arm_length + mallet_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_upper_y_inclusive = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                        upper_arm_length * math.sin(math.radians(upper_joint_angle)))
            endpoint_upper_x_inclusive = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)) +
                        (upper_arm_length + mallet_length) * math.cos(math.radians(upper_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_upper_y_inclusive = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                        (upper_arm_length + mallet_length) * math.sin(math.radians(upper_joint_angle)))
            endpoint_upper_x = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)) +
                        upper_arm_length * math.cos(math.radians(upper_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_upper_y = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)) +
                        upper_arm_length * math.sin(math.radians(upper_joint_angle)))
            xDifference_inclusive = endpoint_lower_x - endpoint_upper_x_inclusive
            yDifference_inclusive = endpoint_lower_y - endpoint_upper_y_inclusive
            xDifference = endpoint_lower_x - endpoint_upper_x
            yDifference = endpoint_lower_y - endpoint_upper_y
        done = False
        xLeg = (width / 2 + multiplier * (distance)) - (width / 2 + xDifference_inclusive)
        yLeg = (height - multiplier * xylophone_height + yDifference_inclusive) - (height - multiplier * base_length)
        goal_lower_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        time.sleep(1)
        while (not done):
            done = True
            if (lower_joint_angle < goal_lower_joint_angle):
                lower_joint_angle += 1
                done = False
            elif (lower_joint_angle > goal_lower_joint_angle):
                lower_joint_angle -= 1
                done = False
            endpoint_base_x = width / 2 + multiplier * (distance)
            endpoint_base_y = height - multiplier * base_length
            endpoint_lower_x = width / 2 + multiplier * (
                        distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                    math.radians(direction)))
            endpoint_lower_y = height - multiplier * (
                        base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle)))
            xDifference2 = endpoint_base_x - endpoint_lower_x
            yDifference2 = endpoint_base_y - endpoint_lower_y
        done = False
        xLeg = (width / 2 + multiplier * (distance)) - (width / 2 + xDifference_inclusive)
        yLeg = (height - multiplier * xylophone_height + yDifference_inclusive) - (height - multiplier * base_length)
        goal_lower_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        time.sleep(1)
        while (not done):
            done = True
            if (lower_joint_angle < goal_lower_joint_angle):
                lower_joint_angle += 1
                done = False
            elif (lower_joint_angle > goal_lower_joint_angle):
                lower_joint_angle -= 1
                done = False
        done = False
        xLeg = (width / 2 + multiplier * (
                    distance + lower_arm_length * math.cos(math.radians(lower_joint_angle)) * math.cos(
                math.radians(direction)))) - (width / 2)
        yLeg = (height - multiplier * xylophone_height) - (
                    height - multiplier * (base_length + lower_arm_length * math.sin(math.radians(lower_joint_angle))))
        goal_upper_joint_angle = int(math.degrees(math.atan2(yLeg, xLeg))) + 180
        time.sleep(1)
        while (not done):
            done = True
            if (upper_joint_angle < goal_upper_joint_angle):
                upper_joint_angle += 1
                done = False
            elif (upper_joint_angle > goal_upper_joint_angle):
                upper_joint_angle -= 1
                done = False
        if (x == goal_lower_joint_angle and y == goal_upper_joint_angle):
            completed = True
        # print("direction: {}".format(direction))
        # print("lower joint angle: {}".format(lower_joint_angle))
        # print("upper joint angle: {}".format(upper_joint_angle))
        x = goal_lower_joint_angle
        y = goal_upper_joint_angle
    return ([direction, lower_joint_angle, upper_joint_angle])
