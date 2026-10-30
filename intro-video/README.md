# فيديو تعريفي — نهى اليحيى

فيديو تعريفي مدته 69.5 ثانية، مبني على محتوى الموقع الشخصي
[nohamalyahya-byte.github.io](https://nohamalyahya-byte.github.io) وبنفس هويته البصرية
(الكحلي والأزرق الثلجي، وخطّا Cormorant Garamond وMontserrat).

| الملف | الوصف |
|---|---|
| `nuha-alyahya-intro.mp4` | الفيديو النهائي: ‎1920×1080، ‏30 إطار/ث، H.264 + AAC، ‏21MB |
| `poster.jpg` | صورة غلاف (Thumbnail) من مشهد الافتتاح |
| `source/` | المصدر الكامل لإعادة التوليد أو التعديل |

## المشاهد

| الوقت | المشهد |
|---|---|
| 0:00 | الافتتاح: الاسم، و Healthcare Leader · Change Maker · Lifelong Learner |
| 0:06 | الشهادات PMP® · CPHQ · CKP، وعبارة "Driven by purpose. Focused on people." |
| 0:12 | الرسالة المهنية |
| 0:19.5 | مجالات الخبرة الأربعة |
| 0:25.5 | الخبرة: مستشفيات الحمادي، والخلفية السريرية |
| 0:31.5 | خمسة مشاريع مختارة (منها بوابة توثيق الأطباء، ‏157 طبيبًا) |
| 0:40.5 | المركز الثاني في HealthThon 2026، مشروع أثر، مع صورة الشهادة |
| 0:46.5 | الشهادات المهنية مع صورها |
| 0:52.5 | التعليم (معدل 4.91 و4.71 من 5) |
| 0:57 | جولة داخل الموقع نفسه |
| 1:03 | الخاتمة: Let's talk + الموقع والبريد ولينكدإن |

الموسيقى أصلية ومولَّدة برمجيًا (`source/scripts/music.py`)، لذلك لا توجد أي قيود ترخيص
على نشرها. ومستوى الصوت مضبوط على ‎-16 LUFS المناسب للمنصات.

## إعادة التوليد بعد أي تعديل

النصوص والتوقيتات كلها موجودة في `source/intro.html` (السمة `data-s` / `data-e` لكل مشهد،
و`data-d` لتأخير ظهور كل عنصر). يلزم Node مع Playwright وChromium، وPython مع numpy، وffmpeg:

```bash
cd intro-video/source
# 1) معاينة لقطات عند ثوانٍ محددة
node scripts/preview.js "$PWD/intro.html" /tmp/preview 4.5 45.5 67
# 2) توليد كل الإطارات (4 متصفحات متوازية)
mkdir -p /tmp/frames && node scripts/render.js "$PWD/intro.html" /tmp/frames 30 69.5 4
# 3) الموسيقى
python3 scripts/music.py /tmp/music.wav
ffmpeg -y -i /tmp/music.wav -af "highpass=f=40,loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 /tmp/music_norm.wav
# 4) الدمج
ffmpeg -y -framerate 30 -i /tmp/frames/f%05d.jpg -i /tmp/music_norm.wav -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 18 -tune animation -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 192k -shortest ../nuha-alyahya-intro.mp4
```

لتحديث لقطة الموقع (`assets/site_full.png`) بعد تعديله استخدم `scripts/shot_site.js`.

الخطوط مرخّصة بـ SIL Open Font License 1.1 (النصوص في `source/fonts/OFL-*.txt`).
