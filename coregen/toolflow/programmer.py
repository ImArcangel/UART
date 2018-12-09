#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>


class Programmer:
    def load_bitstream(self, bitfile):
        raise NotImplementedError

    def flash(self, bitfile):
        raise NotImplementedError

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
