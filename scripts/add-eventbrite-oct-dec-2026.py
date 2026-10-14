#!/usr/bin/env python3
"""Publish the editor-selected Oct.–Dec. 2026 Eventbrite discovery pass."""

from __future__ import annotations

import copy
import json
import re
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data.js"
SOURCE_PATH = ROOT / "research" / "eventbrite-shortlist-2026-10-13.json"
LEDGER_PATH = ROOT / "research" / "eventbrite-publication-pass-2026-10-13.json"
PREFIX = "window.SITE_DATA = "
CHECKED = "2026-10-13"


def cfg(slug, holidays, categories, public_types, description, *, age="See organizer listing for age guidance", flags=None,
        communities=None, art="community", notable=False, accessibility=None, schedule_note=""):
    return {
        "slug": slug, "holidays": holidays, "categories": categories, "publicTypes": public_types,
        "description": description, "age": age, "flags": flags or [], "communities": communities or [],
        "artKey": art, "notable": notable, "accessibility": accessibility, "scheduleNote": schedule_note,
    }


SELECTED = {
    "2001023141081": cfg("avanza-live-2026", ["Hispanic Heritage Month", "Fall"], ["Live music", "DJs", "Latino community"], ["Live Music & Performance", "Nightlife & Parties", "Community & Culture"], "Avanza 88.3 closes Hispanic Heritage Month with live music, DJs and a community-centered dance night at Woodbine.", flags=["Indoor", "Bilingual welcome"], communities=["Latino / Hispanic"], art="nightlife"),
    "1986090600450": cfg("world-climbing-series-salt-lake-city-2026", ["Fall"], ["Climbing competition", "Professional sports", "Festival"], ["Active & Outdoors", "Community & Culture"], "Elite speed and bouldering competitors take over Smith's Ballpark for a three-day international climbing meet with a stadium-scale spectator experience.", age="All ages", flags=["All ages", "Three-day event", "Outdoor stadium"], art="active", notable=True),
    "1992263906976": cfg("america-the-beautiful-250th-anniversary-concert-2026", ["Veterans Day", "Fall"], ["Concert", "American folk music", "Community commemoration"], ["Live Music & Performance", "Community & Culture"], "A concert of patriotic songs, American folk music and familiar favorites marks the country's 250th anniversary in Libby Gardner Concert Hall.", age="All ages", flags=["All ages", "Indoor", "Free and paid seating"], art="performance"),
    "1996471546138": cfg("smutty-girls-go-spooky-bookish-market-2026", ["Halloween", "Fall"], ["Book fair", "Market", "Adult social"], ["Markets & Shopping", "Nightlife & Parties"], "A Halloween edition of the romance-reader market brings books, themed vendors and a playful adults-focused afternoon to The Hearth.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Free and paid options"], communities=["Women-centered"], art="market"),
    "1990301658839": cfg("spooky-sunday-service-drag-brunch-2026", ["Halloween", "Fall"], ["Drag brunch", "Comedy", "Nightlife"], ["Live Music & Performance", "Nightlife & Parties"], "Park City's 69th Ward drag cast pairs a deliberately irreverent Halloween show with brunch at The Cabin.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Drag performance", "Brunch"], communities=["LGBTQ+"], art="nightlife"),
    "1993481734531": cfg("katee-robert-tarot-trials-2026", ["Halloween", "Fall"], ["Author event", "Fantasy / Fandom", "Books"], ["Workshops & Learning", "Community & Culture"], "Romance and fantasy author Katee Robert discusses The Tarot Trials at a ticketed King's English off-site event.", flags=["Indoor", "Book event", "Reservation required"], art="performance"),
    "2002757950944": cfg("free-autism-trick-or-treat-american-fork-2026", ["Halloween", "Fall"], ["Sensory-friendly trick-or-treat", "Family activity", "Book fair"], ["Kids & Family", "Community & Culture"], "Families can trick-or-treat at their own pace, try sensory-friendly games and activities, and browse a small book fair at Success On The Spectrum.", age="Children and families", flags=["Free admission", "Sensory-friendly", "Indoor", "At-your-own-pace"], communities=["Neurodivergent families"], art="community", accessibility={"summary": "The organizer describes the games, activities and trick-or-treat route as sensory-friendly and designed so children can participate at their own pace."}),
    "2001097487453": cfg("halloween-for-every-brain-gateway-2026", ["Halloween", "Fall"], ["Sensory-inclusive Halloween", "Trick-or-treat", "Family festival"], ["Kids & Family", "Community & Culture"], "This all-abilities Halloween celebration combines trick-or-treating with a calmer sensory area, movement activities, behavior support and practical communication tools.", age="All ages", flags=["Free admission", "All ages", "Sensory-inclusive", "Calming area", "Outdoor plaza"], communities=["Neurodivergent families", "Disabled community"], art="community", notable=True, accessibility={"summary": "Designed for different sensory needs, with a calming area, noise-canceling headphones, weighted vests, fidgets, visual and communication tools, and one-on-one behavior support."}),
    "2001095034115": cfg("trolley-square-fall-festival-2026", ["Halloween", "Fall"], ["Fall festival", "Trick-or-treat", "Pumpkin drop"], ["Kids & Family", "Community & Culture"], "Trolley Square's compact family festival combines costumed trick-or-treating with its signature pumpkin drop.", age="All ages", flags=["All ages", "Costumes welcome", "Trick-or-treat", "Pumpkin drop"], art="community"),
    "1990446269373": cfg("utah-county-halloween-book-fair-2026", ["Halloween", "Fall"], ["Book fair", "Market", "Author event"], ["Markets & Shopping", "Community & Culture"], "More than 30 authors and bookish vendors gather for an all-ages market where costumes are encouraged.", age="All ages", flags=["Free admission", "All ages", "Costumes encouraged", "Indoor"], art="market"),
    "2000891492316": cfg("turn-towards-life-queer-birth-story-screening-2026", ["Pride", "Fall"], ["Film screening", "Community gathering", "Documentary"], ["Community & Culture", "Live Music & Performance"], "A work-in-progress documentary screening about queer birth opens into a community conversation at the Sorenson Unity Center.", flags=["Free admission", "Indoor", "Community discussion"], communities=["LGBTQ+", "Parents and caregivers"], art="performance"),
    "2000464681714": cfg("books-and-boos-layton-hills-2026", ["Halloween", "Fall"], ["Trunk-or-treat", "Books", "Family fundraiser"], ["Kids & Family", "Community & Culture", "Giving & Volunteering"], "A storybook-themed trunk-or-treat at Layton Hills Mall offers allergy-friendly treats while raising support for a local doula collective.", age="Children and families", flags=["Free admission", "Allergy-friendly treats", "Indoor", "Trunk-or-treat"], communities=["Parents and caregivers"], art="community"),
    "1978199111795": cfg("queer-poetry-night-open-mic-october-2026", ["Pride", "Fall"], ["Poetry open mic", "Community gathering", "Books"], ["Community & Culture", "Live Music & Performance"], "An all-ages open mic at Under the Umbrella centers queer voices, original poetry and an easygoing community-room atmosphere.", age="All ages", flags=["Free admission", "All ages", "Indoor", "Open mic"], communities=["LGBTQ+"], art="performance"),
    "1999788122106": cfg("murderous-cocktail-affair-vault-2026", ["Halloween", "Fall"], ["Cocktail event", "Live music", "Nightlife"], ["Nightlife & Parties", "Food & Drink", "Live Music & Performance"], "The Vault leans into dark glamour with champagne, cocktails, live music and chef-curated bites for a polished Halloween-weekend night out.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Cocktails", "Dressy"], art="nightlife"),
    "2000729400495": cfg("smores-stars-and-scares-hanksville-2026", ["Halloween", "Fall"], ["Stargazing", "Mars tours", "Community Halloween"], ["Active & Outdoors", "Kids & Family", "Community & Culture"], "Hanksville turns Halloween weekend into a red-rock night out with Mars-themed tours, trick-or-treating, s'mores and dark-sky stargazing.", age="All ages", flags=["Free admission", "All ages", "Outdoor", "Worth the drive", "Stargazing"], art="active"),
    "1969841529040": cfg("witches-paddle-causey-reservoir-2026", ["Halloween", "Fall"], ["Paddle sports", "Costume outing", "Outdoor meetup"], ["Active & Outdoors", "Community & Culture"], "Paddlers bring broomsticks, costumes and boards to Causey Reservoir for a playful cold-weather witches paddle.", flags=["Free admission", "Outdoor", "Bring your own paddleboard", "Cold-water conditions", "Worth the drive"], art="active"),
    "1994592067567": cfg("monster-dash-wheeler-farm-2026", ["Halloween", "Fall"], ["5K", "Family fundraiser", "Costume run"], ["Active & Outdoors", "Kids & Family", "Giving & Volunteering"], "A Halloween-morning 5K at Wheeler Historic Farm brings costumes, movement and community fundraising together in a family-friendly setting.", age="All ages", flags=["All ages", "Outdoor", "Costumes welcome", "Fundraiser"], art="active"),
    "2003046396693": cfg("halloween-burlesque-ogden-2026", ["Halloween", "Fall"], ["Burlesque", "Nightlife", "Halloween performance"], ["Live Music & Performance", "Nightlife & Parties"], "Copper Nickel hosts an adults-focused Halloween-night burlesque show with theatrical performances and an event-space party atmosphere.", age="Adults", flags=["Adults-focused", "Indoor", "Halloween night", "Burlesque"], art="nightlife"),
    "1999975561743": cfg("whispers-through-the-veil-samhain-2026", ["Samhain", "Halloween", "Fall"], ["Samhain gathering", "Spiritual gathering", "Community ritual"], ["Community & Culture", "Workshops & Learning"], "A late-night Samhain gathering focuses on ancestral remembrance, guided reflection and spirit-guide traditions as the holiday begins.", flags=["Free admission", "Indoor", "Late night", "Spiritual gathering"], communities=["Pagan / alternative"], art="community"),
    "2003031576365": cfg("dia-de-los-muertos-centro-civico-2026", ["Día de los Muertos", "Hispanic Heritage Month", "Fall"], ["Cultural celebration", "Altars and remembrance", "Family festival"], ["Community & Culture", "Kids & Family", "Food & Drink"], "Centro Cívico Mexicano's free Día de los Muertos celebration brings altars, music, food and family activities to Salt Lake City's west side.", age="All ages", flags=["Free admission", "All ages", "Cultural tradition", "Family activities"], communities=["Latino / Hispanic", "Indigenous"], art="community", notable=True),
    "2002486517078": cfg("golden-ghouls-drag-brunch-milk-2026", ["Halloween", "Fall"], ["Drag brunch", "Comedy", "Nightlife"], ["Live Music & Performance", "Nightlife & Parties", "Food & Drink"], "Dorothy, Blanche and Rose get a Halloween drag-brunch send-up at MILK+, with Golden Girls costumes and camp encouraged.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Drag performance", "Brunch"], communities=["LGBTQ+"], art="nightlife"),
    "2002098618864": cfg("michelada-fest-salt-lake-2026", ["Día de los Muertos", "Fall"], ["Music festival", "Food and drink", "Car show"], ["Live Music & Performance", "Food & Drink", "Community & Culture"], "A Día de los Muertos edition of Michelada Fest mixes live music, a car-show atmosphere and elaborate micheladas at the 801 Event Center.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Alcohol-centered", "Live music"], communities=["Latino / Hispanic"], art="nightlife"),
    "1991018082682": cfg("manual-cinema-fourth-witch-weber-state-2026", ["Halloween", "Fall"], ["Shadow puppetry", "Theater", "Live music"], ["Live Music & Performance", "Community & Culture"], "Manual Cinema retells Macbeth through handmade shadow puppetry, live music and cinematic stagecraft in a visually inventive touring production.", age="All ages", flags=["Free admission", "All ages", "Indoor", "Shadow puppetry"], art="performance"),
    "1998504931047": cfg("pumpkin-smash-food-drive-glover-nursery-2026", ["Fall"], ["Pumpkin smash", "Food drive", "Family activity"], ["Kids & Family", "Giving & Volunteering", "Community & Culture"], "Bring spent pumpkins to Glover Nursery for an exuberant post-Halloween smash while collecting food for local hunger relief.", age="All ages", flags=["Free admission", "All ages", "Outdoor", "Food donations encouraged"], art="community"),
    "1999738192766": cfg("goetia-cabaret-demon-variety-show-2026", ["Halloween", "Fall"], ["Cabaret", "Aerial arts", "Burlesque"], ["Live Music & Performance", "Nightlife & Parties"], "A demonology-inspired cabaret fills the Salt Lake Masonic Temple with aerial arts, burlesque and dark theatrical spectacle.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Aerial arts", "Burlesque"], art="performance"),
    "1999719560035": cfg("drakes-hollow-immersive-fantasy-tavern-2026", ["Fall"], ["Immersive theater", "Fantasy / Fandom", "Cidery event"], ["Nightlife & Parties", "Live Music & Performance", "Food & Drink"], "Thieves Guild Cidery becomes a participatory fantasy tavern of characters, magic, mystery and improvised story for one evening.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Immersive experience", "Cidery"], art="nightlife"),
    "2003209999032": cfg("witchy-friendsgiving-girls-table-2026", ["Thanksgiving", "Fall"], ["Friendsgiving", "Craft social", "Potluck"], ["Community & Culture", "Food & Drink", "Workshops & Learning"], "A cozy, witchy Friendsgiving combines a potluck dinner, DIY oracle cards and a bookish make-new-friends format.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Potluck", "Craft activity"], communities=["Women-centered"], art="workshop"),
    "2002773146394": cfg("creators-collective-mistletoe-market-2026", ["Christmas", "Fall"], ["Holiday market", "Local makers", "Santa visit"], ["Markets & Shopping", "Kids & Family", "Food & Drink"], "Local makers, small businesses and food trucks fill The Loft Studio, with a midday Santa visit built into the market.", age="All ages", flags=["Free admission", "All ages", "Indoor", "Santa appearance"], art="market"),
    "2002765395210": cfg("lights-on-at-the-gateway-2026", ["Christmas", "Fall"], ["Holiday lights", "Live entertainment", "Community celebration"], ["Lights & Displays", "Live Music & Performance", "Kids & Family"], "The Gateway switches on its holiday lights with live entertainment, food, hot drinks and seasonal cocktails in Olympic Legacy Plaza.", age="All ages", flags=["Free admission", "All ages", "Outdoor", "Live entertainment"], art="community", notable=True),
    "2002954774649": cfg("foster-care-indigenous-fashion-show-2026", ["Native American Heritage Month", "Fall"], ["Indigenous fashion", "Community fundraiser", "Runway show"], ["Community & Culture", "Live Music & Performance", "Giving & Volunteering"], "The Urban Indian Center hosts its fourth runway show pairing Indigenous design and artistry with support for Native children and families touched by foster care.", flags=["Indoor", "Runway show", "Fundraiser"], communities=["Indigenous"], art="performance"),
    "2001095386168": cfg("university-place-gingerbread-competition-2026", ["Christmas", "Fall"], ["Gingerbread competition", "Holiday craft", "Community display"], ["Workshops & Learning", "Kids & Family", "Community & Culture"], "Registration opens for University Place's ninth community gingerbread competition, giving builders time to plan an edible holiday showpiece.", age="All ages", flags=["All ages", "Registration required", "Competition entry"], art="workshop"),
    "2001006426086": cfg("ultimate-litrpg-side-quest-dragonsteel-2026", ["Winter"], ["Fantasy / Fandom", "Books", "Social meetup"], ["Community & Culture", "Nightlife & Parties"], "A low-cost pre-game for Dragonsteel gives LitRPG readers and creators a casual place to meet before the convention rush.", flags=["Indoor", "Fandom meetup", "Dragonsteel week"], art="community"),
    "2003376725716": cfg("little-artist-big-christmas-2026", ["Christmas", "Winter"], ["Kids art workshop", "Gift making", "Holiday craft"], ["Kids & Family", "Workshops & Learning"], "Kids spend 90 minutes painting handmade Christmas gifts in a guided studio session designed around giving their finished work to family.", age="Children; see organizer listing for participating ages", flags=["Indoor", "Reservation required", "Materials included"], art="workshop"),
    "1991945879748": cfg("vivaldi-by-candlelight-titans-baroque-2026", ["Winter"], ["Classical concert", "Candlelight concert", "Baroque music"], ["Live Music & Performance"], "Vivaldi, Bach and Handel anchor an intimate candlelit program of Baroque showpieces at First United Methodist Church.", flags=["Indoor", "Candlelight", "Reserved tickets"], art="performance"),
    "1998895378887": cfg("salt-lake-city-princess-day-2026", ["Winter"], ["Character meet-and-greet", "Kids activity", "Performance"], ["Kids & Family", "Live Music & Performance"], "Costumed princess characters lead songs, stories, dances and crafts during a structured meet-and-greet for young fans.", age="Children and families", flags=["Indoor", "Timed sessions", "Costumes welcome"], art="performance"),
    "2003248383842": cfg("mapleton-dickensian-festival-2026", ["Christmas", "Winter"], ["Dickensian festival", "Dinner event", "Costumed performance"], ["Community & Culture", "Food & Drink", "Live Music & Performance"], "A ticketed evening of period costumes, carols and Dickens-inspired holiday atmosphere turns a Mapleton event venue into a Victorian Christmas gathering.", flags=["Indoor", "Costumes", "Dinner event", "Worth the drive"], art="performance"),
    "2002228814282": cfg("forgotten-carols-musical-slc-2026", ["Christmas", "Winter"], ["Christmas musical", "Theater", "Family tradition"], ["Live Music & Performance", "Kids & Family"], "The staged musical adaptation of Michael McLean's The Forgotten Carols returns with original songs, humor and a redemptive Christmas story.", age="All ages", flags=["All ages", "Indoor", "Matinee"], art="performance"),
    "1988736456276": cfg("slc-nye-masquerade-ball-2026", ["New Year", "Winter"], ["New Year's Eve", "Masquerade ball", "Dance party"], ["Nightlife & Parties", "Food & Drink", "Live Music & Performance"], "Salt Lake's long-running formal masquerade fills The Depot with a DJ, mask and dance contests, strolling performers, a midnight countdown and balloon drop.", age="Adults-focused; organizer does not state a minimum age", flags=["Adults-focused", "Indoor", "Formal dress required", "Cash bars", "Midnight countdown"], art="nightlife", notable=True, schedule_note="The organizer's detailed schedule says doors open at 8 PM; Eventbrite currently displays a 9 PM ticket start. Use the organizer schedule for arrival."),
}


