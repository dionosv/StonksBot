const puppeteer = require('puppeteer');
const fs = require("fs")
const { performance } = require('perf_hooks');
const writeStreamgain = fs.createWriteStream('gain.csv');
const writeStreamlose = fs.createWriteStream('lose.csv');
// const output = fs.createWriteStream('text.txt');
(async() => {
console.log("Loading...")
var start = performance.now();
const browser = await puppeteer.launch({bindAddress: '0.0.0.0',
    args: [
    '--no-sandbox',
    // '--headless',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--remote-debugging-port=9222',
    '--remote-debugging-address=0.0.0.0',
]});
const page = await browser.newPage();
await page.goto('https://investor.rti.co.id/research.jsp',{waitUntil: 'networkidle0'});

await page.click('[id="s4"]')
await page.click('[id="ssm1"]')
await page.waitForTimeout(2000)
let loop=0
while(loop<10){
  await page.waitForSelector('a')
  let ticker = await page.evaluate(el => el.textContent, await page.$(`[id="gainer_code${loop}"]`))
  let nama = await page.evaluate(el => el.textContent, await page.$(`[id="gainer_name${loop}"]`))
  let last = parseInt(await page.evaluate(el => el.textContent, await page.$(`[id="gainer_last${loop}"]`)))
  let selisih = parseInt(await page.evaluate(el => el.textContent, await page.$(`[id="gainer_v_chg${loop}"]`)))
  let persen = parseFloat(await page.evaluate(el => el.textContent, await page.$(`[id="gainer_p_chg${loop}"]`)))
  let vol = await page.evaluate(el => el.textContent, await page.$(`[id="gainer_vol${loop}"]`))
  let turnover = await page.evaluate(el => el.textContent, await page.$(`[id="gainer_val${loop}"]`))
  let freq = parseInt(await page.evaluate(el => el.textContent, await page.$(`[id="gainer_freq${loop}"]`)))
  var info=(`${ticker},${nama},${last},${selisih},${persen},${vol},${turnover},${freq}\n`)
  if(ticker==""||nama==""||last==""||selisih==""||persen==""||vol==""||turnover==""||freq==""){}
  else{writeStreamgain.write(info)}
  loop++}

await page.click('[id="ssm2"]')
await page.waitForTimeout(2000)
let loop2=0
  while(loop2<10){
    await page.waitForSelector('a')
    let ticker = await page.evaluate(el => el.textContent, await page.$(`[id="loser_code${loop2}"]`))
    let nama = await page.evaluate(el => el.textContent, await page.$(`[id="loser_name${loop2}"]`))
    let last = parseInt(await page.evaluate(el => el.textContent, await page.$(`[id="loser_last${loop2}"]`)))
    let selisih = parseInt(await page.evaluate(el => el.textContent, await page.$(`[id="loser_v_chg${loop2}"]`)))
    let persen = parseFloat(await page.evaluate(el => el.textContent, await page.$(`[id="loser_p_chg${loop2}"]`)))
    let vol = await page.evaluate(el => el.textContent, await page.$(`[id="loser_vol${loop2}"]`))
    let turnover = await page.evaluate(el => el.textContent, await page.$(`[id="loser_val${loop2}"]`))
    let freq = parseInt(await page.evaluate(el => el.textContent, await page.$(`[id="loser_freq${loop2}"]`)))
    var info=(`${ticker},${nama},${last},${selisih},${persen},${vol},${turnover},${freq}\n`)
    if(ticker==""||nama==""||last==""||selisih==""||persen==""||vol==""||turnover==""||freq==""){}
    else{writeStreamlose.write(info)}
    loop2++}
    
await browser.close();
var selesai = performance.now();
console.log(`${(selesai - start)/1000}\nDone\nPlease ctrl+c to exit`)
// setTimeout( () =>{}, 1200000);
})();
