# Evidence Exchange Standard (EES) v1.0

## Specification control

| Field | Value |
|---|---|
| Standard ID | `AIQL-EES` |
| Standard name | Evidence Exchange Standard |
| Version | `1.0.0` |
| Status | Proposed for Sprint 19 review |
| Scope | All evidence created, transferred, consumed, challenged, validated, or relied upon within AI Quant Lab |
| Authority | Research OS, Knowledge OS, Decision OS, Agent Contract Framework, MACP, and SMI |
| Provider dependency | None |
| Change control | Evidence Governance, Validation, Knowledge Curator, QA, and affected domain-owner review |

The Evidence Exchange Standard defines the institutional semantics and governance by which evidence is created, identified, packaged, transferred, interpreted, challenged, frozen, amended, invalidated, and audited. It does not prescribe a database, API, serialization format, programming language, or software implementation.

Every AI Quant Lab agent must use EES when creating, transferring, consuming, validating, challenging, or relying on evidence. Evidence that does not satisfy this standard cannot silently acquire institutional authority.

## 1. Evidence Philosophy

### 1.1 Definition

Evidence is a traceable observation, record, result, artifact, or governed body of material capable of supporting, weakening, refuting, qualifying, or contextualizing a defined claim. Evidence has meaning only when its origin, production process, scope, version, uncertainty, limitations, and chain of custody remain attached.

### 1.2 Evidence is relational

Evidence does not exist as institutional evidence in the abstract. It is evidence about a specified claim, under stated conditions, for declared consumers and uses. The same object may support one claim, weaken another, and be irrelevant to a third.

### 1.3 Evidence is not truth

Evidence contributes to justified belief but does not eliminate uncertainty. Reliability, relevance, independence, reproducibility, and admissibility determine how much institutional weight it may carry.

### 1.4 Evidence is not decision

Evidence informs authorized decisions. It cannot approve a strategy, accept risk, allocate capital, or authorize deployment by itself. Decision authority remains with the responsible agent contract.

### 1.5 Evidence is not knowledge until curated

Evidence may enter institutional knowledge only through the Knowledge OS and Knowledge Curator governance. Transfer, acceptance, validation, or repeated use does not automatically promote evidence to knowledge.

### 1.6 Evidence must survive agent boundaries

An evidence package must retain meaning when consumed by an agent that did not create it and has no access to the originating chat, private model context, undocumented assumptions, or human memory.

### 1.7 Negative and contradictory value

Evidence that refutes a hypothesis, fails to reproduce, reveals fragility, or contradicts current belief is institutionally valuable. EES protects it from deletion, downgrading, or omission caused by outcome preference.

### 1.8 Evidence lifecycle versus claim lifecycle

Evidence may remain authentic even when a claim is rejected. Conversely, a claim may remain provisionally supported after one evidence object is invalidated if independent admissible evidence exists. Their identities and lifecycles remain separate.

### 1.9 Long-term purpose

A future authorized reviewer must be able to reconstruct what evidence existed, how it was produced, what it meant, who handled it, which decisions relied upon it, and how later challenges changed its status.

## 2. Evidence Principles

### 2.1 No Evidence Without Provenance

Every evidence object identifies origin, producer, process, source material, transformations, and custody. Unknown provenance blocks unconditional acceptance.

### 2.2 No Evidence Without Scope

Evidence states the populations, markets, instruments, timeframes, periods, regimes, versions, methods, costs, assumptions, and claims to which it applies.

### 2.3 No Silent Evidence Mutation

Material evidence content is never edited in place after submission or use. Correction and extension create new versions with explicit relationships.

### 2.4 Exact Version Referencing

Every consequential use cites the exact evidence version. Current aliases may support discovery but cannot prove what a historical decision used.

### 2.5 Evidence Is Not Decision

Evidence carries no approval authority beyond its documented evidentiary role.

### 2.6 Evidence Is Not Knowledge Until Curated

Only Knowledge Governance may convert accepted findings into governed institutional knowledge.

### 2.7 Evidence May Support, Weaken, or Refute a Claim

Evidence direction is explicit and may differ by claim or scope. Unfavorable direction does not reduce evidence legitimacy.

### 2.8 Limitations Must Travel With Evidence

Every transfer, reference, summary, and downstream use preserves material limitations and unresolved unknowns.

### 2.9 Contradictions Must Remain Visible

Contradictory evidence is linked, not deleted, averaged away, or hidden through selective packaging.

### 2.10 Frozen Evidence Cannot Be Edited In Place

Evidence under validation, risk review, or executive decision is immutable for that review identity. New material creates a new package and review version.

### 2.11 Validation Requires Chain of Custody

Validation cannot issue unconditional conclusions when material evidence identity, handling, transformation, or transfer cannot be reconstructed.

