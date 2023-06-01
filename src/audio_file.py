from pathlib import Path

import librosa
from IPython.display import Audio


class AudioFile:
    """Provide utilities for handling an audio file."""

    def __init__(self, audio_file_path: Path, sampling_rate: int):
        self.audio_file_path = audio_file_path
        self.sampling_rate = sampling_rate

    def get_waveform(self):
        """Return a waveform of the audio. THe result will be cast to mono."""
        with open(self.audio_file_path, "rb") as f:
            waveform, _ = librosa.load(
                self.audio_file_path,
                sr=self.sampling_rate
            )
        return waveform

    def show_player(self):
        """Display an player when called from a notebook."""
        return Audio(self.audio_file_path)
