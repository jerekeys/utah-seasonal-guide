#!/usr/bin/env python3
"""Add the verified Drag Me to Hell fundraiser listing."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data.js"
LEDGER_PATH = ROOT / "research" / "drag-me-to-hell-2026-10-13.json"
PREFIX = "window.SITE_DATA = "
CHECKED = "2026-10-13"


def main() -> None:
    raw = DATA_PATH.read_text()
    assert raw.startswith(PREFIX) and raw.rstrip().endswith(";")
    data = json.loads(raw[len(PREFIX):].rstrip()[:-1])
    by_id = {item["id"]: item for item in data["events"]}

    event = {
        "id": "drag-me-to-hell-milk-2026",
        "Event / attraction": "Drag Me to Hell",
        "Region": "Salt Lake City",
        "Category": "Drag performance, Nightlife, Fundraiser, Costume contest",
        "First date": "2026-10-16",
        "2026 schedule": "Oct 16",
        "Times": "Doors 7 PM; show 8 PM; event ends 11 PM",
        "Price": "$13.57–$17.04 all-in",
        "Cost": "",
        "Age": "21+",
        "Intensity": "",
        "Location": "MILK+, 49 E Harvey Milk Boulevard, Salt Lake City",
        "Status": "Confirmed 2026",
        "Why / thoughts": "Local drag performers take on a villainous Halloween theme for a mutual-aid fundraiser, with dancers, specialty drinks and a costume contest. Proceeds support a local trans community member's top surgery.",
        "Website": "https://www.eventbrite.com/e/drag-me-to-hell-tickets-2001782502351",
        "Social profile": "",
        "Extra notes": "",
        "categories": ["Drag performance", "Nightlife", "Fundraiser", "Costume contest"],
        "sourceCategories": ["Drag performance", "Nightlife", "Fundraiser", "Costume contest"],
        "ghostCount": 0,
        "costCount": 2,
        "isWatch": False,
        "artKey": "nightlife",
        "socials": [],
        "photo": {
            "src": "assets/photos/drag-me-to-hell-2026.webp",
            "alt": "Illustrated moonlit graveyard promoting the Drag Me to Hell Halloween fundraiser.",
            "credit": "Utah March / Eventbrite",
            "creditUrl": "https://www.eventbrite.com/e/drag-me-to-hell-tickets-2001782502351",
            "sourceUrl": "https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F1193968074%2F2654191844571%2F1%2Foriginal.20260920-212826",
            "usageType": "official_organizer_promo",
            "caption": "Official event artwork",
            "reviewedOn": CHECKED,
            "width": 1200,
            "height": 740,
            "rightsNote": "Selected from the organizer's official ticket listing for editorial event-listing use.",
        },
        "sourceRegion": "Salt Lake City",
        "publicRegion": "Salt Lake Metro",
        "publicTypes": ["Live Music & Performance", "Nightlife & Parties", "Giving & Volunteering"],
        "sponsored": False,
        "holidays": ["Halloween", "Fall"],
        "primaryHoliday": "Halloween",
        "startDate": "2026-10-16",
        "endDate": "2026-10-16",
        "travelTier": "Core / easy day trip",
        "lastVerified": CHECKED,
        "qaFlags": "",
        "timezone": "America/Denver",
        "flags": ["21+", "Indoor", "Drag performance", "Costume contest", "Fundraiser", "Free parking"],
        "isFree": False,
        "rating": None,
        "occurrenceDates": ["2026-10-16"],
        "scheduleConfidence": "verified-dates",
        "scheduleNote": "The official ticket page lists the full 7–11 PM event window; the organizer artwork specifies a 7 PM door time and 8 PM show time.",
        "communities": ["LGBTQ+"],
        "theme": "halloween",
        "placeholder": "assets/art/seasonal/halloween-nightlife.svg",
        "notable_event": False,
        "seasons": ["Fall"],
        "accessibility": None,
        "researchEvidence": {
            "checkedOn": CHECKED,
            "sourceUrl": "https://www.eventbrite.com/e/drag-me-to-hell-tickets-2001782502351",
            "method": "Verified the live organizer listing, structured ticket offer, embedded organizer flyer and official venue site. No organizer-stated disability accommodation was found, so none is claimed.",
        },
    }

    if event["id"] in by_id:
        source_row = by_id[event["id"]].get("sourceRow")
        by_id[event["id"]].update(event)
        if source_row is not None:
            by_id[event["id"]]["sourceRow"] = source_row
    else:
        event["sourceRow"] = max((item.get("sourceRow", 0) for item in data["events"]), default=0) + 1
        data["events"].append(event)

    data["meta"]["updated"] = "October 13, 2026"
    data["meta"]["eventCount"] = len(data["events"])
    data["meta"]["confirmedCount"] = sum(not e.get("isWatch") for e in data["events"])
    data["meta"]["watchCount"] = sum(bool(e.get("isWatch")) for e in data["events"])
    data["meta"]["realImageCount"] = sum(bool(e.get("photo")) for e in data["events"])
    data["meta"]["localPhotoListings"] = data["meta"]["realImageCount"]
    data["meta"]["accessibilityListings"] = sum(bool(e.get("accessibility")) for e in data["events"])
    data["planningHorizon"]["from"] = CHECKED
    DATA_PATH.write_text(PREFIX + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

    ledger = {
        "checkedOn": CHECKED,
        "eventId": event["id"],
        "status": "confirmed",
        "decision": "Added to the public dataset; the live organizer listing provides a specific 2026 date, full time window, venue, age limit and active price range.",
        "ticketDepth": {
            "status": "on sale",
            "allInPriceRange": "$13.57–$17.04",
            "refundPolicy": "Eventbrite displays a custom policy and directs refund questions through the organizer.",
        },
        "accessibility": "No organizer-stated accommodation was found; the listing makes no accessibility claim.",
        "sources": [
            "https://www.eventbrite.com/e/drag-me-to-hell-tickets-2001782502351",
            "https://milkslc.com/",
        ],
    }
    LEDGER_PATH.parent.mkdir(exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {event['Event / attraction']}; {len(data['events'])} total events.")


if __name__ == "__main__":
    main()
