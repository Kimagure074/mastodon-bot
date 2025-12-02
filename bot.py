from mastodon import Mastodon
import os

def main():
    token = os.environ.get("MASTODON_TOKEN")
    if not token:
        raise ValueError("MASTODON_TOKEN is not set")

    mastodon = Mastodon(
        access_token=token,
        api_base_url="https://mastodon.social"
    )

    mastodon.status_post("Hello Mastodon World from GitHub Actions!")

if __name__ == "__main__":
    main()
