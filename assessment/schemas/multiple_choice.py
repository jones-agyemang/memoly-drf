MULTIPLE_CHOICE_SECTION_SCHEMA = {
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
                    "question": {"type": "string"},
                    "points": {"type": "integer", "minimum": 0},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {
                                    "type": "string",
                                    "description": (
                                        "The option label, such as A, B, C, or D."
                                    ),
                                },
                                "text": {"type": "string"},
                            },
                            "required": ["label", "text"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["number", "question", "points", "options"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "instructions", "total_points", "questions"],
    "additionalProperties": False,
}


MULTIPLE_CHOICE_ANSWER_KEY_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question_number": {"type": "integer", "minimum": 1},
            "correct_option": {"type": "string"},
            "answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": [
            "question_number",
            "correct_option",
            "answer",
            "explanation",
        ],
        "additionalProperties": False,
    },
}
