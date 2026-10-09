SCENARIO_BASED_SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "instructions": {"type": "string"},
        "total_points": {"type": "integer", "minimum": 0},
        "scenarios": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "minimum": 1},
                    "title": {"type": "string"},
                    "points": {"type": "integer", "minimum": 0},
                    "description": {"type": "string"},
                    "evidence": {
                        "type": "array",
                        "description": (
                            "Commands, logs, events, manifests, or other "
                            "supporting material."
                        ),
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        "text",
                                        "command",
                                        "log",
                                        "event",
                                        "yaml",
                                        "json",
                                        "code",
                                    ],
                                },
                                "content": {"type": "string"},
                            },
                            "required": ["type", "content"],
                            "additionalProperties": False,
                        },
                    },
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "number": {"type": "integer", "minimum": 1},
                                "question": {"type": "string"},
                            },
                            "required": ["number", "question"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": [
                    "number",
                    "title",
                    "points",
                    "description",
                    "evidence",
                    "questions",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "instructions", "total_points", "scenarios"],
    "additionalProperties": False,
}


SCENARIO_BASED_ANSWER_KEY_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "scenario_number": {"type": "integer", "minimum": 1},
            "answers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_number": {"type": "integer", "minimum": 1},
                        "expected_answer": {"type": "string"},
                        "accepted_alternatives": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "question_number",
                        "expected_answer",
                        "accepted_alternatives",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["scenario_number", "answers"],
        "additionalProperties": False,
    },
}
