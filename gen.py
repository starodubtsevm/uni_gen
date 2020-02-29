#!/usr/bin/env python3
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

import sounddevice as sd
import sys
import queue
import numpy as np

#---------------------------------------------------------------------------
class gen_device(object):
	''' Class for create ouput signal '''

	def __audio_callback (self,indata, outdata, frames, time, status):
		"""callback function"""

		data_stereo =[]
		data = []
		data_krl = []
		data_alsn  = []
		data_alsen  = []
		data_ars  = []

		if status:
			print(status, file=sys.stderr)
		t = (self.start_idx + np.arange(frames)) / (sd.default.samplerate)

#--формирование данных для генерации-----------------------------------------
		data_krl    = self.proc_krl(t)
		data_alsn   = self.proc_alsn(t)
		data_ars    = self.proc_ars(t)
		#data_alsen = self proc_alsen(t)

		data = np.asarray(data_krl)\
		 	+ np.asarray(data_alsn) + np.asarray(data_ars)

		#data_stereo = np.column_stack([data_krl, data_krl])
		data_stereo = np.column_stack([data, data])
		self.start_idx += frames
#--передача-потока на аудиовыход--------------------------------------------
		outdata[::] = data_stereo

#--прием потока с микрофоного входа-----------------------------------------

		self.q.put(indata[::self.downsample, self.mapping])
#---------------------------------------------------------------------------

	def __init__(self):
		"""initialization"""
		self.mode = "krl"
		self.data_in = []
		self.count_krl = 0
		self.num_bit = 0
		self.krl_freq = 475
		self.krl_ampl = 0.1
		self.krl_code = 0x2C
		self.krl_fdev = 11
		for j in range(7, -1, -1):
				self.data_in.append((self.krl_code & 1<<j)>>j)

		self.count_alsn = 0
		self.alsn_freq = 50
		self.alsn_ampl = 0.1
		self.alsn_code = "RedYellow"
		self.alsn_green = {
							'pause1': 0.03,
							'pulse1': 0.38,
							'pause2': 0.5,
							'pulse2': 0.72,
							'pause3': 0.84,
							'pulse3': 1.06
							}
		self.alsn_yellow = {
							'pause1': 0.03,
							'pulse1': 0.41,
							'pause2': 0.53,
							'pulse2': 0.91,
							}
		self.alsn_redyellow = {
							'pulse1': 0.23,
							'pause1': 0.80
							}

		self.count_alsen = 0
		self.alsen_freq = 175
		self.alsen_ampl = 0.1
		self.alsen_data = [0,0]

		self.count_ars = 0
		self.ars_freq = 75
		self.ars_ampl = 0.1
		self.sao = False
		self.sao_param = {
							'pulse1': 0.5,
							'pause1': 1.0
						}

		self.downsample = 1
		self.start_idx = 0
		self.channels = [1,2]
		self.fs = 16000
		self.bs = 1024
		sd.default.blocksize = self.bs
		sd.default.samplerate = self.fs
		sd.default.channels = 2
		self.q = queue.Queue()
		self.generator = sd.Stream(device = (sd.default.device, sd.default.device),
									callback = self.__audio_callback)
