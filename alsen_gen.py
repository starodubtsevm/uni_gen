# -*- coding: utf-8 -*-                                                
# ver. 1.0
#*-------------------------------------------------------------
import numpy as np

def proc_alsen(Fs, N, Code_alsen1, Code_alsen2):

   Fcar = 174.89 # несущая АЛС-ЕН

   A = 1
   k = 2 * np.cos(2 * np.pi * Fcar / Fs)
   X0_0 = 0
   X1_0 = 0
   X2_0 = A * np.sin(2 * np.pi * Fcar / Fs)

   X0_90 = 0
   X1_90 = 0
   X2_90 = A * np.sin(2 * np.pi * Fcar / Fs)

   X0_180 = 0
   X1_180 = 0
   X2_180 = A * np.sin(2 * np.pi * Fcar / Fs)

   X0_270 = 0
   X1_270 = 0
   X2_270 = A * np.sin(2 * np.pi * Fcar / Fs)

   y_0   = []
   y_90  = []
   y_180  =[]
   y_270 = []
   y_res = []
   y_test = []

   cycle_count = 0 
   diBit = 0
   count_bit = 8
   Byte1 = Code_alsen1
   Byte2 = Code_alsen2
   imp_duty_count = 0
   temp = []

   for i in range(N):

      if imp_duty_count <= int((1/13.89)/(1/16000)):
         imp_duty_count=imp_duty_count+1
         temp.append(0)

      else:
         temp.append(1)
         imp_duty_count=0
         diBit=((Byte1 & 0x80)>> 6)+((Byte2 & 0x80)>>7)
         print(diBit,Byte1,Byte2)
         Byte1=Byte1<<1
         Byte2=Byte2<<1

         count_bit=count_bit-1
         if count_bit==0:
            count_bit=8
            Byte1=Code_alsen1
            Byte2=Code_alsen2

      X0_0=k*X1_0-X2_0
      y_0.append(X0_0)
      X2_0=X1_0
      X1_0=X0_0

      cycle_count= cycle_count+1

      if cycle_count > 23:
         X0_90=k*X1_90-X2_90
         y_90.append(X0_90)
         X2_90=X1_90
         X1_90=X0_90
      else:
         y_90.append(0)

      if cycle_count > 46:
         X0_180=k*X1_180-X2_180
         y_180.append(X0_180)
         X2_180=X1_180
         X1_180=X0_180
      else:
         y_180.append(0)

      if cycle_count > 69:
         X0_270=k*X1_270-X2_270
         y_270.append(X0_270)
         X2_270=X1_270
         X1_270=X0_270
      else:
         y_270.append(0)

      if diBit == 0: 
         y_res.append(X0_0)
         #print("phase 0")
      if diBit == 1: 
         y_res.append(X0_90)
         #print("phase 90")
      if diBit == 3: 
         y_res.append(X0_180)
         #print("phase 180")
      if diBit == 2: 
         y_res.append(X0_270)
        # print("phase 270")

   return y_res,temp
