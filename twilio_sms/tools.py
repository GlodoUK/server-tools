import json
import os


def twilio_error_codes_dict():
    file = os.path.join(
        os.path.dirname(__file__),
        "data/twilio-error-codes.json",
    )

    with open(file, "r") as f:
        data = json.load(f)

        return {f"twilio:{i.get('code')}": f"Twilio: {i.get('message')}" for i in data}