### 2.12 Reproducibility Is a First-Class Requirement

Evidence states whether and how the producing result can be regenerated, reconciled, independently repeated, or shown to be inherently non-repeatable.

### 2.13 Additional principles

- Evidence uncertainty is explicit.
- Evidence independence is assessed by lineage, not citation count.
- Summaries cannot strengthen their source.
- Missing evidence is not negative evidence unless the design supports that inference.
- Admissibility is use-specific and time-sensitive.
- Every challenge and invalidation is itself evidenced.
- Evidence remains attributable after archival and retirement.

## 3. Evidence Object Model

### 3.1 Definition

An Evidence Object is the smallest independently identifiable and governable unit of evidentiary material. It has stable identity, exact versions, explicit relationships to claims and institutional objects, defined custody, and an immutable audit trail.

### 3.2 Mandatory fields

Every Evidence Object must define:

| Field | Institutional requirement |
|---|---|
| Evidence ID | Stable unique identity across versions |
| Evidence Type | Governed class defined by this standard |
| Originating Agent | Agent responsible for submitting the evidence |
| Producing Process | Identified method, experiment, observation, or institutional process |
| Source MACP Message | Exact message authorizing or transferring the evidence |
| Related Memory Object | SMI identity and version coordinating state |
| Related Knowledge Object | Knowledge OS references and versions, if any |
| Related Decision Object | Decision IDs and versions that consume or govern the evidence |
| Related Experiment | Experiment and run identities and versions, if applicable |
| Supported Claim | Exact claims the evidence supports and degree of support |
| Challenged Claim | Exact claims the evidence weakens, contradicts, or refutes |
| Evidence Scope | Applicable markets, periods, samples, regimes, methods, versions, and uses |
| Evidence Version | Exact immutable state and effective time |
| Data Source | Origin, identity, coverage, access, and revision state of underlying data |
| Method Used | Method identity, purpose, controls, transformations, and evaluation process |
| Assumptions | Explicit requirements for interpretation and applicability |
| Limitations | Known boundaries, defects, missing information, and unresolved uncertainty |
| Known Contradictions | Related evidence and conflict status |
| Confidence Level | Calibrated confidence with dimension-level rationale |
| Reproducibility Status | Declared class, requirements, attempts, and discrepancies |
| Admissibility Status | Proposed use, reviewer, decision, restrictions, and expiry |
| Custody Status | Current custodian, freeze, integrity, and transfer state |
| Created At | Governed creation time and responsible actor |
| Updated At | Latest version or lifecycle event time and responsible actor |
| Audit Trail | Creation, handling, transfer, use, challenge, amendment, and invalidation history |

### 3.3 Additional properties

Where applicable, the object defines:

- title and concise description;
- original author or external institution;
- observation time, availability time, and publication time;
- units, definitions, sampling, and transformations;
- quality dimensions and evidence hierarchy position;
- selection and exclusion lineage;
- independence and shared ancestry;
- confidentiality, licensing, jurisdiction, retention, and access;
- integrity identity and completeness state;
- consumers, dependencies, review date, and expiry triggers;
- successor, correction, archive, and retirement relationships.

### 3.4 Stable versus version identity

Evidence ID identifies one continuing evidentiary object. Evidence Version identifies exact content, provenance, scope, limitations, relationships, and status. Material change creates a new version.

### 3.5 Atomicity and packages

An object must be narrow enough for independent provenance, challenge, versioning, and admissibility. Related objects may form a package, but packaging never erases distinct identities, contradictions, or confidence.

### 3.6 Derived evidence

Derived evidence identifies every material source version, transformation, loss of information, added assumption, responsible agent, and reproduction requirement. Derivation cannot increase authority merely by repetition.

### 3.7 Evidence relationships

Governed relationships include `supports`, `weakens`, `refutes`, `contradicts`, `qualifies`, `replicates`, `fails to replicate`, `extends`, `derived from`, `corrects`, `supersedes`, `invalidates`, `used by`, and `produced by`.

## 4. Evidence Lifecycle

### 4.1 Canonical lifecycle

Evidence follows the canonical lifecycle:

**Proposed → Submitted → Accepted → Frozen → Under Review → Validated → Challenged → Amended → Invalidated → Archived**

Not every valid evidence object passes through every state. Transitions follow object purpose and authority, but history remains complete.

### 4.2 Proposed

Evidence identity and preliminary metadata exist, but completeness, provenance, and admissibility have not been reviewed. It cannot support consequential decisions.

### 4.3 Submitted

The originating agent has delivered a complete candidate Evidence Object or Package under MACP, with declared purpose, consumers, and requested review.

### 4.4 Accepted

