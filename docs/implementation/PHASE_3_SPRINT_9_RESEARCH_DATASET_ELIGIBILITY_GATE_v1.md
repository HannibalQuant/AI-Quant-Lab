# Phase 3 Sprint 9: Research Dataset Eligibility & Controlled Dataset Admission Gate v1.0

## 1. Exact baseline

Implementation started from governed `main`
`9a6d94d0397647316c7ae7acff45bcd72ee18b61`, the merge commit of PR #69.
The superior Constitution v1.0 remains
`50b61266f880cb9657b7f1b477d3d90825fe013f`. Phase 1/2 artifacts, Sprint 1–8
reports and all prior golden fixtures remain unchanged. `EXE-01 = PLANNED_CLOSED`.

## 2. Purpose and bounded scope

Sprint 9 adds one deterministic gate between an existing technical CSV admission and
the controlled research dataset domain. It can decide `ELIGIBLE`, `INELIGIBLE`,
`QUARANTINED`, `INCOMPLETE` or `UNSUPPORTED` under one exact immutable policy. It
does not authenticate a provider, establish legal truth, authorize an experiment,
run research, calculate performance, validate a result, authorize deployment or open
execution.

The preserved authority chain is:

`TECHNICALLY ADMITTED != RESEARCH ELIGIBLE != EXPERIMENT AUTHORIZED != VALIDATED != DEPLOYMENT AUTHORIZED != EXECUTION`.

## 3. Non-goals

No strategy, feature, indicator, signal, backtest, optimizer, walk-forward, Monte
Carlo, validation, portfolio, monitoring, broker/exchange adapter, network client,
paper/live trading or order-routing capability is introduced. No catalog, database,
mutable policy pointer or policy auto-discovery is added.

## 4. Eligibility semantics

`ELIGIBLE` means only that the exact dataset may enter the controlled research data
domain under the exact recorded policy.

## 5. States

The bounded states are `ELIGIBLE`, `INELIGIBLE`, `QUARANTINED`, `INCOMPLETE` and
`UNSUPPORTED`. Every record retains `NOT_TRUSTED`,
`NOT_AUTHORIZED` experiment/deployment state, `NOT_VALIDATED` validation state and
`PLANNED_CLOSED` execution state. Any non-eligible state has explicit sorted unique
findings and `NOT_ADMITTED_TO_RESEARCH`.

## 6. Policy contract

`ResearchDatasetEligibilityPolicy` is frozen, versioned and canonically
fingerprinted. It declares accepted permission, retention, missing-data, duplicate
and ordering states; required timestamp and availability semantics; explicit calendar
semantics; deterministic knowledge cutoff; minimum rows; maximum rejected rows,
quarantined observations, actual gaps and missing intervals; complete-bar
requirement; local-research treatment of redistribution restrictions; and the policy
owner identity. Different policy content or version produces a different exact policy
reference. There is no mutable “current policy”.

## 7. Eligibility record and output

`ResearchDatasetEligibilityRecord` binds:

- exact admission and source-declaration references;
- exact source, instrument, timeframe and schema references;
- exact raw manifest/lock and normalized manifest/lock references where admitted;
- exact policy reference and quality-context fingerprint;
- deterministic status, findings, decision time and actor ID;
- closed downstream experiment, validation, deployment and execution states.

`ResearchDatasetEligibilityResult` returns the record, immutable write results and an
exact lineage verification for technically admitted inputs. An actor ID is evidence,
not authenticated authority; IP-01/IP-03/IP-13 remain open.

## 8. Authority separation

Provider text, filename, hash, parsing, persistence and dataset existence confer no
trust or authenticity. The policy owner and decision actor are exact recorded IDs,
not authenticated principals and not an invented delegation system.

## 9. Source policy

Technical admission alone cannot grant eligibility. Prohibited permission is
`INELIGIBLE`; unknown or non-accepted restricted permission is `QUARANTINED`;
unknown retention is `INCOMPLETE`. Restricted redistribution is allowed only when
the exact policy explicitly permits bounded local research. Unknown permission and
unknown retention remain non-eligible even if listed by a policy allow-list: policy
configuration cannot promote semantic uncertainty into research authority.

