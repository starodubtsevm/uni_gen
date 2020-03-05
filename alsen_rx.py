import numpy   as np
from config import*

class alsen_rx(object):
   '''Приемник сигналов АЛСЕН'''
   def __init__(self):
      '''Инициализация'''
      self.fs = 16000
      self.Fcar = 174.89 # несущая АЛС-ЕН
      self.A = 1
      self.k = 2 * np.cos(2 * np.pi * self.Fcar / self.fs)

      self.X0_0 = 0
      self.X1_0 = 0
      self.X2_0 = self.A * np.sin(2 * np.pi * self.Fcar / self.fs)

      self.X0_90 = 0
      self.X1_90 = 0
      self.X2_90 = self.A * np.sin(2 * np.pi * self.Fcar / self.fs)
      self.cycle_count = 0

      self._data0 = []
      self._data90 = []
      self._buff_size = (1/11)/(1/self.fs)

      self.index= 0
      self.h = h
      self.size= len(h)

   def local_gen(self,t):
      '''Локальный генератор cos и sin'''
      self.cycle_count = self.cycle_count + 1

      self.X0_0 = self.k*self.X1_0-self.X2_0
      y_0 = self.X0_0
      self.X2_0 = self.X1_0
      self.X1_0 = self.X0_0

      if self.cycle_count > 23:
         self.X0_90 = self.k*self.X1_90-self.X2_90
         y_90 = self.X0_90
         self.X2_90=self.X1_90
         self.X1_90=self.X0_90
         self.cycle_count = 24
      else:
         y_90 = 0

      return y_0, y_90

   def mux1(self,gen0,gen90,x0,x90):
      '''Входные перемножители'''
      y0 = x0 * gen0
      y90 = x90 * gen90

      return y0, y90

   def lpf1(self,x0,x90):
      '''ФНЧ (интегратор на периоде длительности посылки)'''

      acc0 = 0   # accumulator
      acc90 = 0
      indx = 0

      for j in range (self.size):
         acc0 = acc0  + x0 * self.h[j]
         acc90= acc90 + x90 * self.h[j]
         if indx == ((self.size)-1):
            indx = 0
         else:
            indx += 1

      return acc0, acc90 # result to 16 bit value

   def diff_decode(self,x0,x90):
      '''Дифференциальный декодер'''
      y1 = 0
      y2 = 0

      return y1, y2

   def delay_T(self,x0,x90):
      '''Задержка сигнала на длительность посылки'''
      self._data0.insert(0,x0)
      self._data0.pop()
      y0 = self._data0[self._buff_size-1]

      self._data90.insert(0,x90)
      self._data90.pop()
      y90 = self._data90[self._buff_size-1]

      return y0, y90

   def decim(self,x0,x90):
      '''Прореживание'''
      if self.count_dec > 10:
          y0 = x0

      return 0

