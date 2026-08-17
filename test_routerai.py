import os
import requests


ROUTERAI_API_KEY = os.getenv("ROUTERAI_API_KEY")

URL = "https://routerai.ru/api/v1/models"


print("=" * 60)
print("ROUTERAI AVAILABLE MODELS")
print("=" * 60)


if not ROUTERAI_API_KEY:
    print("ERROR: ROUTERAI_API_KEY is not set.")
    raise SystemExit(1)


headers = {
    "Authorization": f"Bearer {ROUTERAI_API_KEY}",
    "Accept": "application/json",
}


try:

    response = requests.get(
        URL,
        headers=headers,
        timeout=60,
    )

except requests.RequestException as error:

    print("Connection error:")
    print(error)
    raise SystemExit(1)


print()
print("HTTP STATUS:", response.status_code)
print()


if not response.ok:

    print("RouterAI error:")
    print(response.text)
    raise SystemExit(1)


try:

    data = response.json()

except ValueError:

    print("Invalid JSON response:")
    print(response.text)
    raise SystemExit(1)


print("AVAILABLE MODELS:")
print()


models = data.get("data", [])


if not models:

    print(data)

else:

    for model in models:

        if isinstance(model, dict):

            print(
                model.get(
                    "id",
                    model
                )
            )

        else:

            print(model)


print()
print("=" * 60)
print("TOTAL MODELS:", len(models))
print("=" * 60)