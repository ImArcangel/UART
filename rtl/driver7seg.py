#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from rtl.bin2bcd import bin2bcd
from coregen.utils import log2up
from coregen.utils import createSignal


@hdl.block
def driver7seg(clk_i, rst_i, value_i, anodos_o, segmentos_o, CLK_BUS=50_000_000):
    assert len(anodos_o) == 4, "[driver7seg] Error: longitud de anodos_o debe ser 4. Valor actual: {0}".format(len(anodos_o))
    assert len(segmentos_o) == 8, "[driver7seg] Error: longitud de segmentos_o debe ser 8. Valor actual: {0}".format(len(segmentos_o))

    FREQ_AN     = 240
    MAX_CNT_AN  = CLK_BUS // FREQ_AN
    counter     = createSignal(0, log2up(MAX_CNT_AN))
    tick        = createSignal(0, 1)
    anodos      = createSignal(1, len(anodos_o))
    thousand    = createSignal(0, 4)
    hundred     = createSignal(0, 4)
    ten         = createSignal(0, 4)
    one         = createSignal(0, 4)
    segment_ROM = (0x03, 0x9f, 0x25, 0x0d, 0x99, 0x49, 0x41, 0x1f,
                   0x01, 0x09, 0x11, 0xc1, 0x63, 0x85, 0x61, 0x71)
    b2b         = bin2bcd(clk_i=clk_i, rst_i=rst_i, binary_i=value_i, thousands_o=thousand, hundreds_o=hundred, tens_o=ten, ones_o=one)  # noqa

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def cnt_anodos_proc():
        if counter == MAX_CNT_AN - 1:
            counter.next = 0
            tick.next    = True
        else:
            counter.next = counter + 1
            tick.next    = False

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def anodos_proc():
        if tick:
            anodos.next = hdl.concat(anodos[3:0], anodos[3])

    @hdl.always_comb
    def segmentos_proc():
        anodos_o.next = anodos
        if anodos == 0b0001:
            segmentos_o.next = segment_ROM[one]
        elif anodos == 0b0010:
            segmentos_o.next = segment_ROM[ten]
        elif anodos == 0b0100:
            segmentos_o.next = segment_ROM[hundred]
        elif anodos == 0b1000:
            segmentos_o.next = segment_ROM[thousand]
        else:
            segmentos_o.next = 0xFF

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
