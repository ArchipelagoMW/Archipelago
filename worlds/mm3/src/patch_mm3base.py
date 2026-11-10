import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

mm3 = bytearray(open("Mega Man 3 (USA).nes", 'rb').read())
mm3[0x3C010:0x3C010] = [0] * 0x40000
mm3[0x4] = 0x20  # have to do it here, because we don't this in the basepatch itself
open("mm3_basepatch.nes", 'wb').write(mm3)
