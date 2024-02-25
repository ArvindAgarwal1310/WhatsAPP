import logging
import json
from whatsapp_utils import (
    process_whatsapp_message,
    is_valid_whatsapp_message,
)


def handle_message(body):
    """
    Handle incoming webhook events from the WhatsApp API.

    This function processes incoming WhatsApp messages and other events,
    such as delivery statuses. If the event is a valid message, it gets
    processed. If the incoming payload is not a recognized WhatsApp event,
    an error is returned.

    Every message send will trigger 4 HTTP requests to your webhook: message, sent, delivered, read.

    Returns:
        response: A tuple containing a JSON response and an HTTP status code.
    """
    print(body)
    # logging.info(f"request body: {body}")

    # Check if it's a WhatsApp status update
    if (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("statuses")
    ):
        logging.info("Received a WhatsApp status update.")

    try:
        if is_valid_whatsapp_message(body):
            process_whatsapp_message(body)
            return {"status": "ok"}, 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                {"status": "error", "message": "Not a WhatsApp API event"},
                404,
            )
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return {"status": "error", "message": "Invalid JSON provided"}, 400


# Required webhook verifictaion for WhatsApp
def verify(body):
    # Parse params from the webhook verification request
    challenge = body["hub.challenge"]
    verify_token_received = body["hub.verify_token"]

    # Check if a token and mode were sent
    # Check the mode and token sent are correct
    if verify_token_received =="1310":
        # Respond with 200 OK and challenge token from the request
        logging.info("WEBHOOK_VERIFIED")
        return challenge, 200
    else:
        # Responds with '403 Forbidden' if verify tokens do not match
        logging.info("VERIFICATION_FAILED")
        return {"status": "error", "message": "Verification failed"}, 403




