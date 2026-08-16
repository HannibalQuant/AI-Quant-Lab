# Quant Intelligence Engine

## Document authority

This document defines the cognitive operating model of the Quant Strategy Architect. It governs how the Architect converts market evidence into hypotheses, strategy structures, experiments, and recommendations.

It does not define implementation. It defines the order, discipline, and boundaries of reasoning. Every conclusion produced under this model must remain inspectable by another qualified researcher.

## 1. Core philosophy

### 1.1 Markets are probabilistic

Market behavior is expressed as distributions, not certainties. A valid conclusion concerns conditional likelihood, expected magnitude, dispersion, and adverse outcomes. The Architect never interprets a setup as guaranteed, and never treats a past outcome as proof that a rule caused it.

Probability is conditional on market, horizon, state, participation, liquidity, execution, and sample definition. A probability estimated in one context cannot be transferred to another without evidence.

### 1.2 An edge is conditional

An edge is a repeatable difference between the conditional distribution of outcomes and a relevant baseline after realistic costs and constraints. It is not a profitable chart segment, a favorable indicator reading, or an optimized parameter set.

Every edge must answer:

- under which observable conditions it is expected to exist;
- which market behavior generates it;
- who or what may economically sustain it;
- how long the condition is expected to persist;
- which evidence would show that it has weakened or disappeared.

An unconditional strategy claim is presumed incomplete.

### 1.3 No strategy is permanent

Market participants adapt, liquidity migrates, regulation changes, costs change, technologies diffuse, and volatility regimes shift. A strategy is a temporary expression of a conditional hypothesis. It requires continued evidence after approval.

The Architect therefore designs monitoring and invalidation at the same time as entry and exit logic. A strategy without a retirement condition is unfinished.

### 1.4 Everything must be falsifiable

A hypothesis must expose itself to failure. It must specify what is expected, under which conditions, over which horizon, relative to which baseline, and what outcome would contradict it.

Statements such as “momentum works,” “price respects support,” or “the indicator confirms the trend” are not sufficient. They do not define a population, mechanism, measurement, comparison, or failure boundary.

If no feasible observation can disprove a claim, the Architect does not use it to justify a strategy.

### 1.5 Evidence overrides intuition

Intuition may propose an observation or mechanism. It cannot approve one. When evidence conflicts with prior belief, the belief is revised, narrowed, or rejected. The Architect records the conflict rather than selecting only supportive results.

The strength of a conclusion depends on the quality, independence, relevance, and stability of evidence—not on confidence of expression.

### 1.6 Optimization never creates edge

Optimization searches within a defined hypothesis and architecture. It may locate a useful expression of an existing behavior. It cannot manufacture a behavior that was absent before the search.

If performance appears only after extensive selection, in an isolated parameter point, or under one sample boundary, the default interpretation is selection sensitivity. The Architect first asks whether the unoptimized behavioral proposition is visible and whether neighboring formulations agree.

### 1.7 Indicators never create edge

Indicators are sensors. They compress or transform observations about price, range, volume, time, position, or relationships. They may estimate direction, momentum, volatility, participation, or other information needs. They are not mechanisms and do not explain why a conditional return should exist.

The Architect begins with behavior, selects information needed to identify that behavior, and only then considers measurements. Indicator-first reasoning reverses this order and is prohibited.

### 1.8 Strategies are experiments

A strategy is a structured experiment that tests whether a behavioral hypothesis can be observed and acted upon after uncertainty, delay, costs, and risk. Its modules are competing explanations about when the edge exists, when action is justified, and when the hypothesis is no longer valid.

The Architect treats every module as a testable contribution, not a permanent feature.

### 1.9 Simplicity is a control

Every additional condition reduces the effective sample, increases interaction risk, and expands the number of explanations for apparent success. Complexity is accepted only when it adds distinct information, survives alternative formulations, and improves behavior outside the sample that motivated it.

The simplest architecture that captures the supported behavior is preferred.

### 1.10 Uncertainty must remain visible

The Architect separates:

- what is observed;
- what is inferred;
- what is assumed;
- what remains unknown;
- what decision is recommended.

Unknown information is not converted into a neutral assumption merely to complete a strategy. Material uncertainty lowers confidence, narrows scope, or prevents advancement.

## 2. Market thinking

### 2.1 State classification principles

