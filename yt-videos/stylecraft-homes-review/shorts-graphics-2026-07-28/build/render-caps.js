const path=require('path'),fs=require('fs');
const {chromium}=require('/Users/taylordasch_1/claude-video/branded-maps/node_modules/playwright');
(async()=>{
  const OUT='/private/tmp/claude-502/-Users-taylordasch-1/09bb0d8a-15b8-475b-be39-554ccec5579f/scratchpad/caps';
  fs.mkdirSync(OUT,{recursive:true});
  const b=await chromium.launch({channel:'chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.join(__dirname,'captions-t4.html'));
  await p.waitForLoadState('networkidle');
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>{document.documentElement.style.background='transparent';document.body.style.background='transparent';});
  await p.waitForTimeout(500);
  const ids=await p.evaluate(()=>[...document.querySelectorAll('[id^=cap]')].map(e=>e.id));
  for(const id of ids){ await p.locator('#'+id).screenshot({path:path.join(OUT,id+'.png'),omitBackground:true}); }
  console.log(ids.length+' caption PNGs rendered');
  await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
