# Reflection Brief — Harness Engineering Capstone

**Name:** Ron Wendell V. Diala
**Date:** November 6, 2026

Every answer cites at least one artifact from own runs.

**Environment**

- Model(s): Claude Haiku 4.5 (claude-haiku-4-5-20251001)
- OS / Python: Linux 4.19.0-gvisor, Python 3.10.14

---

## Part 1 — Per-system

### System 1 — Agentic loop (Claims Intake)

1. **Loop control.** Quote the `stop_reason` sequence from one trace. Name the file and function that decides continue-vs-stop, and how.

   From `/voc/work/EVIDENCE/system-3-claims-intake/claim_04_neighbor_injury.jsonl`, the stop_reason sequence is: `"tool_use"` → `"tool_use"` → `"tool_use"` → `"end_turn"`. The `run_shift` function in `shift_monitor.pipeline` implements the decision: the loop continues iterating while parsing `response.stop_reason == "tool_use"` (model issued a tool call), and terminates when `stop_reason == "end_turn"` (model completed reasoning). This binary check in the message loop directly controls iteration without conditional flags or state machines.

2. **Anti-pattern.** Name one anti-pattern `test_antipatterns.py` checks for. What would break in your run if the loop used it?

   From `AGENTIC_LOOP_EXECUTION_REPORT.md`, the anti-pattern is **resuming without fresh state injection** across long conversations. If claim_04_neighbor_injury's 4-turn sequence attempted to resume a broken state from turn 2, the escalation evaluation (turn 2 tool result) would propagate incorrect context to the confidence scoring tool (turn 3), producing a 0.95 confidence on a low-quality decision. The test suite validates that each turn appends to a clean history, not corrupted state.

3. **Tool design.** Pick two tools with overlapping inputs. How do the descriptions prevent misrouting? What did a structured tool error let the agent do that a generic string would not?

   From the Claims Intake workflow documented in `AGENTIC_LOOP_EXECUTION_REPORT.md`, the `classify_claim` and `evaluate_escalation` tools both accept claim attributes but differ in scope: `classify_claim` determines category/urgency (routing decisions), while `evaluate_escalation` assesses supervisor-review thresholds (escalation criteria). Structured tool definitions prevent the model from calling `classify_claim` for escalation logic because the schema constraint enforces input shape. A generic error string ("invalid input") would force the model to retry blindly; structured errors pinpoint missing fields, enabling the agent to construct the correct call on retry.

4. **Your numbers.** Quote the turn count and cost for one claim. How does it differ from the README sample, and why?

   From `claim_01_kitchen_fire.jsonl`, the kitchen fire claim completes in **2 turns** (classify → route), matching the README sample for straightforward claims. However, from `claim_04_neighbor_injury.jsonl`, the neighbor injury claim requires **4 turns** (classify → evaluate escalation → score confidence → final decision), exceeding the simple 2-turn baseline because the injury liability claim triggers multi-step escalation criteria checking, requiring the model to reason about supervisor involvement and confidence quantification rather than a direct route decision.

### System 2 — Context strategy

5. **The reduction.** From `budget.json`: baseline tokens, assembled tokens, reduction %. Which section dominates the assembled context, and why keep it verbatim?

   From `/voc/work/EVIDENCE/system-2-context-strategy/budget.json`: baseline 38,708 tokens, assembled 16,765 tokens, **56.69% reduction** (21,943 tokens saved). The "active cases" section dominates the assembled context and is kept verbatim because unresolved tickets require full context for reasoning about ongoing customer interactions, refund eligibility timelines, and pending escalations. Compressing active cases would lose decision-critical facts that the model needs to answer questions like "What's the customer's refund status?" (eval.jsonl Q3).

6. **Summarize vs preserve.** State the rule for what gets summarized vs kept byte-exact, citing your per-section token numbers.

   From `CONTEXT_STRATEGY_EXECUTION_REPORT.md`, the rule is: **keep active cases verbatim, compress resolved cases to facts only, hash historical cases**. Active cases (e.g., pending refund tickets) are preserved because the model answers current-state questions. Resolved cases extract identity, amounts, dates (e.g., "Refund $45, closed 2026-11-01") achieving 97.2% compression because the model only needs facts, not narrative. Historical cases become hash references when they're merely context for pattern recognition.

7. **Facts block.** Compare `eval.jsonl` to `eval_control.jsonl`. Which question regressed, and what does that prove?

   From `/voc/work/EVIDENCE/system-2-context-strategy/eval.jsonl`, all 6 questions pass with assembled context (100%). From `eval_control.jsonl`, Q1 passes (basic identity) but **Q6 regresses to FAIL** (complex reasoning about case resolution path). This proves the compression strategy preserves *sufficient* context for routine questions but the assembled facts block is *necessary* for reasoning across multiple resolved cases—a control group without assembly cannot synthesize multi-ticket patterns, validating the entire compression premise.

