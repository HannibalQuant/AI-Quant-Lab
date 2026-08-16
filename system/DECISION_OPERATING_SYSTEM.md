# AI Quant Lab Decision Operating System

## Document control

| Field | Value |
|---|---|
| Document class | Master decision architecture specification |
| Status | Proposed for Sprint 5 review |
| Authority | Governs consequential decisions made or communicated by every AI Quant Lab agent |
| Scope | Reasoning, evidence, alternatives, uncertainty, recommendation, review, approval, and learning |
| Out of scope | Software implementation, interface design, workflow tooling, and execution code |
| Change control | Decision Architecture review and explicit governance approval |

The Decision Operating System, or Decision OS, defines how AI Quant Lab transforms observations and knowledge into justified action. It requires every consequential decision to be explainable, reproducible, contestable, and reviewable. It preserves uncertainty and rejected alternatives so later agents can understand not only what was chosen, but what was known, what remained unknown, and why other paths were not taken.

## 1. Decision philosophy

### 1.1 Definition of a decision

A decision is an accountable commitment to an option, state transition, allocation, restriction, or deliberate inaction under a defined context, objective, evidence set, uncertainty, and authority.

A decision has consequences. It changes what the system may do, what work receives resources, which claim is provisionally accepted, which candidate advances, which risk is tolerated, or which action is withheld. A statement that changes nothing is an observation, inference, or recommendation—not a decision.

A valid decision specifies:

- the decision question;
- the accountable owner;
- the authority under which the decision is made;
- the objective and constraints;
- the evidence available at the decision time;
- the feasible alternatives considered;
- the chosen option and reasons;
- the rejected options and reasons;
- known uncertainty and residual risk;
- review, expiry, and reconsideration conditions.

### 1.2 Observation

An observation is a bounded description of something measured, recorded, or directly encountered. It does not contain an explanation or prescribe action.

Examples include a change in market behavior, a failed validation fold, disagreement between two artifacts, a missed execution, or an increase in data gaps. Observations record source, time, context, and measurement limits.

### 1.3 Inference

An inference is an interpretation derived from one or more observations and background knowledge. It connects evidence to a possible meaning but remains conditional on assumptions.

An inference must state its reasoning and plausible alternatives. “Performance weakened because the regime changed” is an inference unless the causal relationship has been independently established.

### 1.4 Hypothesis

A hypothesis is a falsifiable proposition about a relationship, mechanism, or expected outcome. It defines what evidence would support, narrow, or reject it.

Hypotheses guide evidence collection. They do not authorize action simply because they are coherent. A preferred hypothesis must compete with credible alternatives.

### 1.5 Evidence

Evidence is an observation, result, source, comparison, or validated knowledge object used to increase or decrease confidence in a hypothesis, inference, option, or decision.

Evidence is always evaluated relative to the decision question. Its value depends on quality, relevance, independence, recency, consistency, and scope. Evidence against an option remains part of the decision record.

### 1.6 Decision

A decision selects an option or intentional inaction from a feasible alternative set. It applies evidence and policy to a specific context. It is owned, time-bounded when appropriate, and subject to review.

Decision does not mean certainty. It means the system has sufficient reason and authority to commit despite residual uncertainty.

### 1.7 Recommendation

A recommendation is a reasoned proposal from an agent that may not hold the authority to decide. It states the preferred option, alternatives, evidence, uncertainty, risks, and conditions.

Recommendations inform decisions but do not change system state. A recommendation must not be presented as approval.

### 1.8 Approval

Approval is an authorized confirmation that a decision or artifact satisfies a defined gate. It is narrower than general endorsement. Statistical approval, risk approval, quality approval, and deployment approval are separate.

Approval states the scope, authority, effective period, conditions, and evidence version. One approval does not imply another, and silence is never approval.

### 1.9 Decisions are probabilistic

Consequential choices are made under incomplete knowledge, changing environments, noisy evidence, and uncertain outcomes. The Decision OS therefore evaluates expected benefits, adverse distributions, reversibility, information value, and consequences of error rather than assuming a single predicted future.

