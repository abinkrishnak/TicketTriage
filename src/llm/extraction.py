"""Build a bounded extraction request. No policy or gold label enters this call."""
from pathlib import Path
from .schemas import EXTRACTION_SCHEMA
ROOT=Path(__file__).resolve().parents[2]
def build_extraction(query_text):
    import json
    if not isinstance(query_text,str) or not query_text.strip():raise ValueError('Empty query')
    return {'messages':[{'role':'system','content':(ROOT/'prompts/extraction_prompt_v1.txt').read_text(encoding='utf-8')},
                        {'role':'user','content':json.dumps({'customer_request':query_text},ensure_ascii=False)}],
            'schema':EXTRACTION_SCHEMA,'schema_name':'ticket_extraction_v1','max_tokens':900}
def extract(client,query_text,case_id):
    return client.call('extraction',case_id,**build_extraction(query_text))
