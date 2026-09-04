from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

class AssessmentView(APIView):

    MIN_WORD_COUNT = 4
    ASSESSMENT_RESPONSE_SCHEMA = {
        "format": {
          "type": "json_schema",
          "name": "skill_assessment",
          "schema": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "description": "The title of the skill assessment."
              },
              "metadata": {
                "type": "object",
                "properties": {
                  "topic": {
                    "type": "string",
                    "description": "The subject covered by the assessment."
                  },
                  "target_level": {
                    "type": "string",
                    "description": "The intended learner proficiency level."
                  },
                  "suggested_time_minutes": {
                    "type": "object",
                    "properties": {
                      "minimum": {
                        "type": "integer",
                        "minimum": 1
                      },
                      "maximum": {
                        "type": "integer",
                        "minimum": 1
                      }
                    },
                    "required": [
                      "minimum",
                      "maximum"
                    ],
                    "additionalProperties": False
                  },
                  "total_points": {
                    "type": "integer",
                    "minimum": 0
                  }
                },
                "required": [
                  "topic",
                  "target_level",
                  "suggested_time_minutes",
                  "total_points"
                ],
                "additionalProperties": False
              },
              "learning_objectives": {
                "type": "array",
                "description": "Skills or knowledge learners should demonstrate.",
                "items": {
                  "type": "string"
                }
              },
              "sections": {
                "type": "object",
                "properties": {
                  "multiple_choice": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string"
                      },
                      "instructions": {
                        "type": "string"
                      },
                      "total_points": {
                        "type": "integer",
                        "minimum": 0
                      },
                      "questions": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "number": {
                              "type": "integer",
                              "minimum": 1
                            },
                            "question": {
                              "type": "string"
                            },
                            "points": {
                              "type": "integer",
                              "minimum": 0
                            },
                            "options": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "label": {
                                    "type": "string",
                                    "description": "The option label, such as A, B, C, or D."
                                  },
                                  "text": {
                                    "type": "string"
                                  }
                                },
                                "required": [
                                  "label",
                                  "text"
                                ],
                                "additionalProperties": False
                              }
                            }
                          },
                          "required": [
                            "number",
                            "question",
                            "points",
                            "options"
                          ],
                          "additionalProperties": False
                        }
                      }
                    },
                    "required": [
                      "title",
                      "instructions",
                      "total_points",
                      "questions"
                    ],
                    "additionalProperties": False
                  },
                  "short_answer": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string"
                      },
                      "instructions": {
                        "type": "string"
                      },
                      "total_points": {
                        "type": "integer",
                        "minimum": 0
                      },
                      "questions": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "number": {
                              "type": "integer",
                              "minimum": 1
                            },
                            "title": {
                              "type": "string"
                            },
                            "question": {
                              "type": "string"
                            },
                            "points": {
                              "type": "integer",
                              "minimum": 0
                            }
                          },
                          "required": [
                            "number",
                            "title",
                            "question",
                            "points"
                          ],
                          "additionalProperties": False
                        }
                      }
                    },
                    "required": [
                      "title",
                      "instructions",
                      "total_points",
                      "questions"
                    ],
                    "additionalProperties": False
                  },
                  "scenario_based": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string"
                      },
                      "instructions": {
                        "type": "string"
                      },
                      "total_points": {
                        "type": "integer",
                        "minimum": 0
                      },
                      "scenarios": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "number": {
                              "type": "integer",
                              "minimum": 1
                            },
                            "title": {
                              "type": "string"
                            },
                            "points": {
                              "type": "integer",
                              "minimum": 0
                            },
                            "description": {
                              "type": "string"
                            },
                            "evidence": {
                              "type": "array",
                              "description": "Commands, logs, events, manifests, or other supporting material.",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "type": {
                                    "type": "string",
                                    "enum": [
                                      "text",
                                      "command",
                                      "log",
                                      "event",
                                      "yaml",
                                      "json",
                                      "code"
                                    ]
                                  },
                                  "content": {
                                    "type": "string"
                                  }
                                },
                                "required": [
                                  "type",
                                  "content"
                                ],
                                "additionalProperties": False
                              }
                            },
                            "questions": {
                              "type": "array",
                              "items": {
                                "type": "object",
                                "properties": {
                                  "number": {
                                    "type": "integer",
                                    "minimum": 1
                                  },
                                  "question": {
                                    "type": "string"
                                  }
                                },
                                "required": [
                                  "number",
                                  "question"
                                ],
                                "additionalProperties": False
                              }
                            }
                          },
                          "required": [
                            "number",
                            "title",
                            "points",
                            "description",
                            "evidence",
                            "questions"
                          ],
                          "additionalProperties": False
                        }
                      }
                    },
                    "required": [
                      "title",
                      "instructions",
                      "total_points",
                      "scenarios"
                    ],
                    "additionalProperties": False
                  }
                },
                "required": [
                  "multiple_choice",
                  "short_answer",
                  "scenario_based"
                ],
                "additionalProperties": False
              },
              "answer_key": {
                "type": "object",
                "properties": {
                  "multiple_choice": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "question_number": {
                          "type": "integer",
                          "minimum": 1
                        },
                        "correct_option": {
                          "type": "string"
                        },
                        "answer": {
                          "type": "string"
                        },
                        "explanation": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "question_number",
                        "correct_option",
                        "answer",
                        "explanation"
                      ],
                      "additionalProperties": False
                    }
                  },
                  "short_answer": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "question_number": {
                          "type": "integer",
                          "minimum": 1
                        },
                        "expected_answer": {
                          "type": "string"
                        },
                        "accepted_points": {
                          "type": "array",
                          "description": "Individual facts or concepts that may receive credit.",
                          "items": {
                            "type": "string"
                          }
                        }
                      },
                      "required": [
                        "question_number",
                        "expected_answer",
                        "accepted_points"
                      ],
                      "additionalProperties": False
                    }
                  },
                  "scenario_based": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "scenario_number": {
                          "type": "integer",
                          "minimum": 1
                        },
                        "answers": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "question_number": {
                                "type": "integer",
                                "minimum": 1
                              },
                              "expected_answer": {
                                "type": "string"
                              },
                              "accepted_alternatives": {
                                "type": "array",
                                "items": {
                                  "type": "string"
                                }
                              }
                            },
                            "required": [
                              "question_number",
                              "expected_answer",
                              "accepted_alternatives"
                            ],
                            "additionalProperties": False
                          }
                        }
                      },
                      "required": [
                        "scenario_number",
                        "answers"
                      ],
                      "additionalProperties": False
                    }
                  }
                },
                "required": [
                  "multiple_choice",
                  "short_answer",
                  "scenario_based"
                ],
                "additionalProperties": False
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
                          "minimum": 0
                        },
                        "maximum_score": {
                          "type": "integer",
                          "minimum": 0
                        },
                        "proficiency": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "minimum_score",
                        "maximum_score",
                        "proficiency"
                      ],
                      "additionalProperties": False
                    }
                  },
                  "critical_misconception_check": {
                    "type": "string",
                    "description": "A key conceptual distinction learners must understand."
                  }
                },
                "required": [
                  "levels",
                  "critical_misconception_check"
                ],
                "additionalProperties": False
              }
            },
            "required": [
              "title",
              "metadata",
              "learning_objectives",
              "sections",
              "answer_key",
              "scoring_guide"
            ],
            "additionalProperties": False
          },
          "strict": True
        }
    }
    
    @classmethod
    def has_minimum_word_count(cls, topic):
        return isinstance(topic, str) and len(topic.split()) >= cls.MIN_WORD_COUNT

    
    def post(self, request, format='json'):
        topic = request.data.get('topic')

        if not self.has_minimum_word_count(topic):
            return Response(
              data={ "message": "Topic must contain at least four words." },
              status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        client = OpenAI()
        model_result = client.responses.create(
            model="gpt-5.6",
            input=f"Create a skill assessment based on: {request.data}",
            text=self.ASSESSMENT_RESPONSE_SCHEMA
        )

        return Response(
            data=json.loads(model_result.output_text),
            status=status.HTTP_201_CREATED
        )
