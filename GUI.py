import os
import ast
from functools import partial
from tkinter.filedialog import askopenfilename
from types import SimpleNamespace

import pyaudio
import wave
import matplotlib.pyplot as plt
import datetime
from tkinter import *
from simulation import fill_canvas
from fabrik import calculate
from fabrik import calculate_and_draw
import math
from tkinter import *

import PIL.Image
import PIL.ImageTk
import cv2

from Note import Note
from signalprocessing.custompitchtracking import pitch_track


class XylobotGUI:

    def init_window(self):
        arm_width = 20
        mallet_width = 5
        self.direction = 0
        self.lower_joint_angle = 160
        self.upper_joint_angle = 210
        base_length = 18.5
        lower_arm_length = 10
        upper_arm_length = 10
        mallet_length = 5
        distance = 20
        multiplier = 20
        width = self.canvaswidth
        height = self.canvasheight
        xylophone_height = 10
        keywidth = multiplier * 2
        self.birds_eye_view = Canvas(self.window, width=width, height=height, background="black")
        self.side_view = Canvas(self.window, width=width, height=height, background="black")
        # self.birds_eye_view.grid(row=0, column=0)
        # self.side_view.grid(row=0, column=1)
        # self.pack(fill=BOTH, expand=1)
        division = multiplier * 1
        top = height / 2 - multiplier * 5.53
        bottom = height / 2 + multiplier * 5.53
        left = width / 2 - multiplier * 11 - division / 2
        c = 0.4714
        self.birds_eye_view.create_rectangle(left + 0 * (keywidth + division), top + 0 * c,
                                        left + 0 * (keywidth + division) + keywidth, bottom - 0 * c, fill="blue")
        self.birds_eye_view.create_rectangle(left + 1 * (keywidth + division), top + 1 * c,
                                        left + 1 * (keywidth + division) + keywidth, bottom - 1 * c, fill="green")
        self.birds_eye_view.create_rectangle(left + 2 * (keywidth + division), top + 2 * c,
                                        left + 2 * (keywidth + division) + keywidth, bottom - 2 * c, fill="yellow")
        self.birds_eye_view.create_rectangle(left + 3 * (keywidth + division), top + 3 * c,
                                        left + 3 * (keywidth + division) + keywidth, bottom - 3 * c, fill="orange")
        self.birds_eye_view.create_rectangle(left + 4 * (keywidth + division), top + 4 * c,
                                        left + 4 * (keywidth + division) + keywidth, bottom - 4 * c, fill="red")
        self.birds_eye_view.create_rectangle(left + 5 * (keywidth + division), top + 5 * c,
                                        left + 5 * (keywidth + division) + keywidth, bottom - 5 * c, fill="purple")
        self.birds_eye_view.create_rectangle(left + 6 * (keywidth + division), top + 6 * c,
                                        left + 6 * (keywidth + division) + keywidth, bottom - 6 * c, fill="white")
        self.birds_eye_view.create_rectangle(left + 7 * (keywidth + division), top + 7 * c,
                                        left + 7 * (keywidth + division) + keywidth, bottom - 7 * c, fill="darkblue")
        self.side_view.create_rectangle(width / 2 - multiplier * 5.53, height - multiplier * xylophone_height,
                                   width / 2 + multiplier * 5.53, height, fill="blue")
        base = bottom + multiplier * distance - 110.6
        b_line = self.birds_eye_view.create_line(width / 2, base,
                                            width / 2, base,
                                            width / 2 + multiplier * lower_arm_length * math.cos(
                                                math.radians(self.lower_joint_angle)) * math.sin(math.radians(self.direction)),
                                            base + multiplier * (lower_arm_length * math.cos(
                                                math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction))),
                                            width / 2 + multiplier * (lower_arm_length * math.cos(
                                                math.radians(self.lower_joint_angle)) * math.sin(math.radians(self.direction)) +
                                                                      upper_arm_length * math.cos(
                                                        math.radians(self.upper_joint_angle)) * math.sin(
                                                        math.radians(self.direction))),
                                            base + multiplier * (lower_arm_length * math.cos(
                                                math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction)) +
                                                                 upper_arm_length * math.cos(
                                                        math.radians(self.upper_joint_angle)) * math.cos(
                                                        math.radians(self.direction))),
                                            fill="grey", width=arm_width, joinstyle=ROUND, tags="b_line")
        s_line = self.side_view.create_line(width / 2 + multiplier * (distance), height,
                                       width / 2 + multiplier * (distance), height - multiplier * base_length,
                                       width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                           math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction))),
                                       height - multiplier * (base_length + lower_arm_length * math.sin(
                                           math.radians(self.lower_joint_angle))),
                                       width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                           math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction)) +
                                                                 upper_arm_length * math.cos(
                                                   math.radians(self.upper_joint_angle)) * math.cos(
                                                   math.radians(self.direction))),
                                       height - multiplier * (base_length + lower_arm_length * math.sin(
                                           math.radians(self.lower_joint_angle)) +
                                                              upper_arm_length * math.sin(
                                                   math.radians(self.upper_joint_angle))),
                                       fill="grey", width=arm_width, joinstyle=ROUND, tags="s_line")
        b_mallet = self.birds_eye_view.create_line(width / 2 + multiplier * (
                lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.sin(math.radians(self.direction)) +
                upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.sin(math.radians(self.direction)) +
                (arm_width / (2 * multiplier)) * math.cos(math.radians(self.upper_joint_angle - 90))),
                                              base + multiplier * (lower_arm_length * math.cos(
                                                  math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction)) +
                                                                   upper_arm_length * math.cos(
                                                          math.radians(self.upper_joint_angle)) * math.cos(
                                                          math.radians(self.direction)) +
                                                                   (arm_width / (2 * multiplier)) * math.sin(
                                                          math.radians(self.upper_joint_angle - 90))),
                                              width / 2 + multiplier * (lower_arm_length * math.cos(
                                                  math.radians(self.lower_joint_angle)) * math.sin(math.radians(self.direction)) +
                                                                        (upper_arm_length + mallet_length) * math.cos(
                                                          math.radians(self.upper_joint_angle)) * math.sin(
                                                          math.radians(self.direction)) +
                                                                        (arm_width / (2 * multiplier)) * math.cos(
                                                          math.radians(self.upper_joint_angle - 90))),
                                              base + multiplier * (lower_arm_length * math.cos(
                                                  math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction)) +
                                                                   (upper_arm_length + mallet_length) * math.cos(
                                                          math.radians(self.upper_joint_angle)) * math.cos(
                                                          math.radians(self.direction)) +
                                                                   (arm_width / (2 * multiplier)) * math.sin(
                                                          math.radians(self.upper_joint_angle - 90))),
                                              fill="grey", width=mallet_width, joinstyle=ROUND, tags="b_mallet")
        s_mallet = self.side_view.create_line(width / 2 + multiplier * (
                distance + lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.cos(
            math.radians(self.direction)) +
                upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.cos(math.radians(self.direction)) +
                (arm_width / (2 * multiplier)) * math.cos(math.radians(self.upper_joint_angle - 90))),
                                         height - multiplier * (base_length + lower_arm_length * math.sin(
                                             math.radians(self.lower_joint_angle)) +
                                                                upper_arm_length * math.sin(
                                                     math.radians(self.upper_joint_angle)) +
                                                                (arm_width / (2 * multiplier)) * math.sin(
                                                     math.radians(self.upper_joint_angle - 90))),
                                         width / 2 + multiplier * (distance + lower_arm_length * math.cos(
                                             math.radians(self.lower_joint_angle)) * math.cos(math.radians(self.direction)) +
                                                                   (upper_arm_length + mallet_length) * math.cos(
                                                     math.radians(self.upper_joint_angle)) * math.cos(
                                                     math.radians(self.direction)) +
                                                                   (arm_width / (2 * multiplier)) * math.cos(
                                                     math.radians(self.upper_joint_angle - 90))),
                                         height - multiplier * (base_length + lower_arm_length * math.sin(
                                             math.radians(self.lower_joint_angle)) +
                                                                (upper_arm_length + mallet_length) * math.sin(
                                                     math.radians(self.upper_joint_angle)) +
                                                                (arm_width / (2 * multiplier)) * math.sin(
                                                     math.radians(self.upper_joint_angle - 90))),
                                         fill="grey", width=mallet_width, joinstyle=ROUND, tags="s_mallet")
        self.directions = [-12]
        lower_angles = [180 - (-87 + 90)]
        upper_angles = [180 + 26]

    def update_sim(self):
        self.directions = [-30, -15, 0, 15, 30, 0]  # theses three arrays are sequences of goal self.directions and angles
        lower_angles = [160, 185, 160, 185, 160, 170]
        upper_angles = [180, 260, 180, 260, 180, 200]
        i = 0
        while (i < len(self.directions)):
            goal_direction = self.directions[i]
            goal_lower_joint_angle = lower_angles[i]
            goal_upper_joint_angle = upper_angles[i]
            details = fill_canvas(self.birds_eye_view, self.side_view, self.direction, self.lower_joint_angle, self.upper_joint_angle,
                                  goal_direction, goal_lower_joint_angle, goal_upper_joint_angle, 1)
            self.direction = details[0]
            self.lower_joint_angle = details[1]
            self.upper_joint_angle = details[2]
            i += 1
        # calculate_and_draw("yellow", self.birds_eye_view, self.side_view, self.direction, self.lower_joint_angle, self.upper_joint_angle)
        # calculate("yellow", self.birds_eye_view, self.direction, self.lower_joint_angle, self.upper_joint_angle)

    def update_log(self, text):
        if len(self.log_text_list) > self.log_size:
            self.log_text_list.pop()
        self.log_text_list.insert(0, text)
        self.log_text.set('\n'.join(self.log_text_list))

    def play_button(self, key):
        self.update_log(f'playing: {key}')

    def record_clip(self):
        self.record_clip_button_clicked = True
        self.p = pyaudio.PyAudio()  # Create an interface to
        self.update_log('Started recording')
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)
        self.frames = []  # Initialize array to store frames
        self.updaterecording()

    def updaterecording(self):
        self.update_log(f'Updating recording, record button clicked {self.record_clip_button_clicked}')
        if self.record_clip_button_clicked:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            self.window.after(self.delay_audio, self.updaterecording)

    def stop_recording(self):
        self.update_log('Trying to stop recording')

        self.record_clip_button_clicked = False

        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()

        self.update_log('Finished recording')

        # Save the recorded data as a WAV file
        currentdt = datetime.datetime.now()
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'signalprocessing\\data\\clip_{currentdt.strftime("%m-%d_%H-%M-%S")}.wav')
        print(os.path.abspath(filename))
        wf = wave.open(os.path.abspath(filename), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def analyse_clip(self):
        fname = askopenfilename(
            initialdir=os.path.join(os.path.abspath(os.path.dirname(__file__)), f'signalprocessing\\data'),
            filetypes=(("Audio File", "*.wav"), ("All Files", "*.*")),
            title="Choose a clip"
        )
        argsdict = {
            'name': fname.split('/')[-1],
            'plot': False,
            'guiplot': True,
            'level': 'Info',
        }
        keys_and_times, img = pitch_track(SimpleNamespace(**argsdict))
        plt.savefig('displayplot.png')
        self.sequence_entry_text.set(str(keys_and_times))

        self.plot_img = PIL.ImageTk.PhotoImage(PIL.Image.open('displayplot.png'))
        self.plot_canvas.create_image(self.canvaswidth / 2, self.canvasheight / 2, image=self.plot_img)

    def run_sequence(self):
        seq_list = ast.literal_eval(self.sequence_entry_text.get())
        self.update_log(f'Running sequence: {seq_list}')
        note_list = []
        prevtime = 0
        for seqpart in seq_list:
            note, time = seqpart
            note_list.append(Note(key=note, delay=(time - prevtime)))
            prevtime = time

    def closeGUI(self):
        self.window.destroy()
        exit()

    def __init__(self, window, window_title, vid_source_bird=0, vid_source_side=0):
        self.window = window
        self.window.title(window_title)
        self.window.iconbitmap('data/amsterdam.ico')
        screen_factor = 0.9
        self.width = int(window.winfo_screenwidth() * screen_factor)
        self.height = int(window.winfo_screenheight() * screen_factor)
        self.canvaswidth = (self.width / 3)
        self.canvasheight = (self.height / 2)
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.update()

        self.init_window()

        self.log_size = 31
        self.log_text_list = []
        for i in range(self.log_size):
            self.log_text_list.append('---')
        self.log_text = StringVar()

        # 2 for the videos and 8 for xylophone keys and buttons
        self.gridcolumns = 2 + 8
        self.gridrows = 8

        # Create a canvas that can fit the above video source and simulations need to be made to fit
        # self.sim_bird_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
        # self.sim_side_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
        self.sim_bird_canvas = self.birds_eye_view
        self.sim_side_canvas = self.side_view
        self.vid_bird_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
        self.plot_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')

        # set positioning row span for because we have gridrows amount of rows to correctly place buttons
        self.sim_bird_canvas.grid(row=0, column=0, rowspan=4)
        self.sim_side_canvas.grid(row=0, column=1, rowspan=4)
        self.vid_bird_canvas.grid(row=4, column=0, rowspan=4)
        self.plot_canvas.grid(row=4, column=1, rowspan=4)

        self.log = Label(window, bg='white', textvariable=self.log_text)
        self.log.grid(row=0, column=2, columnspan=8, sticky=NSEW)
        self.log['textvariable'] = self.log_text

        key_list = ['c6', 'd6', 'e6', 'f6', 'g6', 'a6', 'b6', 'c7']
        color_list = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'white', 'blue']
        for i, key in enumerate(key_list):
            Button(window, text=key_list[i].upper(), bg=color_list[i], relief=RAISED,
                   command=partial(self.play_button, key)).grid(row=5, column=(2 + i),
                                                                sticky=NSEW, ipadx=(
                        (self.width / self.gridcolumns) / len(key_list)))

        self.sequence_entry_text = StringVar()
        self.sequence_entry = Entry(window, textvariable=self.sequence_entry_text).grid(row=4, column=2, columnspan=8,
                                                                                        sticky=NSEW)
        self.record_button = Button(window, text="Record Clip", command=self.record_clip).grid(row=6, column=2,
                                                                                               columnspan=4,
                                                                                               sticky=NSEW)
        self.stop_button = Button(window, text="Stop Recording", command=self.stop_recording).grid(row=7, column=2,
                                                                                                   columnspan=4,
                                                                                                   sticky=NSEW)
        self.analyse_button = Button(window, text="Analyse Clip", command=self.analyse_clip).grid(row=6, column=6,
                                                                                                  columnspan=4,
                                                                                                  sticky=NSEW)
        self.run_button = Button(window, text="Run Sequence", command=self.run_sequence).grid(row=7, column=6,
                                                                                              columnspan=4, sticky=NSEW)
        self.window.protocol('WM_DELETE_WINDOW', self.closeGUI)
        self.update_log('Initialized window')

        # open vid sources (cameras need to be plugged in
        self.vid_source_bird = vid_source_bird
        self.vid_source_side = vid_source_side
        self.vid_bird = CamCapture(self.canvaswidth, self.canvasheight, self.vid_source_bird)

        if not self.vid_source_side == 0:
            self.vid_side = CamCapture(self.canvaswidth, self.canvasheight, self.vid_source_side)
            self.vid_side_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
            self.vid_side_canvas.grid(row=4, column=1, rowspan=4)

        self.update_log('Initialized cameras')

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10

        self.record_clip_button_clicked = False
        self.updatevid()
        self.update_sim()

        self.delay_audio = 1
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.fs = 44100  # Record at 44100 samples per second
        self.frames = []  # Initialize array to store frames
        self.stream = None
        self.p = None

        self.update_log('Initialized audio recording settings')
        self.update_log('Starting main loop')
        self.window.mainloop()

    def updatevid(self):
        # Get a frame from the video source
        ret_bird, frame_bird = self.vid_bird.get_frame()

        if ret_bird:
            self.photo_bird = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_bird))
            self.sim_bird_canvas.create_image(self.canvaswidth / 2, self.canvasheight / 2, image=self.photo_bird)

        if not self.vid_source_side == 0:
            ret_side, frame_side = self.vid_side.get_frame()
            if ret_side:
                self.photo_side = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_side))
                self.sim_side_canvas.create_image(self.canvaswidth / 2, self.canvasheight / 2, image=self.photo_side)

        self.window.after(self.delay, self.updatevid)

    def updatesim(self):
        pass


class CamCapture:
    def __init__(self, width, height, video_source=0, ):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.vid.set(3, width)  # 3 refers to width
        self.vid.set(4, height)  # 4 refers to height

    def get_frame(self):
        ret = False
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
XylobotGUI(Tk(), "xylobot GUI", 0, 0)  # 1 is webcam
