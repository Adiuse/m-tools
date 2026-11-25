# M-Tools — کتابخانه علمی و عملی استراتژی‌های بازاریابی (Strategy Library v1.0)
تاریخ: ۲۵ نوامبر ۲۰۲۶. وضعیت: طراحی، نه کد یا محصول آماده. مرجع همراه: [معماری فنی](marketing-system-architecture-v1.md)، [مشخصات ۲۹ ابزار](marketing-tool-specifications.md)، [موتور علمی](marketing-scientific-engine-specification.md)، [مرور شواهد](marketing-29-tools-evidence-review.md)، [UX](marketing-ux-design-v1.md).

## ۱. تصمیم معماری و دامنه
۲۶ مسیر تخصصی پیشنهادی بر ۲۹ ابزار موجود و چهار موتور تعریف می‌شود؛ هیچ ابزار مستقل، دیتابیس، agent، موتور علمی یا سرویس جدیدی اضافه نمی‌شود. Strategy Library مجموعه recipe نسخه‌دار و قابل توسعه است؛ نه کتابخانه الگوریتم جدید. هر recipe ترکیبی از قواعد، ابزارهای موجود، قالب ورودی/خروجی و معیار پذیرش است. مالک روش در هر مسیر یک ابزار موجود است؛ تصمیم نهایی استراتژیک همیشه در S03 با تایید مدیر، و برنامه در E01 است. نوع استراتژی، هدف، بازار و کانال را با «نوع کسب‌وکار» اشتباه نگیرید؛ B2B/B2C، کالا/خدمت، اشتراک/تراکنش، محلی/بین‌المللی و online/offline ویژگی‌های context هستند و انتخاب مسیر را تغییر می‌دهند، نه ساختار شایستگی را. این فهرست پوشش طراحی است نه ادعای فهرست تمام استراتژی‌های ممکن. نام‌های نزدیک مثل PPC/SEM، influencer، UGC، inbound/outbound، community، SMS، push، retail/trade، PLG/SLG و demand generation با alias یا زیرمسیر مرتبط قابل دسترسی‌اند. هیچ کانالی پیش‌فرض همه کسب‌وکارها نیست.

## ۲. روش علمی مشترک تدوین
1. سؤال و outcome تجاری قابل سنجش، افق و معیار توقف؛ ثبت baseline و منبع. اگر هدف مبهم است، S01.
2. تشخیص وضعیت و داده‌ها: مشتری، رقبا، بازار، اقتصاد واحد، سفر، ظرفیت، محدودیت حقوقی. داده موجود reuse؛ سؤال غیرقابل پاسخ تبدیل به طرح تحقیق M01.
3. تولید گزینه‌های واقعی شامل ادامه وضعیت موجود؛ STP و ارزش پیشنهادی در صورت نیاز؛ انتخاب‌های «کجا بازی کنیم/چگونه ارزش خلق کنیم/چه چیزی انجام ندهیم». سناریو و trade-off. چارچوب‌ها (STP، 4P/7P، GTM، SOSTAC/RACE در صورت انتخاب تیم) صرفاً ابزار سازمان‌دهی برنامه‌اند، نه الگوریتم پیش‌بینی موفقیت. 4P برای ترکیب محصول، قیمت، توزیع و ترویج؛ 7P برای خدمات در صورت نیاز. هیچ score ثابت یا فرمول تضمین استراتژی وجود ندارد.
4. حذف گزینه‌های ناقض قیود سخت، سپس S04: معیارهای هم‌مقیاس، وزن تاییدشده، شواهد و تحلیل حساسیت. وزن/امتیاز ناقص رتبه قطعی نمی‌سازد. B01/B06 فقط وقتی داده و مدل معتبر باشد؛ در صورت نبود مدل بازده، طرح آزمایشی محدود.
5. تصمیم S03 ثبت نسخه و دلیل، trade-offs، عدم قطعیت، موارد خارج دامنه و صاحب تصمیم. انتخاب و تایید انسانی مستقل از پیشنهاد AI.
6. E01 برنامه، هزینه، وابستگی، مسئول، موعد و معیار پذیرش؛ E02/E03/E04/E05/E06/E07 برحسب مسیر، پیش‌نویس‌های تخصصی را تکمیل می‌کنند. همه اقدام‌ها قبل از فعال‌سازی بررسی و تایید می‌شوند. هیچ خرید، انتشار، ارسال، تغییر قیمت یا CRM خودکار.
7. B04 پروتکل آزمون و B05 KPI واقعی؛ E08 مرور و اصلاح. اگر اجرای ابزار مربوطه فعال نیست، به‌عنوان نیاز توسعه یا ورودی دستی مستند و تاییدشده نشان داده شود؛ نه اجرای ساختگی. استراتژی نسخه جدید پس از تغییر داده/فرض/بودجه با ثبت علت و سابقه ایجاد شود.

## ۳. کاتالوگ و مشخصات ۲۶ مسیر
در هر ردیف، ابزارهای تحلیل و اجرا فهرست کاندید هستند نه زنجیره اجباری. مالک روش می‌تواند همان S03 باشد یا در مرحله تحلیل/طراحی نتیجه تخصصی بسازد. جدول مرحله‌ای بخش ۴ تعیین می‌کند چگونه از چرخه S03↔E01 و وابستگی‌های متقابل اجتناب شود.

| شناسه | استراتژی | مالک روش |
|---|---|---|
| ST01 | استراتژی جامع بازاریابی / Marketing strategy | S03 |
| ST02 | رشد / Growth strategy | S06 |
| ST03 | ورود به بازار / GTM & launch | S06 |
| ST04 | استراتژی محصول و PMF | M07 |
| ST05 | برند و جایگاه‌یابی / Brand strategy | M08 |
| ST06 | قیمت‌گذاری و پروموشن / Pricing | B02 |
| ST07 | استراتژی دیجیتال مارکتینگ | S03 |
| ST08 | شبکه‌های اجتماعی و کامیونیتی / Social media | E02 |
| ST09 | بازاریابی محتوا / Content strategy | E02 |
| ST10 | SEO و جست‌وجوی ارگانیک | E03 |
| ST11 | تبلیغات و Performance marketing / PPC | E03 |
| ST12 | اینفلوئنسر، creator و UGC | E02 |
| ST13 | ایمیل، SMS و پیام‌رسان / Direct lifecycle messaging | E04 |
| ST14 | CRM و مدیریت چرخه مشتری | E04 |
| ST15 | نگهداشت، وفاداری و بازیابی مشتری | E04 |
| ST16 | بهینه‌سازی نرخ تبدیل / CRO | B03 |
| ST17 | تجارت الکترونیک و Marketplace | S03 |
| ST18 | استراتژی فروش و Demand generation | E04 |
| ST19 | بازاریابی B2B و ABM | S03 |
| ST20 | کانال توزیع، خرده‌فروشی و Omnichannel | S06 |
| ST21 | بازاریابی محلی / Local marketing | E03 |
| ST22 | روابط عمومی، اعتبار و مدیریت بحران | E02 |
| ST23 | شراکت، Affiliate و Referral | S06 |
| ST24 | ورود به بازار بین‌المللی / Export & localization | S06 |
| ST25 | رویداد، نمایشگاه، اسپانسرینگ و بازاریابی حضوری | E02 |
| ST26 | تجربه مشتری و بازاریابی خدمات / CX & service | M09 |

### ST01 — استراتژی جامع بازاریابی / Marketing strategy
- **مالک روش:** S03. ابزارهای تحلیل منتخب (مشروط به نیاز): S01,M01,M03,M04,M05,M06,B01,S04. ابزارهای طراحی/اجرا و بازبینی: S06,E01,E02,E03,E04,B05,E08.
- **ورودی تخصصی:** هدف کسب‌وکار، سبد محصول، بازار، منابع، عملکرد و قیود.
- **روش تدوین و انتخاب:** تشخیص شکاف؛ STP؛ انتخاب مزیت، هدف و ترکیب 4P/7P متناسب؛ مقایسه حداقل دو گزینه و گزینه عدم اقدام؛ انتخاب بازار و مدل تخصیص؛ تبدیل به برنامه.
- **خروجی عملی:** سند انتخاب‌های استراتژیک، موارد عدم تمرکز، نقشه KPI و سبد اقدام.
- **KPI:** حاشیه افزایشی، درآمد خالص، سهم بازار فقط با مخرج معتبر، CAC.
- **قید و fallback:** بدون تحقیق و اقتصاد واحد: پیش‌نویس مشروط؛ هیچ درصد بودجه جهانی.
- **پشتوانه:** R01,R02,R03.

