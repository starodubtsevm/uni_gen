import numpy as np
import matplotlib.pyplot as plt
from alsen_rx import*
from alsen_gen import*

fs = 16000
Code_alsen1 = 10
Code_alsen2 = 11
t = np.arange(0., 2.0, 1/fs)

res = []
res2 =[]
sig = []

sig = proc_alsen(fs, len(t), Code_alsen1, Code_alsen2)

rx = alsen_rx()

for i in range (len(t)):

   gen0, gen90 = rx.local_gen(t)
   y0_aftermux1, y90_aftermux1 = rx.mux1(gen0, gen90, sig[i], sig[i])
   y0_afterlpf1,y90_afterlpf1 = rx.lpf1(y0_aftermux1, y90_aftermux1)

   res.append(y0_afterlpf1)
   res2.append(y90_afterlpf1)

ax1 = plt.subplot(511)
ax2 = plt.subplot(512, sharex=ax1)
ax3 = plt.subplot(513, sharex=ax1, sharey=ax1)
ax4 = plt.subplot(514, sharex=ax1, sharey=ax1)
ax5 = plt.subplot(515, sharex=ax1, sharey=ax1)

ax1.plot(t,sig)
ax1.grid(True)

ax2.plot(t,res)
ax2.plot(t,res2)
ax2.grid(True)

#ax3.plot(res2)
ax3.grid(True)

plt.show()

