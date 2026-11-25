# Research and engineering roadmap

## 1. Source verification (highest priority)

Audit Douglas and Cobb–Douglas transcriptions against primary pages; record exact bibliographic metadata, licenses, units, revisions and transforms. Separate data that cannot lawfully be redistributed into an opt-in local-data workflow. Add immutable source-version identifiers and a published errata log.

## 2. Better econometric diagnostics

Add unit-root, cointegration and structural-break diagnostics, sample-split sensitivity, residual autocorrelation tests, uncertainty bands and appropriately justified robust inference. Publish synthetic and historically verified fixtures for each method. Expand reporting before making causal or predictive claims.

## 3. Modern public-data adapters

Design versioned, explicit BEA/FRED/BLS/World Bank adapters with source IDs, request caching, rate limits, provenance and raw snapshot retention. Do not regenerate vanished historical sources from differently defined modern series without an explicit comparison.

## 4. Research workflows

Configuration-driven recipes with peer-reviewed output artifacts and saved citations; optional notebooks using the same library methods; data dictionary browsing with semantic series metadata.

## 5. Release readiness

Third-party license review; public release policy; documentation site; signed tags; package distribution only after source rights and supported-platform validation. Consider stronger typing, benchmark checks, dependency scanning, and reproducible deployment builds.
