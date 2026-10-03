"""Portfolio presentation over unchanged saved evidence and local decision components."""
import os
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS']='false'
from datetime import date
import hashlib
import streamlit as st
from src import demo
from src.guardrails import assess
from src.guardrails.engine import policy_checks

SOURCE='https://github.com/abinkrishnak/TicketTriage'
PAGES=['Demo','How it works','Evaluation','Governance & limitations','About project']
EXAMPLES={
 'P13':('Damaged / incorrect item','Explore a useful draft, its policy evidence and the human reviewer’s noted limitation.'),
 'P04':('After-dispatch cancellation','Compare similar policies: the saved top-ranked candidate is not the gold policy.'),
 'C05':('Account security escalation','Inspect security guidance and the saved model’s mismatch-flag defect.'),
 'C36':('Overdue refund / missed escalation','See the model’s missed escalation alongside the independent control evidence.'),
 'A03':('Unknown dispatch state','See a clarification outcome; this behavior-only case has no saved GPT draft.'),
 'A01':('Unsupported discount','See an abstention outcome; this behavior-only case has no saved GPT draft.'),
}
STATES={'abstain':'Abstain / unsupported','clarify':'Clarification required','escalate':'Escalation required','human_review':'Human review required','multi_policy_review':'Multi-policy review'}
STORIES={'abstain':'The recorded controls stop guidance at an unsupported or unsafe boundary.','clarify':'A decisive reported fact is missing; clarify it instead of guessing.','escalate':'The controls require business or specialist review before proceeding.','human_review':'A support employee must review the evidence and decide the next step.','multi_policy_review':'Several substantive issues need coordinated policy review.'}
st.set_page_config(page_title='TicketTriage',page_icon='📋',layout='wide')
st.markdown('''<style>
.stApp {background:#f7f9fc;color:#172b4d}
h1,h2,h3 {color:#142b49;letter-spacing:-.025em}
.block-container {max-width:1440px;padding-top:2rem;padding-bottom:3rem}
[data-testid="stSidebar"] {background:#edf2f7}
[data-testid="stVerticalBlockBorderWrapper"] {background:white;border-radius:14px}
[data-testid="stMetric"] {background:white;border:1px solid #dde5ee;border-radius:12px;padding:16px}
.badge {display:inline-block;background:#e8eef6;border:1px solid #d7e1ec;color:#294563;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;letter-spacing:.04em}
.disclosure {border-left:3px solid #7892ad;background:#edf3f8;padding:12px 16px;border-radius:8px;font-size:14px;color:#344e68;margin:12px 0 22px}
.flow {padding:16px;background:#edf3f8;border-radius:12px;line-height:2;color:#234969}
</style>''',unsafe_allow_html=True)

def go(page):st.session_state['page']=page

def final_control():
    with st.container(border=True):
        st.markdown('### Human decision required')
        st.write('TicketTriage provides evidence and a draft. The support employee remains responsible for the final response and any business action.')
        st.caption('No auto-send, refund, cancellation, account change or case submission exists.')

def guard_card(guard,saved):
    with st.container(border=True):
        st.markdown('### 5 · Guardrails / review')
        title=STATES.get(guard['primary_behavior'],guard['primary_behavior'])
        if guard['primary_behavior'] in ['abstain','clarify','escalate','multi_policy_review']:st.warning(title)
        else:st.info(title)
        st.write(STORIES.get(guard['primary_behavior'],'Review the recorded control decision.'))
        st.caption('Saved control evidence for the original case/policy; not recomputed for another selection.' if saved else 'Current input-only checks; no draft or selected-policy validation was performed.')
        st.write('Business escalation: **'+('Required' if guard['business_escalation_required'] else 'Not triggered')+'** · Human review: **Mandatory**')
        if guard.get('hold_draft'):st.warning('Draft held for review. This is not permission to send.')
        else:st.caption('No additional deterministic hold. This does not establish correctness or permission to send.')
        for question in guard.get('clarification_questions',[]):st.write('Clarification:',question)
        with st.expander('Control reasons and complete evidence'):
            st.write('Recorded reason codes:',guard['reason_codes'])
            st.write('Recorded violations:',guard['violations'])
            st.json(guard)

