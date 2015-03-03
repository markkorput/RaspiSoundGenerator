import numpy as np
import pygame as pg

class SineSound:
  """SineSound"""
  def __init__(self, frequency=300, gain=0.1, samplerate=44100, channels=1, bits=16):
    self.freq = frequency
    self.gain = gain
    self.samplerate = samplerate
    self.channels = channels
    self.bits = bits
    self.sound = None    
    pg.mixer.pre_init(self.samplerate, -self.bits, self.channels)
    pg.init()

  def start(self):
    if self.sound == None:
      self.sound = self.mkSine(self.freq, self.gain, self.samplerate, self.channels)
    self.sound.play(-1)

  def change(self, frequency=300, gain=0.1):
    self.freq = frequency
    self.gain = gain
    newSound = self.mkSine(self.freq, self.gain, self.samplerate, self.channels)
    pg.mixer.stop()
    self.sound = newSound
    self.sound.play(-1)

  def mkSine(self, freq=1000, peak=0.1, samplerate=44100, nchannels=1):
    wavelen = 0.0
    if( freq != 0.0 ):
      wavelen = 1.0/freq
    wavesize = wavelen * samplerate

    sinusoid = (2**15 - 1) * np.sin(2.0 * np.pi * freq * np.arange(0, wavesize) / float(samplerate)) * peak
    samples = np.array(sinusoid, dtype=np.int16)
    if(nchannels > 1):
      samples = np.tile(samples, (nchannels, 1)).T
    return pg.sndarray.make_sound(samples)