### ST02 — رشد / Growth strategy
- **مالک روش:** S06. ابزارهای تحلیل منتخب (مشروط به نیاز): S01,M02,M05,M07,B01,B03,B06,S04,S05. ابزارهای طراحی/اجرا و بازبینی: E01,E03,E04,B04,B05,E08.
- **ورودی تخصصی:** خط پایه جذب/فعال‌سازی/نگهداشت، ظرفیت، حاشیه، بازار قابل خدمت.
- **روش تدوین و انتخاب:** تجزیه رشد به محرک‌های واقعی؛ مقایسه نفوذ، توسعه بازار/محصول و تنوع؛ تشخیص گلوگاه؛ مقایسه سود افزایشی و ریسک؛ اولویت آزمون‌های کوچک.
- **خروجی عملی:** growth tree، سبد فرصت، سناریو و backlog آزمایش.
- **KPI:** سود افزایشی، مشتری فعال، نرخ نگهداشت، CAC/payback.
- **قید و fallback:** بدون داده، آزمون فرضیه؛ رشد زیان‌ده یا ظرفیت‌ناپذیر رد.
- **پشتوانه:** R01,R03,R08,R15.

### ST03 — ورود به بازار / GTM & launch
- **مالک روش:** S06. ابزارهای تحلیل منتخب (مشروط به نیاز): S02,M01,M02,M03,M04,M05,M06,M07,B01,B02. ابزارهای طراحی/اجرا و بازبینی: E01,E02,E03,E04,B04,B05,E08.
- **ورودی تخصصی:** محصول، ICP/بخش، جایگزین‌ها، کانال، قیمت، ظرفیت تحویل و فروش.
- **روش تدوین و انتخاب:** شناسایی use case و beachhead؛ ارزش و پیام؛ انتخاب sales motion و route-to-market؛ بررسی اقتصاد و آمادگی؛ پایلوت، gate توسعه و لانچ.
- **خروجی عملی:** launch brief، readiness، پیام، کانال، ظرفیت، تقویم و مالک.
- **KPI:** فعال‌سازی، مشتری واجد شرایط، خرید/تمدید، حاشیه، زمان تا ارزش.
- **قید و fallback:** لانچ انبوه بدون ظرفیت یا اعتبار ادعا مجاز نیست؛ pilot مشروط.
- **پشتوانه:** R01,R03,R08.

### ST04 — استراتژی محصول و PMF
- **مالک روش:** M07. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M04,M05,M06,M09,B01,B03,S04. ابزارهای طراحی/اجرا و بازبینی: S03,E01,B04,B05,E08.
- **ورودی تخصصی:** رفتار محصول، بازخورد، نیاز مشتری، cohort، هزینه و ظرفیت.
- **روش تدوین و انتخاب:** تعریف مسئله و لحظه ارزش؛ triangulation رفتار/پرداخت/بازخورد؛ اولویت ویژگی بر اثر و هزینه؛ آزمایش مفهوم و adoption؛ توقف یا توسعه.
- **خروجی عملی:** نقشه فرصت محصول و backlog دارای معیار پذیرش.
- **KPI:** فعال‌سازی، retention cohort، adoption، حاشیه، زمان تا ارزش.
- **قید و fallback:** یک امتیاز PMF یا NPS اثبات تناسب نیست؛ فرضیه با داده کم.
- **پشتوانه:** R08,R09.

### ST05 — برند و جایگاه‌یابی / Brand strategy
- **مالک روش:** M08. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M03,M04,M05,M06,M09. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E03,B04,B05,E08.
- **ورودی تخصصی:** هویت، شواهد ادراک، رقبا، اهداف و دارایی برند.
- **روش تدوین و انتخاب:** ممیزی هویت و ادراک؛ انتخاب positioning و معماری پیام؛ سنجش آگاهی/تداعی/تمایز؛ تعریف promise و proof؛ برنامه brand tracking.
- **خروجی عملی:** brand platform، معماری پیام، دستورالعمل بریف و سنجش.
- **KPI:** آگاهی بی‌کمک/با کمک، consideration، تداعی، ترجیح؛ حاشیه بلندمدت در صورت داده.
- **قید و fallback:** بدون نمونه مخاطب، ادراک نامعلوم؛ تغییر لوگو استراتژی نیست.
- **پشتوانه:** R07,R09,R02.

### ST06 — قیمت‌گذاری و پروموشن / Pricing
- **مالک روش:** B02. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M03,M04,M05,M06,B01,B03,S05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E04,B04,B05,E08.
- **ورودی تخصصی:** قیمت، هزینه متغیر، تخفیف، حجم، قیمت رقیب، ظرفیت و محدودیت قانونی.
- **روش تدوین و انتخاب:** تعیین کف حاشیه؛ بررسی ارزش و willingness-to-pay؛ سناریوی قیمت/حجم؛ آزمایش قیمت یا conjoint معتبر؛ محاسبه cannibalization و سود پس از تخفیف.
- **خروجی عملی:** price architecture، سناریو، قواعد تخفیف و آزمون.
- **KPI:** حاشیه کل و واحد، حجم، نرخ تبدیل، کشش فقط با شناسایی، درآمد خالص.
- **قید و fallback:** کشش پیش‌فرض بازار به کسب‌وکار تحمیل نشود؛ بدون داده فقط سناریو.
- **پشتوانه:** R10,R08,R15.

### ST07 — استراتژی دیجیتال مارکتینگ
- **مالک روش:** S03. ابزارهای تحلیل منتخب (مشروط به نیاز): S01,M03,M04,M05,M06,M09,B01,B03,B05,S04. ابزارهای طراحی/اجرا و بازبینی: E01,E02,E03,E04,E05,B04,E08.
- **ورودی تخصصی:** وب/اپ/CRM، مخاطب، journey، اهداف، هزینه و نتایج کانال، ظرفیت.
- **روش تدوین و انتخاب:** ممیزی دیجیتال و tracking؛ انتخاب بخش و هدف؛ نقش paid/owned/earned در سفر؛ اولویت کانال با شواهد و اقتصاد؛ طراحی سنجش، تقویم و بودجه؛ بهینه‌سازی پس از آزمون.
- **خروجی عملی:** digital strategy، channel role matrix، measurement plan، roadmap.
- **KPI:** حاشیه افزایشی، مشتری جدید، qualified lead، CAC، conversion، retention.
- **قید و fallback:** با داده ناکافی فقط بودجه آزمایشی؛ هیچ وعده ROAS یا follower.
- **پشتوانه:** R04,R05,R13,R14.

### ST08 — شبکه‌های اجتماعی و کامیونیتی / Social media
- **مالک روش:** E02. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M03,M04,M05,M06,M08,M09,B05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E03,E04,B04,E08.
- **ورودی تخصصی:** پلتفرم‌های در دسترس، مخاطب و انگیزه استفاده، محتوای قبلی، هزینه/ظرفیت، پیام و قواعد پاسخ.
- **روش تدوین و انتخاب:** هدف و انگیزه مخاطب؛ نقش social content/social commerce/listening/community/CRM؛ انتخاب پلتفرم بر اساس fit نه شهرت؛ ستون محتوا، قالب، تعامل، moderation، escalation، آزمون؛ تفکیک organic و paid.
- **خروجی عملی:** platform playbook، تقویم، community SLA، فرضیه و قواعد بحران.
- **KPI:** reach با تعریف پلتفرم، ER با مخرج مشخص، qualified engagement، referral/lead، هزینه و conversion.
- **قید و fallback:** بدون داده audience fit، پایلوت؛ فالوئر یا لایک معادل فروش نیست؛ فرکانس ثابت جهانی ممنوع.
- **پشتوانه:** R06,R11,R12,R04.

### ST09 — بازاریابی محتوا / Content strategy
- **مالک روش:** E02. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M04,M05,M06,M08,M09,B03,B05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E03,B04,E08.
- **ورودی تخصصی:** نیاز و سؤال مخاطب، journey، inventory محتوا، منابع و هزینه.
- **روش تدوین و انتخاب:** content audit و gap؛ خوشه موضوع بر اساس نیاز و هدف؛ editorial brief و proof؛ نقش هر محتوا در سفر؛ تولید/توزیع/به‌روزرسانی؛ آزمون کیفیت و اثر.
- **خروجی عملی:** topic map، editorial calendar، brief، reuse و distribution plan.
- **KPI:** qualified consumption، leads/conversions دارای تعریف، هزینه محتوا، assisted outcomes غیرعلّی.
- **قید و fallback:** حجم محتوا KPI موفقیت نهایی نیست؛ ادعا بی‌منبع و بازنشر بدون حق ممنوع.
- **پشتوانه:** R11,R04,R05.

