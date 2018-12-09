#!/usr/bin/env python3
# Copyright (ten) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal


@hdl.block
def bin2bcd(clk_i, rst_i, binary_i, thousands_o, hundreds_o, tens_o, ones_o):
    assert len(binary_i) <= 14, "[bin2bcd] Error: max length of 'binary_i' is 14. Wrong value: {1}".format(len(binary_i))
    assert len(thousands_o) == 4, "[bin2bcd] Error: len(thousands_o) must be 4"
    assert len(hundreds_o) == 4, "[bin2bcd] Error: len(hundreds_o) must be 4"
    assert len(tens_o) == 4, "[bin2bcd] Error: len(tens_o) must be 4"
    assert len(ones_o) == 4, "[bin2bcd] Error: len(ones_o) must be 4"

    NBIT  = len(binary_i)
    shift = [createSignal(0, 16 + NBIT) for _ in range(NBIT + 1)]

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def decomp_proc():
        """ verilator lint_off WIDTH """
        shift[0].next  = binary_i
        for i in range(NBIT):
            thousand = shift[i][NBIT + 16:NBIT + 12] + 3
            hundred  = shift[i][NBIT + 12:NBIT + 8] + 3
            ten      = shift[i][NBIT + 8:NBIT + 4] + 3
            one      = shift[i][NBIT + 4:NBIT] + 3
            shift[i + 1].next = hdl.concat(shift[i][NBIT + 16:NBIT + 12] if shift[i][NBIT + 16:NBIT + 12] < 5 else hdl.modbv(thousand)[4:],
                                           shift[i][NBIT + 12:NBIT + 8] if shift[i][NBIT + 12:NBIT + 8] < 5 else hdl.modbv(hundred)[4:],
                                           shift[i][NBIT + 8:NBIT + 4] if shift[i][NBIT + 8:NBIT + 4] < 5 else hdl.modbv(ten)[4:],
                                           shift[i][NBIT + 4:NBIT] if shift[i][NBIT + 4:NBIT] < 5 else hdl.modbv(one)[4:],
                                           shift[i][NBIT:]) << 1
        """ verilator lint_on WIDTH """

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def assign_proc():
        thousands_o.next = shift[NBIT][NBIT + 16:NBIT + 12]
        hundreds_o.next  = shift[NBIT][NBIT + 12:NBIT + 8]
        tens_o.next      = shift[NBIT][NBIT + 8:NBIT + 4]
        ones_o.next      = shift[NBIT][NBIT + 4:NBIT]

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
