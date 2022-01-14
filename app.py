import os

from discord_webhook import DiscordEmbed, DiscordWebhook
from flask import Flask, Response, request
from flask_bootstrap import Bootstrap

DISCORD_SENTRY_WEBHOOK = os.getenv("DISCORD_SENTRY_WEBHOOK")
SENTRY_SECRET = os.getenv("SENTRY_SECRET")

app = Flask(__name__)
Bootstrap(app)


def get_discord_color(level):
    if level == "debug":
        return "fbe14f"
    elif level == "info":
        return "2788ce"
    elif level == "warning":
        return "f18500"
    elif level == "fatal":
        return "d20f2a"
    else:
        return "e03e2f"


def get_stacktrace(event):
    if "stacktrace" in event:
        return event["stacktrace"]

    elif "exception" in event:
        exception = event["exception"]
        if exception.get("values"):
            return exception["values"][0].get("stacktrace")
    return None


def get_error_code_snippet(event):
    stacktrace = get_stacktrace(event)
    if not stacktrace:
        return None

    if not stacktrace.get("frames"):
        return None

    location = stacktrace["frames"][-1]
    if not location:
        return None

    return " {}\n>{}\n {}".format(
        "\n ".join(location.get("pre_context") or []),
        location.get("context_line"),
        "\n ".join(location.get("post_context") or []),
    )


import json


def handle_event(data):
    webhook = DiscordWebhook(url=DISCORD_SENTRY_WEBHOOK)
    data = json.loads(data)
    event = data["event"]

    snippet = get_error_code_snippet(event)
    location_text = ""
    language = ""

    if location := event.get("location"):
        location_text = "`{}`\n".format(location)
        language = location.split(".")[-1]

    snippet_text = "```{}\n{}\n```".format(language, snippet)

    embed = DiscordEmbed(
        title=event.get("title", "Sentry Event"),
        url=data["url"],
        description="{}{}".format(location_text, snippet_text),
        color=get_discord_color(data["level"]),
        footer={"text": event.get("environment")},
    )
    embed.set_timestamp(event["timestamp"])

    webhook.add_embed(embed)
    webhook.execute()


@app.route("/", methods=["POST"])
def webhook():
    if request.args.get("secret") != SENTRY_SECRET:
        return Response(None, status=401)
    handle_event(request.data)
    return Response(None, status=200)
