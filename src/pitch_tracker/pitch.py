from pathlib import Path

import numpy as np

from pitch_tracker.beat import Beat


NOTES_PATH = Path(__file__).parent / "notes.csv"


class Pitch:
    def __init__(self, beat: Beat):
        self.beat = beat
        w_size = beat.waveform.size
        f_size = beat.frequency.features_length
        w_beats = beat.get_beats()

        self.frequency_beats = (w_beats / w_size * f_size).astype('int')
        self.all_notes, self.all_frequencies, self.all_pitches = self._read_notes()

    def _get_frequencies_as_pitch(self):
        pitches_index = self._get_pitches_index()
        return [int(self.all_pitches[index])
                if index else 0 for index in pitches_index]

    def get_pitches(self):
        frequencies_as_pitch = self._get_frequencies_as_pitch()
        last_beat = self.frequency_beats[0]
        pitches = []
        for beat in self.frequency_beats[1:]:
            pitches_ = frequencies_as_pitch[last_beat: beat]
            pitch = max(pitches_, key=lambda i: pitches_.count(i))
            if pitch:
                pitches.append(pitch)
            last_beat = beat
        return pitches

    def _get_pitches_index(self):
        return [
            np.argmin(
                np.abs(self.all_frequencies - f)
            ) for f in self.beat.frequency.features
        ]

    def _read_notes(self):
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
