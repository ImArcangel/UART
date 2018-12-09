#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import os
import myhdl as hdl
from coregen.utils import createSignal
from rtl.loopback import Loopback

# Constantes
CLK_XTAL    = 12_000_000
BAUD        = 115200
TXRX_DATA   = [ord(i) for i in "Hello world! :D\n"]
TIMEOUT     = int(3 * (12 * len(TXRX_DATA) / BAUD) * CLK_XTAL)  # 12 symbols x char. Worst case: 3 times the message
TICK_PERIOD = 2
RESET_TIME  = 5
TRACE       = True


@hdl.block
def clk_n_timeout(clk, rst):
    @hdl.always(hdl.delay(int(TICK_PERIOD / 2)))
    def gen_clock():
        clk.next = not clk

    @hdl.instance
    def timeout():
        rst.next = True
        yield hdl.delay(RESET_TIME * TICK_PERIOD)
        rst.next = False
        yield hdl.delay(TIMEOUT * TICK_PERIOD)
        raise hdl.Error("Test failed: TIMEOUT at {0}. Clock cycles: {1}".format(hdl.now(), hdl.now() // TICK_PERIOD))

    return hdl.instances()


@hdl.block
def loopback_testbench(fdepth):
    assert fdepth >= len(TXRX_DATA), "Error: FIFO depth = {0}. Size of test data: {1}".format(fdepth, len(TXRX_DATA))
    clk       = createSignal(0, 1)
    rst       = hdl.ResetSignal(0, active=True, isasync=False)
    rx        = createSignal(1, 1)
    tx        = createSignal(0, 1)
    anodos    = createSignal(0, 4)
    segmentos = createSignal(0, 8)
    clk_tout  = clk_n_timeout(clk, rst)  # noqa
    dut       = Loopback(clk_i=clk, rst_i=rst, rx_i=rx, tx_o=tx, anodos_o=anodos, segmentos_o=segmentos,  # noqa
                         FIFO_DEPTH=fdepth, CLK_BUS=CLK_XTAL, BAUD_RATE=BAUD)
    rx_data   = createSignal(0, 8)
    rx_buffer = []

    cmd1 = 'iverilog -o build/dut.o build/dut.v build/tb_dut.v'
    cmd2 = 'vvp -v -m myhdl build/dut.o'
    os.makedirs('./build/', exist_ok=True)
    dut.convert(path='./build', name='dut', trace=TRACE, testbench=True)

    def compilation():
        os.system(cmd1)
        return hdl.Cosimulation(cmd2, clk_i=clk, rst_i=rst, rx_i=rx, tx_o=tx, anodos_o=anodos, segmentos_o=segmentos)

    def _rx_proc(data):
        yield tx.negedge
        data.next = 0
        yield hdl.delay((CLK_XTAL // (BAUD * 2)) * TICK_PERIOD)
        for _ in range(8):
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
            data.next = hdl.concat(tx, data[8:1])
        yield tx.posedge

    def _tx_proc(data, tx):
        tx.next = False
        yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
        for i in range(8):
            tx.next = (data >> i) & 0x01
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
        tx.next = True
        yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)

    # --------------------------------------------------------------------------
    @hdl.instance
    def rx_proc():
        for _ in range(len(TXRX_DATA)):
            yield _rx_proc(rx_data)
            rx_buffer.append(int(rx_data))
            print('Received: {}(0x{})'.format(chr(rx_data), rx_data))
        yield hdl.delay(5 * (CLK_XTAL // BAUD) * TICK_PERIOD)
        print('Buffer: {}'.format(rx_buffer))
        assert TXRX_DATA == rx_buffer, "[Loopback Error]: Send: {0}, Received: {1}".format(TXRX_DATA, rx_buffer)
        print('[Loopback-cosimulation] Test: OK')
        raise hdl.StopSimulation

    @hdl.instance
    def tx_proc():
        yield hdl.delay(2 * (CLK_XTAL // BAUD) * TICK_PERIOD)
        for data in TXRX_DATA:
            yield _tx_proc(data, rx)
            print("Send: {}({})".format(chr(data), hex(data)))

    return hdl.instances(), compilation()


def test_loopback():
    tb = loopback_testbench(len(TXRX_DATA))
    tb.run_sim()


if __name__ == '__main__':
    test_loopback()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
