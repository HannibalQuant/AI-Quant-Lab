# AI Quant Lab Knowledge Operating System

## Document control

| Field | Value |
|---|---|
| Document class | Master knowledge architecture specification |
| Status | Proposed for Sprint 4 review |
| Authority | Governs knowledge used by every AI Quant Lab agent |
| Scope | Acquisition, classification, validation, relationships, retrieval, maintenance, evolution, and retirement of knowledge |
| Out of scope | Storage products, database design, indexing implementation, and user-interface design |
| Change control | Knowledge Architecture review and explicit governance approval |

The Knowledge Operating System, or Knowledge OS, defines how AI Quant Lab turns sources and experience into reliable, contextual, retrievable, and revisable knowledge. It is not a document collection. It is the control system that determines what an agent may know, why that knowledge is credible, where it applies, how it conflicts with other knowledge, and when it must no longer guide decisions.

## 1. Knowledge philosophy

### 1.1 Definition of knowledge

Knowledge is a versioned, contextual claim or relationship that has identifiable provenance, declared scope, evaluated evidence, known uncertainty, and defined consumers. It is sufficiently structured to inform reasoning and sufficiently bounded to be challenged, superseded, or retired.

A statement does not become knowledge merely because it appears in a book, paper, repository, experiment, or prior answer. Sources contain claims. The Knowledge OS determines how those claims are represented, evaluated, connected, and made available.

### 1.2 Data

Data are recorded observations or symbols before interpretation. Examples include market prices, volumes, timestamps, order events, experimental measurements, document text, and reported results.

Data have provenance, collection conditions, definitions, and quality limitations. Data are not neutral when selection, adjustment, missingness, or measurement rules influence what was recorded. The Knowledge OS treats data lineage as necessary but does not treat raw data as an established claim.

### 1.3 Information

Information is data organized to answer a defined question or describe a state. A return series, summary statistic, citation extract, market-state label, or comparison table is information because structure and context have been applied.

Information depends on transformation choices. It must retain the data identity, definitions, time boundaries, and method that produced it.

### 1.4 Knowledge

Knowledge is information interpreted into a bounded claim that has been evaluated for meaning, support, scope, and use. Knowledge states what is believed, why, under which conditions, with what confidence, and what would weaken it.

Knowledge may be descriptive, procedural, causal, statistical, operational, or normative. These types are not interchangeable. An operational rule may be authoritative without being a scientific claim; an empirical regularity may be well measured without establishing a causal mechanism.

### 1.5 Evidence

Evidence is an observation, source, experiment, or result used to increase or decrease confidence in a claim. Evidence is always evidence for or against something. It has relevance, quality, independence, and scope.

Evidence does not become stronger merely by volume. Several sources derived from one original result are not independent confirmations. Evidence that contradicts a claim is preserved with the same care as supportive evidence.

### 1.6 Hypothesis

A hypothesis is a falsifiable proposition about behavior, relationship, mechanism, or outcome that has not yet earned stable knowledge status. It declares expected observations and failure conditions.

Hypotheses remain distinct from established knowledge so agents do not retrieve speculation as fact. Supported hypotheses may mature into bounded knowledge; rejected hypotheses enter historical and failure knowledge rather than disappearing.

### 1.7 Model

A model is a purposeful representation that explains, estimates, classifies, or predicts within a declared domain. It selects some features of reality and omits others. Its usefulness depends on assumptions, calibration, validation, and intended decision.

A model is not knowledge by itself. The model definition, assumptions, evaluation, failure conditions, and observed performance each become linked knowledge objects.

### 1.8 Theory

A theory is a coherent explanatory structure connecting multiple claims and mechanisms across observations. It generates hypotheses and predicts relationships beyond a single result.

Theories carry scope and competing explanations. The Knowledge OS does not elevate a theory because it is widely cited; it records the nature and strength of its support, conflicts, and applicability.

### 1.9 Knowledge is dynamic

Markets, tools, libraries, platforms, regulation, execution venues, and scientific understanding change. Even correct knowledge can lose operational relevance when its context changes. New evidence can narrow, qualify, contradict, or supersede earlier conclusions.

Knowledge therefore has a lifecycle rather than a permanent true/false label. It can be candidate, reviewed, validated, restricted, deprecated, contradicted, superseded, retired, or archived. Historical knowledge remains available for reconstruction even when it is no longer eligible for current decisions.

