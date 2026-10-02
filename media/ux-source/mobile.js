const { chromium } = require('/opt/node-tools/node_modules/playwright');
const CSS=`@font-face{font-family:'Plex';src:url('file:///root/.fonts/IBMPlexSansArabic-Regular.ttf');font-weight:400}@font-face{font-family:'Plex';src:url('file:///root/.fonts/IBMPlexSansArabic-Medium.ttf');font-weight:500}@font-face{font-family:'Plex';src:url('file:///root/.fonts/IBMPlexSansArabic-Bold.ttf');font-weight:700}@font-face{font-family:'Mont';src:url('file:///root/.fonts/Montserrat-ExtraBoldItalic.ttf');font-weight:800;font-style:italic}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:390px;height:844px;font-family:Plex,'IBM Plex Sans Arabic',sans-serif;color:#12243D;background:#F3F7FB;overflow:hidden}
.sb{height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;font-size:14px;font-weight:700}
.top{display:flex;align-items:center;justify-content:space-between;padding:6px 18px 10px}
.logo{display:flex;align-items:center;gap:7px}.logo .ar{font-size:22px;font-weight:700}.logo .vl{width:3px;height:20px;border-radius:3px;background:linear-gradient(180deg,#1855A4,#5BC4CE)}.logo .en{font-family:Mont,'Montserrat';font-style:italic;font-weight:800;font-size:15px;color:#1855A4}
.av{width:34px;height:34px;border-radius:50%;background:#1855A4;color:#fff;display:grid;place-items:center;font-size:12px;font-weight:700}
.wrap{padding:0 16px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:6px 0 12px}
.kpi{background:#fff;border:1px solid #E2EAF3;border-radius:14px;padding:10px 6px;text-align:center}.kpi b{display:block;font-size:22px;line-height:1}.kpi span{font-size:10px;color:#5B6F8A}
.kpi.r b{color:#E4573D}.kpi.o b{color:#D98A1E}.kpi.t b{color:#1C8FA0}.kpi.g b{color:#2E9E6C}
.chips{display:flex;gap:6px;overflow:hidden;margin-bottom:10px}.chip{border:1px solid #E2EAF3;background:#fff;border-radius:999px;padding:6px 12px;font-size:12px;font-weight:600;white-space:nowrap}.chip.on{background:linear-gradient(90deg,#1855A4,#5BC4CE);color:#fff;border-color:transparent}
.card{background:#fff;border:1px solid #E2EAF3;border-radius:16px;padding:12px 14px;margin-bottom:10px;box-shadow:0 4px 14px rgba(18,36,61,.05)}
.card.inst{border-color:rgba(228,87,61,.5)}
.row{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
h3{font-size:15px;font-weight:700}.m{font-size:11.5px;color:#5B6F8A}
.st{font-size:10.5px;padding:3px 9px;border-radius:999px;background:#EEF2F7;color:#5F7896;font-weight:600}.st.work{background:rgba(28,143,160,.12);color:#1C8FA0}.st.done{background:rgba(46,158,108,.12);color:#2E9E6C}
.badges{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}.badge{font-size:10.5px;padding:3px 9px;border-radius:999px;font-weight:700}.b-inst{background:rgba(228,87,61,.12);color:#E4573D;border:1px solid rgba(228,87,61,.35)}.b-cum{background:rgba(217,138,30,.12);color:#B8700F;border:1px solid rgba(217,138,30,.35)}
.score{display:flex;align-items:baseline;gap:4px;margin-top:8px}.score b{font-size:26px}.score span{font-size:11px;color:#5B6F8A}
.lvl{font-size:10.5px;padding:3px 9px;border-radius:999px;font-weight:600}.lv-low{background:#EEF2F7;color:#5F7896}.lv-med{background:rgba(217,138,30,.14);color:#B8700F}.lv-high{background:rgba(228,87,61,.14);color:#C8432A}
.nav{position:absolute;bottom:0;left:0;right:0;height:78px;background:#fff;border-top:1px solid #E2EAF3;display:flex;justify-content:space-around;align-items:flex-start;padding-top:10px}
.nav div{font-size:11px;color:#8A9BB2;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px}.nav i{width:22px;height:22px;border-radius:7px;background:#E2EAF3;display:block}.nav .on{color:#1855A4;font-weight:700}.nav .on i{background:#1855A4}
.hero{background:linear-gradient(120deg,#0B2A55,#1855A4 70%,#1F6FB0);color:#fff;border-radius:16px;padding:14px;margin-bottom:10px}.hero h2{font-size:20px}.hero p{font-size:12px;color:#CFE1EF;margin-top:3px}
.alert{background:rgba(228,87,61,.10);border:1px solid rgba(228,87,61,.45);border-radius:14px;padding:12px;margin-bottom:10px;display:flex;gap:10px}.alert .dot{width:10px;height:10px;border-radius:50%;background:#E4573D;margin-top:5px;flex:none}.alert b{font-size:13px;display:block}.alert p{font-size:11.5px;color:#5B6F8A;margin-top:3px}
.btn{display:inline-block;border-radius:10px;padding:9px 14px;font-size:12.5px;font-weight:700;border:1px solid #E2EAF3;background:#fff}.btn.p{background:linear-gradient(90deg,#1855A4,#5BC4CE);color:#fff;border-color:transparent}
.acts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.acts .btn{text-align:center}
.tl{display:flex;flex-direction:column;gap:8px}.ev{border-right:3px solid #5BC4CE;padding-right:10px}.ev b{font-size:12.5px;display:block}.ev span{font-size:10.5px;color:#5B6F8A}
.field{margin-bottom:10px}.field label{font-size:11.5px;color:#5B6F8A;display:block;margin-bottom:4px;font-weight:600}.field .in{border:1px solid #E2EAF3;border-radius:10px;padding:10px 12px;font-size:13px;background:#fff;display:flex;justify-content:space-between}.field .in.sel::after{content:'⌄';color:#8A9BB2}
.seg{display:flex;background:#EEF2F7;border-radius:12px;padding:3px;margin-bottom:10px}.seg div{flex:1;text-align:center;padding:8px 0;font-size:12px;font-weight:600;border-radius:10px;color:#5F7896}.seg .on{background:#fff;color:#1855A4;box-shadow:0 2px 6px rgba(18,36,61,.1)}
.note{font-size:11px;color:#5B6F8A;border-right:3px solid #5BC4CE;padding-right:8px;margin-top:8px;line-height:1.5}
.consent{position:absolute;inset:0;background:linear-gradient(160deg,#050E1F,#0A1A36 55%,#071429);color:#F2F7FC;padding:60px 24px 40px;display:flex;flex-direction:column}
.consent .pill{align-self:flex-start;font-size:11px;border:1px solid rgba(91,196,206,.5);color:#CFE1EF;border-radius:999px;padding:4px 12px}
.consent h2{font-size:24px;margin-top:28px;line-height:1.3}.consent p{font-size:14px;color:#CFE1EF;line-height:1.7;margin-top:14px}
.consent ul{list-style:none;margin-top:18px;display:flex;flex-direction:column;gap:10px;font-size:13px}.consent li::before{content:'✓';color:#5BC4CE;font-weight:700;margin-left:8px}
.consent .cta{margin-top:auto;display:flex;flex-direction:column;gap:10px}.consent .cta .btn{text-align:center;padding:14px;font-size:15px;border-radius:14px}.consent .btn.ghost{background:transparent;color:#F2F7FC;border-color:rgba(255,255,255,.3)}
.consent small{font-size:11px;color:#7F94AE;text-align:center;margin-top:10px}
.map{height:150px;border:1px dashed rgba(91,196,206,.5);border-radius:12px;margin-top:16px;display:grid;place-items:center;color:#5BC4CE;font-size:12px;background:rgba(255,255,255,.03)}`;
const sb=`<div class="sb"><span>9:43</span><span>●●● ⌁ ▮</span></div>`;
const top=`<div class="top"><div class="logo"><span class="ar">أثر</span><span class="vl"></span><span class="en">ATHAR</span></div><div class="av">م.ت</div></div>`;
const nav=(i)=>`<div class="nav">${['مركز القيادة','الحالات','التحليلات','الإعدادات'].map((t,k)=>`<div class="${k===i?'on':''}"><i></i>${t}</div>`).join('')}</div>`;
const S={
 m1:`${sb}${top}<div class="wrap"><div class="kpis"><div class="kpi r"><b>3</b><span>تنبيه فوري</span></div><div class="kpi o"><b>2</b><span>أولوية تراكمية</span></div><div class="kpi t"><b>2</b><span>قيد المعالجة</span></div><div class="kpi g"><b>1</b><span>تمت</span></div></div>
 <div class="chips"><span class="chip on">الكل</span><span class="chip">تنبيهات فورية</span><span class="chip">أولوية تراكمية</span><span class="chip">قيد المعالجة</span></div>
 <div class="card inst"><div class="row"><div><h3>الحالة أ-01</h3><div class="m">النساء والولادة · 34 سنة</div></div><span class="st">قيد المراجعة</span></div><div class="badges"><span class="badge b-inst">● تنبيه فوري</span></div><div class="row" style="align-items:center"><div class="score"><b>12</b><span>نقطة</span></div><span class="lvl lv-low">أولوية تراكمية منخفضة</span></div></div>
 <div class="card inst"><div class="row"><div><h3>الحالة أ-04</h3><div class="m">الجلدية · 29 سنة</div></div><span class="st">قيد المراجعة</span></div><div class="badges"><span class="badge b-inst">● تنبيه فوري</span><span class="badge b-cum">▲ أولوية تراكمية</span></div><div class="row" style="align-items:center"><div class="score"><b>40</b><span>نقطة</span></div><span class="lvl lv-med">أولوية تراكمية متوسطة</span></div></div>
 <div class="card"><div class="row"><div><h3>الحالة أ-02</h3><div class="m">العظام · 45 سنة</div></div><span class="st work">جارٍ التواصل</span></div><div class="badges"><span class="badge b-cum">▲ أولوية تراكمية</span></div><div class="row" style="align-items:center"><div class="score"><b>28</b><span>نقطة</span></div><span class="lvl lv-low">أولوية تراكمية منخفضة</span></div></div>
 <div class="card"><div class="row"><div><h3>الحالة أ-05</h3><div class="m">القلب · 62 سنة</div></div><span class="st done">تمت المعالجة</span></div></div></div>${nav(0)}`,
 m2:`${sb}${top}<div class="wrap"><div class="hero"><div class="row"><div><h2>الحالة أ-03</h2><p>العمر 58 · القسم: الباطنة</p></div><span class="st" style="background:rgba(255,255,255,.15);color:#fff">قيد المراجعة</span></div></div>
 <div class="alert"><span class="dot"></span><div><b>تنبيه فوري · 09:43</b><p>انتظار 31 دقيقة — تجاوز الحد التوضيحي (30 د). لا يتطلب بلوغ عتبة الأولوية التراكمية.</p></div></div>
 <div class="card"><div class="row"><h3>درجة أولوية التواصل</h3><span class="lvl lv-low">منخفضة</span></div><div class="score"><b>20</b><span>نقطة · مثال توضيحي</span></div><div class="m" style="margin-top:4px">تكرار إعادة الجدولة (8) + انتظار فوق الحد (12)</div><div class="acts"><span class="btn p">لماذا هذه الأولوية؟</span><span class="btn">بدء التواصل</span></div></div>
 <div class="card"><h3 style="margin-bottom:8px">الخط الزمني للرحلة</h3><div class="tl"><div class="ev"><b>انتظار العيادة: 31 دقيقة</b><span>09:12 → 09:43 · نظام الطوابير · مستمر</span></div><div class="ev" style="border-color:#C9D8E8"><b>التسجيل</b><span>09:12 · نظام معلومات المستشفى</span></div><div class="ev" style="border-color:#C9D8E8"><b>تكرار إعادة الجدولة</b><span>نظام المواعيد · انتهى</span></div></div></div></div>${nav(1)}`,
 m3:`${sb}${top}<div class="wrap"><div class="hero"><h2>تحديث الحالة أ-03</h2><p>يُحفظ في سجل الحالة</p></div>
 <div class="field"><label>أولًا: نتيجة التواصل</label><div class="seg"><div class="on">تم التواصل</div><div>لم يرد</div><div>لاحقًا</div></div></div>
 <div class="field"><label>ثانيًا: نتيجة التحقق</label><div class="in sel">احتياج مؤكد</div></div>
 <div class="field"><label>ثالثًا: وصف الإجراء</label><div class="in">التنسيق مع شؤون التأمين لاستكمال الموافقة</div></div>
 <div class="field"><label>الجهة المسند إليها</label><div class="in sel">شؤون التأمين</div></div>
 <div class="field"><label>رابعًا: حالة المعالجة</label><div class="in sel">قيد المعالجة</div></div>
 <div class="note">«تمت المعالجة» تتطلب وصف النتيجة وكيفية التحقق منها. «لم يرد» لا يسمح بإغلاق الحالة.</div>
 <div style="margin-top:14px"><span class="btn p" style="display:block;text-align:center;padding:13px">حفظ تحديث الحالة</span></div></div>${nav(1)}`,
 m4:`<div class="consent"><span class="pill">محاكاة لشاشة المريض</span><h2>السماح بتحديد موقعك داخل المنشأة</h2><p>يساعد تحديد موقعك خلال هذه الزيارة فريق تجربة المريض على معرفة منطقة الخدمة ومدة التوقف لتقديم المساعدة عند الحاجة.</p>
 <ul><li>خلال الزيارة الحالية فقط</li><li>داخل المنشأة فقط</li><li>يمكنك سحب الموافقة في أي وقت</li><li>لا وصول إلى سجلك الطبي</li></ul>
 <div class="map">خريطة مناطق الخدمة (توضيحية)</div>
 <div class="cta"><span class="btn p">أوافق</span><span class="btn ghost">لا أوافق</span><small>بدون الموافقة يستمر أثر بالاعتماد على أحداث الأنظمة فقط.</small></div></div>`
};
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:3});
 for(const k of Object.keys(S)){ await p.setContent(`<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>${CSS}</style></head><body>${S[k]}</body></html>`); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(200); await p.screenshot({path:`ux/${k}.png`}); console.log(k); }
 // wallboard
 const W=`<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>${CSS}
 html,body{width:1920px;height:1080px;background:#050E1F;color:#F2F7FC;overflow:hidden}
 .wb{padding:40px 56px;display:flex;flex-direction:column;gap:26px;height:100%}
 .wh{display:flex;justify-content:space-between;align-items:center}.wh .logo .ar{font-size:44px;color:#fff}.wh .logo .en{font-size:30px;color:#5BC4CE}.wh .logo .vl{height:40px;width:5px}
 .wh .t{font-size:30px;font-weight:700}.wh .c{font-family:Mont,'Montserrat';font-style:italic;font-weight:800;font-size:40px;color:#5BC4CE}
 .wk{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}.wk div{background:rgba(16,32,60,.85);border:1px solid rgba(91,196,206,.18);border-radius:22px;padding:26px 30px}.wk b{font-size:96px;line-height:1;display:block}.wk span{font-size:22px;color:#A9BFD6}
 .wk .r b{color:#FF5D5D}.wk .o b{color:#F2A93B}.wk .t b{color:#5BC4CE}.wk .g b{color:#4CC38A}
 .wg{display:grid;grid-template-columns:1.4fr 1fr;gap:22px;flex:1}
 .wc{background:rgba(16,32,60,.85);border:1px solid rgba(91,196,206,.18);border-radius:22px;padding:26px 30px}.wc h3{font-size:26px;margin-bottom:16px}
 table{width:100%;border-collapse:collapse;font-size:22px}th{color:#A9BFD6;font-weight:600;text-align:right;padding:8px 10px;border-bottom:1px solid rgba(91,196,206,.2)}td{padding:14px 10px;border-bottom:1px solid rgba(255,255,255,.06)}
 .wc .badge{font-size:17px;padding:5px 14px}.wc .b-inst{background:rgba(255,93,93,.18);color:#FFB3A6;border-color:rgba(255,93,93,.45)}.wc .b-cum{background:rgba(242,169,59,.16);color:#FFD89A;border-color:rgba(242,169,59,.45)}
 .bar{display:flex;align-items:center;gap:14px;margin-bottom:14px;font-size:20px}.bar span{width:170px;color:#CFE1EF}.bar .tr{flex:1;height:16px;border-radius:8px;background:rgba(255,255,255,.08)}.bar .fl{height:100%;border-radius:8px;background:linear-gradient(90deg,#1855A4,#5BC4CE)}.bar b{width:40px;text-align:left}
 .foot{display:flex;justify-content:space-between;color:#7F94AE;font-size:18px}
 </style></head><body><div class="wb"><div class="wh"><div class="logo"><span class="ar">أثر</span><span class="vl"></span><span class="en">ATHAR</span></div><div class="t">لوحة قسم الباطنة · تجربة المريض الآن</div><div class="c">11:02</div></div>
 <div class="wk"><div class="r"><b>3</b><span>تنبيهات فورية مفتوحة</span></div><div class="o"><b>2</b><span>حالات بأولوية تراكمية</span></div><div class="t"><b>2</b><span>قيد المعالجة</span></div><div class="g"><b>1</b><span>تمت معالجتها اليوم</span></div></div>
 <div class="wg"><div class="wc"><h3>حالات تحتاج تواصلًا الآن</h3><table><tr><th>الحالة</th><th>القسم</th><th>النوع</th><th>الدرجة</th><th>منذ</th></tr>
 <tr><td><b>أ-04</b></td><td>الجلدية</td><td><span class="badge b-inst">تنبيه فوري</span> <span class="badge b-cum">تراكمي</span></td><td>40</td><td>41 د</td></tr>
 <tr><td><b>أ-01</b></td><td>النساء والولادة</td><td><span class="badge b-inst">تنبيه فوري</span></td><td>12</td><td>27 د</td></tr>
 <tr><td><b>أ-06</b></td><td>الطوارئ</td><td><span class="badge b-inst">تنبيه فوري</span></td><td>12</td><td>6 د</td></tr>
 <tr><td><b>أ-02</b></td><td>العظام</td><td><span class="badge b-cum">تراكمي</span></td><td>28</td><td>جارٍ التواصل</td></tr></table></div>
 <div class="wc"><h3>أكثر نقاط الخدمة ظهورًا للإشارات</h3><div class="bar"><span>التسجيل</span><div class="tr"><div class="fl" style="width:100%"></div></div><b>4</b></div><div class="bar"><span>انتظار العيادة</span><div class="tr"><div class="fl" style="width:100%"></div></div><b>4</b></div><div class="bar"><span>نافذة التأمين</span><div class="tr"><div class="fl" style="width:75%"></div></div><b>3</b></div><div class="bar"><span>العيادة</span><div class="tr"><div class="fl" style="width:50%"></div></div><b>2</b></div><div class="bar"><span>منطقة الأشعة</span><div class="tr"><div class="fl" style="width:25%"></div></div><b>1</b></div><h3 style="margin-top:26px">زمن بدء التواصل (متوسط)</h3><div style="font-size:72px;font-weight:700;color:#5BC4CE;line-height:1">7 <span style="font-size:26px;color:#A9BFD6">دقائق من إنشاء التنبيه</span></div></div></div>
 <div class="foot"><span>بيانات توضيحية اصطناعية · لا يُستخدم لتقييم الموظفين أفرادًا</span><span>Silent Experience Intelligence Engine</span></div></div></body></html>`;
 const w=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1.5}); await w.setContent(W); await w.evaluate(()=>document.fonts.ready); await w.waitForTimeout(200); await w.screenshot({path:'ux/wallboard.png'}); console.log('wallboard');
 await b.close();
})();