def money(value):
    amount = float(value)
    return f"${amount:,.2f}".rstrip("0").rstrip(".")


def price_text(source):
    availability = source.get("ticketAvailability") or {}
    low = availability.get("minimum")
    high = availability.get("maximum")
    low_value = float(low.split()[0]) if low else None
    high_value = float(high.split()[0]) if high else low_value
    if source.get("isFree") or (low_value == 0 and high_value == 0):
        return "Free", True, 1
    if low_value == 0 and high_value:
        return f"Free admission; paid options to {money(high_value)} all-in", True, 2
    if low_value is None:
        return "See organizer ticket page", False, 0
    label = f"{money(low_value)} all-in" if low_value == high_value else f"{money(low_value)}–{money(high_value)} all-in"
    return label, False, 2 if high_value <= 20 else 3 if high_value <= 60 else 4


def format_time(value):
    dt = datetime.fromisoformat(value)
    return dt.strftime("%-I:%M %p").replace(":00", "")


def format_date(value):
    dt = datetime.fromisoformat(value)
    return dt.strftime("%b %-d")


def public_region(city):
    if city in {"Salt Lake City", "Murray", "South Jordan", "West Valley City", "Draper", "South Salt Lake", "Sandy", "Midvale"}:
        return "Salt Lake Metro"
    if city in {"Layton", "Woods Cross", "Bountiful", "Farmington"}:
        return "Davis County"
    if city in {"American Fork", "Provo", "Lehi", "Mapleton", "Orem", "Pleasant Grove"}:
        return "Utah County"
    if city in {"Ogden", "Huntsville"}:
        return "Ogden, Weber & Morgan"
    if city == "Park City":
        return "Park City & Wasatch Back"
    return "Eastern Utah" if city == "Hanksville" else "Statewide / Other"


