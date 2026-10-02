"""Build an OpenRouter chat-completions payload; no network or credential access."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def format_request(stage_request):
    settings=json.loads((ROOT/'data/evaluation/fm_settings_v1.0.json').read_text(encoding='utf-8'))
    return {'model':settings['model'],'temperature':settings['temperature'],
            'max_tokens':stage_request['max_tokens'],'stream':False,
            'messages':stage_request['messages'],'provider':settings['provider'],
            'response_format':{'type':'json_schema','json_schema':{'name':stage_request['schema_name'],
                'strict':True,'schema':stage_request['schema']}}}
