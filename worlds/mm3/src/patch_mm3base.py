from subprocess import run
import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))

mm3 = bytearray(open("Mega Man 3 (USA).nes", 'rb').read())
mm3[0x3C000:0x3C000] = [0] * 0x4000
mm3[0x4] = 0x11 #have to do it here, because we don't this in the basepatch itself
open("mm3_basepatch.nes", 'wb').write(mm3)
