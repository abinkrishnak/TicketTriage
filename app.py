"""Streamlit offline MVP. No LLM transport, key loading, writes or sending tools."""
import os
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS']='false'
from datetime import date
import hashlib
import streamlit as st
from src import demo
from src.guardrails import assess
from src.guardrails.engine import policy_checks

st.set_page_config(page_title='TicketTriage · DemoRetail',page_icon='📋',layout='wide')
st.title('TicketTriage')
st.write('An academic AI prototype that helps an e-commerce support employee find relevant verified policy guidance and prepare information for human review.')
st.caption('Fictional DemoRetail · Offline only · No API key needed')
st.markdown('**How to use it**\n\n1. Choose a saved example to see previously evaluated AI outputs and human review.\n2. Choose Local ticket preview to try a new support ticket with local classification and semantic policy retrieval.')
st.info('No customer messages are sent. No refunds, cancellations or account changes are performed. New local tickets do not generate new GPT responses. Verified policy + human review remain the control points.')
with st.expander('How this works'):
    st.write('Ticket → broad classifier hint → semantic policy candidates → verified policy → structured extraction → grounded draft → guardrails → human review')
    st.write('Classifier is not policy authority. Retriever is not policy authority. LLM is not policy authority. Verified policy + human reviewer are the control points.')

def show_guard(guard,label):
    st.subheader('7 · Guardrails and human review')
    st.caption(label)
    a,b,c=st.columns(3)
    a.metric('Primary outcome',guard['primary_behavior'].replace('_',' '))
    b.metric('Business escalation','Required' if guard['business_escalation_required'] else 'Not triggered')
    c.metric('Human review','MANDATORY')
    if guard.get('hold_draft'):st.warning('Draft held for review. No response may be sent automatically.')
    else:st.info('No additional deterministic hold. Human approval is still required; this is not permission to send.')
    st.write('Reasons:',', '.join(guard['reason_codes']) or 'None recorded')
    st.write('Diagnostics:',', '.join(guard['violations']) or 'None recorded — finite checks cannot guarantee correctness.')
    for q in guard.get('clarification_questions',[]):st.write('Clarification:',q)
    with st.expander('Complete guardrail record'):st.json(guard)
    st.caption('All text is a draft or historical evidence. No refund, cancellation, account change, case submission or customer contact is performed.')

