#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.coregen import Coregen
from coregen.boards import Spartan3sb
from rtl.loopback import Loopback
from coregen.toolflow.platform import Port
from coregen.toolflow.platform import ResetPort


def main():
    io = dict(clk_i=Port('T9', 'LVTTL'),
              rst_i=ResetPort('L14', 'LVTTL', val=0, active=True, isasync=False),
              rx_i=Port('T13', 'LVTTL'),
              tx_o=Port('R13', 'LVTTL'),
              anodos_o=Port('D14 G14 F14 E13', 'LVTTL'),
              segmentos_o=Port('P16 N16 F13 R16 P15 N15 G13 E14', 'LVTTL'))
    params = dict(BAUD_RATE=115200,
                  FIFO_DEPTH=500,
                  CLK_BUS=Spartan3sb.Platform.default_clk_freq)
    board   = Spartan3sb.Platform(module=Loopback, io=io, params=params)
    Coregen(board).run()


if __name__ == '__main__':
    main()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