### 1.10 Provenance is mandatory

Every knowledge object must answer:

- who or what originated the claim;
- where and when it was published, observed, or produced;
- which version or edition was used;
- how the object was transformed or summarized;
- which reviewer validated the representation;
- which parent objects and evidence support it;
- which permissions or licensing constraints apply.

Without provenance, a claim may be retained as an unverified lead but cannot be treated as validated knowledge. Provenance protects against citation drift, duplicated evidence, silent reinterpretation, and false authority.

### 1.11 Knowledge serves decisions

Knowledge quality is evaluated relative to consequence. A general learning resource may tolerate broader uncertainty than a production risk rule. The more consequential the decision, the stronger the requirements for source authority, validation, freshness, scope match, and independent review.

The Knowledge OS must allow an agent to retrieve not only an answer, but also the evidence, contradictions, uncertainty, and applicability required to decide whether the answer may be used.

## 2. Knowledge layers

### 2.1 Layer model

```text
Raw Sources
↓
Structured Knowledge
↓
Validated Knowledge
↓
Research Knowledge
↓
Production Knowledge
↓
Historical Archive
```

Layers express eligibility and responsibility, not storage location. A knowledge object may advance, be restricted, return for revalidation, or enter the archive. Advancement is explicit and never inferred from age or repeated use.

### 2.2 Raw Sources

**Purpose:** preserve source identity and original context before project interpretation.

**Contents:** books, papers, official documentation, repository revisions, community material, datasets, experiment outputs, incident records, meeting decisions, and external observations.

**Responsibilities:** record origin, authorship, date, version, access path, licensing, integrity, capture time, and source type; preserve enough context to verify quotations and claims; identify unavailable or mutable sources.

**Eligibility:** raw sources may support discovery but are not automatically available as authoritative knowledge. Untrusted, promotional, or unverifiable sources are clearly marked.

**Failure boundary:** a source without recoverable identity, permitted use, or sufficient context cannot advance beyond an unverified reference.

### 2.3 Structured Knowledge

**Purpose:** convert source material into explicit claims, definitions, methods, observations, and relationships.

**Contents:** normalized citations, extracted claims, concept definitions, bounded summaries, method descriptions, source-specific assumptions, and candidate links.

**Responsibilities:** separate source claim from project interpretation; assign taxonomy; identify scope, units, markets, horizons, versions, and terminology; preserve quotation boundaries; prevent one document from becoming one undifferentiated object.

**Eligibility:** structured objects are discoverable for review. They remain provisional until evidence and representation are validated.

**Failure boundary:** ambiguous extraction, missing context, unsupported paraphrase, or incorrect classification returns the object to source review.

### 2.4 Validated Knowledge

**Purpose:** identify knowledge whose representation, provenance, evidence, and scope have passed the required review.

**Contents:** reviewed claims, authoritative definitions, verified platform behavior, validated methods, confirmed relationships, and bounded conclusions.

**Responsibilities:** assign evidence and confidence levels; record supporting and contradicting objects; evaluate independence and freshness; define consumers and permitted uses; set revalidation frequency.

**Eligibility:** validated knowledge may inform research within declared scope. Validation does not make a claim universally true or production-approved.

**Failure boundary:** material contradiction, expired review, source retraction, version change, or scope mismatch restricts use until revalidation.

### 2.5 Research Knowledge

**Purpose:** support hypothesis formation, experiment design, strategy architecture, and interpretation of results.

**Contents:** market observations, research hypotheses, experiment plans, internal results, strategy specifications, alternative explanations, negative controls, failure patterns, and research lessons.

**Responsibilities:** link every conclusion to experiments and external evidence; preserve unsuccessful attempts; distinguish exploratory from confirmatory findings; track sample, market, horizon, and regime applicability.

**Eligibility:** research knowledge may guide further research. It cannot independently authorize production behavior.

**Failure boundary:** contamination, undisclosed multiple testing, irreproducibility, or missing experiment lineage prevents promotion and lowers confidence.

### 2.6 Production Knowledge

**Purpose:** provide the narrow, current, approved knowledge required for operational decisions.

**Contents:** approved strategy definitions, execution rules, risk limits, deployment manifests, platform semantics, operating procedures, monitoring thresholds, incident actions, and current known limitations.

**Responsibilities:** enforce exact version, named authority, effective date, environment, scope, dependencies, rollback target, and review schedule; link to validation, risk, and approval evidence.

**Eligibility:** only explicitly promoted objects may enter. Production agents retrieve from this layer by exact identity or approved active reference.

**Failure boundary:** expiry, supersession, unresolved contradiction, failed dependency, breached assumption, or withdrawal of approval immediately restricts operational use.

### 2.7 Historical Archive

**Purpose:** preserve organizational memory, auditability, and the ability to understand past decisions.

**Contents:** superseded versions, retired strategies, deprecated documentation, rejected hypotheses, failed experiments, prior production results, incidents, retractions, and obsolete platform behavior.

**Responsibilities:** preserve lineage and temporal context; prevent archived knowledge from appearing current; support retrospective analysis and repeated-failure prevention; retain legal and policy constraints.

**Eligibility:** archived knowledge is retrievable for history, comparison, and lessons. It cannot guide current production without formal revalidation and promotion.

**Failure boundary:** archive loss, broken lineage, or current retrieval without archival warning is a system integrity failure.

## 3. Knowledge domains

### 3.1 Taxonomy principles

Domains describe subject matter. Layers describe lifecycle status. Object types describe epistemic function. A paper about execution may belong to `Academic Papers` and `Execution`, remain in the Structured layer, and contain several claim objects with different evidence levels.

Objects may have one primary domain and multiple related domains. Classification must not duplicate the object or erase cross-domain relationships.

### 3.2 Source and method domains

| Domain | Scope | Required distinctions |
|---|---|---|
| Books | Durable conceptual, mathematical, market, and operational treatments | Edition, author authority, age, citations, explanatory versus empirical content |
| Academic Papers | Peer-reviewed and preprint research | Publication status, methodology, data, replication, correction, retraction, and scope |
| TradingView Documentation | Platform behavior, chart semantics, alerts, strategies, and limitations | Official documentation versus observed behavior; version and publication date |
| Pine Script | Language semantics, execution model, patterns, and verified limitations | Language version, platform context, confirmed versus inferred behavior |
| Python | Language and library behavior relevant to research | Language and package version, official contract, numerical and behavioral caveats |
| Machine Learning | Learning paradigms, evaluation, representation, and model risk | Supervised, unsupervised, sequential, causal, generative, and reinforcement contexts |
| Statistics | Estimation, testing, resampling, uncertainty, and multiple comparisons | Assumptions, finite-sample behavior, robustness, and misuse conditions |
| Probability | Random processes, distributions, dependence, and stochastic reasoning | Definitions, conditions, approximations, and applicable event space |

### 3.3 Market and decision domains

| Domain | Scope | Required distinctions |
|---|---|---|
| Market Mechanics | Contract, venue, session, funding, settlement, margin, and instrument behavior | Asset class, venue, instrument type, jurisdiction, and effective period |
| Market Microstructure | Order interaction, liquidity, price discovery, impact, and participant behavior | Data resolution, venue structure, queue assumptions, and execution access |
| Portfolio Theory | Allocation, dependence, diversification, concentration, and objectives | Estimated versus assumed relationships, horizon, constraints, and stability |
| Risk Management | Market, liquidity, model, operational, counterparty, and governance risk | Measurement, limit, control, escalation, and residual risk |
| Behavioral Finance | Participant biases, institutional behavior, incentives, and limits to arbitrage | Mechanism evidence, population, context, and alternative explanations |
| Execution | Signal-to-order conversion, fills, costs, routing, and reconciliation | Paper versus live, order type, venue, latency, capacity, and failure state |
| Order Flow | Transactions, imbalance, positioning, and liquidity interaction | Direct measurement versus proxy, aggregation, venue coverage, and sign inference |

### 3.4 Internal evidence and governance domains