def download_photo(source, slug):
    image = source.get("image") or {}
    url = image.get("url")
    if not url:
        return None
    target = ROOT / "assets" / "photos" / f"eventbrite-{slug}.webp"
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=45) as response, tempfile.NamedTemporaryFile(suffix=".img") as temp:
            temp.write(response.read())
            temp.flush()
            subprocess.run(["convert", temp.name, "-auto-orient", "-resize", "1600x1600>", "-strip", "-quality", "82", str(target)], check=True)
    dimensions = subprocess.check_output(["identify", "-format", "%w %h", str(target)], text=True).split()
    organizer = (source.get("organizer") or {}).get("name") or "Event organizer"
    return {
        "src": f"assets/photos/{target.name}",
        "alt": f"Official event image for {source['name']}.",
        "credit": organizer,
        "creditUrl": source["url"],
        "sourceUrl": url,
        "usageType": "official_organizer_image",
        "caption": "Official event image",
        "reviewedOn": CHECKED,
        "width": int(dimensions[0]),
        "height": int(dimensions[1]),
        "rightsNote": "Selected from the organizer's official ticket listing for editorial event-listing use.",
    }


def make_event(source, details, source_row):
    start = datetime.fromisoformat(source["start"]["local"])
    end = datetime.fromisoformat(source["end"]["local"])
    date = start.date().isoformat()
    end_date = end.date().isoformat()
    price, is_free, cost_count = price_text(source)
    city = (source.get("venue") or {}).get("address", {}).get("city") or "Utah"
    venue = source.get("venue") or {}
    address = venue.get("address", {}).get("localized_address_display") or city
    times = f"{format_time(source['start']['local'])}–{format_time(source['end']['local'])}"
    if details["scheduleNote"] and source["id"] == "1988736456276":
        times = "Doors 8 PM; program 9 PM–1 AM"
    occurrence_dates = [date]
    if (end - start).total_seconds() >= 86400:
        occurrence_dates = [(start.date() + timedelta(days=offset)).isoformat() for offset in range((end.date() - start.date()).days + 1)]
    primary = details["holidays"][0]
    theme = {
        "Día de los Muertos": "dayofdead", "New Year": "newyear", "Native American Heritage Month": "indigenous",
        "Veterans Day": "veterans", "Hispanic Heritage Month": "hispanic", "Samhain": "yule", "Yule & Solstice": "yule",
    }.get(primary, primary.lower().replace(" ", "-"))
    seasonal = ROOT / "assets" / "art" / "seasonal" / f"{theme}-{details['artKey']}.svg"
    placeholder = f"assets/art/seasonal/{theme}-{details['artKey']}.svg" if seasonal.exists() else f"assets/art/{details['artKey']}.svg"
    flags = list(dict.fromkeys(details["flags"] + (["Free admission"] if is_free else [])))
    photo = download_photo(source, details["slug"])
    event = {
        "id": details["slug"], "Event / attraction": source["name"].replace("  ", " "),
        "Region": city, "Category": ", ".join(details["categories"]), "First date": date,
        "2026 schedule": format_date(source["start"]["local"]) if date == end_date else f"{format_date(source['start']['local'])}–{format_date(source['end']['local'])}",
        "Times": times, "Price": price, "Cost": "", "Age": details["age"], "Intensity": "",
        "Location": f"{venue.get('name')}, {address}" if venue.get("name") and venue.get("name") not in address else address,
        "Status": "Confirmed 2026", "Why / thoughts": details["description"], "Website": source["url"],
        "Social profile": "", "Extra notes": "", "categories": details["categories"], "sourceCategories": details["categories"],
        "ghostCount": 0, "costCount": cost_count, "isWatch": False, "artKey": details["artKey"], "socials": [], "photo": photo,
        "sourceRegion": city, "publicRegion": public_region(city), "publicTypes": details["publicTypes"], "sponsored": False,
        "holidays": details["holidays"], "primaryHoliday": primary, "startDate": date, "endDate": end_date,
        "travelTier": "Worth the drive" if "Worth the drive" in flags else "Core / easy day trip", "lastVerified": CHECKED,
        "qaFlags": "", "timezone": source["start"]["timezone"], "sourceRow": source_row, "flags": flags, "isFree": is_free,
        "rating": None, "occurrenceDates": occurrence_dates, "scheduleConfidence": "verified-dates", "scheduleNote": details["scheduleNote"],
        "communities": details["communities"], "theme": theme, "placeholder": placeholder, "notable_event": details["notable"],
        "seasons": [season for season in ("Fall", "Winter", "Spring", "Summer") if season in details["holidays"]],
        "accessibility": details["accessibility"],
        "researchEvidence": {"checkedOn": CHECKED, "sourceUrl": source["url"], "method": "Discovered in the statewide Eventbrite crawl, then verified through the public event API with organizer, venue, ticket-availability and official-image details."},
    }
    if source["id"] == "1986090600450":
        event.update({
            "Times": "Fri doors 8 AM; sessions 9 AM & 4 PM. Sat–Sun doors 9 AM; sessions 10 AM & 7 PM",
            "startTimesByDate": {
                "2026-10-16": "08:00",
                "2026-10-17": "09:00",
                "2026-10-18": "09:00",
            },
            "scheduleNote": "The stadium closes between the morning and evening sessions; doors reopen at 3 PM Friday and 6 PM Saturday and Sunday.",
            "accessibility": {
                "summary": "All admission types are seated, and ADA seating areas will be available."
            },
        })
    return event


