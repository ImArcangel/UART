#!/usr/bin/env python3
# Copyright (c) 2017 Angel Terrones <aterrones@usb.ve>

import sys
import subprocess


def write2file(filename, data):
    with open(filename, 'w', newline='\n') as f:
        f.write(data)


def subprocess_call(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
    log = ""
    with proc:
        for line in iter(proc.stdout.readline, ""):
            sys.stdout.write(line)
            log += line

    write2file("xilix_ise.log", log)
    return proc.returncode

# Local Variables:
# flycheck-flake8-maximum-line-length: 200
# flycheck-flake8rc: ".flake8rc"
# End:
