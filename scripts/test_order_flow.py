import json
from dataclasses import dataclass

import requests


BASE_URL = "http://127.0.0.1:8001/webhook"
PHONE = "5491177777777"
PROFILE_NAME = "Matias"


@dataclass
class Step:
    message_id: str
    text: str


FLOW = [
    Step("msg-1", "hola"),
    Step("msg-2", "5"),
    Step("msg-3", "pizza"),
    Step("msg-4", "mitad y mitad"),
    Step("msg-5", "muzza y pepperoni"),
    Step("msg-6", "2"),
    Step("msg-7", "bebida"),
    Step("msg-8", "2"),
    Step("msg-9", "1"),
    Step("msg-10", "finalizar"),
    Step("msg-11", "Rodriguez Pena 1234, Muniz"),
    Step("msg-12", "confirmar"),
]


def build_payload(step: Step) -> dict:
    return {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": PHONE,
                                    "id": step.message_id,
                                    "text": {"body": step.text},
                                }
                            ],
                            "contacts": [
                                {
                                    "profile": {"name": PROFILE_NAME},
                                }
                            ],
                        }
                    }
                ]
            }
        ]
    }


def main() -> None:
    print("=== Aserrín Local Flow Test ===")
    print(f"POST {BASE_URL}")
    print(f"PHONE {PHONE}")
    print("")

    for index, step in enumerate(FLOW, start=1):
        payload = build_payload(step)

        print(f"[{index}] USER -> {step.text!r}")

        response = requests.post(
            BASE_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=10,
        )

        print(f"    HTTP {response.status_code}")
        print(f"    BODY {response.text}")
        print("")

        response.raise_for_status()

    print("=== Flow completed ===")


if __name__ == "__main__":
    main()