const path=require('path'),fs=require('fs');
const {chromium}=require('/Users/taylordasch_1/claude-video/branded-maps/node_modules/playwright');
(async()=>{
  const OUT=path.resolve(__dirname,'..','out'); fs.mkdirSync(OUT,{recursive:true});
  const b=await chromium.launch({channel:'chrome'});
  const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
  await p.goto('file://'+path.join(__dirname,'thumbs.html'));
  await p.waitForLoadState('networkidle');
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(700);
  for(const id of await p.evaluate(()=>[...document.querySelectorAll('.tn')].map(e=>e.id))){
    await p.locator('#'+id).screenshot({path:path.join(OUT,id+'.png')});
    console.log('rendered',id);
  }
  await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
