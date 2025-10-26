###############################################################################
## Makefile for Ido--Esperanto
###############################################################################

LANG1=ido
LANG2=epo
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

# Define source directories for monolingual transducers
# Use local files instead of system-installed
AP_SRC1=/home/mark/apertium-dev/apertium/apertium-ido
AP_SRC2=/usr/share/apertium/apertium-epo

TARGETS_COMMON =		\
	$(PREFIX1).automorf.bin	\
	$(PREFIX1).autobil.bin	\
	$(PREFIX1).autogen.bin	\
	$(PREFIX1).autopgen.bin	\
	$(PREFIX1).t1x.bin	\
	$(PREFIX2).automorf.bin	\
	$(PREFIX2).autobil.bin	\
	$(PREFIX2).autogen.bin	\
	$(PREFIX2).autopgen.bin	\
	$(PREFIX2).rlx.bin	\
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

$(PREFIX1).automorf.bin: .deps/$(LANG1).automorf.bin
	cp $< $@

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

$(PREFIX2).automorf.bin: .deps/$(LANG2).automorf.bin
	cp $< $@

# -------------------
# Esperanto generation:
# ---------------------

$(PREFIX1).autogen.bin: $(AP_SRC2)/$(LANG2).autogen.bin
	cp $< $@

###############################################################################
## Post-generation
###############################################################################

$(PREFIX1).autopgen.bin: $(BASENAME).post-$(LANG2).dix
	apertium-validate-dictionary $<
	lt-comp lr $< $@

$(PREFIX2).autopgen.bin: $(BASENAME).post-$(LANG1).dix
	apertium-validate-dictionary $<
	lt-comp lr $< $@

###############################################################################
## Disambiguation rules  
###############################################################################

$(PREFIX2).rlx.bin: $(BASENAME).$(LANG2).$(LANG2).rlx
	cg-comp $< $@

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
		$(BASENAME).post-$(LANG1).dix	\
		$(BASENAME).post-$(LANG2).dix	\
		$(BASENAME).$(LANG2).$(LANG2).rlx	\
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



###############################################################################
## Build Preparation and Validation
###############################################################################

# Check that required files exist before compilation
check-files:
	@echo "Checking for required files..."
	@test -f $(BASENAME).$(PREFIX1).t1x || (echo "ERROR: Missing $(BASENAME).$(PREFIX1).t1x" && exit 1)
	@test -f $(BASENAME).$(PREFIX2).t1x || (echo "ERROR: Missing $(BASENAME).$(PREFIX2).t1x" && exit 1)
	@test -f $(BASENAME).post-$(LANG1).dix || (echo "ERROR: Missing $(BASENAME).post-$(LANG1).dix" && exit 1)
	@test -f $(BASENAME).post-$(LANG2).dix || (echo "ERROR: Missing $(BASENAME).post-$(LANG2).dix" && exit 1)
	@test -f $(BASENAME).$(LANG2).$(LANG2).rlx || (echo "ERROR: Missing $(BASENAME).$(LANG2).$(LANG2).rlx" && exit 1)
	@echo "All required files present"

# Enhanced validation that includes paradigm checks
validate-dictionaries: check-files
	@echo "Validating dictionaries..."
	@apertium-validate-dictionary $(BASENAME).$(PREFIX1).dix || exit 1
	@echo "Dictionary validation complete"

# Override main targets to include validation
$(PREFIX1).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $<
	lt-comp lr $< $@

$(PREFIX2).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $<
	lt-comp rl $< $@