def policy_card(cs,ticket,evidence,candidates):
    confirmed=False;selected=None
    with st.container(border=True):
        st.markdown('### 2 · Policy guidance')
        st.write('**Recommended policy candidates**')
        if not candidates:st.caption('No semantic candidates are available for this case/mode. No recommendation is invented.')
        for row in candidates:
            card=cs[row['policy_id']]
            with st.container(border=True):
                st.markdown(f"**{row['rank']}. {card['title']}**")
                st.caption(f"{row['policy_id']} · similarity {row['cosine_similarity']:.3f}")
                st.write(card['short_description'])
        st.caption('Similarity is not confidence or policy authority. All 15 cards compete; the classifier never filters them. Descriptions are policy text, not a newly generated applicability judgment.')
        if evidence and evidence['policy_id']:
            gold=cs[evidence['policy_id']]
            st.info(f"Verified policy used for this saved example: {gold['title']} · {gold['policy_id']} · v{gold['version']}")
            st.caption('Historical gold-policy evidence. Select, inspect and confirm it below to unlock its saved draft.')
        identity=hashlib.sha256(ticket.encode()).hexdigest()[:12]
        selected=st.selectbox('Choose a policy after reviewing its applicability',[None]+list(cs),format_func=lambda x:'No policy selected' if x is None else cs[x]['title']+' · '+x,key='policy_'+identity)
        if selected:
            card=cs[selected]
            st.markdown(f"**Selected: {card['title']}**")
            st.caption(f"{selected} · card v{card['version']} · Playbook v1.1 · fictional academic approval")
            with st.expander('Read selected policy and conditions',expanded=True):
                st.write(card['policy_text']);st.write('Eligibility:',card['eligibility_conditions']);st.write('Escalation conditions:',card['escalation_conditions'])
            with st.expander('Complete policy record'):st.json(card)
            problems=policy_checks(card,cs,date.today().isoformat())
            if problems:
                st.error('Policy cannot support current drafting: '+', '.join(problems))
                st.caption('Frozen review dates remain enforced. Historical evidence does not renew a stale policy.')
            else:
                confirmed=st.checkbox('I reviewed this policy and selected it for this ticket.',key='confirm_'+identity+'_'+selected)
                if confirmed:st.success('Policy selection confirmed by you. Final human review is still required.')
    return selected,confirmed

def results(ticket,case,evidence):
    guard=evidence['guardrail'] if evidence else assess(ticket)
    if not case and (guard['signals']['unsupported_scope'] or not guard['signals']['recognized_support_topic']):
        st.warning('This request does not appear to match the supported DemoRetail support topics.')
        st.write('Try an account-access, cancellation, delivery, payment, refund or human-support question. Unrelated policy recommendations are hidden.')
        st.caption('Finite UI heuristic, not a validated out-of-domain detector or confidence threshold.')
        with st.expander('Technical diagnostics — not policy guidance'):
            try:st.dataframe(demo.classify(ticket),hide_index=True)
            except demo.DemoError as exc:st.warning(str(exc))
        guard_card(guard,False);final_control();return
    with st.container(border=True):
        st.markdown('### 1 · Issue overview')
        try:
            scores=demo.saved_classifier(case) if case else demo.classify(ticket)
            st.markdown('**Broad topic hint:** '+scores[0]['category'].replace('_',' ').title())
            st.caption('Saved prediction' if case else 'New server-local prediction')
            with st.expander('Model probabilities — uncalibrated'):
                st.caption('Model preferences among six labels, not certainty, eligibility or scope detection.')
                st.dataframe(scores,hide_index=True)
        except demo.DemoError as exc:st.warning(str(exc))
    cs=demo.cards();candidates=[]
    if case:candidates=demo.saved_rankings(case)
    else:
        available,message=demo.semantic_availability()
        if available:
            try:
                with st.spinner('Reading the pinned local model…'):candidates=demo.local_candidates(ticket)
            except demo.DemoError as exc:st.warning(str(exc))
        else:st.info('Semantic retrieval is unavailable in this cloud demo. Saved evaluation examples remain fully available.')
    selected,confirmed=policy_card(cs,ticket,evidence,candidates)
    matching=evidence and evidence['extraction'] is not None
    with st.container(border=True):
        st.markdown('### 3 · Structured facts')
        if matching:
            extraction=evidence['extraction']
            st.caption('Unedited recorded field values; customer claims are not verified backend facts.')
            st.write('**Customer goal**');st.write(extraction['customer_goal'])
            st.write('**Known facts — customer-reported**')
            for fact in extraction['facts']:st.write('• '+fact['fact'])
            st.write('**Missing information — as extracted**')
            if extraction['missing_information']:
                for item in extraction['missing_information']:st.write('• '+item)
            else:st.caption('None recorded; this is not proof that all required information is present.')
            st.write('Security concern:',extraction['security_concern'])
            st.write('Human requested:',extraction['human_requested'])
            st.write('Business escalation signal — saved generation:',evidence['generation']['business_escalation_required'])
            if extraction['conflicts']:st.write('Reported conflicts:',extraction['conflicts'])
            if extraction['uncertainty_notes']:st.write('Recorded uncertainty:',extraction['uncertainty_notes'])
            with st.expander('Complete saved extraction'):st.json(extraction)
        else:st.info('No recorded extraction exists for this case. New-ticket preview does not create one.')
    with st.container(border=True):
        st.markdown('### 4 · Saved grounded draft')
        if matching and selected==evidence['policy_id'] and confirmed:
            st.caption('Previously evaluated GPT output — not generated live')
            st.text(evidence['generation']['draft_response'])
            human=evidence['human']
            st.write(f"**Final human review:** extraction {human['human_extraction_rating']} · generation {human['human_generation_rating']} · escalation {human['human_escalation_correct']}")
            st.write('Reviewer note:',human['notes'])
            with st.expander('Complete saved generation'):st.json(evidence['generation'])
        elif matching:st.info('Select and confirm the original policy '+evidence['policy_id']+' above to view the saved draft. A different policy cannot unlock it.')
        else:st.info('No saved GPT draft exists here. New inputs do not trigger fresh GPT generation.')
    guard_card(guard,bool(evidence));final_control()

