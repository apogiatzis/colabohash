from colabohash import ColaboHash
from os import environ

if __name__ == "__main__":
    google_email = environ.get("COLABOHASH_GOOGLE_EMAIL")
    google_password = environ.get("COLABOHASH_GOOGLE_PASSWORD")

    colabohash = ColaboHash(
        google_email,
        google_password,
        headless=True,
        terminate_on_finish=True,
        keep_open=False
    )
    colabohash.run_hashcat(
        "hashcat -w 4 -m 2500 --benchmark",
        "https://discordapp.com/api/webhooks/735141229259522088/IHhSBz076hOVVOrmOC9GH-aicnwMWr86cLNEE-EjCTdCfRBgm_HgeStGwdOGYcfRI9J6",
    )

