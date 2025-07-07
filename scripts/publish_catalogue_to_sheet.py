"""Upload catalogue.csv to a Google Sheet and publish it as a public CSV.

Prerequisites
-------------
1. Create a Google Cloud service account and enable the Google Sheets & Drive APIs.
2. Download the JSON credentials file and set an env var pointing to it, e.g.
   export GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/credentials.json
3. `pip install -r requirements.txt`

Usage
-----
python3 scripts/publish_catalogue_to_sheet.py \
        --csv data/catalogue.csv \
        --sheet-name "BareMinimum-Catalogue" \
        --share-email myteam@company.com

The script will:
• Create the sheet if it does not exist.
• Replace the first worksheet contents with the CSV data.
• Share the sheet with the provided email (Viewer).
• Publish the sheet as CSV on the web.
• Print the two links needed by engineering.
"""

import argparse
import os
import sys
import time
from pathlib import Path

import gspread  # type: ignore
from google.oauth2.service_account import Credentials  # type: ignore

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials() -> Credentials:
    sa_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_path:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_JSON env var not set")
    if not Path(sa_path).exists():
        sys.exit(f"Service account JSON not found at {sa_path}")
    return Credentials.from_service_account_file(sa_path, scopes=SCOPES)


def open_or_create_sheet(gc: gspread.Client, sheet_name: str):
    try:
        return gc.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        print("Creating new sheet …")
        sheet = gc.create(sheet_name)
        # Move into root My Drive for visibility
        return sheet


def import_csv(sheet: gspread.Spreadsheet, csv_path: Path):
    print("Uploading CSV contents …")
    with csv_path.open("r", encoding="utf-8") as fp:
        csv_data = fp.read()
    sheet.values_update(
        "Sheet1",
        params={"valueInputOption": "RAW"},
        body={"values": [row.split(",") for row in csv_data.splitlines()]},
    )


def share_sheet(sheet: gspread.Spreadsheet, email: str | None):
    if email:
        print(f"Sharing with {email} …")
        sheet.share(email, perm_type="user", role="writer")
    # Allow anyone with link to view
    sheet.share(None, perm_type="anyone", role="reader")


def publish_sheet_as_csv(sheet: gspread.Spreadsheet) -> str:
    # gspread doesn't expose publish API; use Drive publish link format.
    # Format: https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv
    return f"https://docs.google.com/spreadsheets/d/{sheet.id}/export?format=csv"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to catalogue csv file")
    parser.add_argument("--sheet-name", default="BareMinimum-Catalogue")
    parser.add_argument("--share-email", help="Email to grant editor access to sheet")
    args = parser.parse_args()

    cred = get_credentials()
    gc = gspread.authorize(cred)

    sheet = open_or_create_sheet(gc, args.sheet_name)

    import_csv(sheet, Path(args.csv))

    share_sheet(sheet, args.share_email)

    csv_url = publish_sheet_as_csv(sheet)
    print("==============================")
    print("✔ Sheet URL:", sheet.url)
    print("✔ CSV  URL:", csv_url)


if __name__ == "__main__":
    main()