| Domain | Scope | Required distinctions |
|---|---|---|
| Experiments | Planned comparisons and their artifacts | Exploratory versus confirmatory, parent hypothesis, controls, splits, and stopping rule |
| Internal Research | Project analyses and bounded conclusions | Authoring agent, independent review, data and method lineage, and confidence |
| Strategy Specifications | Authoritative behavioral and decision definitions | Version, lifecycle state, assumptions, invalidation, and consumers |
| Production Results | Paper and live outcomes, execution, risk, and monitoring | Expected versus observed, strategy version, environment, and incident context |
| Failure Reports | Hypothesis, data, method, code, execution, control, and process failures | Detection, impact, root cause, contributing factors, containment, and recurrence risk |
| Lessons Learned | Reviewed reusable conclusions from experience | Supporting objects, scope, confidence, contradictions, and review date |
| Repository Documentation | Architecture, standards, decisions, procedures, and interfaces | Authority, status, owner, effective version, and supersession |

### 3.5 Domain ownership

Each domain has an accountable curator responsible for terminology, inclusion rules, review standards, known gaps, and cross-domain mappings. Ownership does not grant power to approve claims outside the owner's expertise or lifecycle authority.

## 4. Knowledge objects

### 4.1 Unit of knowledge

A knowledge object is the smallest independently citable, versionable, reviewable, and relatable unit that can inform reasoning. A document is usually a source container containing multiple knowledge objects. Splitting is sufficient when claims have different evidence, scope, confidence, contradictions, or consumers.

### 4.2 Mandatory fields

| Field | Requirement |
|---|---|
| Unique ID | Persistent identity that never changes when title or location changes |
| Title | Precise human-readable description of the object |
| Category | Object type, primary domain, secondary domains, and lifecycle layer |
| Source | Recoverable source identity, location, version, and capture context |
| Author | Original author or producing agent, plus validating roles where applicable |
| Publication Date | Original publication or production date and effective date when different |
| Confidence Level | Current confidence with component rationale and uncertainty |
| Evidence Level | Strength and type of supporting evidence under the evidence hierarchy |
| Related Topics | Controlled concepts, markets, methods, states, and artifacts |
| Dependencies | Objects, definitions, data, assumptions, or policies required for validity |
| Contradictions | Conflicting objects, conflict type, status, and current interpretation |
| Consumers | Agents, workflows, and decisions permitted or expected to use the object |
| Last Validation | Date, validator, method, result, and evidence version used |
| Review Frequency | Time-based and event-based revalidation triggers |
| Version History | Immutable revisions, reasons, reviewers, and supersession links |
| Retirement Status | Active, restricted, deprecated, superseded, retired, or archived with reason |

### 4.3 Additional control fields

Decision-grade objects also record scope, non-applicable contexts, claim type, assumptions, supporting objects, counterevidence, source independence, licensing, sensitivity, effective period, owner, review authority, freshness class, and eligible lifecycle uses.

### 4.4 Object types

- **Source object:** identity and integrity of an external or internal source.
- **Claim object:** bounded proposition attributed to a source or project conclusion.
- **Definition object:** controlled meaning of a term, metric, state, or rule.
- **Method object:** repeatable analytical or operational procedure with assumptions.
- **Observation object:** measured behavior without an explanatory claim.
- **Hypothesis object:** falsifiable proposed relationship.
- **Model object:** representation with purpose, assumptions, and evaluation.
- **Evidence object:** result used to support or contradict a claim.
- **Decision object:** authorized choice with evidence and policy context.
- **Failure object:** invalidated assumption, defect, incident, or rejected outcome.
- **Lesson object:** reviewed generalization linked to underlying evidence.

### 4.5 Confidence representation

Confidence is not a popularity score. It records separate judgments for source reliability, representation accuracy, evidence strength, evidence independence, scope match, reproducibility, freshness, and contradiction status.

An aggregate label may be used for retrieval:

- **Unverified:** captured but not adequately reviewed.
- **Low:** limited, indirect, stale, or materially contradicted support.
- **Moderate:** relevant support with unresolved limitations or incomplete independence.
- **High:** strong, relevant, reproducible, independently supported evidence within bounded scope.
- **Authoritative:** governing policy or official behavior for a declared version and context; authority does not imply scientific truth outside that context.

The components and rationale remain visible even when a summary label is present.

### 4.6 Immutability and identity

Once cited in a decision, an object version is immutable. Corrections create a new version and relationship to the original. The persistent Unique ID identifies the conceptual lineage; each version has its own immutable identity.

## 5. Knowledge ingestion

### 5.1 Ingestion flow

