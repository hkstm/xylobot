import librosa
import queue as Queue
import threading

connectedtosetup = False
print(f"Connected to setup: {connectedtosetup}")
if connectedtosetup:
    from control import Calibrator

from Improv import *
from simulation.SimuVector import SimuVector
from simulation.SimuXylo import SimuXylo
from signalprocessing.SignalTrack import pitch_track_wrap
from signalprocessing.SignalTrack import pitch_track_calc
from control.ControlManager import ControlManager
from control.SongManager import Note
from control.Position import Position

from computervision import VideoCamera as vc

import Test
import os
import ast
from tkinter import *
from tkinter.ttk import Combobox, Style
from tkinter.filedialog import askopenfilename
from functools import partial
from types import SimpleNamespace
from control.Point import Point

import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import math

import PIL.Image
import PIL.ImageTk
import cv2

import itertools

screen_factor = 0.9


class XylobotGUI:

    def init_window(self):
        self.number = 0
        self.birds_eye_view = Canvas(self.window, width=self.canvaswidth, height=self.canvasheight, background="black")
        self.side_view = Canvas(self.window, width=self.canvaswidth, height=self.canvasheight, background="black")

        self.simu_xylo = SimuXylo(0,self.birds_eye_view,self.side_view)

        if connectedtosetup:
            self.cm = ControlManager(self.simu_xylo)
            self.cm.sendToArduino(Position(0, 0, 0))

            newNotesCoords = []
            print("LOADING SETUP")
            try:
                with open('notecoords.txt', 'r') as filehandle:
                    newNotesCoords = [notecoords.rstrip() for notecoords in filehandle.readlines()]
                newNotes = [tuple(coord.split()) for coord in newNotesCoords]
                #newNotes = [Point(float(x), float(y), float(z)) for (x, y, z) in newNotes]
                newNotes = [Point(float(x), float(y), float(z)) for (x,y,z) in newNotes]
                self.simu_xylo.setMiddleAndRotationWithPoints(newNotes)
                print(f'newNotes {newNotes}')

                self.cm.setNoteCoordinates(newNotes)
                print(f'newNotes {newNotes}')
                print(f'{type(newNotes)}')
            except Exception as e:
                print(e)
            print("DONE WITH LOADING")


        self.simu_xylo.update_base()

        keys = self.simu_xylo.getKeys()
        for key in keys:
            pts = key.getPoints()
            self.birds_eye_view.create_polygon(pts, fill=key.getColor(), tags = key.getColor())

        self.side_view.create_rectangle(self.simu_xylo.get_side_view_rectangle(), fill="blue", tags= "svrec")

        #self.side_view.create_rectangle(100,200,300,400, fill="blue")


        self.birds_eye_view.create_line(self.simu_xylo.get_b_line(),
                                        fill="grey", width=self.simu_xylo.arm_width, joinstyle=ROUND, tags="b_line")
        self.side_view.create_line(self.simu_xylo.get_s_line(),
                                   fill="grey", width=self.simu_xylo.arm_width, joinstyle=ROUND, tags="s_line")
        self.birds_eye_view.create_line(self.simu_xylo.get_b_mallet(),
                                        fill="grey", width=self.simu_xylo.mallet_width, joinstyle=ROUND,
                                        tags="b_mallet")
        self.side_view.create_line(self.simu_xylo.get_s_mallet(),
                                   fill="grey", width=self.simu_xylo.mallet_width, joinstyle=ROUND, tags="s_mallet")

        self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view,0, 0, 0,1)





    def update_sim(self):
        self.idx_direction = 0
        self.directions = [-30, -15, 0, 15, 30, 0]  # theses three arrays are sequences of goal self.directions and angles
        self.lower_angles = [160, 185, 160, 185, 160, 170]
        self.upper_angles = [180, 260, 180, 260, 180, 200]
        self.direction = 0
        self.lower_joint_angle = 160
        self.upper_joint_angle = 210

        self.is_simlooping = False

        self.update_sim_loop()
        self.window.after(self.delay, self.update_sim_loop)
        #calculate_and_draw("yellow", self.birds_eye_view, self.side_view, self.direction, self.lower_joint_angle, self.upper_joint_angle)
        #calculate("yellow", self.birds_eye_view, self.direction, self.lower_joint_angle, self.upper_joint_angle)

    def update_sim_loop(self):
        goal_direction = self.directions[self.idx_direction]
        goal_lower_joint_angle = self.lower_angles[self.idx_direction]
        goal_upper_joint_angle = self.upper_angles[self.idx_direction]
        self.simu_xylo.update_joint_angles(self.direction, self.lower_joint_angle, self.upper_joint_angle)
        details = self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view,
                                             goal_direction, goal_lower_joint_angle, goal_upper_joint_angle, seconds=20)
        self.direction = details[0]
        self.lower_joint_angle = details[1]
        self.upper_joint_angle = details[2]
        self.idx_direction += 1
        if self.idx_direction == len(self.directions):
            self.is_simlooping = False
        if self.is_simlooping:
            self.window.after(self.delay, self.update_sim_loop)

    def move_simulation_robot(self, goal_direction, goal_lower_joint_angle, goal_upper_joint_angle):
        # TODO: calculate how long the movement should take based on the time the robot takes
        self.simu_xylo.update_joint_angles(self.direction, self.lower_joint_angle, self.upper_joint_angle)
        details = self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view,
                                             goal_direction, goal_lower_joint_angle, goal_upper_joint_angle, seconds=3)
        self.direction = details[0]
        self.lower_joint_angle = details[1]
        self.upper_joint_angle = details[2]

        # self.idx_direction += 1
        # if self.idx_direction == len(self.directions):
        #     self.simlooping = False
        # if self.simlooping:
        #     self.window.after(self.delay, self.update_sim_loop)

    def update_log(self, text):
        if len(self.log_text_list) > self.log_size:
            self.log_text_list.pop()
        text_length_limit = 80
        text_short = (text[:text_length_limit] + '...') if len(text) > text_length_limit else text
        self.log_text_list.insert(0, text_short)
        self.log_text.set('\n'.join(self.log_text_list))

    def set_xylophone_location(self, x, y, z):
        self.simu_xylo.setXyloMidpoint(SimuVector(0, 20, 11), cm=True)
        self.simu_xylo.updateXyloDrawing(self.birds_eye_view,self.side_view)

    def play_btn(self, key, event=None):
        self.update_log(f'playing: {key}')
        # #####3#TODO REMOVE THIS TESTER:
        #
        # pts = [Point(-13.61, 24.67,12),Point(9.037,21.975,12)]
        # pts = [Point(-13.61, 24.67,12),Point(9.037,21.975,12)]
        #
        # self.simu_xylo.setMiddleAndRotationWithPoints(pts)
        #
        #
        # if(key == "d6"):
        #     self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, -33, -63, 68, 0)
        # elif(key == "c6"):
        #     self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, 18.5, -75.9, 46.89, 0)
        # elif(key == "b6"):
        #     self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, -26.1, -60.22, 73.53, 0)
        # elif(key=="f6"):
        #     self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, 5.99, -65.57, 64, 0)
        # else:
        #     self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view,20, 20, 20, 0)



        #self.simu_xylo.setXyloMidpoint(SimuVector(0,0,11), cm = True)
        #self.simu_xylo.goodRotate(30)
        #self.number = self.number + 2
        #print(self.number)

        #self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, 0, self.number, 20,0)
        #self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, 0, 60, 68,0)

        #self.simu_xylo.fill_canvas(self.birds_eye_view, self.side_view, -33.1, -63.25, 68,0)

        #self.simu_xylo.fill_canvas(SimuVector(0,self.number,11),cm=True)
        #self.simu_xylo.setXyloMidpoint(SimuVector(-2.2,23.3,11),cm=True)
        #self.simu_xylo.setRotation(180)
        #self.simu_xylo.setXyloMidpoint(SimuVector(0,self.number,11),cm=True)
        # self.simu_xylo.updateXyloDrawing(self.birds_eye_view, self.side_view)
        #self.move_Simulation_Robot(20,180,220)
        ############3
        # if connectedtosetup:
        #     self.start_pitchcheck(notelist=[Note(key=key, delay=0)])
        #     # control.hitkey(key)
        #     self.cm.hit(Note(key, 0.8), hittype='triangle 2')


    def run_sequence_threaded(self):
        if self.is_pitchchecking:
            self.stop_pitchcheck()
        seq_list = ast.literal_eval(self.sequence_entry_text.get())
        self.update_log(f'Running sequence: {seq_list}')
        note_list = []
        prevtime = 0
        for seqpart in seq_list:
            note, time = seqpart
            note_list.append(Note(key=note, delay=(time - prevtime)))
            prevtime = time
        if connectedtosetup:
            self.start_pitchcheck(notelist=note_list)
            self.cm.addSong('improv', 2, note_list)
            RunSequenceThread(self, self.cm).start()

            # Control.play(note_list)

    # TODO call right method, calibrator needs to be restructured
    def calibrate(self):
        self.queue = Queue.Queue()
        CalibrateThread(self.queue, self,self.simu_xylo).start()
        self.window.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print(msg)
            # Show result of the task if needed
            # self.prog_bar.stop()
        except Queue.Empty:
            self.window.after(100, self.process_queue)

    def start_recordclip(self):
        self.recordclip_btn_isclicked = True
        self.p = pyaudio.PyAudio()  # Create an interface to
        self.update_log('Started recording')
        self.stream = self.p.open(format=self.sampleformat,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)
        self.frames = []  # Initialize array to store frames
        self.do_recordclip()

    def do_recordclip(self):
        self.update_log(f'Updating recording, record button clicked {self.recordclip_btn_isclicked}')
        if self.recordclip_btn_isclicked:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            self.window.after(self.delay_audio, self.do_recordclip)

    def stop_recordclip(self):
        self.update_log('Trying to stop recording')

        self.recordclip_btn_isclicked = False

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self.update_log('Finished recording')

        # Save the recorded data as a WAV file
        currentdt = datetime.datetime.now()
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'signalprocessing\\data\\clip_{currentdt.strftime("%m-%d_%H-%M-%S")}.wav')
        print(os.path.abspath(filename))
        wf = wave.open(os.path.abspath(filename), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sampleformat))
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
            'name': fname.split('/')[-1].split('.')[0],
            'plot': False,
            'guiplot': True,
            'level': 'info',
            'window': 'blackman',
            # 'fftsize': self.fft_entry_text.get(),
            'fftsize': 512,
            'topindex': 1,
            'loudnessfactor': 0.4,
        }
        key_and_times, img = pitch_track_wrap(SimpleNamespace(**argsdict))
        # print(keys_and_times)
        # temp = full_align(keys_and_times)
        # print(temp)
        plt.savefig('displayplot.png')
        self.sequence_entry_text.set(str(key_and_times))

        # self.plot_img = PIL.ImageTk.PhotoImage(PIL.Image.open('signalprocessing\data\displayplot.png'))
        # self.plot_canvas.create_image(self.canvaswidfth / 2, self.canvasheight / 2, image=self.plot_img)

    def update_hitmethods(self, event=None):
        # combobox_event.selection_clear()
        method = self.hitmethods_text.get()

    def play_btn_threaded(self, key, event=None):



        if self.is_pitchchecking:
            self.stop_pitchcheck()
        self.update_log(f'playing: {key}')
        if connectedtosetup:
            self.start_pitchcheck(notelist=[Note(key=key, delay=0)])
            # control.hitkey(key)
            print(f'key {key}')
            self.cm.addSong('singlehit', 3, [Note(key, 0.8)])
            self.queue = Queue.Queue()
            RunSequenceThread(self.queue, self, self.cm).start()
            self.window.after(100, self.process_queue)

    # def play_btn_old(self, key, event=None):
    #     self.update_log(f'playing: {key}')
    #     # #TODO REMOVE THIS TESTER:
    #     # self.xylo.setXyloMidpoint(SimuVector(0,20,11), cm = True)
    #     # self.xylo.goodRotate(30)
    #     # updateXyloDrawing(self.xylo,self.birds_eye_view)
    #     # self.move_Simulation_Robot(20,180,220)
    #     ############
    #     if connectedtosetup:
    #         self.start_pitchcheck(notelist=[Note(key=key, delay=0)])
    #         # control.hitkey(key)
    #         self.cm.hit(Note(key, 0.8), dynamics='p', hittype=self.hitmethods_text.get(), tempo=1)

    # def run_sequence_old(self):
    #     seq_list = ast.literal_eval(self.sequence_entry_text.get())
    #     self.update_log(f'Running sequence: {seq_list}')
    #     note_list = []
    #     prevtime = 0
    #     for seqpart in seq_list:
    #         note, time = seqpart
    #         note_list.append(Note(key=note, delay=(time - prevtime)))
    #         prevtime = time
    #     if connectedtosetup:
    #         self.start_pitchcheck(notelist=note_list)
    #         self.cm.addSong('improv', 3, note_list)
    #
    #         print('after play')
    #         # Control.play(note_list)

    def start_pitchcheck(self, notelist):
        self.is_pitchchecking = True
        self.notelist = notelist
        self.p = pyaudio.PyAudio()  # Create an interface to
        self.update_log('Starting pitch checking')
        self.stream = self.p.open(format=self.sampleformat,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)
        self.numpyframes = []  # Initialize array to store frames

        self.cm.sm.hm.hits = 0
        self.pitchcheckcounter = 0
        self.pitchtrackcalcs = 0

        self.do_pitchcheck()
        # self.stop_pitchcheck()

    def do_pitchcheck(self):
        # self.update_log('doing pitchcheck')
        if self.is_pitchchecking:
            data = self.stream.read(self.chunk)
            self.numpyframes.append((np.frombuffer(data, dtype=np.int16)))
            numpydata = np.hstack(self.numpyframes)
            fft_size = int(self.fft_entry_text.get())
            pitchcheck_every = 1000
            if self.pitchcheckcounter % pitchcheck_every == 0:
                self.update_log('self.pitchcheckcounter % pitchcheck_every == 0')
                if len(numpydata) > self.chunk:
                    print('pitch checking')
                    pitchtrack_resNS = pitch_track_calc(self.fs, numpydata, fft_size, False, False, 1, 'blackman', loudness_factor=0.4, amp_thresh=0)
                    self.pitchtrackcalcs += 1
                    print(pitchtrack_resNS.key_and_times)

            if self.pitchtrackcalcs > 0 and len(pitchtrack_resNS.key_and_times) > 0:
                self.update_log(pitchtrack_resNS.key_and_times)
                self.update_log(self.notelist)

                if pitchtrack_resNS.key_and_times[len(pitchtrack_resNS.key_and_times) - 1] != self.notelist[len(pitchtrack_resNS.key_and_times) - 1]:
                    self.update_log('Setup might need to be recalibrated')
                else:
                    self.update_log("setup still calibrated")

                if self.cm.sm.hm.hits == len(self.notelist) and self.pitchcheckcounter > 0 and len(pitchtrack_resNS.key_and_times) >= len(self.notelist):
                    self.update_log('Stopping pitch check')
                    self.stop_pitchcheck()
                elif self.cm.sm.hm.hits > len(self.notelist):
                    self.update_log("!!!Song hits larger than length note list")
                    self.stop_pitchcheck()
                else:
                    pass
                    # self.update_log('not stopping pitch check')

            self.pitchcheckcounter += 1
            self.window.after(self.delay_audio, self.do_pitchcheck)

    def stop_pitchcheck(self):
        self.update_log('Trying to stop pitch checking')
        self.is_pitchchecking = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.update_log('Stopped pitch checking')

    def improvise_sequence(self):

        self.update_log('Trying to stop recording')
        self.recordclip_btn_isclicked = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.update_log('Finished recording')
        # Save the recorded data as a WAV file
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                f'signalprocessing\\data\\improv.wav')
        print(os.path.abspath(filename))
        wf = wave.open(os.path.abspath(filename), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sampleformat))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        fname = 'improv'
        argsdict = {
            'name': fname.split('/')[-1],
            'plot': False,
            'guiplot': True,
            'level': 'info',
            'window': 'hanning',
            'fftsize': self.fft_entry_text.get(),
            'topindex': 1
        }
        key_and_times = pitch_track_wrap(SimpleNamespace(**argsdict))
        num_improv_notes = 16
        sequence = create_music(key_and_times[0], num_improv_notes)
        if connectedtosetup:
            notes = [0] * len(sequence)
            for i in range(len(sequence)):
                notes[i] = Note(key=sequence[i][0], delay=sequence[i][1])
            self.start_pitchcheck(notelist=sequence)
            self.cm.addSong('improv', 20, notes)
            self.cm.play()

    def close_gui(self):
        self.window.destroy()
        exit()

    def __init__(self, window, window_title, vid_source_bird=0, vid_source_side=0):
        # self.style = Style()
        # print(self.style.theme_use())
        #
        # print(self.style.theme_names())
        # self.style.theme_use('alt')
        self.window = window
        self.window.title(window_title)
        self.window.iconbitmap('data/amsterdam.ico')

        self.width = int(window.winfo_screenwidth() * screen_factor)
        self.height = int(window.winfo_screenheight() * screen_factor)
        self.canvaswidth = (self.width / 3)
        self.canvasheight = (self.height / 2)
        self.window.geometry(f'{self.width}x{self.height}')
        self.window.state('zoomed')
        self.window.update()
        self.init_window()

        self.log_size = 20
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

        self.sim_side_canvas.grid(row=0, column=1, rowspan=4)
        self.vid_bird_canvas.grid(row=0, column=0, rowspan=4)
        self.sim_bird_canvas.grid(row=4, column=0, rowspan=5)
        self.plot_canvas.grid(row=4, column=1, rowspan=5)

        self.log = Label(window, bg='white', textvariable=self.log_text)
        self.log.grid(row=0, column=2, columnspan=8, sticky=NSEW)
        self.log['textvariable'] = self.log_text

        key_list = ['c6', 'd6', 'e6', 'f6', 'g6', 'a6', 'b6', 'c7']
        color_list = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'white', 'blue']
        for i, key in enumerate(key_list):
            Button(window, text=key_list[i].upper(), bg=color_list[i], relief=RAISED,
                   command=partial(self.play_btn_threaded, key)).grid(row=5, column=(2 + i),
                                                                      sticky=NSEW, ipadx=(
                        (self.width / self.gridcolumns) / len(key_list)))
            self.window.bind(f'{i + 1}', partial(self.play_btn_threaded, key))

        self.sequence_entry_text = StringVar()
        self.sequence_entry = Entry(window, textvariable=self.sequence_entry_text).grid(row=4, column=2, columnspan=8,
                                                                                        sticky=NSEW)
        self.calibrate_btn = Button(window, text="Calibrate Setup", command=self.calibrate).grid(row=6, column=2,
                                                                                                 columnspan=2,
                                                                                                 rowspan=1,
                                                                                                 sticky=NSEW)

        self.fft_label = Label(window, text="FFT Size:", relief=RIDGE)
        self.fft_label.grid(row=7, column=2, columnspan=1, sticky=NSEW)

        self.fft_entry_text = StringVar()
        self.fft_entry = Entry(window, textvariable=self.fft_entry_text)
        self.fft_entry.grid(row=7, column=3, columnspan=1, sticky=NSEW)
        self.fft_entry_text.set('2048')

        self.ampthresh_label = Label(window, text="Amp Thresh:", relief=RIDGE)
        self.ampthresh_label.grid(row=7, column=4, columnspan=1, sticky=NSEW)

        self.ampthresh_entry_text = StringVar()
        self.ampthresh_entry = Entry(window, textvariable=self.ampthresh_entry_text)
        self.ampthresh_entry.grid(row=7, column=5, columnspan=1, sticky=NSEW)
        self.ampthresh_entry_text.set('0')

        self.intensity_label = Label(window, text="Intensity:", relief=RIDGE)
        self.intensity_label.grid(row=6, column=6, columnspan=1, sticky=NSEW)

        self.intensity_entry_text = StringVar()
        self.intensity_entry = Entry(window, textvariable=self.intensity_entry_text)
        self.intensity_entry.grid(row=6, column=7, columnspan=1, sticky=NSEW)
        self.intensity_entry_text.set('512')

        # self.hitmethods_text = StringVar()
        # self.hitmethods_cbbox = Combobox(window, textvariable=self.hitmethods_text, state='readonly',
        #                                  values=('Uniform', 'Triangle 1', 'Triangle 2', 'Triangle 3', 'Quadratic'))
        # self.hitmethods_text.set('Triangle 2')
        # self.hitmethods_cbbox.bind('<<ComboboxSelected>>', self.update_hitmethods)

        self.delay_label = Label(window, text="some parameter:", relief=RIDGE)
        self.delay_label.grid(row=6, column=8, columnspan=1, sticky=NSEW)

        self.delay_entry_text = StringVar()
        self.delay_entry = Entry(window, textvariable=self.delay_entry_text)
        self.delay_entry.grid(row=6, column=9, columnspan=1, sticky=NSEW)
        self.delay_entry_text.set('100')

        self.hitmethods_text = StringVar()
        self.hitmethods_cbbox = Combobox(window, textvariable=self.hitmethods_text, state='readonly',
                                         values=('Uniform', 'Triangle 1', 'Triangle 2', 'Triangle 3', 'Quadratic'))
        self.hitmethods_text.set('Triangle 2')
        self.hitmethods_cbbox.bind('<<ComboboxSelected>>', self.update_hitmethods)
        self.hitmethods_cbbox.grid(row=7, column=6, columnspan=4, sticky=NSEW)

        self.record_btn = Button(window, text="Record Clip", command=self.start_recordclip).grid(row=8, column=2,
                                                                                                 rowspan=2,
                                                                                                 columnspan=2,
                                                                                                 sticky=NSEW)
        self.stop_btn = Button(window, text="Stop Recording", command=self.stop_recordclip).grid(row=8, column=4,
                                                                                                 rowspan=2,
                                                                                                 columnspan=2,
                                                                                                 sticky=NSEW)
        self.analyse_btn = Button(window, text="Analyse Clip", command=self.analyse_clip).grid(row=8, column=6,
                                                                                               rowspan=2,
                                                                                               columnspan=2,
                                                                                               sticky=NSEW)
        # self.run_btn = Button(window, text="Run Sequence", command=self.run_sequence).grid(row=8, column=8,
        #                                                                                    rowspan=2,
        #                                                                                    columnspan=2, sticky=NSEW)
        self.run_btn = Button(window, text="Run Sequence", command=self.run_sequence_threaded).grid(row=8, column=8,
                                                                                                    rowspan=2,
                                                                                                    columnspan=2,
                                                                                                    sticky=NSEW)
        self.improvise_btn = Button(window, text="Improvise", command=self.improvise_sequence).grid(row=6, column=4,
                                                                                                    columnspan=2,
                                                                                                    rowspan=1,
                                                                                                    sticky=NSEW)
        self.window.protocol('WM_DELETE_WINDOW', self.close_gui)
        self.update_log('Initialized window')

        # open vid sources (cameras need to be plugged in
        self.vid_source_bird = vid_source_bird
        self.vid_source_side = vid_source_side
        self.vid_bird = CamCapture(self.canvaswidth, self.canvasheight, self.vid_source_bird)
        #
        # if not self.vid_source_side == 0:
        #     self.vid_side = CamCapture(self.canvaswidth, self.canvasheight, self.vid_source_side)
        #     self.vid_side_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
        #     self.vid_side_canvas.grid(row=4, column=1, rowspan=4)

        self.update_log('Initialized cameras')

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10

        self.recordclip_btn_isclicked = False
        self.is_pitchchecking = False

        self.update_vid()
        #self.update_sim()
        # p1 = multiprocessing.Process(target=self.update_sim)
        # p1.start()

        # t1 = threading.Thread(target=self.update_sim)
        # t1.start()
        # t1.join()

        self.delay_audio = 1
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sampleformat = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.fs = 44100  # Record at 44100 samples per second
        self.frames = []  # Initialize array to store frames
        self.stream = None
        self.p = None

        self.update_log('Initialized audio recording settings')
        self.update_log('Starting main loop')
        self.window.mainloop()

    def update_vid(self):
        # Get a frame from the video source
        ret_bird, frame_bird = self.vid_bird.get_frame()

        if ret_bird:
            self.photo_bird = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(cv2.cvtColor(frame_bird, cv2.COLOR_BGR2RGB)))
            self.vid_bird_canvas.create_image(self.canvaswidth / 2, self.canvasheight / 2, image=self.photo_bird)

        # if not self.vid_source_side == 0:
        #     ret_side, frame_side = self.vid_side.get_frame()
        #     if ret_side:
        #         self.photo_side = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_side))
        #         self.sim_side_canvas.create_image(self.canvaswidth / 2, self.canvasheight / 2, image=self.photo_side)

        self.window.after(self.delay, self.update_vid)

    def updateCenterpointsImage(self):
        self.centerpoints_img = PIL.ImageTk.PhotoImage(PIL.Image.open('centerpoints.jpg'))
        self.plot_canvas.create_image(self.canvaswidth / 2, self.canvasheight / 2,
                                      image=self.centerpoints_img)


