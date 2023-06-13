import numpy as np
from sklearn.cluster import KMeans

from pitch_tracker.waveform_features import Amplitude, Frequency


class Beat:
    def __init__(self, amplitude: Amplitude, frequency: Frequency, sampling_rate, min_samples_between_beats):
        np.testing.assert_array_equal(amplitude.waveform, frequency.waveform)
        self.waveform = amplitude.waveform

        self.amplitude = amplitude
        self.frequency = frequency

        self.waveform_length = self.waveform.size
        self.amplitude_beat = AmplitudeBeat(amplitude)
        self.frequency_beat = FrequencyBeat(frequency)
        self.sampling_rate = sampling_rate
        self.min_samples_between_beats = min_samples_between_beats

    def get_beats(self, scaled_to: int = None):
        if scaled_to is None:
            scaled_to = self.waveform.size

        amplitude_beats = self.amplitude_beat.get_beats_scaled_to(scaled_to)
        frequency_beats = self.frequency_beat.get_beats_scaled_to(scaled_to)

        all_beats = np.concatenate(
            [frequency_beats, amplitude_beats]
        )
        all_beats.sort()

        last_beat = None
        beats = []
        for beat in all_beats:
            if last_beat is None:
                last_beat = beat
                beats.append(last_beat)
                continue
            if beat - last_beat < self.min_samples_between_beats:
                if len(beats) > 1:
                    beats.pop()
                    beats.append(beat)
                last_beat = beats[-1]
                continue
            beats.append(beat)
            last_beat = beats[-1]
        return np.array(beats)


class AmplitudeBeat:
    def __init__(self, amplitude: Amplitude):
        self.amplitude = amplitude
        self.beats = None

    def get_beats(self):
        if self.beats is not None:
            return self.beats
        features = self.amplitude.get_features()

        features_range = np.arange(len(features)-1)

        D = np.diff(features).reshape(-1, 1)

        k_means = KMeans(n_clusters=2, n_init="auto").fit(D)
        labels = list(k_means.labels_)

        label = max(labels, key=lambda l: labels.count(l))
        is_edge = (labels != label)

        self.beats = features_range[is_edge]

        return self.beats

    def get_beats_scaled_to(self, array_length: int):
        return np.round(self.get_beats() * array_length / self.amplitude.get_features_length()).astype("int")


class FrequencyBeat:
    def __init__(self, frequency: Frequency):
        self.frequency = frequency
        self.beats = None

    def get_beats(self):
        features = self.frequency.get_features()
        features_range = np.arange(len(features)-1)

        D = np.abs(np.diff(features)).reshape(-1, 1)

        k_means = KMeans(n_clusters=4, n_init="auto").fit(D)
        labels = list(k_means.labels_)

        label = max(labels, key=lambda l: labels.count(l))
        self.is_beat = (labels != label)
        self._drop_unvoiced_starting_beats()
        self.beats = features_range[self.is_beat]

        return self.beats

    def _drop_unvoiced_starting_beats(self):
        last_true_beat = None
        features = self.frequency.get_features()
        for i in range(len(features) - 1):
            if self.is_beat[i]:
                if last_true_beat is None:
                    last_true_beat = i
                    continue
                pitches = features[last_true_beat:i]
                pitch = max(pitches, key=lambda i: list(pitches).count(i))
                if not pitch:
                    self.is_beat[last_true_beat] = False
                last_true_beat = i

    def get_beats_scaled_to(self, array_length: int):
        return np.round(self.get_beats() * array_length / self.frequency.get_features_length()).astype("int")