### ST10 — SEO و جست‌وجوی ارگانیک
- **مالک روش:** E03. ابزارهای تحلیل منتخب (مشروط به نیاز): M03,M04,M05,M06,M09,B03,B05,E05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,B04,E08.
- **ورودی تخصصی:** دامنه، صفحات، query/page/device/country، وضعیت index، conversion و امکان تغییر سایت.
- **روش تدوین و انتخاب:** ممیزی crawl/index و معماری؛ تحلیل intent و gap؛ اولویت صفحه با relevance/effort/value؛ اصلاح فنی و محتوای مفید؛ ثبت baseline و cohort صفحات؛ بازبینی پس از تغییر.
- **خروجی عملی:** technical backlog، keyword-to-page map، content briefs و tracking.
- **KPI:** organic clicks/impressions/CTR، صفحات eligible/indexed، qualified conversions و contribution.
- **قید و fallback:** Search Console همه queryها را نمی‌دهد؛ رتبه و ترافیک تضمین نمی‌شود؛ قواعد spam و privacy.
- **پشتوانه:** R16,R17,R11.

### ST11 — تبلیغات و Performance marketing / PPC
- **مالک روش:** E03. ابزارهای تحلیل منتخب (مشروط به نیاز): M04,M05,M06,M09,B01,B02,B03,B05,B06. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,B04,E08.
- **ورودی تخصصی:** هدف تجاری، هزینه/نمایش/کلیک/فروش، attribution window، margin، ظرفیت و بودجه.
- **روش تدوین و انتخاب:** انتخاب هدف و audience؛ تفکیک prospecting/retargeting و brand/non-brand؛ ساختار کمپین و creative hypotheses؛ سناریوی بودجه؛ کنترل tracking و incrementality؛ scale/hold/stop.
- **خروجی عملی:** media brief، budget caps، test cells، قواعد توقف و گزارش attribution/lift.
- **KPI:** CPA/CAC، CTR/CPC، attributed ROAS، incremental contribution/ROMI با شاهد.
- **قید و fallback:** بدون داده، budget pilot؛ attribution پلتفرم معادل lift نیست؛ MMM فقط با data gate.
- **پشتوانه:** R13,R14,R18.

### ST12 — اینفلوئنسر، creator و UGC
- **مالک روش:** E02. ابزارهای تحلیل منتخب (مشروط به نیاز): M03,M04,M05,M06,M08,B01,B05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E03,B04,E08.
- **ورودی تخصصی:** مخاطب/دسترسی معتبر، سوابق creator، هزینه، حقوق استفاده، brand safety.
- **روش تدوین و انتخاب:** ارزیابی تناسب پیام/مخاطب و کیفیت تعامل؛ بررسی تقلب و تعارض؛ shortlist و مقایسه؛ قرارداد deliverable/disclosure/حقوق؛ pilot با کد یا لینک و کنترل مناسب.
- **خروجی عملی:** creator scorecard، brief، قرارداد پیشنهادی، طرح سنجش.
- **KPI:** qualified reach، cost per qualified action، فروش منتسب، lift در صورت آزمایش.
- **قید و fallback:** تعداد فالوئر به تنهایی انتخاب نیست؛ افشای رابطه تجاری مطابق حوزه قضایی.
- **پشتوانه:** R12,R19.

### ST13 — ایمیل، SMS و پیام‌رسان / Direct lifecycle messaging
- **مالک روش:** E04. ابزارهای تحلیل منتخب (مشروط به نیاز): M04,M05,M06,M09,B01,B03,B05,E05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,B04,E08.
- **ورودی تخصصی:** رضایت/مجوز کانال، contact events، deliverability، stage، frequency و opt-out.
- **روش تدوین و انتخاب:** بخش‌بندی بر lifecycle؛ تعریف trigger/eligibility/suppression؛ طراحی welcome/nurture/win-back؛ تست محتوا و زمان؛ محدودیت فراوانی؛ holdout و کنترل لغو عضویت.
- **خروجی عملی:** journey automation blueprint، message briefs، suppression و measurement.
- **KPI:** delivered، unique click/delivered، conversion، incremental margin، unsubscribe و complaints.
- **قید و fallback:** فقدان رضایت/مجوز مانع ارسال؛ open rate به علت privacy proxy تشخیصی است.
- **پشتوانه:** R20,R21,R22,R23.

### ST14 — CRM و مدیریت چرخه مشتری
- **مالک روش:** E04. ابزارهای تحلیل منتخب (مشروط به نیاز): M04,M05,M09,B01,B03,B05,E05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E06,B04,E08.
- **ورودی تخصصی:** مراحل lifecycle، CRM IDs، رخدادها، owner، رضایت، SLA.
- **روش تدوین و انتخاب:** تعریف lifecycle و single customer view مجاز؛ segment و handoff؛ eligibility و retention touchpoints؛ کیفیت داده، مالکیت، SLA و integration؛ سنجش پیامد.
- **خروجی عملی:** CRM operating model، lifecycle rules، handoff، data requirements.
- **KPI:** stage conversion، time-to-response، repeat/renewal، CLV، کیفیت داده.
- **قید و fallback:** بدون شناسه معتبر linkage ممنوع؛ تغییر CRM/ارسال فقط با مجوز و تایید.
- **پشتوانه:** R23,R05,R24.

### ST15 — نگهداشت، وفاداری و بازیابی مشتری
- **مالک روش:** E04. ابزارهای تحلیل منتخب (مشروط به نیاز): M04,M05,M07,M09,B01,B03,B05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,B04,E08.
- **ورودی تخصصی:** cohort، churn definition، خرید/تمدید، هزینه انگیزه، شکایت و ظرفیت.
- **روش تدوین و انتخاب:** تفکیک churn قراردادی/غیرقراردادی؛ تشخیص friction؛ cohort/RFM/مدل بقا در صورت داده؛ مقایسه service recovery/loyalty/offer؛ holdout و cannibalization.
- **خروجی عملی:** retention plan، loyalty economics، win-back و guardrails.
- **KPI:** cohort retention، churn، repeat، incremental contribution، redemption cost.
- **قید و fallback:** وفاداری عضویتی معادل اثر برنامه نیست؛ تخفیف زیان‌ده رد.
- **پشتوانه:** R23,R24,R25.

### ST16 — بهینه‌سازی نرخ تبدیل / CRO
- **مالک روش:** B03. ابزارهای تحلیل منتخب (مشروط به نیاز): S01,M04,M09,B01,B05,E05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,B04,E08.
- **ورودی تخصصی:** event funnel، device/source، صفحه/فرایند، حجم، حاشیه و محدودیت تجربه.
- **روش تدوین و انتخاب:** اعتبارسنجی event و cohort؛ شناسایی افت و شواهد کیفی؛ فرضیه UX؛ اولویت با اثر/هزینه؛ آزمون واحد مناسب، MDE و guardrail؛ roll-out مشروط.
- **خروجی عملی:** CRO backlog، experiment briefs، acceptance criteria.
- **KPI:** conversion cohort، contribution per eligible visitor، error/return rate، latency.
- **قید و fallback:** بدون sample کافی فقط تحقیق/پایلوت؛ افزایش conversion به قیمت سود یا تجربه رد.
- **پشتوانه:** R05,R13,R26.

### ST17 — تجارت الکترونیک و Marketplace
- **مالک روش:** S03. ابزارهای تحلیل منتخب (مشروط به نیاز): M02,M03,M04,M05,M06,M09,B01,B02,B03,B05,B06. ابزارهای طراحی/اجرا و بازبینی: E01,E02,E03,E04,E05,B04,E08.
- **ورودی تخصصی:** کاتالوگ، موجودی، سفارش/مرجوعی، هزینه ارسال/کارمزد، قیف و سیاست پلتفرم.
- **روش تدوین و انتخاب:** segment/category economics؛ انتخاب direct/marketplace و assortment؛ قیمت/موجودی؛ acquisition و PDP/checkout؛ fulfillment و retention؛ رصد contribution پس از هزینه.
- **خروجی عملی:** commerce plan، category/channel matrix، merchandising backlog.
- **KPI:** net sales، contribution/order، returns، stockouts، conversion، CAC.
- **قید و fallback:** GMV معادل درآمد خالص نیست؛ موجودی و ارسال پیش‌شرط scale.
- **پشتوانه:** R04,R05,R27.

