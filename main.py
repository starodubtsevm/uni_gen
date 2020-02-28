#!/usr/bin/env python3

from classes import *

#---------------------------------------------------------------------------
#afc1 = afc_device(amplitude,frequency,blocksize,samplerate,
#	freq_min,freq_max,freq_step,time_conv)
afc1 = gen_device(time_conv = 0.5, freq_max = 1000)

#fsk1 = fsk_gen(525,235*0,0x2c)	# source fsk signal
input("Press Enter to exit")
#---------------------------------------------------------------------------
