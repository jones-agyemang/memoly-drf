from rest_framework.test import APIRequestFactory
from rest_framework import status
import pytest

from assessment.views import GradeShortAnswer

def describe_grade_short_answer():

    factory = APIRequestFactory()

    def context_invalid_request_body():

        @pytest.mark.parametrize("request_body", [
            {},
            {"data": {}},
            {
                "data": {
                    "user_response": ""
                }
            },
            {
                "data": {
                    "question": "What is a cluster?",
                    "user_response": "",
                    "short_answer_grade_guide": {
                        "expected_answer": "",
                        "accepted_points": []
                    }
                }
            },
            {
                "data": {
                    "question": "Lorem ipsum dolor cap ki?",
                    "user_response": "lorem ipsum dolore cap",
                    "short_answer_grade_guide": {
                        "expected_answer": "Lorem ipsum dolore cap",
                        "accepted_points": [
                            "Lorem ipsum dolor",
                        ]
                    }
                }
            }
        ])
        def it_rejects_grading_process(request_body):
            request = factory.post(
                "/assessment/grade-short-answer/",
                data=request_body,
                format="json"
            )
            response = GradeShortAnswer.as_view()(request)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert response.data == { "message": "Invalid request data" }
    
    def context_valid_request():

        @pytest.fixture
        def valid_attributes():
            return {
                "data": {
                    "question": "Name three core Kubernetes control plane components and explain the primary responsibility of each.",
                    "user_response": "Kubernetes is an open-sourced infrastructure resource provisioning and management tool",
                    "short_answer_grade_guide": {
                        "expected_answer": (
                            "Any three appropriate components with their responsibilities:"
                            "kube-apiserver exposes and validates the Kubernetes API;"
                            "etcd persistently stores API data and cluster state;"
                            "kube-scheduler selects nodes for unscheduled Pods;"
                            "kube-controller-manager runs reconciliation controllers;"
                            "cloud-controller-manager integrates Kubernetes with supported cloud-provider APIs"
                        ),
                        "accepted_points": [
                            "kube-apiserver receives, validates, and processes API requests",
                            "etcd persistently stores Kubernetes API objects and cluster state"
                        ]
                    }
                }
            }

        def it_accepts_grading_process(valid_attributes):
            request = factory.post(
                "/assessment/grade-short-answer/",
                data=valid_attributes,
                format="json"
            )
            response = GradeShortAnswer.as_view()(request)
            assert response.status_code == status.HTTP_201_CREATED