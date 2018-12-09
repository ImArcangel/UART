#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def uart_tx(clk_i, rst_i, tx_tick_i, dat_i, start_i, ready_o, tx_o):
    """
    Escriba su código acá
    """
    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
