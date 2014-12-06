# -*- coding: utf-8 -*-
#  Copyright (C) 2014 Yusuke Suzuki <yusuke.suzuki@sslab.ics.keio.ac.jp>
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# usage
# import-kernel-symbols.py header.h.in System.map

import os
import sys
import re

template = """
%s
#define IMPORT_SYMBOL(name) \\
    static typeof(&name) IMPORTED(name) __attribute__((unused)) = (typeof(&name))IMPORT_SYMBOL_VALUE_FOR_ ## name
#define IMPORTED(name) __i__ ## name
"""

def main():

    header = None
    with open(sys.argv[1]) as file:
        header = file.read()

    directive = re.compile("IMPORT_SYMBOL\((.+)\)")
    dictionary = {}
    for symbol in re.findall(directive, header):
        dictionary[symbol] = -1

    imported = []
    symbols = re.compile("^([0-9a-fA-F]+) . (.+)$")
    with open(sys.argv[2]) as file:
        for line in file:
            m = re.match(symbols, line)
            addr = m.group(1)
            name = m.group(2)
            if dictionary.has_key(name):
                imported.append("#define IMPORT_SYMBOL_VALUE_FOR_%s (0x%sUL)" % (name, addr))
    generated = header.replace('IMPORT_SYMBOL_PROLOGUE', template % '\n'.join(imported))

    sys.stdout.write(generated)
    sys.stdout.flush()
    sys.exit(0)

if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et tw=80 :