### ST18 — استراتژی فروش و Demand generation
- **مالک روش:** E04. ابزارهای تحلیل منتخب (مشروط به نیاز): M02,M04,M05,M06,M09,B01,B03,B05,E06. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E03,B04,E08.
- **ورودی تخصصی:** ICP، stages، lead/deal، فروش و ظرفیت، ACV، چرخه و SLA.
- **روش تدوین و انتخاب:** تعریف lead/account qualification، demand creation/capture، ظرفیت و مسیر فروش؛ pipeline math و handoff؛ enablement و follow-up؛ آزمون پیام و کانال.
- **خروجی عملی:** sales motion، funnel target، SLA، playbook و enablement.
- **KPI:** qualified pipeline، win rate، cycle length، CAC، gross margin، booked vs recognized revenue.
- **قید و fallback:** pipeline value معادل فروش نیست؛ ظرفیت و رضایت کانال enforce.
- **پشتوانه:** R23,R24,R28.

### ST19 — بازاریابی B2B و ABM
- **مالک روش:** S03. ابزارهای تحلیل منتخب (مشروط به نیاز): M02,M03,M04,M05,M06,B01,B03,B05. ابزارهای طراحی/اجرا و بازبینی: E01,E02,E03,E04,E06,B04,E08.
- **ورودی تخصصی:** account universe، نیاز و buying group مستند، ارزش/هزینه، چرخه و مالک فروش.
- **روش تدوین و انتخاب:** انتخاب ICP؛ تفکیک demand generation و ABM؛ رتبه‌بندی حساب با fit/value/effort؛ tier و پیام مبتنی بر مسئله؛ sales alignment؛ ارزیابی account-level.
- **خروجی عملی:** account plan، tier criteria، joint marketing/sales playbook.
- **KPI:** qualified accounts، account pipeline، win rate، expansion، cost per account.
- **قید و fallback:** ABM برای همه B2B اجباری نیست؛ اطلاعات شخصی/نیت خرید حدسی ممنوع.
- **پشتوانه:** R28,R24,R01.

### ST20 — کانال توزیع، خرده‌فروشی و Omnichannel
- **مالک روش:** S06. ابزارهای تحلیل منتخب (مشروط به نیاز): M02,M03,M05,M06,M09,B01,B02,B05,B06. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E03,E04,E05,B04,E08.
- **ورودی تخصصی:** جغرافیا، کانال، هزینه/حاشیه، موجودی و SLA، تجربه مشتری.
- **روش تدوین و انتخاب:** مقایسه direct/intermediary و online/offline؛ بررسی دسترسی، economics، تعارض کانال و integration؛ طراحی مسیر و fulfillment؛ pilot و قواعد همکاری.
- **خروجی عملی:** route-to-market، channel economics، handoff و service levels.
- **KPI:** coverage، sell-through، availability، contribution/channel، repeat.
- **قید و fallback:** فروش sell-in و sell-out جدا؛ هم‌پوشانی مشتری/کانال دوباره‌شماری نشود.
- **پشتوانه:** R05,R27,R29.

### ST21 — بازاریابی محلی / Local marketing
- **مالک روش:** E03. ابزارهای تحلیل منتخب (مشروط به نیاز): M02,M03,M04,M05,M06,M09,B01,B05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E04,B04,E08.
- **ورودی تخصصی:** شعبه/منطقه خدمت، ساعات، ظرفیت، query محلی، تماس/رزرو.
- **روش تدوین و انتخاب:** تعریف catchment و customer intent؛ ممیزی اطلاعات شعب و local search؛ outreach محلی، partnerships، تبلیغ منطقه‌ای؛ سنجش تماس/رزرو و فروش.
- **خروجی عملی:** local playbook per location، profile checklist، geo test.
- **KPI:** qualified calls/bookings، footfall با روش معتبر، contribution/location.
- **قید و fallback:** رتبه وابسته به relevance/distance/prominence؛ بدون موقعیت مجاز حدس نزن.
- **پشتوانه:** R16,R30,R13.

### ST22 — روابط عمومی، اعتبار و مدیریت بحران
- **مالک روش:** E02. ابزارهای تحلیل منتخب (مشروط به نیاز): M03,M04,M08,M09,E07,B05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E05,E06,E08.
- **ورودی تخصصی:** ذی‌نفع، هدف ارتباطی، موضوع، شواهد، رسانه، risk و spokesperson.
- **روش تدوین و انتخاب:** نقشه ذی‌نفع و مسئله؛ انتخاب پیام مستند و کانال؛ چارچوب AMEC output/outtake/outcome/impact؛ سناریوی پاسخ بحران، escalation و بازبینی.
- **خروجی عملی:** PR plan، media brief، response matrix، measurement.
- **KPI:** quality coverage، message recall، trust/sentiment با روش معتبر، outcomes.
- **قید و fallback:** AVE معادل ارزش PR نیست؛ ادعای تاییدنشده یا پاسخ بحران خودکار ممنوع.
- **پشتوانه:** R31,R07,R05.

### ST23 — شراکت، Affiliate و Referral
- **مالک روش:** S06. ابزارهای تحلیل منتخب (مشروط به نیاز): M03,M04,M05,M06,B01,B03,B05,B06,E07. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E03,E04,B04,E08.
- **ورودی تخصصی:** شریک، مخاطب مشترک، هزینه/کمیسیون، attribution، حقوق و ظرفیت.
- **روش تدوین و انتخاب:** ارزیابی strategic fit و economics؛ تعریف ارزش دوطرفه، شرایط و disclosure؛ pilot، attribution و fraud checks؛ مقایسه lift و cannibalization.
- **خروجی عملی:** partner scorecard، proposal، referral rules و کنترل کیفیت.
- **KPI:** qualified referrals، net contribution after commission، incremental acquisition، fraud/returns.
- **قید و fallback:** کمیسیون و فروش تکراری/خودارجاع کنترل؛ consent و disclosure لازم.
- **پشتوانه:** R24,R19,R13.

### ST24 — ورود به بازار بین‌المللی / Export & localization
- **مالک روش:** S06. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M02,M03,M04,M05,M06,B01,B02,B06,S05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E03,E04,E05,B04,E08.
- **ورودی تخصصی:** کشور/قلمرو، تقاضا، رقیب، ارز، هزینه واردات/تحویل، زبان، مقررات و کانال.
- **روش تدوین و انتخاب:** screen بازار و قیود ورود؛ standardization vs adaptation محصول/پیام/قیمت؛ landed cost و FX scenario؛ شریک/کانال؛ pilot و gate حقوقی.
- **خروجی عملی:** market selection matrix، localization plan، landed economics و launch roadmap.
- **KPI:** net contribution در ارز ثابت، qualified demand، conversion، fulfillment SLA.
- **قید و fallback:** قانون/مالیات/تحریم/پرداخت از متخصص و منبع جاری؛ هیچ فرض دسترسی قانونی.
- **پشتوانه:** R32,R01,R27.

### ST25 — رویداد، نمایشگاه، اسپانسرینگ و بازاریابی حضوری
- **مالک روش:** E02. ابزارهای تحلیل منتخب (مشروط به نیاز): M03,M04,M05,M06,M08,B01,B03,B05,E06. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E03,E04,B04,E08.
- **ورودی تخصصی:** هدف، شرکت‌کنندگان/مخاطب، هزینه کامل، ظرفیت، قرارداد و consent.
- **روش تدوین و انتخاب:** ارزیابی تناسب مخاطب و هدف؛ مقایسه گزینه حضور/اسپانسرینگ؛ برنامه قبل/حین/بعد و follow-up؛ ثبت lead واجد شرایط؛ آزمون یا گروه مقایسه مناسب.
- **خروجی عملی:** event brief، logistics/owner، lead capture و follow-up.
- **KPI:** qualified meetings/leads، cost per qualified lead، pipeline و contribution با پنجره مناسب.
- **قید و fallback:** تعداد بازدید یا معادل ارزش تبلیغاتی دلیل ROI نیست؛ اثر causal بدون طرح گزارش نشود.
- **پشتوانه:** R31,R24,R13.

### ST26 — تجربه مشتری و بازاریابی خدمات / CX & service
- **مالک روش:** M09. ابزارهای تحلیل منتخب (مشروط به نیاز): M01,M04,M05,M06,M07,B01,B03,B05,E05. ابزارهای طراحی/اجرا و بازبینی: S03,E01,E02,E04,E06,B04,E08.
- **ورودی تخصصی:** نقاط تماس، شکایت، service SLA، journey، ظرفیت، داده تجربه و رفتار.
- **روش تدوین و انتخاب:** نقشه journey واقعی/فرضی؛ شناسایی friction و moments of value؛ service blueprint و handoff؛ اولویت بر اساس شدت/فراوانی/هزینه؛ recovery و آزمون تغییر.
- **خروجی عملی:** journey/blueprint، service standards، backlog بهبود و آموزش.
- **KPI:** time-to-resolution، first-contact resolution، CSAT با نرخ پاسخ، retention، contribution.
- **قید و fallback:** رضایت پاسخ‌دهندگان معادل همه مشتریان نیست؛ بهبود SLA بدون ظرفیت تایید نشود.
- **پشتوانه:** R05,R09,R23,R27.


