class StrpConfig:
  def __init__(self):
    self.rotaryA = 17 #26 #15
    self.rotaryB = 18 #21 #14
    self.touchOutPins = [22] #[18,22,27,6,19]
    self.touchInPins = [23] #[17,23,13,12,16] 
    self.rotaryFreqStep = 0.0 # how much the rotary affects frequency (make negative to reverse the direction)
    self.rotaryGainStep = 0.0 # how much the rotary affects the gain (make negative to reverse the direction)
    self.rotaryFreqPosStep = 0.1 # how much the rotary affects the frequency sine-wave affector (make negative to reverse the direction)
    self.freqMin = 100.0
    self.freqMax = 150.0
    self.initialActiveGainMin = 0.2 # min gain on initial touch
    self.noTouchDelay = 1.0

    self.startSounds = ['audio/sweep01.wav']

# end of class StrpConfig
