# M-Tools — Brand Positioning & Mental Availability Library v1.0
۲۵ نوامبر ۲۰۲۶ | قرارداد طراحی علمی و عملی، نه پیاده‌سازی یا تضمین موفقیت.
مکمل [موتور علمی](marketing-scientific-engine-specification.md)، [مرور پژوهش](marketing-29-tools-evidence-review.md)، [Strategy Library](marketing-strategy-library.md)، [Planning Library](marketing-planning-library.md)، [معماری](marketing-system-architecture-v1.md)، [UX](marketing-ux-design-v1.md).

## ۱. هدف و مرز مفهومی
هدف: کشف اینکه خریدار دسته در چه موقعیت‌هایی، با چه تداعی‌ها و نسبت به کدام گزینه‌ها برند را می‌شناسد/به یاد می‌آورد/در نظر می‌گیرد؛ سپس انتخاب و ساخت جایگاهی که برای مشتری ارزشمند، برای کسب‌وکار قابل اثبات و اجرا و از نظر اقتصادی قابل دفاع است. شرکت نمی‌تواند جایگاه ذهنی را صرفاً با نوشتن positioning statement تعیین کند. **وضعیت واقعی ادراک (observed)، جایگاه مطلوب (desired)، پیش‌بینی (estimated) و فرضیه (hypothesis) چهار نوع متفاوت خروجی‌اند.**

| سازه | معنی و حدود سنجش |
|---|---|
| Positioning | چارچوب رقابت و معنای نسبی/مطلوب برند برای مخاطب؛ positioning انتخاب شرکت است و perceived position در مشتری اندازه‌گیری می‌شود. |
| Differentiation | تفاوت ارزش/منفعت/تجربه ادراک‌شده نسبت به جایگزین و مرتبط با تصمیم؛ می‌تواند عملکردی، تجربه‌ای یا نمادین باشد. |
| Distinctiveness | قابلیت تشخیص اینکه یک عنصر متعلق به کدام برند است؛ لزوماً دلیل انتخاب یا منفعت متفاوت نیست. |
| Mental availability | احتمال/گستره دسترسی به حافظه برند در موقعیت‌های خرید؛ عملیاتی با CEP linkages؛ نه liking، awareness تک‌سؤال، یا share of sales. |
| Physical availability | آسانی یافتن/خریدن برند؛ موجودی، کانال، توزیع و friction؛ با M09/E03/E04 و ST20 جدا ارزیابی شود. |
| CBBE | پاسخ متفاوت مصرف‌کننده به بازاریابی منتسب به دانش برند؛ چندبعدی و جدا از ارزش‌گذاری مالی برند. |
| Preference/choice | ترجیح اظهارشده، consideration و انتخاب واقعی/آزمایشی؛ سنجه‌های متمایز؛ هیچ کدام به تنهایی رفتار آینده قطعی نیست. |

Keller و Ehrenberg-Bass رویکردهای مکمل با constructهای متفاوت‌اند؛ نه یک شاخص مرکب ابداعی. Nedungadi نشان می‌دهد retrieval ممکن است consideration را بدون تغییر evaluation تحت تاثیر قرار دهد. پژوهش ۲۰۲۶ درباره پیام تمایزبخش در تبلیغات، و مطالعه fame/uniqueness منتشرشده ۲۰۲۵/۲۰۲۶، دلیل تفکیک معنای برند از دارایی تشخیص و سنجش واقعی‌اند. شواهد مزیت همه برندها/دسته‌ها یکسان نیست. شخصیت برند، authenticity و اعتماد در صورت relevance با مقیاس معتبر جدا اندازه‌گیری شوند (R27/R28)، نه از تحلیل چهره، شخصیت مشتری، رفتار پنهان یا «خواندن ذهن». حریم خصوصی و عدم فریب حاکم است؛ ادعای subliminal یا نورومارکتینگ از متن/کلیک مجاز نیست.

## ۲. دامنه و معماری
۱۴ capability recipe با شناسه PO01–PO14 در M06 (جایگاه/انتخاب) و M08 (اندازه‌گیری برند) و همکاری M01/M03/M04/M05، B01/B04/B05، S03/S04، E01/E02/E03/E04/E08. این زیرمسیرها ابزار مستقل ۳۰ام، موتور پنجم، Strategy/Planning recipe جدید یا سرویس جدا نیستند. ST05 و PL13 از آن‌ها استفاده می‌کنند؛ ST03/04/07/08/10/17/19/24/26 نیز در صورت نیاز همان خروجی را reuse می‌کنند. M06 MVP فقط positioning draft/PoP-PoD مبتنی بر داده ورودی تاییدشده و تحقیق M01 فعال؛ M08/M04/B04/E02 و دیگر قابلیت‌های اجرا نشده به‌صورت unavailable/partial، نه نتیجه تولیدشده خیالی. حفظ ۲۹ ابزار، ۴ موتور، ۲۶ ST و ۳۴ PL و هشت ابزار MVP. تعداد ۱۴ انتخاب طراحی است.

## ۳. کاتالوگ مسیرها
| ID | قابلیت | مالک |
|---|---|---|
| PO01 | تعریف بازار و طراحی مطالعه | M01 |
| PO02 | اندازه‌گیری جایگاه فعلی و CBBE | M08 |
| PO03 | تداعی برند و شبکه حافظه | M04 |
| PO04 | نیازها، انگیزه و Means-End Chain | M04 |
| PO05 | نقشه ادراکی رقابتی | M06 |
| PO06 | موقعیت‌های ورود به دسته / CEP | M04 |
| PO07 | دسترس‌پذیری ذهنی / Mental Availability | M08 |
| PO08 | دارایی‌های متمایز برند / DBA | M08 |
| PO09 | نقاط اشتراک و تمایز / PoP-PoD | M06 |
| PO10 | ترجیح، انتخاب و trade-off | M06 |
| PO11 | کشف و مقایسه فرصت جایگاه | M06 |
| PO12 | تدوین و آزمون جایگاه مطلوب | M06 |
| PO13 | بازجایگاه‌سازی و معماری برند | M08 |
| PO14 | Brand tracking و ارزیابی تغییر | M08 |

### PO01 — تعریف بازار و طراحی مطالعه
- **مالک روش:** M01؛ ابزارهای کاندید M03,M05,M06,M08.
- **داده:** category، بازار هدف و خریداران دسته، جایگزین‌ها، تصمیم مورد نظر، افق.
- **روش:** تعریف frame و estimand؛ اکتشاف دسته/جایگزین؛ نمونه و قدرت آزمون؛ نسخه پرسشنامه.
- **خروجی:** پروتکل تحقیق و coverage matrix.
- **قید/fallback:** بدون نمونه واقعی فقط research plan.
- **شواهد:** R01,R02,R15.

### PO02 — اندازه‌گیری جایگاه فعلی و CBBE
- **مالک روش:** M08؛ ابزارهای کاندید M01,M04,M06,B05.
- **داده:** آگاهی، تداعی، ارزیابی، consideration، رفتار؛ نمونه قابل تعریف.
- **روش:** تفکیک آگاهی، تصویر، ترجیح و رفتار؛ مقیاس مناسب و نسبت/میانگین با CI مجاز؛ بررسی سازگاری مقیاس.
- **خروجی:** brand profile با شواهد، نقاط قوت و شکاف.
- **قید/fallback:** هیچ امتیاز کلی ثابت brand equity؛ identity داخلی ≠ perception.
- **شواهد:** R01,R03,R04,R15.

### PO03 — تداعی برند و شبکه حافظه
- **مالک روش:** M04؛ ابزارهای کاندید M01,M08,M06.
- **داده:** تداعی آزاد، پاسخ verbatim، یا نقشه تداعی فردی.
- **روش:** کدگذاری دستی/AI پیشنهادی؛ فراوانی پاسخ‌دهنده، جهت/valence؛ شبکه co-occurrence یا BCM واقعی با برچسب جدا.
- **خروجی:** شبکه تداعی و جدول شواهد.
- **قید/fallback:** co-occurrence ≠ رابطه علّی یا BCM؛ بدون داده، فقط فرضیه.
- **شواهد:** R05,R06,R07.

