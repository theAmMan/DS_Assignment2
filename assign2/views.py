from flask import make_response, request, jsonify
from flask_expects_json import expects_json 
from jsonschema import ValidationError

from assign2 import app, redirector

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        return make_response(
            jsonify(
                {"status":"failure","message":error.description.message}
            ),
            400,
        )
    
    return error 

@app.route(rule = "/topics", methods = ["GET","POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"topic_name": {"type": "string"}},
        "required": ["topic_name"],
    },
    ignore_for=["GET"],
)
def topics():
    if request.method == "POST":
        topic_name = request.get_json(force = True)["topic_name"]
        try:
            redirector.add_topic(topic_name)
            return make_response(
                jsonify(
                    {
                        "status": "success",
                        "message": f"Topic '{topic_name}' created successfully.",
                    }
                ),
                200,
            )
        except Exception as e:
            print("Exception is " + str(e))
            return make_response(
                jsonify({"status": "failure", "message": str(e)}), 400
            )

    # If method is GET return all the topics
    try:
        topics = redirector.get_topics()
        return make_response(
            jsonify({"status": "success", "topics": topics}), 200
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/consumer/register", methods=["POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"topic_name": {"type": "string"}},
        "required": ["topic"],
    }
)
def register_consumer():
    """Register a consumer for a topic."""
    topic_name = request.get_json()["topic"]
    try:
        consumer_id = redirector.add_consumer(topic_name)
        return make_response(
            jsonify({"status": "success", "consumer_id": consumer_id}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/producer/register", methods=["POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"topic": {"type": "string"}},
        "required": ["topic"],
    }
)
def register_producer():
    """Register a producer for a topic."""
    topic_name = request.get_json()["topic"]
    try:
        producer_id = redirector.add_producer(topic_name)
        return make_response(
            jsonify({"status": "success", "producer_id": producer_id}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/producer/produce", methods=["POST"])
@expects_json(
    {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "producer_id": {"type": "int"},
            "message": {"type": "string"},
            "partition_no":{"type":"string"},
        },
        "required": ["topic", "producer_id", "message"],
    }
)
def produce():
    """Add a log to a topic."""
    topic_name = request.get_json()["topic"]
    producer_id = request.get_json()["producer_id"]
    message = request.get_json()["message"]
    partition_no = request.get_json(silent = True)["partition_no"]
    try:
        redirector.add_log(topic_name, producer_id, message,partition_no)
        return make_response(
            jsonify({"status": "success"}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/consumer/consume", methods=["GET"])
@expects_json(
    {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "consumer_id": {"type": "string"},
        },
        "required": ["topic", "consumer_id"],
    }
)
def consume():
    """Consume a log from a topic."""
    topic_name = request.get_json()["topic"]
    consumer_id = request.get_json()["consumer_id"]
    try:
        log = redirector.get_log(topic_name, consumer_id)
        if log is not None:
            return make_response(
                jsonify({"status": "success", "message": log}), 200
            )
        return make_response(
            jsonify(
                {"status": "failure", "message": "No logs available to pull."}
            ),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


@app.route(rule="/size", methods=["GET"])
@expects_json(
    {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "consumer_id": {"type": "string"},
        },
        "required": ["topic", "consumer_id"],
    }
)
def size():
    """Return the number of log messages in the requested topic for this consumer."""
    topic_name = request.get_json()["topic"]
    consumer_id = request.get_json()["consumer_id"]
    try:
        size = redirector.get_size(topic_name, consumer_id)
        return make_response(jsonify({"status": "success", "size": size}), 200)
    except Exception as e:
        return make_response(
            jsonify({"status": "failure", "message": str(e)}), 400
        )


#A link to add new partitions to a specific topic
@app.route(rule = "/partition", methods = ["GET"])
@expects_json(
    {
        "type":"object",
        "properties": {
            "topic":{"type":"string"},
            "producer_id":{"type":"int"},
        },
        "required": ["topic","producer_id"]
    }
)
def partition():
    """Create a new partition in the mentioned topic."""
    topic_name = request.get_json()["topic"]
    producer_id = request.get_json()["producer_id"]

    try:
        outcome = redirector.create_partition(topic_name, producer_id)
        return make_response(jsonify({"status":outcome}),200)
    except Exception as e:
        return make_response(
            jsonify({"status":"failure", "message": str(e)}), 400
        )
        