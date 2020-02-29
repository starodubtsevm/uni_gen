#!/usr/bin/env python3
from gen import *

#---------------------------------------------------------------------------

gks = gen_device()

gks.krl_freq   = 625
gks.krl_ampl   = 0.0
gks.krl_code   = 0x2C
gks.krl_fdev   = 11

gks.alsn_freq  = 500
gks.alsn_ampl  = 0.0
gks.alsn_code  = "Yellow"

gks.alsen_freq = 175
gks.alsen_ampl = 0.0
gks.alsen_data = [0,0]

gks.ars_freq   = 325
gks.ars_ampl   = 0.5
gks.sao        = False

input("Press to start the generator ")

gks.generator.start()
gks.start_plot()

input("Press to stop the generator & exit")

gks.generator.stop()

#---------------------------------------------------------------------------
