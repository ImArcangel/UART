#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def uart_tx(clk_i, rst_i, tx_tick_i, dat_i, start_i, ready_o, tx_o):
	cnt = createSignal(0,4) # Contará de 0 a 9
	data = createSignal(0,8) # Ancho del FIFO
	tx_state = hdl.enum('IDLE','TX') # 2 estados de la FSM
	state = hdl.Signal(tx_state.IDLE) # Estado inicial de estoy ocioso
	

	@hdl.always_seq(clk_i.posedge, reset=rst_i)
	def tx_state_m(): # 50MHz
		if state == tx_state.IDLE:
			ready_o.next = 1
			if start_i: # Condición para cambiar de estado
				data.next = dat_i
				ready_o.next = 0
				state.next = tx_state.TX
			else:
				tx_o.next = 1

		elif state == tx_state.TX:
			if tx_tick_i: #Usando el divisor del clk_i
				if cnt >=1 and cnt <= 8:
					tx_o.next    = data[0]
					data.next   = hdl.concat(False, data[8:1])
					cnt.next = cnt + 1
				else: 
					tx_o.next = 0
					cnt.next = cnt + 1

				if cnt == 9:
						tx_o.next    = 1 
						ready_o.next = 1
						state.next   = tx_state.IDLE
						cnt.next = 0
						
		else:
			state.next = tx_state.IDLE

	return hdl.instances()


# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End: