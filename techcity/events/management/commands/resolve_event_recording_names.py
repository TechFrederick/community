import json
import os

import requests
from django.core.management.base import BaseCommand

from techcity.events.models import Event, EventRecording


class Command(BaseCommand):
    help = "Attempt to resolve the names of event recordings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--openai-api-key",
            type=str,
            help="The OpenAI API key to use for fetching data"
            " (set in env OPENAI_API_KEY)",
            default=os.getenv("OPENAI_API_KEY"),
        )
        parser.add_argument(
            "--openai-model",
            type=str,
            help="The OpenAI model to use for fetching data",
            default="gpt-4o",
        )

    def handle(self, *args, openai_api_key: str, openai_model: str, **kwargs):
        recording = EventRecording.objects.first()

        events = Event.objects.filter(group=recording.group)

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json",
            },
            json=dict(
                model=openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": """
                            Resolve the name of this event recording
                            Return ID of the event it belongs to
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""
                            Recording: {recording.__dict__}

                            List of Events It may Belong To:
                            {[e.__dict__ for e in events]}
                        """,
                    },
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "event_schema",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "description": "ID of the event",
                                    "type": "number",
                                },
                                "name": {
                                    "description": "Name of the event",
                                    "type": "string",
                                },
                            },
                        },
                    },
                },
            ),
            timeout=15,
        )
        # Example:

        # {
        #   "id": "chatcmpl-AOmuw33UyJoiZlFBFZvwWe5Hy8nTf",
        #   "object": "chat.completion",
        #   "created": 1730471274,
        #   "model": "gpt-4o-2024-08-06",
        #   "choices": [
        #     {
        #       "index": 0,
        #       "message": {
        #         "role": "assistant",
        #         "content":
        # "{\"id\":75,\"name\":\"PDF Text Extraction (2nd Wed Talk)\"}",
        #         "refusal": null
        #       },
        #       "logprobs": null,
        #       "finish_reason": "stop"
        #     }
        #   ],
        #   "usage": {
        #     "prompt_tokens": 11248,
        #     "completion_tokens": 17,
        #     "total_tokens": 11265,
        #     "prompt_tokens_details": {
        #       "cached_tokens": 0
        #     },
        #     "completion_tokens_details": {
        #       "reasoning_tokens": 0
        #     }
        #   },
        #   "system_fingerprint": "fp_45cf54deae"
        # }

        response.raise_for_status()
        data = response.json()
        content = json.loads(data["choices"][0]["message"]["content"])

        event = Event.objects.get(id=content["id"])

        print(f"Recording: {recording.title=} {recording.published_at=}")
        print(f"Event: {event.name=} {event.start_at=}")
