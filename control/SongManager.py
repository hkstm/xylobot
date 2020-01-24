import time
from .Point import Point


class Note:
    def __init__(self, key, delay=0.5, coords='', power=4, speed=1, hittype='triangle 2'):
        self.key = key
        self.delay = delay
        self.coords = coords
        self.power = power  # velocity
        self.speed = speed
        self.hittype = hittype

    def __str__(self):
        return f"Note: {self.key}, delay: {self.delay}, coords: {self.coords}, power: {self.power}, speed: {self.speed}, hit type: {self.hittype}"


class Song:
    def __init__(self, name, tempo, notes):
        self.name = name
        self.tempo = tempo
        self.notes = notes

    def getNotes(self):
        return self.notes

    def setNotes(self, notes):
        self.notes = notes

    def getTempo(self):
        return self.tempo

    def setTempo(self, tempo):
        self.tempo = tempo

    def __str__(self):
        return "Name: {}, tempo: {}, notes: {}".format(self.name, self.tempo, self.notes)


class SongManager:

    def __init__(self, hm):
        self.songs = []
        self.notecoords = []
        self.notelist = ['c6', 'd6', 'e6', 'f6', 'g6', 'a6', 'b6', 'c7']
        self.hm = hm
        self.note = Note('tmp', delay=0.01)

    def play(self, dynamics='p', hittype='triangle 2'):
        for song in self.songs:
            tempo = song.getTempo()
            for note in song.getNotes():
                malletBounce = 0
                if dynamics == 'pp':
                    note.power = 1
                    malletBounce = -0.1
                elif dynamics == 'mp':
                    note.power = 2
                    malletBounce = 0.7
                elif dynamics == 'p':
                    note.power = 3
                    malletBounce = 1
                elif dynamics == 'mf':
                    note.power = 4
                    malletBounce = 1.5
                elif dynamics == 'f':
                    note.power = 5
                    malletBounce = 1.3
                elif dynamics == 'ff':
                    note.power = 5
                    malletBounce = 1
                note.hittype = hittype
                #print('malletBounce: ', malletBounce)
                try:
                    #print('[*] Playing note: ', note)
                    if note.delay - tempo*0.1 < 0:
                        time.sleep(note.delay)
                    else:
                        time.sleep(note.delay - tempo * 0.1)
                    self.hit(note, tempo, malletBounce=malletBounce)
                except Warning as w:
                    print(w)
                    pass

    def goCray(self):
        points = [
            Point(10, 18, 16),
            Point(-5, 18, 16),
            Point(10, 18, 16),
            Point(-5, 18, 16),
            Point(10, 18, 16),
            Point(-5, 18, 16)
        ]
        for p in points:
            self.hitPoint(p)
        self.hm.standTall()

    def hit(self, note, tempo=0, malletBounce=0):
        newnote = next((x for x in self.notecoords if x.key == note.key), None)
        note.coords = newnote.coords
        self.hm.calculatePath(note, tempo, malletBounce)
        self.hm.hit()

    def hitPoint(self, point):
        self.note.coords = point
        self.hm.calculatePath(self.note)
        self.hm.hit()

    def add(self, name, tempo, notes):
        self.songs = []
        newnotes = []
        for note in notes:
            newnote = next((x for x in self.notecoords if x.key == note.key), None)
            newnotes.append(Note(note.key, note.delay, newnote.coords))
        song = Song(name, tempo, newnotes)
        if song not in self.songs:
            self.songs.append(song)

    def remove(self, song):
        self.songs.remove(song)

    def getSongs(self):
        return self.songs

    def setSongs(self, songs):
        self.songs = songs

    def initializeCoords(self, coords):
        self.notecoords = []
        i = 0
        for point in coords:
            self.notecoords.append(Note(self.notelist[i], coords=point))
            i = i + 1

    def __str__(self):
        return "Songs: {}".format(self.songs)
