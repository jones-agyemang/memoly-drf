from rest_framework.test import APIRequestFactory
from rest_framework import status
import pytest

from assessment.views import AssessmentView

def describe_assessment():

    factory = APIRequestFactory()

    def context_has_valid_attributes():

        @pytest.fixture
        def valid_attributes():
            return {
                "topic": (
                    "The Kubernetes control plane manages"
                    "the cluster state and scheduling decisions"
                )
            }

        @pytest.mark.vcr()
        def it_permits_creation(valid_attributes):
            request = factory.post("/assessments/", data=valid_attributes)
            response = AssessmentView.as_view()(request)
            assert response.status_code == status.HTTP_201_CREATED
    
    def context_has_invalid_attributes():

        @pytest.mark.parametrize("attributes", [
            {},
            { 'topic': '' },
            { 'topic': ' ' },
            { 'topic': '\t\n ' },
            { 'topic': 123 },
            { 'topic': 'only three words' },
            { 'topic': { 'nested-topic': 'foo bar' } },
        ])
        def it_forbids_creation(attributes, mocker):
            mock_llm_client = mocker.patch("assessment.views.OpenAI")

            request = factory.post("assessment/", data=attributes, format='json')
            response = AssessmentView.as_view()(request)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert response.data == { "message": "Topic must contain at least four words." }
            mock_llm_client.assert_not_called()