## 10. Temporal policy — IP-05

The policy pins required UTC open/close semantics, explicit source availability,
deterministic knowledge cutoff and explicit calendar mode. Availability after the
cutoff fails closed. Decision time is distinct from ingestion and availability time;
a decision predating ingestion is incomplete. `SOURCE_SPECIFIC_REQUIRED` remains
incomplete without a governed source calendar. No availability timestamp is
fabricated and no universal 24/7 assumption is silently applied. Provider late-data,
correction-clock and calendar truth remain unresolved institutional policy.

## 11. Quality policy — IP-11

The gate consumes an exact deterministic quality snapshot covering CSV and ingestion
rejections, quarantined observations, normalization rejections, incomplete bars,
actual missing-interval gaps, bar findings, normalized availability times and import
status. The snapshot fingerprint is bound by both request and record. Explicit policy
bounds decide eligibility; changing the snapshot requires exact rebinding and changes
the decision record. No hidden or universal provider-quality heuristic exists.

## 12. Licensing and retention — IP-12

The gate enforces declared permission, retention and local-use restrictions. These
remain operator declarations, not legal findings. It performs no license
interpretation, redistribution, deletion, recovery or external upload. Competent
legal and lifecycle authority remains open.

## 13. Exact lineage

Before an admitted dataset can become `ELIGIBLE`, the gate calls
`verify_real_csv_lineage()`, which delegates raw-to-normalized verification to
`verify_dataset_lineage()`. It additionally requires declaration-exact source,
instrument, timeframe and schema scopes and verifies the final eligibility record
against exact admission, declaration, policy, quality context and four dataset refs.
Tampered admission, wrong declaration, wrong manifest/lock, broken bar lineage or
policy-version mismatch fails closed.

Required traceability is explicit:

`RealCsvSourceDeclaration -> RealCsvAdmissionRecord -> exact dataset lineage -> eligibility policy -> quality context/findings -> eligibility decision -> immutable record -> verified reload -> test evidence`.

## 14. Persistence and integrity

Sprint 9 reuses canonical JSON v1, domain-separated SHA-256 integrity and
`LocalDatasetRepository`. Two minimal immutable storage families are added:

```text
objects/research-dataset-eligibility-policy/v<version>/<fingerprint>.json
objects/research-dataset-eligibility-record/v1/<fingerprint>.json
```

Writes are exact-key and idempotent; conflicting content never overwrites. Reads are
strict typed canonical reloads with fingerprint verification. There is no latest
alias, index, catalog or database. Hash verifies bytes, not authenticity.

## 15. Findings and determinism

Findings are bounded deterministic strings, sorted and duplicate-free. Examples
include `technical_admission_required`, `source_permission_unknown`,
`source_permission_prohibited`, `retention_unknown`,
`availability_semantics_unknown`, `calendar_semantics_unknown`,
`gaps_exceed_declared_policy`, `insufficient_row_count` and
`availability_after_policy_cutoff`. Same exact dataset, policy, quality context,
actor, decision time and record identity produce the same canonical record and
fingerprint. A material policy change produces a distinct reference and decision.

## 16. Security and failure boundaries

All existing hostile-file, immutable-store and lineage controls remain. Missing
finding context, non-admitted input, reference mismatch, policy mismatch, corrupted
canonical bytes and changed quality context fail closed. There is no fallback,
closest match, inferred source authority, auto-upgrade or downstream authorization.

## 17. Tests and evidence

Focused Sprint 9 tests cover eligible deterministic decisions, policy variation,
canonical round-trip, immutable persistence/reload, exact lineage, all downstream
authority closures, non-admitted/unknown/prohibited/ambiguous inputs, retention,
calendar and coverage gates, tampered admission/declaration/dataset artifacts/bars,
policy mismatch, quality-context mutation and corrupted persisted bytes.

