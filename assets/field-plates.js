/* Utah Every Season generative Field Plates: reusable taxonomy-driven no-photo artwork. */
(()=>{"use strict";
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function code(e){let h=2166136261;for(const ch of String(e?.id||e?.["Event / attraction"]||"field")){h^=ch.charCodeAt(0);h=Math.imul(h,16777619)}return Math.abs(h)>>>0}
const PLATE_PALETTES={
 halloween:{paper:"#fff5e6",ink:"#211b22",accent:"#ef5a29",season:"#a92d34"},
 fall:{paper:"#fcf5e8",ink:"#352818",accent:"#d87a2d",season:"#794521"},
 thanksgiving:{paper:"#fcf5e8",ink:"#352818",accent:"#d87a2d",season:"#794521"},
 christmas:{paper:"#f5f7ee",ink:"#132f25",accent:"#ef5a29",season:"#a32c3a"},
 winter:{paper:"#f0f7fb",ink:"#172e41",accent:"#ef5a29",season:"#38627a"},
 hanukkah:{paper:"#f0f5fc",ink:"#172d4a",accent:"#e7cd7a",season:"#265386"},
 diwali:{paper:"#fff4ee",ink:"#3b1931",accent:"#ffc459",season:"#973d68"},
 yule:{paper:"#f2f5e9",ink:"#23372b",accent:"#ddce81",season:"#3e6350"},
 newyear:{paper:"#f7f2fa",ink:"#292037",accent:"#f5d981",season:"#694983"},
 kwanzaa:{paper:"#f7f5eb",ink:"#222720",accent:"#acd184",season:"#a63436"},
 pride:{paper:"#f7f2fa",ink:"#292037",accent:"#ef5a29",season:"#694983"},
 dayofdead:{paper:"#fbf1f8",ink:"#34213f",accent:"#f7b64d",season:"#7c3658"},
 spring:{paper:"#f0f7eb",ink:"#193426",accent:"#ef5a29",season:"#6f8e4f"},
 summer:{paper:"#f8f5e8",ink:"#163b4e",accent:"#ef5a29",season:"#2e7287"},
 core:{paper:"#f5f0e4",ink:"#17221d",accent:"#ef5a29",season:"#785466"}
};
function paletteFor(e){
 const occasion=[e?.primaryHoliday,...(e?.holidays||[]),...(e?.seasons||[])].filter(Boolean).join(" · ").toLowerCase();
 if(/d[ií]a de los muertos|day of the dead/.test(occasion))return PLATE_PALETTES.dayofdead;
 if(/halloween/.test(occasion))return PLATE_PALETTES.halloween;
 if(/hanukkah/.test(occasion))return PLATE_PALETTES.hanukkah;
 if(/diwali/.test(occasion))return PLATE_PALETTES.diwali;
 if(/yule|solstice/.test(occasion))return PLATE_PALETTES.yule;
 if(/kwanzaa/.test(occasion))return PLATE_PALETTES.kwanzaa;
 if(/new year/.test(occasion))return PLATE_PALETTES.newyear;
 if(/pride/.test(occasion))return PLATE_PALETTES.pride;
 if(/christmas|advent/.test(occasion))return PLATE_PALETTES.christmas;
 if(/thanksgiving|fall|autumn/.test(occasion))return PLATE_PALETTES.fall;
 if(/winter/.test(occasion))return PLATE_PALETTES.winter;
 if(/spring/.test(occasion))return PLATE_PALETTES.spring;
 if(/summer/.test(occasion))return PLATE_PALETTES.summer;
 return PLATE_PALETTES.core;
}
const SPECIAL=[
  [/d[ií]a de los muertos|day of the dead/i,["marigold","MARIGOLD / REMEMBRANCE"]],
  [/diwali/i,["diya","DIYA / LIGHT"]],
  [/hanukkah/i,["menorah","MENORAH / LIGHT"]],
  [/yule|solstice/i,["solstice","SOLSTICE / SUN"]],
  [/pride/i,["prism","WILDFLOWER / PRISM"]]
];
function specimen(e){
 const occasion=[e?.primaryHoliday,...(e?.holidays||[])].filter(Boolean).join(" · ");
 for(const [re,out] of SPECIAL)if(re.test(occasion))return{id:out[0],label:out[1]};
 const hay=[...(e?.publicTypes||[]),e?.Category,e?.["Event / attraction"]].filter(Boolean).join(" · ");
 const rules=[
  [/film|cinema/i,["film","FILM / FRAME"]],
  [/parade|procession/i,["parade","PENNANT / PROCESSION"]],
  [/convention|fandom|fanx|anime|comic/i,["fandom","BADGE / FANDOM"]],
  [/residential|home haunt|drive-through|drive by|display/i,["house","HOUSE / DISPLAY"]],
  [/haunt|scare|ghost|paranormal/i,["moth","NIGHT MOTH / HAUNT"]],
  [/farm|harvest|pumpkin|corn maze/i,["pumpkin","GOURD / HARVEST"]],
  [/light/i,["lights","STAR / LIGHTS"]],
  [/market|shopping/i,["market","MARKET / STALL"]],
  [/music|performance|theater|theatre|ballet|concert|comedy|cabaret|dance/i,["performance","CURTAIN / PERFORMANCE"]],
  [/food|drink|dining/i,["food","BOTANICAL / TABLE"]],
  [/active|outdoor|sports|scenic|train|nature|garden|zoo/i,["outdoors","RIDGELINE / OUTDOORS"]],
  [/workshop|learning|library|education|craft/i,["workshop","TOOLS / MAKING"]],
  [/nightlife|party|social/i,["nightlife","MOON / NIGHTLIFE"]],
  [/santa|family|christmas/i,["pine","EVERGREEN / FAMILY"]],
  [/giving|volunteer|fundraiser|charity/i,["giving","HEART / GIVING"]],
  [/community|culture|festival|historic|museum/i,["wildflower","WILDFLOWER / COMMUNITY"]]
 ];
 for(const [re,out] of rules)if(re.test(hay))return{id:out[0],label:out[1]};
 return{id:"wildflower",label:"WILDFLOWER / FIELD NOTE"};
}
const DRAW={
 moth:`<g class="specimen"><path d="M80 34c-8-18-32-22-47-8 1 23 16 39 38 41M80 34c8-18 32-22 47-8-1 23-16 39-38 41M72 45c-18 3-30 16-32 35 17 6 29 2 39-11M88 45c18 3 30 16 32 35-17 6-29 2-39-11"/><path d="M80 31v55M80 34c-8-11-14-14-20-16M80 34c8-11 14-14 20-16"/><circle cx="80" cy="31" r="4"/></g>`,
 pumpkin:`<g class="specimen"><path d="M80 34c-4-10 1-17 8-22M80 37c-29-15-52 6-47 35 5 27 30 35 47 22M80 37c29-15 52 6 47 35-5 27-30 35-47 22M80 37c-17 2-24 22-20 41 3 14 10 20 20 16M80 37c17 2 24 22 20 41-3 14-10 20-20 16"/><path d="M84 17c8 3 15 1 20-5"/></g>`,
 lights:`<g class="specimen"><path d="M24 34c35 18 75 18 112 0"/><circle cx="34" cy="40" r="6"/><circle cx="58" cy="48" r="6"/><circle cx="84" cy="49" r="6"/><circle cx="110" cy="45" r="6"/><circle cx="132" cy="36" r="6"/><path d="m80 61 7 15 17 2-13 11 4 17-15-9-15 9 4-17-13-11 17-2Z"/></g>`,
 market:`<g class="specimen"><path d="M35 47h90v55H35zM28 47l12-27h80l12 27M28 47h104M55 20v27M80 20v27M105 20v27"/><path d="M52 102V69h28v33M92 69h20v16H92z"/></g>`,
 performance:`<g class="specimen"><path d="M31 21h98M39 21c0 28 9 49 28 64M121 21c0 28-9 49-28 64M39 21v81M121 21v81"/><path d="M67 85c8-6 18-8 26 0M72 65c3 4 7 4 10 0M94 65c-3 4-7 4-10 0"/></g>`,
 food:`<g class="specimen"><circle cx="80" cy="70" r="34"/><circle cx="80" cy="70" r="23"/><path d="M80 46c-8-13-5-24 5-31M84 23c12-6 22-3 28 7-12 7-22 4-28-7M49 95l-15 16M111 95l15 16"/></g>`,
 outdoors:`<g class="specimen"><circle cx="117" cy="28" r="13"/><path d="m20 101 35-55 20 29 18-39 47 65H20Z"/><path d="m43 82 12-18 8 12M82 74l11-20 15 21"/></g>`,
 workshop:`<g class="specimen"><path d="m40 99 56-70 14 11-56 70-20 6Z"/><path d="m96 29 8-10 14 11-8 10M34 116l6-17 14 11Z"/><circle cx="117" cy="82" r="14"/><circle cx="117" cy="108" r="14"/><path d="m107 92-41-41M107 98 65 113"/></g>`,
 nightlife:`<g class="specimen"><path d="M99 25c-27 2-43 24-37 49 6 26 32 39 56 27-36 2-52-43-19-76Z"/><path d="m38 34 4 9 10 1-8 7 3 10-9-6-9 6 3-10-8-7 10-1ZM116 72l3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1Z"/></g>`,
 pine:`<g class="specimen"><path d="M80 14 52 50h16L43 82h22l-30 28h90L95 82h22L92 50h16Z"/><path d="M80 14v96M71 110h18"/><path d="m80 9 3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1Z"/></g>`,
 giving:`<g class="specimen"><path d="M80 104C31 74 35 37 58 34c12-2 19 6 22 14 3-8 10-16 22-14 23 3 27 40-22 70Z"/><path d="M24 88c15-7 26-6 39 2M136 88c-15-7-26-6-39 2M24 88l13 20 28-9M136 88l-13 20-28-9"/></g>`,
 wildflower:`<g class="specimen"><path d="M80 108V58M80 80c-15-12-27-12-37-5 10 13 22 17 37 5M80 92c15-12 27-12 37-5-10 13-22 17-37 5"/><circle cx="80" cy="42" r="10"/><circle cx="80" cy="24" r="14"/><circle cx="98" cy="37" r="14"/><circle cx="91" cy="57" r="14"/><circle cx="69" cy="57" r="14"/><circle cx="62" cy="37" r="14"/></g>`,
 film:`<g class="specimen"><rect x="29" y="26" width="102" height="72" rx="3"/><path d="M29 44h102M29 80h102M48 26v18M68 26v18M92 26v18M112 26v18M48 80v18M68 80v18M92 80v18M112 80v18"/><path d="m69 55 28 13-28 13Z"/></g>`,
 parade:`<g class="specimen"><path d="M44 108V19M44 25c29-14 48 13 78-2v48c-30 15-49-13-78 2"/><path d="M61 91h62M61 101h44"/></g>`,
 fandom:`<g class="specimen"><path d="m80 15 42 24v48l-42 24-42-24V39Z"/><circle cx="80" cy="59" r="17"/><path d="M51 94c7-16 18-24 29-24s22 8 29 24M73 56h14"/></g>`,
 house:`<g class="specimen"><path d="m27 62 53-43 53 43M39 55v54h82V55M69 109V78h22v31M51 68h14v14H51zM97 68h14v14H97z"/><path d="M25 109h110"/></g>`,
 marigold:`<g class="specimen"><path d="M80 108V66M80 83c-13-9-25-8-34-1 9 12 20 14 34 1M80 94c13-9 25-8 34-1-9 12-20 14-34 1"/><circle cx="80" cy="43" r="9"/><circle cx="80" cy="23" r="14"/><circle cx="99" cy="31" r="14"/><circle cx="103" cy="51" r="14"/><circle cx="90" cy="65" r="14"/><circle cx="70" cy="65" r="14"/><circle cx="57" cy="51" r="14"/><circle cx="61" cy="31" r="14"/></g>`,
 diya:`<g class="specimen"><path d="M34 72c16 31 76 31 92 0H34Z"/><path d="M80 69c-20-15-12-34 0-50 12 16 20 35 0 50Z"/><path d="M45 96h70M55 106h50"/></g>`,
 menorah:`<g class="specimen"><path d="M80 105V38M47 105h66M80 70c-24 0-35-16-35-34M80 70c24 0 35-16 35-34M80 82c-36 0-51-21-51-45M80 82c36 0 51-21 51-45M80 93c-47 0-62-25-62-51M80 93c47 0 62-25 62-51"/><path d="M80 28c-7-8-4-16 0-22 4 6 7 14 0 22ZM45 31c-7-8-4-16 0-22 4 6 7 14 0 22ZM115 31c-7-8-4-16 0-22 4 6 7 14 0 22ZM29 32c-7-8-4-16 0-22 4 6 7 14 0 22ZM131 32c-7-8-4-16 0-22 4 6 7 14 0 22ZM18 37c-7-8-4-16 0-22 4 6 7 14 0 22ZM142 37c-7-8-4-16 0-22 4 6 7 14 0 22Z"/></g>`,
 solstice:`<g class="specimen"><circle cx="80" cy="62" r="25"/><path d="M80 13v16M80 95v16M31 62h16M113 62h16M45 27l11 11M104 86l11 11M115 27l-11 11M56 86 45 97"/><path d="M34 112c28-14 64-14 92 0"/></g>`,
 prism:`<g class="specimen"><path d="m80 18 42 82H38Z"/><path d="M17 62h44M99 62h44"/><path d="M100 54l33-16M102 62l37-2M100 70l33 17"/><path d="M80 108V78M80 91c-12-9-23-8-31-2 8 11 18 13 31 2"/></g>`
};
const CONTOURS=[
 `<path d="M-12 35C20 6 51 8 70 30s52 30 102-1M-8 52c30-25 57-26 79-6s57 27 103-5M-4 70c27-19 55-20 78-3s57 23 95-2M12 93c24-13 47-12 66 1s46 16 77 2"/>`,
 `<path d="M-8 27c38 13 53 40 47 61s10 34 42 36M9 15c40 18 56 47 49 71s8 37 41 42M116-9c-24 25-25 49-5 68s23 39 5 69M136-5c-20 23-19 45 2 62s26 36 13 61"/>`,
 `<path d="M18-5c-8 28 4 48 36 58s46 29 39 59M38-8c-4 23 8 39 37 49s45 27 42 54M102 6c27 11 41 31 36 54s4 40 28 52M112 23c18 8 27 21 24 38s5 29 23 38"/>`
];
function svg(e,colors={}){
 const s=specimen(e),variant=code(e)%CONTOURS.length;
 const paper=colors.paper||"var(--plate-paper,#f5f0e4)",ink=colors.ink||"var(--plate-ink,#17221d)",accent=colors.accent||"var(--plate-accent,#ef5a29)",season=colors.season||"var(--plate-season,#785466)";
 return `<svg class="field-plate-art" viewBox="0 0 160 120" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><rect width="160" height="120" fill="${paper}"/><g fill="none" stroke="${season}" stroke-width=".7" opacity=".22">${CONTOURS[variant]}</g><g fill="none" stroke="${ink}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${DRAW[s.id]||DRAW.wildflower}</g><circle cx="145" cy="16" r="6" fill="${accent}"/><circle cx="145" cy="16" r="2" fill="${paper}"/><path d="M145 5v22M134 16h22" stroke="${ink}" stroke-width=".8" opacity=".65"/></svg>`;
}
function html(e){
 const s=specimen(e),plate=String(code(e)%10000).padStart(4,"0"),occasion=e?.primaryHoliday||e?.seasons?.[0]||"UTAH",region=e?.publicRegion||e?.Region||"UTAH",p=paletteFor(e);
 const style=`--plate-paper:${p.paper};--plate-ink:${p.ink};--plate-accent:${p.accent};--plate-season:${p.season}`;
 return `<div class="field-plate" data-specimen="${esc(s.id)}" style="${style}"><span class="sr-only">No event photograph is available. Illustrated Utah Every Season field plate.</span><div class="field-plate-top"><span>FIELD PLATE / ${plate}</span><span>NO EVENT PHOTO</span></div>${svg(e)}<div class="field-plate-bottom"><strong>${esc(s.label)}</strong><span>${esc(occasion)} · ${esc(region)}</span></div></div>`;
}
function dataUrl(e,colors){return "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(svg(e,colors))}
window.FIELD_PLATES={specimen,svg,html,dataUrl,code,paletteFor};
})();