The receiving authority confirms identity, provenance, scope, contract completeness, integrity, access, and baseline fitness for the declared review. Acceptance is not validation or truth.

### 4.5 Frozen

The exact package is immutable for a defined validation, risk, or decision process. Freeze records versions, custodian, consumers, start, purpose, and release conditions.

### 4.6 Under Review

An authorized reviewer evaluates quality, relevance, methods, reproducibility, contradiction, admissibility, and claim relationship without altering the frozen evidence.

### 4.7 Validated

The responsible validation authority confirms that evidence satisfies the declared validation scope. Validation does not promote evidence to knowledge or authorize deployment.

### 4.8 Challenged

A governed challenge identifies a potential defect, contradiction, scope violation, reproduction failure, custody issue, or alternative explanation. Existing consumers are notified according to consequence.

### 4.9 Amended

A new evidence version corrects, extends, qualifies, or narrows a prior version. The prior version remains immutable, and downstream impact is assessed.

### 4.10 Invalidated

The competent authority determines that evidence must not support specified current uses because of fabrication, corruption, material error, invalid method, broken custody, unrecoverable provenance, or decisive contradiction. Invalidation is scoped and evidenced.

### 4.11 Archived

The evidence and complete lifecycle are preserved for audit, reproducibility, institutional memory, and historical decisions. Archived evidence cannot masquerade as current admissible evidence.

### 4.12 Transition rules

- Every transition cites a MACP message, actor, authority, evidence, time, previous state, and affected consumers.
- Acceptance cannot occur without provenance.
- Freeze cannot alter content.
- Challenge does not automatically invalidate evidence.
- Amendment creates a new version.
- Invalidation does not erase historical use.
- Archival preserves contradictions, limitations, and decisions.

## 5. Evidence Types

### 5.1 Market Observation Evidence

Time-bounded records of observed market structure, behavior, liquidity, volatility, participation, or regime characteristics. Observation is not strategy design and must distinguish measurement from interpretation.

### 5.2 Research Literature Evidence

Claims, methods, findings, limitations, corrections, and replications drawn from scientific papers, books, official documentation, and other governed sources with complete citation lineage.

### 5.3 Strategy Architecture Evidence

Artifacts demonstrating that a strategy design, mechanism, information model, module structure, and failure conditions match an approved hypothesis. It is not performance proof.

### 5.4 Engineering Implementation Evidence

Conformance, tests, traceability, deterministic behavior, data lineage, environment, and reconstruction evidence showing what was implemented and how faithfully.

### 5.5 Experiment Result Evidence

Outputs of registered experiments, linked to exact specification, runs, implementation, data, configuration, controls, deviations, and terminal status.

### 5.6 Backtest Evidence

Historical simulation results under declared data, execution, cost, timing, parameter, and accounting assumptions. Backtest evidence alone is never sufficient proof of edge.

### 5.7 Walk-Forward Evidence

Chronological development and test-fold evidence with exact boundaries, selection lineage, parameter freezing, aggregation, and untouched outer-test status.

### 5.8 Monte Carlo Evidence

Distributional evidence generated under explicit uncertainty models, resampling units, dependence assumptions, perturbations, scenario sufficiency, and tail limitations.

### 5.9 Parameter Stability Evidence

Evidence about performance neighborhoods, interactions, boundary behavior, perturbation sensitivity, robust regions, and cross-window consistency. Optimization output alone is not proof of edge.

### 5.10 Negative Control Evidence

Results from procedures expected not to preserve the claimed mechanism, including randomized, shuffled, shifted, or deliberately structure-destroyed controls.

### 5.11 Adversarial Test Evidence

Evidence produced under plausible hostile conditions such as worse costs, latency, missed fills, gaps, shocks, dependency failures, parameter perturbations, and data changes.

### 5.12 Validation Evidence

Independent reproduction, statistical, robustness, bias, scope, confidence, and verdict evidence produced by the Validation Agent.

### 5.13 Risk Evidence

Evidence about loss, drawdown, tails, liquidity, capacity, correlation, concentration, model, execution, operations, controls, limits, and readiness.

### 5.14 Decision Evidence

Evidence documenting what information, alternatives, authority, rationale, conditions, and acknowledgements supported an institutional decision. A decision record is evidence of the decision, not proof that its underlying claim was true.

### 5.15 Operational Monitoring Evidence

Time-indexed production observations of exposure, execution, model, data, controls, limits, incidents, and environmental conditions, with observation and availability timing.

### 5.16 Failure Evidence

Evidence from failed hypotheses, experiments, implementations, reproductions, controls, deployments, incidents, and near misses. Failure evidence is preserved regardless of publication preference.

### 5.17 Contradiction Evidence

Evidence whose institutional purpose is to expose incompatible claims, results, definitions, versions, scopes, or mechanisms. It remains visible until governed resolution.

