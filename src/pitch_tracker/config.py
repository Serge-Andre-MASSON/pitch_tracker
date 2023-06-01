from pathlib import Path

import yaml


class Config:
    def __init__(self, config_path: Path | str):
        self.config_path = config_path
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def get_sampling_rate(self):
        return self.config["sampling_rate"]

    def get_audio_file_config(self):
        return self.config["audio_file"]

    def get_amplitude_config(self):
        return self.config["waveform_features"]["amplitude"]

    def get_frequency_config(self):
        return self.config["waveform_features"]["frequency"]

    def get_beat_config(self):
        return self.config["beat"]

    def get_midi_config(self):
        return self.config["midi"]
