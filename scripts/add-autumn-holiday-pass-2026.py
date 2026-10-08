#!/usr/bin/env python3
"""Add the October 8 autumn-holiday research pass to the public event data."""

from __future__ import annotations

import copy
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data.js"
LEDGER_PATH = ROOT / "research" / "autumn-holiday-pass-2026-10-08.json"
PREFIX = "window.SITE_DATA = "
CHECKED = "2026-10-08"


def dates_between(start: str, end: str) -> list[str]:
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    return [(first + timedelta(days=i)).isoformat() for i in range((last - first).days + 1)]


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
        "rightsNote": "Selected from an official organizer, government or venue page for editorial event-listing use.",
    }


PHOTOS = {
    "moccwalk": photo(
        "assets/photos/moccwalk-2026.webp",
        "MoccWalk participants follow a paved park path beneath an American Indian Services arch.",
        "American Indian Services",
        "https://secure.qgiv.com/event/moccwalk26/",
        "https://96f8f4f60d478d4da507-33b0735e1ef87c51ff6ab3f3c71c7652.ssl.cf1.rackcdn.com/img_3698-1784737051",
        "Previous MoccWalk photo",
        1200,
        1500,
    ),
    "suu_dia": photo(
        "assets/photos/suu-dia-de-los-muertos-2026.webp",
        "A Día de los Muertos dancer in bright traditional dress performs outdoors at Southern Utah University.",
        "Southern Utah Museum of Art",
        "https://www.suu.edu/suma/dotd/",
        "https://www.suu.edu/suma/dotd/dotd-banner.jpg",
        "Previous celebration photo",
        1200,
        452,
    ),
    "health_fair": photo(
        "assets/photos/health-heritage-fair-2026.webp",
        "A DJ performs from a decorated vehicle as people gather at an earlier Health & Heritage Fair.",
        "Take Care Utah",
        "https://takecareutah.org/health-heritage-fair/",
        "https://takecareutah.org/wp-content/uploads/2026/06/tcu-hhf-bringing-people-together-2-2048x1462.jpg",
        "Previous fair photo",
        1600,
        1142,
    ),
    "ballpark": photo(
        "assets/photos/america-first-square-ballpark.webp",
        "The green baseball field and seating at The Ballpark at America First Square.",
        "America First Square",
        "https://www.americafirstsquare.com/",
        "https://media.americafirstsquare.com/wp-content/uploads/baseball-field-rendering.jpg",
        "Venue image",
        596,
        440,
    ),
    "clinton_trot": photo(
        "assets/photos/clinton-turkey-trot-2026.webp",
        "A runner raises both arms while crossing a finish line.",
        "Clinton City",
        "https://www.clintoncity.net/2348/Special-Events",
        "https://www.clintoncity.net/ImageRepository/Document?documentId=4431",
        "Organizer image",
        1499,
        434,
    ),
    "ktown_trot": photo(
        "assets/photos/k-town-turkey-trot-2026.webp",
        "Runners circle Jackson Flat Reservoir during the K-Town Turkey Trot.",
        "Kane County Office of Tourism",
        "https://www.visitsouthernutah.com/events/k-town-turkey-trot-5k/",
        "https://www.earthdiver.com/cdn-cgi/image/width=1500,quality=75,format=auto/http://assets.earthdiver.com/media/autosync-1000079-1747945201319-0.jpg",
        "Previous event photo",
        1500,
        999,
    ),
}


def event(
    *, event_id, name, region, public_region, categories, public_types, start,
    schedule, times, price, age, location, description, website, holidays,
    end=None, occurrences=None, flags=None, is_free=False, cost_count=0,
    art_key="community", theme=None, communities=None, notable=False,
    travel_tier="Core / easy day trip", image=None, accessibility=None,
    schedule_note="", status="Confirmed 2026", extra_notes="",
):
    primary = holidays[0]
    seasons = [s for s in ("Fall", "Winter", "Spring", "Summer") if s in holidays]
    theme_key = theme or primary.lower().replace(" ", "-")
    seasonal_placeholder = ROOT / "assets" / "art" / "seasonal" / f"{theme_key}-{art_key}.svg"
    generic_key = art_key if art_key in {"active", "community", "food", "market", "nightlife", "performance", "workshop"} else "community"
    placeholder = (
        f"assets/art/seasonal/{theme_key}-{art_key}.svg"
        if seasonal_placeholder.exists()
        else f"assets/art/{generic_key}.svg"
    )
    result = {
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
        "Status": status,
        "Why / thoughts": description,
        "Website": website,
        "Social profile": "",
        "Extra notes": extra_notes,
        "categories": categories,
        "sourceCategories": categories,
        "ghostCount": 0,
        "costCount": cost_count,
        "isWatch": False,
        "artKey": art_key,
        "socials": [],
        "photo": copy.deepcopy(image),
        "sourceRegion": region,
        "publicRegion": public_region,
        "publicTypes": public_types,
        "sponsored": False,
        "holidays": holidays,
        "primaryHoliday": primary,
        "startDate": start,
        "endDate": end or start,
        "travelTier": travel_tier,
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
            "method": "Read a dated organizer, venue, government or ticket source and followed detail links when available.",
        },
    }
    return result