def demo_page():
    st.title('TicketTriage')
    st.markdown('### Verified policy guidance for support teams')
    st.write('An academic AI decision-support prototype that helps a Tier-1 support employee identify relevant policy guidance, inspect evidence and review a grounded response before taking action.')
    st.markdown('<span class="badge">Human-reviewed AI prototype</span>',unsafe_allow_html=True)
    a,b,c,_=st.columns([1,1,1,3])
    a.link_button('GitHub',SOURCE,use_container_width=True)
    b.button('How it works',on_click=go,args=('How it works',),use_container_width=True)
    c.button('Evaluation',on_click=go,args=('Evaluation',),use_container_width=True)
    st.markdown('<div class="disclosure"><strong>Portfolio / academic demo.</strong> Saved GPT outputs are replayed for reproducibility.<br>New inputs do not trigger live LLM calls or business actions.</div>',unsafe_allow_html=True)
    left,right=st.columns([1,1.45],gap='large')
    with left:
        st.subheader('Support ticket')
        mode=st.radio('Choose a mode',['Saved evaluated example','New ticket preview'],key='mode')
        case=None;evidence=None
        if mode=='Saved evaluated example':
            case=st.selectbox('Choose an example',list(EXAMPLES),format_func=lambda key:EXAMPLES[key][0],key='example')
            st.caption(f"{case} · {EXAMPLES[case][1]}")
            original=demo.saved_query(case)
            ticket=st.text_area('Customer ticket',original,height=140,max_chars=3000,key='ticket_'+case)
        else:
            ticket=st.text_area('Paste a fictional support ticket',height=140,max_chars=3000,key='local_ticket',placeholder='My card shows two completed charges for the same order.')
            st.caption('New-ticket mode runs classification and available local checks only. It does not generate a fresh GPT response.')
            if not demo.semantic_availability()[0]:st.caption('Cloud profile: new-ticket semantic retrieval is unavailable; saved rankings remain available.')
            st.caption('Text reaches this demo server. No external inference API call is made. Use no credentials or confidential customer details.')
        clicked=st.button('Analyse ticket',type='primary',use_container_width=True,key='analyze')
        signature=(mode,case,ticket)
        if clicked:st.session_state['analysis_signature']=signature
        with st.expander('Privacy and evidence boundaries'):
            st.write('Only fictional/generalized inputs. This app deliberately writes no ticket files and makes no live LLM calls. Hosting infrastructure may retain operational/access logs; this is not a zero-retention guarantee.')
            st.write('Saved cases show fixed experimental evidence. Editing their text invalidates replay. New-ticket processing runs on the server, not your own device.')
    st.sidebar.caption('Demo mode: '+('Saved replay' if mode=='Saved evaluated example' else 'New ticket preview'))
    with right:
        st.subheader('TicketTriage analysis')
        if case and ticket!=original:
            st.warning('Ticket edited: saved evidence is not valid for this text. Restore it or use New ticket preview.');return
        if not ticket.strip() or st.session_state.get('analysis_signature')!=signature:
            with st.container(border=True):
                st.markdown('### Submit a ticket to see the analysis.')
                st.write('Choose an example on the left, then click **Analyse ticket**.')
                st.caption('You will see the topic hint, policy evidence, saved facts/draft and review controls.')
            return
        if case:evidence=demo.saved_evidence(case)
        results(ticket,case,evidence)

