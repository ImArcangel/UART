#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import os
import argparse


class Coregen:
    _build_path = './build'

    def __init__(self, board):
        parser    = argparse.ArgumentParser(description='Core generation.')
        subparser = parser.add_subparsers(title='Sub-commands', description='Available functions',
                                          help='Description')
        # convert
        p2v = subparser.add_parser('toverilog', help='Translate design to Verilog')
        p2v.set_defaults(func=self.convert_to_verilog)
        # build
        build = subparser.add_parser('build', help='Build bitstream using vendor tools')
        build.set_defaults(func=self.build_project)
        # program
        prog = subparser.add_parser('program', help='Program platform')
        prog.add_argument('--flash', help='Download bitfile to ISF', action='store_true')
        prog.set_defaults(func=self.program)

        self.parser = parser
        self.board  = board

    def run(self):
        args = self.parser.parse_args()
        args.func(args)

    def convert_to_verilog(self, args):
        os.makedirs(self._build_path, exist_ok=True)
        self.board.convert(path=self._build_path, trace=False, testbench=False)

    def build_project(self, args):
        os.makedirs(self._build_path, exist_ok=True)
        self.board.build(build_path=self._build_path)

    def program(self, args):
        prog = self.board.get_programmer()
        bitfile = '{}/{}.bit'.format(self._build_path, self.board.name)
        if args.flash:
            prog.flash(bitfile)
        else:
            prog.load_bitstream(bitfile)

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
