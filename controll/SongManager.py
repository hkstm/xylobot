import delayexample as delay
from Point import Point


class Note:
    def __init__(self, key, delay=0.0, coords=''):
        self.key = key
        self.delay = delay
        self.coords = coords

    def __str__(self):
        return "Note: {}, delay: {}, coords: {}".format(self.key, self.delay, self.coords)


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

    def play(self):
        for song in self.songs:
            self.hm.setTempo(song.getTempo())
            for note in song.getNotes():
                try:
                    #print('[*] Playing note: ', note)
                    self.hit(note)
                    delay.sleep(note.delay)
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

    def hit(self, note):
        newnote = next((x for x in self.notecoords if x.key == note.key), None)
        note.coords = newnote.coords
        self.hm.calculatePath(note)
        self.hm.hit()

    def hitPoint(self, point):
        n = Note('sup', delay=0.01, coords=point)
        self.hm.calculatePath(n)
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