class RunSequenceThread(threading.Thread):
    def __init__(self, gui, cm):
        threading.Thread.__init__(self)

        self.gui = gui
        self.cm = cm

    def run(self):
        if connectedtosetup:
            self.gui.update_log('Started note hit thread')
            try:
                try:
                    self.cm.play()
                except Exception as e:
                    pass
            except Exception as e:
                print(e)
                self.gui.update_log(f'Note hit failed: {e}')
        else:
            print('Not connected to setup')



class CalibrateThread(threading.Thread):
    def __init__(self, queue, gui, simulation):
        threading.Thread.__init__(self)
        self.queue = queue
        self.gui = gui

    def run(self):
        print("Connected to setup: ", connectedtosetup)
        if connectedtosetup:
            self.gui.update_log('Started calibration')
            try:
                newNotes = Calibrator.calibrate(self.gui, self.gui.cm)

                with open('notecoords.txt', 'w') as filehandle:
                    filehandle.writelines("%s\n" % notecoords for notecoords in newNotes)

                print(f'newNotes {newNotes}')
                print(f'{type(newNotes)}')

                print('Calibration successful with: ')
                for note in newNotes:
                    print(note.x, note.y)
                    self.gui.update_log(f'{note.x}, {note.y}')
                self.gui.update_log(f'Calibration successful with:')
                # control.setNotes(newNotes)

                self.gui.cm.setNoteCoordinates(newNotes)
                self.gui.updateCenterpointsImage()

                ####TODO set correct place in the simulation
                self.gui.simulation.setMiddleWithPoints(newNotes)
                ####


                try:
                    Calibrator.monitor(self.gui)
                except Exception as e:
                    print('Monitoring xylophone position failed. Recalibrate xylophone to restart closed-loop.')
                    print(e)
                    self.gui.update_log('Recalibrate xylophone to restart closed-loop.')
                    self.gui.update_log(f'Monitoring xylophone position failed: {e}')
            except Exception as e:
                print(e)
                self.gui.update_log(f'Calibration failed: {e}')
                Calibrator.destroyWindows()
        else:
            Test.run(self.gui)

        self.queue.put("Task finished")
        self.queue = None


class CamCapture:
    def __init__(self, width, height, video_source=0, ):
        # Open the video source
        # self.vid = cv2.VideoCapture(video_source)
        self.vid = vc.NewVideoCamera(video_source)
        if not self.vid.isOpen():
            raise ValueError("Unable to open video source", video_source)

        # self.vid.getCap.set(3, width)  # 3 refers to width
        # self.vid.getCap.set(4, height)  # 4 refers to height

        self.width = int(width)
        self.height = int(height)

        # self.vid.setDimensions(width, height)

    def get_frame(self):
        # frame = self.vid.getNextFrame()
        # return frame
        ret = False
        if self.vid.isOpen():
            ret, frame = self.vid.getNextFrame()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                frame = cv2.resize(frame, (self.width, self.height))
                # print((self.width, self.height))
                return ret, frame
            else:
                return ret, None
        else:
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpen():
            self.vid.release()


# Create a window and pass it to the Application object
XylobotGUI(Tk(), "xylobot GUI", 0, 0)  # 1 is webcam
