# Issue Table — Lab 5 Static Code Analysis

Tools: Pylint (quality), Bandit (security), Flake8 (PEP 8 style). Reports for the original code are in [`reports/before/`](reports/before), the fixed code in [`reports/after/`](reports/after).

| # | Issue | Tool / ID | Type | Line(s) (original) | Description | Fix Approach |
|---|-------|-----------|------|--------------------|-------------|--------------|
| 1 | Shell command built from input | Bandit B605 (High) | Security | 63 | `os.system("echo ... " + filename)` lets a crafted filename inject shell commands. | Removed `os.system`; use plain `print()`. |
| 2 | Weak MD5 hash | Bandit B324 (High) | Security | 52 | MD5 is broken and unsuitable for hashing student identifiers. | Switched to `hashlib.sha256`. |
| 3 | `eval()` on user text | Bandit B307 (Medium), Pylint W0123 | Security | 47 | Arbitrary code execution through `discount_expr`. | Parse with `ast` and evaluate only numbers, `base_fee`, `+ - * /` and unary minus via a whitelist evaluator. |
| 4 | Hard-coded secret | Bandit B105 (Low) | Security | 75, 84 | Registrar token committed in source **and printed** to stdout. | Read from `REGISTRAR_AUTH_TOKEN` env var; only print whether it is configured. |
| 5 | Predictable OTP | Bandit B311 (Low) | Security | 56 | `random.randint` is not cryptographically secure. | Use `secrets.randbelow`. |
| 6 | try/except/pass with bare except | Bandit B110, Pylint W0702, Flake8 E722 | Bug | 28-32 | Swallows every error (even `KeyboardInterrupt`) so failures are invisible. | Explicit `courses.get()` lookup and a boolean result. |
| 7 | Mutable default argument | Pylint W0102 | Bug | 15 | `audit_trail=[]` is shared across calls, so unrelated enrollments leak into one list. | Default `None`, create a fresh list inside the function. |
| 8 | **Logic bug (found by running)**: phantom seat on drop | Manual | Bug | 27-32 | `dropCourse("CS202")` added a seat to a course nobody was enrolled in and re-opened it, so the program reported *3* open courses instead of 2. Tuition was never refunded either. | Track an `enrolled` counter; `drop_course` refuses when nobody is enrolled, otherwise frees the seat and refunds the fee. |
| 9 | Global statement | Pylint W0603 | Quality | 16 | Mutating a module global through `global`. | Keep the running total in a `LEDGER` dict. |
| 10 | File opened without `with` / encoding | Pylint R1732, W1514 | Resource | 60-62 | File may stay open on error; encoding is platform dependent. | `with open(..., encoding="utf-8")`. |
| 11 | Naming style | Pylint C0103 | Style | 15, 27, 35, 45, 51, 55, 59, 66 | camelCase function names break PEP 8. | Renamed to `snake_case`. |
| 12 | Missing docstrings | Pylint C0114, C0116 | Style | all | No module/function documentation. | Added docstrings everywhere. |
| 13 | `== None`, redundant if/else, unused names | Pylint C0121, R1703, R1705, W0612, W0611; Flake8 E711, F841, F401 | Style | 4, 36-42, 46, 68 | Non-idiomatic comparison, redundant branches, dead variables and `import math`. | `is None`, direct boolean return, removed dead code. |
| 14 | Redefined outer name | Pylint W0621 | Quality | 66 | Parameter `courses` shadows the global. | Renamed parameter to `catalog`. |
| 15 | Line length / final newline | Flake8 E501, W292, Pylint C0301, C0304 | Style | 7-9, 15, 23, 79, 87 | Lines over 79 characters; no trailing newline. | Wrapped lines, added newline, added `if __name__ == "__main__"` guard. |

## Score summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.00 / 10 | **10.00 / 10** |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | **0 issues** |
| Flake8 | 12 violations | **0 violations** |