```text
Source
↓
Source validation
↓
Claim extraction and classification
↓
Relationship mapping
↓
Evidence and confidence scoring
↓
Knowledge graph review
↓
Controlled availability
```

### 5.2 Source registration

The Research Librarian or producing agent registers source identity, type, authorship, publication state, date, version, access method, licensing, integrity, and reason for ingestion. Mutable sources are captured with a retrieval date and version evidence.

Duplicate detection occurs at source and claim level. Copies, summaries, and citations of one original source do not become independent evidence.

### 5.3 Source validation

Validation asks whether the source is authentic, complete enough for use, current for the intended question, permitted for retention, and represented by the correct version. Retractions, corrections, abandoned repositories, conflicts of interest, and publication status are recorded.

Failure does not always require deletion. A questionable source may remain discoverable as low-confidence context or as evidence of a claim's history, but it cannot silently advance.

### 5.4 Claim extraction

Sources are decomposed into definitions, methods, claims, observations, assumptions, results, limitations, and open questions. Extracted objects preserve exact attribution and local context.

Project inference is stored separately from source claim. A summary cannot strengthen, generalize, or causalize a source beyond its own statement without an explicit derived object and evidence.

### 5.5 Classification

Each object receives type, domain, layer, topic, market, horizon, state, method, consumer, and sensitivity classifications. Unknown classification is explicit. Classification uses controlled vocabulary while preserving source terminology as aliases.

### 5.6 Relationship mapping

The object is connected to definitions, evidence, dependencies, alternatives, contradictions, superseded versions, experiments, strategies, decisions, and consumers. Missing expected relationships create a review flag; for example, a conclusion without evidence or a production rule without approval.

### 5.7 Evidence scoring

Evidence is evaluated for source authority, methodological quality, relevance, independence, reproducibility, sample adequacy, uncertainty, execution realism, and freshness. Score rationale is retained. Automated scoring may prioritize review but cannot convert unreviewed content into validated or production knowledge.

### 5.8 Knowledge graph review

Review verifies claim boundaries, provenance, classification, evidence links, contradiction handling, confidence, consumer eligibility, and review schedule. High-consequence objects require independent subject-matter review.

### 5.9 Availability

Availability is granted by consumer and use case. An object may be visible for exploration but prohibited for production decisions. Retrieval must expose lifecycle state, confidence, evidence, contradictions, version, and freshness alongside content.

## 6. Knowledge quality

### 6.1 Evidence hierarchy

Evidence strength depends on the claim. The following hierarchy provides a default, not an automatic ranking:

1. independently reproduced internal or external evidence under relevant conditions;
2. well-designed primary scientific or empirical research with accessible methods and limitations;
3. authoritative official documentation for a specific system and version;
4. verified internal experiments with complete lineage and independent validation;
5. high-quality synthesis grounded in traceable primary evidence;
6. maintained open-source repositories with reviewed behavior and reproducible tests;
7. expert books with explicit sources and durable conceptual reasoning;
8. documented community analysis with reproducible evidence;
9. forum discussion and anecdotal operational reports;
10. personal observation without controlled validation.

A lower-ranked source may be the best evidence for a narrow operational observation. An official document may be authoritative about intended behavior while an independently reproduced test reveals actual divergence. Claim type and context govern interpretation.

### 6.2 Scientific evidence

Scientific evidence is evaluated through question clarity, design, data suitability, controls, statistical reasoning, effect magnitude, uncertainty, robustness, replication, publication status, conflicts, and applicability to current markets. Peer review is relevant but not sufficient.

### 6.3 Books

Books are evaluated for author expertise, edition, citations, distinction between theory and anecdote, age relative to changing mechanics, and consistency with primary evidence. Books are often strong for frameworks and weak as sole support for current empirical claims.

### 6.4 Official documentation

Official documentation is authoritative for declared interfaces, semantics, rules, and supported behavior of a named version. It may be incomplete, outdated, or inconsistent with observed behavior. Verified discrepancies become contradiction objects rather than silent corrections.

### 6.5 Open-source repositories

Repositories are evaluated by exact revision, ownership, maintenance, license, test evidence, issue history, dependency risk, reproducibility, and correspondence between documentation and behavior. Popularity does not establish correctness.

### 6.6 Community content

