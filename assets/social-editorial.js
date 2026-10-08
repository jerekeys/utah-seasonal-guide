(function(root,factory){
  const editorial=factory();
  if(typeof module==='object'&&module.exports)module.exports=editorial;
  root.SOCIAL_EDITORIAL=editorial;
})(typeof window!=='undefined'?window:globalThis,function(){
  return{
    schemaVersion:1,
    updated:'2026-10-08',
    events:{
      'ogden-d-a-de-los-muertos':[
        {decision:'lead',series:['weekend'],from:'2026-10-08',through:'2026-10-11',rank:1,note:'One-day cultural event worth the regional exception'}
      ],
      'snowbird-oktoberfest-2026':[
        {decision:'include',series:['weekend'],from:'2026-10-08',through:'2026-10-11',rank:2,note:'Major seasonal event on its closing weekend'}
      ],
      'little-haunts-this-is-the-place':[
        {decision:'lead',series:['kids'],from:'2026-10-08',through:'2026-10-10',rank:1,note:'Strong child-specific Halloween programming'}
      ],
      'spooky-science-nights-natural-history-museum-of-utah':[
        {decision:'include',series:['kids'],from:'2026-10-08',through:'2026-10-28',rank:2,note:'Hands-on science gives the kids series a distinct angle'}
      ],
      'garden-after-dark-adventures-in-neverland':[
        {decision:'lead',series:['kids'],from:'2026-10-12',through:'2026-10-30',rank:1,note:'Immersive family event with a limited run'}
      ],
      'ginormous-pumpkin-regatta':[
        {decision:'lead',series:['kids','weekend'],from:'2026-10-12',through:'2026-10-17',rank:1,note:'Singular one-day local tradition'}
      ],
      'halloween-train-heber-valley-railroad':[
        {decision:'include',series:['kids'],from:'2026-10-08',through:'2026-10-30',rank:3}
      ],
      'dinos-in-the-dark':[
        {decision:'include',series:['kids'],from:'2026-10-11',through:'2026-10-24',rank:4}
      ],
      'goblin-valley-spooky-dark-sky-wildlife-programs':[
        {decision:'lead',series:['drive'],from:'2026-10-08',through:'2026-10-25',rank:1,note:'The setting makes the trip part of the experience'}
      ],
      'dead-horse-point-halloween-night-programs':[
        {decision:'include',series:['drive'],from:'2026-10-08',through:'2026-10-31',rank:2}
      ],
      'zoobrew-october':[
        {decision:'lead',series:['adults'],from:'2026-10-08',through:'2026-10-14',rank:1,note:'Verified 21+ event with a strong seasonal premise'}
      ],
      'agave-after-dark-bats-tequila':[
        {decision:'lead',series:['adults'],from:'2026-10-15',through:'2026-10-24',rank:1,note:'Distinctly adult event combining education and drinks'}
      ]
    }
  };
});
