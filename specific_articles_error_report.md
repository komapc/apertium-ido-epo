# Translation Error Analysis Report

**Analysis Date:** October 9, 2025

## Overview

This report analyzes translation errors in 3 Wikipedia articles translated between Ido and Esperanto using Apertium.

## Articles Analyzed

1. **France (Esperanto → Ido)**
   - Title: Francio
   - Direction: epo-ido

2. **France (Ido → Esperanto)**
   - Title: Francia
   - Direction: ido-epo

3. **Gaza Strip (Ido → Esperanto)**
   - Title: Gaza-strio
   - Direction: ido-epo

---

## France (Esperanto → Ido)

**Title:** Francio  
**Source Language:** eo  
**Target Language:** Ido  
**Direction:** `epo-ido`

### Statistics

| Metric | Value |
|--------|-------|
| Original Words | 806 |
| Translated Words | 806 |
| Word Ratio | 1.0 |
| Error Rate | 77.05% |
| @ Errors | 322 |
| # Errors | 262 |
| * Errors | 37 |
| **Total Errors** | **621** |

### Unknown Words and Error Patterns

#### Unknown Words (@ marker)

These words were not found in the dictionary:

- `@plej`
- `@landlimo`
- `@19a`
- `@reĝa`
- `@ĝis`
- `@supra`
- `@Ludoviko`
- `@dissolviĝi`
- `@Unesko`
- `@de`
- `@Nazia`
- `@aperi`
- `@Aliancano`
- `@venkinto`
- `@falo`

*...and 5 more*

#### Analysis Errors (# marker)

These forms could not be analyzed:

- `#komerc`
- `#1815`
- `#La`
- `#quo`
- `#Rejno`
- `#Hom`
- `#Franco`
- `#Atlantiko`
- `#si`
- `#2019`
- `#1870`
- `#modern`
- `#nom`
- `#mond`
- `#2010`

*...and 5 more*

#### Generation Errors (* marker)

These forms could not be generated:

- `*industrilando`
- `*mondpotenco`
- `*G20`
- `*G8`
- `*Okcidentfranka`
- `*Maarten`
- `*Nordatlantika`
- `*dukapa`
- `*partis`
- `*fʁɑ`
- `*Sint`
- `*ekformis`
- `*G10`
- `*pluas`
- `*Hugenotoj`

### Specific Translation Issues

- **Untranslated phrases:** 10 instances

### Sample Errors in Context

Here are some examples of errors found in the translation:

**Example 1** (line 1):

```
Franco #od #Franco @(@oficiala #la #Francian Republiko@, @franca @Franca @\[*fʁɑ̃@s@\] #od *République *française @\[*ʁepyblik *fʁɑ̃*sɛz@\]@) esas stato@, @kies metropolito situesas en @Okcidenta Eŭro
```

**Example 2** (line 2):

```
Franco #od #Franco @(@oficiala #la #Francian Republiko@, @franca @Franca @\[*fʁɑ̃@s@\] #od *République *française @\[*ʁepyblik *fʁɑ̃*sɛz@\]@) esas stato@, @kies metropolito situesas en @Okcidenta Eŭro
```

**Example 3** (line 3):

```
Franco havas @landlimo kun #Belgio@, @Luksemburgio e @Germanio @nordorienta@, kun @Svislando e #Italio @orienta@, e kun monako@, @Andoro e #Hispanio @suda@, e #la @supra #mencion mari@. @Danke al #si 
```

**Example 4** (line 4):

```
@Dum #la @Ferepoko@, #l #quo esas @nun @metropola Franco esis @loĝi da @Gaŭlo@, @noma @kelta populo@. #Romio anexis #la areon en #la yaro #51 @a.K.@, e @teni #ol @ĝis #la @alveno da @ĝermana Franki en
```

**Example 5** (line 5):

```
@En la komenco da #la @19a #yarcent@, #Napoleono *enpoviĝis e establisis #la #Francian Imperion@. #La @posta @Napoleona Militi @(#1803–#15@) formacis #la #futur estadon da @kontinenta #Europa@. Pos #l
```

### Original Text Excerpt (first 500 characters)

```
Francio aŭ Francujo (oficiale la Franca Respubliko, france France [fʁɑ̃s] aŭ République française [ʁepyblik fʁɑ̃sɛz]) estas ŝtato, kies metropolo situas en Okcidenta Eŭropo, kaj kies transmaraj departementoj situas en aliaj kontinentoj. Francio etendiĝas ekde Mediteraneo ĝis la Manika Markolo, kaj ekde la riverego Rejno ĝis Atlantiko. En Franclingvio, Francio havas la kromnomon l’Hexagone (la "sesangulo") pro sia ĝenerala konturo.
Francio havas landlimojn kun Belgio, Luksemburgio kaj Germanio no...
```

