from rest_framework import status
from rest_framework.test import APIRequestFactory

from assessment.schemas import (
    ANSWER_KEY_SCHEMAS,
    ASSESSMENT_RESPONSE_SCHEMA,
    ASSESSMENT_TYPES,
    MULTIPLE_CHOICE_ANSWER_KEY_SCHEMA,
    MULTIPLE_CHOICE_SECTION_SCHEMA,
    SCENARIO_BASED_ANSWER_KEY_SCHEMA,
    SCENARIO_BASED_SECTION_SCHEMA,
    SECTION_SCHEMAS,
    SHORT_ANSWER_ANSWER_KEY_SCHEMA,
    SHORT_ANSWER_SECTION_SCHEMA,
)
from assessment.views import AssessmentView


def test_composes_sections_by_assessment_type():
    assert list(SECTION_SCHEMAS) == list(ASSESSMENT_TYPES)
    assert SECTION_SCHEMAS["multiple_choice"] is MULTIPLE_CHOICE_SECTION_SCHEMA
    assert SECTION_SCHEMAS["short_answer"] is SHORT_ANSWER_SECTION_SCHEMA
    assert SECTION_SCHEMAS["scenario_based"] is SCENARIO_BASED_SECTION_SCHEMA


def test_composes_answer_keys_by_assessment_type():
    assert list(ANSWER_KEY_SCHEMAS) == list(ASSESSMENT_TYPES)
    assert (
        ANSWER_KEY_SCHEMAS["multiple_choice"]
        is MULTIPLE_CHOICE_ANSWER_KEY_SCHEMA
    )
    assert ANSWER_KEY_SCHEMAS["short_answer"] is SHORT_ANSWER_ANSWER_KEY_SCHEMA
    assert (
        ANSWER_KEY_SCHEMAS["scenario_based"]
        is SCENARIO_BASED_ANSWER_KEY_SCHEMA
    )


def test_aggregate_schema_preserves_required_strict_objects():
    response_format = ASSESSMENT_RESPONSE_SCHEMA["format"]
    root_schema = response_format["schema"]
    sections_schema = root_schema["properties"]["sections"]
    answer_key_schema = root_schema["properties"]["answer_key"]

    assert response_format["type"] == "json_schema"
    assert response_format["name"] == "skill_assessment"
    assert response_format["strict"] is True
    assert root_schema["required"] == [
        "title",
        "metadata",
        "learning_objectives",
        "sections",
        "answer_key",
        "scoring_guide",
    ]
    assert root_schema["additionalProperties"] is False
    assert sections_schema["properties"] is SECTION_SCHEMAS
    assert sections_schema["required"] == list(ASSESSMENT_TYPES)
    assert sections_schema["additionalProperties"] is False
    assert answer_key_schema["properties"] is ANSWER_KEY_SCHEMAS
    assert answer_key_schema["required"] == list(ASSESSMENT_TYPES)
    assert answer_key_schema["additionalProperties"] is False


def test_view_exposes_and_sends_composed_schema(mocker):
    mock_openai = mocker.patch("assessment.views.OpenAI")
    mock_openai.return_value.responses.create.return_value.output_text = "{}"
    request = APIRequestFactory().post(
        "/assessment/",
        data={"topic": "The Kubernetes control plane manages clusters"},
        format="json",
    )

    response = AssessmentView.as_view()(request)

    assert AssessmentView.ASSESSMENT_RESPONSE_SCHEMA is ASSESSMENT_RESPONSE_SCHEMA
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {}
    mock_openai.return_value.responses.create.assert_called_once_with(
        model="gpt-5.6",
        input=(
            "Create a skill assessment based on: "
            "{'topic': 'The Kubernetes control plane manages clusters'}"
        ),
        text=ASSESSMENT_RESPONSE_SCHEMA,
    )