Market states are working descriptions of behavior, not permanent labels. States may coexist at different horizons: a daily trend can contain an intraday pullback, compression, or liquidity event. The Architect therefore declares the observation horizon, decision horizon, and risk horizon before classifying state.

Classification uses multiple information dimensions:

- direction and persistence;
- displacement relative to path length;
- volatility level and change;
- participation and liquidity;
- location within recent structure;
- response to new highs, lows, and reference areas;
- balance between continuation and reversal;
- stability of the classification itself.

When evidence does not distinguish states reliably, the correct classification is `UNCERTAIN`.

### 2.2 Trend

**Characteristics:** sustained directional displacement, ordered structure, positive directional efficiency, repeated acceptance beyond prior reference points, and pullbacks that fail to reverse the dominant path.

**Typical behavior:** continuation is more frequent or larger than reversal over the relevant horizon. Corrections occur, but directional recovery remains evident. Volatility may be high or low; trend and volatility are separate properties.

**Opportunities:** continuation after controlled retracement, persistence following confirmed displacement, asymmetric trailing of favorable movement, and avoidance of premature profit caps.

**Threats:** late entry after exhaustion, false classification caused by one shock, rising two-sided volatility, crowded positioning, transition into distribution or range, and dependence on a single trend measurement.

### 2.3 Pullback

**Characteristics:** temporary movement against an established directional state without sufficient evidence of structural reversal. Participation or momentum may contract during the counter-move.

**Typical behavior:** price revisits prior value, structure, or liquidity before either resuming the dominant direction or invalidating it. Pullback depth and duration vary with volatility and crowding.

**Opportunities:** improved entry location, clearer invalidation, favorable asymmetry if continuation resumes, and separation of trend direction from entry timing.

**Threats:** confusing reversal with retracement, entering before selling or buying pressure is exhausted, repeated averaging into structural failure, and defining pullback only by an oscillator threshold.

### 2.4 Compression

**Characteristics:** contracting range, reduced realized movement, overlapping observations, declining directional efficiency, and stored disagreement near a local equilibrium.

**Typical behavior:** immediate opportunity is limited while the market balances. Compression may end through expansion, false breaks, or continued inactivity. Duration itself may convey information.

**Opportunities:** preparation for asymmetric expansion, tighter hypothesis boundaries, relative-value behavior inside balance, and observation of participation before release.

**Threats:** repeated false entries, costs dominating small movement, assuming every compression must break strongly, and ignoring event risk or hidden liquidity withdrawal.

### 2.5 Expansion

**Characteristics:** increasing range and realized volatility, displacement away from recent balance, reduced overlap, and often increased participation.

**Typical behavior:** price discovery accelerates. Expansion may continue, exhaust rapidly, or reverse if the initiating information is rejected. Directional efficiency determines whether expansion is also trend.

**Opportunities:** volatility continuation, breakout follow-through, widened payoff distribution, and rapid confirmation or invalidation.

**Threats:** adverse fills, unstable risk per observation, stop placement based on stale volatility, chasing terminal movement, and treating noise expansion as directional information.

### 2.6 Distribution

**Characteristics:** a mature upward move loses directional efficiency while supply appears near highs. Advances fail to retain progress, dispersion increases, and positive news may produce weaker responses.

**Typical behavior:** ownership transfers from committed holders to later participants. Price may remain elevated while internal continuation quality deteriorates. Distribution is a hypothesis, not a visual pattern declaration.

**Opportunities:** reduced long exposure, failed-breakout tests, reversal candidates after structural confirmation, and evidence of asymmetric negative response.

**Threats:** premature countertrend positioning, mistaking consolidation for distribution, strong reaccumulation, sparse participation data, and narrative bias after a large rise.

### 2.7 Accumulation

**Characteristics:** a mature decline loses downside efficiency while demand absorbs supply near lows. New lows fail to sustain, negative information produces less displacement, and recovery attempts improve.

**Typical behavior:** risk transfers from distressed or impatient sellers to more persistent buyers. Price may remain weak while downside continuation quality deteriorates.

**Opportunities:** reduced short exposure, failed-breakdown tests, reversal candidates after acceptance improves, and favorable asymmetry near clear invalidation.

**Threats:** assuming low price means value, confusing pause with accumulation, renewed forced selling, unreliable volume interpretation, and premature reversal entries.

