#!/bin/bash
# Simple wrapper for ido-epo translation
# Usage: echo "text" | ./translate-ido-epo.sh

cd "$(dirname "$0")"
lt-proc ido-epo.automorf.bin | apertium-pretransfer | lt-proc -b ido-epo.autobil.bin | apertium-transfer -b apertium-ido-epo.ido-epo.t1x ido-epo.t1x.bin | lt-proc -g ido-epo.autogen.bin | lt-proc -p ido-epo.autopgen.bin