### Translation Excerpt (first 500 characters)

```
Franco #od #Franco @(@oficiala #la #Francian Republiko@, @franca @Franca @\[*fʁɑ̃@s@\] #od *République *française @\[*ʁepyblik *fʁɑ̃*sɛz@\]@) esas stato@, @kies metropolito situesas en @Okcidenta Eŭropo@, e @kies @transmara departmenti situesas en @alia kontinenti@. Franco @etendi @ekde #Mediteraneo @ĝis #la @Manika @Markolo@, e @ekde #la fluvio #Rejno @ĝis #Atlantiko@. En @Franclingvio@, Franco havas #la @kromnomo @l@’*Hexagone @(#la "@sesangulo"@) pro #si @ĝenerala @konturo@.
Franco havas @lan...
```

---

## France (Ido → Esperanto)

**Title:** Francia  
**Source Language:** io  
**Target Language:** Esperanto  
**Direction:** `ido-epo`

### Statistics

| Metric | Value |
|--------|-------|
| Original Words | 786 |
| Translated Words | 787 |
| Word Ratio | 1.0 |
| Error Rate | 51.72% |
| @ Errors | 13 |
| # Errors | 78 |
| * Errors | 316 |
| **Total Errors** | **407** |

### Unknown Words and Error Patterns

#### Unknown Words (@ marker)

These words were not found in the dictionary:

- `@nask`
- `@lor`
- `@Belgi`
- `@ofic`
- `@statal`
- `@klar`
- `@mult`
- `@vertikal`
- `@rest`
- `@teritori`
- `@Paris`

#### Analysis Errors (# marker)

These forms could not be analyzed:

- `#Dum`
- `#Mediteraneo`
- `#Svislando`
- `#kia`
- `#l`
- `#Germanio`
- `#Atlantiko`
- `#Luksemburgo`
- `#igi`
- `#Multaj`
- `#Andoro`
- `#post`
- `#dum`
- `#kelkaj`
- `#Italio`

*...and 5 more*

#### Generation Errors (* marker)

These forms could not be generated:

- `*Auguste`
- `*Caesar`
- `*nomizar`
- `*Lascaux`
- `*quankam`
- `*himno`
- `*kolonial`
- `*tipo`
- `*1789`
- `*formacesis`
- `*kande`
- `*trovita`
- `*Klodovecho`
- `*unionesis`
- `*filii`

### Sample Errors in Context

Here are some examples of errors found in the translation:

**Example 1** (line 1):

```
#Francio, en longa formo: Respubliko *Franca (*République *française), estas lando en *westal #Eŭropo #kia ankaŭ havas *teritorii en aliaj kontinentoj. Lia *chef-urbo - kaj *maxim *populoza urbo - est
```

**Example 2** (line 2):

```
#Francio, en longa formo: Respubliko *Franca (*République *française), estas lando en *westal #Eŭropo #kia ankaŭ havas *teritorii en aliaj kontinentoj. Lia *chef-urbo - kaj *maxim *populoza urbo - est
```

**Example 3** (line 3):

```
Lia oficiala *linguo estas la *Franca, kaj lia valuto estas Eŭro. Lia devizo estas *Liberté, *égalité, *fraternité (*Ide: *libereso, *egaleso, *frateso), kaj lia standardo #en) *ek *tri @vertikal bend
```

**Example 4** (line 4):

```
#Francio estas malnova lando, #kia *formacesis #dum la fino de la *Mezepoko. *Del frua *17ma *yarcento ĝis #l'*unesma parto de *20ma *yarcento, #Francio havis vasta *kolonial imperio. #Post la jaroj *
```

**Example 5** (line 5):

```
#Francio okupis en *2012 la *kinesma etendiĝo *mondala *segun tuta *nacionala *produkturo antaŭ impostoj. Lia ekonomio, de *tipo *kapitalista kun *sat forta @statal *interveno, #igi, fari lin *un *ek 
```

### Original Text Excerpt (first 500 characters)

```
Francia, en longa formo: Republiko Franca (République française), esas lando en westal Europa qua anke havas teritorii en altra kontinenti. Lua chef-urbo - e maxim populoza urbo - esas Paris, kun 2 125 245 habitanti segun la demografiala kontado di 1999. Havanta entote 68 084 217 habitanti segun statistiki por julio 2021, inkluzite la habitantaro di transmara regioni, Francia esas developata lando, kun tre alta indexo pri homala developeso. En la kontinento Europana, ol havas kom vicini Hispania...
```

