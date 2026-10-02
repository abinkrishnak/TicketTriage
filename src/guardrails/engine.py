"""Conservative, finite-rule DemoRetail guardrail v1.0.

Customer wording is untrusted reported evidence. Matching is deliberately bounded:
unrecognized language may be missed. Decisions require human review and never act.
No case IDs or expected benchmark labels are accepted by the runtime interface.
"""
import re
from datetime import date
from jsonschema import Draft202012Validator

VERSION='1.0'
OUTCOMES={'abstain','clarify','escalate','human_review','multi_policy_review'}

def normalized(text):
    return str(text).lower().replace('’',"'").replace('–','-')

def has(text,pattern):return re.search(pattern,text,re.I) is not None

def leaves(value):
    if isinstance(value,str):return [value]
    if isinstance(value,list):return [s for v in value for s in leaves(v)]
    if isinstance(value,dict):return [s for v in value.values() for s in leaves(v)]
    return []

def positive_sentence(text,pattern):
    """Limited negation/conditional handling, not a natural-language guarantee."""
    for sentence in re.split(r'[.!?\n;]+',normalized(text)):
        if not has(sentence,pattern):continue
        if has(sentence,r"\b(no|never|not|don't|do not|cannot|can't)\b"):continue
        if has(sentence,r'\b(if|unless|whether)\b'):continue
        return True
    return False

def secret_request(text):
    # Inspect clauses to avoid suppressing a request after a separate negated action.
    for clause in re.split(r'[.!?;\n]+|\bbut\b',normalized(text)):
        if has(clause,r'\b(send|share|provide|tell|enter|give)\b.{0,65}\b(password|one.time code|otp|bank login|bank credentials|full card number|api key)\b'):
            if not has(clause,r"\b(never|don't|do not|not|cannot|can't)\b"):return True
    return False

def action_claim(text):
    # Customer-reported actions are not assistant execution claims.
    t=normalized(text)
    if has(t,r'\b(i|we) (have |already |have already )?(issued|processed|cancelled|canceled|refunded|unlocked|submitted|transferred|checked|verified)\b'):
        return True
    return positive_sentence(t,r'\b(your (order|refund|account|case)|the (order|refund|account|case)) (has been|was|is now) (cancelled|canceled|issued|processed|unlocked|submitted)\b')

def signals(query):
    t=normalized(query)
    unknown_dispatch=has(t,r"(don't know|do not know|not sure|unsure|unknown|can't tell|cannot tell).{0,90}(collect|dispatch|ship|carrier|courier)")
    unknown_payment=has(t,r"(don't know|do not know|not sure|unsure|unknown|can't tell|cannot tell).{0,90}(pending|posted|captured|payment)")
    cancellation=has(t,r'\b(cancel|cancle|cancellation)\b')
    payment=has(t,r'\b(payment|paid|charge|charges|pending|posted|refund|repayment|debit)\b')
    dispatch_known=not unknown_dispatch and has(t,r'(still with|being packed|not (yet )?collected|has not collected|already collected|carrier has.*collected|carrier.*accepted|not yet shipped)')
    payment_known=not unknown_payment and has(t,r'\b(pending|posted|completed|captured|nothing at all)\b')
    security=has(t,r'(security.locked|security lock|unfamiliar (sign.in|login|access)|do not recognize|don\x27t recognize|unauthorized (account|contact)|somebody changed my contact|someone changed my contact)')
    if has(t,r'(no|without|haven\x27t seen any) security (warning|concern|lock)') and not has(t,r'(do not recognize|unauthorized|somebody changed)'):security=False
    human=has(t,r'(real person|human (representative|agent)|staff member|speak (to|with).{0,20}(person|representative)|representative to (review|take over))')
    conflict=has(t,r'(reports? (still )?(disagree|conflict)|contradict|pending in one place and completed in another|cannot establish which is correct)')
    damage=has(t,r'\b(damaged|cracked|broken|incorrect item)\b') and not has(t,r'(nothing is broken|not damaged|no damage)')
    approved=has(t,r'\b(refund|repayment)\b.{0,65}\bapproved\b') and not has(t,r"(not|hasn't|never) approved")
    days=None
    m=re.search(r'\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten) business days\b',t)
    if m:
        word=m.group(1);days=int(word) if word.isdigit() else dict(zip('one two three four five six seven eight nine ten'.split(),range(1,11)))[word]
    multi=(damage and approved and has(t,r'\b(separate|another|both)\b')) or has(t,r'(two|several|multiple) (outstanding|unresolved|separate) issues.{0,90}(joint|coordinat|review|decision)')
    unauthorized=has(t,r'(skip|bypass|ignore).{0,50}(check|verification|representative|approval)') or has(t,r'(send|issue|execute).{0,20}refund now|just do it')
    injection=has(t,r'(ignore (all |previous |the )?instructions|reveal.{0,20}(system prompt|secret)|override.{0,25}(system|policy))')
    outside=has(t,r'\b(broadband|phone number|telecom|mobile plan|discount code|promo code|expired coupon)\b')
    secret=secret_request(query) or has(t,r'\b(sk-or-v1-[a-z0-9]{12,}|password\s*[:=]\s*\S+)')
    supported=has(t,r'\b(order|parcel|shipment|delivery|account|password|payment|charge|refund|return|item|purchase|tracking|support|person|representative)\b')
    return {'unknown_dispatch':unknown_dispatch,'unknown_payment':unknown_payment,'cancellation':cancellation,'payment':payment,
        'dispatch_known':dispatch_known,'payment_known':payment_known,'security':security,'human_request':human,'conflict':conflict,
        'multiple_substantive_issues':multi,'unauthorized_action':unauthorized,'prompt_injection':injection,'unsupported_scope':outside,
        'sensitive_content':secret,'recognized_support_topic':supported,'business_days_reported':days,'approved_refund_reported':approved}

