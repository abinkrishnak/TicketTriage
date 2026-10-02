"""Strict structured-output contracts. Schema validity is not factual correctness."""
def obj(properties):
    return {'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}
STR={'type':'string'}
BOOL={'type':'boolean'}
def array(items=STR):return {'type':'array','items':items}
def enum(values):return {'type':'string','enum':values}
EXTRACTION_SCHEMA=obj({
 'customer_goal':STR,'issue_summary':STR,
 'high_level_issue':enum(['account_access','cancellation','delivery','payment','refund','human_support','multiple','unknown']),
 'facts':array(obj({'fact':STR,'source':enum(['explicit_customer_text']),'source_quote':STR})),
 'missing_information':array(),'conflicts':array(),
 'risk_flags':array(enum(['security_concern','conflicting_reports','multiple_issues','unauthorized_action_requested','sensitive_credentials','insufficient_information'])),
 'security_concern':BOOL,'human_requested':BOOL,'multiple_issues':BOOL,'uncertainty_notes':array()})
GENERATION_SCHEMA=obj({
 'policy_id':STR,'policy_version':STR,'answerable_from_policy':BOOL,'missing_information':array(),
 'requires_human_review':{'type':'boolean','enum':[True]},'business_escalation_required':BOOL,
 'risk_flags':array(enum(['policy_mismatch','security_concern','conflicting_reports','multiple_issues','unauthorized_action_requested','sensitive_credentials','insufficient_information','extraction_disagreement'])),
 'draft_status':enum(['draft_for_human_review']),'draft_response':STR,
 'grounding_notes':array(obj({'policy_field':enum(['supported_issue','short_description','policy_text','eligibility_conditions','required_information','exceptions','exclusions','agent_actions','prohibited_actions','escalation_conditions','customer_facing_guidance']),'evidence_quote':STR}))})