Probability may be estimated quantitatively or expressed through disciplined qualitative ranges when measurement is not credible. False numerical precision is not preferred over an explicit bounded judgment.

### 1.10 Uncertainty is never removed

More evidence may reduce uncertainty, partition it, or reveal its structure. It does not eliminate uncertainty. Every decision retains:

- uncertainty about the state of the world;
- uncertainty about measurement;
- uncertainty about interpretation;
- uncertainty about future response;
- uncertainty about the decision model itself.

The system does not convert unresolved unknowns into assumptions merely to complete a decision. Material uncertainty affects confidence, option choice, exposure, reversibility, review frequency, and escalation.

### 1.11 Decisions are temporal

A decision is correct only relative to the evidence, objective, policy, and constraints available at a stated time. Later outcomes do not by themselves prove that the decision process was good or bad. A sound decision can have an adverse outcome; a weak decision can benefit from chance.

Evaluation therefore separates decision quality from outcome quality.

### 1.12 Inaction is an option

The Decision OS always permits intentional inaction, delay, evidence gathering, reduction of scope, or escalation when no option satisfies the minimum decision threshold. The system is not required to manufacture action from inadequate evidence.

## 2. Decision pipeline

### 2.1 Pipeline overview

```text
Observation
↓
Context
↓
Knowledge Retrieval
↓
Hypothesis Generation
↓
Evidence Collection
↓
Alternative Generation
↓
Risk Assessment
↓
Decision
↓
Confidence
↓
Recommendation or Approval Request
↓
Review
↓
Continuous Learning
```

The pipeline is not a license to proceed mechanically. Any stage may reveal that the question is malformed, authority is missing, evidence is inadequate, or risk exceeds mandate. In that case, the decision pauses, narrows, returns to an earlier stage, or escalates.

### 2.2 Observation

The decision begins with a recorded trigger. The trigger is expressed without explanation and includes origin, time, affected scope, measurement limits, and urgency.

The owner asks whether the observation is real, duplicated, stale, or the result of a changed definition. An invalid trigger ends the decision process with a recorded disposition.

### 2.3 Context

Context defines the decision question, objective, constraints, authority, stakeholders, time horizon, reversibility, consequence of error, and deadline. It identifies what is inside and outside scope.

A decision without an explicit objective cannot compare alternatives. A decision without authority cannot proceed beyond recommendation.

### 2.4 Knowledge retrieval

The owner retrieves current eligible knowledge, definitions, prior decisions, failures, lessons, policies, and contradictions relevant to the question. Retrieval includes exact versions and records material gaps.

Past decisions are precedent, not automatic answers. Changed context or new evidence may justify a different choice.

### 2.5 Hypothesis generation

The owner develops competing explanations for the observation and expected consequences of action. At least one hypothesis must challenge the preferred interpretation when the decision is consequential.

Hypotheses state assumptions, predictions, failure conditions, and discriminating evidence. If no meaningful hypothesis can be formed, the decision remains exploratory.

### 2.6 Evidence collection

Evidence collection is driven by the decision question and competing hypotheses. The owner identifies which evidence is required, which is desirable, which is unavailable, and whether delay to collect more evidence is justified.

Search stops according to declared sufficiency, deadline, or diminishing information value. It does not continue until only supportive evidence remains.

### 2.7 Alternative generation

The owner creates structurally different options, including inaction or evidence gathering. Alternatives must be feasible under authority and constraints. Variations that differ only cosmetically are not independent options.

The option set is frozen before final comparative assessment unless new evidence materially changes the decision frame. Late additions are recorded with cause.

### 2.8 Risk assessment

Each alternative is evaluated for downside, reversibility, uncertainty, dependency, opportunity cost, failure detection, and recovery. Risk includes research error, model error, financial loss, operational disruption, knowledge corruption, security, and governance failure as relevant.

Risks that exceed the owner's authority are escalated. Risk cannot be averaged away by unrelated benefits.

### 2.9 Decision