Community articles, videos, scripts, and analyses may generate leads or reveal practical failure cases. They require attribution, evidence tracing, conflict review, and independent validation before becoming research knowledge.

### 6.7 Forum discussions

Forum discussions are low-control evidence useful for discovering terminology, incidents, edge cases, and contested behavior. Identity, incentives, sample selection, and reproducibility are usually uncertain. They are never treated as independent confirmation merely because many posts repeat a claim.

### 6.8 Personal observations

Personal or agent observations are valid starting points for hypotheses. They become knowledge only after their population, measurement, baseline, and alternative explanations are examined. The original observation remains linked to subsequent evidence and rejection.

### 6.9 Confidence adjustment

Confidence increases with relevant independent support, successful reproduction, stable scope, verified provenance, discriminating tests, and survival of counterevidence. Confidence decreases with contradiction, dependency on one source or sample, failed reproduction, stale context, changed system version, weak applicability, or unknown transformation.

Confidence does not increase because an object is frequently retrieved or operationally convenient.

## 7. Knowledge graph

### 7.1 Purpose

The knowledge graph represents why objects are related, not merely that they share words. Relationships are directed, typed, version-aware, and attributable. Each relationship may have its own evidence, confidence, scope, and review state.

### 7.2 Core relationships

| Relationship | Meaning |
|---|---|
| `SUPPORTS` | Source object increases confidence in the target within declared scope |
| `CONTRADICTS` | Source object conflicts with the target's claim, conditions, or implication |
| `EXTENDS` | Source object broadens or adds detail without replacing the target |
| `DEPENDS_ON` | Source object requires the target's validity or definition |
| `SUPERSEDES` | Source object replaces the target for current eligible use |
| `DERIVED_FROM` | Source object was transformed or inferred from the target |
| `ALTERNATIVE_TO` | Objects provide competing methods, explanations, or formulations |
| `REQUIRES` | Object cannot be used without the target condition, approval, or capability |
| `USED_BY` | Named agent, strategy, decision, or workflow consumes the object |
| `PRODUCES` | Experiment, method, process, or agent generated the target object |

### 7.3 Relationship rules

`SUPPORTS` and `CONTRADICTS` require a stated claim dimension; one object may support existence while contradicting mechanism or scope. `SUPERSEDES` does not delete the prior object. `DERIVED_FROM` preserves transformation lineage. `USED_BY` records actual or authorized consumption and enables impact analysis.

Circular dependencies are review failures unless the cycle is explicitly explanatory rather than evidentiary. A claim cannot support itself through derived summaries.

### 7.4 Contradiction model

Contradictions are classified as:

- direct factual conflict;
- difference in definitions;
- difference in market, period, horizon, or regime;
- difference in method or measurement;
- intended behavior versus observed behavior;
- version change;
- competing causal explanation;
- statistical uncertainty;
- unresolved source-quality conflict.

The Knowledge OS does not force premature consensus. Conflicting objects remain available with their evidence and scopes. A contradiction may be resolved, contextualized, escalated for discriminating research, or left open. Retrieval must disclose material unresolved contradictions.

### 7.5 Impact tracing

When an object is corrected, deprecated, or contradicted, the graph identifies dependent strategies, experiments, documents, decisions, models, and agents. Impact review determines whether consumers require revalidation, restriction, or replacement.

## 8. Knowledge consumption

### 8.1 Retrieval contract

Agents request knowledge by question, intended decision, domain, market, horizon, required evidence, maximum acceptable staleness, and eligible lifecycle layer. Retrieval returns a bounded evidence set, not a single decontextualized answer.

Every response includes object identities, versions, claims, provenance, confidence, evidence level, scope, assumptions, contradictions, dependencies, freshness, and permitted use. If knowledge is insufficient, the result states the gap and recommended acquisition or experiment.

### 8.2 Quant Strategy Architect

Retrieves market behavior, mechanisms, strategy-family evidence, market mechanics, failure patterns, prior specifications, and relevant negative results. It requires competing explanations and contradictions. It may consume validated and research knowledge but cannot treat exploratory findings as production authority.

### 8.3 Research Agent

Retrieves broad source and evidence maps, unresolved questions, prior experiments, definitions, and known gaps. It may access lower-confidence structured knowledge for discovery, provided lifecycle status remains visible. Its outputs return as hypotheses or candidate objects, not silent updates to validated knowledge.

