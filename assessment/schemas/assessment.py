from assessment.schemas.multiple_choice import (
    MULTIPLE_CHOICE_ANSWER_KEY_SCHEMA,
    MULTIPLE_CHOICE_SECTION_SCHEMA,
)
from assessment.schemas.scenario_based import (
    SCENARIO_BASED_ANSWER_KEY_SCHEMA,
    SCENARIO_BASED_SECTION_SCHEMA,
)
from assessment.schemas.short_answer import (
    SHORT_ANSWER_ANSWER_KEY_SCHEMA,
    SHORT_ANSWER_SECTION_SCHEMA,
)


ASSESSMENT_TYPES = (
    "multiple_choice",
    "short_answer",
    "scenario_based",
)

SECTION_SCHEMAS = {
    "multiple_choice": MULTIPLE_CHOICE_SECTION_SCHEMA,
    "short_answer": SHORT_ANSWER_SECTION_SCHEMA,
    "scenario_based": SCENARIO_BASED_SECTION_SCHEMA,
}

ANSWER_KEY_SCHEMAS = {
    "multiple_choice": MULTIPLE_CHOICE_ANSWER_KEY_SCHEMA,
    "short_answer": SHORT_ANSWER_ANSWER_KEY_SCHEMA,
    "scenario_based": SCENARIO_BASED_ANSWER_KEY_SCHEMA,
}

ASSESSMENT_RESPONSE_SCHEMA = {
    "format": {
        "type": "json_schema",
        "name": "skill_assessment",
        "schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the skill assessment.",
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The subject covered by the assessment.",
                        },
                        "target_level": {
                            "type": "string",
                            "description": (
                                "The intended learner proficiency level."
                            ),
                        },
                        "suggested_time_minutes": {
                            "type": "object",
                            "properties": {
                                "minimum": {"type": "integer", "minimum": 1},
                                "maximum": {"type": "integer", "minimum": 1},
                            },
                            "required": ["minimum", "maximum"],
                            "additionalProperties": False,
                        },
                        "total_points": {"type": "integer", "minimum": 0},
                    },
                    "required": [
                        "topic",
                        "target_level",
                        "suggested_time_minutes",
                        "total_points",
                    ],
                    "additionalProperties": False,
                },
                "learning_objectives": {
                    "type": "array",
                    "description": "Skills or knowledge learners should demonstrate.",
                    "items": {"type": "string"},
                },
                "sections": {
                    "type": "object",
                    "properties": SECTION_SCHEMAS,
                    "required": list(ASSESSMENT_TYPES),
                    "additionalProperties": False,
                },
                "answer_key": {
                    "type": "object",
                    "properties": ANSWER_KEY_SCHEMAS,
                    "required": list(ASSESSMENT_TYPES),
                    "additionalProperties": False,
                },
                "scoring_guide": {
                    "type": "object",
                    "properties": {
                        "levels": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "minimum_score": {
                                        "type": "integer",
                                        "minimum": 0,
                                    },
                                    "maximum_score": {
                                        "type": "integer",
                                        "minimum": 0,
                                    },
                                    "proficiency": {"type": "string"},
                                },
                                "required": [
                                    "minimum_score",
                                    "maximum_score",
                                    "proficiency",
                                ],
                                "additionalProperties": False,
                            },
                        },
                        "critical_misconception_check": {
                            "type": "string",
                            "description": (
                                "A key conceptual distinction learners must understand."
                            ),
                        },
                    },
                    "required": ["levels", "critical_misconception_check"],
                    "additionalProperties": False,
                },
            },
            "required": [
                "title",
                "metadata",
                "learning_objectives",
                "sections",
                "answer_key",
                "scoring_guide",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    }
}
