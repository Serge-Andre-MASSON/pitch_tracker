from mido import second2tick, bpm2tempo
import numpy as np


MAX_BPM = 140
MIN_BMP = 70

MIDI_TICKS = np.array([240., 480., 720., 960., 1920])


def get_durations(beats_in_ms):
    return np.diff(beats_in_ms)


def get_bpm(durations_in_ms):
    shortest_duration = min(durations_in_ms)
    spb = shortest_duration / 1000
    bps = 1 / spb
    bpm = round(bps * 30)  # Assuming the shortest note is a heighth
    if bpm < MIN_BMP:  # If too slow, heighth is actually a quarter
        return bpm * 2
    return bpm


def ms_to_midi_ticks(ms, bpm):
    s = ms / 1000
    tempo = bpm2tempo(bpm)
    ticks = second2tick(s, 480, tempo)
    i = np.argmin(
        np.abs(MIDI_TICKS - ticks)
    )
    return int(MIDI_TICKS[i])


def get_bpm_and_midi_ticks(beats_in_ms):
    durations = get_durations(beats_in_ms)
    bpm = get_bpm(durations)
    midi_ticks = [
        ms_to_midi_ticks(duration, bpm)
        for duration in durations
    ]
    return bpm, midi_ticks
