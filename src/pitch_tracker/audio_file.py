from pathlib import Path

import librosa
import numpy as np


class AudioFile:
    """Provide utilities for handling an audio file."""

    def __init__(self, audio_file_path: Path, sampling_rate: int):
        self.audio_file_path = audio_file_path
        self.sampling_rate = sampling_rate
        self.waveform: np.ndarray = None

    def get_waveform(self):
        """Return a waveform of the audio. The result will be cast to mono."""
        if self.waveform is None:
            with open(self.audio_file_path, "rb") as f:
                self.waveform, _ = librosa.load(
                    self.audio_file_path,
                    sr=self.sampling_rate
                )
        return self.waveform

    def get_duration_in_ms(self):
        w = self.get_waveform()
        return w.size * 1000 / self.sampling_rate