### 8.4 Python Agent

Retrieves authoritative definitions of metrics, statistical methods, data semantics, validated strategy specifications, market mechanics, dependency behavior, and known numerical failures. Version match is mandatory. Community examples may inform exploration but cannot override official or internally validated contracts.

### 8.5 Pine Agent

Retrieves official TradingView and Pine semantics, validated platform observations, approved strategy definitions, parity lessons, and prior platform failures. It must receive the exact applicable language and strategy versions, plus unresolved contradictions between documentation and observed behavior.

### 8.6 Validation Agent

Retrieves validation policy, metric definitions, known biases, test methods, failure database, strategy lineage, prior contradictory evidence, and holdout-access rules. It receives evidence independently of the producing agent's preferred summary.

### 8.7 Risk Agent

Retrieves current risk policy, market and venue mechanics, stress history, liquidity behavior, dependency maps, incidents, model limitations, and production assumptions. Only current validated or production-eligible knowledge may define enforceable limits; historical objects support comparison with clear archival status.

### 8.8 CEO Agent

Retrieves decision-ready evidence bundles, unresolved contradictions, validation and risk dispositions, production dependencies, knowledge gaps, and impact analysis. Summaries must preserve blocking uncertainty and dissent. The CEO Agent cannot infer approval from frequent use or high source count.

### 8.9 Consumption accountability

Decision records capture which object versions were used. Agents must not rely on private memory where an authoritative object exists. If an agent rejects retrieved knowledge, it records the reason and either selects an eligible alternative or requests review.

## 9. Knowledge evolution

### 9.1 Versioning

Material changes to claim, scope, evidence, confidence, relationships, permitted use, or conclusion create a new object version. Metadata corrections that do not alter interpretation may use a controlled correction record. Versions remain linked and retrievable.

The version used by a past decision never changes retroactively.

### 9.2 Deprecation

Deprecation signals that an object remains interpretable but should not be selected for new work. Reasons include newer guidance, changed terminology, approaching expiry, partial contradiction, or better alternatives. Deprecation declares replacement, affected consumers, and transition period when applicable.

### 9.3 Revalidation

Revalidation is triggered by time, system version change, new contradiction, source correction, failed reproduction, market-structure change, production anomaly, new evidence, policy change, or dependency retirement.

Review scope is proportional to impact. Production knowledge receives the shortest review horizon and the strongest event triggers. Revalidation may confirm, narrow, downgrade, supersede, or retire an object.

### 9.4 Replacement

Replacement creates a `SUPERSEDES` relationship and migration guidance. Consumers are identified through `USED_BY`, `DEPENDS_ON`, and `REQUIRES` relationships. Replacement is complete only when active consumers either migrate or record an approved exception.

### 9.5 Knowledge decay

Knowledge decay is loss of decision relevance caused by changed environment, weakened evidence, outdated version, missing maintenance, or widening mismatch between scope and use. Decay risk depends on domain:

- mathematical definitions decay slowly;
- scientific conclusions decay when evidence changes;
- market behavior may decay with participants and regimes;
- platform and library semantics decay with versions;
- liquidity and execution knowledge may decay rapidly;
- production procedures decay when dependencies or controls change.

Objects have freshness classes and decay indicators. Age alone does not prove invalidity, but expired review prevents high-consequence use.

### 9.6 Continuous learning

Continuous learning is the governed conversion of new evidence into candidate knowledge. It includes experiments, paper and live results, failures, incidents, external research, and changed documentation.

Learning never silently changes production knowledge. New observations enter ingestion, receive provenance and classification, and pass review. If they alter an approved strategy or rule, a new version re-enters the appropriate research and validation lifecycle.

### 9.7 Retirement

Retirement removes an object from eligible current use while preserving it in historical context. Retirement records reason, authority, date, replacement, affected consumers, unresolved risk, and conditions for possible reactivation.

Retired objects cannot return through retrieval frequency or agent preference. Reactivation requires revalidation under current policy.

### 9.8 Lessons learned

A lesson is not created from one surprising result. It requires linked evidence, bounded applicability, review, contradiction analysis, and a statement of how future decisions should change. Lessons inherit revalidation triggers from their dependencies.

