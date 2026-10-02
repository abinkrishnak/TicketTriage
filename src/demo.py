"""Offline demo adapters. No API clients, credential loading or artifact writes."""
from pathlib import Path
from functools import lru_cache
import csv,hashlib,json,os

ROOT=Path(__file__).resolve().parents[1]
REV='1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
for key in ['HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE','HF_HUB_DISABLE_TELEMETRY']:
    os.environ[key]='1'
os.environ['TOKENIZERS_PARALLELISM']='false'

DEMOS={
    'P13':'P13 · Damaged item — useful draft',
    'P04':'P04 · After-dispatch cancellation — confusable retrieval',
    'C05':'C05 · Account security — escalation',
    'C36':'C36 · Overdue refund — missed escalation flag',
    'A03':'A03 · Unknown dispatch state — clarification',
    'A01':'A01 · Expired discount — abstention',
}
class DemoError(Exception):pass

def json_file(relative):
    try:return json.loads((ROOT/relative).read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:raise DemoError(f'Cannot read {relative}. Restore the project file and restart the app.') from None

def rows(relative):
    try:
        with (ROOT/relative).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
    except (OSError,ValueError):raise DemoError(f'Cannot read {relative}. Restore the project file and restart the app.') from None

def verify(relative,expected):
    try:actual=hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()
    except OSError:raise DemoError(f'Missing local file: {relative}. Restore it; this app never downloads models.') from None
    if actual!=expected:raise DemoError(f'Integrity check failed: {relative}. Restore the frozen original; do not retrain or overwrite it.')

def runtime_verify(relative):
    manifest=json_file('data/demo/runtime_manifest.json')
    verify(relative,manifest['sha256'][relative])

@lru_cache(maxsize=1)
def cards():
    path='data/playbook/demoretail_policies.v1.1.json'
    runtime_verify(path)
    return {p['policy_id']:p for p in json_file(path)['policies']}

@lru_cache(maxsize=1)
def bundle():
    runtime_verify('data/demo/saved_examples.json')
    runtime_verify('src/guardrails/engine.py')
    return json_file('data/demo/saved_examples.json')['examples']

def saved_query(case_id):
    return bundle()[case_id]['query_text']

def saved_classifier(case_id):
    return bundle()[case_id]['classifier']

@lru_cache(maxsize=1)
def classifier():
    import joblib
    runtime_verify('models/intent_tfidf_logreg.joblib')
    try:return joblib.load(ROOT/'models/intent_tfidf_logreg.joblib')
    except Exception:raise DemoError('The classifier could not load. Install requirements.txt in the project virtual environment.') from None

def classify(query):
    try:
        model=classifier();p=model.predict_proba([query])[0]
        return sorted([{'category':str(c),'probability':float(v)} for c,v in zip(model.classes_,p)],key=lambda x:-x['probability'])
    except DemoError:raise
    except Exception:raise DemoError('Local classification failed. Check the project environment; saved evidence remains available.') from None

def saved_rankings(case_id):
    return bundle()[case_id]['rankings']

@lru_cache(maxsize=1)
def local_encoder():
    path=Path(os.environ.get('TICKETTRIAGE_MODEL_DIR',str(ROOT/'.local_runtime/models/all-MiniLM-L6-v2'/REV)))
    runtime_verify('data/demo/semantic_model_assets.json')
    assets=json_file('data/demo/semantic_model_assets.json')
    for name,meta in assets['files'].items():verify(str(path/name),meta['sha256'])
    try:
        import torch
        from sentence_transformers import SentenceTransformer
        torch.set_num_threads(4)
        model=SentenceTransformer(str(path),device='cpu',local_files_only=True,trust_remote_code=False)
        model.max_seq_length=512;model.eval()
        return model
    except Exception:raise DemoError('Local MiniLM could not load. Use saved replay or restore the pinned local model and requirements-local.txt. No download was attempted.') from None

def local_candidates(query):
    # Reuse the exact saved policy vectors; no corpus edits or benchmark reruns.
    import numpy as np
    cs=cards()
    runtime_verify('results/retrieval/semantic_embeddings_v1.0.npz')
    model=local_encoder()
    length=len(model.tokenizer(query,add_special_tokens=True,truncation=False)['input_ids'])
    if length>512:raise DemoError(f'Ticket contains {length} tokens; the locked limit is 512. Shorten it. No text was truncated.')
    v=model.encode([query],normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)[0]
    with np.load(ROOT/'results/retrieval/semantic_embeddings_v1.0.npz',allow_pickle=False) as data:pe=data['policy_embeddings']
    scores=pe@v;order=np.argsort(-scores,kind='stable')[:3];ids=list(cs)
    return [{'rank':i+1,'policy_id':ids[j],'cosine_similarity':float(scores[j])} for i,j in enumerate(order)]

def saved_evidence(case_id):
    record=bundle()[case_id]
    if record['generation'] is not None:
        if record['generation']['policy_id'] not in cards():
            raise DemoError('The saved draft policy is absent from the verified playbook.')
    return {k:record[k] for k in ['guardrail','policy_id','extraction','generation','human']}