### Translation Excerpt (first 500 characters)

```
#Francio, en longa formo: Respubliko *Franca (*République *française), estas lando en *westal #Eŭropo #kia ankaŭ havas *teritorii en aliaj kontinentoj. Lia *chef-urbo - kaj *maxim *populoza urbo - estas @Paris, kun *2 *125 *245 *habitanti *segun la *demografiala *kontado de *1999. *Havanta *entote *68 *084 *217 *habitanti *segun statistikoj por julio *2021, *inkluzite la loĝantaro de *transmara regionoj, #Francio estas *developata lando, kun *tre alta indekso pri homa *developeso. En la kontinen...
```

---

## Gaza Strip (Ido → Esperanto)

**Title:** Gaza-strio  
**Source Language:** io  
**Target Language:** Esperanto  
**Direction:** `ido-epo`

### Statistics

| Metric | Value |
|--------|-------|
| Original Words | 120 |
| Translated Words | 122 |
| Word Ratio | 1.02 |
| Error Rate | 54.92% |
| @ Errors | 2 |
| # Errors | 18 |
| * Errors | 47 |
| **Total Errors** | **67** |

### Unknown Words and Error Patterns

#### Unknown Words (@ marker)

These words were not found in the dictionary:

- `@tal`
- `@precipu`

#### Analysis Errors (# marker)

These forms could not be analyzed:

- `#km`
- `#Mediteraneo`
- `#dum`
- `#Egiptio`
- `#Israelo`
- `#kia`
- `#l`
- `#km²`
- `#la`
- `#Palestino`
- `#ĉar`

#### Generation Errors (* marker)

These forms could not be generated:

- `*غزة`
- `*Dayr`
- `*40`
- `*Abasan`
- `*teritorii`
- `*konsequantajo`
- `*habitata`
- `*Bala`
- `*עזה`
- `*1967`
- `*Rafa`
- `*longesas`
- `*Cisjordania`
- `*360`
- `*1994`

### Sample Errors in Context

Here are some examples of errors found in the translation:

**Example 1** (line 1):

```
*Gaza-strio (en #l'araba: *Kita` *Gaza - *قطاع *غزة, en la #la hebrea lingvo: *Retzu'*at '*Aza - *רצועת *עזה ), @tal *nomesas #ĉar #l'urbo *Gaza *sud-okcidente de #Israelo. *Gaza-strio kun *Cisjordani
```

**Example 2** (line 2):

```
*Gaza-strio (en #l'araba: *Kita` *Gaza - *قطاع *غزة, en la #la hebrea lingvo: *Retzu'*at '*Aza - *רצועת *עזה ), @tal *nomesas #ĉar #l'urbo *Gaza *sud-okcidente de #Israelo. *Gaza-strio kun *Cisjordani
```

### Original Text Excerpt (first 500 characters)

```
Gaza-strio (en l'Arabiana: Kita` Gaza - قطاع غزة, en la Hebrea: Retzu'at 'Aza - רצועת עזה ), tale nomesas pro l'urbo Gaza sud-weste de Israel. Gaza-strio kun Cisjordania esas parto di Palestina, nun nomizite Palestinana teritorii. La regiono konquestesis da Israel en 1967 dum la Sis-dia milito e kom konsequantajo di la paco-konkordo transdonesis a la Palestinan Autoritato qua depos 1994 guvernas la regiono, precipue habitata da Palestinani.
Gaza-strio havas surfaco de cirkume 360 km² e havas fro...
```

### Translation Excerpt (first 500 characters)

```
*Gaza-strio (en #l'araba: *Kita` *Gaza - *قطاع *غزة, en la #la hebrea lingvo: *Retzu'*at '*Aza - *רצועת *עזה ), @tal *nomesas #ĉar #l'urbo *Gaza *sud-okcidente de #Israelo. *Gaza-strio kun *Cisjordania estas parto de #Palestino, *nun *nomizite *Palestinana *teritorii. La regiono *konquestesis de #Israelo en *1967 #dum la *Sis-*dia milito kaj kiel *konsequantajo de la paco-*konkordo *transdonesis al la *Palestinan Aŭtoritato #kia *depos *1994 direktas la regionon, @precipu *habitata de *Palestina...
```

---

## Overall Summary

- **Total articles analyzed:** 3
- **Total words translated:** 1,715
- **Total error markers:** 1,095
- **Average error rate:** 61.23%

### Esperanto → Ido

- Articles: 1
- Average error rate: 77.05%

### Ido → Esperanto

- Articles: 2
- Average error rate: 53.32%

---

*Note: This is an error analysis only. No corrections have been made to the translation system.*
