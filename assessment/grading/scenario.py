from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from openai import OpenAI
import vcr
import json

from assessment.libs.dig import Dig
from assessment.validators.input_validator import InputValidator

load_dotenv()

from assessment.schemas.grade_scenario import GRADE_SCENARIO_RESPONSE_SCHEMA

class GradeScenario(APIView, Dig, InputValidator):

    @classmethod
    def build_payload_values(cls, payload) -> list:
        payload_values = list()
        payload_values.append(cls.dig(payload, 'title'))
        payload_values.append(cls.dig(payload, 'description'))

        payload_values.append(
            ",".join(
                cls.dig(payload, 'evidence', default=list())
            )
        )

        for analysis in cls.dig(payload, "analysis", default=[]):
            payload_values.append(cls.dig(analysis, "question"))
            payload_values.append(cls.dig(analysis, "user_response"))
            payload_values.append(cls.dig(analysis, "scenario_grade_guide", "expected_answer"))
            payload_values.append(
                ",".join(
                    cls.dig(analysis, "scenario_grade_guide", "accepted_alternatives", default=[])
                )
            )

        return payload_values

    def post(self, request, format="json"):
        payload = request.data.get("data")
        payload_values = self.build_payload_values(payload)

        valid_attributes = all(map(self.has_minimum_char_count, payload_values))

        if not valid_attributes:
            return Response(data=None, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        (
            title,
            description,
            evidence,
            question,
            *tail
        ) = payload_values
        analysis = self.dig(payload, "analysis")

        grade_scenario_meta_prompt = f"""
            A scenario with the following title "{title}" and description "{description}
            have been given to a user. The scenario is supported by the following evidence: {evidence}.

            The user is presented with several analysis. 
            Analysis: {analysis}
            The analysis summary contains information about question_number, question (based on the given scenario),
            user_response is the user's response to the question based on this scenario, and a scenario_grade_guide 
            contains grading guidance to help you evaluate the correctness of each analysis.

            Evaluate the quality of the responses through the lens of the respective criteria coverage.
            Provide an assessment score for each criteria on a continuous scale of 0 to 1,
            where 0 indicates no score and 1 indicates an extremely excellent score.
            A score is excellent if it is closely aligned to the model score and the given criteria.
            Base your marking/grading scheme on each analysis's accepted_alternatives.

            The expected_answer field holds the model, perfect or ideal answer.
            Provide a final headline assessment i.e.
            for an extremely excellent score you can respond with "Perfect response",
            for a poor response you can respond wuth "Inadequate" response.
            These examples serves as guides to help you facilitate judgement.
            Additionally, provide a rationale for your assessment i.e. "You covered most of the key ideas" 
        """

        cassette = vcr.VCR(
            cassette_library_dir="assessment/cassettes/development",
            record_mode="new_episodes",
            match_on=["method", "scheme", "host", "port", "path", "query", "body"],
            filter_headers=["authorization"],
        )

        with cassette.use_cassette("grading-scenario.yaml"):
            client = OpenAI()
            model_result = client.responses.create(
                model="gpt-5.6",
                input=grade_scenario_meta_prompt,
                text=GRADE_SCENARIO_RESPONSE_SCHEMA,
            ) 
        
        return Response(data=json.loads(model_result.output_text), status=status.HTTP_201_CREATED)