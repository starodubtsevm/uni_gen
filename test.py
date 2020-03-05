N =20000
imp_duty_count = 0
count_bit = 8
Code_alsen1 = 0
Code_alsen2 = 16
Byte1 = Code_alsen1
Byte2 = Code_alsen2

for i in range(N):

      if imp_duty_count < int((1/13.89)/(1/16000)):
         imp_duty_count=imp_duty_count+1
      else:
         imp_duty_count=0
         if count_bit==0:
            count_bit=8
            Byte1=Code_alsen1
            Byte2=Code_alsen2
         diBit=((Byte1 & 0x80)>> 6)+((Byte2 & 0x80)>>7)
         print (diBit,count_bit)
         Byte1=Byte1<<1
         Byte2=Byte2<<1
         count_bit=count_bit-1
         diBit = 0

