import numpy as np
import simpleaudio as sa
from time import sleep


class LetteredMusicNotePlayer:
    def __init__(self, note_duration=0.5):
        self.note_duration = note_duration
        self.base_notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
                           'F#', 'G', 'G#', 'A', 'A#', 'B']

    def _play_note(self, frequency, duration):
        '''
        Adapted from: https://realpython.com/playing-and-recording-sound-python
        '''
        sample_rate = 44100  # 44100 samples per second
        t = np.linspace(0, duration, int(duration * sample_rate), False)
        note = np.sin(frequency * t * 2 * np.pi)
        audio = note * (2 ** 15 - 1) / np.max(np.abs(note))
        audio = audio.astype(np.int16)
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        play_obj.wait_done()

    def _play_notes(self, notes):
        for note in notes:
            if note[0] < 0:
                sleep(note[1])
            else:
                self._play_note(note[0], note[1])

    def _get_frequency(self, lettered_note, octave):
        note_idx = self.base_notes.index(lettered_note)
        n = -21 + note_idx + len(self.base_notes) * (octave - 3)
        return 440 * pow(2, n / 12)

    def _get_notes_from_lettered_notes(self, lettered_notes):
        notes = []
        for lettered_note in lettered_notes:
            lettered_note = lettered_note.strip()
            duration = self.note_duration
            if lettered_note != '|':
                octave = 4
                if lettered_note[-1] == '-':
                    duration /= 2
                    lettered_note = lettered_note[:-1]
                if lettered_note[0] == '^':
                    octave += 1
                    lettered_note = lettered_note[1:]
                elif lettered_note[0] == '*':
                    octave += 2
                    lettered_note = lettered_note[1:]
                elif lettered_note[0] == '.':
                    octave -= 1
                    lettered_note = lettered_note[1:]
                if len(lettered_note) > 1 and \
                   lettered_note[0] in 'ABCDEFG' and \
                   lettered_note[1] in 'ABCDEFG':
                    notes.append((
                        self._get_frequency(str(lettered_note[0]), octave),
                        duration
                        ))
                    lettered_note = lettered_note[1:]
                    octave = 4
                if lettered_note[-1] == 'b':
                    flatless_index = self.base_notes.index(lettered_note[:-1])
                    lettered_note = self.base_notes[flatless_index - 1]
                notes.append((
                    self._get_frequency(lettered_note, octave),
                    duration))
            elif lettered_note == '|':
                notes.append((-1, duration))
        return notes

    def play_song(self, url):
        with open('lettered_notes/' + url + '.txt', 'r') as f:
            lettered_notes = f.readline().split(',')
            f.close()
            notes = self._get_notes_from_lettered_notes(lettered_notes)
            self._play_notes(notes)


if __name__ == '__main__':
    player = LetteredMusicNotePlayer(0.24)
    player.play_song('super-mario-bros-theme-nintendo')
    player = LetteredMusicNotePlayer(0.48)
    player.play_song('a-whole-new-world-aladdin')
    player = LetteredMusicNotePlayer(0.64)
    player.play_song('take-me-home-country-roads-john-denver')
    player = LetteredMusicNotePlayer(0.32)
    player.play_song('let-it-go-frozen-disney')
