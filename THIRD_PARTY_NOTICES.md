# Licensing and third-party notices

## Original code

[MIT](LICENSE) applies to the original TicketTriage project code and accompanying project documentation, copyright 2026 Kaivelikkal Abin Krishna. This grant does not relicense third-party data, models, dependencies or provider-generated responses, or claim ownership of them. Project policies/questions are fictional academic material; assistant-authored and personal-query provenance is preserved in the evaluation files. Recorded GPT outputs are labeled model outputs, not original human writing.

## Bitext dataset and classifier results

Training source: [Bitext customer-support dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset/tree/430d1a89bd93bd1fa23c16f29dd53e73f0087443), revision `430d1a89bd93bd1fa23c16f29dd53e73f0087443`, v11 CSV. Publisher attribution: (c) Bitext Innovations, 2024. The archived dataset card declares [Community Data License Agreement – Sharing, Version 1.0](https://cdla.dev/sharing-1-0/). The local source, card and license archive were hash-verified for publication; [provenance](data/demo/third_party_provenance.json) records the source links and hashes.

Raw/cleaned training records and original Bitext response text are not bundled. The included `models/intent_tfidf_logreg.joblib` is a project-trained TF-IDF/logistic-regression pipeline containing learned vocabulary/weights, not a training-record archive. Classifier metric tables are computational results. CDLA-Sharing-1.0 section 1.11 defines Results (excluding more than a de minimis portion of source Data); section 3.5 imposes no restrictions on use/publication of Results. This is the documented basis for including trained results separately from source data. Upstream text or other source Data, if separately obtained or redistributed, retains CDLA-Sharing-1.0, not MIT. No ownership of Bitext wording is claimed.

## Semantic model and saved embeddings

Semantic retrieval uses [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41), pinned revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Upstream weights/tokenizer are neither bundled nor downloaded automatically; preserve their upstream terms/notices when acquiring them. The small saved embedding array is computed from this project's fictional policies/queries, not a copy of MiniLM weights. The model is third-party work, not authored by this project.

## Dependencies and provider outputs

Streamlit, jsonschema, NumPy, scikit-learn, SciPy, joblib and threadpoolctl are separately installed third-party dependencies. Optional dependencies are sentence-transformers, Transformers, PyTorch, tokenizers, huggingface-hub and safetensors. Their packages, bundled components and notices retain their own upstream licenses; no package source or wheels are redistributed here, and MIT does not override those terms. Installed package metadata was inspected locally; no new license is assigned where metadata is incomplete.

Saved extraction/generation was produced by OpenAI GPT-4o-mini through OpenRouter, with the OpenAI provider. Those providers/models are not the author's work. Saved evidence preserves original generated content and human-review labels; it does not redistribute provider model weights or provide API access.
