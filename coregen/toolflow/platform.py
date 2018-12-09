#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import myhdl as hdl


class Pins:
    def __init__(self, pin_list):
        self.identifiers = pin_list.split()
        self._n_pins     = len(self.identifiers)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, " ".join(self.identifiers))

    def __len__(self):
        return self._n_pins


class IOStandard:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.name)


class Port(hdl.SignalType):
    def __init__(self, pins, iostandard):
        self.pins       = Pins(pins)
        self.iostandard = IOStandard(iostandard)
        npins = len(self.pins)
        if npins > 1:
            super().__init__(hdl.modbv(0)[len(self.pins):])
        else:
            super().__init__(False)


class ResetPort(hdl.ResetSignal):
    def __init__(self, pins, iostandard=None, **kwargs):
        self.pins       = Pins(pins)
        self.iostandard = IOStandard(iostandard)
        super().__init__(**kwargs)


class Platform:
    def __init__(self, device, module, io, params=None, name=None):
        self.device = device
        self.module = module
        self.io     = io
        self.params = params
        if name is None:
            name = self.module.__name__
        self.name   = name

    def convert(self, name=None, **kwargs):
        if self.params is not None:
            io = {**self.io, **self.params}
        else:
            io = self.io
        if name is None:
            name = self.name
        print('Generate verilog: {}.v'.format(name))
        top = self.module(**io)
        top.convert(name=name, **kwargs)

    def build(self):
        raise NotImplementedError

    def get_programmer(self):
        raise NotImplementedError

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
