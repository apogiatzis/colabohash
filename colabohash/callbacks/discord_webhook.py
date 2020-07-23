import requests #dependency
import json

def callback(*args, **kwargs):
    url = kwargs["DISCORD_WEBHOOK_URL"]

    data = {}
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = kwargs["MESSAGE"]
    data["username"] = "Colabohash"

    #leave this out if you dont want an embed
    data["embeds"] = []
    embed = {}
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    embed["description"] = kwargs["EMBED_DESCRIPTION"]
    embed["title"] = kwargs["EMBED_TITLE"]
    data["embeds"].append(embed)

    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