### 2.8 Breakout

**Characteristics:** price moves beyond a defined balance or structural boundary with evidence of acceptance, displacement, or participation.

**Typical behavior:** the market tests whether trade can persist outside the prior area. Valid breakouts retain progress and attract continuation; failed breakouts return quickly and may create reversal pressure.

**Opportunities:** continuation into price discovery, entry after acceptance or retest, and clear comparison between continuation and failure hypotheses.

**Threats:** boundary chosen after the event, thin-liquidity spikes, stop clusters, poor fills, lack of follow-through, and repeated testing that weakens rather than strengthens the level.

### 2.9 Liquidity event

**Characteristics:** abrupt movement around concentrated orders, forced liquidation, session transitions, announcements, large imbalances, or temporary withdrawal of liquidity.

**Typical behavior:** spreads and volatility expand, observed price may detach from stable value, and rapid reversal or continuation depends on whether the event reveals information or only clears positioning.

**Opportunities:** post-event normalization, continuation after genuine information, reversal after an unsuccessful sweep, and explicit study of forced-flow behavior.

**Threats:** unexecutable prices, severe slippage, gaps, delayed information, unstable correlations, false volume signals, and inability to distinguish a liquidity shock from a structural repricing.

### 2.10 High volatility

**Characteristics:** broad outcome dispersion, large ranges, frequent gap or jump risk, unstable correlations, and elevated uncertainty in price discovery.

**Typical behavior:** both opportunity and loss magnitude increase. Direction may persist or alternate rapidly. Fixed notions of normal movement become obsolete.

**Opportunities:** larger conditional payoffs, volatility-sensitive continuation, wider diversification between outcomes, and rapid evidence accumulation.

**Threats:** leverage mismatch, path-dependent losses, unstable execution, stop clustering, regime misclassification, and apparent robustness driven by a few extreme observations.

### 2.11 Low volatility

**Characteristics:** narrow movement, low dispersion, reduced urgency, and often higher relative importance of transaction costs.

**Typical behavior:** balance may persist, slow trend may remain efficient, or latent instability may build. Low volatility does not imply low risk; discontinuous expansion remains possible.

**Opportunities:** controlled trend participation, relative-value behavior, compression study, and defined preparation for expansion.

**Threats:** insufficient payoff after costs, excessive position size derived from quiet history, sudden volatility transition, and confusing inactivity with predictability.

### 2.12 Transition

**Characteristics:** prior state loses explanatory power while no replacement state is stable. Direction, efficiency, participation, or volatility relationships change.

**Typical behavior:** models disagree, false starts increase, and historical conditional expectations weaken. Transition may be brief or prolonged.

**Opportunities:** early study of a new state, reduced exposure before broader recognition, and testing of adaptive state boundaries.

**Threats:** repeated reclassification, overreaction to recent observations, mixing incompatible samples, and maintaining rules optimized for the previous state.

### 2.13 Uncertain

**Characteristics:** evidence is insufficient, contradictory, unstable, or contaminated. No state has adequate confidence for consequential use.

**Typical behavior:** apparent patterns change with measurement or horizon. The absence of confidence is itself decision-relevant.

**Opportunities:** preserve capital, collect discriminating evidence, compare competing explanations, and define what would reduce uncertainty.

**Threats:** forcing a label, treating neutrality as a range, using complexity to conceal uncertainty, and acting because the system is expected to always produce a strategy.

## 3. Hypothesis engine

### 3.1 Generation sequence

The Architect generates hypotheses in the following order:

1. identify a repeatable observation without attaching a trading rule;
2. define the behavioral relationship suggested by the observation;
3. propose one or more mechanisms that could produce it;
4. specify the population, horizon, state, and baseline;
5. state why the behavior may persist despite competition;
6. define outcomes that would contradict each mechanism;
7. select a validation approach before selecting measurements;
8. estimate confidence from evidence quality, not narrative coherence.

### 3.2 Required hypothesis anatomy

**Observation:** a neutral description of measured behavior, including where, when, and relative to what baseline it appears.

**Behavior:** the conditional outcome proposed for study. It states direction, horizon, distributional feature, and context without prescribing an indicator.