def main():
    raw = DATA_PATH.read_text()
    data = json.loads(raw[len(PREFIX):].rstrip()[:-1])
    sources = {event["id"]: event for event in json.loads(SOURCE_PATH.read_text())["events"]}
    by_id = {event["id"]: event for event in data["events"]}
    next_row = max((event.get("sourceRow", 0) for event in data["events"]), default=0) + 1
    published = []
    for eventbrite_id, details in SELECTED.items():
        source = sources[eventbrite_id]
        event = make_event(source, details, by_id.get(details["slug"], {}).get("sourceRow", next_row))
        if details["slug"] in by_id:
            by_id[details["slug"]].update(event)
        else:
            data["events"].append(event)
            by_id[details["slug"]] = event
            next_row += 1
        published.append(details["slug"])

    # Replace the stale winter-market record with the current organizer listing.
    current = sources["1978941183351"]
    old = by_id["always-queer-market-winter-market"]
    old.update({
        "Event / attraction": "Always Queer Market — November Pop-Up", "First date": "2026-11-21", "startDate": "2026-11-21",
        "endDate": "2026-11-21", "2026 schedule": "Nov 21", "Times": "12–4 PM", "Price": "Free", "Age": "All ages",
        "Status": "Confirmed 2026", "Website": current["url"], "Why / thoughts": "A compact pop-up market of locally made art, books and gifts from queer Utah creators inside Under the Umbrella.",
        "Extra notes": "", "lastVerified": CHECKED, "flags": ["Free admission", "All ages", "Indoor", "Local makers"],
        "occurrenceDates": ["2026-11-21"], "holidays": ["Pride", "Fall"], "primaryHoliday": "Pride", "theme": "pride", "seasons": ["Fall"],
        "photo": download_photo(current, "always-queer-market-november-2026"), "scheduleConfidence": "verified-dates", "scheduleNote": "",
        "researchEvidence": {"checkedOn": CHECKED, "sourceUrl": current["url"], "method": "Replaced the older event instance with the current 2026 organizer listing and verified its date, hours, free admission and official image."},
    })

    data["meta"]["updated"] = "October 13, 2026"
    data["meta"]["eventCount"] = len(data["events"])
    data["meta"]["confirmedCount"] = sum(not e.get("isWatch") for e in data["events"])
    data["meta"]["watchCount"] = sum(bool(e.get("isWatch")) for e in data["events"])
    data["meta"]["realImageCount"] = sum(bool(e.get("photo")) for e in data["events"])
    data["meta"]["localPhotoListings"] = data["meta"]["realImageCount"]
    data["meta"]["accessibilityListings"] = sum(bool(e.get("accessibility")) for e in data["events"])
    DATA_PATH.write_text(PREFIX + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

    ledger = {
        "checkedOn": CHECKED, "crawl": "research/eventbrite-crawl-2026-10-13.json",
        "deepReview": "research/eventbrite-shortlist-2026-10-13.json", "publishedNewIds": published,
        "correctedExistingIds": ["always-queer-market-winter-market"],
        "heldForFurtherReview": ["Nightmare On Main", "Witching Hour", "Dolly & Denim at the Utah Capitol", "Jingle Bell Jog 5K"],
        "reasonHeld": "The current discovery record did not provide enough practical detail to publish confidently without another organizer/ticket-depth check.",
        "result": {"newEvents": len(published), "correctedEvents": 1, "totalEvents": len(data["events"]), "localPhotoListings": data["meta"]["localPhotoListings"]},
    }
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(f"Published {len(published)} new Eventbrite discoveries and corrected 1 stale listing; {len(data['events'])} total events.")


if __name__ == "__main__":
    main()
