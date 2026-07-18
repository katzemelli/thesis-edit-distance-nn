# Slide 3 — What are embeddings?

*Build doc. Prof's layout: definition + four named examples (BERT / CLIP / ProtTrans / ESM) with
citations. Citations verified 2026-07-18 (`REFERENCES_verified.md`).*

---

## Where it sits
Second concept slide. Defines the tool (embeddings) before slide 4 asks whether embeddings already
capture sequence similarity.

## On the slide

**Definition (top, the load-bearing line):**
> An **embedding** maps an object to a **vector**, so that **distance between vectors reflects
> similarity between the underlying objects**.

**Examples (with citations under each — the prof audits references):**
| domain | model | citation |
|---|---|---|
| **text** | BERT | Devlin et al., *BERT: Pre-training of Deep Bidirectional Transformers…*, **NAACL, 2019** (Google) |
| **image** | CLIP | Radford et al., *Learning Transferable Visual Models From Natural Language Supervision*, **ICML, 2021** (OpenAI) |
| **protein sequence** | ProtTrans | Elnaggar et al., *ProtTrans: Toward Understanding the Language of Life…*, **IEEE TPAMI, 2022** |
| **protein sequence** | ESM(-2) | Lin et al., *Evolutionary-scale prediction of atomic-level protein structure…*, **Science, 2023** |

## Stage script (~45 s)
"An embedding turns an object — a word, an image, a protein — into a vector, trained so that
*distance between the vectors mirrors similarity between the objects*. It's everywhere: BERT does it
for text, CLIP for images, and for proteins there's ProtTrans and ESM. The key thing to notice is
*what* each of these is trained for — none of them was trained on edit distance. So the natural
question is: do these vectors, trained for their own objectives, already preserve *string*
similarity? That's the next slide."

## Guardrails
- **BERT year:** use **2019 (NAACL)**, the published venue (not 2018 arXiv) — recommended default.
- **ProtTrans:** journal is **IEEE TPAMI**, not "IEEE"; published title is "*Toward Understanding…*"
  (the arXiv "*Towards Cracking…*" is different — use the published one).
- **ESM = Lin et al., Science 2023** (ESM-2). If asked, the original ESM *representation* paper is
  Rives et al., PNAS 2021 — but the prof's placeholder says "Science," so Lin 2023 is correct here.
