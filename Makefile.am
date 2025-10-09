###############################################################################
## Makefile for Ido--Esperanto
###############################################################################

LANG1=ido
LANG2=epo
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

TARGETS_COMMON =		\
	$(PREFIX1).automorf.bin	\
	$(PREFIX1).autobil.bin	\
	$(PREFIX1).autogen.bin	\
	$(PREFIX1).t1x.bin	\
	$(PREFIX2).automorf.bin	\
	$(PREFIX2).autobil.bin	\
	$(PREFIX2).autogen.bin	\
	$(PREFIX2).t1x.bin


# This include defines goals for install-modes, .deps/.d, autobil.prefixes and .mode files:
@ap_include@

###############################################################################
## Monolingual transducers
###############################################################################

# -------------------
# Ido analysis:
# -------------------

.deps/$(LANG1).automorf.bin: $(AP_SRC1)/$(LANG1).automorf.bin .deps/.d
	cp $< $@

$(PREFIX1).automorf.bin: .deps/$(LANG1).automorf.bin $(PREFIX1).autobil.bin
	lt-trim $^ $@

# -------------------
# Ido generation:
# ---------------------

$(PREFIX2).autogen.bin: $(AP_SRC1)/$(LANG1).autogen.bin
	cp $< $@

# -------------------
# Esperanto analysis:
# -------------------

.deps/$(LANG2).automorf.bin: $(AP_SRC2)/$(LANG2).automorf.bin .deps/.d
	cp $< $@

$(PREFIX2).automorf.bin: .deps/$(LANG2).automorf.bin $(PREFIX2).autobil.bin
	lt-trim $^ $@

# -------------------
# Esperanto generation:
# ---------------------

$(PREFIX1).autogen.bin: $(AP_SRC2)/$(LANG2).autogen.bin
	cp $< $@

###############################################################################
## Bilingual dictionaries
###############################################################################

$(PREFIX1).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $<
	lt-comp lr $< $@

$(PREFIX2).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $<
	lt-comp rl $< $@

###############################################################################
## Structural transfer rules
###############################################################################

$(PREFIX1).t1x.bin: $(BASENAME).$(PREFIX1).t1x
	apertium-validate-transfer $<
	apertium-preprocess-transfer $< $@

$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
	apertium-validate-transfer $<
	apertium-preprocess-transfer $< $@

###############################################################################
## Distribution
###############################################################################

EXTRA_DIST=					\
		$(BASENAME).$(PREFIX1).dix	\
		$(BASENAME).$(PREFIX1).t1x	\
		$(BASENAME).$(PREFIX2).t1x	\
		modes.xml

###############################################################################
## Installation
###############################################################################

apertium_ido_epodir=$(prefix)/share/apertium/$(BASENAME)/

# Files which should be installed to $(prefix)/share/apertium/$(BASENAME)/:
apertium_ido_epo_DATA=	\
	$(TARGETS_COMMON)				\
	$(BASENAME).$(PREFIX1).t1x			\
	$(BASENAME).$(PREFIX2).t1x

# All modes are created by the same goal, listing several will just give problems with make -j2
noinst_DATA=modes/$(PREFIX1).mode

install-data-local: install-modes

###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local:
	-rm -rf .deps modes

###############################################################################
## Test
###############################################################################

test: all
	apertium-regtest test