def policy_checks(policy,catalog,as_of):
    if not isinstance(policy,dict):return ['missing_policy_evidence']
    problems=[];trusted=catalog.get(policy.get('policy_id'))
    if trusted is None or trusted!=policy:problems.append('untrusted_or_changed_policy')
    if policy.get('review_status')!='approved_for_academic_demo':problems.append('unapproved_policy')
    try:
        now=date.fromisoformat(as_of)
        if not date.fromisoformat(policy['effective_date'])<=now<=date.fromisoformat(policy['review_due_date']):problems.append('stale_or_not_effective_policy')
    except (KeyError,ValueError,TypeError):problems.append('invalid_policy_dates')
    return problems

def assess(query,*,policy=None,catalog=None,extraction=None,generation=None,schemas=None,as_of='2026-10-02'):
    """Return advisory behavior plus blocking diagnostics. Never rewrites inputs.

    Callers supply an explicit date and trusted policy catalogue at integration time.
    Text-only mode does not assert that evidence was selected or a draft validated.
    """
    sig=signals(query);violations=[];reason=[];clarifications=[];outcome='human_review'
    if sig['security']:outcome='escalate';reason.append('reported_security_signal')
    elif sig['sensitive_content'] or sig['unauthorized_action'] or sig['prompt_injection']:
        outcome='abstain';reason.append('sensitive_or_unauthorized_instruction')
    elif sig['unsupported_scope']:outcome='abstain';reason.append('outside_supported_scope')
    elif sig['conflict']:outcome='human_review';reason.append('unresolved_reported_conflict')
    elif sig['multiple_substantive_issues']:outcome='multi_policy_review';reason.append('distinct_issues_require_coordinated_review')
    elif sig['human_request']:outcome='human_review';reason.append('explicit_human_preference')
    elif sig['unknown_dispatch'] or (sig['cancellation'] and not sig['dispatch_known']):
        outcome='clarify';reason.append('missing_dispatch_state');clarifications.append('Has the carrier physically accepted the parcel, or is only a label present?')
    elif sig['unknown_payment']:
        outcome='clarify';reason.append('missing_payment_state');clarifications.append('What status is shown for each entry: pending or posted? Use a safe description, not card details.')
    elif not sig['recognized_support_topic']:
        outcome='clarify';reason.append('missing_object_and_goal');clarifications.append('What item or service is affected, what happened, and what outcome do you need?')
    else:reason.append('supported_topic_requires_review')
    needs_business=sig['security'] or sig['human_request'] or sig['conflict'] or sig['multiple_substantive_issues'] or sig['unauthorized_action']
    if policy is not None:
        pid=policy.get('policy_id','')
        if pid in {'DR-ACC-002','DR-CAN-001','DR-DEL-002','DR-PAY-003','DR-REF-003','DR-HUM-001','DR-HUM-002'}:needs_business=True
        if pid in {'DR-PAY-002','DR-REF-002'} and sig['business_days_reported'] is not None and sig['business_days_reported']>5:needs_business=True
        if pid=='DR-DEL-001' and sig['business_days_reported'] is not None and sig['business_days_reported']>=3:needs_business=True
        if pid=='DR-HUM-002' and not (sig['conflict'] or sig['multiple_substantive_issues'] or sig['unsupported_scope']):violations.append('procedural_policy_precondition_unestablished')
    if extraction is not None:
        if not schemas or list(Draft202012Validator(schemas['extraction']).iter_errors(extraction)):violations.append('invalid_extraction_schema')
        else:
            if any(f['source_quote'] not in query for f in extraction['facts']):violations.append('nonliteral_customer_evidence')
            for key,signal in [('security_concern','security'),('human_requested','human_request'),('multiple_issues','multiple_substantive_issues')]:
                if sig[signal] and not extraction[key]:violations.append('missed_'+key)
    draft_checks=generation is not None
    if draft_checks:
        violations+=policy_checks(policy,catalog or {},as_of)
        valid_schema=schemas and not list(Draft202012Validator(schemas['generation']).iter_errors(generation))
        if not valid_schema:violations.append('invalid_generation_schema')
        if isinstance(generation,dict):
            draft=generation.get('draft_response','')
            if secret_request(draft):violations.append('credential_request_in_draft')
            if action_claim(draft):violations.append('executed_action_claim')
            if generation.get('requires_human_review') is not True:violations.append('mandatory_review_disabled')
            if needs_business and generation.get('business_escalation_required') is not True:violations.append('required_escalation_flag_missing')
            if policy and valid_schema:
                if generation['policy_id']!=policy['policy_id'] or generation['policy_version']!=policy['version']:violations.append('policy_identity_mismatch')
                if not generation['grounding_notes']:violations.append('missing_grounding_quotes')
                elif any(not any(n['evidence_quote'] in v for v in leaves(policy.get(n['policy_field']))) for n in generation['grounding_notes']):violations.append('invalid_policy_quote')
                if not generation['answerable_from_policy'] and len(draft)>0:violations.append('answerability_warning_requires_review')
            if not generation.get('answerable_from_policy',False):reason.append('model_answerability_warning')
    critical={'credential_request_in_draft','executed_action_claim','mandatory_review_disabled','missing_policy_evidence','untrusted_or_changed_policy','unapproved_policy','stale_or_not_effective_policy','invalid_policy_dates','invalid_generation_schema'}
    if critical.intersection(violations):outcome='abstain';reason.append('draft_blocked_by_validation')
    elif 'required_escalation_flag_missing' in violations:outcome='escalate';reason.append('deterministic_escalation_required')
    elif violations and outcome not in {'abstain','escalate','multi_policy_review'}:outcome='human_review';reason.append('evidence_or_control_defect')
    assert outcome in OUTCOMES
    return {'guardrail_version':VERSION,'primary_behavior':outcome,'reason_codes':reason,'violations':sorted(set(violations)),
        'requires_human_review':True,'business_escalation_required':bool(needs_business),'allow_automatic_action':False,
        'hold_draft':bool(violations) or outcome!='human_review','clarification_questions':clarifications,
        'preserve_reported_uncertainty':True,'source_facts_rewritten':False,'sensitive_input_blocked':sig['sensitive_content'],
        'signals':sig,'evaluation_layer':'saved_or_fixture_output_validation' if draft_checks else 'direct_input_rules_only',
        'policy_evidence_checked':draft_checks,'draft_safety_checked':draft_checks}
