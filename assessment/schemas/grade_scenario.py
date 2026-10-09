GRADE_SCENARIO_RESPONSE_SCHEMA = {
    "format": {
        "type": "json_schema",
        "name": "grade_scenario",
        "schema": {
            "type": "object",
            "properties": {
                "analysis": {
                    "type": "array",
                    "description": (
                        "One grading result for each analysis in the request."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_number": {
                                "type": "integer",
                                "minimum": 1,
                                "description": (
                                    "The question_number from the corresponding "
                                    "analysis in the request."
                                ),
                            },
                            "criteria_scores": {
                                "type": "array",
                                "description": (
                                    "Scores for the criteria derived from this "
                                    "analysis's accepted_alternatives, using "
                                    "expected_answer as the ideal answer. "
                                    "Equivalent accepted alternatives are valid "
                                    "ways to satisfy a criterion, not separate "
                                    "requirements the user must all meet."
                                ),
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "criterion": {
                                            "type": "string",
                                            "description": (
                                                "The grading criterion being assessed."
                                            ),
                                        },
                                        "score": {
                                            "type": "number",
                                            "minimum": 0,
                                            "maximum": 1,
                                            "description": (
                                                "How well the response covers the "
                                                "criterion, from 0 (not covered) "
                                                "to 1 (excellent coverage)."
                                            ),
                                        },
                                    },
                                    "required": ["criterion", "score"],
                                    "additionalProperties": False,
                                },
                            },
                        },
                        "required": ["question_number", "criteria_scores"],
                        "additionalProperties": False,
                    },
                },
                "headline_assessment": {
                    "type": "string",
                    "description": (
                        "A concise final assessment across all analysis responses, "
                        "such as 'Perfect response' or 'Inadequate response'."
                    ),
                },
                "rationale": {
                    "type": "string",
                    "description": (
                        "A concise explanation of the final assessment, covering "
                        "strengths and gaps relative to each analysis's "
                        "expected_answer and accepted_alternatives."
                    ),
                },
            },
            "required": ["analysis", "headline_assessment", "rationale"],
            "additionalProperties": False,
        },
        "strict": True,
    }
}