The accountable owner selects an option or intentional inaction using the declared objective, constraints, evidence, risk, and policy. The owner explains the decisive considerations and which evidence did not materially influence the choice.

If no alternative passes minimum acceptability, the correct decision is to reject, defer, reduce scope, gather evidence, or escalate.

### 2.10 Confidence

Confidence is assessed after option selection so it describes the decision actually made. It reflects evidence strength, uncertainty, option separation, assumption sensitivity, and risk-control effectiveness.

Confidence does not modify the historical evidence. Low confidence may still accompany an urgent reversible action; high confidence does not authorize action outside mandate.

### 2.11 Recommendation or approval request

If the owner lacks final authority, the decision is communicated as a recommendation or approval request. It includes the complete alternative and uncertainty record. The receiving authority must not be shown only the favored option.

### 2.12 Review

An independent reviewer challenges context, evidence, alternatives, assumptions, conflicts, confidence, and authority. The reviewer may approve, approve with explicit conditions, return for revision, reject, or escalate.

Conditional approval is allowed only when conditions are observable, owned, time-bounded, and enforced. A condition that cannot be verified is an unresolved assumption.

### 2.13 Continuous learning

After outcomes or new evidence become available, the system compares expectations with observations, evaluates the quality of the decision process, and updates eligible knowledge through review. Learning never rewrites the original decision record.

## 3. Decision types

### 3.1 Strategic decisions

**Purpose:** define long-horizon project direction, priorities, capital boundaries, authority, and irreversible commitments.

**Owner:** Founder for purpose and capital authority; CEO Agent for delegated portfolio and research strategy.

**Inputs:** mission, policy, resource constraints, risk appetite, capability evidence, external obligations, scenario analysis, and prior strategic outcomes.

**Outputs:** strategic decision record, priority changes, authority boundaries, resource allocation, and review horizon.

**Failure conditions:** unstated objective; decision outside delegated authority; inadequate scenario range; irreversible commitment without alternatives or exit path; operational preference presented as strategy; missing Founder approval where required.

### 3.2 Research decisions

**Purpose:** select hypotheses, research questions, experimental scope, evidence thresholds, and whether a candidate should advance, revise, or stop.

**Owner:** Quant Strategy Architect or Research Agent within mandate; CEO Agent for research portfolio priority.

**Inputs:** observations, Knowledge OS retrieval, competing hypotheses, prior experiments, failure database, data feasibility, and research budget.

**Outputs:** research recommendation, hypothesis record, experiment request, scope restriction, stop decision, or validation-candidate recommendation.

**Failure conditions:** indicator-first rationale; hypothesis formed only after outcome selection; missing alternatives; undisclosed repeated search; use of final evaluation evidence to redesign the candidate; continuation after the core behavioral claim fails.

### 3.3 Engineering decisions

**Purpose:** choose a precise interpretation or technical approach that preserves an approved specification and satisfies quality constraints.

**Owner:** Python Agent or Pine Agent within its domain, subject to architectural and QA review.

**Inputs:** frozen specification, authoritative definitions, platform constraints, known failure modes, compatibility requirements, and test evidence.

**Outputs:** engineering decision record, selected approach, rejected approaches, trade-offs, assumptions, compatibility impact, and required validation.

**Failure conditions:** changing strategy intent without specification revision; selecting convenience over semantic correctness without disclosure; missing compatibility analysis; hidden platform divergence; self-approval of material behavior.

### 3.4 Validation decisions

**Purpose:** determine whether an artifact or candidate satisfies predefined evidence and robustness requirements.

**Owner:** Validation Agent, independently of the producer.

**Inputs:** frozen candidate, validation policy, acceptance gates, complete evidence, negative controls, contradiction record, and holdout-access history.

**Outputs:** pass, conditional pass, fail, or incomplete disposition; failure register; scope limits; and revalidation conditions.

**Failure conditions:** thresholds changed after seeing results; missing adverse evidence; contaminated holdout; producer influence over disposition; aggregate result hiding failed components; approval outside validation scope.

### 3.5 Risk decisions

