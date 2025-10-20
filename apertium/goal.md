# Project Goal

Create an Ido → Esperanto dictionary using Cross-Lingual Alignment of Contextual Word Embeddings

## Data Sources

* **Ido corpus**: Wikipedia dump
* **Esperanto corpus**: Wikipedia dump + additional sources
* **Starting point**: Ido/Esperanto dictionary from Wiktionaries

## Libraries to be Used

Choose one of the following:

* **MUSE** (Multilingual Unsupervised and Supervised Embeddings)
* **FastText**
* **VecMap**
* **NLTK and Gensim**

## Plan

1. **Data Collection**
   - Download and extract Ido Wikipedia dump
   - Download and extract Esperanto Wikipedia dump
   - Extract Ido/Esperanto dictionary entries from Wiktionaries

2. **Corpus Preprocessing**
   - Clean and tokenize Ido corpus
   - Clean and tokenize Esperanto corpus
   - Normalize text and handle special characters

3. **Word Embeddings Training**
   - Train monolingual word embeddings for Ido
   - Train monolingual word embeddings for Esperanto
   - Evaluate embedding quality

4. **Cross-Lingual Alignment**
   - Use seed dictionary from Wiktionaries
   - Apply cross-lingual alignment techniques
   - Map Ido embeddings to Esperanto embedding space

5. **Dictionary Extraction**
   - Generate translation candidates using nearest neighbors
   - Filter and rank translations by confidence scores
   - Validate against existing dictionary entries

6. **Evaluation and Refinement**
   - Evaluate dictionary quality and coverage
   - Manually review sample translations
   - Iterate and improve alignment parameters  



To build a dictionary between Ido and Esperanto using cross-lingual alignment of contextual word embeddings, you can follow these steps and resources:

Recommended Lectures
"Cross-Lingual Word Embeddings" by Facebook AI Research (FAIR)

This lecture delves into the fundamental concepts of cross-lingual word embeddings and explores various alignment strategies. It provides valuable insights into the methodologies used in the field, which will be essential for your project.
Watch here
"Multilingual Word Embeddings" by Stanford NLP

In this lecture, you will learn about multilingual embeddings and their use cases, including specific alignment techniques. It serves as an excellent introduction to the complexities of working with multiple languages.
Watch here
"Introduction to Natural Language Processing" by Stanford University

While this course covers broader topics in natural language processing, it lays a strong groundwork necessary to grasp the intricacies of language models and embeddings, which are key to your dictionary project.
Watch here