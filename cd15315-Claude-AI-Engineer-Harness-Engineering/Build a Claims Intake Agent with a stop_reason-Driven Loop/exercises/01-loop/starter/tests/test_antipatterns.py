"""Anti-pattern audit.

Verifies, by static AST analysis, that the agentic loop does NOT:
- use string-membership tests against text content to drive control flow
- use an integer-literal iteration cap as its primary stopping mechanism
- omit reference to `stop_reason` as the loop-breaking signal

And that the package broadly does not branch on `claim_type` equality
outside of the tool-schema definitions and the cost-estimate module.

Each test parses the relevant file with `ast` and walks the tree. There are
no runtime imports of claims_intake here — the audit is static, so it works
even if loop.py / tools.py do not run end-to-end.
"""

from __future__ import annotations

import ast
from pathlib import Path

PKG = Path(__file__).resolve().parents[1] / "claims_intake"
LOOP_PY = PKG / "loop.py"


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


# ---------------------------------------------------------------------------
# Anti-pattern 1 — no string-membership tests against assistant text in the loop
# ---------------------------------------------------------------------------
def test_no_string_membership_against_text_in_loop() -> None:
    """No `"some_token" in <something>` expressions in loop.py.

    Heuristic: any `ast.Compare` node using `ast.In` whose `left` operand is a
    string `ast.Constant` is flagged. The loop has no legitimate reason to test
    for the presence of a magic string inside the model's output — that would be
    natural-language-driven control flow.
    """
    tree = _parse(LOOP_PY)
    offenders = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            # Check if any op is ast.In and left operand is a string constant
            if any(isinstance(op, ast.In) for op in node.ops):
                if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                    offenders.append(ast.unparse(node))

    assert not offenders, f"Found string-membership tests in loop.py: {offenders}"


# ---------------------------------------------------------------------------
# Anti-pattern 2 — no integer-literal iteration cap as the primary stop mechanism
# ---------------------------------------------------------------------------
def test_no_integer_literal_iteration_cap_in_loop() -> None:
    """No `for _ in range(<int literal>)` and no `while <var> < <int literal>` in loop.py.

    Token/wall-clock/config-sourced budgets are explicitly allowed because they
    read their cap from a `Budget` instance (an attribute access or a function
    arg), not from a literal. If you need a cap, pass it in.
    """
    tree = _parse(LOOP_PY)
    offenders = []

    for node in ast.walk(tree):
        # Check for range(<int literal>) in for loops
        if isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call):
                if isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
                    # Check if any argument is an int constant
                    for arg in node.iter.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, int):
                            offenders.append(ast.unparse(node.iter))
                            break

        # Check for <var> < <int literal> in while loops
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Compare):
                # Check if right side has an int constant
                for comparator in node.test.comparators:
                    if isinstance(comparator, ast.Constant) and isinstance(comparator.value, int):
                        offenders.append(ast.unparse(node.test))
                        break

    assert not offenders, f"Found integer-literal iteration caps in loop.py (use a Budget instead): {offenders}"


# ---------------------------------------------------------------------------
# Positive evidence — stop_reason is the value that breaks the while loop
# ---------------------------------------------------------------------------
def test_stop_reason_is_loop_control() -> None:
    """loop.py references `stop_reason` AND a `while` loop exits via return/raise on it."""
    tree = _parse(LOOP_PY)

    # Check 1: At least one reference to stop_reason
    stop_reason_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr == "stop_reason":
                stop_reason_found = True
                break
        if isinstance(node, ast.Name):
            if node.id == "stop_reason":
                stop_reason_found = True
                break

    assert stop_reason_found, "No reference to 'stop_reason' found in loop.py"

    # Check 2: At least one while loop that references stop_reason and contains return/raise
    while_loop_ok = False
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            body_text = ast.unparse(node)
            has_stop_reason = "stop_reason" in body_text
            has_return_or_raise = "return" in body_text or "raise" in body_text
            if has_stop_reason and has_return_or_raise:
                while_loop_ok = True
                break

    assert while_loop_ok, "No while loop found that exits on stop_reason with return/raise in loop.py"


# ---------------------------------------------------------------------------
# Decision-tree-in-Python — no `if claim_type == "..."` branches in the package
# ---------------------------------------------------------------------------
def test_no_claim_type_equality_branching_in_package() -> None:
    """Decision logic about claim type lives in the model, not in Python.

    tools.py is exempt (it defines the enum in input_schema).
    pricing.py is exempt (it may map claim_type to per-queue cost weights).
    """
    offenders = []

    # Walk every .py file under PKG recursively
    for py_file in PKG.rglob("*.py"):
        # Skip exempt files
        if py_file.name in ("tools.py", "pricing.py", "__init__.py"):
            continue

        tree = _parse(py_file)

        # Find ast.Compare nodes with ast.Eq comparing claim_type to a string constant
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                if any(isinstance(op, ast.Eq) for op in node.ops):
                    # Check if left operand is claim_type (Name or Attribute)
                    left_is_claim_type = False
                    if isinstance(node.left, ast.Name) and node.left.id == "claim_type":
                        left_is_claim_type = True
                    elif isinstance(node.left, ast.Attribute) and node.left.attr == "claim_type":
                        left_is_claim_type = True

                    # Check if compared against a string constant
                    if left_is_claim_type:
                        for comparator in node.comparators:
                            if isinstance(comparator, ast.Constant) and isinstance(comparator.value, str):
                                expr = ast.unparse(node)
                                offenders.append(f"{py_file.name}:{node.lineno}: {expr}")

    assert not offenders, (
        f"Found claim_type equality branching in package (move decision to model): {offenders}"
    )
