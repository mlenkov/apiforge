"""Example: Yandex Metrika API with ApiForge."""

from apiforge import ApiForgeClient


def main():
    # Create client
    client = ApiForgeClient(config_path="yandex/metrika.json")

    # List available resources
    print("Available resources:")
    for name in client.list_resources():
        print(f"  - {name}")

    # Example: Get stats
    # response = client.request(
    #     "stats",
    #     params={
    #         "ids": 12345678,
    #         "metrics": "ym:s:visits,ym:s:pageviews",
    #         "date1": "2024-01-01",
    #         "date2": "2024-01-31",
    #     },
    # )
    # print(response.json())


if __name__ == "__main__":
    main()
