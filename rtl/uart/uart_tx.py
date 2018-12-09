#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def uart_tx(clk_i, rst_i, tx_tick_i, dat_i, start_i, ready_o, tx_o):
	cnt = createSignal(0,4)  # Debe contar de 0 a 10
	data = createSignal(0,8) # Ancho del FIFO.
	tx_state = hdl.enum('IDLE','DATA') # 2 estados de la FSM.
	state = hdl.signal(tx_state.IDLE) # Estado inicial de estoy ocioso.
	cnt = hdl.signal(0)
	
	@hdl.always_seq(clk_i.posedge, reset=rst_i) # 50MHz
	def tx_state_m():
		if state == tx_state.IDLE:
			ready_o.next = 1
			if start_i: # Condición para cambiar de estado.
				data.next = dat_i
				ready_o.next = 0
				state.next = tx_state.DATA
			else:
				tx_o.next = 1 # No estoy transmitiendo

		elif state == tx_state.DATA: # Sifuiendo estructura rx
			if tx_tick_i: # Usando el divisor del clk_i
				if cnt => 1 and cnt <= 8
					tx_o.next    = data[0]
					data.next   = hdl.concat(0, data[8:1])
					cnt.next = cnt + 1
				else    cnt.next = cnt + 1
				
				if cnt == 9:
					if tx_tick_i:
						tx_o.next    = 1
						ready_o.next = 1
						state.next   = tx_state.IDLE
						
		else:
			state.next = tx_state.IDLE #Default

	return hdl.instances()


# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
