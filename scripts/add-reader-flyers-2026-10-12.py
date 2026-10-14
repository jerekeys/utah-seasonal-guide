#!/usr/bin/env python3
"""Add and correct listings discovered from reader-submitted flyers on Oct. 12, 2026."""

from __future__ import annotations

import copy
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data.js"
LEDGER_PATH = ROOT / "research" / "reader-flyers-2026-10-12.json"
PREFIX = "window.SITE_DATA = "
CHECKED = "2026-10-12"


def dates_between(start: str, end: str) -> list[str]:
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    return [(first + timedelta(days=i)).isoformat() for i in range((last - first).days + 1)]


def photo(src, alt, credit, credit_url, source_url, caption, width, height, *, usage="official_web_photo", note=None):
    return {
        "src": src,
        "alt": alt,
        "credit": credit,
        "creditUrl": credit_url,
        "sourceUrl": source_url,
        "usageType": usage,
        "caption": caption,
        "reviewedOn": CHECKED,
        "width": width,
        "height": height,
        "rightsNote": note or "Selected from an official organizer, venue or ticket page for editorial event-listing use.",
    }


PHOTOS = {
    "labyrinth": photo(
        "assets/photos/labyrinth-in-concert-2026.webp",
        "Sarah faces Jareth the Goblin King amid characters from Jim Henson's Labyrinth.",
        "Live at the Eccles",
        "https://live-at-the-eccles.com/events/labyrinth-in-concert",
        "https://live-at-the-eccles.com/storage/app/uploads/public/696/558/343/thumb_3183_1200_630_0_0_crop.jpg",
        "Official event image",
        1200,
        630,
    ),
    "mia": photo(
        "assets/photos/mia-asano-urban-lounge-2026.webp",
        "Electric violinist Mia Asano performs under blue and violet stage lights.",
        "24tix / JRC Events",
        "https://www.24tix.com/events/71022114245",
        "https://www.24tix.com/events/f6uqqncjbnaibokrwy5xuq5a4i/image",
        "Official ticket image",
        720,
        481,
    ),
    "witchy": photo(
        "assets/photos/witchy-woman-2026.webp",
        "Marrlo Suzzanne and The Galaxxy Band perform in dramatic red stage lighting.",
        "24tix / JRC Events",
        "https://www.24tix.com/events/emrohz624zcqzlbltejw7qpaay",
        "https://www.24tix.com/events/emrohz624zcqzlbltejw7qpaay/image",
        "Official ticket image",
        720,
        481,
    ),
    "deep_love": photo(
        "assets/photos/deep-love-ghostly-rock-opera-2026.webp",
        "Two Deep Love performers sing beneath theatrical red and white lights.",
        "Deep Love: A Ghostly Rock Opera",
        "https://www.deeploveopera.com/",
        "https://images.squarespace-cdn.com/content/v1/53755ed2e4b021fbdcea05ea/7521547f-e4a3-48e8-9664-3e37a3d7c642/Untitled%2Bdesign%2B%281%29.png",
        "Official production photo",
        1080,
        1080,
    ),
    "bongripper": photo(
        "assets/photos/bongripper-aces-high-halloween-2026.webp",
        "Colorful illustrated Halloween concert poster for Bongripper, Past the Light, Gout and Redskin.",
        "Aces High Saloon",
        "https://aceshighsaloon.com/event/bongripper-past-the-light-tba/",
        "https://aceshighsaloon.com/event/bongripper-past-the-light-tba/",
        "Organizer flyer photographed by a site contributor",
        864,
        1536,
        usage="organizer_promo_flyer",
        note="Photographed from the organizer's printed promotional flyer and provided for editorial event-listing use.",
    ),
    "craft": photo(
        "assets/photos/craft-club-hocus-pocus-book-2026.webp",
        "Two handmade brown spellbooks with sculpted eyes and gold stitching beside workshop details.",
        "Craft Club SLC",
        "https://www.craftclubslc.com/events/hocus-pocus-book",
        "https://cdn.prod.website-files.com/677aecfbee49d7a7b6576833/6ac170354b73a87c9596524b_Orange%20and%20Black%20Halloween%20Party%20Flyer.png",
        "Official workshop image",
        1080,
        1080,
    ),
    "ken": photo(
        "assets/photos/kens-pumpkin-patch-2026.webp",
        "Rows of glowing, hand-carved foam pumpkins fill Ken's front-yard display after dark.",
        "Ken's Pumpkin Patch",
        "https://www.facebook.com/kenspumpkinpatch/videos/1755934818946416/",
        "https://www.facebook.com/kenspumpkinpatch/videos/1755934818946416/",
        "Official organizer video still",
        900,
        1600,
    ),
}