**Purpose:** determine acceptable exposure, limits, controls, exceptions, and response to risk changes.

**Owner:** Risk Agent within Founder-approved policy; Founder or delegated authority for mandate changes.

**Inputs:** validated evidence, downside distributions, liquidity, dependencies, portfolio state, stress scenarios, operational controls, and risk policy.

**Outputs:** risk disposition, limits, restrictions, kill conditions, exception record, and review triggers.

**Failure conditions:** risk accepted outside mandate; missing tail or dependency analysis; reliance on the strategy as sole control; unenforceable condition; exception without owner and expiry; return objective overriding hard risk boundary.

### 3.6 Deployment decisions

**Purpose:** authorize, restrict, suspend, roll back, or retire a specific approved artifact in a defined environment.

**Owner:** CEO Agent for lifecycle authorization, with mandatory Risk and QA approvals; Execution Agent may make bounded operational responses.

**Inputs:** immutable deployment candidate, validation disposition, risk approval, QA approval, portfolio eligibility, monitoring plan, rollback plan, and operational readiness.

**Outputs:** deployment approval or rejection, effective scope, conditions, authority, monitoring requirements, and rollback target.

**Failure conditions:** version ambiguity; missing approval; unresolved blocking defect; no rollback or monitoring; production scope broader than validated scope; unapproved change between review and deployment.

### 3.7 Knowledge decisions

**Purpose:** determine whether a claim is validated, restricted, contradicted, superseded, deprecated, retired, or eligible for specific consumers.

**Owner:** Knowledge Curator with domain-owner and independent review; governance owner for normative policy knowledge.

**Inputs:** provenance, evidence evaluation, contradictions, dependencies, source status, consumer impact, freshness, and prior versions.

**Outputs:** knowledge lifecycle decision, confidence update, relationship changes, revalidation schedule, consumer notification, and archival disposition.

**Failure conditions:** missing provenance; popularity treated as evidence; contradiction hidden; source and project inference merged; historical object overwritten; production eligibility granted without required review.

### 3.8 Emergency decisions

**Purpose:** limit imminent harm when normal review time is unavailable.

**Owner:** explicitly designated emergency authority; agents may take only pre-authorized protective actions.

**Inputs:** incident observation, current exposure, affected systems, available controls, uncertainty, and emergency policy.

**Outputs:** containment action, temporary restriction, escalation, incident decision record, expiry, and mandatory retrospective.

**Failure conditions:** emergency used to bypass normal review for convenience; action increases exposure; missing time limit; authority unclear; evidence destroyed; no retrospective; temporary exception becomes permanent silently.

## 4. Evidence evaluation

### 4.1 Evaluation purpose

Evidence evaluation determines how much a specific item should change confidence in a hypothesis or alternative. It does not create a universal score for source prestige.

### 4.2 Dimensions

**Evidence quality:** methodological strength, measurement integrity, controls, uncertainty, reproducibility, and directness of the result.

**Source reliability:** provenance, competence, incentives, track record, authority for the claim type, and correction behavior.

**Recency:** time since validation relative to how quickly the subject changes. Recency is critical for liquidity and platform behavior, less decisive for stable mathematical definitions.

**Relevance:** match between evidence and the decision's market, horizon, state, population, objective, and operational context.

**Consistency:** agreement with other relevant evidence after accounting for definitions and scope. Consistency does not mean majority vote.

**Independence:** degree to which evidence originates from distinct data, methods, authors, incentives, and causal paths. Repeated citations of one source count once.

**Contradictions:** material evidence against the claim, including type, strength, scope, and whether resolved or contextualized.

**Unknowns:** missing evidence, untested assumptions, unavailable populations, uncertain transformations, and possible blind spots.

### 4.3 Evidence assessment record

Each decision-grade evidence item records:

- claim or option affected;
- direction: supports, contradicts, or limits;
- quality assessment and rationale;
- source reliability and provenance;
- relevance and applicable scope;
- freshness and review status;
- independence from other evidence;
- known limitations and unknowns;
- sensitivity of the decision to removing the item.