def run():
    mode=st.sidebar.radio('Mode',['Saved evidence replay','Local ticket preview'],key='mode')
    st.sidebar.markdown('**Saved evidence replay**\n\nFull demo using previously evaluated and saved AI outputs. Behavior-only examples have no saved GPT draft.\n\n**Local ticket preview**\n\nTry a new ticket using the local classifier and semantic retrieval only. No new GPT extraction or draft is generated.')
    if mode=='Saved evidence replay':
        case=st.sidebar.selectbox('Saved example',list(demo.DEMOS),format_func=demo.DEMOS.get,key='example')
        original=demo.saved_query(case)
        ticket=st.text_area('1 · Ticket text',value=original,height=130,key='ticket_'+case,max_chars=3000)
        if ticket!=original:
            st.warning('Ticket edited: saved results are not valid for this text. Restore the example or switch to Local ticket preview. No saved draft is reused.')
            return
        evidence=demo.saved_evidence(case)
    else:
        case=None;evidence=None
        suggestions=['My parcel says delivered, but I have not received it.','My card shows two completed charges for one order.','Someone changed the contact details on my account.']
        with st.expander('Try a suggested ticket'):
            for i,text in enumerate(suggestions):
                if st.button(text,key='suggest_'+str(i)):
                    st.session_state['local_ticket']=text
                    st.session_state.pop('analyzed_ticket',None)
        ticket=st.text_area('1 · Ticket text',height=130,max_chars=3000,key='local_ticket',placeholder='Use only fictional or generalized support text.')
        st.caption('New text stays local and is not written to a file. Use no credentials or real customer details.')
        if not ticket.strip():st.info('Enter a ticket to preview local routing.');return
        if not st.button('Analyze locally',key='analyze') and st.session_state.get('analyzed_ticket')!=ticket:return
        st.session_state['analyzed_ticket']=ticket
        guard=assess(ticket)
        if guard['signals']['unsupported_scope'] or not guard['signals']['recognized_support_topic']:
            st.warning('This request does not appear to match the supported DemoRetail support topics.')
            st.write('Supported topics: account access, cancellation, delivery, payment, refund, and human-support requests.')
            st.caption('UI heuristic — not a validated OOD detector. It uses finite deterministic topic signals, not a classifier confidence threshold. Novel unsupported wording can still be misclassified or clarified rather than abstained.')
            st.info('Please describe a DemoRetail support issue. Policy candidates are hidden to avoid presenting unrelated guidance.')
            with st.expander('Technical diagnostics — not valid policy guidance'):
                try:st.dataframe(demo.classify(ticket),hide_index=True)
                except demo.DemoError as e:st.warning(str(e))
                st.caption('The classifier has no OOD class and must choose a known category. These probabilities do not establish relevance.')
                st.json(guard)
            show_guard(guard,'Original Guardrails v1.0 input-only outcome. The UI warning does not change this outcome or any evaluation label.')
            return
    st.subheader('2 · Broad classifier hint')
    try:
        scores=demo.saved_classifier(case) if case else demo.classify(ticket)
        st.metric('Suggested category',scores[0]['category'])
        st.caption(f"Model probability: {scores[0]['probability']:.1%}"+(' · saved local prediction' if case else ' · local prediction'))
        st.caption('Uncalibrated probability, not certainty or scope detection. This hint never filters retrieval.')
        with st.expander('All six class probabilities'):st.dataframe(scores,hide_index=True)
    except demo.DemoError as e:st.warning(str(e))
    cs=demo.cards()
    st.subheader('3 · Semantic policy candidates')
    try:
        if case:
            candidates=demo.saved_rankings(case)
            st.caption('Saved Stage 7 ranking · all 15 policies competed · no classifier filtering')
            if not candidates:st.info('This behavior-only example has no saved semantic ranking. No candidate or gold policy is invented.')
        else:
            with st.spinner('Reading the local pinned MiniLM model…'):candidates=demo.local_candidates(ticket)
            st.caption('Local preview only; no evaluation scores updated. MiniLM pinned revision, 512-token maximum, saved policy vectors, all policies compete.')
        if candidates:st.dataframe([{**r,'title':cs[r['policy_id']]['title']} for r in candidates],hide_index=True)
        st.caption('Cosine similarity is not confidence or approval. Inspect candidates; top-1 can be wrong.')
    except demo.DemoError as e:st.warning(str(e))
    st.subheader('4 · Explicit verified-policy selection')
    identity=hashlib.sha256(ticket.encode()).hexdigest()[:12]
    selected=st.selectbox('Choose a policy after reviewing its applicability',[None]+list(cs),format_func=lambda p:'No policy selected' if p is None else p+' · '+cs[p]['title'],key='policy_'+identity)
    confirmed=False
    if selected:
        card=cs[selected]
        st.write(f"**{selected} · {card['title']} · card v{card['version']}**")
        st.caption('Frozen Playbook v1.1 · fictional academic approval')
        with st.expander('Inspect complete policy',expanded=True):
            st.write(card['policy_text']);st.write('Eligibility:',card['eligibility_conditions']);st.write('Escalation:',card['escalation_conditions']);st.json(card,expanded=False)
        problems=policy_checks(card,cs,date.today().isoformat())
        if problems:st.error('Policy cannot support current drafting: '+', '.join(problems))
        else:confirmed=st.checkbox('I reviewed this policy and selected it for this ticket.',key='confirm_'+identity+'_'+selected)
    st.subheader('5 · Structured extraction')
    matching=evidence and evidence['extraction'] is not None
    if matching:
        st.caption('Unedited saved GPT-4o-mini extraction for this exact ticket. No new call.')
        st.json(evidence['extraction'],expanded=False)
    else:st.info('No saved foundation-model extraction for this ticket. Offline mode does not invent one.')
    st.subheader('6 · Grounded draft response')
    if matching and selected==evidence['policy_id'] and confirmed:
        st.caption('Historical Stage 8 GOLD-card component output. Your selection enables replay; it does not cause fresh generation. Guardrails below retain observed defects.')
        st.text(evidence['generation']['draft_response'])
        with st.expander('Complete unedited generation output'):st.json(evidence['generation'])
        h=evidence['human'];st.caption(f"Abin’s final review: extraction {h['human_extraction_rating']} · generation {h['human_generation_rating']} · escalation {h['human_escalation_correct']}")
        st.write('Review note:',h['notes'])
    elif matching:
        st.warning('Draft replay locked. Select and confirm the original supplied policy '+evidence['policy_id']+'. A saved response will not be attached to a different policy.')
    else:st.info('No saved LLM draft exists. Local preview cannot generate or send a response.')
    if evidence:
        show_guard(evidence['guardrail'],'Saved Stage 9 evidence for the original ticket '+('and original gold policy '+evidence['policy_id'] if evidence['policy_id'] else '(direct-input rules only)')+'. Not recomputed; not validation of a different selection.')
    else:
        show_guard(assess(ticket),'Current local input-only check. No draft/evidence validation occurred; policy selection does not generate a response.')

try:run()
except demo.DemoError as e:st.error(str(e));st.info('Restore the named local artifact, then restart. No model download or paid fallback will occur.')
except Exception:st.error('A local component could not be read. Restart with the project virtual environment and check the demo guide. No API call or business action was attempted.')