## 10. Future integrations

### 10.1 Integration principles

Integrations provide sources, metadata, observations, or controlled actions. They do not assign final knowledge status. Every integration must preserve source identity, version, retrieval time, licensing, transformation, and access constraints.

Provider-specific classifications are mapped to project taxonomy without erasing original terms. Failure or removal of an integration must not destroy already accepted provenance or knowledge identity.

### 10.2 TradingView MCP

TradingView MCP may provide official and observed platform knowledge, script and alert artifacts, chart-context observations, and parity evidence. Read and write capabilities remain separate. Retrieved behavior is tagged by platform state, script version, symbol, timeframe, and capture time. Platform output cannot self-validate strategy knowledge.

### 10.3 GitHub

GitHub provides versioned repository documentation, source definitions, reviews, issues, release history, and decision context. Commit and release identity are preserved. Repository popularity, stars, or forks are not evidence of correctness. Mutable branches are not permanent knowledge identities.

### 10.4 arXiv

arXiv provides preprints and version history. Objects retain preprint status, revision, authorship, category, and links to later publication, correction, withdrawal, replication, or critique. Preprint availability is not peer-review evidence.

### 10.5 SSRN

SSRN provides working papers and research versions, particularly in finance and economics. Version, publication progression, methodology, and conflicts are tracked. Working-paper claims remain bounded by their review and replication state.

### 10.6 Google Scholar

Google Scholar supports discovery and citation mapping. Search rank and citation count are discovery signals, not quality scores. The Knowledge OS resolves records to original sources and identifies citation dependence before evidence scoring.

### 10.7 Official documentation

Official documentation integrations track product, language, platform, and library versions, effective dates, deprecation notices, corrections, and observed discrepancies. Exact-version retrieval is required for decision-grade use.

### 10.8 Internal experiments

Experiment integration registers hypotheses, plans, manifests, artifacts, failures, and validation status. It prevents results from entering knowledge without parent questions, data identity, method, and review. Exploratory and confirmatory status remain distinct.

### 10.9 Benchmark datasets

Benchmark integrations preserve dataset version, license, collection process, population, splits, known leakage, revisions, and limitations. Benchmark performance is knowledge only within the benchmark's scope and cannot establish production suitability.

### 10.10 Research databases

Research databases may supply papers, metadata, replications, market data, reference data, and institutional research. Access rights, retention limits, redistribution constraints, source dependencies, and update behavior are attached to every derived object.

### 10.11 Integration acceptance

A future integration is accepted only when it defines source authority, object mapping, version semantics, provenance guarantees, licensing, update and deletion behavior, failure states, contradiction handling, and revalidation triggers.

## 11. Knowledge governance

### 11.1 Roles

- **Research Librarian:** acquires and represents external sources.
- **Knowledge Curator:** maintains taxonomy, relationships, lifecycle, contradictions, and lessons.
- **Domain owner:** validates meaning and scope within expertise.
- **Producing agent:** owns accuracy of internally generated objects.
- **Independent reviewer:** assesses evidence, confidence, and eligibility.
- **Consumer:** uses exact eligible versions and records material use.
- **CEO Agent:** resolves cross-domain priority and decision conflicts.
- **Founder:** approves changes to governing purpose and irreversible knowledge policy.

### 11.2 Non-negotiable controls

1. No provenance, no validated knowledge.
2. No immutable version, no decision-grade citation.
3. No scope, no safe reuse.
4. No contradiction disclosure, no complete retrieval.
5. No review state, no production eligibility.
6. No consumer mapping, no reliable impact analysis.
7. No historical preservation, no organizational learning.
8. No revalidation trigger, no durable trust.

### 11.3 Health measures

Knowledge OS health is assessed through provenance completeness, orphaned objects, unresolved contradictions, expired reviews, unsupported claims, stale production dependencies, failed retrieval traceability, duplication, broken supersession chains, uncurated failures, and consumer use of ineligible versions.

Retrieval volume is not a quality measure. A healthy Knowledge OS improves the relevance, transparency, and correction speed of decisions.

### 11.4 Governing outcome

The Knowledge OS succeeds when every agent can determine not only what the project currently believes, but why, within which scope, with what uncertainty, against which contradictions, for which decisions, and until when that belief remains eligible for use.

