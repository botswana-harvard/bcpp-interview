import numpy as np
import os
import sounddevice as sd
import time

from django.conf import settings


class AudioError(Exception):
    pass


class Audio(object):

    def __init__(self, filename, block_duration=None):
        self.filename = os.path.join(settings.UPLOAD_FOLDER, filename)
        self.data = np.ndarray(0, dtype='float32')
        self.status = 'ready'
        self.time = 0
        self.start_time = None
        self.stop_time = None
        self.device = 0
        self.chunk = 1024
        self.channels = 2
        self.samplerate = sd.query_devices(self.device, 'input')['default_samplerate']
        self.block_duration = block_duration or 3600

    def record(self):
        if self.status == 'ready':
            self.start_time = time.process_time()
            self.data = sd.rec(
                self.block_duration * self.samplerate,
                channels=self.channels)
            self.status = 'recording'

    def get_status(self):
        if time.process_time() - self.start_time == self.block_duration:
            self.stop()
        return self.status

    def get_time(self):
        if self.status == 'recording':
            self.time = time.process_time() - self.start_time
        return self.time

    def stop(self):
        if self.status != 'recording':
            print('Device is not recording. Current status is \'{}\''.format(self.status))
        else:
            sd.stop()
            self.stop_time = time.process_time() - self.start_time
            self.status = 'done'

    def save(self):
        if self.data.size > 0:
            self.stop()
            np.savez_compressed(self.filename, self.data)
            self.reset()

    def reset(self):
        self.time = 0
        self.data = np.ndarray(0, dtype='float32')
        self.status = 'ready'
        self.start_time = None
        self.stop_time = None

    def play(self):
        sd.play(self.data, self.samplerate)

    def load(self):
        self.data = np.load(self.filename).items()[0][1]
