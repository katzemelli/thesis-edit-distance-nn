# Verified references — Zwischenpräsentation (v17 deck)

*Verified 2026-07-18 against primary/publisher sources. Format per professor's R2 feedback:
`Nachname et al., Title, Journal/Venue, Year.` — put a small cite under every borrowed figure,
and a full References slide at the end. Legend: ✅ = re-verified at source today · 📋 = verified
earlier in our record (SLIDE_v16 / prior), not re-checked today · ⚠️ = unresolved, do not use yet.*

---

## Slide 3 — What are embeddings? (the four examples)

- ✅ **BERT** — Devlin J., Chang M.-W., Lee K., Toutanova K. *BERT: Pre-training of Deep
  Bidirectional Transformers for Language Understanding.* **NAACL-HLT 2019**, pp. 4171–4186.
  (Google AI Language; arXiv 2018.) → slide placeholder "google" = **2019** (NAACL); use 2018 only
  if you cite the arXiv preprint.
- ✅ **CLIP** — Radford A. et al. *Learning Transferable Visual Models From Natural Language
  Supervision.* **ICML 2021.** (OpenAI.) → placeholder "OpenAI" = **2021**.
- ✅ **ProtTrans** — Elnaggar A. et al. *ProtTrans: Toward Understanding the Language of Life
  Through Self-Supervised Learning.* **IEEE Transactions on Pattern Analysis and Machine
  Intelligence (TPAMI)** 44(10):7112–7127, **2022.** doi:10.1109/TPAMI.2021.3095381.
  ⚠️ *Title trap:* the arXiv/bioRxiv title is "*Towards Cracking the Language of Life's Code…*";
  the **published** TPAMI title is "*Toward Understanding…*". Use the published one. Journal =
  **IEEE TPAMI**, not "IEEE".
- ✅ **ESM** — Lin Z. et al. *Evolutionary-scale prediction of atomic-level protein structure with a
  language model.* **Science** 379(6637):1123–1130, **2023.** doi:10.1126/science.ade2574.
  *(This is ESM-2 / ESMFold — the "Science" paper the professor means. Note: the ESM embedding
  paper often cited is Rives et al., PNAS 2021 — but the placeholder says Science, so Lin 2023.)*

## Slide 4 — String comparison ↔ sequence embeddings (Fenoy)

- 📋 **Fenoy E., Edera A. A., Stegmayer G.** *Transfer learning in proteins: evaluating novel
  protein learned representations for bioinformatics tasks.* **Briefings in Bioinformatics**
  23(4):bbac232, **2022.** *(Journal = Briefings in Bioinformatics, NOT "Oxford Academic".)*
  - **Distance answer for the "eucl? or angular?" blank: cosine similarity.** ρ = 0.66 is
    ESM cosine vs **BLASTp identity**; the 0.66 row is **ESM-1b**. Data = CAFA3 subset, 9,479
    human proteins ≤700 aa.
- ✅ **BLAST** — Altschul S. F., Gish W., Miller W., Myers E. W., Lipman D. J. *Basic local
  alignment search tool.* **Journal of Molecular Biology** 215(3):403–410, **1990.**
  doi:10.1016/S0022-2836(05)80360-2.
- ✅ **MMseqs2** (scaling tool) — Steinegger M., Söding J. *MMseqs2 enables sensitive protein
  sequence searching for the analysis of massive data sets.* **Nature Biotechnology**
  35(11):1026–1028, **2017.** doi:10.1038/nbt.3988.

## Slide 5 — The four (five) approaches — all 📋 verified in SLIDE_v16

- **Vinden N., Foxcroft J., Antonie L.** *Analysing Siamese Neural Network Architectures for
  Computing Name Similarity.* **IJPDS** 7(3):301, **2022.** *(⚠️ exact success metric not stated
  in the 1-page paper — keep that cell generic.)*
- **Dai X., Yan X., Zhou K., Wang Y., Yang H., Cheng J.** *Convolutional Embedding for Edit
  Distance* (**CNN-ED**). **SIGIR 2020**, pp. 599–608. doi:10.1145/3397271.3401045. *(conference.)*
- **Fenoy et al.** — see slide 4.
- **Corso G., Ying R., Pándy M., Veličković P., Leskovec J., Liò P.** *Neural Distance Embeddings
  for Biological Sequences* (**NeuroSEED**). **NeurIPS 2021.** (arXiv 2109.09740.)
- **Ohtomo T., Takasu A., Akutsu T.** *Computing Hamming and Levenshtein Distances Using ReLU
  Neural Networks.* **IEEE Access** 13:210089, **2025.** *(origin/existence-proof slide, not the
  peer table.)*

## Slide 8 — Synthetic training data (statistical floor)

- ✅ **Chvátal V., Sankoff D.** *Longest common subsequences of two random sequences.* **Journal of
  Applied Probability** 12(2):306–315, **1975.** → the floor exists: `E[LCS]/n → γ_k`.
- ✅ **Kiwi M., Loebl M., Matoušek J.** *Expected length of the longest common subsequence for large
  alphabets.* **Advances in Mathematics** 197(2):480–498, **2005.** → `γ_k √k → 2` (the `1/√k`
  law; fewer letters ⇒ higher floor — explains BAND_LOW 0.30 AA vs 0.56 SS).