The new read-only repository-owned
`tests/golden/research_dataset_eligibility_v1.json` pins admission, declaration, raw
and normalized manifest/lock, policy, quality-context and eligibility fingerprints,
status and findings. It is never regenerated by tests. All earlier goldens remain
byte-identical.

Quality evidence at branch completion:

- focused Sprint 9: 19 passed;
- full pytest: 293 passed;
- governance-negative: 14 passed;
- ruff format/check and mypy: passed;
- Python 3.12/3.13 CI: pending Draft PR.

## 18. Preconditions BEFORE -> AFTER

No technical implementation substitutes for competent approval. Counts remain
`RESOLVED 0 -> 0`, `PARTIALLY_RESOLVED 5 -> 5`, `OPEN 9 -> 9`, `DEFERRED 0 -> 0`.

| ID | Before -> after | Sprint 9 evidence | Remaining authority gap |
|---|---|---|---|
| IP-01 | OPEN -> OPEN | actor ID recorded | authentication and assurance |
| IP-02 | PARTIAL -> PARTIAL | canonical integrity/reload | signatures, trust roots, authenticity |
| IP-03 | OPEN -> OPEN | no authority inferred from IDs | delegation/revocation authority |
| IP-04 | PARTIAL -> PARTIAL | policy/record canonical codecs | broader representation approval |
| IP-05 | PARTIAL -> PARTIAL | UTC, availability, cutoff, calendar policy | provider late-data/calendar/clock truth |
| IP-06 | OPEN -> OPEN | no emergency runtime | emergency/release authority |
| IP-07 | OPEN -> OPEN | no approval runtime | confirmation/expiry policy |
| IP-08 | OPEN -> OPEN | no validation/monitoring freshness claim | freshness crosswalk |
| IP-09 | OPEN -> OPEN | no validation method | validation specification |
| IP-10 | OPEN -> OPEN | no monitoring method | thresholds/windows/multiplicity |
| IP-11 | PARTIAL -> PARTIAL | exact quality snapshot and explicit bounds | provider/universal acceptance authority |
| IP-12 | OPEN -> OPEN | declared restrictions enforced locally | legal verification and lifecycle authority |
| IP-13 | OPEN -> OPEN | exact actor/source/file lineage | authenticated actor/provider and broader adapters |
| IP-14 | PARTIAL -> PARTIAL | deterministic golden/reload/failure tests | production release governance |

## 19. Readiness matrix

- `RESEARCH_DATASET_ELIGIBILITY_GATE_READY`
- `DATASET_ELIGIBILITY_POLICY_READY`
- `ELIGIBILITY_LINEAGE_READY`
- `ELIGIBILITY_PERSISTENCE_READY`
- `CONTROLLED_RESEARCH_DATASET_READY`
- `EXPERIMENT_AUTHORIZATION_NOT_READY`
- `BACKTESTING_NOT_READY`
- `VALIDATION_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `EXECUTION_CLOSED`

These labels apply only to the repository-owned governed test pathway and exact
policy-bound datasets. They are not production, legal, authenticity or experiment
readiness claims.

## 20. Blockers and limitations

No blocker remains for the bounded eligibility gate. Provider authenticity,
authenticated decision authority, competent legal/license approval, source-specific
late-data/calendar truth, broader quality acceptance and production release remain
open. Multi-object policy/record persistence is not transactional and inherits the
bounded local durability/concurrency limits documented in Sprint 7.

## 21. Sprint disposition

`PHASE 3 SPRINT 9 COMPLETE WITH OPEN PRECONDITIONS` if final local gates and CI pass.

## 22. Recommended Sprint 10 discussion only

The next candidate is **Controlled Experiment Authorization & Experiment Foundation**:
exact experiment identity, eligible-dataset binding, deterministic configuration and
seed, no-lookahead contract, cost/slippage declarations, explicit authorization and
reproducibility evidence. Sprint 9 implements none of that work and does not jump to
strategy optimization.
