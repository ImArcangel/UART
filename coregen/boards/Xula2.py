#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.toolflow.xilinx.programmer import XSTOOLS
from coregen.toolflow.xilinx.platform import XilinxPlatform


class Platform(XilinxPlatform):
    default_clk_freq = 12_000_000

    def __init__(self, toolchain='ise', programmer='xstools', *args, **kwargs):
        super().__init__(device='xc6slx25-2-ftg256', *args, **kwargs)
        self.toolchain.add_bitgen_options("-g ConfigRate:10 -g DonePin:PullUp -g TckPin:PullNone -g UnusedPin:PullNone -g StartUpClk:CClk")
        self.programmer = programmer

    def get_programmer(self):
        if self.programmer == 'xstools':
            return XSTOOLS('xula2-lx25')
        else:
            raise ValueError('{} programmer is not supported'.format(self.programmer))

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