### 4.4 Weighting rules

No fixed arithmetic formula applies across all decision types. The owner assigns decision-specific importance before final comparison and explains departures from default evidence hierarchy.

Evidence cannot compensate across non-substitutable requirements. Strong expected performance does not compensate for missing authority, a breached hard risk limit, contaminated validation, or uncertain order state.

### 4.5 Evidence sufficiency

Evidence is sufficient when it is strong enough for the consequence, alternatives are meaningfully separable, material contradictions are addressed, and remaining uncertainty is controlled through option design, limits, reversibility, or monitoring.

Sufficiency is not completeness. The Decision OS requires a threshold for justified action, not impossible omniscience.

### 4.6 Contradictory evidence

When evidence conflicts, the owner first tests whether the conflict arises from different definitions, samples, horizons, versions, methods, or contexts. If conflict remains, the decision records both sides, lowers confidence, identifies discriminating evidence, and selects a more reversible or restricted option when consequence warrants.

Unresolved contradiction must not be summarized as neutral agreement.

### 4.7 Unknowns and evidence gaps

The owner distinguishes evidence not found, evidence unavailable, evidence impossible to obtain, and evidence intentionally not collected because its value did not justify cost or delay. Each gap has a consequence for confidence and review.

## 5. Alternative generation

### 5.1 Requirement

Every consequential decision generates multiple feasible alternatives before choosing. The purpose is to avoid anchoring on the first coherent solution and to expose trade-offs that a single proposal hides.

### 5.2 Required option set

**Best option:** the alternative with the strongest expected fit to the declared objective after constraints and risk. It is not necessarily the highest-return or fastest option.

**Second-best option:** the nearest credible alternative. It reveals which assumptions separate the preferred choice from a reasonable substitute.

**High-risk option:** an option with greater upside, speed, information gain, or scope but materially larger downside or uncertainty. It is included for explicit comparison, not presumed eligible.

**Low-risk option:** a more reversible, limited, delayed, or conservative choice. It includes controlled inaction where appropriate.

**Experimental option:** a bounded action designed primarily to obtain discriminating evidence before broader commitment.

An option may occupy more than one category only if the overlap is explained. The decision record still requires at least three structurally distinct feasible paths for material decisions, unless policy or emergency conditions make fewer possible.

### 5.3 Alternative construction

Alternatives vary meaningful dimensions such as scope, timing, reversibility, evidence demand, exposure, method, dependency, or objective trade-off. Changing only presentation or minor detail does not create an alternative.

The owner also considers:

- do nothing;
- defer until a stated evidence condition;
- reduce scope;
- stage the commitment;
- gather information;
- transfer or escalate authority;
- reject the decision frame and redefine the question.

### 5.4 Fair comparison

Alternatives are evaluated under the same objective, evidence date, constraints, and risk definitions. The preferred option must not receive optimistic assumptions while alternatives receive conservative ones.

### 5.5 Rejected alternatives remain visible

Every rejected option records why it was credible, why it lost, which assumptions harmed it, and what future evidence could make it preferable. Rejected options remain linked to the decision and may be reconsidered without reconstructing history.

### 5.6 Dominance and elimination

An option may be eliminated early when it violates hard policy, lacks authority, is infeasible, or is dominated across all relevant objectives. Elimination still receives a recorded reason. Policy-ineligible options are not used to make the preferred option appear stronger.

## 6. Uncertainty management

### 6.1 Known

A known is sufficiently established for the decision scope through authoritative definition, direct observation, or validated evidence. Known does not mean permanent or universal.

**Effect on confidence:** supports confidence only within its exact scope and freshness. Known dependencies still require monitoring when they can change.

### 6.2 Known unknown

A known unknown is an identified uncertainty whose nature is understood but value or outcome is not. Examples include future volatility, unavailable evidence, uncertain effect magnitude, or pending platform behavior.

**Effect on confidence:** lowers confidence in proportion to sensitivity. It may be managed through experiments, limits, staging, contingency, or review triggers.

### 6.3 Unknown unknown

