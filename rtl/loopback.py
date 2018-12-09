#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from rtl.uart.uart import UART
from rtl.fifo.fifo import FIFO
from rtl.driver7seg import driver7seg
from coregen.utils import createSignal
from coregen.utils import log2up


@hdl.block
def Loopback(clk_i, rst_i, rx_i, tx_o, anodos_o, segmentos_o, FIFO_DEPTH=1024, CLK_BUS=50_000_000, BAUD_RATE=115200):
    """
    Escriba su código acá
    """
    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
