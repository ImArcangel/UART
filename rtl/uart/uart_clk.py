#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal
from coregen.utils import log2up


@hdl.block
def clk_div(clk_i, rst_i, uart_tick, uart_tick_x8, CLK_BUS=50000000, BAUD_RATE=115200):
    MULTX     = 8
    _divisor8 = CLK_BUS // (BAUD_RATE * MULTX)
    counter   = createSignal(0, log2up(MULTX))
    counter8  = createSignal(0, log2up(_divisor8))

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def counter_proc():
        if counter8 == 0:
            counter.next = counter + 1

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def counter16_proc():
        if counter8 == _divisor8 - 1:
            counter8.next = 0
        else:
            counter8.next = counter8 + 1

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def uart_tick_proc():
        uart_tick_x8.next = counter8 == 0
        uart_tick.next    = counter == 0 and uart_tick_x8

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
