N =20000
imp_duty_count = 0
count_bit = 8
Code_alsen1 = 10
Code_alsen2 = 11
Byte1 = Code_alsen1
Byte2 = Code_alsen2
diBit = 0
phase = 0
d_phase = 0

for i in range(N):

      if imp_duty_count < int((1/13.89)/(1/16000)):
         imp_duty_count=imp_duty_count+1
      else:
         imp_duty_count=0
         diBit=((Byte1 & 0x80)>> 6)+((Byte2 & 0x80)>>7)

         if diBit == 0:
            d_phase = 0
            print("phase +0")
         if diBit == 1:
            d_phase = 90
            print("phase +90")
         if diBit == 3:
            d_phase = 180
            print("phase +180")
         if diBit == 2:
            d_phase = 270
            print("phase +270")
         phase = phase + d_phase
         print(diBit, d_phase, phase)
         Byte1=Byte1<<1
         Byte2=Byte2<<1

         count_bit=count_bit-1
         if count_bit==0:
            count_bit=8
            Byte1=Code_alsen1
            Byte2=Code_alsen2

