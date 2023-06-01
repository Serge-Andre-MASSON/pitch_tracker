from pathlib import Path

import librosa
import numpy as np


NOTES_PATH = Path(__file__).parent / "notes.csv"


def read_notes():
    notes = ["nan"]
    frequencies = [0]
    pitches = [0]

    with open(NOTES_PATH) as csv:
        for line in csv:
            n, f, p = line.split(',')
            notes.append(n)
            frequencies.append(float(f))
            pitches.append(p.replace("\n", ""))

    return np.array(notes), np.array(frequencies), np.array(pitches)


class PitchFinder:
    def __init__(self) -> None:
        # self.sampling_rate = sampling_rate
        self.notes, self.frequencies, self.pitches = self._read_notes()

    def _read_notes(self):
        notes = []
        frequencies = []
        pitches = []

        with open(NOTES_PATH) as csv:
            for line in csv:
                n, f, p = line.split(',')
                notes.append(n)
                frequencies.append(float(f))
                pitches.append(p.replace("\n", ""))

        return np.array(notes), np.array(frequencies), np.array(pitches)

    def get_frequency(self, split):
        f0, _, _ = librosa.pyin(
            y=split,
            sr=self.sampling_rate,
            fmin=80, fmax=1400,
            boltzmann_parameter=20,
        )
        f0: np.ndarray = np.array(f0)
        l = len(f0) // 3
        f = f0[l:l*2]
        return f.mean()

    def get_closest_frequency_index(self, frequency):
        return np.argmin(
            np.abs(self.frequencies - frequency)
        )

    def get_closest_frequency(self, frequency):
        index = self.get_closest_frequency_index(frequency)
        return self.frequencies[index]

    def get_pitch(self, frequency):
        index = self.get_closest_frequency_index(frequency)
        return self.pitches[index]

    def get_note(self, frequency):
        index = self.get_closest_frequency_index(frequency)
        return self.notes[index]
