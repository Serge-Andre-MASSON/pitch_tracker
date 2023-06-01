from pathlib import Path

import yaml


class Config:
    def __init__(self, config_path: Path | str):
        self.config_path = config_path
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def get_audio_file_config(self):
        return self.config["audio_file"]