from mastodon import Mastodon
import os
from datetime import datetime, timezone, timedelta
import logging

def is_now_in_times(jst_times):
    # 現在時刻をJSTで取得して、分単位でマッチ判定
    now_utc = datetime.now(timezone.utc)
    # JST = UTC +9
    now_jst = now_utc.astimezone(timezone(timedelta(hours=9)))
    now_hm = now_jst.strftime("%H:%M")  # "09:00" 形式
    return now_hm in jst_times

def main():
    token = os.environ.get("MASTODON_TOKEN")
    if not token:
        raise ValueError("MASTODON_TOKEN is not set")
    
    # 定期投稿と決まった時刻用のメッセージ（例）
    regular_text = "定期投稿（10分ごと）"
    special_text = "決まった時刻の投稿です"

    # SCHEDULE_TIMES_JST は "09:00,17:00" 形式で env に入れる（Optional）
    times_env = os.environ.get("SCHEDULE_TIMES_JST", "")
    jst_times = [t.strip() for t in times_env.split(",") if t.strip()]

    mastodon = Mastodon(access_token=token, api_base_url="https://mastodon.social")

    # 現在 UTC 時刻の分単位で判定（GitHub Actions の cronはUTC）
    now_utc = datetime.now(timezone.utc)
    # regular: 10分ごと判定（UTCベースで実行されるため、cronと合わせるなら常にTrue）
    # ここではワークフローが10分ごとに起動する想定のため、regular は True。
    # 追加安全策：さらに分%10==0 をチェックすることも可。
    do_regular = now_utc.minute % 10 == 0

    # special: JSTでの決まった時刻かどうか
    do_special = False
    if jst_times:
        # JST 現在時刻
        now_jst = now_utc.astimezone(timezone(timedelta(hours=9)))
        hm = now_jst.strftime("%H:%M")
        do_special = hm in jst_times

    # 重複防止ロジック（例：直近の投稿と同じテキストならスキップ）
    recent = mastodon.account_statuses(mastodon.me()["id"], limit=5)
    recent_texts = {s['content'] if isinstance(s, dict) else s.content for s in recent}

    if do_special:
        if special_text not in recent_texts:
            mastodon.status_post(special_text)
            logging.info("Posted special message")
        else:
            logging.info("Skipping special post due to duplicate")
    elif do_regular:
        if regular_text not in recent_texts:
            mastodon.status_post(regular_text)
            logging.info("Posted regular message")
        else:
            logging.info("Skipping regular post due to duplicate")
    else:
        logging.info("No posting scheduled at this run")

    mastodon.status_post("Hello Mastodon World from GitHub Actions!")

if __name__ == "__main__":
    main()