An unknown unknown is an unrecognized factor that may affect the decision. It cannot be listed individually at decision time, but exposure to it can be acknowledged through model humility, diversification, reversibility, monitoring, and bounded authority.

**Effect on confidence:** imposes a confidence ceiling for novel, complex, irreversible, or weakly observed decisions. The system must not claim all material uncertainty is enumerated.

### 6.4 Ambiguous

Ambiguity exists when definitions, observations, or interpretations permit multiple meanings. It may be linguistic, conceptual, temporal, or contextual.

**Effect on confidence:** prevents decision until material terms are clarified or the decision is explicitly robust to each interpretation. Ambiguity is not averaged into a midpoint.

### 6.5 Contradictory

Contradictory uncertainty exists when credible evidence supports incompatible conclusions.

**Effect on confidence:** reduces confidence according to evidence strength and relevance, triggers scope analysis or discriminating research, and favors reversible or restricted action. Material unresolved contradiction must appear in the review summary.

### 6.6 Missing

Missing uncertainty exists when required evidence, context, ownership, or definition is absent.

**Effect on confidence:** if the missing item is mandatory, the decision is `INCOMPLETE`. If non-mandatory, its expected impact and reason for omission are recorded. Missing evidence is not equivalent to negative evidence.

### 6.7 Confidence dimensions

Decision confidence evaluates:

- context confidence;
- knowledge and evidence confidence;
- hypothesis confidence;
- alternative completeness;
- risk assessment confidence;
- assumption stability;
- reversibility and control confidence;
- review independence;
- confidence that the selected option remains preferable under reasonable variation.

An aggregate rating may summarize these dimensions but cannot conceal a critical weak component.

### 6.8 Confidence and action

Confidence is not the only determinant of action. Urgency, reversibility, downside, information value, and authority also matter. Low-confidence reversible experiments may be justified. High-confidence irreversible actions may still require wider review.

## 7. Decision record

### 7.1 Purpose

The decision record is the immutable account of what was decided and why. It allows independent reconstruction without relying on agent memory or outcome hindsight.

### 7.2 Mandatory fields

| Field | Requirement |
|---|---|
| Unique ID | Persistent identity for the decision and its later reviews |
| Timestamp | Decision time, effective time, and relevant evidence cutoff |
| Context | Question, objective, scope, constraints, authority, urgency, and reversibility |
| Evidence | Exact evidence objects, evaluations, contradictions, and missing items |
| Alternatives | Feasible option set and comparable assessment |
| Chosen Option | Selected action or deliberate inaction, owner, scope, and conditions |
| Rejected Options | Reasons, decisive trade-offs, and reconsideration triggers |
| Confidence | Component assessments, aggregate conclusion, and confidence limits |
| Reviewer | Reviewer identity, independence, authority, findings, and disposition |
| Lessons Learned | Initially expected learning; later retrospective lessons linked without rewriting the record |

### 7.3 Additional fields

Consequential records also include assumptions, risks, residual risk, approvals, dependencies, affected artifacts, expiry, review date, monitoring conditions, rollback or recovery, escalation path, and superseding decision.

### 7.4 Version discipline

A decision record is immutable after approval. Corrections and changed decisions create linked versions or successor records. Later evidence and outcomes attach as reviews, not edits to the historical basis.

### 7.5 Reproducibility standard

An independent reviewer must be able to reconstruct the evidence set, policy, alternatives, assumptions, assessment, owner authority, and review state that existed at the timestamp. If essential reasoning remains only in private dialogue, the record is incomplete.

## 8. Review protocol

### 8.1 Mandatory review questions

**Why this decision?** Identify the decisive objective, evidence, and constraints. Separate decisive reasons from supportive context.

**Why not the alternatives?** Test whether rejected options were represented fairly and whether any remains preferable under plausible assumptions.

**What assumptions exist?** Identify explicit and implicit assumptions, their evidence, sensitivity, owners, and monitoring.

**What evidence is weakest?** Name the least reliable decision-relevant evidence and evaluate the decision without it.

