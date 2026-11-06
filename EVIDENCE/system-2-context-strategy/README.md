# System 2: Long-Conversation Context Strategy

**Exercise:** Engineer a Long-Conversation Context Strategy for a Retail Support Copilot
**Module:** 04-assemble-and-locate (Solution)
**Date:** November 6, 2026

## Overview

The Context Strategy compresses long-running customer support conversations into concise assembled context, reducing token consumption while preserving question-answering quality. This evidence captures one complete context compression and evaluation run.

## Key Artifacts

### 1. **CONTEXT_STRATEGY_EXECUTION_REPORT.md**
- Full analysis of context compression strategy
- Token metrics: 56.69% reduction (38,708 → 16,765 tokens)
- Evaluation methodology and results
- Detailed breakdown of compression by case segment

### 2. **test_log.txt**
- System 2 pytest evidence: 30/30 tests passing
- Complete test suite validation
- Confirms all context assembly logic and evaluation framework

### 3. **budget.json** (509 bytes)
- Token reduction metrics:
  - Baseline: 38,708 tokens
  - Assembled: 16,765 tokens
  - Savings: 21,943 tokens
  - Reduction Rate: 56.69%
- Per-segment compression ratios:
  - Refund case: 97.2% reduction
  - Subscription case: 96.4% reduction

### 4. **eval.jsonl** (3.4 KB)
- 6 evaluation questions with **full context** answers
- All 6 questions passing (100%)
- Demonstrates quality preservation with compressed context:
  - Q1: Basic customer info (identity preservation)
  - Q2: Recent escalations (priority understanding)
  - Q3: Refund eligibility (complex rule application)
  - Q4: Subscription timeline (chronological reasoning)
  - Q5: Interaction patterns (behavioral analysis)
  - Q6: Case resolution path (complex reasoning chain)

### 5. **eval_control.jsonl** (1.5 KB)
- Control group: **without assembled context**
- Q1: PASS (basic facts available without compression)
- Q6: FAIL (requires compressed case facts)
- **Expected regression:** Demonstrates necessity of context assembly

## Key Findings

### Compression Success
- **56.69% token reduction** (exceeds 50% target)
- **100% evaluation pass rate** (full context)
- **Expected control failure:** Q6 regression identifies crucial context segments

### Evaluation Methodology
1. **Full Context (eval.jsonl):**
   - All 6 questions answerable
   - Compression preserves critical information
   - Pass rate: 6/6 (100%)

2. **Control (eval_control.jsonl):**
   - No assembled context provided
   - Basic questions pass (Q1)
   - Complex reasoning fails (Q6)
   - Pass rate: 1/6 (expected)

### Architecture Highlights

#### Case Fact Extraction
The system identifies and preserves:
- Customer identity and account status
- Refund eligibility rules and dates
- Subscription timeline and changes
- Escalation history and severity
- Previous interaction context

#### Compression Strategy
1. **Active Cases:** Full context (not compressed)
2. **Resolved Cases:** Extract facts only
   - Customer identity
   - Refund amounts/dates
   - Subscription changes
   - Escalation flags
3. **Historical Cases:** Hash-based references
   - Reduces verbosity
   - Preserves enough for contextual reasoning

#### Assembly Process
```
Long conversation
    ↓
Segment by case
    ↓
Extract facts (resolved) / compress (historical)
    ↓
Interleave with active context
    ↓
Assembled context (56.69% smaller)
```

## Reproducibility

The context strategy is **deterministic and measurable:**
- ✅ Exact token count via budget.json
- ✅ Question-level pass/fail via eval.jsonl
- ✅ Expected control regression documented
- ✅ Per-segment compression transparent

## Notes

- **Baseline:** Full conversation (38,708 tokens)
- **Assembled:** Curated context (16,765 tokens)
- **Savings:** 21,943 tokens (56.69%)
- **Quality:** 100% pass rate on evaluation questions

## File Structure

```
system-2-context-strategy/
├── README.md (this file)
├── CONTEXT_STRATEGY_EXECUTION_REPORT.md
├── test_log.txt (30/30 pytest passing)
├── budget.json (56.69% reduction)
├── eval.jsonl (6/6 passing)
└── eval_control.jsonl (1/6 expected)
```

## Strategic Value

This system demonstrates how to:
1. **Reduce token costs** for long-running copilot conversations
2. **Maintain reasoning quality** via intelligent context assembly
3. **Measure compression impact** through evaluation
4. **Handle mixed contexts** (active + resolved + historical)
5. **Guide model focus** with extracted facts

### Example Compression
- **Full:** "Customer opened ticket Tuesday about refund. Then Wednesday mentioned subscription issue. Thursday escalated to supervisor. Friday supervisor resolved subscription, but refund still pending..."
- **Assembled:** "Identity: acct-123; Refund: $45 pending since Tue; Subscription: changed Wed, resolved Fri; Escalation: supervisor, resolved"
- **Savings:** ~85% token reduction while preserving all question-answerable facts
