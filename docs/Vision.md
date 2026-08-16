# Vision

## Document status

- **Purpose:** define the durable purpose and five-year target state of AI Quant Lab
- **Audience:** owners, agent designers, quantitative researchers, developers, reviewers, and operators
- **Authority:** normative for project scope and design priorities
- **Review cadence:** annually or after a material change in project mandate

## Definition

AI Quant Lab is a governed multi-agent system for quantitative strategy research. It coordinates specialized analytical and engineering roles through explicit contracts, reproducible workflows, and independent quality gates.

The intended lifecycle is:

```text
market universe
→ data qualification
→ market and timeframe selection
→ regime characterization
→ hypothesis and edge testing
→ strategy specification
→ implementation
→ optimization
→ independent validation
→ portfolio and risk review
→ deployment decision
→ live monitoring
→ adaptation or retirement
```

AI Quant Lab is not a signal generator, a collection of indicators, or a prompt library. Its primary product is a traceable decision process supported by code and evidence.

## Why the project exists

Quantitative research often fails through process defects rather than lack of computational power. Recurring defects include:

- searching many combinations without controlling for multiple testing;
- allowing future information to influence features, labels, parameters, or selection;
- optimizing and evaluating on the same historical segment;
- changing hypotheses after observing results without preserving the original test;
- using data with undocumented gaps, revisions, timezones, or venue-specific errors;
- modeling fills that could not occur under realistic spread, liquidity, funding, or latency;
- treating one instrument, timeframe, window, or seed as representative;
- implementing different semantics in research, chart, alert, and execution code;
- reporting returns without tail, drawdown, stability, and capacity analysis;
- losing lineage between a conclusion and the code, data, configuration, and decision that produced it.

AI Quant Lab exists to make these defects observable and enforceable. Automation is useful only when it strengthens controls; faster invalid research is not progress.

## Problem solved

The project coordinates five domains that require different incentives:

1. **Research:** convert observations into falsifiable hypotheses and defensible tests.
2. **Engineering:** produce deterministic, testable, and portable implementations.
3. **Validation:** attempt to invalidate candidates independently of their producers.
4. **Risk:** constrain position, portfolio, liquidity, and operational exposure.
5. **Governance:** decide what may advance and preserve the evidence for that decision.

A research agent should explore; a validation agent should challenge; a risk agent should constrain; a governance agent should decide. Combining these responsibilities creates self-approval without an effective control boundary.

## Why retail trading tools are insufficient

Retail platforms are effective for visualization, scripting, alerts, and rapid prototyping. They are generally insufficient as the sole institutional research environment because they provide only part of the lifecycle. Typical limitations include:

- limited experiment lineage and environment capture;
- weak enforcement of training, validation, and untouched evaluation boundaries;
- inadequate controls for repeated trials and selection bias;
- simplified execution, capacity, funding, and liquidity models;
- inconsistent chart, backtest, alert, and broker behavior;
- restricted portfolio-level and cross-strategy risk analysis;
- limited Walk-Forward, Monte Carlo, parameter-stability, negative-control, and adversarial testing;
- weak independent approval workflows and immutable decision records;
- difficult semantic reconciliation with external research code.

AI Quant Lab does not replace useful retail platforms. It isolates them behind adapters and treats their output as evidence subject to verification. TradingView may remain a delivery and visualization surface; Python provides the reference research environment; parity tests govern the boundary.

## Philosophy

### Research must be falsifiable

Each strategy begins with a statement about conditional market behavior, the mechanism that may support it, the population to which it applies, and observations that would invalidate it. Indicator combinations without a stated hypothesis do not qualify as research specifications.

### Evidence has a hierarchy

An attractive in-sample result is weak evidence. Stronger evidence includes chronological holdouts, repeated Walk-Forward folds, parameter neighborhoods, cross-market tests, conservative execution perturbations, negative controls, and stable results across independent seeds.

### Reproducibility is part of correctness

A result that cannot be recreated from recorded inputs is not a valid project artifact. Code revision, data fingerprint, configuration, runtime environment, random seed, and execution assumptions are mandatory lineage fields.

### Agents have bounded authority

Agents may propose, implement, analyze, reject, or escalate within explicit mandates. No agent may silently change validation boundaries, risk limits, or deployment state. Greater autonomy requires stronger observability, rollback, and kill-switch mechanisms.

### Simplicity is a control

Complexity must earn its place through measurable incremental value. Fewer parameters, explicit state transitions, stable interfaces, and small modules reduce statistical and operational risk.

### Rejection is a valid result

The system should reject most candidates. A supported rejection reduces future research waste and protects the integrity of the candidate set. Negative findings retain the same lineage standards as positive findings.

## Five-year target state

### Unified research control plane

All experiments are registered before execution and produce immutable manifests. The platform can reconstruct why a candidate exists, which evidence supports it, which data it used, and which reviews authorized every state transition.

### Multi-asset research

Data adapters normalize crypto, foreign exchange, commodities, indices, and equities while preserving venue-specific mechanics. Core modules consume stable domain schemas rather than provider payloads.

### Specialized agent organization

Strategy design, evidence management, Python implementation, Pine implementation, validation, risk, QA, and governance operate independently. Communication occurs through validated artifacts and event records.

### Institutional validation discipline

Evaluation includes chronological holdouts, Walk-Forward, Monte Carlo, parameter stability, multiple-testing controls, selection-bias measures, adversarial execution scenarios, cross-market tests, and portfolio-risk interaction.

### Controlled deployment lifecycle

Strategies advance through `RESEARCH`, `VALIDATION`, `PAPER`, `CANDIDATE`, `CHAMPION`, `DEGRADED`, `DISABLED`, and `RETIRED`. Transitions require defined evidence and named authority. Deployment artifacts are immutable and reversible.

### Continuous evidence monitoring

Paper and live behavior are compared with expected distributions. The system monitors data quality, execution divergence, rolling expectancy, profit factor, drawdown, signal frequency, regime exposure, and assumption validity. Degradation triggers escalation or disablement according to policy.

### Human-accountable autonomy

Routine research orchestration may be autonomous, but material risk changes, new execution venues, capital allocations, and validation exceptions require accountable approval.

## Success criteria

The project succeeds when:

- a third party can reproduce an experiment from its manifest;
- no candidate reaches deployment without independent required reviews;
- Python and Pine executions reconcile trade by trade when both are used;
- every metric traces to a dataset, configuration, code revision, and execution model;
- failed work remains searchable;
- strategy degradation is detected against predefined expectations;
- execution can stop or roll back without relying on the failing component;
- adding a market, agent, or integration does not require rewriting the research core.

Profitability alone is not a sufficient project success criterion. The platform is responsible for research integrity and controlled execution; market returns remain uncertain.