## ۴. قرارداد پیاده‌سازی recipe و وابستگی‌ها

### ۴.۱ مدل ثابت و مشترک
Recipe catalog در کد نسخه‌دار (JSON/YAML یا ساختار Python به انتخاب تیم، با Pydantic schema). فقط metadata و ارجاع به ابزارهای موجود؛ داده اصلی در workspace PostgreSQL. حداقل فیلد:
- strategy_id (ST01–ST26)، recipe_version، title/fa/en، aliases، applicability (market/business context)، owner_tool_id، candidate_tools، stage_templates، required_evidence_rules، output_schema_version، metric_refs، source_ids، method_limits، availability derived from registry.
- PipelineRun همان قرارداد فعلی: mode=domain یا full برحسب پوشش، recipe_id? و recipe_version? به‌عنوان metadata اختیاری، نه mode چهارم. اجرای single tool تغییری نمی‌کند. PipelineStep نقش stage_key و output binding مشخص دارد؛ plan_version، workspace/profile_version و dependencies حفظ شوند.
- StrategyResult یک گزارش ترکیبی موجود (AnalysisRun/PipelineRun report)، نه جدول مستقل Strategy: context_ref، strategy_id/version، goal_refs، evidence_refs، assumptions[], options[], chosen_option_ref?، decision_ref?، channel_roles[]، KPI_refs، budget_plan_ref?، action_refs[]، experiment_refs[]، review_schedule، coverage و missing_requirements. هر گزاره دارای نوع observed/estimate/hypothesis/recommendation و source/ref، date و scope؛ عدم قطعیت estimate مستند. داده غیرواقعی صریحاً hypothetical.
- قابلیت اجرا از feature registry و state هر ابزار محاسبه می‌شود؛ یک recipe به دلیل تعریف سند، «قابل اجرا» نمی‌شود. نسخه MVP همان ۸ ابزار (S01,S03,M01,M05,M06,B01,B03,E01) و ثبت KPI پایه B05 باقی می‌ماند. امکان طرح استراتژی اولیه از ابزارهای فعال و ورودی تاییدشده؛ مسیر کامل فقط بعد از توسعه مراحل لازم.
- API جدید مستقل لازم نیست: GET کاتالوگ/metadata از endpoint کاتالوگ موجود یا افزودن فیلد recipe در پاسخ؛ POST pipeline-previews با recipe_id/version و context؛ سپس همان pipeline create/status/commands. انتخاب recipe و نتایج از workspace فعلی، tenant isolation و مجوز عضو رعایت شود.

### ۴.۲ قواعد ساخت DAG قابل اجرا
مرحله D (تشخیص S01 اختیاری)، R (شواهد M/B مرتبط و S02؛ داده‌های گذشته)، O (طراحی گزینه با مالک روش و S04/S05 در صورت نیاز؛ E02/E03/E04 می‌توانند در حالت draft برای گزینه‌ها خروجی بدهند)، C (S03 و ثبت انتخاب انسانی)، P (طرح E01 و جزئیات اجرایی؛ بودجه/ظرفیت reconciliation)، A (تایید انسانی برنامه)، V (B04 protocol، B05/E08 review بعد از نتیجه واقعی). B04 protocol می‌تواند پیش از A تهیه شود؛ effect تنها با داده آزمون بعد از اجرا. B05 baseline در R و outcome در V اجراهای مجزا هستند. اگر E01 برای یک گزینه به‌عنوان ورودی S03 لازم باشد، فقط cost/feasibility preview بدون decision approved است؛ E01 نهایی بعد از C. وابستگی‌ها به artifact مرحله قبلی و شناسه اجرا، نه اتصال حلقوی نام ابزار. مثال M09←B03 از داده قبلی؛ B03 نباید منتظر E04 برنامه همین run باشد. داده manually_supplied فقط با منبع، واحد، دوره و تایید؛ جای اجرای ابزار unavailable را در coverage پنهان نکند. اگر خروجی الزامی غایب، مرحله blocked؛ مراحل مستقل ادامه. چرخه بازبینی E08 فقط نسخه/run بعدی می‌سازد. پیش‌نمایش، skip optional، pause/resume، idempotency و partial result طبق معماری فعلی.

### ۴.۳ قواعد فعال‌سازی و روش‌های عددی
- پایه: شواهد دستی، Decimal، Pandas/SQL، Pydantic و AI adapter برای خلاصه/پیشنهاد؛ هیچ محاسبه مالی یا ادعای اثربخشی قطعی به LLM واگذار نشود.
- اگر پیمایش پیچیده: M01/svy طبق موتور؛ برای متن M04 embedding و مرور انسانی؛ برای segment M05 الگوریتم متناسب نوع داده؛ M06 conjoint یا MDS فقط داده طراحی‌شده؛ B02 forecasting یا قیمت‌گذاری، B03 retention/churn و B04 causal تنها تحت پیش‌شرط‌های سند علمی.
- E03: اگر response خطی معتبر، LP/MILP حسب مسئله؛ اگر اشباع/بازده نزولی، response curve یا مدل مناسب و محدودیت دامنه. Meridian/PyMC-Marketing تنها مطابق قرارداد علمی و داده کافی؛ جداسازی وابستگی موجود حفظ شود. هرگونه برآورد ROI شرطی است و baseline/attribution/causal جدا نگهداری شود.
- برنامه آزمایشی: مبلغ، بازه، واحد تخصیص، primary metric، MDE/power اگر قابل تعیین، stop و harm guardrail، owner و زمان بازبینی. توقف بر مبنای قاعده از پیش تعریف شده؛ توقف آماری زودرس بدون روش sequential ممنوع. هزینه و درآمد صفر با داده ناموجود فرق دارد.

## ۵. سنجه‌های مشترک و قرارداد داده
همه KPIها MetricDefinition موجود: id، numerator/denominator و واحد، grain (customer/account/order/session/impression/location)، زمان/پنجره attribution، cohort، منبع و timezone، ارز، baseline، target، owner، cadence و guardrail. هدف از ظرفیت/اقتصاد و تاریخچه یا فرضیه تاییدشده می‌آید؛ هیچ benchmark عمومی به‌صورت target اجباری. مقایسه دوره‌ها با یکسان‌سازی تعاریف و وضعیت cohort. KPI اولیه کسب‌وکار، leading indicator، diagnostic و guardrail از هم جدا شوند.

| سنجه | تعریف / کنترل |
|---|---|
| CAC | هزینه جذب تعریف‌شده / تعداد مشتری جدید همان cohort/پنجره؛ paid و blended جدا؛ CPA برای رویداد غیرمشتری CAC نیست. |
| contribution / ROMI | درآمد خالص منهای هزینه متغیر طبق تعریف B01؛ ROMI=(حاشیه افزایشی پیش از هزینه کمپین − هزینه کمپین)/هزینه کمپین، فقط با شواهد افزایشی معتبر؛ هزینه کمپین دوبار کم نشود. |
| ROAS | درآمد منتسب طبق مدل و پنجره / هزینه رسانه؛ نه profit یا lift. iROAS فقط با درآمد افزایشی معتبر. |
| CTR / CPC / CPM | clicks/impressions، spend/clicks، spend/impressions×1000؛ شمارش پلتفرم‌ها و currency/window صریح. |
| CVR / stage conversion | تعداد واحد یکتای تبدیل‌شده در پنجره / واحد واجد شرایط همان cohort؛ session و person یکی نیستند. |
| CPL / CPQL | هزینه تعریف‌شده / lead یا qualified lead یکتا با معیار qualification نسخه‌دار. |
| Retention / churn | درصد باقی‌مانده یا ریزش در cohort واجد شرایط در پنجره؛ churn قراردادی و غیرقراردادی تعریف جدا؛ censoring کنترل. |
| LTV / payback | حاشیه مورد انتظار مشتری در افق مشخص، با تنزیل و نگهداشت مستند؛ payback نخستین زمان عبور حاشیه تجمعی از CAC، نه نسبت ثابت مگر فرض حاشیه ثابت. |
| Engagement rate | تعاملات تعریف‌شده / reach یا impressions یا followers؛ مخرج صریح و نرخ‌های ناهم‌تعریف بین کانال‌ها مقایسه نشوند؛ reach چند پلتفرم dedup نشده جمع به عنوان افراد یکتا ممنوع. |
| Email | unique clicks/delivered؛ unsubscribe و spam complaints با مخرج و قرارداد provider؛ open rate diagnostic به علت privacy. |
| Brand awareness | پاسخ معتبر آگاه/کل پاسخ معتبر با نمونه و weighting متناسب؛ assisted/unaided جدا. |
| SEO | Search Console clicks/impressions/CTR و صفحات index؛ GA/CRM conversion با attribution متفاوت؛ join بدون grain مشترک و داده ناقص ممنوع. |
| B2B pipeline | sum ارزش opportunityهای واجد تعریف و وضعیت؛ weighted pipeline فقط با احتمال stage معتبر و horizon؛ booked/recognized revenue جدا. |
| Sell-through / return | واحد فروش نهایی / موجودی قابل فروش تعریف‌شده؛ سفارش برگشتی/کل سفارش cohort با پنجره کافی. |
| Incremental lift | اختلاف outcome گروه treatment و control طبق estimand و واحد تخصیص؛ CI و فرض‌ها؛ attribution یکسان نیست. |
| CSAT | پاسخ رضایت تعریف‌شده / پاسخ‌های معتبر؛ همراه response rate و روش جذب. |
| Budget | sum هزینه همه اقدام‌ها + ذخیره مصوب ≤ سقف؛ هزینه رسانه، تولید، ابزار، کارمزد، نیروی انسانی، مالیات/ارز مطابق scope؛ اشتراک هزینه میان recipeها یک بار در plan مشترک. |

