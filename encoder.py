from myhdl import *

def encoder(clk,reset,
		S,A,B,
		VALUE
	):
	
	#0 -> lin, 1 -> log
	linORlog = Signal(False)

	CLKFREQ = 12000000
	COUNTERMAX = (CLKFREQ // 2000) - 1
	counter = Signal(intbv(0,min = 0, max = COUNTERMAX))

	@always_seq(clk.posedge,reset=reset)
	def debouncer():
		if S == False:
			counter.next = 0
		else:
			counter.next = counter + 1
			if counter == COUNTERMAX - 1:
				linORlog.next = not linORlog
			else:
				linORlog.next = linORlog

	@always_seq(A.posedge,reset=reset)
	def counter():
		if B == 0:
			#we're moving cw
			if linORlog:
				VALUE.next = VALUE << 1
			else:
				VALUE.next = VALUE + 1
		else:
			#we're moving ccw
			if linORlog:
				VALUE.next = VALUE >> 1
			else:
				VALUE.next = VALUE - 1

	return counter, debouncer