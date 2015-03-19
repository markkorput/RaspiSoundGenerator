class StrpConfig:
  def __init__(self):
    self.rotaryA = 17 #26 #15
    self.rotaryB = 18 #21 #14
    self.touchOutPins = [27,23,5,13] #[18,22,27,6,19]
    self.touchInPins = [22,24,6,19] #[17,23,13,12,16] 
    self.rotaryFreqStep = 0.0 # how much the rotary affects frequency (make negative to reverse the direction)
    self.rotaryGainStep = 0.0 # how much the rotary affects the gain (make negative to reverse the direction)
    self.rotaryPosStep = 0.1 # how much the rotary affects the frequency sine-wave affector (make negative to reverse the direction)
    self.posAffectGain = True
    self.posAffectFreq = False
    self.touchFreqs = [100.0, 100.0, 70.0, 130.0, 55.0, 60.0]# [130.0, 130.0, 110.0, 120.0, 140.0,  130.0, 130.0,130.0,130.0]
    self.freqMin = 50.0
    self.freqMax = 150.0
    self.defaultFreq = 100.0
    self.initialActiveGainMin = 0.50 # min gain on initial touch
    self.noTouchDelay = 1.0
    self.startSounds = [] # ['audio/sweep01.wav']
    # max interaction
    self.maxInteraction = 60.0
    self.minIdle = 5.0 # time of enforced idle after max activity
    # monitor
    self.maxIdle = 400.0 # time the fluids are allowed to lay idle
    self.activateDuration = 90.0
    self.mixingAudio = 'audio/mixSoundtrack.wav'
    self.activateGain = 0.8
    self.idleLimit = 0.2 # minimum gain level at which fluids stay mixed
    self.activeMinGain = 0.5
    self.activeMaxGain = 1.3
    self.affectorAmp = 10.0
    self.affectorSpeed = 0.1

# end of class StrpConfig