مخرج صفر/ناموجود null و reason، نه صفر یا بی‌نهایت. هدف عددی بدون baseline و مدل، proposed_target است. KPI و حدود عددی مثال‌های این سند فرضی‌اند و نباید به default مشتری تبدیل شوند.

## ۶. UX عملی، داده و تحویل
در بخش «ابزارها و پایپلاین‌ها» یک تب/فیلتر «استراتژی‌ها»؛ جست‌وجوی نام فارسی/انگلیسی/alias. صفحه اولیه فقط نوع کسب‌وکار از پروفایل، هدف، بودجه/افق (اختیاری برای پیش‌نویس)، بازار هدف و محدودیت. اطلاعات ثبت‌شده دوباره پرسیده نشود. سؤال‌های تخصصی فقط وقتی داده واقعاً کم است. بعد: پیش‌نمایش مسیر، داده‌های لازم، ابزارهای فعال/غیرفعال، امکان حذف اختیاری، انتخاب داده قبلی، اجرا و نمایش نتیجه/تصمیم و برنامه. نه ۲۶ منوی اصلی و نه فرم بلند ۲۹ ابزار.

خروجی هر strategy pack: خلاصه یک صفحه، تشخیص، هدف/بازار/positioning، گزینه‌ها و rationale، نقش کانال یا عملیات، KPI dictionary، بودجه و برنامه ۳۰/۶۰/۹۰ روزه یا افق کاربر، owner/dependency و اولویت، experiment/measurement plan، محدودیت‌ها و شواهد. اگر owner یا budget تایید نشده باشد draft، و اگر داده مفقود است نیاز به داده یا تحقیق. خروجی مدیریتی PDF/DOCX/XLSX/PPTX از ReportViewModel مشترک و CSV برای KPI/actions در DEV طبق C-02، بدون موتور گزارش مستقل. تاریخچه و نسخه استراتژی در بخش موجود. برای استراتژی ترکیبی (مثلاً digital + SEO + social)، recipe فرزند انتخاب می‌شود، مرحله مشترک فقط یک‌بار با input snapshot برابر اجرا، و بودجه مشترک با شناسه cost line و تخصیص یکتا؛ targetهای متعارض در S03 حل می‌شوند. ترکیب recipeها مرحله پیشرفته پس از اجرای پایه است و MVP نیازمند UI پیچیده برای آن نیست.

### اتصال داده (اولویت عملی)
1. ورودی دستی و CSV/XLSX دارای grain, id, timestamp, metric, currency, source و consent status در صورت لزوم؛ نگاشت ستون و پیش‌نمایش/validation. CRM و سفارش pseudonymous IDs؛ عدم ارسال اطلاعات شخصی خام به مدل.
2. اتصال read-only اختیاری و مجاز فقط GA4 Data API، Google Ads reporting، Search Console Search Analytics و CRM (vendor بعد از تعیین مالک) طبق [قرارداد C-05](marketing-competitive-enhancements.md). URL Inspection فقط read-only مشروط در همان Search Console. Facebook/Meta، social، فروشگاه، ایمیل و حسابداری connector ندارند؛ داده مجاز سایر منابع فقط دستی/CSV/XLSX. نسخه، scopes، quota، mapping و validation قبل از فعال‌سازی؛ داده aggregate افراد یکتا نیست، Search Console همه سطرها را تضمین نمی‌کند. هیچ connector فعال یا حساب متصل ادعا نمی‌شود.
3. قوانین بازاریابی، افشای تبلیغ، opt-out، حقوق محتوا و محدودیت صنعت/کشور با منابع جاری و تایید متخصص. اتوماسیون خروجی به بیرون خارج از scope پیش‌فرض.

## ۷. نمونه‌های عملی کامل (synthetic، نه پیشنهاد برای کسب‌وکار واقعی)

### A. استراتژی دیجیتال + social برای فروشگاه
فرض: ۱۰۰۰ واحد بودجه در ۳۰ روز، هدف افزایش مشتری جدید سودآور، محصول با حاشیه قبل از جذب ۴۰ واحد به ازای سفارش، امکان خدمت ۶۰ سفارش اضافه، داده عملکرد کانال موجود نیست. مراحل: S01 → M05/M06 (مشتری و پیام از شواهد تاییدشده) → B01 (حاشیه) → S03 (گزینه تبلیغ search pilot، social content pilot یا ادامه وضعیت موجود) → E01 (پیش‌نویس و سقف) → E02/E03 در صورت فعال بودن (brief کانال) → B04 protocol → تایید مدیر → ثبت outcome → B05/E08.
- بودجه نمونه: search pilot ۳۰۰، social paid pilot ۲۰۰، content production ۲۰۰، tracking ۱۰۰، ذخیره ۲۰۰؛ مجموع ۱۰۰۰. هیچ فروش یا ROAS پیش‌بینی نمی‌شود. سقف CAC نقطه سربه‌سر اولین سفارش در این فرض ۴۰، نه CAC target قطعی؛ هزینه ثابت/مرجوعی/حاشیه آینده در صورت وجود وارد شود.
- برنامه: روز ۱–۷ تکمیل اندازه‌گیری و دو brief، ۸–۲۱ اجرای پایلوت پس از تایید و تخصیص، ۲۲–۳۰ مرور داده و تصمیم scale/hold/stop. مالک tracking، content، ads و review از تیم واقعی تعیین شود؛ بدون owner فقط draft. primary = incremental contribution اگر lift قابل سنجش، در غیر این صورت attributed contribution جداگانه و بدون causal claim. سقف ظرفیت ۶۰ و هزینه ۱۰۰۰ guardrail.
- اگر ۱۰ مشتری جدید از search با spend=۳۰۰ در پنجره تعریف‌شده ثبت شوند: attributed CAC=۳۰؛ contribution پیش از media=۴۰۰، بعد از media=۱۰۰ (با فرض یک سفارش هر مشتری و سایر هزینه‌ها خارج scope). بدون کنترل، این ۱۰۰ اثر افزایشی نیست؛ ROMI null. reserve بدون تایید خرج نمی‌شود.

### B. B2B و ABM
فرض: ۳۰ حساب ICP مستند، ظرفیت ۱۰ جلسه در ماه، بودجه ۶۰۰، هیچ نرخ تاریخی قابل اعتماد. M05/M06 → S03 (ABM محدود به ۱۰ حساب مناسب یا demand gen عمومی، گزینه status quo) → E01 → E04/E02 → B04 → B05/E08. هدف پیشنهادی عملیاتی: حداکثر ۱۰ جلسه و ثبت qualified opportunity؛ تعداد برد/درآمد پیش‌بینی نشود. اولویت حساب‌ها با fit/value/effort مستند و تایید مدیر، نه احتمال خرید ساخته‌شده. بودجه ۲۵۰ research/enablement، ۲۰۰ outreach content، ۱۰۰ measurement، ۵۰ reserve. اگر ۸ جلسه و ۳ فرصت واجد شرایط از ۳۰ حساب ثبت شود، نرخ فرصت account-level=۳/۳۰=۱۰٪ (اگر denominator همه ۳۰ واجد exposure/پیگیری مطابق تعریف باشند؛ در غیر این صورت cohort واقعی). هیچ استنباط اثر ABM از این عدد. اگر تیم فقط ۵ جلسه ظرفیت دارد، طرح قبل از تایید اصلاح شود.

