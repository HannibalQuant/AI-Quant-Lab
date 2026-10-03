# PB0 engine support v1

Implements the frozen pullback_design_v1.json on main baseline `0d12e22de50e2b67559f848eaa68a2c93b5f2cfe`.

New StrategyModel MULTI_SIGNAL_PULLBACK_LONG_SHORT uses the existing version2 strategy schema with a distinct exact replay engine `multi-signal-pullback-long-short-backtest-engine-v1`. Existing trend engine IDs, strategy contracts, zero/warmup behavior and SOL evidence are unchanged. Old engine authorization cannot authorize PB0.

Only flat-position entry direction changes. Exactly previous bar touches/closes across its EMA20, current confirmed T0 direction reclaims EMA20 and breaks previous extreme. Both bars are post-warmup; first eligible signal index N+1. No setup state, search or new parameter. Open-position risk and opposite T0 direction exit remain unchanged; next eligible open and terminal fail-closed preserved.

Independent accounting additionally checks every opening order against exact PB0 entry predicates and availability/warmup bar refs. Codec roundtrip and governed authorization/replay tests cover the new identity. Synthetic comparison boundary tests cover both sides; a synthetic filled entry and opposite trend exit prove that exits do not require opposite PB0 entry. Tampered setup and old-engine refs fail closed. Existing multi-signal risk/warmup tests run unchanged.

Pine generation and optimization do not support this new model and remain fail-closed. No execution connectivity. This implementation alone grants no BTC experiment authorization: freeze exact strategy/specification/policy and pass existing authorization before the three preregistered runs.
