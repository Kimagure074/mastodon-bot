from mastodon import Mastodon
import os
from datetime import datetime, timezone, timedelta  # ← timedelta を import

def main():
    token = os.environ.get("MASTODON_TOKEN")
    if not token:
        raise ValueError("MASTODON_TOKEN is not set")

    mastodon = Mastodon(access_token=token, api_base_url="https://mastodon.social")

    # JST = UTC + 9 hours
    now_utc = datetime.now(timezone.utc)
    now_jst = now_utc + timedelta(hours=9)   # ← ここで timedelta が使える

    print("now_jst:", now_jst.strftime("%Y-%m-%d %H:%M:%S"))
    mastodon.status_post("Hello Mastodon World from GitHub Actions!")

if __name__ == "__main__":
    main()
