import argparse
import datetime as dt
import json
import sqlite3
import sys
import urllib.request

GITHUB_RELEASE_URL = "https://api.github.com/repos/videolan/vlc/releases/latest"
DEFAULT_DB_PATH = "vlc_updates.db"
PRODUCT_NAME = "vlc"


def fetch_latest_version(user_agent: str) -> str:
    request = urllib.request.Request(
        GITHUB_RELEASE_URL,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    tag_name = payload.get("tag_name")
    if not tag_name:
        raise ValueError("Fant ingen tag_name i GitHub-responsen.")
    return tag_name.lstrip("v")


def init_db(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            latest_version TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            source TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS state (
            product TEXT PRIMARY KEY,
            last_seen_version TEXT NOT NULL,
            last_checked_at TEXT NOT NULL
        )
        """
    )
    connection.commit()


def get_previous_version(connection: sqlite3.Connection, product: str) -> str | None:
    row = connection.execute(
        "SELECT last_seen_version FROM state WHERE product = ?",
        (product,),
    ).fetchone()
    return row[0] if row else None


def store_check(
    connection: sqlite3.Connection,
    product: str,
    latest_version: str,
    checked_at: str,
    source: str,
) -> None:
    connection.execute(
        """
        INSERT INTO checks (product, latest_version, checked_at, source)
        VALUES (?, ?, ?, ?)
        """,
        (product, latest_version, checked_at, source),
    )
    connection.execute(
        """
        INSERT INTO state (product, last_seen_version, last_checked_at)
        VALUES (?, ?, ?)
        ON CONFLICT(product)
        DO UPDATE SET last_seen_version = excluded.last_seen_version,
                      last_checked_at = excluded.last_checked_at
        """,
        (product, latest_version, checked_at),
    )
    connection.commit()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sjekker om VLC har en ny versjon og lagrer resultatet i SQLite.",
    )
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help="Sti til SQLite database.")
    parser.add_argument(
        "--product",
        default=PRODUCT_NAME,
        help="Navn på produktet (standard: vlc).",
    )
    parser.add_argument(
        "--user-agent",
        default="vlc-update-checker/1.0",
        help="User-Agent brukt for nettverkskall.",
    )
    parser.add_argument(
        "--mock-version",
        help="Bruk en fast versjon og hopp over nettverk (for testing).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    checked_at = dt.datetime.now(dt.timezone.utc).isoformat()
    source = "mock" if args.mock_version else "github"

    try:
        latest_version = args.mock_version or fetch_latest_version(args.user_agent)
    except Exception as exc:
        print(f"Feil ved henting av versjon: {exc}", file=sys.stderr)
        return 1

    with sqlite3.connect(args.db) as connection:
        init_db(connection)
        previous_version = get_previous_version(connection, args.product)
        store_check(connection, args.product, latest_version, checked_at, source)

    if previous_version is None:
        print(
            "Ingen tidligere versjon lagret. "
            f"Siste kjente versjon er nå {latest_version}."
        )
        return 0

    if latest_version != previous_version:
        print(
            "Oppdatering funnet! "
            f"Forrige versjon: {previous_version} -> Ny versjon: {latest_version}."
        )
        return 0

    print(f"Ingen oppdatering. Versjon er fortsatt {latest_version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
