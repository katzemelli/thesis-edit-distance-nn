# References slide — topic-ordered

*The end-of-deck References slide (prof R2 asked for one). Every entry is drawn from
`REFERENCES_verified.md` and reformatted to `Nachname et al., Title, Venue, Year.`
Ordered by TOPIC, not by slide. Internal/unpublished sources (SS "ferras") are omitted —
no public citation. ⚠️ flags below are build notes, not slide text.*

---

## On the slide (7 topical groups)

**Neural edit-distance & sequence-distance embedding**
- Ohtomo, Takasu & Akutsu. *Computing Hamming and Levenshtein Distances Using ReLU Neural Networks.* IEEE Access, 2025.
- Dai et al. *Convolutional Embedding for Edit Distance (CNN-ED).* SIGIR, 2020.
- Corso et al. *Neural Distance Embeddings for Biological Sequences (NeuroSEED).* NeurIPS, 2021.
- Vinden, Foxcroft & Antonie. *Analysing Siamese Neural Network Architectures for Computing Name Similarity.* IJPDS, 2022.

**Siamese & metric-learning architecture**
- Bromley et al. *Signature Verification Using a "Siamese" Time Delay Neural Network.* NIPS, 1993.
- Hadsell, Chopra & LeCun. *Dimensionality Reduction by Learning an Invariant Mapping.* CVPR, 2006.
- Abdu-Aguye et al. *Adaptive Pooling Is All You Need.* IJCNN, 2020.

**Sequence embeddings & protein language models**
- Devlin et al. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL-HLT, 2019.
- Radford et al. *Learning Transferable Visual Models From Natural Language Supervision (CLIP).* ICML, 2021.
- Elnaggar et al. *ProtTrans: Toward Understanding the Language of Life Through Self-Supervised Learning.* IEEE TPAMI, 2022.
- Lin et al. *Evolutionary-scale prediction of atomic-level protein structure with a language model (ESM-2).* Science, 2023.
- Fenoy, Edera & Stegmayer. *Transfer learning in proteins: evaluating novel protein learned representations for bioinformatics tasks.* Briefings in Bioinformatics, 2022.

**Classical sequence comparison & structural search**
- Altschul et al. *Basic local alignment search tool (BLAST).* Journal of Molecular Biology, 1990.
- Steinegger & Söding. *MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets.* Nature Biotechnology, 2017.
- van Kempen et al. *Fast and accurate protein structure search with Foldseek.* Nature Biotechnology, 2024.

**Data & alphabets (CATH, 3Di, secondary structure)**
- Sillitoe et al. *CATH: increased structural coverage of functional space.* Nucleic Acids Research, 2021.
- Kabsch & Sander. *Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features.* Biopolymers, 1983.
- *(3Di alphabet: van Kempen et al. 2024, above.)*

**Edit-distance theory — LCS floor & fluctuations**
- Chvátal & Sankoff. *Longest common subsequences of two random sequences.* Journal of Applied Probability, 1975.
- Kiwi, Loebl & Matoušek. *Expected length of the longest common subsequence for large alphabets.* Advances in Mathematics, 2005.
- Baik, Deift & Johansson. *On the distribution of the length of the longest increasing subsequence of random permutations.* Journal of the AMS, 1999.
- Majumdar & Nechaev. *Anisotropic ballistic deposition model with links to the longest increasing subsequence.* Physical Review E, 2005.

**Edit-distance theory — metric & embeddability**
- Li & Liu. *A Normalized Levenshtein Distance Metric.* IEEE TPAMI, 2007.
- Krauthgamer & Rabani. *Improved Lower Bounds for Embeddings into L₁.* SIAM Journal on Computing, 2009.
- Ostrovsky & Rabani. *Low Distortion Embeddings for Edit Distance.* Journal of the ACM, 2007.
- Bourgain. *On Lipschitz embedding of finite metric spaces in Hilbert space.* Israel Journal of Mathematics, 1985.

---

## Build notes (NOT slide text)
- 25 references, 7 groups. If it's too dense for one slide, split at the natural seam:
  **methods/architecture/embeddings/search** (slides-1–4 content) on one References slide,
  **data + theory** (slides 8–15 content) on a second. The group order above already runs
  roughly in deck order, so a 2-way split is clean.
- **BERT = 2019** (NAACL, published venue); use 2018 only if citing the arXiv preprint.
- **ProtTrans title trap:** published TPAMI title is "Toward *Understanding*…", not the
  arXiv "Towards Cracking…". Venue = IEEE TPAMI, not "IEEE".
- **ESM** row = Lin et al. 2023 (Science) — this is ESM-2/ESMFold, the paper the prof means
  (not Rives et al. PNAS 2021).
- **Foldseek/3Di** senior author = Steinegger → the prof's "REF steinegge" resolves here,
  NOT to MMseqs2. Listed once (search group); cross-referenced under data.
- **SS "ferras"** = internal unpublished group paper → omitted; DSSP (Kabsch & Sander)
  covers the SS assignment itself, so the slide is still fully sourced.
- Optional LCS constants (γ₂ bounds: Lueker 2009, Dixon 2013) live in
  `SLIDE_08_synthetic_training_data.md`; left off this slide to keep it clean.
- Full annotations, DOIs, page numbers, and the ⚠️ honesty guards stay in
  `REFERENCES_verified.md` — that file remains the source of truth.
