#!/usr/bin/python3

import re
import sys, os
import fileinput

RE_COMMENT  = re.compile("#.*")
RE_METADATA = re.compile("!(\w+)=(.+)(oh \s*#.*)?")
RE_PACKET   = re.compile("([CS]\d*)\s+([A-Fa-f0-9]+)(?:\s+@([0-9]+))?(\s*#.*)?")

for index, line in enumerate(fileinput.input(files=sys.argv[1:])):
    # remove leading and trailing whitespace
    line = line.strip()

    # ignore full-line comments
    if line.startswith("#"):
        continue

    # check for metadata
    metadata = RE_METADATA.match(line)
    if metadata:
        print("Metadata: %r -> %r" % (metadata.group(1), metadata.group(2)))
        continue

    # check for packets
    packet = RE_PACKET.match(line)
    if packet:
        print("packet: [%s] sent [%s] (timestamp: %s)" % (packet.group(1), packet.group(2), packet.group(3)))
        continue

    # give up
    raise ValueError("Could not parse line %d: [%s]" % (index, line))