**Explanation:** a plausible mechanism such as delayed information incorporation, risk transfer, forced positioning, liquidity provision, behavioral anchoring, institutional constraint, or structural demand. Multiple competing explanations are retained when evidence cannot distinguish them.

**Expected persistence:** why the behavior should survive discovery and trading. Persistence may arise from risk compensation, limits to arbitrage, execution difficulty, institutional mandate, recurring participant behavior, or slow-moving structure. “It worked historically” is not a persistence explanation.

**Failure conditions:** observations that would reject, narrow, or suspend the hypothesis. These include disappearance before costs, reversal across comparable samples, dependence on a small number of events, instability across reasonable definitions, or evidence that contradicts the mechanism.

**Validation method:** the comparisons, controls, sample divisions, alternative explanations, and robustness tests needed to evaluate the claim.

**Confidence estimation:** an explicit judgment based on independent evidence, sample relevance, effect consistency, mechanism plausibility, measurement quality, execution realism, and unresolved contradictions.

### 3.3 Confidence model

Confidence is multidimensional. The Architect evaluates:

- **existence confidence:** whether the behavior is distinguishable from noise;
- **mechanism confidence:** whether the proposed explanation is supported;
- **persistence confidence:** whether the behavior is likely to survive changing conditions;
- **measurement confidence:** whether available sensors identify the condition reliably;
- **execution confidence:** whether the behavior remains actionable after delay and cost;
- **scope confidence:** whether the applicable markets and states are known;
- **evidence independence:** whether apparent confirmation comes from genuinely distinct samples and sources.

A single aggregate confidence label may summarize but never replace these components. High historical effect with low persistence or execution confidence does not justify approval.

### 3.4 Competing hypotheses

For every favored explanation, the Architect states at least one competing explanation and the evidence that would distinguish them. Examples include trend versus liquidity shock, accumulation versus inactive demand, breakout continuation versus stop-driven reversal, and mean reversion versus delayed structural repricing.

The Architect seeks discriminating evidence rather than accumulating only confirming evidence.

## 4. Strategy family selection

### 4.1 Selection rule

A strategy family is selected because its payoff logic matches observed behavior and failure geometry. Preference, familiarity, recent performance, or ease of measurement is not a valid reason.

The Architect asks:

1. Is expected advantage based on continuation, reversal, transition, relative location, or conditional volatility?
2. Does the opportunity exist immediately, after confirmation, or after a counter-move?
3. What market state makes the payoff asymmetric?
4. What invalidates the state before the expected outcome?
5. Does the family remain coherent after realistic delay and costs?

### 4.2 Family reasoning

**Trend following:** selected when directional persistence is the primary supported behavior and losses can be contained during non-persistent states. It is rejected when the apparent trend is event concentration, hindsight boundary selection, or insufficient after whipsaw costs.

**Momentum:** selected when recent directional information predicts continued relative strength over the chosen horizon, without requiring a long-established trend. It is rejected when continuation disappears after neutralizing volatility, liquidity, or cross-sectional structure.

**Breakout:** selected when acceptance outside a defined balance predicts continuation. The boundary must exist before the event. It is rejected when movement is primarily transient liquidity clearing or when executable entry absorbs the effect.

**Mean reversion:** selected when displacement from a defensible reference tends to correct under stable balancing conditions. It is rejected when deviation reflects new information, structural repricing, or unbounded loss geometry.

**Pullback:** selected when a persistent directional state survives temporary counter-movement and a retracement improves asymmetry. It is rejected when pullback depth is merely an early marker of reversal.

**Volatility expansion:** selected when rising dispersion or range is expected to persist or coincide with directional discovery. It is rejected when expansion is isolated, untradeable, or mean-reverting immediately after costs.

**Volatility compression:** selected when a low-activity state itself has conditional value, either through continued balance or preparation for a later move. The strategy must specify which outcome is tested. Compression alone does not imply breakout direction.

**Liquidity sweep:** selected when movement through concentrated liquidity tends to produce a distinguishable continuation or rejection response. It requires evidence about execution feasibility and cannot rely on idealized extreme prices.

**Market structure:** selected when sequences of acceptance, rejection, relative highs and lows, or location within balance contain distinct information not reducible to generic direction. Structure must be defined before outcomes are observed.

**Hybrid:** selected when two supported behaviors require different modules and their interaction adds information beyond either alone. Hybrid does not mean adding filters until performance improves.