def how_page():
    st.title('How it works');st.write('One fixed workflow. Several distinct jobs. A human remains responsible.')
    st.markdown('<div class="flow">Customer ticket → Privacy / scope checks → Broad classifier hint → Policy retrieval → Verified policy selection → Structured extraction → Grounded draft → Deterministic guardrails → Mandatory human review → Final human action outside the app</div>',unsafe_allow_html=True)
    stages=[('Customer ticket','Records the reported issue and goal.','Establishes the question.','Does not verify backend facts.'),('Privacy / scope checks','Uses limited topic/secret signals.','Flags known boundaries before guidance.','Not complete redaction or out-of-domain detection.'),('Classifier','Asks: what general topic does this look like?','Fast broad hint.','Does not choose policy or filter retrieval.'),('Retriever','Asks: which policy cards look relevant? Searches all 15.','Discovers candidate evidence.','Similarity is not policy authority.'),('Verified policy selection','A person inspects and confirms applicable evidence.','Makes the control point explicit.','No automatic eligibility decision.'),('Structured extraction','Organizes customer-reported facts into fields.','Makes evidence inspectable.','No invented backend facts; public demo replays saved extraction.'),('Grounded draft','Uses supplied policy for response guidance.','Helps explain the procedure.','No action execution; public demo replays saved drafts.'),('Deterministic guardrails','Checks whether to stop, clarify, escalate or review.','Adds repeatable finite controls.','Does not prove general safety.'),('Mandatory human review','Checks policy, draft and control decisions.','Preserves human authority.','Not waived by high similarity or valid JSON.'),('Final human action','Occurs outside the app in authorized procedures.','Keeps accountable action with the employee.','This app cannot send or change anything.')]
    for name,what,why,limit in stages:
        with st.container(border=True):
            st.markdown('#### '+name);st.write(what);st.caption('Why: '+why+' Boundary: '+limit)
    st.subheader('Why not just use one LLM?')
    st.write('Different components solve different tasks. Separate evaluation exposes failure sources; local hints avoid paying for every simple label; verified policy provides grounding; deterministic checks are inspectable; a human retains accountability. No GPT-for-everything comparison or measured total-cost advantage was established.')
    st.caption('Steps are known in advance. No model-selected arbitrary tool sequence, write action or autonomous external-feedback loop exists. This is a workflow, not an agent.')

def evaluation_page():
    st.title('Evaluation');st.info('Different layers were evaluated separately. There is no single overall accuracy.')
    cols=st.columns(4)
    for col,label,value in zip(cols,['Broad classifier','TF-IDF retrieval Recall@1','Semantic retrieval Recall@1','Semantic retrieval Recall@3'],['99.65%','58.33%','63.33%','96.67%']):col.metric(label,value)
    st.caption('Classifier: cleaned Bitext six-category holdout only (2,275 requests). Retrieval: 60 frozen queries across 15 cards.')
    st.write('Semantic top-1 improvement was nominal: 38/60 vs 35/60. The +10pp target was not met. High Recall@3 motivated showing candidates rather than silently trusting top-1.')
    st.caption('The target was chosen after the TF-IDF aggregate, before semantic scoring. Personal Recall@1 was 11/15 for both methods; no conclusive-superiority claim.')
    st.subheader('Foundation-model human review')
    st.table([{key:str(value) for key,value in row.items()} for row in [{'Component':'Extraction','PASS':4,'PARTIAL':11,'FAIL':0,'AMBIGUOUS':'—'},{'Component':'Generation','PASS':2,'PARTIAL':6,'FAIL':7,'AMBIGUOUS':'—'},{'Component':'Escalation','PASS':9,'PARTIAL':'—','FAIL':5,'AMBIGUOUS':1}]])
    st.caption('15 cases; correct GOLD policy deliberately supplied. One project-author reviewer saw provisional assistant judgments: anchoring and reviewer independence are limitations. Not production prevalence. Schema-valid output is not factual correctness.')
    st.subheader('Deterministic controls')
    a,b=st.columns(2);a.metric('Frozen behavior cases','10/10');b.metric('Development fixtures','17/18')
    st.write('Known failures informed rule design. Replay caught five known missed escalations. The unsupported-airline fixture failure remains; these are coverage/regression results, not general safety.')
    st.warning('These results measure different components and cannot be multiplied or combined into an overall success rate.')
    st.subheader('What we learned')
    st.markdown('- Broad classification was easier than exact policy selection in these separate tests.\n- Correct policy still did not guarantee good LLM guidance.\n- Deterministic controls caught known escalation failures.\n- Human review remained necessary.')
    st.caption('The corpus and 45 controlled queries share assistant authorship. The 15 personal queries are policy-aware, experience-inspired and supplied with disclosed assistant-assisted adaptation; not an independent blinded customer sample.')
    st.link_button('Read evaluation evidence',SOURCE+'/blob/main/docs/evaluation.md')