def main():
    raw = DATA_PATH.read_text()
    assert raw.startswith(PREFIX) and raw.rstrip().endswith(";")
    data = json.loads(raw[len(PREFIX):].rstrip()[:-1])
    by_id = {item["id"]: item for item in data["events"]}
    next_source_row = max((item.get("sourceRow", 0) for item in data["events"]), default=0) + 1

    def existing_photo(event_id):
        return copy.deepcopy(by_id[event_id].get("photo"))

    new_events = [
        event(
            event_id="owl-o-ween-eccles-wildlife-center-2026", name="OWL-o-ween at Eccles Wildlife Education Center",
            region="Davis County", public_region="Davis County", categories=["Wildlife program", "Halloween festival"],
            public_types=["Community & Culture", "Active & Outdoors", "Workshops & Learning"], start="2026-10-10",
            schedule="Oct 10", times="10 AM–1 PM; owl programs at 10 and 11:30 AM",
            price="Free", age="Families and all ages", location="Eccles Wildlife Education Center, 1157 S Waterfowl Way, Farmington",
            description="Meet live owls, learn about nocturnal wildlife, walk the nature trail and stop for games and trunk-or-treating.",
            website="https://recreation.utah.gov/event/owl-o-ween/", holidays=["Halloween", "Fall"],
            flags=["Free admission", "Live owls", "Costumes welcome", "Outdoor trail"], is_free=True, cost_count=1,
            art_key="family", theme="halloween", notable=True,
        ),
        event(
            event_id="bumbles-drone-spooktacular-2026", name="Bumble’s Drone Spooktacular",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Drone show", "Family Halloween"],
            public_types=["Live Music & Performance", "Community & Culture"], start="2026-10-16", end="2026-10-17",
            occurrences=["2026-10-16", "2026-10-17"], schedule="Oct 16–17", times="6 PM both nights",
            price="Ticketed; current price is shown after choosing a date on the ticket page", age="All ages; children under 2 do not need a ticket",
            location="The Ballpark at America First Square, 11131 S Ballpark Way, South Jordan",
            description="A two-night Halloween program at the ballpark built around a coordinated drone-light show and family entertainment.",
            website="https://www.ticketmaster.com/the-ballpark-at-america-first-square-tickets-south-jordan/venue/247103",
            holidays=["Halloween", "Fall"], flags=["Two nights", "Outdoor stadium", "Ticketed"],
            theme="halloween", art_key="performance", image=PHOTOS["ballpark"],
            accessibility={"summary": "The venue welcomes service animals; contact the ticket office for accessible seating and route details."},
        ),
        event(
            event_id="dia-de-los-muertos-tyler-library-2026", name="Día de los Muertos at Tyler Library",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Library program", "Cultural celebration"],
            public_types=["Community & Culture", "Live Music & Performance"], start="2026-11-02",
            schedule="Nov 2", times="6–8 PM", price="Free", age="All ages",
            location="Ruth Vine Tyler Library, 8041 S Wood Street, Midvale",
            description="An evening of performances, crafts, music and treats centered on a community ofrenda and remembrance.",
            website="https://slcls.libnet.info/event/17322841", holidays=["Día de los Muertos", "Fall"],
            flags=["Free admission", "Community ofrenda", "Crafts", "Indoor"], is_free=True, cost_count=1,
            communities=["Mexican / Latino"], theme="dayofdead", art_key="community",
            accessibility={"summary": "Library program; contact the branch for accommodation or seating requests."},
        ),
        event(
            event_id="dia-de-los-muertos-west-valley-library-2026", name="Día de los Muertos Party — West Valley Library",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Library program", "Cultural celebration"],
            public_types=["Community & Culture"], start="2026-11-02", schedule="Nov 2", times="6–7 PM",
            price="Free", age="Families and all ages", location="West Valley Library, West Valley City",
            description="A one-hour library celebration with face painting and hands-on activities connected to Día de los Muertos.",
            website="https://slcls.libnet.info/event/17477322", holidays=["Día de los Muertos", "Fall"],
            flags=["Free admission", "Face painting", "Indoor"], is_free=True, cost_count=1,
            communities=["Mexican / Latino"], theme="dayofdead", art_key="family",
            accessibility={"summary": "Library program; contact the branch for accommodation or seating requests."},
        ),
        event(
            event_id="oaxaca-en-utah-dia-de-los-muertos-2026", name="Oaxaca en Utah Día de los Muertos — Ogden",
            region="Ogden / Weber", public_region="Ogden, Weber & Morgan", categories=["Community festival", "Cultural celebration"],
            public_types=["Community & Culture", "Live Music & Performance", "Food & Drink"], start="2026-11-02",
            schedule="Nov 2", times="5–9 PM", price="Free admission; food purchases extra", age="All ages",
            location="Myers Evergreen Memorial Park, 100 N Monroe Boulevard, Ogden",
            description="A remembrance walk, community photo display and ofrenda share the evening with mariachi, folklórico, face painting, a Catrina contest and food trucks.",
            website="https://www.playeasy.com/events/01a0fb6b-8bee-7850-8bcd-93d70c43dd56",
            holidays=["Día de los Muertos", "Fall"], flags=["Free admission", "Mariachi", "Catrina contest", "Food trucks"],
            is_free=True, cost_count=1, communities=["Mexican / Latino"], theme="dayofdead", art_key="community",
        ),
        event(
            event_id="suu-community-ofrenda-2026", name="Community Ofrenda at Southern Utah Museum of Art",
            region="Cedar / Iron County", public_region="Cedar / Iron County", categories=["Art exhibit", "Community ofrenda"],
            public_types=["Community & Culture", "Workshops & Learning"], start="2026-10-18", end="2026-11-07",
            occurrences=dates_between("2026-10-18", "2026-11-07"), schedule="Oct 18–Nov 7", times="During museum hours",
            price="Free", age="All ages", location="Southern Utah Museum of Art, 13 S 300 W, Cedar City",
            description="A community altar at SUMA invites visitors to remember loved ones through photographs, names and traditional Día de los Muertos imagery.",
            website="https://www.suu.edu/suma/dotd/", holidays=["Día de los Muertos", "Fall"],
            flags=["Free admission", "Community ofrenda", "Indoor"], is_free=True, cost_count=1,
            communities=["Mexican / Latino"], theme="dayofdead", art_key="community", image=PHOTOS["suu_dia"],
        ),
        event(
            event_id="suu-day-of-the-dead-celebration-2026", name="Day of the Dead Celebration — Southern Utah University",
            region="Cedar / Iron County", public_region="Cedar / Iron County", categories=["Cultural festival", "Music and dance"],
            public_types=["Community & Culture", "Live Music & Performance", "Food & Drink"], start="2026-11-07",
            schedule="Nov 7", times="11 AM–3 PM", price="Free", age="All ages",
            location="Eccles Music Center and Southern Utah Museum of Art, Cedar City",
            description="Southern Utah’s large public Día de los Muertos celebration brings together music, dance, food, art activities and cultural history.",
            website="https://www.suu.edu/suma/dotd/", holidays=["Día de los Muertos", "Fall"],
            flags=["Free admission", "Live performance", "Art activities", "Complimentary pan de muerto"], is_free=True,
            cost_count=1, communities=["Mexican / Latino"], theme="dayofdead", art_key="performance", image=PHOTOS["suu_dia"], notable=True,
        ),
        event(
            event_id="moccwalk-steps-for-scholarships-2026", name="MoccWalk — Steps for Scholarships",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Community walk", "Native culture"],
            public_types=["Community & Culture", "Active & Outdoors", "Giving & Volunteering"], start="2026-10-12",
            schedule="Oct 12", times="Check-in 4:30–5:30 PM; walk 5:30–6:30 PM", price="Free registration and participation",
            age="All ages; everyone welcome", location="Wardle Fields Regional Park, 14148 S 2700 W, Bluffdale",
            description="Walk in moccasins or sneakers at this annual celebration of Native culture, education and scholarship support for Native students.",
            website="https://secure.qgiv.com/event/moccwalk26/", holidays=["Indigenous Peoples’ Day", "Fall"],
            flags=["Free admission", "Free registration", "Family-friendly", "Outdoor walk", "Fundraiser"], is_free=True, cost_count=1,
            communities=["Native / Indigenous"], theme="indigenous", art_key="active", image=PHOTOS["moccwalk"], notable=True,
        ),
        event(
            event_id="military-tribute-field-pleasant-view-2026", name="Military Tribute Field — Pleasant View",
            region="Ogden / Weber", public_region="Ogden, Weber & Morgan", categories=["Outdoor memorial", "Veterans Week"],
            public_types=["Community & Culture", "Giving & Volunteering"], start="2026-11-01", end="2026-11-14",
            occurrences=dates_between("2026-11-01", "2026-11-14"), schedule="Nov 1–14", times="Open-air display; no daily visiting hours posted",
            price="Free to visit; optional flag sponsorship supports the foundation", age="All ages",
            location="Pleasant View City Hall, 520 W Elberta Drive, Pleasant View",
            description="Hundreds of flags form a walk-through memorial for veterans, active-duty service members and first responders, many with personal tribute tags.",
            website="https://majorbrenttaylor.com/event/military-tribute-field/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Free to visit", "Outdoor memorial", "Volunteer opportunities"], is_free=True, cost_count=1,
            theme="veterans", art_key="community", notable=True,
        ),
        event(
            event_id="veterans-day-devotional-north-ogden-2026", name="Veterans Day Devotional — North Ogden",
            region="Ogden / Weber", public_region="Ogden, Weber & Morgan", categories=["Community gathering", "Interfaith observance"],
            public_types=["Community & Culture", "Live Music & Performance"], start="2026-11-01", schedule="Nov 1", times="Time not yet posted",
            price="Free", age="Family-friendly; all faiths welcome", location="Barker Park Amphitheater, 2375 Fruitland Drive, North Ogden",
            description="A non-denominational outdoor gathering uses music, brief messages and prayer to honor veterans and reflect on military service.",
            website="https://majorbrenttaylor.com/event/veterans-day-devotional/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Outdoor", "Bring a chair or blanket"], is_free=True, cost_count=1,
            theme="veterans", art_key="performance",
        ),
        event(
            event_id="veterans-memorial-blood-drive-pleasant-view-2026", name="Veterans Memorial Blood Drive — Pleasant View",
            region="Ogden / Weber", public_region="Ogden, Weber & Morgan", categories=["Blood drive", "Veterans Week"],
            public_types=["Giving & Volunteering", "Community & Culture"], start="2026-11-05", schedule="Nov 5", times="Begins 1 PM; appointment times vary",
            price="Free; blood-donor eligibility rules apply", age="Eligible blood donors",
            location="Pleasant View LDS Church, 2250 W Elberta Drive, Pleasant View",
            description="A community blood drive offers a practical way to mark Veterans Week; walk-ins are welcome and appointments are encouraged.",
            website="https://majorbrenttaylor.com/event/veterans-blood-drive/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Appointments encouraged", "Walk-ins welcome", "Indoor"], is_free=True, cost_count=1,
            theme="veterans", art_key="community",
        ),
        event(
            event_id="memorial-ruck-march-north-ogden-2026", name="Memorial Ruck March — North Ogden",
            region="Ogden / Weber", public_region="Ogden, Weber & Morgan", categories=["Memorial walk", "Veterans Week"],
            public_types=["Active & Outdoors", "Community & Culture"], start="2026-11-07", schedule="Nov 7", times="7 AM",
            price="Participation details on organizer page", age="General audience; choose a pace appropriate to the route",
            location="Starts at Ben Lomond Cemetery, 526 E 2850 N, North Ogden",
            description="Participants ruck, walk or run from Ben Lomond Cemetery toward Coldwater Canyon while carrying a pack, flag or the name of someone they wish to honor.",
            website="https://majorbrenttaylor.com/event/memorial-ruck-march-2/", holidays=["Veterans Day", "Fall"],
            flags=["Outdoor route", "Walk, run or ruck"], theme="veterans", art_key="active",
        ),
        event(
            event_id="layton-veterans-parade-2026", name="Layton Veterans Parade",
            region="Davis County", public_region="Davis County", categories=["Parade", "Veterans Week"],
            public_types=["Community & Culture"], start="2026-11-07", schedule="Nov 7", times="11:11 AM",
            price="Free", age="All ages", location="Layton Commons area; volunteer staging at 789 N Wasatch Drive, Layton",
            description="Veterans, families and community groups parade through Layton, including volunteers carrying the foundation’s 30-by-60-foot flag.",
            website="https://majorbrenttaylor.com/event/layton-veterans-parade/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Outdoor parade", "Volunteer opportunity"], is_free=True, cost_count=1,
            theme="veterans", art_key="community", image=existing_photo("layton-halloween-bash"),
        ),
        event(
            event_id="draper-veterans-day-ceremony-2026", name="Draper Veterans Day Ceremony",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Civic ceremony", "Veterans Day"],
            public_types=["Community & Culture", "Live Music & Performance"], start="2026-11-11", schedule="Nov 11", times="11–11:30 AM",
            price="Free", age="All ages", location="Gold Star Families Memorial Monument at Draper Park, 12500 S 1300 E, Draper",
            description="A concise civic ceremony includes the posting of colors, musical performances and a keynote address at Draper’s Gold Star Families memorial.",
            website="https://www.draperutah.gov/events-programs/community-events/veterans-day-ceremony/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Outdoor ceremony", "Refreshments"], is_free=True, cost_count=1,
            theme="veterans", art_key="community", image=existing_photo("draper-international-arts-crafts-festival-2026"),
        ),
        event(
            event_id="sunriver-veterans-day-service-2026", name="SunRiver Veterans Honor Park Service",
            region="Southwest Utah", public_region="Southern Utah", categories=["Memorial service", "Veterans Day"],
            public_types=["Community & Culture"], start="2026-11-11", schedule="Nov 11", times="9 AM–noon",
            price="Free", age="All ages", location="SunRiver Veterans Honor Park, 1766 W Wide River Drive, St. George",
            description="A Veterans Day service at SunRiver’s honor park brings the community together for remembrance and recognition of military service.",
            website="https://veterans.utah.gov/event/sunriver-veterans-honor-park-veterans-day-service/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Outdoor", "Bring a chair; seating is limited"], is_free=True, cost_count=1,
            theme="veterans", art_key="community",
        ),
        event(
            event_id="cottonwood-heights-star-spangled-finale-2026", name="Cottonwood Heights Star-Spangled Finale",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Student performance", "Veterans recognition"],
            public_types=["Live Music & Performance", "Community & Culture"], start="2026-11-12", schedule="Nov 12", times="7–8 PM",
            price="Free", age="Veterans, families and community members", location="Butler Middle School, 7530 S 2700 E, Cottonwood Heights",
            description="Ridgecrest Elementary students perform the songs of each military branch in an evening created to recognize local veterans and their families.",
            website="https://veterans.utah.gov/events/list/page/2/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Student performance", "Indoor"], is_free=True, cost_count=1,
            theme="veterans", art_key="performance",
        ),
        event(
            event_id="northeastern-utah-veterans-wellness-fair-2026", name="Northeastern Utah Military & Veterans Wellness Fair",
            region="Eastern Utah", public_region="Eastern Utah", categories=["Resource fair", "Veterans support"],
            public_types=["Community & Culture", "Workshops & Learning"], start="2026-11-13", schedule="Nov 13", times="2–6 PM",
            price="Free", age="Military members, veterans and families", location="Vernal Utah National Guard Armory, 220 S 500 E, Vernal",
            description="A practical resource fair connects military households with veteran-service groups, health and mental-health providers, benefits specialists and career support.",
            website="https://veterans.utah.gov/events/list/page/2/", holidays=["Veterans Day", "Fall"],
            flags=["Free admission", "Resource fair", "Indoor"], is_free=True, cost_count=1,
            theme="veterans", art_key="learning", travel_tier="Worth the drive",
        ),
        event(
            event_id="china-poblana-dress-exhibit-2026", name="La China Poblana Dress Exhibit",
            region="Salt Lake City", public_region="Salt Lake Metro", categories=["Museum exhibit", "Latine heritage"],
            public_types=["Community & Culture", "Workshops & Learning"], start="2026-09-01", end="2026-12-31",
            occurrences=dates_between("2026-09-01", "2026-12-31"), schedule="Sep 1–Dec 31", times="During Marriott Library hours",
            price="Free", age="General audience", location="J. Willard Marriott Library, 295 S 1500 E, Salt Lake City",
            description="Historic China Poblana ensembles, recorded performances and borderlands stories explore clothing as an archive of identity, migration and tradition.",
            website="https://culture.utah.edu/events/latine-heritage-month.php", holidays=["Hispanic Heritage Month", "Fall", "Winter"],
            flags=["Free admission", "Indoor exhibit", "Extended run"], is_free=True, cost_count=1,
            communities=["Latino / Hispanic"], theme="hispanic", art_key="learning",
            schedule_note="The university page’s detailed exhibit listing gives Sep. 1–Dec. 31; its page header uses a shorter range.",
        ),
        event(
            event_id="health-heritage-fair-utah-2026", name="Health & Heritage Fair",
            region="Salt Lake City", public_region="Salt Lake Metro", categories=["Community fair", "Health services", "Cultural festival"],
            public_types=["Community & Culture", "Food & Drink", "Live Music & Performance"], start="2026-09-26",
            schedule="Sep 26", times="Noon–8:30 PM", price="Free", age="All ages; everyone welcome",
            location="Utah State Fairpark, 155 N 1000 W, Salt Lake City",
            description="A daylong fair combines free health screenings and vaccines with cultural performances, family activities, a parade of countries, vendors and food.",
            website="https://takecareutah.org/health-heritage-fair/", holidays=["Hispanic Heritage Month", "Fall"],
            flags=["Free admission", "Free health services", "Family activities", "Cultural performances"], is_free=True, cost_count=1,
            communities=["Latino / Hispanic", "Immigrant / Refugee"], theme="hispanic", art_key="community", image=PHOTOS["health_fair"],
            status="Confirmed 2026; past",
        ),
        event(
            event_id="beisbol-en-salt-lake-2026", name="Béisbol en Salt Lake",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Baseball", "Cultural festival"],
            public_types=["Active & Outdoors", "Community & Culture", "Food & Drink"], start="2026-09-26", end="2026-09-27",
            occurrences=["2026-09-26", "2026-09-27"], schedule="Sep 26–27",
            times="Sat gates 4:30 PM, game 6:35 PM; Sun gates 11 AM, game 1:05 PM",
            price="Single-game tickets $15 or $20; suites $1,200", age="All ages",
            location="The Ballpark at America First Square, 11131 S Ballpark Way, South Jordan",
            description="Two professional baseball games add live Latin music and dance, youth activities and a Saturday drone show; Sunday closes with postgame mariachi and a family base walk.",
            website="https://www.mlb.com/milb/salt-lake/news/beisbol-en-salt-lake-returns-to-the-ballpark-at-america-first-square",
            holidays=["Hispanic Heritage Month", "Fall"], flags=["Two games", "Saturday drone show", "Sunday mariachi", "Kids clinic"],
            cost_count=2, communities=["Latino / Hispanic"], theme="hispanic", art_key="active", image=PHOTOS["ballpark"], status="Confirmed 2026; past",
        ),
        event(
            event_id="mi-gente-millcreek-2026", name="Mi Gente — A Celebration of Latin & Hispanic Heritage",
            region="Salt Lake Valley", public_region="Salt Lake Metro", categories=["Cultural festival", "Night market"],
            public_types=["Community & Culture", "Live Music & Performance", "Markets & Shopping", "Food & Drink"], start="2026-09-26",
            schedule="Sep 26", times="5–10 PM", price="Free admission; food and drink purchases extra", age="All ages; full bar for adults 21+",
            location="Millcreek Common, 1354 E Chambers Avenue, Millcreek",
            description="An evening festival fills Millcreek Common with Latin and Hispanic performers, dancing, a makers market, food and family activities, with a separate full-bar service for adults.",
            website="https://www.eventeny.com/events/migente-33264/", holidays=["Hispanic Heritage Month", "Fall"],
            flags=["Free admission", "Live music and dance", "Market", "21+ bar area"], is_free=True, cost_count=1,
            communities=["Latino / Hispanic"], theme="hispanic", art_key="community", image=existing_photo("dia-de-los-muertos-ofrenda-millcreek-common"), status="Confirmed 2026; past",
        ),
        event(
            event_id="latinarte-nuestras-raices-2026", name="LatinArte: Nuestras Raíces",
            region="Salt Lake City", public_region="Salt Lake Metro", categories=["Art exhibit", "Latine heritage"],
            public_types=["Community & Culture", "Workshops & Learning"], start="2026-08-13", end="2026-09-25",
            occurrences=dates_between("2026-08-13", "2026-09-25"), schedule="Aug 13–Sep 25", times="During gallery hours",
            price="Free", age="General audience", location="George S. & Dolores Doré Eccles Gallery, SLCC South City Campus, 1575 S 200 E, Salt Lake City",
            description="The eighth juried exhibition gathers work by 37 Latino artists from Utah and western Wyoming alongside the Sor Juana Spanish Poetry Contest.",
            website="https://www.slcc.edu/exhibitions-collections/exhibitions/previous-exhibitions/latinarte.aspx",
            holidays=["Hispanic Heritage Month", "Summer", "Fall"], flags=["Free admission", "37 regional artists", "Indoor gallery"],
            is_free=True, cost_count=1, communities=["Latino / Hispanic"], theme="hispanic", art_key="learning", status="Confirmed 2026; past",
        ),
        event(
            event_id="latinarte-artist-panel-2026", name="LatinArte Artist Panel",
            region="Salt Lake City", public_region="Salt Lake Metro", categories=["Artist talk", "Latine heritage"],
            public_types=["Workshops & Learning", "Community & Culture"], start="2026-09-24",
            schedule="Sep 24", times="6–7 PM", price="Free", age="General audience",
            location="George S. & Dolores Doré Eccles Gallery, SLCC South City Campus, 1575 S 200 E, Salt Lake City",
            description="Award-winning artists Daniella Ortiz Ramírez, Bianca Velasquez and Andrea Cárdenas Arceo discuss their work, process and experiences as Utah artists.",
            website="https://calendar.slcc.edu/event/latinarte-nuestra-raices-our-roots-artist-panel",
            holidays=["Hispanic Heritage Month", "Fall"], flags=["Free admission", "Artist conversation", "Indoor"],
            is_free=True, cost_count=1, communities=["Latino / Hispanic"], theme="hispanic", art_key="learning", status="Confirmed 2026; past",
        ),
        event(
            event_id="clinton-city-turkey-trot-2026", name="Clinton City Turkey Trot",
            region="Davis County", public_region="Davis County", categories=["5K", "Community walk"],
            public_types=["Active & Outdoors", "Community & Culture"], start="2026-11-14", schedule="Nov 14", times="9 AM",
            price="$15 per participant", age="All ages; choose a 5K or 2-mile walk", location="Clinton; start point provided with registration",
            description="A low-cost city turkey trot offers a timed 5K option and a two-mile walk for families and casual participants.",
            website="https://www.clintoncity.net/2348/Special-Events", holidays=["Thanksgiving", "Fall"],
            flags=["5K", "2-mile walk", "Registration closes Nov 12"], cost_count=2,
            theme="thanksgiving", art_key="active", image=PHOTOS["clinton_trot"],
        ),
        event(
            event_id="moab-city-turkey-trot-2026", name="Moab City Turkey Trot 5K",
            region="Eastern Utah", public_region="Eastern Utah", categories=["5K", "Community run"],
            public_types=["Active & Outdoors", "Community & Culture"], start="2026-11-21", schedule="Nov 21", times="9 AM–11:59 AM",
            price="Registration price not posted", age="Runners and walkers", location="Moab Recreation and Aquatic Center / Swanny City Park, 400 N 100 W, Moab",
            description="Moab’s annual community 5K welcomes runners, walkers and casual trotters for a Saturday morning route from the recreation center.",
            website="https://moabcity.gov/Calendar.aspx?EID=1324", holidays=["Thanksgiving", "Fall"],
            flags=["5K", "Runners and walkers", "ADA-accessible park facilities"], theme="thanksgiving", art_key="active", travel_tier="Worth the drive",
            accessibility={"summary": "Swanny City Park lists ADA access, parking, restrooms, water and picnic facilities."},
        ),
        event(
            event_id="k-town-turkey-trot-2026", name="K-Town Turkey Trot 5K",
            region="Southwest Utah", public_region="Southern Utah", categories=["5K", "Fun run"],
            public_types=["Active & Outdoors", "Community & Culture"], start="2026-11-26", schedule="Nov 26", times="Start time not posted",
            price="Registration details not posted", age="All ages; families welcome", location="Jackson Flat Reservoir, Sherry Belle Trail, Kanab",
            description="A costume-friendly Thanksgiving morning 5K follows the three-mile Sherry Belle Trail around Jackson Flat Reservoir.",
            website="https://www.visitsouthernutah.com/events/k-town-turkey-trot-5k/", holidays=["Thanksgiving", "Fall"],
            flags=["5K fun run", "Costumes encouraged", "Reservoir trail"], theme="thanksgiving", art_key="active", image=PHOTOS["ktown_trot"], travel_tier="Worth the drive",
        ),
        event(
            event_id="west-point-turkey-trot-benefit-run-2026", name="West Point Turkey Trot Benefit Run",
            region="Davis County", public_region="Davis County", categories=["Benefit run", "Community gathering"],
            public_types=["Active & Outdoors", "Giving & Volunteering", "Community & Culture"], start="2026-11-26", schedule="Nov 26", times="8–10:30 AM; check-in from 7:30 AM",
            price="$20 per runner or $60 per family", age="All ages; runners and non-runners welcome", location="Loy Blake Park, 550 N 3500 W, West Point",
            description="A community benefit run directs proceeds to a local family and adds a bonfire, prize drawing, scones, cocoa and a bake sale for supporters who are not racing.",
            website="https://www.eventbrite.com/e/2026-turkey-trot-benefit-run-tickets-2002847650237", holidays=["Thanksgiving", "Fall"],
            flags=["Benefit run", "Family rate", "Registration closes Nov 13", "Packet pickup Nov 25"], cost_count=2,
            theme="thanksgiving", art_key="active",
        ),
        event(
            event_id="hunger-fight-utah-thanksgiving-outreach-2026", name="Utah Thanksgiving Community Outreach — Hunger Fight",
            region="Utah County", public_region="Utah County", categories=["Meal-packing volunteer event", "Community service"],
            public_types=["Giving & Volunteering", "Community & Culture"], start="2026-11-23", end="2026-11-24",
            occurrences=["2026-11-23", "2026-11-24"], schedule="Nov 23–24", times="Starts Nov 23 at 5 PM; concludes Nov 24 at 8 PM",
            price="Free to volunteer; registration required", age="Groups, teams and community volunteers",
            location="547 S Locust Avenue, Pleasant Grove",
            description="Volunteer teams assemble shelf-stable meals during a two-day Thanksgiving outreach designed to support local food relief.",
            website="https://give.hungerfight.org/campaigns/45485-4th-annual-utah-thanksgiving-community-outreach-event",
            holidays=["Thanksgiving", "Fall"], flags=["Free admission", "Volunteer registration", "Meal packing", "Two-day project"], is_free=True, cost_count=1,
            theme="thanksgiving", art_key="community",
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

    # Columbus Day is a real user-facing research bucket even when no current Utah
    # public celebration survives primary-source verification.
    if "Columbus Day" not in data["holidays"]:
        insert_at = data["holidays"].index("Indigenous Peoples’ Day") + 1
        data["holidays"].insert(insert_at, "Columbus Day")
    traditions = data["holidayGroups"]["Holidays & traditions"]
    if "Columbus Day" not in traditions:
        traditions.insert(traditions.index("Indigenous Peoples’ Day") + 1, "Columbus Day")

    data["meta"]["updated"] = "October 8, 2026"
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
        "scope": ["Halloween", "Día de los Muertos", "Veterans Day", "Columbus Day", "Indigenous Peoples’ Day", "Hispanic Heritage Month", "Thanksgiving"],
        "addedOrUpdatedIds": [e["id"] for e in new_events],
        "result": {
            "newOrUpdated": len(new_events),
            "totalEvents": len(data["events"]),
            "realImageListings": data["meta"]["realImageCount"],
            "columbusDayPublicEventsConfirmed": 0,
            "note": "Columbus Day was added as a filterable observance. Government office closures were not treated as public events, and no current Utah public celebration was promoted without evidence.",
        },
        "sources": sorted({e["Website"] for e in new_events}),
        "excluded": [
            {"name": "St. George Turkey Trot & Harvest Festival", "reason": "Official city page says the 2026 event is cancelled."},
            {"name": "Columbus Day office closures", "reason": "Administrative closures are not public events."},
        ],
    }
    LEDGER_PATH.parent.mkdir(exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(f"Applied {len(new_events)} autumn-holiday records; {len(data['events'])} total events.")


if __name__ == "__main__":
    main()