### PO04 — نیازها، انگیزه و Means-End Chain
- **مالک روش:** M04؛ ابزارهای کاندید M01,M05,M06,M09.
- **داده:** مصاحبه از تجربه واقعی و دلیل اهمیت ویژگی.
- **روش:** laddering از attribute→consequence→value، کدگذاری روابط، ماتریس مستقیم/غیرمستقیم و HVM.
- **خروجی:** نقشه نیاز و منافع، نقل شاهد و موارد مخالف.
- **قید/fallback:** نه تشخیص روان‌شناسی؛ مصاحبه کیفی شیوع جمعیت نیست.
- **شواهد:** R08,R05.

### PO05 — نقشه ادراکی رقابتی
- **مالک روش:** M06؛ ابزارهای کاندید M01,M03,M05,M08.
- **داده:** رتبه ویژگی‌های برند یا داده عدم‌شباهت یا جدول تداعی.
- **روش:** انتخاب PCA/MDS/CA مطابق داده؛ fit و عدم قطعیت، جدول عددی؛ مقایسه موج با anchor.
- **خروجی:** نقشه، کیفیت نمایش، رقبای نزدیک و ماتریس ویژگی.
- **قید/fallback:** محور و فاصله ساختگی ممنوع؛ فضای خالی ≠ تقاضا.
- **شواهد:** R09,R10,R16,R17,R18.

### PO06 — موقعیت‌های ورود به دسته / CEP
- **مالک روش:** M04؛ ابزارهای کاندید M01,M05,M08,M09.
- **داده:** مصاحبه و سنجش موقعیت واقعی خرید، وقوع/اهمیت و برندهای به‌یادآمده.
- **روش:** کشف موقعیت از why/when/where/with whom/how/need؛ ادغام و پیش‌آزمون؛ اندازه‌گیری cue→brand و frequency جدا.
- **خروجی:** CEP registry، occurrence و ماتریس ارتباط برند–CEP.
- **قید/fallback:** CEP شعار یا ویژگی محصول نیست؛ مصاحبه برای اولویت عددی کافی نیست.
- **شواهد:** R11,R12,R13.

### PO07 — دسترس‌پذیری ذهنی / Mental Availability
- **مالک روش:** M08؛ ابزارهای کاندید M01,M04,B05.
- **داده:** respondent×brand×CEP و frame مشترک، وزن در صورت نیاز.
- **روش:** محاسبه mental penetration، network size، mental market share، link rate؛ تحلیل کاربران/غیرکاربران.
- **خروجی:** MA dashboard و CEP gaps با مخرج و wave.
- **قید/fallback:** پوشش ناقص برند/CEP یا نمونه نامقایسه‌پذیر مانع سهم مقایسه‌ای؛ MA سهم فروش نیست.
- **شواهد:** R11,R12,R13.

### PO08 — دارایی‌های متمایز برند / DBA
- **مالک روش:** M08؛ ابزارهای کاندید M01,M04,M06,E02.
- **داده:** نمونه رنگ، شکل، بسته‌بندی، صوت، لوگو/شخصیت بدون نام برند؛ پاسخ نام برند.
- **روش:** آزمون بدون cue نام، کدگذاری انتساب درست/رقیب/هیچ؛ fame و uniqueness، confusion matrix.
- **خروجی:** asset grid و تصمیم حفظ/توسعه/بازآزمایی.
- **قید/fallback:** نظر مدیر جای داده مصرف‌کننده نیست؛ threshold جهانی اجباری نیست.
- **شواهد:** R14,R19.

### PO09 — نقاط اشتراک و تمایز / PoP-PoD
- **مالک روش:** M06؛ ابزارهای کاندید M03,M04,M05,M08,B01.
- **داده:** معیار ورود دسته، نیاز مهم، ادراک رقبا و قابلیت اثبات.
- **روش:** تعریف frame of reference، table stakes، benefit/function/symbolic؛ relevance، relative advantage، proof و deliverability.
- **خروجی:** ماتریس PoP/PoD و claim register.
- **قید/fallback:** بدون proof هیچ ادعای برترین/انحصاری مجاز نیست؛ تمایز با تشخیص هویت فرق دارد.
- **شواهد:** R01,R02,R20.

### PO10 — ترجیح، انتخاب و trade-off
- **مالک روش:** M06؛ ابزارهای کاندید M01,B02,B01.
- **داده:** طراحی انتخاب، alternatives/levels/price، choice sets، opt-out در صورت مناسب.
- **روش:** مدل انتخاب multinomial logit، nested/mixed مشروط؛ WTP فقط با coefficient مناسب و عدم قطعیت؛ holdout.
- **خروجی:** part-worth/choice scenario و trade-offs.
- **قید/fallback:** intent ≠ خرید؛ share simulation ≠ market share forecast.
- **شواهد:** R21,R22.

### PO11 — کشف و مقایسه فرصت جایگاه
- **مالک روش:** M06؛ ابزارهای کاندید M02,M03,M05,M07,B01,S04,S05.
- **داده:** موقعیت‌های ممکن، تقاضا/درد، رقبا، هزینه/ظرفیت و شواهد.
- **روش:** حذف گزینه ناقض PoP/قانون/ظرفیت/حاشیه؛ امتیاز چندمعیاره، گزینه حفظ وضع، sensitivity و trade-off.
- **خروجی:** shortlist قابل دفاع، وضعیت داده و دلایل رد.
- **قید/fallback:** هیچ وزن جهانی؛ نبود شاهد ≠ صفر؛ فضای خالی نقشه فقط فرضیه.
- **شواهد:** R02,R10,R20,R23.

### PO12 — تدوین و آزمون جایگاه مطلوب
- **مالک روش:** M06؛ ابزارهای کاندید S03,M08,M04,E02,B04,B01.
- **داده:** shortlist، target، frame، benefit، reason to believe.
- **روش:** بیانیه positioning و value proposition؛ message hierarchy؛ monadic random test مفهوم/پیام، مقایسه معیارهای relevance، credibility، differentiation، brand linkage و intention.
- **خروجی:** decision candidate، creative brief و protocol.
- **قید/fallback:** پیش از تایید S03 فقط پیشنهادی؛ تست پیام اثبات تغییر پایدار ذهن نیست.
- **شواهد:** R01,R02,R20,R24.

### PO13 — بازجایگاه‌سازی و معماری برند
- **مالک روش:** M08؛ ابزارهای کاندید M06,S03,S05,M07,B01,E01,E02,E03,E04,M09.
- **داده:** current vs desired، دارایی‌های قوی، مشتری موجود و هدف جدید، محصول و کانال.
- **روش:** gap analysis، retain/refresh/reposition، ریسک از دست دادن پیوندها/مشتری، تغییر واقعی offer و CX، pilot و gate.
- **خروجی:** migration roadmap و تصمیم حفظ دارایی‌ها، PL13.
- **قید/fallback:** تغییر صرف پیام/لوگو کافی نیست؛ برند جدید/extension به تصمیم مستقل.
- **شواهد:** R01,R14,R25,R20.

### PO14 — Brand tracking و ارزیابی تغییر
- **مالک روش:** M08؛ ابزارهای کاندید M01,M06,B04,B05,E08.
- **داده:** baseline و waveهای قابل مقایسه، exposures/controls در صورت طرح، بودجه و KPI.
- **روش:** اندازه‌گیری ثابت، اختلاف و CI design-aware، tracking association/CEP/assets؛ آزمایش اثر و review.
- **خروجی:** گزارش تغییر، KPI، توصیه ادامه/اصلاح.
- **قید/fallback:** قبل/بعد بدون counterfactual فقط تغییر مشاهده‌شده؛ افزایش sales اثر قطعی نیست.
- **شواهد:** R03,R12,R13,R15,R24.


