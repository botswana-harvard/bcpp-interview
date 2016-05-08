import numpy as np
import os
import sounddevice as sd
import time

from django.conf import settings
from django.utils import timezone

RECORDING = 'recording'
READY = 'ready'


class AudioError(Exception):
    pass


class Audio(object):

    def __init__(self):
        self.data = np.ndarray(0, dtype='float32')
        self.filename = None
        self.status = READY
        self.recording_time = 0
        self.start_time = 0
        self.block_duration = None
        self.device = 0
        self.chunk = 1024
        self.channels = 1
        self.samplerate = sd.query_devices(self.device, 'input')['default_samplerate']

    def record(self, filename, samplerate=None, block_duration=None):
        self.start_datetime = timezone.now()
        self.samplerate = samplerate or self.samplerate
        self.filename = filename
        if os.path.exists(self.filename):
            raise AudioError('Error recording. File already exists! Got {}'.format(self.filename))
            return False
        self.block_duration = block_duration or 3600
        if self.status == READY:
            self.start_time = time.process_time()
            self.data = sd.rec(
                self.block_duration * self.samplerate,
                channels=self.channels)
            self.status = RECORDING
        return True

    def get_status(self):
        return self.status

    @property
    def ready(self):
        return True if self.status == READY else False

    @property
    def recording(self):
        return True if self.status == RECORDING else False

    @property
    def duration(self):
        return time.process_time() - self.start_time

    def stop(self):
        if self.status != RECORDING:
            raise AudioError('Cannot stop. Device is not recording. Current status is \'{}\''.format(self.status))
        else:
            sd.stop()
            self.stop_datetime = timezone.now()
            self.recording_time = self.duration
            self.status = 'done'

    def save(self, compress=None, reset=None):
        reset = True if reset is None else False
        if self.data.size > 0:
            self.stop()
            if compress:
                np.savez_compressed(self.filename, self.data)
            else:
                np.savez(self.filename, self.data)
        if reset:
            self.reset()

    def reset(self):
        self.recording_time = 0
        self.data = np.ndarray(0, dtype='float32')
        self.status = READY
        self.start_time = None
        self.filename = None

    def play(self):
        sd.play(self.data, self.samplerate)

    def load(self, filename):
        self.filename = filename
        self.status = 'file_loaded'
        self.data = np.load(filename).items()[0][1]
