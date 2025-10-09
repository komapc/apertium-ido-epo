###############################################################################
## Makefile for Ido-Esperanto Apertium language pair
###############################################################################

LANG1=ido
LANG2=epo
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

## Dictionaries
DICS=$(PREFIX1).autobil.bin $(PREFIX1).automorf.bin $(PREFIX1).autogen.bin $(PREFIX1).autopgen.bin \
     $(PREFIX2).autobil.bin $(PREFIX2).automorf.bin $(PREFIX2).autogen.bin $(PREFIX2).autopgen.bin

## Transfer rules
TRANSFER=$(PREFIX1).t1x.bin $(PREFIX2).t1x.bin

## Build targets
all: $(DICS) $(TRANSFER)

## Morphological analyzers (using lt-comp)
$(PREFIX1).automorf.bin: apertium-$(LANG1).$(LANG1).dix
	lt-comp lr $< $@

$(PREFIX2).automorf.bin: apertium-$(LANG2).$(LANG2).dix
	lt-comp lr $< $@

## Morphological generators (using lt-comp)
$(PREFIX1).autogen.bin: apertium-$(LANG2).$(LANG2).dix
	lt-comp rl $< $@

$(PREFIX2).autogen.bin: apertium-$(LANG1).$(LANG1).dix
	lt-comp rl $< $@
## Post-generation dictionaries
$(PREFIX1).autopgen.bin: $(BASENAME).post-$(LANG2).dix
	lt-comp lr $< $@

$(PREFIX2).autopgen.bin: $(BASENAME).post-$(LANG1).dix
	lt-comp lr $< $@


## Bilingual dictionaries (using lt-comp)
$(PREFIX1).autobil.bin: $(BASENAME).$(PREFIX1).dix
	lt-comp lr $< $@

$(PREFIX2).autobil.bin: $(BASENAME).$(PREFIX1).dix
	lt-comp rl $< $@

## Transfer rules (using apertium-preprocess-transfer and lt-comp)
$(PREFIX1).t1x.bin: $(BASENAME).$(PREFIX1).t1x
	apertium-preprocess-transfer $< $@

$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
	apertium-preprocess-transfer $< $@

## Modes
modes: modes.xml
	apertium-gen-modes modes.xml

## Test targets
test-ido-epo:
	@echo "Testing Ido → Esperanto"
	@echo "abako" | apertium -d . $(PREFIX1)

test-epo-ido:
	@echo "Testing Esperanto → Ido"
	@echo "abako" | apertium -d . $(PREFIX2)

test: test-ido-epo test-epo-ido

## Clean
clean:
	rm -f $(DICS) $(TRANSFER)
	rm -rf .deps modes *.mode

.PHONY: all modes test test-ido-epo test-epo-ido clean