## ۴. گردش کار علمی و ابزار عملی
1. brief: category/frame of reference، geography/period، product/brand vs corporate/sub-brand، target و کل خریداران دسته (نتایج هر دو جدا)، تصمیم و محدودیت. جایگزین مستقیم، غیرمستقیم و no-buy/status quo در choice در صورت مناسب؛ برندهای کوچک و خریداران غیرمشتری حذف سیستماتیک نشوند.
2. evidence audit: محصول/قیمت/کانال/خدمت، research قبلی، CRM aggregate، feedback و رقبا، identity/asset inventory. داده فروش یا review تصویر ذهنی کل دسته نیست. هر observation به evidence/source/date/sample/measurement mode متصل شود.
3. qualitative discovery: پرسش باز بدون تلقین، تجربه خرید اخیر، free associations، laddering، CEP. دو کدگذار مستقل بر زیرنمونه برای codebook ساختاریافته در صورت نیاز و حل اختلاف؛ در reflexive thematic analysis توافق بین کدگذار شرط جهان‌شمول نیست. متن اصلی و کد نسخه‌دار؛ AI فقط پیشنهاد، با انسان؛ translation review، normalization فارسی (ی/ک، فاصله، نیم‌فاصله و alias) بدون حذف negation؛ موارد مخالف و غیرمرسوم حفظ.
4. quantitative research: تعریف estimand، frame، inclusion/weights/strata/clusters، نمونه مستقل یا panel، هدف precision/MDE، pretest. ترتیب unaided recall → CEP/association modules با جلوگیری از contamination (split sample در صورت نیاز) → aided recognition/ratings/choice → مشخصات. asset test بدون نام یا cue قبلی، جدا/تصادفی؛ order randomization متوازن، «هیچ‌کدام/نمی‌دانم» و skip جدا. در مطالعه ثابت همه موج‌ها instrument/version/category/brand list/cue list/mode/weights comparable؛ تغییرات bridge study یا parallel measure، نه trend خام.
5. diagnosis: محاسبه سنجه‌ها و عدم قطعیت، map و شبکه متناسب با داده؛ تفکیک کل دسته/segment/users vs nonusers؛ نگاه به تقاضا، category penetration و physical availability جدا. کوچک بودن نمونه گروه با هشدار/suppress طبق threshold از پیش تعریف‌شده؛ missing را صفر نکن. یک dashboard بدون ادعای علت.
6. positioning choice: گزینه حفظ وضع + حداقل یک گزینه تغییر (در صورت داده و امکان)، PoP/PoD، relevance و proof، ظرفیت و اقتصاد B01/B02، قواعد S04 و sensitivity؛ تصمیم انسانی S03.
7. activate: positioning statement → promise/proof/message hierarchy → asset/CEP/experience touchpoint matrix و PL13/E01 برنامه مصوب؛ E02 creative، E03 media، E04 sales/CRM، M09/E05 service delivery. اگر وعده قابل تحویل نیست، اصلاح offer قبل تبلیغ؛ نه صرف slogan.
8. measurement: B04 test plan، baseline/target/guardrail B05، tracking M08، E08 بازنگری؛ تغییر مورد نیاز نسخه جدید. هیچ انتشار، تغییر نام، قیمت یا خرید رسانه خودکار.

### ۴.۱ پرسشنامه عملی نمونه (قابل بومی‌سازی، نه متن مقیاس دارای حق نشر)
- screener: آیا در دوره مرتبط از دسته X خرید/جست‌وجو/تصمیم خرید داشته‌اید؟ نقش خریدار B2B/کاربر و تصمیم‌گیر جدا؛ تاریخ، موقعیت و جغرافیا؛ تعریف frame روشن.
- unaided: «وقتی به [دسته] فکر می‌کنید چه نام‌هایی به ذهن شما می‌آید؟» اولین ذکر و همه ذکرها؛ code aliases به brand_id؛ عدم پاسخ ≠ none.
- CEP: «در موقعیت [موقعیت تاییدشده]، کدام نام‌ها برای خرید [دسته] به ذهنتان می‌رسد؟» در pick-any aided جدا برچسب بخورد، همه برندهای فهرست ممکن، none و unknown؛ cue occurrence/frequency در سؤال جدا. پاسخ انتخاب چندگانه؛ برندهای واقعی، بدون تبلیغ.
- association: برای هر برند شناخته‌شده کدام توصیف‌ها صدق می‌کند؟ یا rating با مقیاس anchor مشترک و «نمی‌دانم». مسیر brand→attribute با attribute→brand جدا؛ تحلیل conditional on familiarity صریح. importance و satisfaction جدا؛ سؤال مستقیم تمایز/credibility و open reason.
- choice: گزینه‌های واقع‌بینانه با ویژگی/قیمت، randomization مطابق طراحی و opt-out وقتی واقعی است؛ تعداد task بر اساس پیش‌آزمون، خستگی و design؛ قصد خرید با رفتار واقعی یکسان نیست.
- assets: محرک بدون نام برند، «این نشانه متعلق به چه برندی است؟» free response (اجازه پاسخ چندگانه بر اساس پروتکل)، none/unknown، exposure تصادفی و کنترل cue؛ اگر نام قابل حذف نیست تست recognition جدا نه DBA استاندارد.
- test concept: stimulus هم‌اندازه/هم‌کیفیت؛ تک‌مفهومی تصادفی نسبت به گزینه فعلی/control، relevance، credibility، perceived differentiation، brand linkage، consideration و guardrail (مثلاً confusion/negative perception)، primary outcome و MDE از پیش تعیین شود. هیچ questionnaire نسخه‌دار proprietary بدون اجازه کپی نشود.

### ۴.۲ نمونه و کیفیت
برای نسبت در SRS: n0=z² p(1−p)/e²، finite population correction در نمونه بدون جایگزینی n=n0/(1+(n0−1)/N)، ceil؛ 95%، p=.5، e=.05 → 385 (پیش از adjustment)، فقط مثال فرضی. برای طراحی پیچیده از design effect و برآورد طرح‌مبنا، نرخ پاسخ و coverage؛ n_approached=ceil(n_required/expected_response_rate) صرفاً طرح دعوت، نه رفع bias. برای مقایسه/آزمایش power متناسب metric/unit/cluster/repeated measures و MDE؛ 385 حداقل همه مطالعات نیست. Quota/opt-in فقط sample descriptive یا inference مدل‌مبنا با فرض روشن؛ conventional MOE ممنوع. داده respondent-level برای paired/clustered CI و covariance لازم، aggregate فقط descriptive مگر اطلاعات طراحی کافی. طراحی/وزن از M01/svy؛ Wilson برای SRS نسبت بدون وزن؛ bootstrap پاسخ‌دهنده برای iid sample، replicate weights/PSU-strata برای پیچیده؛ نه bootstrap سلول‌ها یا پاسخ‌های متعدد به عنوان مستقل. Missing pattern/response rate/base، weighting، sample exclusions و comparability ثبت؛ هیچ respondent یا attribute ساختگی تولید نشود.

## ۵. قرارداد محاسباتی

