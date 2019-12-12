import xylobot.delayexample as delay


class Note:
    def __init__(self, key, delay='', coords=''):
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

    def __str__(self):
        return "Name: {}, tempo: {}, notes: {}".format(self.name, self.tempo, self.notes)


class SongManager:

    def __init__(self, hm, coords=''):
        self.songs = []
        self.notecoords = []
        self.notelist = ['c6', 'd6', 'e6', 'f6', 'g6', 'a6', 'b6', 'c7']
        self.hm = hm
        if coords != '':
            self.initializeCoords(coords)

    def play(self):
        for song in self.songs:
            for note in song.getNotes():
                print('[*] Playing note: ', note)
                delay.sleep(note.delay)
                #self.hm.hit(note, 'quadratic')
                #self.hm.hit(note, 'triangle 1')
                #self.hm.hit(note, 'triangle 2')
                self.hm.hit(note, 'uniform')

    def add(self, name, tempo, notes):
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
        i = 0
        for point in coords:
            self.notecoords.append(Note(self.notelist[i], coords=point))
            i = i + 1

    def __str__(self):
        return "Songs: {}".format(self.songs)
