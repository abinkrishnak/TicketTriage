"""Draft from one explicitly selected card. No retrieval rank is treated as authority."""
from pathlib import Path
import json
from .schemas import GENERATION_SCHEMA
ROOT=Path(__file__).resolve().parents[2]
def build_generation(query_text,extraction,policy,*,selection_basis):
    if selection_basis not in {'gold_component_evaluation','human_reviewed_selection'}:
        raise ValueError('An explicit gold-evaluation or human-reviewed policy selection is required')
    if policy.get('review_status')!='approved_for_academic_demo':raise ValueError('Unapproved policy')
    payload={'customer_request':query_text,'structured_extraction':extraction,
             'policy_id':policy['policy_id'],'policy_version':policy['version'],'supplied_policy':policy}
    return {'messages':[{'role':'system','content':(ROOT/'prompts/grounded_generation_prompt_v1.txt').read_text(encoding='utf-8')},
                        {'role':'user','content':json.dumps(payload,ensure_ascii=False)}],
            'schema':GENERATION_SCHEMA,'schema_name':'grounded_draft_v1','max_tokens':1100}
def generate(client,query_text,extraction,policy,case_id,*,selection_basis):
    return client.call('generation',case_id,**build_generation(query_text,extraction,policy,selection_basis=selection_basis))