## 6. Evidence Package Structure

### 6.1 Purpose

An Evidence Package groups related objects for a declared question and consumer while preserving each object's identity, direction, limitations, contradictions, and admissibility.

### 6.2 Required package sections

- Package ID, version, title, and status;
- originating agent, custodian, reviewers, consumers, and authority;
- institutional question and exact claims;
- purpose, intended use, prohibited use, and decision horizon;
- object inventory with exact Evidence IDs and versions;
- provenance and production-process summary;
- scope and applicability matrix;
- methods, assumptions, controls, and selection lineage;
- quality, confidence, independence, and completeness assessment;
- limitations, unknowns, exclusions, and access constraints;
- contradictions, negative evidence, and unresolved challenges;
- reproducibility manifest and attempt history;
- admissibility by consumer and use;
- custody, freeze, transfer, acknowledgement, and audit records;
- amendments, invalidations, successors, review, and expiry triggers.

### 6.3 Package integrity

The package states expected and present objects, missing objects, partial objects, integrity status, and whether absence affects interpretation. A selected subset cannot be presented as complete evidence.

### 6.4 Balanced packaging

Material unfavorable and contradictory evidence must travel with favorable evidence. Package construction cannot optimize for a preferred decision.

### 6.5 Claim-evidence matrix

Each claim maps to supporting, weakening, refuting, qualifying, and missing evidence. Relationships identify independence and common lineage.

### 6.6 Package versioning

Any addition, removal, substitution, correction, scope change, or relationship change creates a new package version. Frozen package versions remain immutable.

### 6.7 Package summary

Summaries distinguish evidence facts, producer interpretation, reviewer assessment, and decision relevance. They cannot replace underlying objects for validation or audit.

## 7. Evidence Provenance Requirements

### 7.1 Provenance chain

Evidence provenance records:

**Original source → acquisition or observation → producing process → transformations → experiment or analysis → Evidence Object → transfers → reviews → consumers → decisions → amendments or invalidation**

### 7.2 Source provenance

Identify creator, institution, publication or observation context, date, version, access path, authenticity, licensing, jurisdiction, and correction or retraction status.

### 7.3 Data provenance

Identify data provider, instrument and field definitions, timestamps, revision policy, coverage, sampling, missingness, exclusions, transformations, quality checks, and content version.

### 7.4 Process provenance

Identify responsible agent, approved specification, method, implementation, environment, dependencies, configuration, seeds, controls, selection path, deviations, and output identity.

### 7.5 Human and agent attribution

Human judgment, agent inference, automated transformation, and external-source claims are attributed separately. One cannot be presented as another.

### 7.6 Independence lineage

Multiple objects that derive from one source or experiment are one evidentiary lineage unless independent evidence exists. Copies, summaries, replications, and reanalyses are classified accurately.

### 7.7 Provenance gaps

Unknown or inaccessible lineage is explicit. Material provenance gaps restrict admissibility and confidence; they cannot be repaired through reputation or repetition.

### 7.8 Provenance correction

Correcting provenance creates a new version, identifies affected consumers and decisions, and determines whether prior admissibility or validation must be reopened.

## 8. Evidence Quality and Confidence

### 8.1 Quality dimensions

Evidence quality is assessed across:

- authenticity and integrity;
- provenance completeness;
- methodological appropriateness;
- data quality and temporal validity;
- relevance to the declared claim;
- sample sufficiency and representativeness;
- transparency and reproducibility;
- independence from related evidence;
- robustness and sensitivity;
- consistency and contradiction;
- recency and scope currency;
- bias, selection, and conflict-of-interest risk.

### 8.2 Quality levels

- **High quality:** strong provenance, suitable method, direct relevance, reproducibility, and no unresolved material defect.
- **Qualified quality:** useful evidence with explicit limitations or narrower applicability.
- **Provisional quality:** plausible but awaiting essential verification, access, replication, or lineage completion.
- **Weak quality:** material methodological, provenance, relevance, or independence limitations.
- **Unusable:** integrity, fabrication, corruption, or scope defects prevent the declared use.

### 8.3 Confidence dimensions

Confidence reflects evidence identity, quality, direction, effect magnitude, uncertainty, independence, consistency, reproducibility, robustness, and unresolved alternatives.

### 8.4 Confidence levels

- **High:** the stated evidentiary relationship is unlikely to reverse within declared scope given current admissible evidence.
- **Moderate:** the relationship is supported but material uncertainty or limitation remains.
- **Low:** evidence is suggestive but insufficient for reliance beyond exploratory use.
- **Indeterminate:** available evidence cannot support a calibrated direction.

### 8.5 Confidence is not authority

