from abc import ABC, abstractmethod

import librosa
import numpy as np


class WaveformFeature(ABC):

    def __init__(self, waveform: np.ndarray, sampling_rate: int):
        self.waveform = waveform
        self.sampling_rate = sampling_rate
        self.features: np.ndarray = None
        self.features_length: int = None

    @abstractmethod
    def _set_features(self):
        pass

    def get_features(self):
        if self.features is None:
            self._set_features()
        return self.features

    def get_features_length(self):
        if self.features_length is None:
            self.get_features()
        return self.features_length


class Frequency(WaveformFeature):

    def _set_features(self):
        features, _, _ = librosa.pyin(
            y=self.waveform,
            sr=self.sampling_rate,
            fmin=70, fmax=1400,
            boltzmann_parameter=2,
            fill_na=0
        )
        self.features = features
        self.features_length = features.size

    def get_features(self):
        """Return frequencies contour of the waveform."""
        return super().get_features()


class Amplitude(WaveformFeature):

    def __init__(self, waveform: np.ndarray, sampling_rate: int, window_size_inverse_ratio: int,) -> None:
        super().__init__(waveform, sampling_rate)
        self.window_size = sampling_rate // window_size_inverse_ratio

    def _set_features(self):
        w = self.window_size
        n_samples = self.waveform.size
        self.features = np.array([self.waveform[w*i:w*(i+1)].max()
                                  for i in range(n_samples // w)])
        self.features_length = self.features.size

    def get_features(self):
        """Return the upper envelop of the waveform."""
        return super().get_features()
