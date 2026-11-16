"""Course enrollment system: catalog, enrollment, drops, tuition and roster."""
import ast
import hashlib
import operator
import os
import secrets

courses = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "enrolled": 0,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "enrolled": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "enrolled": 0,
        "fee": 600.0,
        "is_closed": False,
    },
}

LEDGER = {"total_tuition": 0.0}


def enroll_student(course_id, student_name, credits_registered=3,
                   audit_trail=None):
    """Enroll a student in a course; return True on success."""
    if audit_trail is None:
        audit_trail = []
    if course_id not in courses or courses[course_id]["is_closed"]:
        return False
    course = courses[course_id]
    course["seats"] -= 1
    course["enrolled"] += 1
    if course["seats"] <= 0:
        course["is_closed"] = True
    LEDGER["total_tuition"] += course["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Drop one enrolled student, free the seat and refund the fee."""
    course = courses.get(course_id)
    if course is None or course["enrolled"] <= 0:
        return False
    course["enrolled"] -= 1
    course["seats"] += 1
    course["is_closed"] = False
    LEDGER["total_tuition"] -= course["fee"]
    return True


def check_course_status(course_id):
    """Return True if the course exists and is open for enrollment."""
    course = courses.get(course_id)
    return course is not None and not course["is_closed"]


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval(node, base_fee):
    """Evaluate a parsed arithmetic expression without using eval()."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, base_fee)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "base_fee":
        return base_fee
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](
            _safe_eval(node.left, base_fee), _safe_eval(node.right, base_fee))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_eval(node.operand, base_fee)
    raise ValueError("unsupported discount expression")


def calculate_scholarship_tuition(course_id, discount_expr):
    """Evaluate a discount such as 'base_fee * 0.75' (arithmetic only)."""
    base_fee = courses[course_id]["fee"]
    tree = ast.parse(discount_expr, mode="eval")
    return _safe_eval(tree, base_fee)


def generate_student_hash(roll_no):
    """Return a hex digest identifying a student roll number."""
    return hashlib.sha256(roll_no.encode()).hexdigest()


def generate_enrollment_otp():
    """Return a 4-digit one-time enrollment code."""
    return 1000 + secrets.randbelow(9000)


def export_course_roster(filename="course_roster.txt"):
    """Write the course catalog to a text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(courses))
    print("Course roster exported to:", filename)


def get_open_courses_summary(catalog):
    """Count courses that are still open."""
    return sum(1 for details in catalog.values() if not details["is_closed"])


def main():
    """Run a demonstration of the enrollment system."""
    registrar_auth_token = os.environ.get("REGISTRAR_AUTH_TOKEN")
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    print("Scholarship Fee:",
          calculate_scholarship_tuition("CS303", "base_fee * 0.75"))
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(courses))
    print("Registrar Token configured:", registrar_auth_token is not None)


if __name__ == "__main__":
    main()
