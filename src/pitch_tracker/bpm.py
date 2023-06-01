from mido import second2tick, bpm2tempo
import numpy as np

MAX_BPM = 120
MIN_BMP = 80

def get_durations(beats_in_ms):
    return np.diff(beats_in_ms)

def get_bpm(durations_in_ms):
    longest_beat = max(durations_in_ms)
    spb = longest_beat / 1000
    bps = 1 / spb
    bpm = round(bps * 60)

    if bpm > MAX_BPM:
        return bpm // 2
    if bpm < MIN_BMP:
        return bpm * 2

    return bpm


def ms_to_midi_ticks(ms, bpm):
    midi_ticks = np.array([240., 480., 720., 960.])
    s = ms / 1000
    tempo = bpm2tempo(bpm)
    ticks = second2tick(s, 480, tempo)
    i = np.argmin(
        np.abs(midi_ticks - ticks)
    )
    return int(midi_ticks[i])


def get_bpm_and_midi_ticks(beats_in_ms):
    durations = get_durations(beats_in_ms)
    bpm = get_bpm(durations)
    midi_ticks = [
        ms_to_midi_ticks(duration, bpm)
        for duration in durations
    ]
    return bpm, midi_ticks
