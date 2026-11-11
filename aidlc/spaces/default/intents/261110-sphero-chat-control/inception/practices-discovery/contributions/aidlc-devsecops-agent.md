**Collaborator:** aidlc-devsecops-agent

## Contribution

### Secret management
The project uses `.env` for the OpenRouter API key. `.env` must never be committed to version control: add `.env` (and `.env.*` overrides) to `.gitignore` immediately, serve secrets from CI-protected environment variables or a secrets manager in non-local environments, and run secret detection (gitleaks/trufflehog or equivalent) as a pre-commit check and CI scan so any accidentally committed key fails the pipeline. If any key has already been committed, rotate it and purge it from history.

### Dependency scanning
Integrate dependency vulnerability scanning into CI (npm audit/Snyk/equivalent for the chosen language) so new and transitive vulnerabilities fail the build above an agreed severity threshold. Scan on every pull request and on a recurring schedule for newly disclosed CVEs in already-deployed dependencies.

### SAST/DAST
Add SAST (CodeGuru Security, SonarQube, or language-equivalent) to the CI pipeline as a blocking security gate, and schedule DAST against deployed staging endpoints before production promotion. Security findings must block merge at agreed severity, not merely advise.

### Lint/format rules
Keep the lead's proposal of a project-configured formatter and linter blocking CI, but extend the linter with security rules (e.g., ESLint security plugin, Ruff bandit rules for Python, or language-equivalent) so insecure patterns (eval, shell injection, disabled authentication) are caught at lint time rather than in review.

### Supply-chain controls
Pin direct dependencies in a lockfile committed to the repo, vet third-party packages before adoption (maintenance, license, vulnerability history), generate an SBOM for each release artifact, and verify artifact integrity/signature where the toolchain supports it. Treat the dependency graph as part of the trusted computing base.

## Positions

AGREE: Deploy on merge to staging with production gated by manual approval — matches org.md deployment guidance and keeps production changes under human review.
AGREE: Linter run in CI before merge with failure blocking the PR — gives security gates a natural enforcement point in the pipeline.
AGREE: Trunk-based development on `main` with squash-merged Bolt branches — short-lived branches reduce the window for exposed secrets and divergent, unreviewed code.
OBJECT: Code Style section covers formatter/linter but omits SAST, dependency scanning, and secret detection — without these, CI has no automated security gate and vulnerabilities reach merge undetected.
OBJECT: No rule that `.env` must never be committed — the project uses `.env` for the OpenRouter API key, so a hard secret-management rule (gitignore `.env`, pre-commit secret scanning, key rotation if leaked) is required.
OBJECT: No supply-chain controls are stated — third-party dependencies are an unmanaged attack surface; dependency pinning/locking, pre-adoption vetting, and SBOM generation should be added.
