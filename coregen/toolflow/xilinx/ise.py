#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import os
from coregen.toolflow.platform import Pins
from coregen.toolflow.platform import IOStandard
from coregen.toolflow import tools


def _format_constraint(c):
    if isinstance(c, Pins):
        return 'LOC=' + c.identifiers[0]
    elif isinstance(c, IOStandard):
        return 'IOSTANDARD=' + c.name
    else:
        return ValueError('Invalid type: {}'.format(type(c)))


def _format_ucf(signame, pins, ios):
    lsc = []
    for c in [Pins(pins)] + ios:
        fc = _format_constraint(c)
        lsc.append(fc)
    constraints = " | ".join(lsc)
    return 'NET "{}" {};\n'.format(signame, constraints)


def _build_ucf(io):
    ucf = ''
    for port_name, port in io.items():
        pins = port.pins
        ios  = [port.iostandard]
        if len(port) > 1:
            for i, p in enumerate(pins.identifiers):
                ucf += _format_ucf(port_name + '<{}>'.format(i), pins.identifiers[i], ios)
        else:
            ucf += _format_ucf(port_name, pins.identifiers[0], ios)
    return ucf


def _create_ucf(io, filename):
    print('create UCF')
    tools.write2file(filename + '.ucf', _build_ucf(io))


def _create_xst_files(device, sources, build_name, xst_opt):
    print('create XST files')
    prj = ''
    for filename, language, library in sources:
        prj += '{} {} {}\n'.format(language, library, filename)
    tools.write2file(build_name + '.prj', prj)

    xst = """run
-ifn {0}.prj
-top {0}
{1}
-ofn {0}.ngc
-p {2}
""".format(build_name, xst_opt, device)
    tools.write2file(build_name + '.xst', xst)


def _run_ise(build_name, map_opt, par_opt, ngdbuild_opt, bitgen_opt):
    print('run ISE')
    build_script = """xst -ifn {build_name}.xst
ngdbuild {ngdbuild_opt} -uc {build_name}.ucf {build_name}.ngc {build_name}.ngd
map {map_opt} -o {build_name}_map.ncd {build_name}.ngd {build_name}.pcf
par {par_opt} {build_name}_map.ncd {build_name}.ncd {build_name}.pcf
bitgen {bitgen_opt} {build_name}.ncd {build_name}.bit
""".format(build_name=build_name,
           map_opt=map_opt,
           par_opt=par_opt,
           ngdbuild_opt=ngdbuild_opt,
           bitgen_opt=bitgen_opt)
    script_file = "build_{}.sh".format(build_name)
    tools.write2file(script_file, build_script)
    cmd = ['bash'] + [script_file]
    r = tools.subprocess_call(cmd)
    if r != 0:
        raise OSError("Executing script failed")


class XilinxISE():
    def __init__(self):
        self.xst_opt = """-ifmt MIXED
-opt_mode SPEED
-opt_level 2
-register_balancing yes"""
        self.map_opt      = '-ol high -w -pr b -timing'
        self.par_opt      = '-ol high -w'
        self.ngdbuild_opt = ''
        self.bitgen_opt   = '-w'

    def add_bitgen_options(self, opt):
        self.bitgen_opt += " " + opt

    def build(self, platform, build_path='build', build_name='top'):
        cwd = os.getcwd()
        os.chdir(build_path)
        try:
            sources = {(build_name + '.v', "verilog", "work")}
            platform.convert(name=build_name, trace=False, testbench=False)
            _create_ucf(platform.io, build_name)
            _create_xst_files(platform.device, sources, build_name, self.xst_opt)
            _run_ise(build_name, self.map_opt, self.par_opt, self.ngdbuild_opt, self.bitgen_opt)
        finally:
            os.chdir(cwd)

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
