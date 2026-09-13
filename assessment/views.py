import json

from dotenv import load_dotenv
from openai import OpenAI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import vcr

from assessment.schemas import (
    ASSESSMENT_RESPONSE_SCHEMA as COMPOSED_ASSESSMENT_RESPONSE_SCHEMA,
)


load_dotenv()


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
            "Where helpful/viable include illustrations using mermaid. Wrap mermaid as blocks with triple backticks and 'mermaid' as the language tag.
        """

        # with cassette.use_cassette("assessment-typescript-utility-types.yaml"):
        # with cassette.use_cassette("assessment.yaml"):
        # with cassette.use_cassette("assessment-ruby-class.yaml"):
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
