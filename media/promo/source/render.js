const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const FPS=30, DUR=+process.argv[2]||48, OUT=process.argv[3]||'video_noaudio.mp4', START=+process.argv[4]||0;
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox','--disable-gpu-vsync']});
 const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+__dirname+'/'+(process.env.AD||'ad.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-r',String(FPS),OUT],{stdio:['pipe','inherit','inherit']});
 const n=Math.round((DUR-START)*FPS); const t0=Date.now();
 for(let i=0;i<n;i++){const t=START+i/FPS;await p.evaluate(t=>render(t),t);
  const buf=await p.screenshot({type:'jpeg',quality:95});
  if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
  if(i%150===0) console.log('frame',i,'/',n,((Date.now()-t0)/1000).toFixed(1)+'s');}
 ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('done',((Date.now()-t0)/1000).toFixed(1)+'s');
})();
