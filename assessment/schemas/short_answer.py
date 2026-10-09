SHORT_ANSWER_SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "instructions": {"type": "string"},
        "total_points": {"type": "integer", "minimum": 0},
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "minimum": 1},
                    "title": {"type": "string"},
                    "question": {"type": "string"},
                    "points": {"type": "integer", "minimum": 0},
                },
                "required": ["number", "title", "question", "points"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "instructions", "total_points", "questions"],
    "additionalProperties": False,
}


SHORT_ANSWER_ANSWER_KEY_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question_number": {"type": "integer", "minimum": 1},
            "expected_answer": {"type": "string"},
            "accepted_points": {
                "type": "array",
                "description": (
                    "Individual facts or concepts that may receive credit."
                ),
                "items": {"type": "string"},
            },
        },
        "required": ["question_number", "expected_answer", "accepted_points"],
        "additionalProperties": False,
    },
}