def event(
    *, event_id, name, region, public_region, categories, public_types, start,
    schedule, times, price, age, location, description, website, holidays,
    end=None, occurrences=None, flags=None, is_free=False, cost_count=0,
    art_key="community", theme=None, communities=None, notable=False,
    image=None, accessibility=None, schedule_note="", extra_notes="",
    social_profile="", socials=None,
):
    primary = holidays[0]
    seasons = [s for s in ("Fall", "Winter", "Spring", "Summer") if s in holidays]
    theme_key = theme or primary.lower().replace(" ", "-")
    generic_key = art_key if art_key in {"active", "community", "food", "market", "nightlife", "performance", "workshop"} else "community"
    seasonal = ROOT / "assets" / "art" / "seasonal" / f"{theme_key}-{art_key}.svg"
    placeholder = f"assets/art/seasonal/{theme_key}-{art_key}.svg" if seasonal.exists() else f"assets/art/{generic_key}.svg"
    return {
        "id": event_id,
        "Event / attraction": name,
        "Region": region,
        "Category": ", ".join(categories),
        "First date": start,
        "2026 schedule": schedule,
        "Times": times,
        "Price": price,
        "Cost": "",
        "Age": age,
        "Intensity": "",
        "Location": location,
        "Status": "Confirmed 2026",
        "Why / thoughts": description,
        "Website": website,
        "Social profile": social_profile,
        "Extra notes": extra_notes,
        "categories": categories,
        "sourceCategories": categories,
        "ghostCount": 0,
        "costCount": cost_count,
        "isWatch": False,
        "artKey": art_key,
        "socials": socials or [],
        "photo": copy.deepcopy(image),
        "sourceRegion": region,
        "publicRegion": public_region,
        "publicTypes": public_types,
        "sponsored": False,
        "holidays": holidays,
        "primaryHoliday": primary,
        "startDate": start,
        "endDate": end or start,
        "travelTier": "Core / easy day trip",
        "lastVerified": CHECKED,
        "qaFlags": "",
        "timezone": "America/Denver",
        "flags": flags or [],
        "isFree": is_free,
        "rating": None,
        "occurrenceDates": occurrences or [start],
        "scheduleConfidence": "verified-dates",
        "scheduleNote": schedule_note,
        "communities": communities or [],
        "theme": theme_key,
        "placeholder": placeholder,
        "notable_event": notable,
        "seasons": seasons or ["Fall"],
        "accessibility": accessibility,
        "researchEvidence": {
            "checkedOn": CHECKED,
            "sourceUrl": website,
            "method": "Read the submitted flyer, then verified the organizer, venue and ticket details at least one level deeper.",
        },
    }


