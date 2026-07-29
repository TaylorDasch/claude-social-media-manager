const path=require('path'),fs=require('fs');
const {chromium}=require('/Users/taylordasch_1/claude-video/branded-maps/node_modules/playwright');
(async()=>{
  const OUT=path.resolve(__dirname,'..','out'); fs.mkdirSync(OUT,{recursive:true});
  const b=await chromium.launch({channel:'chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.join(__dirname,'vertical.html'));
  await p.waitForLoadState('networkidle');
  await p.evaluate(()=>document.fonts.ready);
  // strip page background so .alpha cards keep real transparency
  await p.evaluate(()=>{document.documentElement.style.background='transparent';document.body.style.background='transparent';});
  await p.waitForTimeout(600);
  const els=await p.evaluate(()=>[...document.querySelectorAll('.v')].map(e=>({id:e.id,alpha:e.classList.contains('alpha')})));
  for(const {id,alpha} of els){
    await p.locator('#'+id).screenshot({path:path.join(OUT,id+'.png'),omitBackground:alpha});
    console.log((alpha?'alpha ':'opaque')+'  '+id+'.png');
  }
  await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
