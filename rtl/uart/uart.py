#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal
from rtl.uart.uart_tx import uart_tx
from rtl.uart.uart_rx import uart_rx
from rtl.uart.uart_clk import clk_div


@hdl.block
def UART(clk_i, rst_i,
         tx_dat_i, tx_start_i, tx_ready_o, tx_o,
         rx_dat_o, rx_ready_o, rx_i,
         CLK_BUS=50_000_000,
         BAUD_RATE=115200):
    rx_tick = createSignal(0, 1)
    tx_tick = createSignal(0, 1)
    clks    = clk_div(clk_i=clk_i, rst_i=rst_i, uart_tick=tx_tick, uart_tick_x8=rx_tick, CLK_BUS=CLK_BUS, BAUD_RATE=BAUD_RATE)  # noqa
    tx      = uart_tx(clk_i=clk_i, rst_i=rst_i, tx_tick_i=tx_tick, dat_i=tx_dat_i, start_i=tx_start_i, ready_o=tx_ready_o, tx_o=tx_o)  # noqa
    rx      = uart_rx(clk_i=clk_i, rst_i=rst_i, rx_tick_i=rx_tick, rx_i=rx_i, dat_o=rx_dat_o, ready_o=rx_ready_o)  # noqa

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
