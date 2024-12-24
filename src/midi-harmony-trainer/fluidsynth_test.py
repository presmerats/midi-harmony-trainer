import time
import fluidsynth

fs = fluidsynth.Synth()
#fs.start(driver='coreaudio')
fs.start(device = 'hw:0',driver='coreaudio')  
# on Windows, use "driver = 'dsound'"

sfid = fs.sfload('./external/FluidR3_GM.sf2')  # replace path as needed
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(3.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)