### ۵.۱ Awareness، associations و preference
- unaided top-of-mind = weighted fraction of eligible respondents first mentioning b؛ unaided any recall = fraction naming b at least once؛ aided awareness = fraction recognizing b با prompt؛ brand familiarity و consideration/intent با تعریف و مخرج مستقل. none پاسخ معتبر؛ skip نامعلوم. لیست brand aliases versioned؛ نمره آگاهی نمی‌تواند از فهرست mention ناقص محاسبه شود. در ابزار چندپاسخی جمع share respondent ممکن است >100%.
- association rate q_ba = sum(w_i * I_link_iba) / sum(w_i * valid_iba) با base، wording/direction و missing policy صریح؛ در میان familiar users و category buyers دو metric مجزا. Strength عملیاتی فراوانی/شدت rating جدا؛ favorability rating واقعی؛ uniqueness در context نسبت به جایگزین سنجیده می‌شود، نه «منحصربه‌فرد» صرفاً چون در داده کم دیده شده. مانع آگاهی پایین و prevalence برند را با rateهای absolute و comparative residual نشان دهید. تفاوت خام از brand size confounded می‌شود. اگر N_ba از base و instrument هم‌مقیاس ساخته شده، expected تحت استقلال E_ba=row_total*col_total/grand_total، observed/expected و residual (N−E)/sqrt(E) برای الگوی exploratory؛ multi-response وابسته است، p-value ساده chi-square نامعتبر؛ CI از طرح پاسخ‌دهنده و multiplicity. PoP/PoD باید علاوه بر نسبی بودن، اهمیت، شواهد و قابلیت تحویل داشته باشد.
- CBBE multi-item فقط مقیاس مجاز و اعتبار داده/ترجمه، factor/reliability checks متناسب (برای latent comparison invariance configural/metric/scalar یا روش مناسب ordinal و گروه). scale composite دلخواه با وزن AI یا یک نمره ۰–۱۰۰ پیش‌فرض ممنوع. به‌جای آن داشبورد چندبعدی. CFA/SEM اگر مطالعه واقعاً نیازمند آن است، متخصص و انتخاب فناوری در DEV؛ فرض نمی‌شود در MVP موجود. Brand personality و authenticity فقط سنجه‌های جدا در صورت نیاز، نه روان‌شناسی فرد.
- network co-occurrence از هر respondent مجموعه کدهای تاییدشده؛ node count = تعداد افراد یکتا دارای کد، edge count = افراد یکتا دارای هر دو؛ weighted Jaccard = W(A∩B)/W(A∪B)، base مشترک/threshold/edge pruning مستند. NetworkX گراف؛ centrality فقط ویژگی شبکه اندازه‌گیری‌شده، نه اهمیت علّی. BCM از individual maps و قواعد consensus منتشرشده، جهت و link strength واقعی؛ اگر فقط متن دارید برچسب co-occurrence، نه BCM. laddering implication matrix direct/indirect separate، cut-off و حساسیت آن، hierarchical value map به عنوان تحلیل کیفی.

### ۵.۲ Mental Availability / CEP
در یک wave با eligible buyers مشترک و instrument ثابت، x_i,b,c∈{0,1} برای پاسخ معتبر به cue c و brand b، w_i>0 در صورت وزن؛ none = 0 برای تمام برندهای نمایش‌داده‌شده، skip = missing؛ برای محاسبه share و network باید همه cue×brand لازم برای هر فرد مشاهده یا طبق طرح معتبر برآورد شده باشد. default complete common base و گزارش missing/excluded؛ اگر randomized split module، estimand/design-weighting مخصوص قبل از محاسبه؛ بدون آن metrics مشترک null. تعریف:
- W=Σ_i w_i؛ L_b=Σ_i w_i Σ_c x_i,b,c ؛ P_b=Σ_i w_i I(Σ_c x_i,b,c>0).
- Mental Penetration MP_b=P_b/W (درصد category buyers حداقل یک link)، Network Size NS_b=L_b/P_b (میانگین CEP linked بین افراد دارای link)، Mental Market Share MMS_b=L_b/Σ_j L_j (سهم linkages برندهای اندازه‌گیری‌شده، نه سهم بازار فروش).
- Mean links per category buyer = L_b/W = MP_b×NS_b اگر P_b>0؛ MMS_b = (L_b/W)/Σ_j(L_j/W)، بنابراین MP×NS به‌تنهایی MMS نیست. MP=0 و L=0 → NS=null؛ اگر Σ L=0، MMS تمام برندها null. لینک‌ها duplicate نشوند. Per-CEP link rate q_bc=Σ w_i x_i,b,c/W (همان common base)؛ category occurrence rate و purchase frequency متغیر مستقل، نه وزن CEP پیش‌فرض. در نسخه weighted CEP index نام و مخرج جدا، هرگز برچسب standard MMS نده.
- چارچوب فرصت: occurrence/relevance (تحقیق)، current link/competitive gap، feasibility/proof، reach/cost، consistency with positioning. برای relative over/under-index از جدول برند×CEP و expected residual با caveat وابستگی نمونه. CEP کم‌رقیب اگر تقاضا/fit ندارد اولویت نیست؛ محدود کردن برند به یک cue ممکن است دسترس‌پذیری را کم کند، اما همه cueها به‌طور اجباری انتخاب نشوند؛ تناسب و ظرفیت تعیین کند.
- users/nonusers، segments و wave separately with comparable denominators. سهم از universe محدود «share within measured brands/CEPs»؛ تغییر برند یا cue list break in series؛ bridge یا fixed common set با برچسب. confidence interval از resampling entire respondent vector / design replicate weights. target بر اساس baseline، precision و تصمیم مدیر نه benchmark جهانی.

### ۵.۳ Distinctive Brand Assets
برای asset a و focal brand b، valid exposed respondents و w_i، free brand responses کد شده و dedup within respondent×brand؛ C_b=Σ_i w_i I(named b)؛ R=Σ_j Σ_i w_i I(named brand j) روی all brand responses طبق protocol (including other coded brands)؛ Fame=C_b/Σ_i w_i؛ Uniqueness=C_b/R. اگر single response، R فقط افراد نام‌برنده برند؛ none/unknown as valid no brand در fame denominator؛ اگر missing invalid خارج base. multi-response برای uniqueness شمار response links نه تعداد افراد؛ none در R نیست؛ miscoding generic terms و unknown audit. R=0 → uniqueness null، fame=0 اگر valid base>0. fame و uniqueness دو محورند؛ confusion matrix و تعداد نام رقیب، CI، scale مشترک؛ تصمیم invest/protect/test/deprioritize بر مبنای داده، strategic fit، هزینه/ریسک و thresholds تاییدشده؛ هیچ quadrant cutoff جهانی ثابت. برای دارایی جدید کم‌آشنا، test recognition، learning و confusion قبل تغییر گسترده؛ trademark/legal/rights review. بدون داده مصرف‌کننده صرفاً inventory و expert hypothesis.

### ۵.۴ Perceptual mapping — روش بر اساس نوع داده
| نوع داده | انتخاب روش و API | کیفیت / تفسیر |
|---|---|---|
| امتیاز مستقیم دو ویژگی معنایی | weighted means / proportions با طراحی M01، scatter دو محور نام‌دار واقعی | CI هر محور و covariance اگر داده paired؛ بدون dimension reduction. MVP ساده با داده تاییدشده. |
| brand×attribute ratings قابل مقایسه | sklearn PCA 1.9.1 روی ماتریس brand profiles؛ standardization فقط اگر scale/variance و هدف justify | loadings، explained_variance_ratio_، preprocessing، missing/base; PCA unweighted brand-profile مگر روش weighted explicit. محور latent نام‌گذاری با loading و تایید. |
| dissimilarity pairwise | sklearn.manifold.MDS(n_components=2, metric='precomputed', metric_mds=True, n_init=8, init='random', random_state=seed, normalized_stress=True) candidate API 1.9.1؛ برای ordinal ranks metric_mds=False با semantics zero بررسی؛ ClassicalMDS alternative | D مربع، finite، symmetric، nonnegative، diag 0، missing distinct from zero، یکسان سازی unit؛ چند شروع، stress normalized و Shepard plot، fit در 1/2/3D و stability. n_init=8 صرفاً پیشنهاد فنی، نه optimum جهانی. محور MDS arbitrary، تفسیر فاصله فقط در fit معتبر. |
| nonnegative contingency brand×attribute/CEP | CA؛ optional Prince CA candidate، یا SciPy SVD استاندارد (بدون وابستگی جدید) | positive masses، inertia/contributions/cos²، scaling ثبت، residual table؛ row-row و col-col distances در scaling مناسب، proximity row-column به‌تنهایی شدت association نیست. multi-response inference وابسته به respondent. |
| انتخاب ویژگی/قیمت | Biogeme 3.3.5 MNL baseline و mixed/nested شرطی | coding design، identifiable utility، convergence/SE، IIA مناسب MNL، panel dependence، holdout choice tasks/person، probability calibration. WTP=-β_attribute/β_price فقط coefficient معنادار و uncertainty مناسب؛ price nonnegative/negative sign plausibility. |