def main():
    raw = DATA_PATH.read_text()
    assert raw.startswith(PREFIX) and raw.rstrip().endswith(";")
    data = json.loads(raw[len(PREFIX):].rstrip()[:-1])
    by_id = {item["id"]: item for item in data["events"]}
    next_source_row = max((item.get("sourceRow", 0) for item in data["events"]), default=0) + 1

    new_events = [
        event(
            event_id="mia-asano-urban-lounge-2026",
            name="Mia Asano — 2026 West Coast Tour",
            region="Salt Lake City",
            public_region="Salt Lake Metro",
            categories=["Live music", "Rock / Alternative", "Nightlife"],
            public_types=["Live Music & Performance", "Nightlife & Parties"],
            start="2026-10-13",
            schedule="Oct 13",
            times="Doors 7 PM; show 8 PM",
            price="$28.64 all-in general admission; VIP sales closed",
            age="21+",
            location="The Urban Lounge, 241 S 500 E, Salt Lake City",
            description="Electric violinist Mia Asano brings an arena-sized blend of classical technique, metal and cinematic rock to an intimate club stage.",
            website="https://www.24tix.com/events/71022114245",
            holidays=["Fall"],
            flags=["21+", "Indoor", "General admission", "ADA ticket selection"],
            cost_count=2,
            art_key="nightlife",
            theme="fall",
            image=PHOTOS["mia"],
            accessibility={"summary": "The official ticket page offers ADA ticket selection; contact 24tix or the venue for seating details."},
            social_profile="https://www.instagram.com/miaasanomusic/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/miaasanomusic/"}],
        ),
        event(
            event_id="jim-hensons-labyrinth-in-concert-kingsbury-2026",
            name="Jim Henson's Labyrinth: In Concert",
            region="Salt Lake City",
            public_region="Salt Lake Metro",
            categories=["Film with live music", "Concert", "Fantasy / Fandom"],
            public_types=["Live Music & Performance", "Community & Culture"],
            start="2026-10-14",
            schedule="Oct 14",
            times="7:30 PM",
            price="$48.75–$80.85 all-in; every patron needs a ticket",
            age="All ages; every patron needs a ticket",
            location="Kingsbury Hall, 1395 E Presidents Circle, Salt Lake City",
            description="Watch the full 1986 fantasy film in HD while a live band performs David Bowie and Trevor Jones' soundtrack in sync with the movie. Costumes, singing along and cheering are welcome.",
            website="https://live-at-the-eccles.com/events/labyrinth-in-concert",
            holidays=["Halloween", "Fall"],
            flags=["All ages", "Indoor", "Costumes welcome", "Live score", "Accessible seating"],
            cost_count=3,
            art_key="performance",
            theme="halloween",
            image=PHOTOS["labyrinth"],
            notable=True,
            accessibility={
                "summary": "Mobility-device access uses the southeast entrance. Accessible seating is arranged through the box office; free assistive-listening devices are available, and ASL interpretation can be requested at least five business days ahead. Captioning and audio description may be available with advance notice.",
            },
        ),
        event(
            event_id="deep-love-ghostly-rock-opera-2026",
            name="Deep Love: A Ghostly Rock Opera",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            categories=["Rock opera", "Theater", "Halloween performance"],
            public_types=["Live Music & Performance", "Haunts & Scares"],
            start="2026-10-29",
            end="2026-10-30",
            occurrences=["2026-10-29", "2026-10-30"],
            schedule="Oct 29–30",
            times="7 PM both nights; about 2 hours including intermission",
            price="$40 listed by the production; ticketing fees may apply",
            age="All ages; infants held by an adult do not need a ticket",
            location="Mid-Valley Performing Arts Center, 2525 Taylorsville Blvd, Taylorsville",
            description="Four singers and a live band tell a gothic ghost story entirely through rock music, without spoken dialogue. The fully staged production invites audience energy, and funeral attire is recommended.",
            website="https://www.saltlakecountyarts.org/events/deep-love-a-ghostly-rock-opera/",
            holidays=["Halloween", "Fall"],
            flags=["All ages", "Indoor", "Funeral attire encouraged", "Two performances", "Accessible seating"],
            cost_count=2,
            art_key="performance",
            theme="halloween",
            image=PHOTOS["deep_love"],
            notable=True,
            accessibility={
                "summary": "The venue offers wheelchair and companion seating, curb-to-seat assistance, free assistive-listening devices, sensory supports and accessible restrooms. ASL interpretation and captioning can be requested through ArtTix at least two weeks ahead.",
            },
            schedule_note="The official production and venue calendars both confirm Oct. 29–30, 2026; one paragraph on the venue page still carries an uncorrected 2027 year.",
        ),
        event(
            event_id="bongripper-aces-high-halloween-2026",
            name="Bongripper Halloween at Aces High",
            region="Salt Lake City",
            public_region="Salt Lake Metro",
            categories=["Live music", "Heavy metal", "Halloween nightlife"],
            public_types=["Live Music & Performance", "Nightlife & Parties"],
            start="2026-10-31",
            schedule="Oct 31",
            times="Venue calendar begins at 6 PM; the event flyer advertises 7 PM",
            price="$35 advance; $40 day of show",
            age="21+",
            location="Aces High Saloon, 1588 S State Street, Salt Lake City",
            description="Instrumental doom band Bongripper headlines a Halloween-night bill with Past the Light, Gout and Redskin at Salt Lake's heavy-music bar.",
            website="https://aceshighsaloon.com/event/bongripper-past-the-light-tba/",
            holidays=["Halloween", "Fall"],
            flags=["21+", "Indoor", "Halloween night", "Standing-room concert"],
            cost_count=2,
            art_key="nightlife",
            theme="halloween",
            image=PHOTOS["bongripper"],
            schedule_note="The venue calendar currently opens the listing at 6 PM; the printed event flyer says 7 PM. Use the ticket page as the final day-of check.",
        ),
        event(
            event_id="craft-club-hocus-pocus-book-2026",
            name="Hocus Pocus Book — Craft Club SLC",
            region="Salt Lake City",
            public_region="Salt Lake Metro",
            categories=["Craft workshop", "Social meetup", "Halloween"],
            public_types=["Workshops & Learning", "Community & Culture"],
            start="2026-10-13",
            schedule="Oct 13",
            times="6:30–8:30 PM",
            price="$40; supplies included; sold out",
            age="Adults; the organizer does not post a minimum age",
            location="The Tasting Room, Salt Lake City",
            description="Build a display-ready, eye-and-stitch spellbook inspired by Hocus Pocus during a guided two-hour craft night designed for making alongside new people.",
            website="https://www.craftclubslc.com/events/hocus-pocus-book",
            holidays=["Halloween", "Fall"],
            flags=["Sold out", "Reservation required", "Indoor", "Supplies included"],
            cost_count=2,
            art_key="workshop",
            theme="halloween",
            communities=["Women-centered"],
            image=PHOTOS["craft"],
            social_profile="https://www.instagram.com/craftclubslc/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/craftclubslc/"}],
        ),
        event(
            event_id="kens-pumpkin-patch-farmington-2026",
            name="Ken's Pumpkin Patch",
            region="Davis County",
            public_region="Davis County",
            categories=["Neighborhood display", "Pumpkin display", "Food-drive collection"],
            public_types=["Lights & Displays", "Community & Culture", "Giving & Volunteering"],
            start="2026-10-12",
            end="2026-10-31",
            occurrences=dates_between("2026-10-12", "2026-10-31"),
            schedule="Nightly through Oct 31; verified active Oct 12",
            times="Dusk–10 PM",
            price="Free; nonperishable food donations for the Bountiful Food Pantry are appreciated",
            age="All ages",
            location="1288 S Cannon Drive, Farmington",
            description="Nearly 500 hand-carved foam pumpkins glow across a front-yard display, with familiar characters, intricate portraits and optical illusions to spot after dark.",
            website="https://www.facebook.com/kenspumpkinpatch/videos/1755934818946416/",
            holidays=["Halloween", "Fall"],
            flags=["Free admission", "All ages", "Outdoor", "Nightly", "Food donations encouraged", "Residential display"],
            is_free=True,
            cost_count=1,
            art_key="community",
            theme="halloween",
            image=PHOTOS["ken"],
            social_profile="https://www.instagram.com/kenspumpkinpatch/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/kenspumpkinpatch/"}],
        ),
    ]

    for item in new_events:
        if item["id"] in by_id:
            source_row = by_id[item["id"]].get("sourceRow")
            by_id[item["id"]].update(item)
            if source_row is not None:
                by_id[item["id"]]["sourceRow"] = source_row
        else:
            item["sourceRow"] = next_source_row
            next_source_row += 1
            data["events"].append(item)
            by_id[item["id"]] = item

    # Correct the existing ticket-depth gap and replace its generic venue photo.
    witchy = by_id["witchy-woman-halloween-special"]
    witchy.update({
        "Event / attraction": "Witchy Woman — A Halloween Drag Concert",
        "Times": "Doors 7 PM; show 8 PM",
        "Price": "$24.48 all-in general admission; six-person booth $113.01 and does not include admission",
        "Why / thoughts": "Marrlo Suzzanne and The Galaxxy Band turn songs by Heart, Pat Benatar, Journey, the Eagles and more into a live-band drag concert of witches, dark glamour and rock vocals.",
        "Website": "https://www.24tix.com/events/emrohz624zcqzlbltejw7qpaay",
        "photo": copy.deepcopy(PHOTOS["witchy"]),
        "lastVerified": CHECKED,
        "flags": ["21+", "Indoor", "Live band", "Drag performance", "ADA ticket selection"],
        "accessibility": {"summary": "The official ticket page offers ADA ticket selection; contact 24tix or Metro Music Hall for seating details."},
        "researchEvidence": {
            "checkedOn": CHECKED,
            "sourceUrl": "https://www.24tix.com/events/emrohz624zcqzlbltejw7qpaay",
            "method": "Verified both performance dates, then opened the Oct. 22 ticket page for door time, show time, age limit and current all-in prices.",
        },
    })

    # The submitted Weeb Streets flyer independently confirms the existing record.
    weeb = by_id["weeb-streets-3rd-annual-halloween-cosplay-party"]
    weeb["lastVerified"] = CHECKED
    weeb["researchEvidence"] = {
        "checkedOn": CHECKED,
        "sourceUrl": "https://weebstreets.com/",
        "method": "Matched the submitted organizer flyer against the official event page, including date, hours, 18+ limit, venue and advance/door prices.",
    }

    data["meta"]["updated"] = "October 12, 2026"
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
        "input": "Nine reader-submitted flyer and ad images",
        "confirmedNewIds": [e["id"] for e in new_events],
        "correctedExistingIds": ["witchy-woman-halloween-special", "weeb-streets-3rd-annual-halloween-cosplay-party"],
        "notAdded": [
            {"image": "IMG_0210.jpeg", "name": "The Missionary Position", "reason": "Book advertisement with no dated public event."},
        ],
        "result": {
            "newEvents": len(new_events),
            "correctedEvents": 2,
            "totalEvents": len(data["events"]),
            "confirmedEvents": data["meta"]["confirmedCount"],
            "realImageListings": data["meta"]["realImageCount"],
        },
        "sources": sorted({e["Website"] for e in new_events} | {
            "https://www.24tix.com/events/emrohz624zcqzlbltejw7qpaay",
            "https://weebstreets.com/",
        }),
    }
    LEDGER_PATH.parent.mkdir(exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {len(new_events)} events and corrected 2 existing listings; {len(data['events'])} total events.")


if __name__ == "__main__":
    main()
