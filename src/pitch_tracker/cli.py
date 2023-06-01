import queue
import sounddevice as sd
import soundfile as sf
from argparse import ArgumentParser
from pathlib import Path
import sys


from pitch_tracker.config import Config
from pitch_tracker.audio_file import AudioFile


parser = ArgumentParser(prog="Pitch tracker")

parser.add_argument("--file", "-f")
parser.add_argument("--record", "-r", action="store_true")
parser.add_argument("--conf", "-c")


def to_kwargs(args):
    return vars(args)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def sample_to_ms(n_samples, sampling_rate):
    samples_per_ms = sampling_rate // 1000
    return n_samples // samples_per_ms


q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


def cli():

    args = parser.parse_args()
    kwargs = to_kwargs(args)

    config_path = kwargs["conf"]
    if config_path is None:
        config_path = Path("conf.yaml")
    config = Config(config_path)
    sampling_rate = config.get_sampling_rate()

    if kwargs["file"]:
        print(kwargs["file"])
        audio_file_path = kwargs["file"]
        audio_file = AudioFile(audio_file_path, config.get_audio_file_config())
        waveform = audio_file.get_waveform()

    if kwargs["record"]:
        print("recording")

        try:
            audio_file_path = Path("test.wav")
            with sf.SoundFile(audio_file_path, mode='x', samplerate=sampling_rate, channels=1) as file:
                with sd.InputStream(samplerate=sampling_rate, device=18,
                                    channels=1, callback=callback):
                    print('#' * 80)
                    print('press Ctrl+C to stop the recording')
                    print('#' * 80)
                    while True:
                        file.write(q.get())
        except KeyboardInterrupt:
            print('\nRecording finished')
            i = input("Save : s / quit: q\n")
            if i == "s":
                pass
            else:
                audio_file_path.unlink()
            parser.exit(0)
        except Exception as e:
            parser.exit(type(e).__name__ + ': ' + str(e))
