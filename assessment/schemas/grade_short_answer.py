GRADE_SHORT_ANSWER_RESPONSE_SCHEMA = {
    "format": {
        "type": "json_schema",
        "name": "grade_short_answer",
        "schema": {
            "type": "object",
            "properties": {
                "criteria_scores": {
                    "type": "array",
                    "description": (
                        "A score for each accepted point used to grade the answer."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "criterion": {
                                "type": "string",
                                "description": (
                                    "The accepted point being assessed."
                                ),
                            },
                            "score": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "description": (
                                    "How well the response covers the criterion, "
                                    "from 0 (not covered) to 1 (excellent coverage)."
                                ),
                            },
                        },
                        "required": ["criterion", "score"],
                        "additionalProperties": False,
                    },
                },
                "headline_assessment": {
                    "type": "string",
                    "description": (
                        "A concise overall assessment, such as "
                        "'Perfect response' or 'Inadequate response'."
                    ),
                },
                "rationale": {
                    "type": "string",
                    "description": (
                        "A concise explanation of the assessment based on the "
                        "model answer and accepted points."
                    ),
                },
            },
            "required": [
                "criteria_scores",
                "headline_assessment",
                "rationale",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    }
}
