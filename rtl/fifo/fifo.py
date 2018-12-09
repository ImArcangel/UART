#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from rtl.fifo.ram_dp import RAM_DP
from coregen.utils import createSignal


@hdl.block
def FIFO(clk_i, rst_i, enqueue_i, dequeue_i, dat_i, dat_o, count_o, empty_o, full_o, A_WIDTH=8, D_WIDTH=8):
    assert len(dat_i) == D_WIDTH, "[FIFO] Error: Data width mismatch"
    assert len(dat_o) == D_WIDTH, "[FIFO] Error: Data width mismatch"
    assert len(count_o) == A_WIDTH + 1, "[FIFO] Error: Invalid width for signal 'count' = {}. Must be A_WIDTH + 1".format(len(A_WIDTH))

    _enqueue    = createSignal(0, 1)
    _dequeue    = createSignal(0, 1)
    _count      = createSignal(0, len(count_o))
    _empty      = createSignal(0, 1)
    _full       = createSignal(0, 1)
    enqueue_ptr = createSignal(0, A_WIDTH)
    dequeue_ptr = createSignal(0, A_WIDTH)
    ram_dat_o   = createSignal(0, D_WIDTH)
    ram         = RAM_DP(clk_i=clk_i, raddr_i=dequeue_ptr, waddr_i=enqueue_ptr, dat_i=dat_i, we_i=_enqueue, dat_o=ram_dat_o, A_WIDTH=A_WIDTH, D_WIDTH=D_WIDTH)  # noqa

    @hdl.always_comb
    def assign_output_ports_proc():
        count_o.next = _count
        empty_o.next = _empty
        full_o.next  = _full
        dat_o.next   = dat_i if _empty else ram_dat_o

    @hdl.always_comb
    def assign_flags_proc():
        _empty.next = _count == 0
        _full.next  = _count[A_WIDTH]

    @hdl.always_comb
    def assign_internals_proc():
        _enqueue.next = not _full and enqueue_i   # ignore if full
        _dequeue.next = not _empty and dequeue_i  # ignore if empty

    @hdl.always_seq(clk_i.posedge, reset=rst_i)
    def addr_ptr_proc():
        """ verilator lint_off WIDTH """
        enqueue_ptr.next = enqueue_ptr + _enqueue
        dequeue_ptr.next = dequeue_ptr + _dequeue
        _count.next      = _count + _enqueue - _dequeue
        """ verilator lint_on WIDTH """

    return hdl.instances()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