CA math: N>=0، n>0، P=N/n، r=P1,c=Pᵀ1، S=D_r^-1/2(P−rcᵀ)D_c^-1/2، S=UΣVᵀ، row principal F=D_r^-1/2 UΣ، column principal G=D_c^-1/2 VΣ؛ eigenvalues=σ²، total inertia=sum eigenvalues؛ صفر row/col را با گزارش حذف (نه جایگزینی arbitrary). نمایش یک‌بعدی اگر rank<2؛ total inertia≈0 → هیچ ساختار تمایز قابل نمایش؛ جدول باقی. row/column scaling مناسب برای سوال، با contribution و original residual table. SciPy فقط linear algebra نه inference پیچیده.
برای MDS/PCA/CA عدم قطعیت از resample واحد پاسخ‌دهنده با preserve design و بازسازی map؛ alignment به anchor مشترک (translation/orthogonal Procrustes، reflection/rotation مجاز؛ scale فقط با تعریف ثابت و گزارش)؛ اگر تغییر axes, scaling, instrument یا rank/anchor ناپایدار، overlay غیرمجاز. برای direct semantic axes same scale/wording و comparability. Position desired به صورت concept tested point فقط اگر همان instrument و داده مستقل واقعی؛ در غیر این صورت target hypothesis annotation خارج از point cloud یا جدول، نه مختصات علمی. گراف 2D فقط اگر fit/diagnostics معیار از پیش تعیین‌شده و expert review پذیرفته شود؛ threshold stress جهان‌شمول نیست. اگر fit کم، 1D/3D یا جدول/heatmap؛ هیچ t-SNE/UMAP پیش‌فرض برای نقشه فاصله و بازار خالی (global distance interpretable نیست). Benchmark عمومی جایگاه‌سازی همه دسته‌ها یافت نشده؛ مقالات روش‌شناسی، dataset BRAND (R26) برای نمونه کنترل recognition/attitude، داده Biogeme برای choice demo و CA fixtures معتبرند؛ هیچ‌کدام ground truth بازار مشتری، MA/DBA یا «بهترین الگوریتم» جهانی نیست.

### ۵.۵ انتخاب جایگاه و برنامه عملی
ابتدا hard gates: frame صحیح و نیاز قابل شناسایی، PoP ضروری/مجوز و truthfulness، قابلیت تحویل و حداقل حاشیه/ظرفیت مصوب؛ داده حیاتی غایب=blocked یا hypothesis/pilot، نه score صفر. سپس گزینه‌های feasible با value functions در مقیاس یکسان: relevance، distinct benefit، credibility/proof، mental link/CEP opportunity، fit/capacity، incremental economics/scenario، execution risk. معیار مرتبط برای هر تصمیم، double counting (مثلاً relevance و intent) کنترل، weights nonnegative sum1 از مدیر؛ additive model فقط با compensability/independence معقول؛ حساسیت weights/uncertainty و rank reversals؛ MCDA کمک به تصمیم نه حقیقت. گزینه با ادعای خلاف/عدم تحویل قابل انتخاب نهایی نیست. وضعیت current/desired جدا؛ بیان: «برای [target و frame]، [brand] [benefit قابل تحویل] را ارائه می‌کند، زیرا [proof]؛ نسبت به [alternative] [difference مستند].» اگر proof هنوز hypothesis، علامت مشروط و research/offer action؛ تبلیغ ممنوع. Positioning statement داخلی با slogan خارجی فرق دارد.
پس از S03: message architecture (promise→benefit→proof→CTA/CEP)، asset usage، tone، touchpoint changes (product features/service, price, distribution, communication)، matrix brand×CEP×channel×proof؛ E01/PL13 و در صورت نیاز PL15/16/19/34، هزینه و owner و زمان، consistent claim registry و approval. حفاظت asset و پیوندهای فعلی با مشتریان موجود؛ pilot reposition، monitoring adverse associations/customer loss، no untested change at scale. هیچ الگوریتم تبلیغ/پروفایل آسیب‌پذیری فردی یا فریب مشتری نیست.

### ۵.۶ Tracking و نتیجه
baseline wave، target magnitude از decision (proposed تا تایید)، stable questionnaire/context/base، interval و primary metric تعریف قبل. دو موج مستقل SRS proportion: difference و CI متناسب (Newcombe در صورت مناسب)، paired panel: matched difference/paired analysis و attrition check، survey complex design-aware. Multiple brands/CEP/assets: کنترل FDR یا family-wise حسب هدف و pre-spec؛ exploratory برچسب، حداقل گروه کوچک suppress. عدم significance ≠ اثبات عدم تغییر؛ effect/CI و practical MDE گزارش. randomized monadic concept test اثر stimulus روی outcome فوری را می‌سنجد، نه تغییر ذهن بلندمدت؛ RCT/geo lift مناسب در B04 برای اثر کمپین با unit، contamination، exposure و power؛ قبل/بعد یا مدل attribution اثر علّی اثبات نمی‌کند. اندازه‌گیری فروش/contribution، distribution، رقابت و seasonal separate؛ target MA یا DBA تضمین فروش نیست. E08 hold/modify/scale پیشنهاد و approval؛ never optimize فقط لایک یا short-term click.

## ۶. انتخاب فناوری و شواهد فنی
| قابلیت | انتخاب پایه | پیشرفته مشروط / قید |
|---|---|---|
| تحقیق | SurveyJS + Pandas، M01 | svy همان candidate موتور برای طرح پیچیده، نه جایگزین طراحی علمی |
| متن/laddering | codebook و انسانی؛ Python/Pandas | Sentence Transformers Qwen3-Embedding-0.6B candidate / BGE-M3 challenger، BERTopic فقط corpus مناسب؛ Persian semantic quality هنوز تایید نشده |
| سنجه‌های MA/DBA | Pandas/NumPy، weighted respondent-level formulas | svy/design-aware CI؛ no LLM numeric authority |
| گراف | NetworkX موجود | BCM rules یا HVM با ورودی واقعی، نه الگوریتم ساختگی |
| نقشه | direct 2-axis / sklearn PCA و MDS، SciPy | CA از scipy.linalg.svd یا Prince candidate فقط برای convenience پس از release metadata/fixture؛ نسخه جدید Prince در جستجو دیده شد ولی صفحه release باز نشد؛ نصب اجباری یا pin جدید نداریم |
| انتخاب مشتری | Biogeme 3.3.5 طبق موتور | mixed/nested و مدل latent فقط با design/identifiability; official datasets/examples |
| انتخاب جایگاه | S04 NumPy/Decimal | pymcdm موجود candidate برای MCDA در نیاز، حساسیت/weights از مدیر |
| آزمون و tracking | Statsmodels/SciPy/Pandas، M01/B04/B05 | DoWhy/EconML فقط با فرض identification؛ نه برای causal کردن نقشه |
| UI | ECharts/جدول موجود و accessible SVG/canvas chart | هیچ موتور visualization مستقل؛ tooltip sample/base/CI/quality، accessible table |
Runtime baseline Python 3.12 و نسخه‌های candidate قبلی بدون تغییر. API MDS 1.9.1 در مستند رسمی بررسی شد: metric='precomputed'، metric_mds boolean، n_init صریح چون default تغییر کرده؛ پیش از DEV همان version و init='random' بررسی شود. SciPy 1.15.3 linalg موجود. Prince package دارای CA و cross-checkهای پروژه با R است؛ این ادعا اثبات سازگاری تمام stack نیست. گزینه R FactoMineR یا نرم‌افزار پژوهشی تجاری در صورت نیاز specialist/feature ارزیابی می‌شود، نه فقط به علت قیمت رد؛ ابتدا scipy/sklearn کافی. برای به‌روزرسانی نسخه‌ها مرجع موتور علمی است؛ هیچ نصب/lockfile جدید یا CI اجرا نشده. آزمون fixture کافی برای اتصال صحیح به روش علمی منتشرشده؛ الگوریتم تحقیق را دوباره اختراع نمی‌کنیم.

