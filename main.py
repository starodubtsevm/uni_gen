import numpy as np
import matplotlib.pyplot as plt
from alsen_rx import*
from alsen_gen import*
from comparator import*

fs = 16000
Code_alsen1 = 0
Code_alsen2 = 16
t = np.arange(0.0, 2, 1/fs)

res0 =[]
res90 =[]
res = []
res2 =[]
res3 =[]
res4 =[]
res11=[]
res12=[]
res13=[]
res14=[]
sig =[]

sig = proc_alsen(fs, len(t), Code_alsen1, Code_alsen2)

flt_iir1 = IIR2Filter(2, [26], 'low',design='cheby1',rs = 1, fs=fs)
flt_iir2 = IIR2Filter(2, [26], 'low',design='cheby1',rs = 1, fs=fs)
rx = alsen_rx()
comp0 = comparator(-0.1,0.1, 1)
comp90 = comparator(-0.1,0.1, 1)

for i in range (len(t)):

   gen0, gen90 = rx.local_gen(t)
   y0_aftermux1, y90_aftermux1 = rx.mux1(gen0, gen90, sig[i])
   y0_afterlpf1 = flt_iir1.filter(y0_aftermux1)
   y90_afterlpf1 = flt_iir2.filter(y90_aftermux1)

   y7,y8 = rx.diff_decode(y0_afterlpf1, y90_afterlpf1)
   y9 = comp0.proc(y7)
   y10 = comp90.proc(y8)

   res0.append(gen0)
   res90.append(gen90)
   res11.append(y0_aftermux1)
   res12.append(y90_aftermux1)
   res.append(y0_afterlpf1)
   res2.append(y90_afterlpf1)
   res3.append(y7)
   res4.append(y8)
   res13.append(y9)
   res14.append(y10)

ax1 = plt.subplot(311)
ax2 = plt.subplot(312, sharex=ax1)
ax3 = plt.subplot(313, sharex=ax1, sharey=ax2)

ax1.plot(t,sig)
ax1.grid(True)

ax2.plot(t,res3)
ax2.plot(t,res13)
ax2.grid(True)

ax3.plot(t,res4)
ax3.plot(t,res14)
ax3.grid(True)

plt.show()

