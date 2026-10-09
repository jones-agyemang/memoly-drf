from rest_framework.test import APIRequestFactory
from rest_framework import status 
import pytest

from assessment.grading.scenario import GradeScenario

def describe_scenario_grading():

    factory = APIRequestFactory()

    def context_invalid_request():

        @pytest.mark.parametrize("request_body", [
            {},
        ])
        def it_rejects_grading_process(request_body):
            request = factory.post(
                "/assessment/grade-scenario/",
                data=request_body,
                format="json"
            )
            response = GradeScenario.as_view()(request)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def context_valid_request():

        @pytest.fixture
        def valid_attributes():
            return {
                "data": {
                    "title": "Preparing a Fruit Report",
                    "description": "A shop needs three reports from the same basket data",
                    "evidence": ["basket = ['pear', 'apple', 'orange']"],
                    "analysis": [
                        {
                            "question_number": 12,
                            "question": "Write three loops that produce the requested reports. Use `sorted()`, `sorted(set(...))`, and `reversed()` as appropriate.",
                            "user_response": "```python basket_a = sorted(basket)```",
                            "scenario_grade_guide": {
                                "expected_answer": "```pythonfor fruit in sorted(basket):    print(fruit)for fruit in sorted(set(basket)):    print(fruit)for fruit in reversed(basket):    print(fruit)```",
                                "accepted_alternatives": [
                                    "Equivalent loops that use `sorted(basket)`, `sorted(set(basket))`, and `reversed(basket)` without mutating `basket`."
                                ]
                            }
                        }
                    ]
                }
            }

        def it_returns_grading_for_assessment(valid_attributes):
            request = factory.post(
                "/assessment/grade-scenario/",
                data=valid_attributes,
                format="json"
            )
            response = GradeScenario.as_view()(request)

            assert response.status_code == status.HTTP_201_CREATED