## ۷. قرارداد داده و اتصال به سیستم
recipe metadata PO01–14 با version، owner_tool_id، required_fields، method_gate، outputs، source IDs و availability از registry موجود؛ در M06/M08 و PipelineRun recipe_id/version یا AnalysisRun metadata، همان modeها. artifact PositioningResult (schema_version) از AnalysisRun/گزارش PipelineRun، نه جدول/سرویس جدید. reuse Workspace/BusinessProfile/Product/Segment/Competitor/Evidence/Dataset/MetricDefinition/Observation/Goal/Decision/Action/Outcome/AuditEvent. داده در workspace؛ respondent pseudonymous، حذف PII، permissions و consent برای research، export فقط aggregate مجاز. هیچ داده شناسایی‌شده به مدل بیرونی.
| ساختار | فیلدهای ضروری |
|---|---|
| StudySpec | study_id/version، workspace، category/region/period، target/group، frame، sampling_design، recruitment، questionnaire_version، language، brand_list/CEP_list versions، weighting/replicate schema، codebook、 eligibility/missing rules، method/estimand، consent_ref، analysis_plan_ref |
| Response | respondent_id pseudonymous، wave_id، question_id، brand_id?/cep_id?/asset_id?/attribute_id?، prompt_mode، value/status (valid/none/unknown/skipped/ineligible)، w_i/stratum/PSU/replicate refs، timestamp/source_ref |
| Brand/CEP/Asset/Attribute | stable id/version، label/alias、 category، definition، stimulus_ref، evidence refs، inclusion and wording、 valid scope؛ asset rights/claim proof refs |
| Association/Choice | direction، respondent/code links، valence/strength source؛ choice task/alternative/levels/availability/chosen、 experimental assignment، holdout |
| MetricObservation | metric_definition_version، estimate/null_reason، base unweighted/weighted، group/wave/instrument、 CI/method、 comparability、 observed/estimate/hypothesis |
| MapResult | method/version/parameters/seed، matrix/data_ref、 coordinate/dimension/scale/loadings/inertia/stress、 fit/stability، alignment/anchor、 missing policy، observed vs target labels、 numeric table |
| PositionOption | frame、 target、 benefits、 POP/POD、 proof/unknown、 capability/economics/risks、 criteria/weights/sensitivity、 claim status |
| PositioningResult | coverage、 study refs、 current measures/map refs、 CEP/asset/association refs、 options、 selected_candidate?、 decision_ref?、 statement/proof、 plan_ref?、 tracking_ref、 limits、 evidence_refs |
Composite key response participant×wave×question×entity×task depending design; duplicated events reject/dedup audited; zero vs unknown rules; no cross-tenant read. Reuse previous waves only version-compatible. Stage plan: research M01 → diagnosis M04/M08/M03 → M06 options/S04 → S03 approval → E01 plan/PL13 → E02/E03/E04 → B04/B05/E08 after data. E02 draft stimulus and B04 protocol may precede S03 final choice with clearly draft state; dependencies artifacts and separate runs, no cycle. M06 direct mode for draft without requiring all PO. Full route blocked only on essential unavailable steps, independent continue, no fake complete. Coverage shows required/available/executed/manual; decision approval separate from plan approval. Export snapshot same version.

## ۸. UX — ساده، با جزئیات اختیاری
entry «جایگاه برند در ذهن مشتری» روی M06 و ST05 در catalog موجود؛ M08 برای tracking/assets. سه انتخاب: «جایگاه فعلی را بسنج»، «جایگاه مناسب را انتخاب کن»، «تغییر جایگاه و اثر را پیگیری کن». گزینه وارد کردن پژوهش قبلی یا ساخت پرسشنامه/برنامه تحقیق؛ اطلاعات کسب‌وکار reuse و فقط سوال‌های ضروری (دسته/بازار، برند/رقبا، هدف، داده موجود/ندارد). حالت فاقد داده: card وضعیت «نیازمند تحقیق» و CTA M01؛ یک positioning hypothesis مجزا، هیچ نقشه/MA/DBA fabricated.
Result wizard: (۱) خلاصه تصمیم و coverage، (۲) جایگاه واقعی (metric cards awareness/consideration/MP/NS/MMS with base & wave؛ map + fit and data table؛ filter segment/wave)، (۳) تداعی‌ها و CEP (heatmap absolute/relative و نمونه و source، graph if supported)، (۴) دارایی‌ها (fame/uniqueness scatter و confusion table)، (۵) گزینه‌های مطلوب (criteria, proof, risk, sensitivity، candidate vs observed explicitly، approval)، (۶) plan & tracking (PL13 action, KPI, baseline, target, actual/trend and missing). همه panels collapsible و only relevant؛ ۱۴ صفحه اصلی جدید نیست. در map، no-data/low-fit shows table، legend/axis/source/CI و label؛ target annotation جدا؛ no color-only distinction، RTL, keyboard, mobile table. filter changes denominator recompute and display, cannot compare incompatible waves. Card کلی «امتیاز برند ۸۲» ممنوع. export report شامل raw aggregate/CI, evidence, option rationale and plan; actual vs hypothesis distinction in print. UX detailed wireframes in UX document; approval human, no auto publish. 

## ۹. مثال‌های مصنوعی و fixture (نه داده واقعی)
### A. Mental availability
5 خریدار وزن برابر، 3 CEP، 3 برند A/B/C، در هر cell مجموعه برندهایی که فرد link کرده است، none=∅.
| فرد | CEP1 | CEP2 | CEP3 |
|---|---|---|---|
| 1 | A,B | A | C |
| 2 | A | B | A,C |
| 3 | B | ∅ | C |
| 4 | A,C | A,B | ∅ |
| 5 | ∅ | B | C |
A: L=6، P=3، MP=60%، NS=2، links/buyer=1.2؛ B: L=5، P=5، MP=100%، NS=1؛ C: L=5، P=5، MP=100%، NS=1. MMS A=6/16=37.5%، B=C=31.25%؛ A CEP1=3/5=60%، CEP2=2/5=40%، CEP3=1/5=20%. C افراد 1,2,3,4,5. وزن مثال: فرد1 وزن2، دیگران1 → W=6، A L=8 P=4 MP=2/3 NS=2، B L=6 P=6، C L=6 P=6؛ MMS A=40%. اگر فرد5 CEP3 skipped نه none، standard complete common base فرد5 حذف با گزارش، W=4 در unweighted، A L=6 P=3، B L=4 P=4، C L=4 P=4، MMS A=6/14. داده کوچک فقط fixture، CI عملی/عمومی نیست؛ MP×NS=1.2 نه MMS.

### B. دارایی برند
100 نفر valid exposed، single answer: 35 A، 15 B، 10 C، 40 none. Fame=35%، uniqueness=35/60=58.333...%، misattribution B=15% از all exposed، 25% از named brand responses؛ denominator label. اگر همه none، fame=0 و uniqueness=null. برای multi-response اگر 100 نفر و A=35,B=30,C=20 links، uniqueness=35/85 نه 35/100؛ تعداد distinct individuals ممکن است کمتر از 85. تغییر asset بدون حق استفاده blocked. هیچ threshold جهان‌شمول.