High confidence does not convert evidence into validation, knowledge, risk approval, or executive authorization.

### 8.6 Weak-link rule

Critical integrity, provenance, custody, or scope defects cap confidence regardless of favorable statistics elsewhere.

### 8.7 Confidence change

New evidence, contradiction, reproduction, correction, scope change, or invalidation creates a new assessment version and preserves the prior judgment.

## 9. Evidence Scope and Limitations

### 9.1 Scope dimensions

Every object states applicable:

- claim and null or competing claims;
- market, instrument, venue, asset class, and geography;
- timeframe, sampling, session, and decision horizon;
- historical period and regime;
- population, sample, and inclusion or exclusion rules;
- strategy, implementation, experiment, parameter, data, and method versions;
- cost, execution, liquidity, capacity, and operational assumptions;
- consumer, institutional use, and decision class.

### 9.2 Scope inheritance

Derived evidence cannot have broader scope than its material sources without separate evidence and justification. Aggregation does not automatically create generality.

### 9.3 Scope violations

Use outside scope creates an Evidence Use Error, requires consumer notification, and may reopen dependent decisions. Successful out-of-scope use does not retroactively authorize the violation.

### 9.4 Limitations

Limitations include missing data, sample bias, dependence, measurement error, model assumptions, approximations, selection, multiplicity, low power, sparse tails, cost uncertainty, unavailable sources, reproduction gaps, and conflicts.

### 9.5 Limitation propagation

Every transfer, summary, package, memory reference, validation, risk review, and decision preserves material limitations. Downstream agents may add limitations but cannot remove them without authorized evidence.

### 9.6 Unknowns

Known unknowns state impact, owner, closure evidence, and decision sensitivity. Unknown unknowns are addressed through robustness, monitoring, conservative scope, and revalidation triggers, not claims of certainty.

### 9.7 Expiry

Scope and admissibility expire when time, market structure, data, method, version, model, venue, cost, or operational context changes materially.

## 10. Evidence Transfer Rules

### 10.1 Transfer authority

Every transfer uses a valid MACP Evidence Transfer message identifying sender, recipients, purpose, package, versions, custody state, permissions, expected acknowledgement, and downstream use.

### 10.2 Sender duties

The sender verifies identity, completeness, provenance, integrity, scope, limitations, contradictions, access, current status, and intended use before transfer.

### 10.3 Recipient duties

The recipient validates sender authority, package identity, version compatibility, custody, admissibility, scope, restrictions, and completeness before acceptance or reliance.

### 10.4 Transfer outcomes

- accepted for declared use;
- accepted with explicit qualification;
- received but not admissible;
- requires correction or missing evidence;
- rejected for integrity, authority, access, or incompatibility;
- quarantined or escalated.

### 10.5 No implied acceptance

Delivery, access, citation, storage, or acknowledgement of receipt does not imply admissibility, validation, agreement, or decision acceptance.

### 10.6 Partial transfer

Partial, sampled, summarized, or redacted transfer states what is absent and whether the recipient can perform the intended task. Restricted primary evidence cannot be replaced by an unrestricted summary without limitation.

### 10.7 Transfer lineage

Each transfer records source and destination custodians, time, package version, integrity check, restrictions, acknowledgement, and resulting memory references.

### 10.8 Duplicate transfer

Duplicate delivery cannot create new evidence identity, repeat authority, or conceal differing versions. Conflicting duplicates trigger quarantine.

## 11. Evidence Freezing and Chain of Custody

### 11.1 Freeze purpose

Evidence freezing establishes an exact immutable package for validation, risk review, executive decision, audit, or other consequential process.

### 11.2 Freeze record

Every freeze defines:

- Freeze ID and source MACP message;
- package and object versions;
- purpose and consuming process;
- custodian and authorized readers;
- start, expiry, release, and invalidation conditions;
- integrity state and completeness;
- prohibited changes;
- permitted annotations and challenge path;
- affected tasks, decisions, and memory locks.

### 11.3 Frozen evidence

Frozen evidence cannot be edited, substituted, removed, or silently supplemented. Annotation, challenge, and external analysis create linked objects without changing the frozen package.

### 11.4 New evidence during review

New evidence is registered separately. The competent reviewer decides whether to complete the current review, suspend it, or create a new package and review version. It cannot be slipped into the current freeze.

### 11.5 Custody events

Creation, acquisition, transfer, transformation, freeze, access, reproduction, challenge, amendment, invalidation, archival, and retirement are custody events with actor, authority, time, version, integrity, and purpose.

### 11.6 Custody status

- intact;
- intact with qualified gap;
- disputed;
- broken but partially reconstructable;
- broken and inadmissible;
- archived under verified retention.

### 11.7 Custody break