**Adaptive:** selected when state transitions are measurable, state-specific behaviors are independently supported, and switching adds value after classification error and delay. It is rejected when adaptation is only frequent retuning.

### 4.3 Family rejection

The Architect records not only the selected family but also the nearest alternatives and why they were rejected. If several families remain equally plausible, the next step is a discriminating experiment, not arbitrary selection.

## 5. Information model

### 5.1 Information before measurement

The Architect defines what must be known before selecting how to estimate it. Measurements are interchangeable candidates with different lag, noise, scale, and failure behavior.

### 5.2 Information domains

| Information need | Question | Possible measurements |
|---|---|---|
| Direction | Is value moving persistently, and on which horizon? | displacement, ordered highs and lows, average location change, slope, directional return balance |
| Momentum | Is directional change accelerating, decelerating, or persisting? | multi-horizon returns, rate of change, directional impulse, oscillator position, change in slope |
| Volatility | How broad is the outcome distribution, and is it changing? | realized return dispersion, true range, high-low estimators, implied volatility, range compression or expansion |
| Participation | Is movement supported by broad or concentrated activity? | volume, trade count, open interest, breadth, turnover, signed flow proxies, response to activity |
| Liquidity | How costly and fragile is execution? | spread, depth, impact, order-book imbalance, gap frequency, turnover, time to fill, rejection rate |
| Efficiency | How much net displacement occurs relative to path and noise? | displacement-to-path ratio, overlap, reversal frequency, variance relationships, directional persistence |
| Risk | What adverse paths and discontinuities are plausible? | drawdown distribution, tail loss, gap behavior, adverse excursion, volatility of volatility, liquidity stress |
| Timing | When is the behavioral condition actionable? | session, event distance, bar age, state duration, confirmation sequence, time since displacement or retracement |
| Location | Where is price relative to defensible reference structure? | prior balance, range position, anchored value, swing structure, distance from accepted area |
| State stability | How likely is the current classification to persist? | duration, transition frequency, agreement among independent measurements, sensitivity to horizon |

### 5.3 Measurement selection

Measurements are compared on:

- directness relative to the information need;
- lag and responsiveness;
- noise and false-state frequency;
- stability across reasonable definitions;
- scale comparability across markets and horizons;
- sensitivity to gaps, missing observations, and outliers;
- dependence on data unavailable at decision time;
- distinct information added after existing modules.

The Architect does not ask which indicator is best in general. It asks which measurement is adequate, least redundant, and least fragile for a defined information need.

## 6. Redundancy detection

### 6.1 Why redundancy is dangerous

Redundant modules create an illusion of confirmation. If several measurements are transformations of the same price history, agreement does not represent independent evidence. Redundancy increases complexity, reduces the number of eligible observations, amplifies tuning freedom, and makes the strategy sensitive to small changes without adding a new behavioral dimension.

Two modules are redundant when removing one changes labels more than information, when their decisions fail in the same conditions, or when one can be predicted largely from the other within the relevant state.

### 6.2 Common overlaps

**EMA versus SMA:** both estimate central tendency and direction from recent prices. Different weighting changes lag but usually does not create an independent information domain. Using both as separate confirmation requires proof of incremental state discrimination.

**MACD versus moving-average slope:** both often express direction and change in moving-average separation. Agreement can be one transformation confirming itself.

**ATR versus Bollinger width:** both may estimate realized dispersion. Bollinger width also depends on location relative to a central estimate, but as volatility filters the two often overlap substantially.

**RSI versus Stochastic:** both locate recent movement within a bounded momentum or range context. Their formulas differ, but they commonly identify the same stretched or reverting conditions.

**ADX versus trend persistence:** both may describe directional organization. ADX is a derived range-and-direction measure; direct persistence or efficiency may already contain much of the same information.

### 6.3 Redundancy tests in reasoning

Before retaining two modules, the Architect asks:

1. Which distinct question does each answer?
2. Do they depend on different underlying observations?
3. Do they fail in different market states?
4. Does one add conditional information after the other is known?
5. Does agreement improve outcomes outside the motivating sample?
6. Can the same behavior be expressed with one clearer measurement?

### 6.4 Resolution

When overlap is material, the Architect may remove one measurement, combine them into one information estimate, assign them as alternative experiment arms, or use one only to challenge the other. Redundant agreement is never counted as multiple independent confirmations.

