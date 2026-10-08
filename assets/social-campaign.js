(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.SOCIAL_CAMPAIGN=api;
})(typeof window!=='undefined'?window:globalThis,function(){
  const SEASONS=new Set(['Spring','Summer','Fall','Winter']);
  const SERIES={
    auto:{label:"Editor's next post",eyebrow:'THE FIELD EDIT',description:'Chooses the most useful series for the publish day instead of blending every idea into one generic list.'},
    weekend:{label:'The Weekend File',eyebrow:'THE WEEKEND FILE',description:'A Salt Lake-first weekend shortlist: major moments, one-day events and a varied mix of plans that feel worth acting on now.'},
    tonight:{label:'Tonight',eyebrow:'TONIGHT',description:'Low-friction plans actually happening tonight, led by Salt Lake options with concrete hours and a bias toward live or one-night experiences.'},
    free:{label:'Free This Weekend',eyebrow:'FREE THIS WEEKEND',description:'Genuinely free, useful weekend plans with a community-minded mix—not simply the usual paid attractions with a free edge case.'},
    topical:{label:'Right Now',eyebrow:'RIGHT NOW',description:'One coherent current holiday or cultural story, showing different ways to experience it rather than six versions of the same outing.'},
    lastchance:{label:'Last Chance',eyebrow:'LAST CHANCE',description:'Events and limited runs that are truly ending soon, ordered by urgency and usefulness.'},
    drive:{label:'Worth the Drive',eyebrow:'WORTH THE DRIVE',description:'Destination-worthy Utah outings where distance is the point; Salt Lake convenience is deliberately deprioritized.'},
    adults:{label:'Adults Focused',eyebrow:'GROWN-UP PLANS',description:'Verified 21+, nightlife, drinks and distinctly grown-up programming—not merely all-ages events adults could attend.'},
    kids:{label:'Events for Kids',eyebrow:'FOR KIDS',description:'Programming intentionally made for children and families, with age fit, scare level and practical timing considered.'},
    found:{label:'Found It',eyebrow:'FOUND IT',description:'Specific, unusual and under-the-radar discoveries that reward curiosity instead of repeating the biggest attractions.'},
    field:{label:"Editor's Field Guide",eyebrow:'THE FIELD GUIDE',description:'A Salt Lake-first editorial sampler balancing a headline, a timely one-off and several meaningfully different ways to go out.'}
  };
  const POLICY={
    weekend:{days:3,metroShare:.66},tonight:{days:0,metroShare:.66},free:{days:3,metroShare:.66},
    topical:{days:28,metroShare:.66},lastchance:{days:10,metroShare:.66},drive:{days:35,farShare:.80},
    adults:{days:28,metroShare:.66},kids:{days:28,metroShare:.66},found:{days:35,metroShare:.66},field:{days:14,metroShare:.66,futureShare:.83}
  };
  const clean=value=>String(value||'').replace(/\s+/g,' ').trim();
  const isoDate=value=>/^\d{4}-\d{2}-\d{2}$/.test(String(value||''))?String(value):'';
  const asDate=value=>new Date((isoDate(value)||'1970-01-01')+'T12:00:00Z');
  const addDays=(value,count)=>{const d=asDate(value);d.setUTCDate(d.getUTCDate()+count);return d.toISOString().slice(0,10)};
  const dayDiff=(from,to)=>Math.round((asDate(to)-asDate(from))/86400000);
  const inRange=(date,start,end)=>date>=start&&date<=end;
  const datesFor=event=>(event.occurrenceDates||[]).map(isoDate).filter(Boolean).sort();
  const nextDate=(event,anchor)=>datesFor(event).find(date=>date>=anchor)||'';
  const singleDay=event=>datesFor(event).length===1&&!/daily|weekly|monthly|recurr/i.test(clean(event.recurrence));
  const eventText=event=>[event['Event / attraction'],event['Why / thoughts'],event['Extra notes'],event.Times,event.Location,event.Age,event.artKey,...(event.publicTypes||[]),...(event.flags||[])].map(clean).join(' ');
  function weekendRange(anchor){
    const weekday=asDate(anchor).getUTCDay();
    if(weekday===0)return[anchor,anchor];
    if(weekday===6)return[anchor,addDays(anchor,1)];
    const start=addDays(anchor,(5-weekday+7)%7);
    return[start,addDays(start,2)];
  }
  function upcoming(events,anchor,days){
    const end=addDays(anchor,days);
    return events.filter(event=>!event.isWatch&&datesFor(event).some(date=>inRange(date,anchor,end)));
  }
  function strongestTopic(events,anchor,days=28){
    const counts=new Map();
    for(const event of upcoming(events,anchor,days))for(const tag of event.holidays||[]){
      if(!tag||SEASONS.has(tag))continue;
      const local=event.publicRegion==='Salt Lake Metro'?1.35:1;
      counts.set(tag,(counts.get(tag)||0)+local+(singleDay(event)?.2:0));
    }
    return [...counts].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]))[0]||['',0];
  }
  function resolveSeries(requested,events,anchor){
    if(requested&&requested!=='auto')return requested;
    const weekday=asDate(anchor).getUTCDay();
    if(weekday===4||weekday===5)return'weekend';
    if(weekday===6||weekday===0)return'tonight';
    const [,topicCount]=strongestTopic(events,anchor,21);
    if(weekday===2&&topicCount>=5)return'topical';
    if(weekday===3)return'found';
    return'field';
  }
  function windowFor(series,events,anchor){
    if(series==='weekend'||series==='free')return weekendRange(anchor);
    return[anchor,addDays(anchor,POLICY[series]?.days??14)];
  }
  const PROXIMITY={
    'Salt Lake Metro':4,'Davis County':3,'Park City & Wasatch Back':3,'Tooele':3,'Utah County':3,
    'Ogden, Weber & Morgan':2,'Cache / Box Elder':1,'Box Elder County':1,'Statewide / Other':1,
    'Eastern Utah':0,'Cedar / Iron County':0,'Southern Utah':0
  };
  function proximityLevel(event){return PROXIMITY[event.publicRegion]??1}
  function adultProfile(event){
    const age=clean(event.Age),types=(event.publicTypes||[]).join(' '),text=eventText(event);
    const age21=/\b21\s*\+|21 and (?:over|older)|ages? 21|must be 21/i.test(age);
    const age18=!age21&&(/\b18\s*\+|18 and (?:over|older)|ages? 18|adults?[- ]only/i.test(age));
    const nightlife=/Nightlife & Parties/i.test(types)||event.artKey==='nightlife'||/\bnightlife\b|\bnight ?club\b|\brave\b|\bDJ\b|late[- ]night|goth|burlesque|drag (?:show|brunch|performance)/i.test(text);
    const drinks=/cocktail|tequila|beer|wine|brewery|brewing|\bbar\b|spirits|tasting menu/i.test(text);
    const family=/all ages|family|families|children|kids?|youth|santa/i.test(age+' '+types);
    return{age21,age18,nightlife,drinks,family,focused:age21||age18||nightlife||drinks};
  }
  function kidProfile(event){
    const age=clean(event.Age),types=(event.publicTypes||[]).join(' '),text=eventText(event);
    const ageSuitable=/all ages|family|families|children|kids?|youth|ages?\s*(?:[0-9]|1[0-2])\s*\+/i.test(age);
    const childSpecific=/Santa & Family|children|kids?|youth|little haunts|storytell|scavenger hunt|crafts?|trick[- ]or[- ]treat|costume parade|candy cannon|dinosaur|dinos|pumpkin (?:float|walk)|train ride|animal encounters?/i.test(types+' '+text);
    const teenOrAdult=/teens?\s*\+|\b1[368]\s*\+|\b21\s*\+|adult/i.test(age);
    const intensity=Number(event.ghostCount)||0;
    return{ageSuitable,childSpecific,teenOrAdult,intensity,focused:ageSuitable&&childSpecific&&!teenOrAdult&&!adultProfile(event).age18&&!adultProfile(event).age21};
  }
  function editorialRule(event,series,anchor,editorial){
    const rules=editorial?.events?.[event.id]||[];
    return rules.filter(rule=>(rule.series||[]).includes(series)&&(!rule.from||anchor>=rule.from)&&(!rule.through||anchor<=rule.through)).sort((a,b)=>(a.rank||99)-(b.rank||99))[0]||null;
  }
  function eventMatches(event,series,start,end,topic,editorial,anchor=start){
    if(event.isWatch||!datesFor(event).some(date=>inRange(date,start,end)))return false;
    if(editorialRule(event,series,anchor,editorial)?.decision==='exclude')return false;
    if(series==='free'&&!event.isFree)return false;
    if(series==='topical'&&topic&&!(event.holidays||[]).includes(topic))return false;
    if(series==='lastchance'&&!(event.endDate&&inRange(event.endDate,start,end)))return false;
    if(series==='adults'&&!adultProfile(event).focused)return false;
    if(series==='kids'&&!kidProfile(event).focused)return false;
    if(series==='found'){
      const adult=adultProfile(event);
      if(adult.age21||adult.age18||/(Santa & Family)/i.test((event.publicTypes||[]).join(' ')))return false;
      const discoveryText=[event['Event / attraction'],event.artKey,...(event.categories||[]),...(event.publicTypes||[])].map(clean).join(' ');
      if(!/(odd|unusual|witch|paranormal|immersive|museum|animal|raptor|craft|workshop|story|tea|train|cemetery|historic|scavenger|secret|curious)/i.test(discoveryText))return false;
    }
    return true;
  }
  function baseScore(event,anchor){
    const date=nextDate(event,anchor),days=Math.max(0,dayDiff(anchor,date));
    let value=92-Math.min(days,45)*1.35;
    if(event.notable_event&&days<=45)value+=22;
    if(singleDay(event))value+=10;
    if(event.photo?.src)value+=12;else value-=10;
    if(event.scheduleConfidence==='verified-dates')value+=7;
    if(event.accessibility?.summary)value+=3;
    if(/pending|unverified/i.test(clean(event.Status)))value-=20;
    return value;
  }
  function score(event,series,anchor,topic,recentIds=[]){
    let value=baseScore(event,anchor),types=(event.publicTypes||[]).join(' '),text=eventText(event),proximity=proximityLevel(event),travel=clean(event.travelTier);
    if((recentIds||[]).includes(event.id))value-=46;
    if(topic&&(event.holidays||[]).includes(topic))value+=14;
    if(series==='drive'){
      value+=(4-proximity)*18;
      if(/Overnight \/ destination/i.test(travel))value+=28;
      else if(/Extended day trip/i.test(travel))value+=20;
      else if(/Utah outing/i.test(travel))value+=12;
      else if(/Core \/ easy day trip/i.test(travel))value-=18;
      if(/Active & Outdoors|Community & Culture|Farms & Harvest/i.test(types))value+=8;
    }else if(event.publicRegion==='Salt Lake Metro')value+=26;
    else if(proximity===3)value+=4;
    else value-=8;
    if(series==='weekend'){
      if(singleDay(event))value+=22;
      if(event.notable_event)value+=18;
      if(/Community & Culture|Live Music & Performance|Food & Drink|Active & Outdoors/i.test(types))value+=10;
      if(datesFor(event).length>12)value-=8;
    }
    if(series==='tonight'){
      if(singleDay(event))value+=26;
      if(/Live Music & Performance|Nightlife & Parties|Workshops & Learning|Food & Drink/i.test(types))value+=18;
      if(/\b(?:[4-9]|10|11)(?::\d\d)?\s*(?:AM|PM)/i.test(clean(event.Times)))value+=8;
      if(datesFor(event).length>15)value-=18;
      if(/pumpkin patch|corn maze|haunted house/i.test(text))value-=6;
    }
    if(series==='free'){
      if(singleDay(event))value+=20;
      if(/Community & Culture/i.test(types))value+=20;
      if(/Workshops & Learning|Active & Outdoors|Markets & Shopping/i.test(types))value+=10;
      if(/Nightlife & Parties/i.test(types))value-=5;
    }
    if(series==='topical'){
      if(singleDay(event))value+=18;
      if(/Community & Culture|Live Music & Performance|Workshops & Learning/i.test(types))value+=10;
      if(datesFor(event).length>18)value-=9;
    }
    if(series==='lastchance'){
      const daysLeft=Math.max(0,dayDiff(anchor,event.endDate));
      value+=Math.max(0,32-daysLeft*3);
      if(datesFor(event).length>1)value+=14;
      if(singleDay(event))value-=8;
    }
    if(series==='adults'){
      const adult=adultProfile(event);
      if(adult.age21)value+=44;else if(adult.age18)value+=24;
      if(adult.nightlife)value+=28;if(adult.drinks)value+=12;
      if(adult.family&&!adult.age21&&!adult.age18)value-=16;
    }
    if(series==='kids'){
      const kid=kidProfile(event);
      if(/family|families|children|kids?|youth/i.test(clean(event.Age)))value+=36;
      if(/Santa & Family/i.test(types))value+=30;
      if(kid.childSpecific)value+=22;if(event.isFree)value+=8;
      if(kid.intensity<=2)value+=8;else if(kid.intensity>=4)value-=30;else value-=12;
      if(/\b(?:9|10|11)(?::\d\d)?\s*PM|midnight/i.test(clean(event.Times)))value-=14;
    }
    if(series==='found'){
      const discoveryText=[event['Event / attraction'],event.artKey,...(event.categories||[]),...(event.publicTypes||[])].map(clean).join(' ');
      if(/odd|unusual|paranormal|immersive|raptor|cemetery|secret|curious/i.test(discoveryText))value+=24;
      if(/Workshops & Learning|Food & Drink/i.test(types))value+=12;
      if(event.notable_event)value-=24;
      if(/Farms & Harvest|Haunts & Scares/i.test(types)&&!/unusual|unique|paranormal|immersive/i.test(text))value-=12;
    }
    if(series==='field'){
      if(event.notable_event)value+=24;if(singleDay(event))value+=18;
      if(/Community & Culture|Live Music & Performance|Active & Outdoors|Workshops & Learning/i.test(types))value+=9;
    }
    return value;
  }
  function venueKey(event){return clean(event.Location).toLowerCase().replace(/\b(?:utah|the|at|in)\b/g,'').replace(/[^a-z0-9]+/g,' ').trim()}
  function adjustedScore(item,chosen,series){
    const event=item.event,artCount=chosen.filter(x=>x.artKey&&x.artKey===event.artKey).length,typeCount=Math.max(0,...(event.publicTypes||[]).map(type=>chosen.filter(x=>(x.publicTypes||[]).includes(type)).length)),venue=venueKey(event),venueCount=venue?chosen.filter(x=>venueKey(x)===venue).length:0;
    let value=item.base-artCount*13-typeCount*4-venueCount*22;
    if(series==='drive')value-=chosen.filter(x=>x.publicRegion===event.publicRegion).length*5;
    return value;
  }
  function pickBest(pool,chosen,series,predicate=()=>true){
    const eligible=pool.filter(item=>predicate(item.event));
    if(!eligible.length)return null;
    eligible.sort((a,b)=>adjustedScore(b,chosen,series)-adjustedScore(a,chosen,series)||nextDate(a.event,a.anchor).localeCompare(nextDate(b.event,b.anchor))||clean(a.event['Event / attraction']).localeCompare(clean(b.event['Event / attraction'])));
    return eligible[0];
  }
  function take(item,pool,chosen){
    if(!item||chosen.some(event=>event.id===item.event.id))return false;
    chosen.push(item.event);const index=pool.findIndex(candidate=>candidate.event.id===item.event.id);if(index>=0)pool.splice(index,1);return true;
  }
  function selectDiverse(candidates,count,series,anchor,topic,editorial,recentIds=[]){
    const pool=candidates.map(event=>({event,anchor,base:score(event,series,anchor,topic,recentIds)})),chosen=[];
    const curated=pool.map(item=>({...item,rule:editorialRule(item.event,series,anchor,editorial)})).filter(item=>item.rule&&['lead','include'].includes(item.rule.decision)).sort((a,b)=>(a.rule.decision==='lead'?0:1)-(b.rule.decision==='lead'?0:1)||(a.rule.rank||99)-(b.rule.rank||99)||nextDate(a.event,anchor).localeCompare(nextDate(b.event,anchor)));
    for(const item of curated){if(chosen.length>=count)break;take(item,pool,chosen)}
    const policy=POLICY[series]||POLICY.field;
    if(policy.futureShare){
      const futureAfter=weekendRange(anchor)[1],target=Math.min(count,Math.ceil(count*policy.futureShare));
      while(chosen.length<count&&chosen.filter(event=>nextDate(event,anchor)>futureAfter).length<target){
        if(!take(pickBest(pool,chosen,series,event=>event.publicRegion==='Salt Lake Metro'&&nextDate(event,anchor)>futureAfter),pool,chosen))break;
      }
    }
    if(policy.metroShare){
      const target=Math.min(count,Math.ceil(count*policy.metroShare));
      while(chosen.length<count&&chosen.filter(event=>event.publicRegion==='Salt Lake Metro').length<target){
        if(!take(pickBest(pool,chosen,series,event=>event.publicRegion==='Salt Lake Metro'),pool,chosen))break;
      }
    }
    if(policy.farShare){
      const target=Math.min(count,Math.ceil(count*policy.farShare));
      while(chosen.length<count&&chosen.filter(event=>proximityLevel(event)<=1).length<target){
        if(!take(pickBest(pool,chosen,series,event=>proximityLevel(event)<=1),pool,chosen))break;
      }
    }
    const maxOutside=policy.metroShare?Math.floor(count*(1-policy.metroShare)):count;
    while(pool.length&&chosen.length<count){
      const outside=chosen.filter(event=>event.publicRegion!=='Salt Lake Metro').length;
      const picked=pickBest(pool,chosen,series,event=>!policy.metroShare||event.publicRegion==='Salt Lake Metro'||outside<maxOutside);
      if(!take(picked,pool,chosen))break;
    }
    return chosen;
  }
  function selectionReason(event,series,anchor,topic,editorial){
    const rule=editorialRule(event,series,anchor,editorial);
    if(rule?.decision==='lead')return rule.note||'Editorial lead';
    if(rule?.decision==='include')return rule.note||'Editorial pick';
    if(series==='drive')return proximityLevel(event)<=1?'Destination-worthy outing':'Strong regional exception';
    if(series==='kids')return event.isFree?'Made for kids · free':'Made specifically for kids';
    if(series==='adults'){const p=adultProfile(event);return p.age21?'Verified 21+':p.nightlife?'Nightlife pick':'Grown-up programming'}
    if(series==='free')return singleDay(event)?'Free one-day event':'Useful free plan';
    if(series==='lastchance')return`Ends ${formatDate(event.endDate)}`;
    if(series==='found')return'Unusual local find';
    if(series==='topical')return`${topic} · distinct angle`;
    if(singleDay(event))return'Single-day timely pick';
    if(event.notable_event)return'Notable current event';
    return event.publicRegion==='Salt Lake Metro'?'Strong Salt Lake option':'Editorial regional pick';
  }
  function formatDate(date){return date?asDate(date).toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',timeZone:'UTC'}):''}
  function compactSchedule(event,anchor){
    const dates=datesFor(event).filter(date=>date>=anchor);if(!dates.length)return clean(event['2026 schedule']);
    if(dates.length===1)return formatDate(dates[0]);
    return formatDate(dates[0])+'–'+formatDate(dates.at(-1));
  }
  function price(event){return event.isFree?'Free admission':clean(event.Price||'See organizer for current admission')}
  function place(event){return clean(event.Location||event.publicRegion||event.Region||'Utah')}
  function titleFor(series,topic,start,end,count){
    if(series==='weekend')return`${count} Salt Lake-first ideas for ${formatDate(start)}–${formatDate(end).replace(/^\w+,\s*/, '')}`;
    if(series==='free')return`${count} free weekend plans near Salt Lake`;
    if(series==='tonight')return`${count} things to do near Salt Lake tonight`;
    if(series==='topical')return`${topic}: ${count} different ways to celebrate`;
    if(series==='lastchance')return`${count} Salt Lake-area events ending soon`;
    if(series==='drive')return`${count} Utah events worth the drive`;
    if(series==='adults')return`${count} grown-up plans near Salt Lake`;
    if(series==='kids')return`${count} Salt Lake-area events made for kids`;
    if(series==='found')return`${count} wonderfully specific Salt Lake finds`;
    return`${count} timely Salt Lake-area ideas worth leaving the house for`;
  }
  function captionFor(campaign){
    const intro=`${campaign.eyebrow}: ${campaign.title}\n\nDates, hours and prices were checked against the listed sources, but event details can change.`;
    const entries=campaign.events.map((event,index)=>{
      const access=event.accessibility?.summary?`\nAccess: ${clean(event.accessibility.summary)}`:'';
      const notes=clean(event['Extra notes'])?`\nGood to know: ${clean(event['Extra notes'])}`:'';
      return`${index+1}. ${clean(event['Event / attraction'])}\n${compactSchedule(event,campaign.anchor)} · ${clean(event.Times||'See schedule')}\n${place(event)}\n${price(event)}\n\n${clean(event['Why / thoughts'])}${notes}${access}\nPlan your visit: ${clean(event.Website)}`;
    }).join('\n\n');
    return`${intro}\n\n${entries}\n\nSave this list, share it with the person who always asks what you should do, and find the full guide at Utah Every Season.\n\n#UtahEvents #ThingsToDoInUtah #UtahEverySeason`;
  }
  function altTextFor(campaign){
    const rows=[`Slide 1: Branded cover reading “${campaign.title}.”`];
    campaign.events.forEach((event,index)=>rows.push(`Slide ${index+2}: ${clean(event.photo?.alt||event['Event / attraction'])} Text identifies ${clean(event['Event / attraction'])}, ${compactSchedule(event,campaign.anchor)}, ${place(event)} and ${price(event)}.`));
    rows.push(`Slide ${campaign.events.length+2}: Branded closing card inviting readers to save the post and use Utah Every Season for full details.`);
    return rows.join('\n\n');
  }
  function creditsFor(campaign){return campaign.events.filter(event=>event.photo?.credit).map((event,index)=>`Slide ${index+2}: ${clean(event['Event / attraction'])} — ${clean(event.photo.credit)}${event.photo.creditUrl?' — '+event.photo.creditUrl:''}`).join('\n')||'No external photographs in this set.'}
  function generate(events,options={}){
    const anchor=isoDate(options.anchor)||new Date().toISOString().slice(0,10),series=resolveSeries(options.series||'auto',events,anchor),[start,end]=windowFor(series,events,anchor),[topic,topicCount]=strongestTopic(events,anchor,28),editorial=options.editorial||globalThis.SOCIAL_EDITORIAL||{events:{}},recentIds=options.recentIds||[];
    const candidates=events.filter(event=>eventMatches(event,series,start,end,series==='topical'?topic:'',editorial,anchor));
    const selected=selectDiverse(candidates,Math.max(3,Math.min(9,Number(options.count)||6)),series,anchor,series==='topical'?topic:'',editorial,recentIds);
    const campaign={anchor,series,seriesLabel:SERIES[series].label,seriesDescription:SERIES[series].description,eyebrow:series==='topical'&&topic?topic.toUpperCase():SERIES[series].eyebrow,topic:series==='topical'?topic:'',topicCount,start,end,events:selected,candidates:candidates.sort((a,b)=>score(b,series,anchor,topic,recentIds)-score(a,series,anchor,topic,recentIds)),editorial,recentIds,generatedAt:new Date().toISOString()};
    campaign.selectionNotes=Object.fromEntries(selected.map(event=>[event.id,selectionReason(event,series,anchor,campaign.topic,editorial)]));
    campaign.title=titleFor(series,campaign.topic,start,end,selected.length);campaign.caption=captionFor(campaign);campaign.altText=altTextFor(campaign);campaign.credits=creditsFor(campaign);
    return campaign;
  }
  return{SERIES,POLICY,clean,addDays,dayDiff,datesFor,nextDate,weekendRange,strongestTopic,resolveSeries,proximityLevel,adultProfile,kidProfile,editorialRule,eventMatches,score,selectionReason,formatDate,compactSchedule,price,place,captionFor,altTextFor,creditsFor,generate};
});