### C. SEO و CRM در کسب‌وکار با داده محدود
هدف رزرو واجد شرایط. Search Console فقط clicks/impressions را دارد و CRM اتصال سفارش ندارد. SEO ابتدا technical audit و intent-to-page backlog (E05/E02/E03 در صورت فعال بودن)، سپس تعریف event رزرو و reconcile با CRM. CRM consent غایب: outbound blocked، داده تجمعی مجاز برای تحلیل؛ مسیر SEO مستقل ادامه. خروجی پیش‌نویس و measurement plan، نه ادعای organic revenue. بعد از ثبت داده، B03/B05 و E08 review. هیچ فعالیت بیرونی توسط recipe انجام نمی‌شود.

## ۸. معیار پذیرش طراحی/DEV (تست محدود پیاده‌سازی)
- Catalog: ۲۶ شناسه یکتا، owner/candidate/execution در ۲۹ شناسه معتبر، همه source_idها موجود، alias غیرمبهم یا سؤال انتخاب. نسخه و وضعیت derived از registry.
- DAG: مرحله لازم بدون dependency معتبر blocked؛ no cycles؛ نتیجه پیشین قابل reuse، input تغییر یافته نسخه جدید؛ شاخه مستقل ادامه؛ pause/resume idempotent و گزارش coverage دقیق.
- Evidence: داده ناموجود null، claim بی‌شاهد hypothesis/unverified؛ بدون causal design، incrementality/ROMI ممنوع. داده اختلاط واحد/ارز/پنجره رد شود.
- Budget: مثال A ۱۰۰۰، افزایش هر هزینه به ۱۰۰۱ بدون کاهش دیگر/افزایش مصوب سقف رد شود؛ رزرو دوباره شمرده نشود؛ ۶۰ ظرفیت و ۶۱ سفارش پیشنهادی violation. مثال B نرخ ۳/۳۰=.10 فقط با cohort معتبر.
- UX/Approval: استراتژی فقط از ۸ ابزار MVP نباید complete اعلام شود اگر ابزار الزامی غیرفعال است؛ نمایش داده مفقود و draft؛ CTA فعال‌سازی بدون approval، owner، policy و guardrails ممنوع. کاربر بتواند مستقل digital، social یا SEO را انتخاب کند و گزارش چند strategy مشترک هزینه تکراری نداشته باشد.
- Privacy: workspace A نمی‌تواند evidence B را reuse کند؛ opt-out فعال هرگز وارد پیام‌رسانی نشود؛ هیچ خروجی خودکار به بیرون. نسخه AI/provider و evidence refs در audit؛ template دستی در صورت نبود AI.
- محدودیت تست: fixture و آزمون اتصال ابزار هنگام DEV کافی برای صحت کد؛ الگوریتم‌های منتشرشده را از صفر اعتبارسنجی نمی‌کنیم. کارایی پیش‌بینی/اثر در context واقعی تابع داده/فرض‌ها و monitoring است. در این commit هیچ CI جدید، اجرای مدل، تست runtime یا اعتبارسنجی تجربی ادعا نمی‌شود.

## ۹. رجیستری شواهد
مرور هدفمند منابع بنیادی، پژوهش‌های به‌روز ۲۰۲۵–۲۰۲۶، فراتحلیل‌ها و مستندات رسمی. این یک systematic review مستقل با غربالگری PRISMA نیست؛ در دسترسی محدود، رکورد/چکیده و صفحات رسمی بررسی شده و متن کامل همه مقالات ارزیابی نشده است. R09 و R26 از مرور پژوهشی قبلی پروژه به ارث رسیده‌اند و در این نوبت به‌صورت مستقل متن کامل آن‌ها مرور نشده است. قدرت شواهد وابسته به نوع مطالعه و مسئله است؛ منابع فنی/استاندارد حرفه‌ای صرفاً قواعد عملی را پشتیبانی می‌کنند؛ از case study، ارتباط آماری یا ادعای vendor اثر علّی تعمیم داده نشود. انتخاب و مسیرهای فوق synthesis طراحی M-Tools هستند، نه یک چارچوب ۲۶تایی منتشرشده یا تضمین موفقیت. برای الگوریتم‌ها، بنچمارک‌ها و نسخه کتابخانه‌ها، سند Evidence Review و Scientific Engine مرجع است؛ این سند نسخه runtime یا وابستگی جدید تحمیل نمی‌کند.

