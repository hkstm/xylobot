import os
import ast
import pyaudio
import wave
import matplotlib.pyplot as plt
import datetime

from tkinter import *
from functools import partial
from tkinter.filedialog import askopenfilename
from types import SimpleNamespace

import PIL.Image
import PIL.ImageTk
import cv2

from Note import Note
from signalprocessing.custompitchtracking import pitch_track


class XylobotGUI:

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
            note_list.append(Note(note=note, time=(time-prevtime)))
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

        self.log_size = 31
        self.log_text_list = []
        for i in range(self.log_size):
            self.log_text_list.append('---')
        self.log_text = StringVar()

        # 2 for the videos and 8 for xylophone keys and buttons
        self.gridcolumns = 2 + 8
        self.gridrows = 8

        # Create a canvas that can fit the above video source and simulations need to be made to fit
        self.sim_bird_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
        self.sim_side_canvas = Canvas(window, width=self.canvaswidth, height=self.canvasheight, background='black')
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
