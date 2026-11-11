**Collaborator:** aidlc-developer-agent

## Contribution

### Code Style
- Defer formatter and linter to project-level configuration (Prettier for JS/TS, Black for Python, gofmt for Go; ESLint/Ruff/golangci-lint) configured in repo root, with CI blocking merge on lint failure — as proposed in the lead draft.
- Add type-safety rules: no implicit `any`/untyped parameters, explicit return types on public functions, `const` by default (reassign only when needed).
- Require docstrings/JSDoc on all public APIs and exported types; inline comments reserved for non-obvious logic only.
- Enforce import ordering (stdlib, third-party, relative) and consistent quote style per formatter config; max line length 100 unless the project config differs.
- The agent's code-style suggestion fires only when the project linter doesn't already cover it (per org.md).

### Naming Conventions
- Variables and functions: camelCase (JS/TS), snake_case (Python).
- Classes, types, interfaces, components: PascalCase.
- Constants and enum members: SCREAMING_SNAKE_CASE.
- Files: kebab-case (JS/TS), snake_case (Python); one module per file, filename matches the exported symbol.
- No project-wide rename rules unless the team affirms one.

### Layer Boundaries
- Define four layers: API/presentation (controllers/routes), service/application (use cases), domain (entities/value objects), data access/infrastructure (repositories, external clients).
- Dependencies flow inward only: API → service → domain; data access implements domain-defined repository interfaces. No layer skips another; domain knows nothing of outer layers.
- Each layer owns its own DTOs/models; map at boundaries (never leak domain entities to API responses, and never let external schemas into the domain).

### Error Handling
- Fail fast, fail loud: validate all inputs at system boundaries (API requests, file I/O, DB calls, external service responses); throw or return errors immediately, never swallow silently.
- Distinguish recoverable errors (retry/fallback/circuit-break) from fatal errors (fail fast); log context with the error at the catch site.
- Standardize error types per layer (domain errors vs infrastructure errors) and map them at boundaries so callers receive meaningful, actionable errors.
- No exceptions across service-layer boundaries without a declared contract; prefer `Result<T, E>` or explicit error returns where the language supports it.

### File Organization
- Organize by feature/domain directory, not by technical type (avoid top-level `controllers/`, `models/`, `services/` buckets that scatter related code).
- Colocate tests with the module under test (e.g., `*.test.ts` / `*_test.py` next to the source).
- Barrel/index files only for the public surface of a domain folder; avoid deep re-export chains.
- Separate source from configuration and scripts (`src/` or app root, `config/`, `scripts/`; shared fixtures only under `tests/`).

## Positions

AGREE: Trunk-based development on `main` with Bolt/feature branches squash-merged — matches org.md default and keeps a linear history mapping to delivery-planning's Bolt sequence.
AGREE: Test-after methodology with implement-then-test ordering — a pragmatic default for a greenfield intent; scope floors (80% coverage, CI before merge) are additive per org.md.
AGREE: Deploy on merge to staging with manual production approval (tech lead + product owner) — standard, safe gating; continuous deployment to production remains a team decision.
AGREE: Defer formatter/linter/naming to project-level config with CI blocking — avoids bikeshedding and follows org.md code-style guidance.
OBJECT: No layer-boundary convention declared — greenfield code needs explicit layers (API/service/domain/data) with inward-only dependencies to prevent concern entanglement.
OBJECT: No error-handling convention declared — integration boundaries require standardized fail-fast/no-silent-swallowing handling or production incidents become hard to debug.
OBJECT: No file-organization convention declared — feature/domain-based organization with colocated tests aids discoverability; type-based buckets scatter related code.
OBJECT: Naming covers only variables and functions — missing conventions for constants, classes/types, files, and imports leave style decisions ad hoc.
