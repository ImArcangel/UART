#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.boards.xilinx import Xula2
from coregen.boards.xilinx import Spartan3sb

xboards = dict(xula2=Xula2, spartan3=Spartan3sb)


def get_board(name):
    if name in xboards:
        return xboards[name]
    else:
        raise ValueError("Invalid board: {board}".format(board=name))


def get_board_list():
    return list(xboards.keys())

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
