#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>


from coregen.toolflow.xilinx.programmer import iMPACT
from coregen.toolflow.xilinx.platform import XilinxPlatform


class Platform(XilinxPlatform):
    default_clk_freq = 50_000_000

    def __init__(self, toolchain='ise', programmer='impact', *args, **kwargs):
        super().__init__(device='xc3s200-ft256-4', *args, **kwargs)
        # self.toolchain.add_bitgen_options("-g StartUpClk:CClk")
        self.programmer = programmer

    def get_programmer(self):
        if self.programmer == 'impact':
            return iMPACT()
        else:
            raise ValueError('{} programmer is not supported'.format(self.programmer))


# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