**Can new evidence change the decision?** State reconsideration triggers, evidence thresholds, expiry, and whether reversal remains possible.

### 8.2 Review roles

The reviewer must be independent of the decision's primary production when consequence requires separation. Domain-specific approvals remain separate: validation reviews evidence robustness; risk reviews exposure; QA reviews conformance; governance reviews authority and lifecycle.

### 8.3 Reviewer challenge

The reviewer checks:

- whether the question and objective are correctly framed;
- whether evidence cutoff and versions are complete;
- whether source dependence creates false confirmation;
- whether contradictory and adverse evidence is visible;
- whether alternatives are truly distinct and feasible;
- whether confidence exceeds evidence;
- whether risk and uncertainty are transferred rather than resolved;
- whether the owner has authority;
- whether conditions and monitoring are enforceable;
- whether decision and approval are being confused.

### 8.4 Review dispositions

- **APPROVE:** requirements are satisfied within declared scope.
- **APPROVE WITH CONDITIONS:** conditions are observable, owned, enforceable, and time-bounded.
- **REVISE:** the decision remains viable but evidence, alternatives, scope, or reasoning requires correction.
- **REJECT:** the decision is not justified or violates policy.
- **INCOMPLETE:** mandatory information, review, or authority is missing.
- **ESCALATE:** the decision exceeds authority or contains unresolved cross-domain conflict.

### 8.5 Dissent

Reasoned dissent is preserved even when approval occurs. The dissent record states the disputed assumption, evidence, expected failure, and reconsideration trigger. Consensus is not manufactured by deleting minority analysis.

### 8.6 Review depth

Review depth scales with consequence, irreversibility, novelty, uncertainty, exposure, and precedent. Routine reversible decisions may use standardized review. Capital, policy, production, emergency, and irreversible decisions require broader independent review.

## 9. Continuous improvement

### 9.1 Decision feedback

The system compares expected outcomes, risk ranges, uncertainty, and monitoring triggers with what occurred. Feedback identifies calibration quality, not just success or failure.

### 9.2 Experiments

Where alternatives cannot be separated with current evidence, bounded experiments generate discriminating information. Experiment outcomes update knowledge and future decision priors through review. They do not retroactively justify the original decision.

### 9.3 Failures

Failures are classified across framing, observation, knowledge retrieval, evidence evaluation, alternative generation, uncertainty, risk, authority, execution, review, and monitoring. Root cause distinguishes bad outcome from bad process.

### 9.4 Knowledge updates

Validated lessons, contradictions, changed assumptions, and new evidence enter the Knowledge OS with provenance and scope. Decisions depending on changed knowledge are identified for impact review.

### 9.5 Retrospectives

A retrospective asks:

- Was the original question correct?
- Were decisive assumptions visible?
- Were probabilities and confidence calibrated?
- Were alternatives represented fairly?
- Did controls and monitoring behave as expected?
- What evidence was over- or underweighted?
- Did authority and review function correctly?
- Which lesson is reusable, and within what scope?

Retrospectives do not punish justified decisions for unfavorable randomness or excuse weak decisions because outcomes were favorable.

### 9.6 Decision calibration

Over time, the system compares confidence categories with observed decision-quality indicators. Persistent overconfidence, underconfidence, ignored dissent, repeated missing alternatives, or recurring failure modes trigger changes to review thresholds and agent authority.

### 9.7 Policy improvement

Repeated decision evidence may justify changes to policy, but policy changes require their own decision record and higher authority. Agents do not silently adapt governing rules based on recent outcomes.

## 10. AI agent decision contract

### 10.1 Common contract

Every agent communicating a consequential conclusion must label it as observation, inference, hypothesis, evidence assessment, recommendation, decision, or approval. The communication includes scope, object versions, alternatives, uncertainty, confidence, authority, and requested next action.

Agents must not:

- present recommendations as approvals;
- omit credible rejected alternatives;
- conceal missing or contradictory evidence;
- claim authority they do not hold;
- overwrite prior decisions;
- use private memory instead of authoritative records;
- convert urgency into certainty.