- ✅ **Baik J., Deift P., Johansson K.** *On the distribution of the length of the longest increasing
  subsequence of random permutations.* **J. Amer. Math. Soc.** 12:1119–1178, **1999.** → LIS
  fluctuations = Tracy–Widom (rigorous, exactly-solvable case).
- ✅ **Majumdar S. N., Nechaev S.** *Anisotropic ballistic deposition model with links to the longest
  increasing subsequence.* **Physical Review E** 72(2):020901, **2005.** → the **simplified LCS
  model** whose fluctuations are provably Tracy–Widom — the paper behind the Wikipedia line.
  ⚠️ **Honesty guard:** TW is proven only for these *simplified/solvable* models, NOT for true
  finite-alphabet LCS (open conjecture, KPZ universality). Say "the universality class," never "my
  scores are Tracy–Widom distributed." Full treatment in `SLIDE_08_synthetic_training_data.md`.
- *(optional numbers)* binary constant **0.788 ≤ γ₂ ≤ 0.826** (Lueker 2009), estimate **≈ 0.811**
  (Dixon 2013).

## Slide 9 — Test data (CATH, three alphabets)

- ✅ **CATH / CATH-S20** — Sillitoe I. et al. *CATH: increased structural coverage of functional
  space.* **Nucleic Acids Research** 49(D1):D266–D273, **2021.** doi:10.1093/nar/gkaa1079.
  *(S20 = representatives clustered at ≤20% sequence identity.)*
- ✅ **3Di alphabet / Foldseek** — van Kempen M. et al. *Fast and accurate protein structure search
  with Foldseek.* **Nature Biotechnology** 42:243–246, **2024.** doi:10.1038/s41587-023-01773-0.
  *(Senior author = M. Steinegger — the professor's "REF steinegge" resolves to this paper, NOT to
  MMseqs2.)*
- ✅ **Secondary structure (DSSP)** — Kabsch W., Sander C. *Dictionary of protein secondary
  structure: pattern recognition of hydrogen-bonded and geometrical features.* **Biopolymers**
  22(12):2577–2637, **1983.** doi:10.1002/bip.360221211.
- ℹ️ **"ferras" (SS)** — an **internal, unpublished** paper from the group; used internally for this
  group presentation. No public citation needed. (DSSP above covers the SS *assignment* itself.)

## Slide 10 — Target function (normalized Levenshtein)

- 📋 **Li Y., Liu B.** *A Normalized Levenshtein Distance Metric.* **IEEE TPAMI** 29(6), **2007.**
  *(from record; relevant if asked "why max, and is 1−d/max a metric?" — it isn't, it fails the
  triangle inequality; Li–Liu give a form that is.)*

## Slide 12 — SNNEED architecture (Siamese lineage)

- ✅ **Bromley J., Guyon I., LeCun Y., Säckinger E., Shah R.** *Signature Verification Using a
  "Siamese" Time Delay Neural Network.* **NIPS 1993.** *(Also published as Int. J. Pattern
  Recognition and Artificial Intelligence 7(4):669–688, 1993 — cite either; NIPS is the usual
  LeCun-lineage cite.)* → origin of the Siamese architecture.
- ✅ **Hadsell R., Chopra S., LeCun Y.** *Dimensionality Reduction by Learning an Invariant
  Mapping.* **CVPR 2006**, pp. 1735–1742. doi:10.1109/CVPR.2006.100. → learn a map into Euclidean
  space whose distances approximate a distance defined on the inputs = this thesis's problem
  statement.
- 📋 **Abdu-Aguye M. G. et al.** *Adaptive Pooling Is All You Need…* **IJCNN 2020.**
  doi:10.1109/IJCNN48605.2020.9207082. *(validates the AdaptiveAvgPool choice.)*

## Slide 15 — Discussion (no exact Euclidean embedding)

- ✅ **Krauthgamer R., Rabani Y.** *Improved Lower Bounds for Embeddings into L₁.* **SIAM Journal on
  Computing** 38(6):2487–2498, **2009** (prelim. **SODA 2006**, pp. 1010–1017). → edit distance on
  {0,1}ⁿ into ℓ₁ requires distortion **Ω(log n)**, where **n = string length** (ℓ₂ ↪ ℓ₁, so the
  same bound holds for Euclidean).
- ✅ **Ostrovsky R., Rabani Y.** *Low Distortion Embeddings for Edit Distance.* **Journal of the
  ACM** 54(5):Art. 23, **2007** (prelim. **STOC 2005**). → matching upper bound
  2^O(√(log d · log log d)).
- ✅ **Bourgain J.** *On Lipschitz embedding of finite metric spaces in Hilbert space.* **Israel
  Journal of Mathematics** 52:46–52, **1985.** → any n-point metric ↪ ℓ₂ with distortion O(log n)
  (n = **#points**; O(log n) is essentially tight). **Keep the two n's distinct on the slide**
  (Krauthgamer–Rabani n = string length vs Bourgain n = #points).

---

## Notes / open
- ~~"REF ferras"~~ RESOLVED: internal unpublished group paper — no public citation needed.
- **BERT year** — 2018 (arXiv) or 2019 (NAACL)? Recommend **2019 (NAACL)** as the published venue.