| ID | منبع و تاریخ | لینک | نقش و محدودیت |
|---|---|---|---|
| R01 | Varadarajan (2010), Strategic marketing and marketing strategy, JAMS | https://doi.org/10.1007/s11747-009-0176-7 | چارچوب نظری تصمیم‌های بازار/محصول و مزیت؛ نه الگوریتم اثبات‌شده. |
| R02 | Morgan et al. (2019), Research in marketing strategy, JAMS | https://doi.org/10.1007/s11747-018-0598-1 | مرور پژوهش‌های استراتژی، اجرا و محدودیت شواهد. |
| R03 | The dynamics and contingencies of marketing and business performance relationship (2026) | https://doi.org/10.1016/j.iedeen.2026.100321 | فراتحلیل ۸۳ مطالعه؛ تناسب زمینه و قابلیت‌ها مهم است، اثر ثابت جهانی نیست. |
| R04 | Kannan & Li (2017), Digital marketing: A framework, review and research agenda, IJRM | https://www.sciencedirect.com/science/article/pii/S0167811616301550 | مرور و چارچوب touchpoint، اقدامات و پیامدهای دیجیتال. |
| R05 | Lemon & Verhoef (2016), Understanding Customer Experience Throughout the Customer Journey, JM | https://doi.org/10.1509/jm.15.0420 | چارچوب سفر و تجربه چند نقطه تماس؛ مسیر هر کسب‌وکار باید با داده خودش تعریف شود. |
| R06 | Li, Larimo & Leonidou (2021), Social media marketing strategy, JAMS | https://doi.org/10.1007/s11747-020-00733-3 | چارچوب چهار مؤلفه و taxonomy مبتنی بر engagement؛ شواهد مطالعات و داده مدیران، نه جدول جهانی فرکانس. |
| R07 | Keller (1993), Customer-Based Brand Equity, JM | https://doi.org/10.1177/002224299305700101 | چارچوب نظری دانش و پاسخ برند؛ نه امتیاز واحد جهانی. |
| R08 | Henard & Szymanski (2001), Why Some New Products are More Successful than Others, JMR | https://doi.org/10.1509/jmkr.38.3.362.18861 | فراتحلیل محرک‌های موفقیت محصول؛ مزیت، نیاز، بازار و منابع. |
| R09 | Customer insights for innovation (2024/2025), JAMS | https://doi.org/10.1007/s11747-024-01051-8 | مرجع مرور پیشین پروژه برای چرخه insight؛ رجوع به سند evidence review. |
| R10 | Bijmolt, Van Heerde & Pieters (2005), New empirical generalizations on determinants of price elasticity, JMR | https://doi.org/10.1509/jmkr.42.2.141.62296 | فراتحلیل ناهمگنی کشش؛ کشش زمینه‌مند، نه ضریب پیش‌فرض. |
| R11 | Koob (2021), Determinants of content marketing effectiveness, PLOS ONE | https://pubmed.ncbi.nlm.nih.gov/33793631/ | مطالعه تجربی مدیریتی؛ ارتباط روشنی استراتژی و نیاز/کیفیت محتوا با اثربخشی؛ علیت قطعی نیست. |
| R12 | Influencer marketing effectiveness: A meta-analytic review (2025), JAMS | https://doi.org/10.1007/s11747-024-01052-7 | فراتحلیل ۲۵۱ مقاله؛ اثر وابسته به ویژگی پیام، فرد، محصول و کانال. تکمیل: https://doi.org/10.1007/s11747-025-01107-3 (2025 online/2026 issue). |
| R13 | Lewis & Rao (2015), Unfavorable Economics of Measuring Returns to Advertising, QJE | https://doi.org/10.1093/qje/qjv023 | ۲۵ آزمایش میدانی؛ عدم قطعیت بازده تبلیغات حتی با نمونه بزرگ. |
| R14 | Blake, Nosko & Tadelis (2015), Consumer Heterogeneity and Paid Search Effectiveness, Econometrica | https://doi.org/10.3982/ECTA12423 | آزمایش میدانی eBay؛ تفاوت اثر بین مشتریان، attribution مشاهده‌ای با اثر یکی نیست. |
| R15 | Google Meridian causal methodology | https://developers.google.com/meridian/docs/causal-inference/about-mmm-causal-inference-methodology | مستند فنی؛ برآورد ROI علّی مشروط به فرض‌ها و DAG، نه fit تنها. |
| R16 | Google Search Central, SEO Starter Guide & Search Essentials | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | راهنمای رسمی فنی، نه پژوهش اثرگذاری جهانی. https://developers.google.com/search/docs/essentials |
| R17 | Search Console API / Search Analytics; GA + Search Console | https://developers.google.com/webmaster-tools/v1/searchanalytics | محدودیت بازگشت top rows؛ راهنمای مقایسه داده: https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console |
| R18 | Google Ads Conversion Lift and lift reporting | https://support.google.com/google-ads/answer/12003020 | مستند رسمی آزمایش افزایشی؛ قابلیت و eligibility وابسته به حساب. API: https://developers.google.com/google-ads/api/docs/experiments/lift-reporting |
| R19 | FTC Disclosures 101 for Social Media Influencers | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | راهنمای ایالات متحده؛ به بازارهای دیگر تعمیم حقوقی داده نشود. |
| R20 | Sahni, Wheeler & Chintagunta (2018), Personalization in Email Marketing, Marketing Science | https://www.gsb.stanford.edu/faculty-research/publications/personalization-email-marketing-role-non-informative-advertising | آزمایش تصادفی در سه شرکت؛ شخصی‌سازی می‌تواند اثرگذار باشد، اثر عددی تعمیم خودکار ندارد. |
| R21 | Nudges in email marketing campaigns (2025), ECRA | https://doi.org/10.1016/j.elerap.2025.101534 | آزمایش‌های میدانی؛ اثر subject/sender وابسته به زمینه، نه قاعده ارسال عمومی. |
| R22 | Gmail Email sender guidelines; Apple Mail Privacy Protection | https://support.google.com/mail/answer/81126 | قواعد ارسال و opt-out و هویت؛ محدودیت مشاهده open: https://www.apple.com/legal/privacy/data/en/mail-privacy-protection/ |
| R23 | Payne & Frow (2005), A Strategic Framework for CRM, JM | https://doi.org/10.1509/jmkg.2005.69.4.167 | چارچوب CRM فرایندی؛ مشتری، ارزش، کانال و اطلاعات. |
| R24 | Palmatier et al. (2006), Factors Influencing Effectiveness of Relationship Marketing, JM | https://doi.org/10.1509/jmkg.70.4.136 | فراتحلیل رابطه‌محوری؛ کاربرد متناسب با نوع رابطه، نه تضمین سود. |
| R25 | Understanding Loyalty Program Effectiveness across the Customer Journey (2026), Journal of Retailing | https://www.sciencedirect.com/science/article/pii/S0022435926000758 | فراتحلیل تازه؛ مبنای ارزیابی برنامه در مراحل سفر؛ در این مرور تنها رکورد/خلاصه قابل مشاهده بررسی شد و اثر عددی نقل نمی‌شود. |
| R26 | Where A/B Testing Goes Wrong (2025), Journal of Marketing | https://doi.org/10.1177/00222429241275886 | مرجع مرور علمی پیشین پروژه درباره delivery و اعتبار آزمایش؛ اصول B04 حاکم‌اند. |
| R27 | The Effectiveness of Omnichannel Strategy: A Meta-analytical Approach (2025) | https://doi.org/10.1177/23197145251343708 | فراتحلیل ۶۳ مطالعه؛ سازوکارها و تفاوت زمینه‌ای. تکمیل مرور بخش‌بندی کانال ۲۰۲۶: https://doi.org/10.1057/s41270-026-00538-3 |
| R28 | Unpacking account-based marketing (2026), Industrial Marketing Management | https://doi.org/10.1016/j.indmarman.2026.02.006 | مفهوم‌پردازی و فعالیت‌های ABM؛ شواهد نوظهور، مطالعه/نمونه صنعتی تضمین ROI نیست. تکمیل مدیریت پس از فروش B2B: https://doi.org/10.1016/j.jbusres.2025.115700 |
| R29 | From Fragmentation to Value Cocreation: A Meta-Review of Omnichannel Research (2026) | https://doi.org/10.1177/23409444261460902 | مرور مرورها؛ نیاز به هماهنگی کانال‌ها، داده و عملیات، نه صرف حضور چندکاناله. |
| R30 | Google Business Profile, Tips to improve local ranking | https://support.google.com/business/answer/7091 | راهنمای رسمی relevance/distance/prominence؛ تضمین رتبه نمی‌دهد. |
| R31 | AMEC Integrated Evaluation Framework / Barcelona Principles 4.0 (2025) | https://amecorg.com/amecframework/ | استاندارد حرفه‌ای سنجش ارتباطات از خروجی تا نتیجه و اثر؛ نه پژوهش causal مستقل. |
| R32 | Digital standardization vs. adaptation: Mitigating the liability of outsidership (2025), IBR | https://doi.org/10.1016/j.ibusrev.2025.102487 | مرور ادبیات استانداردسازی/انطباق؛ انتخاب وابسته به بازار و قابلیت‌ها. |

## ۱۰. تصمیم توسعه
تمام مسیرها طراحی و در catalog مستندند. اجرای اولیه از Marketing/Digital/Social با ابزارهای موجود به‌عنوان پیش‌نویس شفاف، سپس تکمیل قابلیت‌های E02/E03/B04/B05 و سایر ابزارها طبق roadmap مصوب؛ ترتیب دقیق توسعه تابع backlog مالک است و MVP بدون تایید مالک توسعه دامنه نمی‌یابد. استراتژی‌های تخصصی جدید در آینده به‌صورت recipe اضافه می‌شوند و تا زمانی که ابزار موجود کفایت دارد ابزار سی‌ام ایجاد نمی‌شود.


## ۱۱. اتصال استراتژی به برنامه‌ریزی
[Marketing Planning Library](marketing-planning-library.md) برای همه ST01–ST26 یک recipe تخصصی PL09–PL34 و ۸ الگوی مشترک دارد. استراتژی انتخاب‌ها و هدف را نگه می‌دارد؛ E01 و PLها زمان، هزینه، ظرفیت، مالک، acceptance، measurement و baseline را یکپارچه می‌کنند. برنامه اولیه در StrategyResult یک پیش‌نویس یا plan_ref است؛ بودجه/کار را دوباره نسازد. برنامه مصوب و forecast/actual جدا؛ تغییر استراتژیک به S03 ارجاع شود.

## ۱۲. اتصال جایگاه‌سازی ذهنی به استراتژی برند
ST05 از [Brand Positioning & Mental Availability Library](marketing-positioning-library.md) و زیرمسیرهای PO01–PO14 برای تشخیص ادراک فعلی، تمایز/PoP-PoD، موقعیت خرید، سنجه‌های MA و DBA، انتخاب جایگاه، آزمون و بازجایگاه‌سازی استفاده می‌کند. ST03/04/07 و سایر استراتژی‌های مرتبط همان شواهد و PositioningResult را reuse می‌کنند؛ هیچ strategy جدید یا محاسبه تکراری ایجاد نمی‌شود. S03 مالک انتخاب مصوب و PL13 مالک برنامه فعال‌سازی/سنجش، نه ساختن جایگاه واقعی از شعار. محدودیت داده و تایید انسانی حاکم است.

## تکمیل Workbench در مسیر استراتژی

[Competitive Enhancements](marketing-competitive-enhancements.md) C-12: واردسازی سند موجود به S03 StrategyResult و E01 PlanResult draft، source anchor، mapping بخش/هدف/بودجه/KPI/اقدام، conflict review و approval داخلی؛ ادامه از نسخه واردشده بدون pipeline اجباری. C-10 پیشنهاد پروفایل با review. C-04 درس‌آموخته E08 با context/evidence، reuse اختیاری در تدوین استراتژی. C-03 PR01–04 در ST06/قیمت؛ C-07 PREFMAP در ST05؛ C-08 Bass در ST03/02 فقط first adoption و fit/scenario؛ C-11 SNA در مسیر referral/partner (ST23) و CX (ST26) با داده رابطه معتبر، نه connector اجتماعی. C-01/02 template/demo و گزارش چهارفرمت مشترک. C-05 تنها چهار provider مصوب، no mutation، هیچ تغییر ۲۶ recipe یا هشت full MVP.
