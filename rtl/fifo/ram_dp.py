#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def RAM_DP(clk_i, raddr_i, waddr_i, dat_i, we_i, dat_o, A_WIDTH=8, D_WIDTH=8):
    """
    Dual-port RAM
    """
    _ram = [createSignal(0, D_WIDTH) for _ in range(2**A_WIDTH)]

    @hdl.always(clk_i.posedge)
    def ram_proc():
        if we_i:
            _ram[waddr_i].next = dat_i
        dat_o.next = _ram[raddr_i]

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
