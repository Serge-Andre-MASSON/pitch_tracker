import subprocess
from tempfile import NamedTemporaryFile

import mido


class Midi:
    def __init__(self, bpm, guitar, sampling_rate, sound_font) -> None:
        self.bpm = bpm
        self.guitar = guitar
        self.sampling_rate = sampling_rate
        self.sound_font = sound_font
        self._init_mido(self.bpm, self.guitar)
        self.start = 0

    def _init_mido(self, bpm, guitar):
        self.mido = mido.MidiFile()
        self.track = mido.MidiTrack()
        tempo = mido.bpm2tempo(bpm)
        self.track.append(
            mido.MetaMessage("set_tempo", tempo=tempo))
        self.track.append(
            mido.Message("program_change", program=guitar))

        self.mido.tracks.append(self.track)

    def __str__(self) -> str:
        return self.mido.__str__()

    def __repr__(self) -> str:
        return self.mido.__repr__()

    def add_note(self, duration, note):
        self.track.append(
            mido.Message(
                'note_on', note=note, velocity=100, time=self.start))
        self.track.append(
            mido.Message(
                'note_off', note=note, velocity=100, time=duration))
        self.start = 0

    def add_rest(self, duration):
        self.start += duration

    def play(self):
        midi_file = NamedTemporaryFile(suffix=".mid")
        self.mido.save(midi_file.name)
        subprocess.run([
            'fluidsynth',
            '-iq',
            self.sound_font,
            midi_file.name,
            '-r', str(self.sampling_rate)])
        midi_file.close()

    def save_wav_to(self, wav_path):
        midi_file = NamedTemporaryFile(suffix=".mid")
        self.mido.save(midi_file.name)
        subprocess.run(
            [
                'fluidsynth',
                '-ni',
                self.sound_font,
                midi_file.name,
                '-F',
                str(wav_path),
                '-r', str(self.sampling_rate),
                "--quiet"
            ]
        )
        midi_file.close()