### C. perceptual map و choice
برای A/B/C/D فاصله بین چهار گوشه مربع مختصات (0,0),(1,0),(0,1),(1,1): D symmetric diag0، off diagonal 1 یا sqrt2؛ metric MDS/ClassicalMDS باید pairwise distances در 2D در tolerance از پیش تعریف‌شده (ClassicalMDS نزدیک عددی، iterative MDS tolerance وابسته convergence) بازسازی کند؛ rotation/sign arbitrary، نه assertion بر coordinate خام. D asymmetric/missing reject. CA N=[[30,10],[10,30]] → row/column masses .5، expected20 each، S=[[.25,-.25],[-.25,.25]]، singular value .5، inertia .25، rank1؛ 2D fake ممنوع. N=[[20,20],[20,20]] inertia0 → no structure; table only. Choice مثال utility A=1,B=0 در MNL دو گزینه موجود، probabilities e/(1+e)≈.731 و .269، نه سهم بازار؛ missing choice/invalid availability رد. اینها تست فنی نه مقایسه performance مدل.

### D. تصمیم جایگاه و اجرا
فرض فروشگاه خدمات تعمیر: داده فرضی 200 پاسخ valid هم‌تعریف، current association «تحویل سریع» 40/200=20%، competitor 80/200=40%، اهمیت سرعت بالا طبق مطالعه فرضی؛ برند فقط 30 سفارش/روز ظرفیت دارد و وعده 24 ساعت را هنوز اثبات نکرده. گزینه A «سریع‌ترین/24 ساعت قطعی» hard gate fail؛ گزینه B «زمان تحویل شفاف با پیگیری» مشروط به capability/proof، گزینه C حفظ وضع موجود. هیچ مختصات مطلوب ساختگی. اگر B proof دارد و معیارهای relevance/credibility/economic fit scores [.8,.7,.6] و C [.6,.9,.8]، وزن [.5,.3,.2] → B=.73، C=.73 tie؛ گزارش tie، sensitivity و انتخاب انسانی؛ تغییر وزن به [.7,.2,.1] → B=.76 و C=.68؛ اعداد تصمیم فرضی‌اند. PL13: اصلاح SLA/فرایند، تهیه proof و asset brief، pilot message با B04 و KPI «ارتباط برند با تحویل شفاف»، guardrail شکایت و ظرفیت؛ target پیشنهادی 30% فقط پس از تایید و sample/MDE. موج بعد 60/200=30% → +10pp observed؛ بدون طرح کنترل نمی‌گوییم پیام باعث تغییر شده. اگر داده ندارد، تنها research plan و hypothesis، نه map.
 
## ۱۰. acceptance gates برای DEV
- 14 شناسه یکتا و owner/ref موجود، ST05/PL13 و M06/M08 links؛ state unavailable واقعاً enforce؛ 8-tool MVP unchanged. 
- fixture A و B weighted/unweighted, none vs skipped, duplicate, zero denominators, brand universe و wave change؛ missing report. q_bc و observed/expected, confidence method سازگار؛ هیچ درصد/مخرج ساختگی.
- map C، zero inertia/rank, symmetry, stress and n_init/seed, table fallback؛ alignment only comparable؛ target data proof. MNL normalization و invalid choice. هیچ claim با تخمین NLP بدون شاهد.
- decision D: veto, tie/sensitivity، proof gate، no automatic approval/publish؛ target vs observed vs causal separate. plan owners/costs shared with PL13؛ tenant isolation/consent.
- UI: بدون داده map/metric null، بدیل CTA، sample و CI کنار هر نتیجه، RTL/mobile/table/keyboard، فیلتر comparability، draft/partial/approved متمایز، source drilldown و export version. 
- test فنی کد، API، fixture و data validation در DEV؛ benchmarks منتشرشده reuse، نه بازتولید تحقیقات. در این commit نصب، solver/model fit، تست runtime یا CI اجرا نشده؛ تنها طراحی و بررسی ایستا. هیچ آزمون اعتبار تجربی روی مشتری واقعی ادعا نمی‌شود.
 
