#!/usr/bin/python3

import re
import sys, os
import fileinput

RE_BITS = {
    "packet": "(?P<source>[CS]\d*)\s+(?P<packet>[A-Fa-f0-9]+)",
    "metadata": "!(?P<key>\w+)(?:=(?P<value>\S+?))?",
    "comment": "(?:#\s*(?P<comment>.*))?",
    "timestamp": "(?:@(?P<timestamp>[0-9]+))?",
}
RE_COMMENT  = re.compile("^%(comment)s$" % RE_BITS)
RE_METADATA = re.compile("^%(metadata)s\s*%(timestamp)s\s*%(comment)s$" % RE_BITS)
RE_PACKET   = re.compile("^%(packet)s\s*%(timestamp)s\s*%(comment)s$" % RE_BITS)

if len(sys.argv) < 2:
    print("Usage: %s <apd files..>" % sys.argv[0])
    sys.exit(1)

for index, line in enumerate(fileinput.input(files=sys.argv[1:])):
    # ignore full-line comments
    if RE_COMMENT.match(line):
        continue

    # check for metadata
    metadata = RE_METADATA.match(line)
    if metadata:
        print("Metadata: %r -> %r" % (metadata.group("key"), metadata.group("value")))
        continue

    # check for packets
    packet = RE_PACKET.match(line)
    if packet:
        print("packet: [%s] sent [%s] (timestamp: %s)" % (packet.group("source"), packet.group("packet"), packet.group("timestamp")))
        continue

    # give up
    raise ValueError("Could not parse line %d: [%s]" % (index, line))
