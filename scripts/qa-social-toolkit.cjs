const {chromium}=require('playwright');
const AxeBuilder=require('axe-core');
const fs=require('fs');
const path=require('path');

const base=process.env.SITE_URL||'http://127.0.0.1:8765';
const evidence=path.resolve('research/qa');
fs.mkdirSync(evidence,{recursive:true});

async function audit(page,label){
  const results=await page.evaluate(source=>{eval(source);return axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})},AxeBuilder.source);
  const serious=results.violations.filter(item=>['serious','critical'].includes(item.impact));
  fs.writeFileSync(path.join(evidence,`${label}-axe.json`),JSON.stringify(results,null,2));
  if(serious.length)throw new Error(`${label}: ${serious.map(item=>item.id).join(', ')}`);
}

(async()=>{
  const browser=await chromium.launch({headless:true});
  for(const width of [390,1440]){
    const page=await browser.newPage({viewport:{width,height:1100},deviceScaleFactor:1});
    await page.goto(`${base}/toolkit/`,{waitUntil:'networkidle'});
    await page.getByRole('heading',{name:'Your next post is already assembled.'}).waitFor();
    await page.locator('#campaignDate').fill('2026-10-07');
    await page.locator('#series').selectOption('weekend');
    await page.locator('#campaignCount').selectOption('6');
    await page.getByRole('button',{name:'Generate my next post'}).click();
    const firstNames=await page.locator('.lineup-item strong').allTextContents();
    if(firstNames.length!==6)throw new Error(`${width}: expected six selected events, found ${firstNames.length}`);
    if(await page.locator('#slideTabs button').count()!==8)throw new Error(`${width}: expected eight carousel slides`);
    await page.locator('.lineup-item').first().getByRole('button',{name:/Move .* later/}).click();
    const movedNames=await page.locator('.lineup-item strong').allTextContents();
    if(movedNames[1]!==firstNames[0])throw new Error(`${width}: lineup reorder failed`);
    await page.locator('.lineup-item').last().getByRole('button',{name:/Remove/}).click();
    if(await page.locator('.lineup-item').count()!==5)throw new Error(`${width}: remove failed`);
    await page.locator('#addEvent').selectOption({index:1});
    await page.getByRole('button',{name:'Add',exact:true}).click();
    const finalNames=await page.locator('.lineup-item strong').allTextContents();
    if(finalNames.length!==6)throw new Error(`${width}: add failed`);
    const caption=await page.locator('#caption').inputValue();
    for(const name of finalNames)if(!caption.includes(name))throw new Error(`${width}: detailed caption missing ${name}`);
    if(!caption.includes('Plan your visit:'))throw new Error(`${width}: planning links missing from caption`);
    await page.locator('#campaignDate').fill('2026-10-08');
    await page.locator('#series').selectOption('kids');
    await page.getByRole('button',{name:'Generate my next post'}).click();
    const kidNames=await page.locator('.lineup-item strong').allTextContents();
    if(kidNames[0]!=='Little Haunts — This Is The Place')throw new Error(`${width}: kids editorial lead was not first`);
    if(await page.locator('.selection-reason').count()!==kidNames.length)throw new Error(`${width}: selection rationales are missing`);
    if(!/intentionally made for children/i.test(await page.locator('#seriesBrief').textContent()))throw new Error(`${width}: kids brief is not visible`);
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    if(overflow>1)throw new Error(`${width}: horizontal overflow by ${overflow}px`);
    await audit(page,`social-toolkit-${width}`);
    await page.screenshot({path:path.join(evidence,`social-toolkit-${width}.png`),fullPage:true});
    await page.close();
  }
  await browser.close();
  console.log('Social toolkit campaign editing, responsive layout and accessibility checks passed');
})().catch(error=>{console.error(error);process.exit(1)});
