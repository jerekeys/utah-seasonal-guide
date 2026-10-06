'use strict';
// Collections describe experiences; they do not imply admission or access policies.
window.VIBE_GUIDES = [
 ['spooky-not-scary','Spooky, not scary','Halloween atmosphere, gentle displays and themed outings without committing to a haunted house.',{names:'Halloween Cruise|Halloween Lift Rides|Little Haunts|Spooky Light Show|Autumn Apparitions|Pumpkin House|Pumpkin Walk|Pirate Yard'}],
 ['serious-scares','Serious scares','Haunted attractions with intense sets, live actors and startling effects. Check each option’s age and contact rules.',{scare:4}],
 ['date-night','Date night','Scenic evenings, atmospheric performances and special meals that give you something to enjoy together.',{names:'Halloween Lift Rides|Halloween Cruise|Ballet West|Franck|Garden After Dark|Freakshow|Luminaria|Candlelight|Murder at the Juice'}],
 ['unusual','Only-in-Utah oddities','Pumpkin boats, oversized displays and local traditions worth seeking out for their unusual character.',{names:'Pumpkin House|Bison Roundup|Trailing of the Sheep|Pumpkin Regatta|Tunnel of Terror|Giant Pumpkin Drop|Peach Days'}],
 ['family','Bring the family','Outings listed for families, children or all ages. Read the detail page for age recommendations, noise and optional scares.',{audience:'famil|all ages|children|youth'}],
 ['queer-joy','Queer joy','Pride celebrations, drag performances and gatherings explicitly connected to LGBTQ+ communities.',{text:'LGBTQ|Pride|drag brunch|HalloQueen|Horror Icons|Sapphic'}],
 ['animals','Animal encounters','Meet live animals, watch wildlife or learn about conservation. Evening zoo lights do not necessarily include animal viewing.',{names:'Agave After Dark|Reading with Raptors|Birds in the Lab|Bison Roundup|Creature Crawl|Creatures of the Night'}],
 ['dogs','Bring the dog','Dog-focused parades, costume gatherings and designated dog sessions. Check the organizer’s leash and entry rules.',{names:'Hounds & Haunts|Dog Daze|Dogden|Purple Paw|Howl-O-Ween'}],
 ['witchy','Witchy outings','Witch-themed markets, crafts, performances and costume nights, from playful family programs to adult evenings.',{text:'witch|WitchFest|Puck.s Magical|spell jars|SpookyFest'}],
 ['books','Books and stories','Author events, storytelling, literary workshops and book-centered gatherings for readers and listeners.',{text:'bookstore|bookshop|author|storytelling|horror writing|Fear & Lust|Princess in Black|Hansel & Gretel|Spookytown'}],
 ['make-learn','Make or learn something','Hands-on crafts, classes and workshops where taking part is the point. Materials and registration vary.',{types:['Workshops & Learning']}],
 ['shows','Take in a show','Music, dance, theatre, comedy and film events with a performance to plan your visit around.',{types:['Live Music & Performance','Film & Screen']}],
 ['free','Free admission','Events with free entry. Food, purchases, rides, parking or optional activities may still cost extra.',{free:true}],
 ['active','Get moving','Races, hikes, skating and outdoor activities. Check the route, conditions and physical demands before booking.',{types:['Active & Outdoors']}],
 ['farm','Fall farms and pumpkins','Pumpkin patches, corn mazes, hayrides and harvest activities. Some farms sell separate haunted experiences.',{category:'Fall Farm / Pumpkin',names:'Harvest Moon|Peach Days'}],
 ['lights','Lights and wonder','Illuminated gardens, light walks and decorated displays. Expect different levels of walking and weather exposure.',{types:['Lights & Displays']}],
 ['food','Eat, drink and celebrate','Special meals, tastings and food-centered gatherings. Check what admission includes and whether alcohol changes entry rules.',{types:['Food & Drink']}],
 ['markets','Browse something different','Seasonal markets, handmade goods and unusual vendors. Browse freely where offered; purchases are separate.',{types:['Markets & Shopping']}],
 ['culture','Local traditions and cultural celebrations','Public festivals, heritage gatherings and traditions where you can experience local art, food, music and customs.',{types:['Community & Culture'],names:'Greek Festival|Festa Italiana|Harvest Moon|Día de los Muertos|Peach Days'}],
 ['quick-stop','A quick stop','Exterior displays, small exhibitions and other stops you can fit around dinner or a longer outing.',{names:'Tunnel of Terror|Autumn Apparitions|Pumpkin House|Granville Graveyard|Spooky Light Show|Haunt on Aster|Raven Manor'}],
 ['residential','Neighborhood Halloween displays','Decorated homes and residential haunts. Respect viewing hours, sidewalks, neighbors and private property.',{category:'Home Haunt / Display'}],
 ['road-trip','Make a day of it','Destination outings beyond the central metro area, with enough nearby ideas to start planning a longer visit.',{regions:['Southern Utah','Cache / Box Elder','Cedar / Iron County','Park City & Wasatch Back','Box Elder County','Eastern Utah']}],
 ['southern-utah','Southern Utah outings','Farms, displays and seasonal events around St. George, Cedar City and neighboring communities.',{regions:['Southern Utah']}],
 ['nightlife','A night out','Late-night parties, dance floors and costume gatherings. Minimum ages, ID checks and dress rules vary.',{types:['Nightlife & Parties']}],
 ['sensory','Sensory-friendly sessions','Specific sessions advertised as sensory-friendly. Read the accommodation details; this does not promise every part of a venue is quiet.',{flag:'Sensory-friendly'}],
 ['adaptive','Additional access support','Programs with advertised adaptive appointments or accommodations. Review eligibility and reserve where required.',{flag:'Adaptive appointments'}],
 ['give-back','Give a little back','Volunteer activities, community meals and charitable events where participation can support others.',{types:['Giving & Volunteering']}]
].map(([id,title,description,rule])=>({id,title,description,rule}));
window.matchesVibe = (e,v) => {
 const r=v.rule,text=['Event / attraction','Why / thoughts','Extra notes','Category','communities'].map(k=>String(e[k]||'')).join(' ');
 return !!((r.free&&e.isFree)||(r.scare&&/scare/i.test(e.rating?.type||'')&&+e.rating.value>=r.scare)||(r.audience&&new RegExp(r.audience,'i').test(e.Age))||(r.names&&new RegExp(r.names,'i').test(e['Event / attraction']))||(r.text&&new RegExp(r.text,'i').test(text))||(r.category&&String(e.Category||'').includes(r.category))||(r.types&&e.publicTypes.some(t=>r.types.includes(t)))||(r.regions&&r.regions.includes(e.publicRegion))||(r.flag&&e.flags.some(f=>f.toLowerCase()===r.flag.toLowerCase())));
};
