# Research Decisions

Research performed during speckit-plan, with a research agent as requested by that skill.

- Decision: Python `casefold()` and literal substring membership, trimming search whitespace.
  Rationale: handles Unicode such as Straße/STRASSE and treats `%`/`_` as literal characters.
  Alternatives: SQLite LIKE is ASCII-limited by default and adds wildcard semantics; FTS is unnecessary.
- Decision: bound SQL status predicate, followed by title filtering in ascending ID order.
  Rationale: no interpolation and no migration. At 10,000 rows a linear scan is appropriate.
  Alternative: new indexes/search services add needless complexity.
- Decision: argparse choices and backwards-compatible defaults (`search=''`, `status='all'`).
  Rationale: invalid choices fail before opening the DB; old commands and JSON shape remain valid.
- Decision: unittest with temporary SQLite files and real CLI subprocesses.
  Rationale: zero dependencies; verifies persistence, exit codes, literal inputs and integration.

All technical questions resolved; no deferred research items.