def governance_page():
    st.title('Governance & limitations');a,b=st.columns(2,gap='large')
    with a:
        st.subheader('Governance')
        for title,text in [('Data','Public/synthetic Bitext, fictional DemoRetail policies and generalized experience-inspired queries.'),('Knowledge','Policy IDs, versions, review dates and fictional owner / academic approval metadata. No real-company approval is implied.'),('Model','Fixed prompts, frozen benchmarks, preserved failures and recorded results. Hashes establish artifact identity, not independent chronological preregistration.'),('Action','No auto-send, refund, cancellation, account change or case submission.'),('Human','Mandatory final review; selected policy and human reviewer are the control points.')]:
            with st.container(border=True):st.markdown('#### '+title);st.write(text)
    with b:
        st.subheader('Limitations')
        st.markdown('- No real user study or measured handling-time savings\n- No classifier ablation or measured policy-selection friction\n- Only 15 short fictional policies\n- Small, gold-conditioned FM review set\n- One reviewer; anchoring risk and rubric/adjudication differences\n- Finite guardrails, including a preserved out-of-domain failure\n- No persistent production telemetry\n- No live GPT in public deployment\n- New-ticket semantic retrieval unavailable in the cloud profile\n- Not production-ready')
        st.info('User-entered text reaches the hosted server for local checks/classification. The app sends no text to an external inference API and deliberately writes no ticket files. Hosting logs are outside this assurance. Use no secrets or confidential data.')
        st.caption('Stale policies block draft confirmation. A portfolio deployment never renews frozen policies.')
    st.link_button('Governance documentation',SOURCE+'/blob/main/docs/governance_and_privacy.md')

def about_page():
    st.title('About project');st.markdown('### TicketTriage · PE6201 Emerging AI Technologies')
    st.write('**Persona:** Raj — Tier-1 e-commerce support employee. Raj is a design persona; no real-user study was conducted.')
    st.write('**Problem:** Support employees may understand the broad issue but still need to locate the exact applicable policy.')
    st.write('**Project question:** Can classification, retrieval, foundation-model assistance and deterministic controls help surface verified guidance while keeping humans responsible for the final decision?')
    st.table([{'Class':'1','Project connection':'Choose the right AI approach'},{'Class':'2','Project connection':'RAG / system architecture'},{'Class':'3','Project connection':'Prompting, structured output and evals'},{'Class':'4','Project connection':'Fixed workflow, not an autonomous agent'},{'Class':'5','Project connection':'Cost-to-serve and business value'},{'Class':'6','Project connection':'Failures, guardrails and governance'}])
    st.subheader('Economics, with assumptions visible')
    st.write('Measured FM variable cost: US$0.00064629 per component ticket. Sequential latency: median 4.613 s; p95 6.093 s. Illustrative low/moderate/high cost-to-serve: $0.40264629 / $2.11064629 / $6.63064629 per ticket.')
    st.caption('Human review, runtime and escalation inputs are assumptions. No measured savings, ROI or break-even; no production handling-time claim.')
    a,b,c=st.columns(3);a.link_button('GitHub',SOURCE);b.link_button('README',SOURCE+'#readme');c.link_button('Evaluation documentation',SOURCE+'/blob/main/docs/evaluation.md')

st.sidebar.title('TicketTriage')
page=st.sidebar.radio('Navigation',PAGES,key='page',label_visibility='collapsed')
st.sidebar.caption('PE6201 academic project')
try:
    {'Demo':demo_page,'How it works':how_page,'Evaluation':evaluation_page,'Governance & limitations':governance_page,'About project':about_page}[page]()
except demo.DemoError as exc:
    st.error(str(exc));st.info('The required evidence could not be verified. Restore the original artifact; no paid fallback or model substitution occurs.')
except Exception:
    st.error('A component could not be displayed. Please reload or check the deployment guide. No API call or business action was attempted.')