A material unexplained custody break blocks unconditional validation and consequential reliance until independent governance resolves admissibility.

### 11.8 Freeze release

Release records review outcome, package integrity, resulting decisions, retained locks, consumers, new evidence, and archival obligations.

## 12. Evidence Contradictions and Challenges

### 12.1 Challenge right

Any authorized agent may challenge evidence within its competence. A challenge must identify the evidence version, issue, supporting material, consequence, and requested review. Challenges cannot alter the object directly.

### 12.2 Challenge classes

- provenance or authenticity challenge;
- custody or integrity challenge;
- method or assumption challenge;
- data quality or temporal challenge;
- reproducibility challenge;
- scope or applicability challenge;
- statistical or robustness challenge;
- independence or selection challenge;
- contradiction or alternative-explanation challenge;
- version, transfer, or admissibility challenge.

### 12.3 Challenge states

A challenge is recorded as submitted, accepted for review, rejected as unsupported, under investigation, resolved, sustained, partially sustained, or unresolved.

### 12.4 Interim treatment

Material challenge may qualify, freeze, quarantine, suspend admissibility, or notify consumers depending on severity. Challenge existence alone does not automatically invalidate evidence.

### 12.5 Contradiction record

Contradictory objects remain distinct and linked. The record compares claims, scopes, versions, data, methods, assumptions, independence, quality, and possible reconciliation.

### 12.6 Resolution outcomes

- not genuinely contradictory;
- scope-separated;
- method-dependent;
- version- or time-dependent;
- one object amended or invalidated;
- both retained with qualified confidence;
- unresolved pending new evidence.

### 12.7 Prohibited handling

Contradictions cannot be deleted, hidden, averaged without justification, resolved by popularity, or excluded because they reduce confidence or approval probability.

### 12.8 Consumer notification

Material challenge or contradiction identifies every validation, risk review, decision, knowledge object, and active task that relied on the evidence and communicates required action.

## 13. Evidence Amendment and Invalidation

### 13.1 Amendment classes

- metadata or provenance correction;
- scope clarification or narrowing;
- method or assumption correction;
- added limitation or contradiction;
- extended data or analysis;
- corrected result;
- successor evidence;
- breaking amendment that changes institutional interpretation.

### 13.2 Amendment requirements

Every amendment states parent version, reason, new evidence, changed and unchanged fields, authority, compatibility, affected claims, consumers, admissibility, confidence, and re-review obligations.

### 13.3 Historical preservation

The amended version never overwrites the parent. Historical decisions remain linked to the version they used, with later amendment notices.

### 13.4 Invalidation grounds

- fabrication or falsification;
- corruption or identity loss;
- irrecoverable provenance or custody failure;
- material implementation or data defect;
- invalid method or unauthorized transformation;
- decisive reproduction failure;
- material scope misrepresentation;
- retraction or correction that removes support;
- contradiction that conclusively defeats the declared use;
- governance violation that makes the evidence inadmissible.

### 13.5 Invalidation scope

Invalidation may apply to one claim, use, consumer, period, version, or the entire object. It states what remains valid and what is prohibited.

### 13.6 Invalidation authority

The authority depends on defect domain. Originating agents may report defects but cannot unilaterally erase evidence already used. Validation, Knowledge, Risk, Executive, QA, or other competent governance determines downstream status.

### 13.7 Impact analysis

Every invalidation traces dependent packages, tasks, experiments, validations, risk decisions, executive decisions, knowledge objects, artifacts, and production states. Required actions include annotation, suspension, revalidation, mitigation, revocation, or no impact.

### 13.8 Restoration

Invalidated evidence is not silently restored. A corrected object receives a new version and must pass provenance, quality, custody, admissibility, and review requirements again.

## 14. Evidence Admissibility

### 14.1 Definition

Admissibility is a governed determination that an exact evidence version may be used for a declared institutional purpose under stated restrictions. It is not a universal quality label.

### 14.2 Admissibility criteria

- stable identity and exact version;
- complete enough provenance and chain of custody;
- integrity and authenticity;
- declared scope matching proposed use;
- suitable method and data;
- visible assumptions, limitations, contradictions, and uncertainty;
- required reproducibility status;
- current lifecycle state;
- access and licensing permission;
- compatible MACP and SMI references;
- appropriate independent review and authority.

### 14.3 Admissibility outcomes

- admissible for declared use;
- admissible with qualifications;
- provisional and restricted;
- requires additional evidence or correction;
- inadmissible for declared use;
- quarantined pending integrity review.

### 14.4 Use-specific gates

Research exploration may admit provisional evidence with labels. Validation requires frozen chain-of-custody packages. Risk review must cite validated or explicitly qualified evidence. Executive deployment decisions must cite admissible validation and risk evidence for the same versions and scope.

