
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
        "hashcat -m 0 -a 3 -1 ?u -2 -?l?u?d -3 ?d  https://gist.githubusercontent.com/apogiatzis/125d631fdadb92d918f892925103aa63/raw/49ee8707658665909e54aeca91b813326048b94b/colabohash_test.txt ?1?2?2?2?3?3?3",
        "https://discordapp.com/api/webhooks/735141229259522088/IHhSBz076hOVVOrmOC9GH-aicnwMWr86cLNEE-EjCTdCfRBgm_HgeStGwdOGYcfRI9J6",
    )