#		self.generator.start()
		self.mapping = [c - 1 for c in self.channels] 


	def proc_krl(self,t):
		''' формирование сигнала КРЛ '''

		data_krl  = []

		for i in range(len(t)):
			if self.data_in[self.num_bit] == 1:
				f_cur = self.krl_freq + self.krl_fdev
			else:
				f_cur = self.krl_freq - self.krl_fdev
			data_krl.append(self.krl_ampl*np.sin(2*np.pi*f_cur*t[i]))
			self.count_krl+= 1.0/self.fs
			if self.count_krl >= 1.0/self.krl_fdev:
				self.count_krl = 0
				self.num_bit+= 1
				if self.num_bit > 7:
					self.num_bit = 0
		return data_krl

	def proc_alsn(self,t):
		''' формирование сигнала АЛСН '''

		data_alsn  = []

		if	self.alsn_code not in ("Green","Yellow","RedYellow"):
			self.alsn_code = None

		for i in range(len(t)):
			self.count_alsn+= 1.0/self.fs

			if self.alsn_code == "Green":
				if (self.count_alsn <= self.alsn_green['pause1']):
					alsn_on = 0

				elif (self.count_alsn > self.alsn_green['pause1']) &\
						 (self.count_alsn <= self.alsn_green['pulse1']):
					alsn_on = 1

				elif (self.count_alsn > self.alsn_green['pulse1']) &\
						 (self.count_alsn <= self.alsn_green['pause2']):
					alsn_on = 0

				elif (self.count_alsn > self.alsn_green['pause2']) &\
				(self.count_alsn <= self.alsn_green['pulse2']):
					alsn_on = 1

				elif (self.count_alsn > self.alsn_green['pulse2']) &\
				(self.count_alsn <= self.alsn_green['pause3']):
					alsn_on = 0

				elif (self.count_alsn > self.alsn_green['pause3']) &\
				(self.count_alsn <= self.alsn_green['pulse3']):
					alsn_on = 1

				elif (self.count_alsn > self.alsn_green['pulse3']):
					alsn_on = 0
					self.count_alsn = 0
					
			elif self.alsn_code == "Yellow":
				if (self.count_alsn <= self.alsn_yellow['pause1']):
					alsn_on = 0

				elif (self.count_alsn > self.alsn_yellow['pause1']) &\
						 (self.count_alsn <= self.alsn_yellow['pulse1']):
					alsn_on = 1

				elif (self.count_alsn > self.alsn_yellow['pulse1']) &\
						 (self.count_alsn <= self.alsn_yellow['pause2']):
					alsn_on = 0

				elif (self.count_alsn > self.alsn_yellow['pause2']) &\
				(self.count_alsn <= self.alsn_yellow['pulse2']):
					alsn_on = 1
					self.count_alsn = 0

			elif self.alsn_code == "RedYellow":
				if (self.count_alsn <= self.alsn_redyellow['pulse1']):
					alsn_on = 1

				elif (self.count_alsn > self.alsn_redyellow['pulse1']) &\
						 (self.count_alsn <= self.alsn_redyellow['pause1']):
					alsn_on = 0

				elif (self.count_alsn > self.alsn_redyellow['pause1']):
					self.count_alsn = 0
					alsn_on = 0
			else:
				alsn_on = 1

			data_alsn.append(alsn_on*self.alsn_ampl*\
									np.sin(2*np.pi*self.alsn_freq*t[i]))
		return data_alsn

	def proc_ars(self,t):
		''' формирование сигнала АРС '''

		data_ars = []
		ars_on = 1
		for i in range(len(t)):
			self.count_ars+= 1.0/self.fs
			if self.sao == True:
				if (self.count_ars <= self.sao_param['pulse1']):
					ars_on = 1
				elif (self.count_ars > self.sao_param['pulse1']) &\
						 (self.count_ars <= self.sao_param['pause1']):
					ars_on = 0
				elif (self.count_ars > self.sao_param['pause1']):
					ars_on = 0
					self.count_ars = 0

			data_ars.append(ars_on*self.ars_ampl*\
									np.sin(2*np.pi*self.ars_freq*t[i]))
		return data_ars

	def proc_alsen(self, t, alsen_data):
		''' формирование сигнала АЛСЕН '''

		data_alsen = []
		for i in range(len(t)):
			self.count_ars+= 1.0/self.fs

		return data_alsen


	def update_plot(self,frame):
		"""This is called by matplotlib for each plot update.
		Typically, audio callbacks happen more frequently than plot updates,
		therefore the queue tends to contain multiple blocks of audio data.
		"""
		global plotdata
		global lines

		while True:
			try:
				data = self.q.get_nowait()
			except queue.Empty:
				break

			shift = len(data)

			plotdata = np.roll(plotdata, -shift, axis=0)
			plotdata[-shift:, :] = data

		for column, line in enumerate(lines):
			line.set_ydata(plotdata[:, column])
		return lines
	
	def plotting(self,samplerate):
		''' '''
		global plotdata
		global lines
		global data_mean

		length = int(1500 * samplerate / (1000 * self.downsample))
		plotdata = np.zeros((length, len(self.channels)))
		fig, ax = plt.subplots()
		lines = ax.plot(plotdata)
		if len(self.channels) > 1:
			ax.legend(['channel {}'.format(c) for c in self.channels],
				loc='lower left', ncol=len(self.channels))
		ax.axis((0, len(plotdata), -1.0, 1.0))
		ax.set_xlabel('время')
		ax.set_ylabel('амплитуда, уе')
		plt.title("Входной сигнал")
		ax.yaxis.grid(True)
		ax.tick_params(bottom=True, top=False, labelbottom=True,
				right=False, left=True, labelleft=True)

		return fig

	def start_plot(self):
		''' '''
		self.figure = self.plotting(self.fs)
		ani = FuncAnimation(self.figure, self.update_plot, interval = 50, blit = True)
		plt.show()
