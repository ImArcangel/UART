#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def uart_tx(clk_i, rst_i, tx_tick_i, dat_i, start_i, ready_o, tx_o):
	cnt = createSignal(0,3)
	data = createSignal(0,8)
	tx_state = hdl.enum('IDLE','DATA')
	state = hdl.signal(tx_state.IDLE)

	@hdl.always_seq(clk_i.posedge, reset=rst_i)
	def tx_state_m():
		if state == tx_state.IDLE:
			ready_o.next = 1
			if start_i:
				data.next = dat_i
				ready_o.next = 0
				state.next = tx_state.DATA
			else:
				tx_o.next = 1

		elif state == tx_state.DATA:
			if tx_tick_i:
				tx_o.next    = data[0]
				data.next   = hdl.concat(0, data[8:1])
				cnt.next = cnt + 1
				if cnt == 7:
					if tx_tick_i:
						tx_o.next    = 1
						ready_o.next = 1
						state.next   = tx_state.IDLE
						
		else:
			state.next = tx_state.IDLE

	return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
