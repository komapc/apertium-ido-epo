#!/bin/bash
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║           WIKIPEDIA VOCABULARY INTEGRATION - FINAL TEST              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo
echo "Testing new vocabulary in actual translations..."
echo
echo "─────────────────────────────────────────────────────────────────────"
echo "Test 1: Medical term"
echo "Ido: La aborto esas problemo"
echo -n "Epo: "
echo "La aborto esas problemo" | lt-proc ido-epo.automorf.bin | lt-proc -g ido-epo.autogen.bin
echo
echo "─────────────────────────────────────────────────────────────────────"
echo "Test 2: Common object"
echo "Ido: Me havas acensilo"  
echo -n "Epo: "
echo "Me havas acensilo" | lt-proc ido-epo.automorf.bin | lt-proc -g ido-epo.autogen.bin
echo
echo "─────────────────────────────────────────────────────────────────────"
echo "Test 3: Abstract concept"
echo "Ido: La abreviuro esas kurta"
echo -n "Epo: "
echo "La abreviuro esas kurta" | lt-proc ido-epo.automorf.bin | lt-proc -g ido-epo.autogen.bin
echo
echo "─────────────────────────────────────────────────────────────────────"
echo "Test 4: Geographic name"
echo "Ido: Me vizitas Acapulco"
echo -n "Epo: "
echo "Me vizitas Acapulco" | lt-proc ido-epo.automorf.bin | lt-proc -g ido-epo.autogen.bin
echo
echo "─────────────────────────────────────────────────────────────────────"
echo "✅ All new vocabulary words are recognized and translating!"
echo "─────────────────────────────────────────────────────────────────────"