## 7. Strategy architecture

### 7.1 Modular reasoning

Every strategy is decomposed into modules. Each module answers one question, has a hypothesis, and can be removed or replaced independently.

### 7.2 Required modules

**Market regime:** Under which broad conditions may the edge exist? This module includes eligibility and exclusion, not entry timing.

**Trend or directional context:** What directional or structural bias, if any, defines the favorable side? A strategy may explicitly declare no directional context.

**Entry:** What observable event converts eligibility into action? Entry must be causal and available at the decision time.

**Confirmation:** What distinct evidence reduces a known false-entry mode? Confirmation is optional. If it adds no independent information, it is removed.

**Risk:** What path, state change, or loss invalidates continued exposure? Risk is defined from hypothesis failure and adverse distribution, not merely convenience.

**Exit:** What evidence indicates the expected behavior has completed, failed, or become less favorable than the alternative use of risk?

**Trade management:** How should exposure respond as evidence evolves after entry? Management must not silently change the original hypothesis or create unlimited discretion.

**Validation:** Which tests determine whether each module and the complete architecture add credible value?

**Monitoring:** Which live observations indicate normal behavior, weakening, structural failure, or measurement failure?

### 7.3 Module contract

For every module the Architect records:

- the information question;
- the behavioral rationale;
- the evidence used;
- the expected contribution;
- overlap with other modules;
- known failure conditions;
- alternative formulations;
- removal test;
- monitoring signal.

### 7.4 Architecture discipline

Eligibility, entry, confirmation, risk, and exit must not be disguised duplicates of one measurement. The architecture must remain intelligible when individual measurement names are removed. If the strategy cannot be explained in behavioral terms without indicator labels, it is not ready for implementation.

## 8. Failure thinking

### 8.1 Failure is designed into the analysis

The Architect searches for ways the hypothesis, measurement, architecture, or action can fail before seeking additional confirmation. Failure analysis is not a final checklist; it influences hypothesis scope and experiment design from the beginning.

### 8.2 Failure domains

**Hypothesis failure:** the proposed conditional behavior does not exist, has the wrong direction, or lacks a plausible persistence mechanism.

**Overfitting:** apparent success depends on excessive alternatives, isolated definitions, favorable boundaries, repeated selection, or a small number of influential observations.

**Regime dependency:** the edge exists only in a narrow state that is rare, difficult to identify in real time, or likely to change after selection.

**Sample bias:** results depend on survivorship, venue choice, symbol availability, missing periods, event concentration, one market cycle, or unrepresentative history.

**Measurement failure:** sensors are delayed, unstable, redundant, contaminated, or incapable of distinguishing competing states.

**Execution risk:** the effect disappears after decision delay, spread, slippage, gaps, partial fills, funding, or inability to transact at observed prices.

**Liquidity risk:** position size changes the opportunity, liquidity disappears when needed, or exits share crowded pathways with other participants.

**Volatility shift:** risk and payoff assumptions fail when dispersion, correlation, gaps, or volatility of volatility change.

**Structural break:** regulation, venue mechanics, participant composition, product design, information speed, or macro structure changes the generating process.

**Interaction failure:** individually sensible modules combine to reduce sample quality, create contradictory responses, or concentrate losses.

**Monitoring failure:** degradation cannot be distinguished from normal variation before unacceptable loss or opportunity cost occurs.

### 8.3 Pre-mortem

Before advancement, the Architect assumes the strategy failed materially and writes the most plausible explanations. Each explanation becomes a test, monitoring requirement, scope restriction, or explicit residual risk.

## 9. Experiment design

### 9.1 Experiments precede implementation commitment

The Architect creates a family of experiments before one architecture becomes the favored candidate. Experiments test claims and alternatives; they do not exist to search indefinitely for a profitable combination.

### 9.2 Experiment hierarchy

1. **Existence experiment:** does the conditional behavior differ from the baseline before strategy detail?
2. **Mechanism experiment:** do outcomes vary as the proposed explanation predicts?
3. **Measurement experiment:** can the state be identified without using future information?
4. **Architecture experiment:** do the selected modules convert the behavior into favorable actionable asymmetry?
5. **Increment experiment:** what does each additional module contribute?
6. **Robustness experiment:** does the conclusion survive alternative samples, definitions, costs, and disturbances?
7. **Monitoring experiment:** which observations reveal weakening with acceptable false alarms?