## ۱۱. رجیستری شواهد
مرور هدفمند مقاله، مرور نظام‌مند/فراتحلیل، روش بنیادی، منابع فنی رسمی و public dataset؛ نه PRISMA مستقل. بخشی از شواهد به شکل چکیده/رکورد و مستندات و بخش‌هایی از متن قابل دسترس مطالعه شده، نه متن کامل همه. ۳۰ مدخل شامل ۳ مرجع داخلی (R23/R29/R30) که شواهد پیشین را reuse می‌کنند؛ شمار مدخل برابر شمار مقالات مستقل نیست. داده BRAND و Biogeme فقط نمونه روش/benchmarked tasks، نه ranking مستقیم عملکرد positioning libraries. پژوهش‌های ۲۰۲۵–۲۰۲۶ به‌روز و مطالعات بنیادین جدا؛ میزان اطمینان وابسته به مطالعه و دسته.
| ID | منبع | پیوند | نقش و محدودیت |
|---|---|---|
| R01 | Keller (1993), Conceptualizing, Measuring, and Managing Customer-Based Brand Equity | https://doi.org/10.1177/002224299305700101 | چارچوب دانش برند، آگاهی و تداعی قوی/مطلوب/منحصربه‌فرد؛ مدل نظری، نه فرمول ارزش مالی. |
| R02 | Fuchs & Diamantopoulos (2010), Evaluating effectiveness of brand-positioning strategies | https://pure.au.dk/portal/en/publications/evaluating-the-effectiveness-of-brand-positioning-strategies-from/ | شواهد مقایسه چند نوع positioning؛ هیچ روش برتر در تمام ابعاد/دسته‌ها نیست. |
| R03 | Yoo & Donthu (2001), multidimensional consumer-based brand equity scale | https://www.sciencedirect.com/science/article/pii/S0148296399000983 | توسعه مقیاس و آزمون invariance؛ اعتبار ترجمه و نمونه در کاربرد جدید مهم است. |
| R04 | Models of brand equity: a systematic and critical review (2024) | https://doi.org/10.1080/23311975.2024.2433168 | مرور تنوع مدل‌های CBBE/مالی؛ امتیاز واحد جهان‌شمول استنتاج نمی‌شود. |
| R05 | John, Loken, Kim & Monga (2006), Brand Concept Maps | https://doi.org/10.1509/jmkr.43.4.549 | روش elicitation، نقشه فردی و consensus aggregation؛ شبکه واقعی فراتر از هم‌وقوعی متن. |
| R06 | Advanced brand concept maps (2012) | https://www.sciencedirect.com/science/article/pii/S0167811612000444 | افزودن favorability به ساختار تداعی؛ داده جهت/ارزش لازم است. |
| R07 | Eliciting brand association networks using online community data (2022) | https://www.sciencedirect.com/science/article/pii/S0040162522002712 | روش استخراج از اجتماع آنلاین؛ منبع خودانتخابی، نه نمونه نماینده. |
| R08 | Methodological considerations on means-end chain analysis revisited (2021) | https://doi.org/10.1002/mar.21521 | نقد مفروضات laddering و تحلیل زنجیره؛ کدگذاری و تفسیر دقیق، نه علت قطعی. |
| R09 | Assessing brand image through communalities and asymmetries in brand-to-attribute and attribute-to-brand associations (2009) | https://www.sciencedirect.com/science/article/abs/pii/S0377221708002026 | CA بر ماتریس‌های جهت‌دار؛ دو جهت association قابل جایگزینی نیستند. |
| R10 | Customer-Perceived Positioning Effectiveness (2012) | https://doi.org/10.1111/j.1540-5885.2011.00892.x | مقیاس چندبعدی و شواهد پیش‌بینی؛ سنجه attitude تنها کافی نیست. |
| R11 | Romaniuk & Sharp (2004), Conceptualizing and measuring brand salience | https://doi.org/10.1177/1470593104047643 | salience چند cue و دسترسی حافظه، جدا از attitude. |
| R12 | Romaniuk (2022), Category Entry Points in a B2B world, Ehrenberg-Bass Institute | https://marketingscience.info/news-and-insights/category-entry-points-in-a-business-to-business-b2b-world | راهنمای پژوهش‌محور CEP، mental penetration/network size/mental market share؛ مخرج مجموعه برندها مهم است. |
| R13 | Vaughan et al. (2020 online), Measuring advertising’s effect on mental availability | https://doi.org/10.1177/1470785320955095 | کاربرد چهار سنجه MA در tracking؛ تفاوت گروه‌های آگاه از تبلیغ به تنهایی causal نیست. |
| R14 | Assessing branding strength: comparing marketer judgement and consumer data (2025 online/2026 issue) | https://doi.org/10.1057/s41262-025-00395-y | مطالعه 405 عنصر، 50 برند، 5 دسته؛ fame و uniqueness باید با داده مصرف‌کننده سنجیده شود. |
| R15 | AAPOR Disclosure Standards | https://aapor.org/standards-and-ethics/disclosure-standards/ | استاندارد نمونه، وزن، design effects، disclosure و محدودیت nonprobability. |
| R16 | scikit-learn 1.9.1 MDS and ClassicalMDS documentation | https://scikit-learn.org/stable/modules/generated/sklearn.manifold.MDS.html | API metric/precomputed و metric_mds، n_init صریح؛ ClassicalMDS: https://scikit-learn.org/stable/modules/generated/sklearn.manifold.ClassicalMDS.html . |
| R17 | scikit-learn 1.9.1 PCA | https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html | روش خطی؛ scale و explained variance؛ API انتخاب نسخه. |
| R18 | Prince CA / Python package and SciPy 1.15.3 linear algebra | https://github.com/MaxHalford/Prince | CA/SVD و آزمون‌های پروژه؛ PyPI https://pypi.org/project/prince/ ؛ SciPy https://docs.scipy.org/doc/scipy-1.15.3/reference/linalg.html . نسخه Prince 0.23.1 در نتیجه جستجو 28 Oct 2026 دیده شد، اما صفحه همان release قابل بازگشایی نبود؛ pin قطعی یا سازگاری ادعا نمی‌شود. |
| R19 | Romaniuk & Nenycz-Thiel (2014), Measuring the Strength of Color Brand-Name Links | https://doi.org/10.2501/JAR-54-3-313-319 | معیارهای fame و relative competitor links؛ دارایی دیداری ≠ مزیت محصول. |
| R20 | The missing big idea: Brand-differentiating messages and advertising effectiveness across the brand funnel (2026), JAMS | https://doi.org/10.1007/s11747-026-01166-0 | مطالعه طولی ده سال تبلیغات Super Bowl؛ relevance/تمایز پیام و مراحل قیف؛ محیط خاص، نه اندازه اثر قابل تعمیم. |
| R21 | Incentive alignment in conjoint analysis: a meta-analysis on predictive validity (2025) | https://doi.org/10.1007/s11002-025-09764-8 | فراتحلیل اعتبار پیش‌بینی و hypothetical bias؛ طراحی و holdout مهم است. |
| R22 | Biogeme 3.3.5 documentation and public choice datasets | https://biogeme.epfl.ch/sphinx/ | maximum likelihood discrete choice؛ https://biogeme.epfl.ch/ ؛ datasets برای مثال/fixture، نه benchmark جایگاه‌سازی. |
| R23 | مرور علمی S04/M06/B01 در پروژه | marketing-29-tools-evidence-review.md | MCDA، حساسیت و اقتصاد؛ انتخاب مدیر و قید سخت مقدم؛ منبع داخلی synthesis نه مقاله مستقل. |
| R24 | Nedungadi (1990), Recall and Consumer Consideration Sets | https://doi.org/10.1086/208556 | دو آزمایش حافظه‌محور؛ دسترسی حافظه ممکن است consideration را بدون تغییر ارزیابی تغییر دهد؛ جداسازی سازه‌ها. |
| R25 | Branding in New Ventures: A Systematic Review of Extant Research and Future Research Directions (2026) | https://doi.org/10.1111/ijcs.70167 | مرور برند کسب‌وکار نو؛ positioning، credibility و activation؛ توصیه‌ها زمینه‌مند. |
| R26 | BRAND: Brand Recognition and Attitude Norms Database (2025) | https://doi.org/10.3758/s13428-024-02525-x | داده عمومی آشنایی، liking و memory از 2000 مصرف‌کننده آمریکا، دو سال؛ نمونه کاربرد و کنترل روش، نه معیار ایران/بازار مشتری. |
| R27 | Advancing Antecedents of Brand Personality: A Meta-Analytical Review (2025) | https://doi.org/10.1002/mar.22216 | فراتحلیل زمینه traits و عوامل brand personality؛ trait ≠ CEP و برچسب خودکار شخصیت مشتری ممنوع. |
| R28 | Authenticity in marketing: A conceptual model and meta-analysis (12 Nov 2026) | https://doi.org/10.1007/s11747-026-01222-9 | فراتحلیل جدید authenticity و سازه‌های مرتبط؛ نتایج وابسته به تعریف/زمینه؛ تضمین اثر نیست. |
| R29 | SurveyJS, scikit-learn, svy, Sentence Transformers and NetworkX — scientific engine references | marketing-scientific-engine-specification.md | reuse فناوری مصوب، مدل فارسی candidate، پیچیدگی پیمایش و API مطابق release؛ مرجع داخلی نه مدرک برتری مدل. |
| R30 | Measuring effect and experiments — B04/B05 | marketing-29-tools-evidence-review.md | روش‌های آزمایش و گزارش اثر؛ استفاده از شواهد قبلی پروژه، بدون ادعای مرور مستقل تمام مقالات. |

## ۱۲. مسیر توسعه
M06/M01 MVP: brief، research questionnaire plan، descriptive metrics from validated supplied data، PoP/PoD و option/statement مشروط؛ هیچ ابزار غیرفعال را active اعلام نکن. بعد از توسعه M04/M08/B04 و داده لازم، MA/DBA، network و tracking؛ advanced maps/choice فقط با data gate، ابزار فنی مطابق موتور. PL13/E01 و ST05/S03 همزمان reuse؛ مرجع ترتیب تحویل [Full Product Vertical Slice Development Plan](marketing-full-product-development-plan.md) است: VS05 پایه M01/M05/M06 و VS15 پذیرش تک‌تک PO01–14 با روش‌های کامل و gateهای علمی؛ ST05/PL13 در VS19. تمام ۱۴ PO در محصول نهایی الزام دامنه‌اند، نه backlog بعد از MVP. افزودن capability نیازمند evidence و acceptance gate است، نه افزایش تعداد ابزار.

## تکمیل PO05/PO10 — Preference Mapping (C-07)

[Competitive Enhancements](marketing-competitive-enhancements.md) بخش ۶، external PREFMAP را در PO05/PO10 و M06 تعریف می‌کند: regression ترجیح روی coordinate version معتبر، vector β، مدل circular y=α+β^T x−γ||x||² و ideal point β/(2γ) فقط γ مثبت و fit/rank/CV مناسب؛ نقطه خارج hull extrapolated، عدم کفایت → جدول/طرح تحقیق، مدل داخلی PCA ترجیح فضای متفاوت. uncertainty، گروه و domain صریح؛ perceived/preferences/desired سه لایه جدا. بدون PO15 یا مدل conjoint موازی. PR03 choice pricing همان PO10؛ C-11 graph روابط انسانی M09 با graph co-occurrence PO03 یکی نیست. C-01 template preference/coordinates و نمونه، C-02 export چهارفرمت؛ تمام gate و proof قبلی حفظ. هیچ اجرا/fit/CI جدید.
