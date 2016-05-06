import sys
import pyaudio
import wave
import math
import struct
import time


# sample using PyAudio
# https://people.csail.mit.edu/hubert/pyaudio/#downloads
# brew install portaudio 
# pip install pyaudio

class Audio(object):

    def __init__(self, filename, duration):
        self.filename = filename or "output.wav"
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.duration = 5

    def record(self):
        p = pyaudio.PyAudio()
        # Open stream using callback
        stream = p.open(format=self.format,
                        channels=2,
                        rate=self.rate,
                        frames_per_buffer=self.chunk,
                        input=True,
                        # output=True,
                        stream_callback=self.callback)

        print("* recording")

        frames = []

        for i in range(0, int(self.rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def callback(self, in_data, frame_count, time_info, status):
        levels = []
        for _i in range(1024):
            levels.append(struct.unpack('<h', in_data[_i:_i + 2])[0])
        avg_chunk = sum(levels) / len(levels)
        self.print_audio_level(avg_chunk, time_info['current_time'])
        return (in_data, pyaudio.paContinue)

    def print_audio_level(self, avg_chunk, current_time):
        pass
