(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.SOCIAL_CAMPAIGN=api;
})(typeof window!=='undefined'?window:globalThis,function(){
  const SEASONS=new Set(['Spring','Summer','Fall','Winter']);
  const SERIES={
    auto:{label:'Best timely story',eyebrow:'THE FIELD EDIT'},
    weekend:{label:'The Weekend File',eyebrow:'THE WEEKEND FILE'},
    tonight:{label:'Tonight',eyebrow:'TONIGHT'},
    free:{label:'Free This Weekend',eyebrow:'FREE THIS WEEKEND'},
    topical:{label:'Current holiday / topical',eyebrow:'RIGHT NOW'},
    lastchance:{label:'Last Chance',eyebrow:'LAST CHANCE'},
    drive:{label:'Worth the Drive',eyebrow:'WORTH THE DRIVE'},
    adults:{label:'Adults Focused',eyebrow:'GROWN-UP PLANS'},
    found:{label:'Found It',eyebrow:'FOUND IT'},
    field:{label:'The Field Guide',eyebrow:'THE FIELD GUIDE'}
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
      counts.set(tag,(counts.get(tag)||0)+1);
    }
    return [...counts].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]))[0]||['',0];
  }
  function resolveSeries(requested,events,anchor){
    if(requested&&requested!=='auto')return requested;
    const weekday=asDate(anchor).getUTCDay();
    if(weekday===4||weekday===5)return'weekend';
    if(weekday===6||weekday===0)return'tonight';
    const [,topicCount]=strongestTopic(events,anchor,21);
    return topicCount>=5?'topical':'field';
  }
  function windowFor(series,events,anchor){
    if(series==='weekend'||series==='free')return weekendRange(anchor);
    if(series==='tonight')return[anchor,anchor];
    if(series==='lastchance')return[anchor,addDays(anchor,10)];
    if(series==='drive'||series==='found')return[anchor,addDays(anchor,35)];
    if(series==='adults')return[anchor,addDays(anchor,28)];
    if(series==='topical')return[anchor,addDays(anchor,28)];
    return[anchor,addDays(anchor,14)];
  }
  const PROXIMITY={
    'Salt Lake Metro':4,
    'Davis County':3,
    'Park City & Wasatch Back':3,
    'Tooele':3,
    'Utah County':3,
    'Ogden, Weber & Morgan':2,
    'Cache / Box Elder':1,
    'Box Elder County':1,
    'Statewide / Other':1,
    'Eastern Utah':0,
    'Cedar / Iron County':0,
    'Southern Utah':0
  };
  function proximityLevel(event){return PROXIMITY[event.publicRegion]??1}
  function adultProfile(event){
    const age=clean(event.Age),types=(event.publicTypes||[]).join(' '),text=[event['Event / attraction'],event['Why / thoughts'],event['Extra notes'],event.Times,event.Location,age,types,event.artKey].map(clean).join(' ');
    const age21=/\b21\s*\+|21 and (?:over|older)|ages? 21|must be 21/i.test(age);
    const age18=!age21&&(/\b18\s*\+|18 and (?:over|older)|ages? 18|adults?[- ]only/i.test(age));
    const nightlife=/Nightlife & Parties/i.test(types)||event.artKey==='nightlife'||/\bnightlife\b|\bnight ?club\b|\brave\b|\bDJ\b|late[- ]night|goth|burlesque|drag (?:show|brunch|performance)/i.test(text);
    const drinks=/cocktail|tequila|beer|wine|brewery|brewing|\bbar\b|spirits|tasting menu/i.test(text);
    const family=/all ages|family|families|children|kids?|youth|santa/i.test(age+' '+types);
    return{age21,age18,nightlife,drinks,family,focused:age21||age18||nightlife||drinks};
  }
  function eventMatches(event,series,start,end,topic){
    if(event.isWatch)return false;
    if(!datesFor(event).some(date=>inRange(date,start,end)))return false;
    if(series==='free'&&!event.isFree)return false;
    if(series==='topical'&&topic&&!(event.holidays||[]).includes(topic))return false;
    if(series==='lastchance'&&!(event.endDate&&inRange(event.endDate,start,end)))return false;
    if(series==='adults'&&!adultProfile(event).focused)return false;
    if(series==='found'&&!/(odd|unusual|unique|only|witch|paranormal|immersive|museum|animal|craft|workshop)/i.test([event['Event / attraction'],event['Why / thoughts'],...(event.publicTypes||[])].join(' ')))return false;
    return true;
  }
  function score(event,series,anchor,topic){
    const date=nextDate(event,anchor);let value=120-Math.max(0,dayDiff(anchor,date))*2;
    if(event.notable_event&&dayDiff(anchor,date)<=45)value+=28;
    if(singleDay(event))value+=12;
    if(event.photo?.src)value+=16;else value-=12;
    if(event.scheduleConfidence==='verified-dates')value+=7;
    if(event.isFree)value+=series==='free'?24:4;
    if(topic&&(event.holidays||[]).includes(topic))value+=18;
    const proximity=proximityLevel(event),travel=clean(event.travelTier);
    if(series==='drive'){
      value+=(4-proximity)*16;
      if(/Overnight \/ destination/i.test(travel))value+=26;
      else if(/Extended day trip/i.test(travel))value+=18;
      else if(/Utah outing/i.test(travel))value+=10;
      else if(/Core \/ easy day trip/i.test(travel))value-=12;
    }else value+=proximity*9;
    if(series==='adults'){
      const adult=adultProfile(event);
      if(adult.age21)value+=44;
      else if(adult.age18)value+=24;
      if(adult.nightlife)value+=28;
      if(adult.drinks)value+=12;
      if(adult.family&&!adult.age21&&!adult.age18)value-=16;
    }
    if(event.accessibility?.summary)value+=3;
    if(/pending|unverified/i.test(clean(event.Status)))value-=20;
    return value;
  }
  function selectDiverse(candidates,count,series,anchor,topic){
    const pool=candidates.map(event=>({event,base:score(event,series,anchor,topic)}));
    const chosen=[],regions=new Map(),types=new Map();
    while(pool.length&&chosen.length<count){
      pool.sort((a,b)=>{
        const adjusted=item=>item.base-(regions.get(item.event.publicRegion)||0)*9-Math.max(0,...(item.event.publicTypes||[]).map(type=>(types.get(type)||0)*3));
        return adjusted(b)-adjusted(a)||nextDate(a.event,anchor).localeCompare(nextDate(b.event,anchor))||clean(a.event['Event / attraction']).localeCompare(clean(b.event['Event / attraction']));
      });
      const picked=pool.shift().event;chosen.push(picked);
      regions.set(picked.publicRegion,(regions.get(picked.publicRegion)||0)+1);
      for(const type of picked.publicTypes||[])types.set(type,(types.get(type)||0)+1);
    }
    return chosen;
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
    if(series==='weekend')return`${count} Utah ideas for ${formatDate(start)}–${formatDate(end).replace(/^\w+,\s*/, '')}`;
    if(series==='free')return`${count} free Utah outings this weekend`;
    if(series==='tonight')return`${count} things happening in Utah tonight`;
    if(series==='topical')return`${topic}: ${count} Utah events to know about`;
    if(series==='lastchance')return`${count} Utah events ending soon`;
    if(series==='drive')return`${count} Utah events worth the drive`;
    if(series==='adults')return`${count} grown-up Utah plans`;
    if(series==='found')return`${count} wonderfully specific Utah finds`;
    return`${count} timely Utah ideas worth leaving the house for`;
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
    const anchor=isoDate(options.anchor)||new Date().toISOString().slice(0,10);
    const series=resolveSeries(options.series||'auto',events,anchor);
    const [start,end]=windowFor(series,events,anchor);
    const [topic,topicCount]=strongestTopic(events,anchor,28);
    let candidates=events.filter(event=>eventMatches(event,series,start,end,series==='topical'?topic:''));
    const selected=selectDiverse(candidates,Math.max(3,Math.min(9,Number(options.count)||6)),series,anchor,series==='topical'?topic:'');
    const campaign={anchor,series,seriesLabel:SERIES[series].label,eyebrow:series==='topical'&&topic?topic.toUpperCase():SERIES[series].eyebrow,topic:series==='topical'?topic:'',topicCount,start,end,events:selected,candidates:candidates.sort((a,b)=>score(b,series,anchor,topic)-score(a,series,anchor,topic)),generatedAt:new Date().toISOString()};
    campaign.title=titleFor(series,campaign.topic,start,end,selected.length);
    campaign.caption=captionFor(campaign);campaign.altText=altTextFor(campaign);campaign.credits=creditsFor(campaign);
    return campaign;
  }
  return{SERIES,clean,addDays,dayDiff,datesFor,nextDate,weekendRange,strongestTopic,resolveSeries,proximityLevel,adultProfile,score,formatDate,compactSchedule,price,place,captionFor,altTextFor,creditsFor,generate};
});
