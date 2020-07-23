from colabohash import ColaboHash
from os import environ

def on_login_callback():
    print("Test on_login callback from __main__")

def on_run_callback():
    print("Test on_run callback from __main__")

if __name__ == "__main__":
    google_email = environ.get("COLABOHASH_GOOGLE_EMAIL")
    google_password = environ.get("COLABOHASH_GOOGLE_PASSWORD")

    colabohash = ColaboHash(
        google_email,
        google_password,
        headless=True,
        terminate_on_finish=True,
        keep_open=False,
    )

    colabohash.set_on_login_callback(on_login_callback)
    colabohash.set_on_run_callback(on_run_callback)
    
    colabohash.run_hashcat(
        "hashcat -w 4 -m 2500 --benchmark",
        "https://discordapp.com/api/webhooks/735141229259522088/IHhSBz076hOVVOrmOC9GH-aicnwMWr86cLNEE-EjCTdCfRBgm_HgeStGwdOGYcfRI9J6",
    )