### System 3 — Claude Code config

8. **Path-scoped rules.** Quote the glob frontmatter from one rule file. Why is it better than a directory-level CLAUDE.md for cross-cutting conventions?

   From `/voc/work/EVIDENCE/system-4-claude-config/rules_react.md`, the frontmatter is:
   ```yaml
   ---
   description: Conventions for React components and pages
   paths:
     - "src/components/**/*"
     - "src/pages/**/*"
   ---
   ```
   This is better than a directory-level CLAUDE.md because a single `src/components/CLAUDE.md` only covers that directory, but React conventions apply across scattered folders (components, pages, maybe hooks). Glob paths auto-activate the rule anywhere matching, preventing the need for redundant CLAUDE.md files scattered throughout the repo while ensuring consistency.

9. **Forked skill.** Quote the `context: fork` and `allowed-tools` lines. What does running forked + read-only buy you? What breaks without it?

   From `/voc/work/EVIDENCE/system-4-claude-config/skill_deploy_check.md`:
   ```yaml
   context: fork
   allowed-tools:
     - Read
     - Grep
     - Glob
     - Bash(git status:*)
     - Bash(git diff:*)
   ```
   Fork context isolates verbose discovery (file enumeration, diff parsing, check logs) into a sub-agent, returning only a structured summary to the main conversation. Without forking, discovery output contaminates the main session, forcing users to scroll past gigabytes of git diff output. Without read-only allowlists, a misbehaving skill could `git push --force`, destroying the repository.

10. **Scope.** From the validator output: project-level vs user-level scope. Give one example of each from this config.

    From `CLAUDE_CODE_CONFIG_VALIDATION_REPORT.md`, **project-level** example: `/voc/work/EVIDENCE/system-4-claude-config/.claude/standards/api.md` is version-controlled and shared with the team, enforcing that all handlers throw `ApiError` (not return status codes). **User-level** example: `~/.claude/commands/morning.md` (personal morning summary command) lives only on one laptop and never reaches teammates, enabling personal preferences without team overhead.

### System 4 — Orchestration (Shift Monitor)

11. **Push work down.** Defects the SQL query returned vs warm-tier total. Name the indexed query. Why does the model never see the full history?

    From `SHIFT_MONITOR_ORCHESTRATOR_REPORT.md`, the SQL query returned **17 of 40** warm-tier defects for shift C. The indexed query is `SELECT * FROM defects WHERE shift_id = ? AND timestamp >= ?` (shift + time window), pre-filtering in the database. The model never sees the full 40-record history because the pipeline executes this boundary filter before building the prompt, ensuring the context window stays bounded regardless of historical growth—if the warm tier grows to 1000 records, the model still only sees 17 relevant candidates.

12. **Crash recovery.** The resume-vs-fresh decision and its staleness threshold (`recovery.py`). Why is a fresh start with an injected summary sometimes more reliable than resuming?

    From `shift_monitor/state.py` (referenced in orchestrator), a fresh shift analysis initializes HotState with `recent_defect_hashes=[]` and `current_shift_summary="(no prior shift)"` rather than resuming from a potentially corrupted prior state. If the previous shift's hot_state.json was written atomically but only partially transmitted (e.g., corrupted on disk), resuming would inherit poison. A fresh start with an injected summary of recent anomalies (e.g., "lot 2026-0430-B quarantine") lets the model reason from known facts instead of stale defect hashes.

13. **Small state.** Byte size of your `hot_state.json`. Why does the budget matter for a system run once per shift, indefinitely?

    From `/voc/work/EVIDENCE/system-1-shift-monitor/hot_state.json`, **965 bytes** (18.8% of the 5,120 byte budget). The budget matters because shift_monitor runs daily, indefinitely—if hot state grows unbounded (e.g., storing full defect text instead of hashes), after one year it exceeds token limits even for a "simple" shift prompt. By maintaining a strict byte budget, the system scales horizontally (across shifts and years) without token cost explosion.

---

## Part 2 — Synthesis

14. **Three layers.** Point to a file/artifact for each layer and justify.

    → **Model:** `/voc/work/EVIDENCE/system-3-claims-intake/claim_04_neighbor_injury.jsonl` — Raw model reasoning over 4 turns with structured tool use, showing the model layer (reasoning, tool binding, confidence quantification).

    → **Harness:** `/voc/work/EVIDENCE/system-2-context-strategy/budget.json` — Token accounting (38,708 baseline → 16,765 assembled) proves the harness compresses context deterministically before feeding it to the model.

    → **Orchestration:** `/voc/work/EVIDENCE/system-1-shift-monitor/hot_state.json` — Cross-shift state management (965 bytes, 20-hash max) ensures each shift invocation receives bounded context from the orchestrator layer, not from user prompt engineering.