### 14.5 Mandatory rules

- Evidence must never be accepted without provenance.
- Evidence must never be used outside its declared scope.
- Evidence must never be silently rewritten after being used.
- A backtest result is not sufficient evidence by itself.
- Optimization output is not proof of edge.
- Validation must use frozen evidence packages.
- Risk review must cite validated or explicitly qualified evidence.
- Executive decisions must cite admissible evidence.
- Contradictory evidence must not be deleted, hidden, or overwritten.
- Evidence uncertainty must be explicit.
- Evidence limitations must remain attached through all downstream use.

### 14.6 Admissibility expiry

Admissibility expires after material change to evidence, scope, method, data, implementation, market structure, consumer purpose, governing standard, validation verdict, or custody status.

### 14.7 Consumer responsibility

Every consumer validates current admissibility, version, scope, limitations, and expiry before consequential use. Prior acceptance by another consumer is not sufficient.

## 15. Integration with MACP

### 15.1 Relationship

MACP governs communication; EES governs evidentiary meaning. Every evidence creation, submission, transfer, acceptance, freeze, challenge, amendment, invalidation, and archival event uses an appropriate MACP message.

### 15.2 Message mappings

| MACP message | EES function |
|---|---|
| Request | Initiates evidence creation, retrieval, review, reproduction, or challenge |
| Evidence Transfer | Moves an exact package with provenance, scope, limitations, custody, and permissions |
| Acknowledgement | Records receipt, acceptance, qualification, rejection, or consumer obligation |
| Status Report | Communicates lifecycle, freeze, review, reproduction, or custody state |
| Error | Reports integrity, provenance, version, scope, access, or transfer failure |
| Escalation | Routes high-impact evidence conflict or governance issue |
| Conflict Report | Registers contradictory objects and resolution authority |
| Validation Event | Records freeze, review, verdict, suspension, or revalidation evidence state |
| Risk Event | Records evidence used, qualification, mitigation need, or risk-state impact |
| Decision | Cites exact admissible evidence and preserves rejected alternatives |
| Audit Message | Requests or records custody, lineage, access, and compliance evidence |
| Lifecycle Event | Announces submission, acceptance, freeze, challenge, amendment, invalidation, or archive |

### 15.3 Source message

Every Evidence Object and lifecycle transition cites its source MACP message. A file, result, or observation outside governed communication is not automatically institutional evidence.

### 15.4 Transfer acknowledgement

Recipients acknowledge exact versions, intended use, restrictions, missing elements, and custody. Acknowledgement of receipt is distinct from admissibility acceptance.

### 15.5 Communication integrity

MACP and EES states must agree on sender, recipient, versions, lifecycle, custody, conditions, and effective time. Inconsistency blocks consequential use.

### 15.6 No hidden context

Evidence interpretation cannot depend on private messages, model memory, or unstated conversation. Required context is inside the package or referenced through governed accessible objects.

### 15.7 Idempotency

Duplicate message delivery cannot create duplicate evidence, repeat freeze, or change admissibility. Conflicting message versions trigger an Error or Conflict Report.

## 16. Integration with SMI

### 16.1 Relationship

SMI preserves shared institutional state and references; EES governs the evidence those references identify. An SMI Evidence Reference is not a copy, replacement, or mutable view of the Evidence Object.

### 16.2 Required memory state

Every active Evidence Object has a related SMI object containing Evidence ID, exact version, type, owner, readers, writers, source MACP message, related objects, lifecycle, expiry, retirement, custody, and audit references.

### 16.3 Field ownership

Originating agents may create and propose evidence metadata. Custodians manage transfer and freeze state. Validation controls validation assessments. Knowledge Curator controls knowledge relationships. Risk and Executive agents control their decisions, not the evidence content.

### 16.4 Evidence immutability in memory

SMI cannot mutate frozen evidence or historical content. A write creates a new version or lifecycle event and preserves the prior object.

### 16.5 Locks

Evidence freezes use SMI locking to protect exact objects and package versions. Lock scope, owner, purpose, readers, duration, release, and emergency rules are explicit.

### 16.6 Reads

Consequential reads resolve exact versions and validate status, admissibility, custody, scope, limitations, contradictions, access, and expiry. Current aliases are recorded at read time.

### 16.7 Writes

Writes require authorized field ownership, source MACP message, current-version awareness, lock compliance, validation, lineage, and consumer notification.

### 16.8 Conflict objects

Contradictory evidence, concurrent amendment, stale write, and disputed custody create SMI Conflict Objects. Resolution preserves all candidate versions and authority.

### 16.9 Impact propagation

Amendment, challenge, invalidation, or expiry triggers SMI dependency analysis and MACP notification to tasks, experiments, validations, risk decisions, executive decisions, knowledge objects, and artifacts.

