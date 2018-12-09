#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl
from coregen.utils import createSignal
from rtl.uart.uart import UART

# Constantes
CLK_XTAL    = 1000
BAUD        = 10
TXRX_DATA   = [ord(i) for i in "Hello world! :D"]
TIMEOUT     = int(3 * (12 * len(TXRX_DATA) / BAUD) * CLK_XTAL)  # 12 symbols x char. Worst case: 5 times the message
TICK_PERIOD = 2
RESET_TIME  = 5
TRACE       = False


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
def uart_tx_testbench():
    clk      = createSignal(0, 1)
    rst      = hdl.ResetSignal(0, active=True, isasync=False)
    tx_data  = createSignal(0, 8)
    rx_data  = createSignal(0, 8)
    tx_start = createSignal(0, 1)
    tx_ready = createSignal(0, 1)
    rx_ready = createSignal(0, 1)
    rx       = createSignal(1, 1)
    tx       = createSignal(0, 1)
    rx_check = createSignal(0, 8)
    clk_tout = clk_n_timeout(clk, rst)  # noqa
    dut      = UART(clk, rst, tx_data, tx_start, tx_ready, tx,  # noqa
                    rx_data, rx_ready, rx,
                    CLK_BUS=CLK_XTAL, BAUD_RATE=BAUD)

    def _rx_proc(data):
        yield tx.negedge
        yield hdl.delay((CLK_XTAL // (BAUD * 2)) * TICK_PERIOD)
        for _ in range(8):
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
            data.next = hdl.concat(tx, data[8:1])
        yield tx.posedge

    @hdl.instance
    def uart_stimulus():
        yield tx_ready.posedge
        for data in TXRX_DATA:
            tx_data.next  = data
            tx_start.next = True
            yield hdl.delay(TICK_PERIOD)
            yield _rx_proc(rx_check)
            yield tx_ready.posedge
            tx_start.next = False
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
            assert rx_check == data, "[TX error] Received: {0}. Send: {1}".format(hex(rx_check), hex(data))
        yield hdl.delay((CLK_XTAL // (BAUD * 2)) * TICK_PERIOD)
        raise hdl.StopSimulation

    return hdl.instances()


@hdl.block
def uart_rx_testbench():
    clk      = createSignal(0, 1)
    rst      = hdl.ResetSignal(0, active=True, isasync=False)
    tx_data  = createSignal(0, 8)
    rx_data  = createSignal(0, 8)
    tx_start = createSignal(0, 1)
    tx_ready = createSignal(0, 1)
    rx_ready = createSignal(0, 1)
    rx       = createSignal(1, 1)
    tx       = createSignal(0, 1)
    tx_check = createSignal(0, 8)
    clk_tout = clk_n_timeout(clk, rst)  # noqa
    dut      = UART(clk, rst, tx_data, tx_start, tx_ready, tx,  # noqa
                    rx_data, rx_ready, rx,
                    CLK_BUS=CLK_XTAL, BAUD_RATE=BAUD)

    def _tx_proc(data, tx):
        tx.next = False
        yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
        for i in range(8):
            tx.next = (data >> i) & 0x01
            yield hdl.delay((CLK_XTAL // BAUD) * TICK_PERIOD)
        tx.next = True

    @hdl.instance
    def uart_stimulus():
        yield hdl.delay(2 * (CLK_XTAL // BAUD) * TICK_PERIOD)
        # test RX
        for data in TXRX_DATA:
            yield _tx_proc(data, rx)
            tx_check.next = rx_data
            yield hdl.delay(1)
            assert tx_check == data, "[RX error] Send: {0}. Received: {1}".format(hex(data), hex(tx_check))
            yield hdl.delay(2 * (CLK_XTAL // BAUD) * TICK_PERIOD)
        yield hdl.delay((CLK_XTAL // (BAUD * 2)) * TICK_PERIOD)

        raise hdl.StopSimulation

    return hdl.instances()


@hdl.block
def uart_loopback_testbench():
    clk      = createSignal(0, 1)
    rst      = hdl.ResetSignal(0, active=True, isasync=False)
    tx_data  = createSignal(0, 8)
    rx_data  = createSignal(0, 8)
    tx_start = createSignal(0, 1)
    tx_ready = createSignal(0, 1)
    rx_ready = createSignal(0, 1)
    txrx     = createSignal(1, 1)
    clk_tout = clk_n_timeout(clk, rst)  # noqa
    dut      = UART(clk, rst, tx_data, tx_start, tx_ready, txrx,  # noqa
                    rx_data, rx_ready, txrx,
                    CLK_BUS=CLK_XTAL, BAUD_RATE=BAUD)

    @hdl.instance
    def uart_stimulus():
        yield hdl.delay(2 * (CLK_XTAL // BAUD) * TICK_PERIOD)
        for data in TXRX_DATA:
            tx_data.next  = data
            tx_start.next = True
            yield tx_ready.posedge
            tx_start.next = False
            yield rx_ready.posedge
            assert rx_data == data, "[TXRX error] Send: {0}, Received: {1}".format(hex(data), hex(rx_data))
            yield hdl.delay(2 * (CLK_XTAL // BAUD) * TICK_PERIOD)

        raise hdl.StopSimulation

    return hdl.instances()


def test_uart_tx():
    tb = uart_tx_testbench()
    tb.config_sim(trace=TRACE)
    tb.run_sim()


def test_uart_rx():
    tb = uart_rx_testbench()
    tb.config_sim(trace=TRACE)
    tb.run_sim()


def test_uart_loopback():
    tb = uart_loopback_testbench()
    tb.config_sim(trace=TRACE)
    tb.run_sim()

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
