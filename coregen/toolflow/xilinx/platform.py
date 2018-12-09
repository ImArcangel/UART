#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

from coregen.toolflow.xilinx import ise
from coregen.toolflow.platform import Platform


class XilinxPlatform(Platform):
    def __init__(self, toolchain='ise', *args, **kwargs):
        super().__init__(*args, **kwargs)
        if toolchain == 'ise':
            self.toolchain = ise.XilinxISE()
        elif toolchain == 'vivado':
            raise NotImplementedError('Vivado toolchain is not implemented (yet)')
        else:
            raise ValueError('Unknown toolchain')

    def build(self, **kwargs):
        self.toolchain.build(platform=self, build_name=self.name, **kwargs)

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