### 16.10 Archival and retirement

SMI preserves evidence identity, versions, lifecycle, custody, relationships, consumers, and audit state after archival or retirement. Retired evidence cannot authorize new work.

## 17. Governance

### 17.1 Constitutional scope

EES is mandatory for all AI Quant Lab agents, authorized humans, external gateways, and future models involved in evidence creation or use. Domain standards may strengthen but cannot weaken it.

### 17.2 Governance ownership

- Research agents own evidence production within approved research.
- Quant Strategy Engineer owns engineering evidence and implementation conformance records.
- Experiment Orchestrator owns experiment package and operational lineage.
- Validation Agent owns independent validation evidence and verdict assessment.
- Risk Governance owns risk evidence assessment and use qualification.
- Executive Decision Agent owns executive evidence-use decisions.
- Research Librarian owns source acquisition evidence and provenance packages.
- Knowledge Curator owns evidence-to-knowledge governance relationships.
- MACP Governance owns evidence communication.
- SMI Governance owns shared evidence-reference state and locks.
- QA independently audits compliance, custody, and remediation.
- Founder authority approves constitutional changes and reserved exceptions.

### 17.3 Agent conformance

Every Agent Contract must declare:

- evidence types created and consumed;
- producing processes and required provenance;
- claim and scope responsibilities;
- package, transfer, freeze, custody, and acknowledgement duties;
- quality, confidence, reproducibility, and admissibility requirements;
- amendment, challenge, invalidation, and conflict rights;
- MACP and SMI integration;
- retention, security, audit, and retirement obligations.

An agent unable to satisfy these requirements cannot create or rely on institutional evidence.

### 17.4 Violations

Violations include missing provenance or scope, hidden assumptions, silent mutation, unversioned reference, omitted contradiction, overstated confidence, broken custody, out-of-scope use, false admissibility, modified freeze, unauthorized invalidation, or decision reliance on inadmissible evidence.

Material violation triggers quarantine, consumer and dependency tracing, notification, suspension of affected reviews or decisions, independent investigation, correction or invalidation, remediation, and institutional knowledge capture.

### 17.5 Exceptions

An exception defines rule, evidence, purpose, scope, objects, consumers, risk, uncertainty, information loss, compensating controls, authority, duration, expiry, audit, and return to conformance. No exception may authorize fabricated provenance, silent mutation, hidden contradiction, false custody, or presentation of inadmissible evidence as validated.

### 17.6 Standard evolution

Every EES amendment defines:

- problem and supporting evidence;
- semantic change and alternatives;
- affected evidence types, lifecycle states, and agents;
- compatibility and historical interpretation;
- migration, custody, and lineage preservation;
- admissibility, reproducibility, security, MACP, SMI, and audit impact;
- conformance review, effective date, deprecation, and rollback;
- approving authorities.

### 17.7 Compatibility

Incompatible EES versions may coexist only through an approved translation and migration boundary that preserves provenance, scope, limitations, custody, and historical decisions. Silent downgrade is prohibited.

### 17.8 Periodic review

Governance asks:

- Does every accepted object have complete enough provenance and scope?
- Are exact versions used by every consequential consumer?
- Do limitations and contradictions travel with evidence?
- Are frozen packages genuinely immutable?
- Can chain of custody be reconstructed?
- Are backtests and optimization outputs prevented from becoming standalone proof?
- Do confidence and admissibility remain calibrated to later evidence?
- Are invalidations propagated to every dependent decision?
- Do MACP and SMI preserve evidence semantics and state?
- Are negative and failure evidence retained?
- Are exceptions becoming hidden policy?

### 17.9 Archival and retirement

Evidence may be archived after active use ends and all custody, consumer, decision, reproduction, and retention obligations are satisfied. Retirement prohibits new active use but preserves lawful identity, history, contradiction, and impact records.

### 17.10 Permanent rules

- Evidence must never be accepted without provenance.
- Evidence must never be used outside its declared scope.
- Evidence must never be silently rewritten after use.
- Frozen evidence cannot be edited in place.
- Evidence uncertainty and limitations remain explicit and attached.
- Backtest evidence alone is insufficient proof of edge.
- Optimization output is not proof of edge.
- Validation uses frozen evidence with intact custody.
- Risk review cites validated or explicitly qualified evidence.
- Executive decisions cite admissible evidence.
- Contradictory evidence is never deleted, hidden, or overwritten.
- Evidence remains distinct from decision and curated knowledge.
- Every consequential evidence state remains explainable, traceable, versioned, reproducible where required, and auditable.

EES governs evidence without changing the constitutional authority of the agents that create research, implement systems, validate science, accept risk, curate knowledge, or make institutional decisions.