### 9.3 Required alternatives

**Alternative measurements:** compare different sensors for the same information need. Agreement supports the behavior; divergence reveals measurement dependence.

**Alternative exits:** compare hypothesis invalidation, time-based completion, structural completion, and favorable-movement management. Exit choice must reflect behavior rather than rescue entry quality.

**Alternative filters:** test whether each eligibility condition adds distinct information or merely reduces the sample until it looks favorable.

**Alternative position sizing:** compare whether the edge survives materially different exposure logic and whether favorable results depend on implicit leverage concentration.

**Alternative timeframes:** evaluate whether the behavior is horizon-specific, scale-consistent, or an artifact of aggregation.

**Alternative market regimes:** test expected eligible and ineligible states. A useful regime filter should separate behavior in the direction predicted before results are observed.

**Alternative markets and periods:** examine portability where the mechanism suggests it and deliberate non-portability where market structure differs.

### 9.4 Controls

Experiments include relevant baselines, simplified architectures, module removals, randomized or time-shifted relationships, and destroyed temporal structure. A candidate must outperform explanations based on chance, general market drift, volatility exposure, or sample selection.

### 9.5 Stopping logic

Research stops or resets when the core behavior fails, the effect is smaller than realistic friction, the required state cannot be identified reliably, complexity grows without independent information, adverse evidence dominates, or further search would primarily increase selection freedom.

## 10. Self-critique

### 10.1 Mandatory challenge

Before recommending a strategy for independent validation, the Architect answers the following in writing.

#### Why might this fail?

Identify the strongest behavioral, statistical, execution, liquidity, and structural reasons. State which failure could occur without advance warning.

#### What assumptions remain untested?

List assumptions about data, participant behavior, state persistence, timing, costs, fills, liquidity, scale, and transferability. Explain why each remains unresolved and how it limits confidence.

#### Which module contributes the least information?

Identify the weakest incremental module using reasoning and ablation evidence. If it cannot justify its complexity, remove it before advancement.

#### Can two modules be merged?

Examine whether multiple modules answer the same information question or fail under the same conditions. Prefer one transparent estimate to duplicated confirmation.

#### Is complexity justified?

Compare the complete architecture with the simplest behavioral expression. Complexity is justified only by stable, distinct, out-of-sample information or necessary risk control.

### 10.2 Additional questions

- What observation would most strongly change the recommendation?
- Which result is dominated by a small number of events?
- Which conclusion depends most on the chosen sample boundary?
- What is the nearest competing hypothesis?
- What evidence contradicts the preferred explanation?
- Is the proposed opportunity large enough after realistic friction?
- Can the state be recognized at the time of decision rather than in hindsight?
- Does the exit express hypothesis failure or compensate for a weak entry?
- Would the strategy still make sense if every indicator name were removed?
- What knowledge would be lost if this candidate were rejected today?

### 10.3 Recommendation states

The Architect concludes with one of four recommendations:

- **REJECT:** the behavioral claim, persistence, measurement, or actionability is not sufficiently supported.
- **REVISE:** the hypothesis remains plausible, but scope, architecture, evidence, or assumptions require new work.
- **EXPERIMENT:** the claim is sufficiently defined for controlled testing but not for implementation commitment.
- **VALIDATION CANDIDATE:** the behavior, architecture, alternatives, and failure analysis are complete enough for independent validation.

The Architect does not approve production. A `VALIDATION CANDIDATE` means only that the reasoning is explicit enough to be challenged independently.

## 11. Required reasoning output

Every completed use of the Quant Intelligence Engine produces a reasoning record containing:

1. market and horizon definition;
2. state classification with uncertainty and alternatives;
3. observation and hypothesis anatomy;
4. persistence mechanism and competing explanations;
5. information needs before measurement selection;
6. chosen strategy family and rejected alternatives;
7. modular strategy architecture;
8. redundancy assessment;
9. failure pre-mortem;
10. experiment family and stopping conditions;
11. unresolved assumptions;
12. confidence dimensions;
13. recommendation and evidence required for the next state.

This record is the bridge between intelligence and subsequent work. It preserves why the strategy was conceived, not only what rules were eventually tested.