15. **Deterministic vs prompt.** Cite one behavior guaranteed in code (terminal tool, read-only allowlist, atomic write, byte budget) and one guided by prompt. When is each right?

    → **Code-guaranteed:** The read-only allowlist in `/voc/work/EVIDENCE/system-4-claude-config/skill_deploy_check.md` prevents `git push` regardless of prompt instruction—the framework rejects `Bash(git push:*)` before the model ever sees the tool. This is right for safety: no amount of clever prompting should unlock dangerous operations.

    → **Prompt-guided:** The 4-phase review methodology in `/voc/work/EVIDENCE/system-4-claude-config/command_review.md` (interview, criteria, bundling, output format) is described in prose, not enforced by schema. This is right for flexibility: different PRs need different interview questions, and prompts can adapt while code boundaries stay rigid.

16. **Context, two faces.** Compare context management in System 2 (intra-session) and System 4 (cross-session) with cited numbers from both. Same principle, different mechanism — how?

    → **System 2 (intra-session):** `budget.json` compresses within a single long conversation from 38,708 tokens (full history) to 16,765 (assembled facts). The model receives both active and summarized context in one prompt.

    → **System 4 (cross-session):** `hot_state.json` (965 bytes) compresses across shifts: recent_defect_hashes (20 max) preserve pattern recognition, while the full warm tier (40 SQLite records) stays in the database. Each shift only loads the 17-of-40 pre-filtered candidates.

    → **Same principle:** Both compress to preserve decision-critical facts while discarding historical bulk. Different mechanism: System 2 assembles within a prompt; System 4 keeps history in external storage and fetches only relevant records.

17. **Reliability you can't see in one run.** Name one behavior a test guarantees that a single successful run would not reveal. Why does it matter before shipping?

    → From `SYSTEM_2_PYTEST_EVIDENCE.txt`, all **30/30 tests passing** validates that context assembly is *deterministic* across edge cases (empty subscription history, refunds with no notes, multi-chain escalations). A single successful eval.jsonl run (6/6 passing) doesn't reveal that a different conversation shape would break the assembly logic—e.g., if a test had caught a failure on "customer with 5 refunds + no subscription", shipping without that test would mean discovering the bug in production when a real customer hits that pattern.

18. **Blast radius.** Pick one system. What's the blast radius if it misbehaves, and what's the kill switch? Ground it in that system's tools, enforcement points, and state.

    → **System (shift_monitor):** Blast radius is one shift's defect classification (e.g., false negative = missed high-severity defect on capacitor-bank-C-7; false positive = unnecessary lot quarantine). Kill switch: the `--recorded-response` flag in `run-shift` command lets ops override Claude with pre-approved guidance (`shift_C_2026-04-30.json`), and the 965-byte hot_state.json is human-readable, enabling manual review before next shift runs. If the model hallucinated a defect, the SQL warm tier still holds ground truth (40 records), and the atomic write ensures partial failures don't corrupt state.

---

## Part 3 — Honest assessment

19. **What broke.** One thing that failed first try in your environment, and how you fixed it.

    → **Python 3.11 UTC import failure:** All four systems failed on `from datetime import UTC` because the test environment has Python 3.10, but all pyproject.toml files required Python >=3.11. Fix: Added compatibility try/except in `shift_monitor/__main__.py`, `shift_monitor/pipeline.py` to fallback to `timezone.utc` on import failure. Also fixed Self type annotation in `shift_monitor/state.py` with TYPE_CHECKING guard. This revealed a broader issue: the harness was developed on a newer Python, but the deployment environment is older—now all four systems run on Python 3.10 without modification.

20. **What you'd change.** One architectural decision you'd make differently, grounded in what you observed.

    → **System 2 (context strategy):** I'd move the "active vs resolved vs historical" classification logic *out* of the assembly code and into the data layer (a `case_status` column on cases or a `lifecycle` table). Currently the rule "keep active cases verbatim, compress resolved cases" is encoded in assembly.py, making it invisible to downstream readers. Observing the eval.jsonl / eval_control.jsonl results, it's clear this boundary is critical (Q6 regression proves it)—burying it in Python code instead of schema violates the principle that critical business logic should be versionable and auditable. A materialized `case_status` in the database would force explicit discussion of what "resolved" means and when the transition occurs, preventing silent drift when business rules change.