### 10.2 CEO Agent

The CEO Agent communicates strategic and lifecycle decisions. It receives domain recommendations and approvals, preserves dissent, and states which evidence was decisive. It cannot rewrite validation or risk conclusions. Its decisions identify authority, resource impact, lifecycle transition, conditions, and review trigger.

### 10.3 Quant Strategy Architect

The Quant Strategy Architect communicates research architecture recommendations. It separates market observation, behavioral inference, hypothesis, measurements, experiment evidence, and recommendation. It records competing strategy families and why they were rejected. It may recommend a validation candidate but cannot approve production.

### 10.4 Research Agent

The Research Agent communicates observations, evidence maps, hypotheses, knowledge gaps, and research recommendations. It distinguishes exploratory findings from confirmatory evidence and source claims from project inference. It does not elevate a favored hypothesis into a decision without the required owner.

### 10.5 Python Agent

The Python Agent communicates engineering decisions and experimental evidence. It identifies the governing specification, interpretations considered, chosen interpretation, compatibility, assumptions, and tests. It cannot modify research intent or claim statistical approval.

### 10.6 Pine Agent

The Pine Agent communicates platform-specific engineering decisions, constraints, and divergences. It identifies official knowledge, observed behavior, alternatives, and parity implications. It cannot conceal a mismatch by changing strategy meaning or approve its own parity.

### 10.7 Validation Agent

The Validation Agent communicates independent gate decisions. It states policy, evidence set, failures, adverse distributions, missing tests, holdout status, confidence, and scope. It cannot change thresholds after results or redesign the candidate it validates.

### 10.8 Risk Agent

The Risk Agent communicates risk decisions, limits, restrictions, exceptions, residual uncertainty, and kill conditions. It distinguishes risk recommendation from capital-authority approval. It cannot trade return potential against a hard mandate without escalation.

### 10.9 QA Agent

The QA Agent communicates conformance and release-readiness decisions. It identifies standards, checks, skipped or unreliable evidence, defects, traceability, and disposition. It does not treat successful test execution as proof that research, validation, or risk requirements are satisfied.

### 10.10 Decision handoff

A decision handoff contains:

1. decision type and question;
2. current owner and required authority;
3. context and constraints;
4. evidence identities and cutoff;
5. alternatives and comparative reasoning;
6. chosen or recommended option;
7. uncertainty and confidence;
8. risks, conditions, and reversibility;
9. review status and dissent;
10. requested action and response deadline.

The receiving agent either accepts the handoff, returns it as incomplete, requests clarification, reviews it, or escalates. It does not silently infer missing authority or evidence.

## 11. Decision governance

### 11.1 Non-negotiable rules

1. No context, no valid decision.
2. No alternatives, no consequential choice.
3. No evidence identity, no reproducibility.
4. No uncertainty record, no credible confidence.
5. No owner, no accountability.
6. No authority, no approval.
7. No rejected-option record, no complete review.
8. No reconsideration trigger, no durable decision.
9. No retrospective, no organizational learning.
10. No historical preservation, no trustworthy governance.

### 11.2 Decision quality

Decision quality is evaluated by clarity of question, evidence discipline, alternative completeness, uncertainty calibration, authority, risk control, review independence, reproducibility, and learning—not by favorable outcome alone.

### 11.3 Health indicators

The Decision OS is unhealthy when decisions lack owners, alternatives repeat cosmetically, confidence is uncalibrated, contradictions disappear from summaries, conditional approvals never expire, emergency authority becomes routine, recommendations are treated as approvals, outcome bias dominates retrospectives, or agents repeatedly use superseded evidence.

### 11.4 Governing outcome

The Decision OS succeeds when any qualified reviewer can answer:

- What was observed?
- What was inferred?
- What evidence was available?
- Which alternatives were feasible?
- What remained uncertain?
- Who held authority?
- Why was this option selected?
- Why were the others rejected?
- What could change the decision?
- What did the system learn afterward?

If those questions cannot be answered from the record, the system has produced an action, not a governed decision.

