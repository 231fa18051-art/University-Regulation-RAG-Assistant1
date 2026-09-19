def understand_query(question):
    """
    Understand the student's question and expand it with
    regulation-related concepts to improve retrieval.
    """

    question_lower = question.lower().strip()

    expanded_terms = []

    # =====================================================
    # SGPA
    # =====================================================

    if any(term in question_lower for term in [
        "sgpa",
        "semester gpa",
        "semester grade point average",
        "semester grade point",
        "semester average"
    ]):

        expanded_terms.extend([
            "SGPA",
            "Semester Grade Point Average",
            "grade points",
            "course credits",
            "credits",
            "computation of SGPA"
        ])

    # =====================================================
    # CGPA
    # =====================================================

    elif any(term in question_lower for term in [
        "cgpa",
        "cumulative gpa",
        "cumulative grade point average",
        "overall gpa",
        "overall grade point average",
        "overall academic average"
    ]):

        expanded_terms.extend([
            "CGPA",
            "Cumulative Grade Point Average",
            "grade points",
            "course credits",
            "credits",
            "computation of CGPA"
        ])

    # =====================================================
    # GRADING / LETTER GRADE
    # =====================================================

    elif any(term in question_lower for term in [
        "grading",
        "grading system",
        "letter grade",
        "letter grades",
        "grade point",
        "grade points",
        "what grade",
        "which grade",
        "grade will i get",
        "o grade",
        "s grade",
        "a grade",
        "b grade",
        "c grade",
        "marks"
    ]):

        expanded_terms.extend([
            "COMPUTATION OF GRADING",
            "Letter Grade",
            "Grade Point",
            "Grade Points",
            "Percentage of Marks",
            "Outstanding",
            "Excellent",
            "Very good",
            "Good",
            "Fair",
            "Marginal",
            "Incomplete",
            "O",
            "S",
            "A",
            "B",
            "C",
            "M",
            "I",
            "Table 14"
        ])

    # =====================================================
    # ATTENDANCE
    # =====================================================

    elif any(term in question_lower for term in [
        "attendance",
        "attend",
        "attendance percentage",
        "attendance requirement",
        "attendance shortage",
        "shortage of attendance",
        "present percentage",
        "absent percentage",
        "can i write exam",
        "write exams with"
    ]):

        expanded_terms.extend([
            "ATTENDANCE",
            "minimum attendance",
            "75%",
            "attendance requirement",
            "attendance eligibility",
            "shortage of attendance",
            "examination eligibility"
        ])

    # =====================================================
    # SUPPLEMENTARY / COURSE FAILURE
    # =====================================================
    # SUPPLEMENTARY / COURSE FAILURE
    elif (
        any(term in question_lower for term in [
            "supplementary",
            "supplementary exam",
            "supplementary examination",
            "back paper",
            "reappear",
            "write again",
            "clear a backlog"
        ])
        or
        any(term in question_lower for term in [
            "failed subject",
            "failed course",
            "fail a subject",
            "fail a course",
            "failed in",
            "fail in",
            "course failure",
            "failed a course"
        ])
    ):
        expanded_terms.extend([
            "COURSE FAILURE",
            "failed course",
            "failed subject",
            "course failure rules",
            "failure in a course",
            "failed courses",
            "supplementary examination",
            "supplementary exam",
            "re-examination",
            "reappear",
            "backlog",
            "back paper",
            "course completion",
            "pass the course"
        ])

    # =====================================================
    # BRANCH CHANGE
    # =====================================================

        # =====================================================
    # BRANCH CHANGE
    # =====================================================

    elif (
        any(term in question_lower for term in [
            "branch change",
            "change branch",
            "change my branch",
            "switch branch",
            "change department",
            "change my department",
            "branch transfer",
            "transfer branch"
        ])
        or (
            any(term in question_lower for term in [
                "move from",
                "move to",
                "switch from",
                "switch to",
                "change from",
                "change to"
            ])
            and any(term in question_lower for term in [
                "cse",
                "ece",
                "eee",
                "mech",
                "civil",
                "it",
                "department",
                "branch"
            ])
        )
    ):

        expanded_terms.extend([
            "CHANGE OF BRANCH",
            "branch change",
            "branch transfer",
            "eligibility for branch change",
            "procedure for changing branch"
        ])
    # =====================================================
    # PROMOTION
    # =====================================================

        # =====================================================
    # PROMOTION
    # =====================================================

    elif (
        any(term in question_lower for term in [
            "promotion",
            "promoted",
            "next semester",
            "next year",
            "move to next semester",
            "move to next year",
            "eligible for next semester"
        ])
        or (
            any(term in question_lower for term in [
                "backlog",
                "backlogs",
                "failed subject",
                "failed course"
            ])
            and any(term in question_lower for term in [
                "next semester",
                "next year",
                "promoted",
                "promotion",
                "continue",
                "move forward"
            ])
        )
    ):

        expanded_terms.extend([
            "PROMOTION",
            "promotion to next semester",
            "promotion requirements",
            "academic promotion",
            "next semester",
            "backlogs"
        ])

    # =====================================================
    # COURSE REGISTRATION
    # =====================================================

    elif any(term in question_lower for term in [
        "course registration",
        "register course",
        "register courses",
        "course enrollment",
        "course enrolment",
        "enroll course",
        "enrol course",
        "registration of courses"
    ]):

        expanded_terms.extend([
            "COURSE REGISTRATION",
            "registration of courses",
            "course enrollment",
            "semester registration"
        ])

    # =====================================================
    # LATERAL ENTRY
    # =====================================================

        # =====================================================
    # LATERAL ENTRY
    # =====================================================

    elif (
        any(term in question_lower for term in [
            "lateral entry",
            "lateral entry student",
            "lateral entry students",
            "diploma entry",
            "diploma student",
            "diploma students",
            "joined through diploma"
        ])
        or (
            any(term in question_lower for term in [
                "diploma",
                "polytechnic"
            ])
            and any(term in question_lower for term in [
                "b.tech",
                "btech",
                "b tech",
                "joined",
                "admission",
                "entry"
            ])
        )
    ):

        expanded_terms.extend([
            "LATERAL ENTRY",
            "lateral entry students",
            "diploma students",
            "admission through lateral entry"
        ])
    # =====================================================
    # CREDITS
    # =====================================================

    elif any(term in question_lower for term in [
        "how many credits",
        "total credits",
        "credit requirement",
        "credit requirements",
        "credits required",
        "number of credits"
    ]):

        expanded_terms.extend([
            "CREDITS",
            "total credits",
            "credit requirements",
            "credits required for completion",
            "B.Tech credits"
        ])

    # =====================================================
    # DEGREE REQUIREMENTS
    # =====================================================

    elif any(term in question_lower for term in [
        "degree requirement",
        "degree requirements",
        "complete b.tech",
        "complete btech",
        "finish b.tech",
        "finish btech",
        "graduate",
        "graduation requirements",
        "requirements for degree"
    ]):

        expanded_terms.extend([
            "DEGREE REQUIREMENTS",
            "award of B.Tech degree",
            "requirements for degree",
            "completion requirements",
            "credits required"
        ])

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    expanded_terms = list(dict.fromkeys(expanded_terms))

    # =====================================================
    # CREATE EXPANDED QUERY
    # =====================================================

    expanded_query = question

    if expanded_terms:
        expanded_query += " " + " ".join(expanded_terms)

    return expanded_query