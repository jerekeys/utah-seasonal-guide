#!/usr/bin/env python3
"""Add and enrich the October–November 2026 Día de los Muertos listings."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data.js"
PREFIX = "window.SITE_DATA = "
CHECKED = "2026-10-08"


def photo(src, alt, credit, credit_url, source_url, caption, width, height):
    return {
        "src": src,
        "alt": alt,
        "credit": credit,
        "creditUrl": credit_url,
        "sourceUrl": source_url,
        "usageType": "official_web_photo",
        "caption": caption,
        "reviewedOn": CHECKED,
        "width": width,
        "height": height,
        "rightsNote": "Selected from an official organizer or venue website for editorial event-listing use.",
    }


PARK_CITY_PHOTO = photo(
    "assets/photos/dia-de-los-muertos-park-city-2026.webp",
    "A colorful Día de los Muertos altar decorated with marigolds, candles, photographs, crafts and sugar skulls beneath papel picado banners.",
    "Arts Council of Park City & Summit County",
    "https://www.pcscarts.org/dia-de-los-muertos",
    "https://images.squarespace-cdn.com/content/v1/673cdf69b75fe402092de85e/0d1ff941-e346-476e-8221-16aaf4ef8d16/4A3A8880.jpg",
    "Organizer photo",
    1067,
    1600,
)

MILLCREEK_PHOTO = photo(
    "assets/photos/millcreek-common-dia-2026.webp",
    "Millcreek Common’s illuminated plaza and skating loop at night.",
    "Millcreek Common",
    "https://millcreekcommon.org/",
    "https://images.squarespace-cdn.com/content/v1/654a9a06484490657b8414bc/7dc87002-d739-4488-83b1-c872972d6c00/DJI_20241207181331_0018_D.jpg?format=1500w",
    "Venue photo",
    1500,
    840,
)

OQUIRRH_PHOTO = photo(
    "assets/photos/dia-de-los-muertos-oquirrh-2026.webp",
    "A vibrant Día de los Muertos altar with colorful decorations, photos, flowers and sugar skulls.",
    "Oquirrh Recreation and Parks District",
    "https://www.oquirrhrec.gov/dia-de-los-muertos-c5316ac",
    "https://streamline.imgix.net/9be7d580-ee10-457e-b190-a4c6692be86c/31fc5cec-3c8c-4404-879a-d224e21d8618/20251105_8238.png",
    "Organizer photo",
    1600,
    1066,
)

UNION_STATION_PHOTO = photo(
    "assets/photos/dia-de-los-muertos-union-station-2026.webp",
    "Historic Ogden Union Station and its front garden.",
    "Ogden Union Station",
    "https://theunionstation.org/",
    "https://theunionstation.org/wp-content/uploads/UnionStation.jpg",
    "Venue photo",
    1025,
    342,
)


def event(
    *,
    event_id,
    name,
    region,
    public_region,
    category,
    public_types,
    date,
    end_date=None,
    occurrence_dates=None,
    schedule,
    times,
    price,
    age,
    location,
    description,
    website,
    flags,
    is_free=False,
    cost_count=0,
    art_key="community",
    travel_tier="Core / easy day trip",
    notable=False,
    image=None,
    social_profile="",
    socials=None,
    extra_notes="",
    accessibility=None,
    holidays=None,
    schedule_note="",
):
    categories = [category]
    result = {
        "Event / attraction": name,
        "Region": region,
        "Category": category,
        "First date": date,
        "2026 schedule": schedule,
        "Times": times,
        "Price": price,
        "Cost": "",
        "Age": age,
        "Intensity": "👻",
        "Location": location,
        "Status": "Confirmed 2026",
        "Why / thoughts": description,
        "Website": website,
        "Social profile": social_profile,
        "Extra notes": extra_notes,
        "id": event_id,
        "categories": categories,
        "ghostCount": 0,
        "costCount": cost_count,
        "isWatch": False,
        "artKey": art_key,
        "socials": socials or [],
        "photo": image,
        "sourceRegion": region,
        "publicRegion": public_region,
        "sourceCategories": categories,
        "publicTypes": public_types,
        "sponsored": False,
        "holidays": holidays or ["Día de los Muertos", "Fall"],
        "primaryHoliday": "Día de los Muertos",
        "startDate": date,
        "endDate": end_date or date,
        "travelTier": travel_tier,
        "lastVerified": CHECKED,
        "qaFlags": "",
        "timezone": "America/Denver",
        "sourceRow": 0,
        "flags": flags,
        "isFree": is_free,
        "rating": None,
        "occurrenceDates": occurrence_dates or [date],
        "scheduleConfidence": "verified-dates",
        "scheduleNote": schedule_note,
        "communities": ["Mexican / Latino"],
        "theme": "dayofdead",
        "placeholder": "assets/art/seasonal/dayofdead-community.svg",
        "evidence": {
            "schedule": {
                "url": website,
                "method": "Organizer, venue or official ticket page",
                "checked": CHECKED,
            }
        },
        "notable_event": notable,
        "seasons": ["Fall"],
    }
    if accessibility:
        result["accessibility"] = accessibility
    return result


def main():
    raw = DATA_PATH.read_text()
    assert raw.startswith(PREFIX) and raw.rstrip().endswith(";")
    data = json.loads(raw[len(PREFIX):].rstrip()[:-1])

    new_events = [
        event(
            event_id="dia-de-los-muertos-ogden-union-station",
            name="Día de los Muertos — Ogden Union Station",
            region="Ogden / Weber",
            public_region="Ogden, Weber & Morgan",
            category="Community Festival, Market / Shopping, Cultural / Día",
            public_types=["Community & Culture", "Markets & Shopping", "Live Music & Performance"],
            date="2026-10-24",
            schedule="Oct 24",
            times="1–7 PM",
            price="Free admission; food and shopping extra",
            age="all ages",
            location="Ogden Union Station, 2501 Wall Avenue, Ogden",
            description="A full afternoon of remembrance and celebration with a community altar, live music, dancers, a craft market, car show and food at historic Union Station.",
            website="https://culturaandcraft.com/",
            social_profile="https://www.instagram.com/culturaandcraft/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/culturaandcraft/"}],
            flags=["Free admission", "Community altar", "Food and vendors", "All ages"],
            is_free=True,
            cost_count=1,
            art_key="market",
            notable=True,
            image=UNION_STATION_PHOTO,
        ),
        event(
            event_id="dia-de-los-muertos-ofrenda-millcreek-common",
            name="Día de los Muertos Ofrenda — Millcreek Common",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Art / Exhibit, Cultural / Día",
            public_types=["Community & Culture", "Workshops & Learning"],
            date="2026-10-19",
            end_date="2026-10-31",
            occurrence_dates=[f"2026-10-{day:02d}" for day in range(19, 32)],
            schedule="Oct 19–31",
            times="Daily 9 AM–5 PM",
            price="Free",
            age="all ages",
            location="Grandview, sixth floor of Millcreek City Hall, 1330 E Chambers Avenue, Millcreek",
            description="Visit a community ofrenda in the Grandview event space, with photographs, marigolds and objects honoring people who have died.",
            website="https://millcreekcommon.org/",
            social_profile="https://www.instagram.com/millcreekcommon/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/millcreekcommon/"}],
            flags=["Free admission", "Indoor", "Community altar", "All ages"],
            is_free=True,
            cost_count=1,
            image=MILLCREEK_PHOTO,
        ),
        event(
            event_id="dia-de-los-muertos-workshops-millcreek-common",
            name="Día de los Muertos Workshops — Millcreek Common",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Workshop / Class, Cultural / Día",
            public_types=["Workshops & Learning", "Community & Culture"],
            date="2026-10-23",
            end_date="2026-10-28",
            occurrence_dates=["2026-10-23", "2026-10-27", "2026-10-28"],
            schedule="Oct 23, 27 and 28",
            times="6:30–8:30 PM",
            price="Registration details not posted",
            age="Audience details not posted",
            location="Millcreek Common, 1330 E Chambers Avenue, Millcreek",
            description="Three evening workshops explore mini altars, alebrijes and sugar-skull traditions through hands-on artmaking.",
            website="https://millcreekcommon.org/",
            flags=["Three workshop dates", "Hands-on art", "Registration may be required"],
            art_key="workshop",
            image=MILLCREEK_PHOTO,
        ),
        event(
            event_id="an-evening-with-la-catrina-millcreek",
            name="An Evening with La Catrina — Millcreek Common",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Film / Theater / Performance, Cultural / Día",
            public_types=["Live Music & Performance", "Community & Culture"],
            date="2026-10-30",
            schedule="Oct 30",
            times="Shows at 7:30 and 9 PM",
            price="Admission details not posted",
            age="Audience details not posted",
            location="Grandview at Millcreek Common, 1330 E Chambers Avenue, Millcreek",
            description="A staged evening centered on La Catrina, the elegant skeletal figure closely associated with modern Día de los Muertos imagery.",
            website="https://millcreekcommon.org/",
            flags=["Two performances", "Indoor"],
            art_key="performance",
            image=MILLCREEK_PHOTO,
        ),
        event(
            event_id="gran-dia-de-los-muertos-millcreek-common",
            name="Gran Día de los Muertos Celebration & La Catrina Parade",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Community Festival, Active / Outdoors / Sports, Cultural / Día",
            public_types=["Community & Culture", "Active & Outdoors", "Live Music & Performance"],
            date="2026-10-31",
            schedule="Oct 31",
            times="5–10 PM; free face painting during the first two hours",
            price="Free admission and skating; skate rentals $5",
            age="all ages",
            location="Millcreek Common Plaza, 1330 E Chambers Avenue, Millcreek",
            description="Millcreek Common closes its Día de los Muertos series with a La Catrina parade, face painting, costumes, prizes and the season’s final roller-skating night.",
            website="https://www.millcreekut.gov/Calendar.aspx?EID=2413&calType=0&day=8&month=10&year=2026",
            social_profile="https://www.instagram.com/millcreekcommon/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/millcreekcommon/"}],
            flags=["Free admission", "Free skating", "$5 rentals", "Costumes encouraged", "Outdoor"],
            is_free=True,
            cost_count=1,
            art_key="community",
            image=MILLCREEK_PHOTO,
            holidays=["Día de los Muertos", "Halloween", "Fall"],
        ),
        event(
            event_id="dia-de-los-muertos-thanksgiving-point",
            name="Día de los Muertos — Thanksgiving Point",
            region="Utah County",
            public_region="Utah County",
            category="Community Festival, Cultural / Día",
            public_types=["Community & Culture", "Live Music & Performance", "Markets & Shopping"],
            date="2026-10-24",
            schedule="Oct 24",
            times="10 AM–8 PM; Catrina and Catrin contest at 3:30 PM",
            price="$16 adults; $5 ages 3–12; ages 2 and younger free; members save 10%",
            age="all ages",
            location="Show Barn at Thanksgiving Point, 2476 Sycamore Lane, Lehi",
            description="A daylong celebration with community ofrendas, mariachi, singers, storytelling, vendors and a Catrina and Catrin costume contest.",
            website="https://thanksgivingpoint.org/events/dia-de-muertos/",
            social_profile="https://www.instagram.com/thanksgivingpoint/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/thanksgivingpoint/"}],
            flags=["Children 2 and younger free", "Member discount", "Costume contest", "Food and vendors", "All ages"],
            cost_count=2,
            art_key="community",
            notable=True,
        ),
        event(
            event_id="dia-de-los-muertos-park-city",
            name="Día de los Muertos — Park City",
            region="Summit / Wasatch",
            public_region="Park City & Wasatch Back",
            category="Community Festival, Art / Exhibit, Cultural / Día",
            public_types=["Community & Culture", "Workshops & Learning"],
            date="2026-11-01",
            schedule="Nov 1",
            times="2–5 PM",
            price="Free",
            age="all ages",
            location="CREATE PC, 1500 Kearns Boulevard, Suite F110, Park City",
            description="Gather around a public ofrenda with tamales, pan de muerto, face painting, crafts and Catrinas. Community members may contribute photographs and mementos beginning October 20.",
            website="https://www.pcscarts.org/dia-de-los-muertos",
            social_profile="https://www.instagram.com/pcscarts/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/pcscarts/"}],
            flags=["Free admission", "Community altar", "Food", "All ages", "ASL interpreting"],
            is_free=True,
            cost_count=1,
            travel_tier="Extended day trip",
            image=PARK_CITY_PHOTO,
            accessibility={
                "summary": "ASL interpreting, Spanish translation, large-print materials and sensory kits are available.",
                "url": "https://www.pcscarts.org/accessibility-accommodations",
                "tone": "positive",
            },
            extra_notes="ASL interpreting, Spanish translation, large-print materials and sensory kits are available. For accommodation questions, contact emma@pcscarts.org.",
        ),
        event(
            event_id="michelada-music-festival-dia-de-los-muertos-edition",
            name="Michelada Music Festival & Car Show — Día de los Muertos Edition",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Live Music, Car Show, Cultural / Día",
            public_types=["Live Music & Performance", "Community & Culture", "Food & Drink"],
            date="2026-11-01",
            schedule="Nov 1",
            times="Noon–10 PM",
            price="See ticket page for current admission",
            age="all ages",
            location="801 Event Center, 1055 W North Temple, Salt Lake City",
            description="An all-ages Día de los Muertos edition of the Michelada Music Festival pairs a full music program with a car show and food-and-drink vendors.",
            website="https://ticketeras.com/products/michelada-music-festival-car-show",
            flags=["All ages", "Live music", "Car show", "Food and vendors"],
            cost_count=0,
            art_key="performance",
        ),
        event(
            event_id="dia-de-los-muertos-801-event-center",
            name="Día de los Muertos — Mi Preferida & La Ley",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Community Festival, Live Music, Cultural / Día",
            public_types=["Community & Culture", "Live Music & Performance", "Food & Drink"],
            date="2026-11-02",
            schedule="Nov 2",
            times="1–10 PM",
            price="Admission price not posted",
            age="Audience details not posted",
            location="801 Event Center, 1055 W North Temple, Salt Lake City",
            description="Mi Preferida 104.7 and La Ley 107.1 host an afternoon and evening of food, live music and their fourth annual Catrina contest.",
            website="https://www.instagram.com/reel/Dd9blfkiXuB/",
            social_profile="https://www.instagram.com/laley1071fm/",
            socials=[
                {"platform": "instagram", "url": "https://www.instagram.com/laley1071fm/"},
                {"platform": "facebook", "url": "https://www.facebook.com/laley1071fm/"},
            ],
            flags=["Live music", "Catrina contest", "Food available"],
            art_key="performance",
        ),
        event(
            event_id="dia-de-los-muertos-oquirrh-park-fitness-center",
            name="Día de los Muertos — Oquirrh Park Fitness Center",
            region="Salt Lake Valley",
            public_region="Salt Lake Metro",
            category="Community Festival, Cultural / Día",
            public_types=["Community & Culture", "Workshops & Learning", "Live Music & Performance"],
            date="2026-11-02",
            schedule="Nov 2",
            times="6–8:30 PM",
            price="Admission price not posted",
            age="all ages",
            location="Oquirrh Park Fitness Center, 5624 S Cougar Lane, Kearns",
            description="A community evening with live entertainment, crafts and a shared altar. Guests are encouraged to dress for the celebration and bring a photograph or memento for the ofrenda.",
            website="https://www.oquirrhrec.gov/dia-de-los-muertos-c5316ac",
            social_profile="https://www.instagram.com/oquirrhrec/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/oquirrhrec/"}],
            flags=["Community altar", "Crafts", "Live entertainment", "All ages"],
            image=OQUIRRH_PHOTO,
        ),
        event(
            event_id="dia-de-muertos-orem-city-center",
            name="Día de Muertos — Orem City Center Park",
            region="Utah County",
            public_region="Utah County",
            category="Community Festival, Cultural / Día",
            public_types=["Community & Culture", "Live Music & Performance"],
            date="2026-11-02",
            schedule="Nov 2",
            times="6–8 PM",
            price="Free admission",
            age="all ages",
            location="Orem City Center Park, 289 E Center Street, Orem",
            description="Elevate Utah and Orem Public Library bring a community Día de Muertos celebration to City Center Park with cultural activities and performances.",
            website="https://www.instagram.com/elevateutahcenter/",
            social_profile="https://www.instagram.com/elevateutahcenter/",
            socials=[{"platform": "instagram", "url": "https://www.instagram.com/elevateutahcenter/"}],
            flags=["Free admission", "Outdoor", "All ages"],
            is_free=True,
            cost_count=1,
            schedule_note="Current reporting lists 6–8 PM; check the organizer’s latest post before leaving because social listings may show a shorter end time.",
        ),
        event(
            event_id="day-of-the-dead-st-george-museum-of-art",
            name="Day of the Dead — St. George Museum of Art",
            region="Southern Utah",
            public_region="Southern Utah",
            category="Art / Exhibit, Community Festival, Cultural / Día",
            public_types=["Workshops & Learning", "Community & Culture"],
            date="2026-11-02",
            schedule="Nov 2",
            times="5–8 PM",
            price="Free",
            age="all ages",
            location="St. George Museum of Art, 47 E 200 N, St. George",
            description="A free family and community art exhibition built around “Remember Me,” honoring people whose lives and influence continue to matter.",
            website="https://sgcityutah.gov/parksandrec/arts___culture/art_museum/events/day_of_the_dead.php",
            flags=["Free admission", "Indoor", "Family art exhibition", "All ages"],
            is_free=True,
            cost_count=1,
            travel_tier="Overnight / destination",
            art_key="museum",
        ),
    ]

    by_id = {item["id"]: item for item in data["events"]}
    added = []
    updated = []
    for item in new_events:
        if item["id"] in by_id:
            by_id[item["id"]].update(item)
            updated.append(item["id"])
        else:
            data["events"].append(item)
            by_id[item["id"]] = item
            added.append(item["id"])

    uccc = by_id["d-a-de-los-muertos-utah-cultural-celebration-center"]
    uccc.update({
        "Price": "$7 adults; $5 West Valley City residents; $3 ages 4–12; ages 3 and younger free; $20 family pass for up to six",
        "flags": ["Ages 3 and younger free", "$20 family pass", "West Valley City resident discount", "All ages"],
        "lastVerified": CHECKED,
        "notable_event": True,
        "evidence": {
            "schedule": {"url": "https://www.culturalcelebration.org/dayofthedead", "method": "Official venue page", "checked": CHECKED},
            "price": {"url": "https://www.culturalcelebration.org/dayofthedead", "method": "Official venue page", "checked": CHECKED},
        },
    })
    updated.append(uccc["id"])

    ogden = by_id["ogden-d-a-de-los-muertos"]
    ogden.update({
        "Times": "Noon–8 PM; Las Cafeteras perform at 5:45 PM",
        "Price": "Free admission; food and shopping extra",
        "costCount": 1,
        "flags": ["Free admission", "Outdoor", "Community altar", "Food and vendors", "All ages"],
        "isFree": True,
        "lastVerified": CHECKED,
        "notable_event": True,
        "evidence": {
            "schedule": {"url": "https://ofoam.org/dia-de-los-muertos", "method": "Official organizer page and current local reporting", "checked": CHECKED},
            "price": {"url": "https://krcl.org/events/?event=871416", "method": "Current community-calendar listing", "checked": CHECKED},
        },
    })
    updated.append(ogden["id"])

    max_source_row = max(int(item.get("sourceRow") or 0) for item in data["events"])
    for item in data["events"]:
        if not item.get("sourceRow"):
            max_source_row += 1
            item["sourceRow"] = max_source_row

    data["meta"]["updated"] = "October 8, 2026"
    data["meta"]["eventCount"] = len(data["events"])
    data["meta"]["confirmedCount"] = sum(not item.get("isWatch") for item in data["events"])
    data["meta"]["watchCount"] = sum(bool(item.get("isWatch")) for item in data["events"])
    data["meta"]["realImageCount"] = sum(bool(item.get("photo")) for item in data["events"])
    data["meta"]["localPhotoListings"] = sum(
        bool(item.get("photo", {}).get("src", "").startswith("assets/photos/"))
        for item in data["events"]
        if item.get("photo")
    )
    data["meta"]["accessibilityListings"] = sum(bool(item.get("accessibility")) for item in data["events"])

    DATA_PATH.write_text(PREFIX + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
    ledger = {
        "checked": CHECKED,
        "article": "https://www.ksl.com/article/51633661/ogden-salt-lake-city-park-city-st-george-and-other-locales-hosting-da-de-los-muertos-events",
        "added": [item["id"] for item in new_events],
        "newlyAddedThisRun": added,
        "updated": sorted(set(updated)),
        "notes": "The roundup was used for discovery; event records were checked against official organizer, venue, city or ticket pages where available.",
    }
    research_path = ROOT / "research" / "dia-de-los-muertos-additions-2026-10-08.json"
    research_path.parent.mkdir(exist_ok=True)
    research_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {len(added)} events; updated {len(set(updated))}; total {len(data['events'])}")


if __name__ == "__main__":
    main()
