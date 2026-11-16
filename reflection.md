# Reflection

**1. Which tool found the most serious problems, and why?**
Bandit. Its High findings (shell injection through `os.system`, MD5 hashing) and the Medium `eval()` finding are exploitable flaws, whereas Pylint and Flake8 mostly report maintainability and style. Pylint did find real bugs hidden in the code (mutable default argument, bare `except`).

**2. What did static analysis *not* catch?**
The logic bug. `dropCourse("CS202")` quietly re-opened a full course nobody was enrolled in, so the program printed `Open courses: 3`. No tool flagged it, because the code is syntactically and stylistically valid. I only found it by running the program and questioning the output, then fixed it by tracking an `enrolled` counter and refunding tuition.

**3. How did fixing one issue affect others?**
Replacing the bare `except` with an explicit `courses.get()` cleared the Bandit B110, Pylint W0702 and Flake8 E722 findings at once, and removing `os.system` removed both a High security finding and the need for a shell. Wrapping long lines for Flake8 also raised the Pylint score. Fixing the root cause usually clears several reports.

**4. How would static analysis fit into your workflow?**
Flake8 and Pylint in an editor or pre-commit hook for fast feedback, and Bandit plus a minimum Pylint score in CI so insecure code (hard-coded tokens, `eval`, weak hashes) cannot be merged. It complements tests and code review rather than replacing them, as the drop-course bug shows.
