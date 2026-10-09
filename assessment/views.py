import json

from dotenv import load_dotenv
from openai import OpenAI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import vcr

from assessment.schemas import (
    ASSESSMENT_RESPONSE_SCHEMA as COMPOSED_ASSESSMENT_RESPONSE_SCHEMA,
    GRADE_SHORT_ANSWER_RESPONSE_SCHEMA,
)
from assessment.validators.input_validator import InputValidator

load_dotenv()

class GradeShortAnswer(APIView, InputValidator):

    RESPONSE_SCHEMA = GRADE_SHORT_ANSWER_RESPONSE_SCHEMA

    MANDATORY_FIELDS = [
        "user_response",
        "short_answer_grade_guide.expected_answer",
        "short_answer_grade_guide.accepted_points"
    ]

    @classmethod
    def dig(cls, data, *keys):
        if not keys: return data

        head, *tail = keys

        if not isinstance(data, dict): return None

        result = data.get(head)

        return cls.dig(result, *tail) if tail else result


    def post(self, request, format="json"):
        payload = request.data.get("data")

        payload_values = []
        payload_values.append(self.dig(payload, 'question'))
        payload_values.append(self.dig(payload, 'user_response'))
        payload_values.append(self.dig(payload, 'short_answer_grade_guide', 'expected_answer'))

        result = self.dig(payload, 'short_answer_grade_guide', 'accepted_points')
        if result:
            payload_values.append(",".join(result))
        else:
            payload_values.append("")

        if all(map(self.has_minimum_word_count, payload_values)):
            (question, user_response, expected_answer, accepted_points) = payload_values

            grade_short_answer_meta_prompt = f"""
                Review the following response {user_response} to the following question {question}.
                Evaluate the quality of the response through the lens of this criteria coverage.

                Provide an assessment score for each critera on a continuous scale of 0 to 1,
                where 0 indicates no score and 1 indicates an extremely excellent score.
                A score is excellent if it is closely aligned to the model score and the given criteria.
                Base your marking/grading scheme through the following accepted points {accepted_points}.

                This is the model, perfect or ideal answer {expected_answer}.
                Provide a final headline assessment i.e.
                for an extremely excellent score you can respond with “Perfect response”,
                for a poor response you can respond with “Inadequate” response.
                These examples serves as guides to help you facilitate judgement.
                Additionally, provide a rationale for your assessment i.e. “You covered most of the key ideas”
            """

            cassette = vcr.VCR(
                cassette_library_dir="assessment/cassettes/development",
                record_mode="new_episodes",
                match_on=["method", "scheme", "host", "port", "path", "query", "body"],
                filter_headers=["authorization"],
            )

            with cassette.use_cassette("grading-short-answer.yaml"):
                client = OpenAI()
                model_result = client.responses.create(
                    model="gpt-5.6",
                    input=grade_short_answer_meta_prompt,
                    text=self.RESPONSE_SCHEMA,
                )

            response = Response(
                data=json.loads(model_result.output_text),
                status=status.HTTP_201_CREATED,
            )
        else:
            response = Response(
                data={"message": "Invalid request data"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return response

class AssessmentView(APIView):
    MIN_WORD_COUNT = 4
    ASSESSMENT_RESPONSE_SCHEMA = COMPOSED_ASSESSMENT_RESPONSE_SCHEMA

    @classmethod
    def has_minimum_word_count(cls, topic):
        return isinstance(topic, str) and len(topic.split()) >= cls.MIN_WORD_COUNT


    def post(self, request, format="json"):
        topic = request.data.get("topic")

        if not self.has_minimum_word_count(topic):
            return Response(
                data={"message": "Topic must contain at least four words."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        cassette = vcr.VCR(
            cassette_library_dir="assessment/cassettes/development",
            record_mode="new_episodes",
            match_on=["method", "scheme", "host", "port", "path", "query", "body"],
            filter_headers=["authorization"],
        )
        client = OpenAI()
        meta_prompt = f"""
            Create a skill assessment based on: {request.data}.  
            "Wrap code blocks in triple backticks with language tag and inline code with single backticks.
            "Where helpful/viable include illustrations using mermaid(favour top-down orientation). Wrap mermaid as blocks with triple backticks and 'mermaid' as the language tag.
        """

        with cassette.use_cassette("assessment-0.yaml"):
            model_result = client.responses.create(
                model="gpt-5.6",
                input=meta_prompt,
                text=self.ASSESSMENT_RESPONSE_SCHEMA,
            )

        response_data = json.loads(model_result.output_text)
        response_data["metadata"]["original_source"] = topic
        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED
        )
