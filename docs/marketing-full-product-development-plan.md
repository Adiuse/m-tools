# M-Tools — Full Product Vertical Slice Development Plan v1.0

**شناسه:** MT-FULL-DEV-V1  
**وضعیت:** FROZEN_DESIGN / EXECUTION_NOT_STARTED  
**مبنای قرارداد:** `ffe312bb7569fb17828de67cb2b0db084ad3f8bd`، [Development Baseline](marketing-development-baseline.md) و تصمیم صریح مالک: محصول کامل نهایی، نه توقف در MVP.  
**محدوده:** صرفاً نقشه توسعه و پذیرش. این سند هیچ method، connector، pipeline یا محصول اجراشده‌ای اعلام نمی‌کند و هیچ وابستگی/نسخه یا قابلیت علمی جدیدی انتخاب نمی‌کند. D0 طبق baseline فعلاً BLOCKED است.

## ۱. سیاست اجرا و حدود محصول

۷ فاز D0–D6 و ۲۲ PR برنامه‌ریزی‌شده (VS00–VS21) با ترتیب و وابستگی مشخص. VS00 gate محیط، VS01 زیرساخت، VS02–VS20 نوزده برش تحویلی قابلیت‌محور، VS21 پذیرش نهایی. برش‌های فنی D0/D1 به‌اندازه لازم برای مسیر کاربردی بعدی‌اند؛ سایر برش‌ها شامل backend/روش علمی، API، داده/ذخیره، UI، template/demo، گزارش و آزمون end-to-end همان قابلیت هستند؛ PR جداگانه صرفاً برای لایه backend یا frontend یا یک فرم کوچک ایجاد نشود. شناسه VS شماره واقعی GitHub PR نیست؛ PRهای DEV بعد از merge سند مبنا و دستور شروع مالک ایجاد شوند. هر VS یک PR با branch از آخرین مبنای پذیرفته‌شده و وابستگی‌های merge‌شده؛ اجرای موازی فقط در صورت استقلال و عدم تغییر هم‌زمان قرارداد مشترک. هیچ تغییر scope یا شکستن برش به چند PR بدون دلیل مستند و تصمیم مالک. اصلاح نقص داخل همان PR پیش از merge.

دامنه نهایی بدون تغییر: چهار موتور، ۲۹ ابزار کامل، ۷۲ method قرارداد ثبت‌شده (۲۹ پایه، ۲۸ پیشرفته، ۱۵ QT)، ۲۴ row schema، ۱۳ artifact type، ۲۳۰ fixture اولیه، ۲۶ ST، ۳۴ PL، ۱۴ PO، ۳۶ KN، ۵ F و ۱۱ C منتخب، چهار گزارش PDF/DOCX/XLSX/PPTX و فقط چهار connector مستقیم read-only GA4/Google Ads/Search Console/CRM. تمام جزئیات روش‌ها/شاخه‌ها/UX و acceptance در اسناد مصوب حتی اگر برای آن‌ها method_id جداگانه تعریف نشده، داخل برش مالک قرار دارند. **عدد ۷۲ سقف قابلیت‌های علمی نیست و ثبت ۷۲ contract به‌تنهایی اثبات پوشش همه جزئیات علمی نیست.** برای مثال VRIO، RFM، survey design، CBBE/CEP/DBA، WBS/EVM و رویه‌های validation باید مطابق بندهای مالک اجرا شوند. challengerهای اختیاری (مانند R، Chronos-2 و مدل جایگزین) طبق شرط و شواهد سند بررسی/انتخاب می‌شوند؛ فعال‌سازی همه challengerها یا همه dependencyهای اختیاری اجباری نیست. این قاعده اجازه حذف روش یا قابلیت مصوب نیست؛ اگر یک method/variant مصوب نیاز به تکمیل schema دارد، در همان VS و قبل از اجرای آن schema/fixture versioned تکمیل شود و coverage baseline با دلیل به‌روزرسانی گردد.

MVP در پایان D3 پس از gate VS00–07 یک محصول پایه قابل استفاده با ۸ ابزار اصلی و B05 پایه است؛ **milestone میانی، نه انتشار/پایان نهایی.** full-tool readiness هر ابزار پس از تمام روش‌ها و قابلیت‌های مصوب مربوط، نه صرف روش پایه. D4/D5 فازهای الزامی ادامه توسعه‌اند، نه backlog اختیاری. داده ناکافی در یک run می‌تواند needs_data صحیح باشد؛ روش غیرفعال/ساخته‌نشده نباید به اسم fallback آماده یا کامل معرفی شود. اولویت‌بندی F03 می‌تواند با evidence و تصویب مالک ترتیب را اصلاح کند، نه دامنه را. اگر دسترسی/مجوز/credential/vendor/داده پژوهشی مانع پذیرش شد، برش و release وضعیت BLOCKED/NOT_READY دارند، نه حذف پنهان.

مرجع علمی و اجرایی: [Architecture](marketing-system-architecture-v1.md)، [Scientific Engine](marketing-scientific-engine-specification.md)، [Evidence Review](marketing-29-tools-evidence-review.md)، [Tool Specifications](marketing-tool-specifications.md)، [Pipeline Architecture](marketing-decision-pipeline-architecture.md)، [UX](marketing-ux-design-v1.md)، [Workbench](marketing-workbench-design.md)، [Competitive Enhancements](marketing-competitive-enhancements.md)، [Strategy](marketing-strategy-library.md)، [Planning](marketing-planning-library.md)، [Positioning](marketing-positioning-library.md)، [Contracts](../contracts/analysis.v1.schema.json) و [Fixtures](../contracts/fixtures.v1.json). این سند مرجع حاکم **ترتیب/محدوده PR و پذیرش تحویل** است؛ در علم، امنیت، قرارداد و مجوز به اسناد مالک رجوع شود.

## ۲. فازها، برش‌ها و نقاط عطف

| فاز | برش‌ها | نقطه خروج |
|---|---|---|
| D0 — قفل و سازگاری | VS00 | core lock و compatibility واقعی |
| D1 — زیرساخت و ورود/خروج داده | VS01–02 | محیط کسب‌وکار و داده/گزارش قابل استفاده، زیرساخت مشترک |
| D2 — میزکار روزمره | VS03 | ۱۳ QT اولیه و ۳۶ KN، personal workbench مستقل |
| D3 — نقطه عطف MVP | VS04–07 | هشت ابزار MVP در دامنه پایه مصوب و B05 پایه، برنامه و گزارش؛ milestone |
| D4 — تکمیل ابزارها و اتصال‌های کاربردی | VS08–14 | روش پایه تمام ۲۹ ابزار، QT12/13، عملیات/شبکه/حافظه و چهار connector؛ اتصال‌ها gate مستقل دارند |
| D5 — روش‌های پیشرفته و کتابخانه‌های کامل | VS15–20 | روش‌های پیشرفته مصوب و همه PO/ST/PL با pipeline و full-tool readiness |
| D6 — پذیرش نهایی | VS21 | پذیرش یکپارچه و شواهد واقعی/پایلوت؛ تصمیم release مالک |

جدول برنامه PR و وابستگی مستقیم (تمام وابستگی‌های transitively لازم نیز اعمال می‌شوند؛ فازها به ترتیب اجرا/پذیرش می‌شوند):

| PR plan ID | فاز | موضوع | پیش‌نیاز مستقیم | روش‌های قرارداد |
|---|---|---|---|---:|
| VS00 | D0 | Stack lock & compatibility | — | 0 |
| VS01 | D1 | Foundation — حساب، کسب‌وکار و اجرای مشترک | VS00 | 0 |
| VS02 | D1 | Data intake, executive exports & company profile | VS01 | 0 |
| VS03 | D2 | Daily Workbench — Quick Tools, Knowledge & personalization | VS01، VS02 | 13 |
| VS04 | D3 | تشخیص مسئله تا انتخاب استراتژیک | VS01، VS02، VS03 | 2 |
| VS05 | D3 | تحقیق، بخش‌بندی و جایگاه‌سازی اولیه | VS01، VS02، VS03، VS04 | 5 |
| VS06 | D3 | اقتصاد مشتری، قیف و KPI پایه | VS01، VS02، VS03 | 3 |
| VS07 | D3 | برنامه یکپارچه و واردسازی استراتژی قبلی | VS02، VS04، VS05، VS06 | 2 |
| VS08 | D4 | Market intelligence, TAM, qualitative & PMF | VS02، VS05، VS06 | 5 |
| VS09 | D4 | مدل کسب‌وکار، اولویت، سناریو و GTM | VS04، VS06، VS08 | 6 |
| VS10 | D4 | قیمت، آزمایش و تخصیص سرمایه پایه | VS02، VS06، VS09 | 5 |
| VS11 | D4 | کمپین، رسانه، فروش و چرخه مشتری | VS04، VS06، VS07، VS08، VS09، VS10 | 3 |
| VS12 | D4 | عملیات، منابع، ذی‌نفعان و حافظه سازمانی | VS06، VS07، VS11 | 7 |
| VS13 | D4 | برند، سفر مشتری، شبکه روابط و Process Mining | VS05، VS06، VS08، VS11، VS12 | 5 |
| VS14 | D4 | چهار اتصال داده و کیفیت گزارش چندمنبعی | VS02، VS06، VS11، VS12 | 0 |
| VS15 | D5 | Scientific research & full positioning library | VS05، VS08، VS09، VS10، VS11، VS12، VS13 | 5 |
| VS16 | D5 | Pricing research, demand forecast & causal analytics | VS08، VS10، VS15 | 7 |
| VS17 | D5 | Customer lifetime, churn, lead & media models | VS06، VS10، VS11، VS12، VS14، VS16 | 4 |
| VS18 | D5 | Pipeline execution & common strategy/planning recipes | VS04، VS05، VS06، VS07، VS08، VS09، VS10، VS11، VS12، VS13، VS15، VS16، VS17 | 0 |
| VS19 | D5 | Growth, commercial & customer strategy/planning recipes | VS18 | 0 |
| VS20 | D5 | Digital, communications & channel strategy/planning recipes | VS18 | 0 |
| VS21 | D6 | Full-product acceptance, pilot & release gate | VS00، VS01، VS02، VS03، VS04، VS05، VS06، VS07، VS08، VS09، VS10، VS11، VS12، VS13، VS14، VS15، VS16، VS17، VS18، VS19، VS20 | 0 |

VS14 و VS17/18–20 وابستگی عملیاتی به داده زنده برای اجرای fixture ندارند؛ اگر live C05 مسدود شد، کار توسعه مستقل با داده دستی/fixture در branch پذیرفته‌شده و با ثبت blocker قابل انجام است، نه merge با ادعای C05 کامل. ترتیب فاز/گیت پذیرش کامل محصول تا رفع آن برقرار می‌ماند. VS17 وابسته به قرارداد و کیفیت connector برای مصرف داده است، نه داشتن حساب تجاری در اجرای آزمایش synthetic. هیچ merge یا تایید خودکار با وجود پیش‌نیاز مسدود؛ تغییر ترتیب عملی با ثبت تصمیم مالک.

## ۳. Definition of Done مشترک تمام برش‌ها

1. قبل از کدنویسی scope VS و بندهای دقیق اسناد مالک، method_id/version، dataset/artifact schema، release_gate، وابستگی و fixture در شرح همان PR ثبت شود. از قرارداد موجود استفاده؛ اگر زیرکلید/variant/semantic gate ناقص است همان‌جا با دلیل و backward/migration strategy تکمیل شود؛ بدون schema آزاد یا API/method موازی. بررسی مجوز توسعه و lock گروه موردنیاز قبل از استفاده؛ مدل AI/وزن و provider فقط با مجوز و benchmark لازم.
2. پیاده‌سازی عمودی: یک registry و یک DB؛ Django/DRF، محاسبه علمی server-side، React/TS، مسیر کاربر و UX فارسی/RTL و انگلیسی طبق UX، فرم فقط پیش‌شرط لازم، واضح بودن method/version/حدود و provenance. داده واقعی و synthetic جدا، no observed without evidence؛ هیچ external write/auto decision، no unsupported recommendation. fixture/dataset/schema و source/result version trace، state run جدا از analysis و approval.
3. پذیرش هر method: حداقل اجرای معتبر با dataset مصنوعی کامل یا ورودی مرجع، missing، invalid، edge/negative، comparison/parity و independent oracle مطابق نوع روش؛ مدل پیشرفته با fit/holdout/diagnostics/baseline واقعی و شرط applicability. **fixture نیازمند داده جای fixture fit مثبت نیست.** هر variant یا قابلیت جزئی مصوب در owner spec با آزمون اختصاصی پوشش داده شود. تمام template/راهنما/نمونه synthetic واقعاً قابل اجرا در روش active؛ report از snapshot مشترک و ۴ فرمت برای artifact سازمانی؛ scratch طبق قرارداد موقت. استراتژی/برنامه/PO برای هر ID مستقل fixture positive و required-missing/invalid و trace. عدم کفایت داده واقعی به‌صورت conditional/needs_data، نه failure ساختگی.
4. API+DB integration با migrations و permission/tenant isolation، validation و immutable snapshot، failure/retry/idempotency/rollback برای مسیر مربوط؛ frontend keyboard/responsive/RTL و E2E واقعی از ورود/انتخاب تا نتیجه/ذخیره/گزارش/approval حسب مسیر. برای هر قابلیت حداقل سناریوی مثبت و حالت خطا، نه mock صرف یا screenshot. هیچ UI به method planned یا مسیر mock برچسب ready نزند.
5. PR evidence: commit SHA، نسخه lock/گروه و interpreter، schema/method/fixture version، commands و exit code/log، تعداد واقعی PASS/FAIL/SKIP/NOT_RUN، tests E2E و visual/report QA حسب scope، evidence_refs و محدودیت علمی، coverage الزامات، diff scope و blockers. static/schema pass ≠ runtime/fit pass؛ synthetic ≠ validation بازار. ابتدا tests local یا منابع مجاز، workflow manual-only، no paid CI بدون اجازه. تست ناقص/ردشده release gate را باز نمی‌کند. قبل از merge: review بندبه‌بند، رفع نقص در همان PR، تکرار آزمون مرتبط و ثبت وضعیت.
6. وضعیت برش PLANNED/IN_PROGRESS/BLOCKED/FAILED/ACCEPTED؛ در این سند همه PLANNED به‌جز VS00 BLOCKED سابق. در PRهای اجرا، وضعیت method readiness فقط با evidence؛ variantهای مشروط، علت و fallback صریح. status عمومی tool از actual registry و پوشش مشتق شود؛ برنامه‌ای که نیازمند ابزار unavailable است draft/partial. خروجی مورد انتظار در جدول‌ها نمونه طراحی است، نه گزارش تست اجراشده.

## ۴. قرارداد مستقل هر برش (PR scope + delivery + acceptance)

### VS00 — Stack lock & compatibility (D0)

- پیش‌نیاز: —.
- قرارداد method: —.
- تحویل قابل استفاده: محیط توسعه بازتولیدپذیر برای backend/frontend و PostgreSQL، با گزارش واقعی resolver و آزمون.
- محدوده PR: همان manifestهای مصوب، uv.lock و pnpm-lock.yaml، runtime و Linux x86_64 هدف، verify_stack.py، checker و ۲۲ oracle، PostgreSQL 17 و psycopg اتصال/تراکنش واقعی، lock و license record. اصلاح نسخه فقط بر مبنای conflict/security evidence، حفظ قابلیت علمی. گروه‌های optional و Meridian تنها برای ترکیب موردنیاز در برش مالک lock شوند؛ full profile برای ممیزی ترکیب، نه نصب اجباری مدل‌های سنگین در core.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): اجرای موفق core resolve و frozen install از checkout تمیز؛ ثبت hash و commit، pip check، API/import smoke، checker استاندارد schema/fixture، oracle 22/22، اتصال و rollback تراکنش PG، بررسی مجوز توسعه. نسخه‌های نصب‌شده با lock برابر. شکست نسخه/شبکه → BLOCKED یا FAIL واقعی؛ هیچ lock دست‌ساز یا تغییر خودکار نسخه.
- Gate/محدودیت: فعلاً BLOCKED: محیط پیشین registry و Python 3.12 هدف نداشت. اجرای D0 روی محیط مجاز؛ CI manual-only و بدون dispatch پولی خودکار.

### VS01 — Foundation — حساب، کسب‌وکار و اجرای مشترک (D1)

- پیش‌نیاز: VS00.
- قرارداد method: —.
- تحویل قابل استفاده: کاربر وارد میزکار می‌شود، کسب‌وکار می‌سازد، داده/شاهد دستی ثبت می‌کند و تاریخچه مجاز همان شرکت را می‌بیند.
- محدوده PR: Django/DRF + React/TS، migrations، User/Workspace/Membership/CompanyProfile، Evidence/Dataset/MetricDefinition/Observation/Goal/Hypothesis، version و snapshots، Run/Job/Artifact/Decision/Action/Outcome، registry ۷۲ method planned، permission/CSRF، کاتالوگ و صفحات مشترک question/input/result، status/finding/limitations، draft/resume/history، preflight و job DB؛ scratch contract و API، نه محاسبه QT جعلی. تصمیم و تایید انسانی جدا؛ business profile optional برای scratch. لینک‌ها و معماری RTL/responsive/keyboard.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): از UI ورود، انتخاب/ساخت دو workspace، ثبت شاهد/داده معتبر، بازیابی نسخه، نمایش تاریخچه و بازگشت به میزکار؛ تست cross-tenant FK و API/export/ref، CSRF، invalid input، idempotency 409، transaction failure/retry/lease، ثبت immutable، no hidden scratch persistence، deny-by-default. تمام ۲۹ full و ۱۵ QT با وضعیت واقعی planned تا فعال‌سازی مالک؛ stub نتیجه واقعی نیست.
- Gate/محدودیت: D0 PASS؛ migration/DB و امنیت پایه در همین PR؛ اجرای ابزار یا recipe خارج از scope.

### VS02 — Data intake, executive exports & company profile (D1)

- پیش‌نیاز: VS01.
- قرارداد method: —.
- مالک تحویل F/C: C-01، C-02، C-10.
- تحویل قابل استفاده: ورود داده از Excel/CSV و فرم، آغاز پروفایل از وب‌سایت/سند با بازبینی، و دانلود گزارش مدیریتی نسخه‌دار از داده مجاز.
- محدوده PR: قالب/راهنما/مثال C01 از method schema، preview/mapping/validation/error report/Dataset immutable، DEMO isolation؛ ReportViewModel مشترک و PDF/DOCX/XLSX/PPTX، export job/private download؛ intake C10 URL عمومی منتخب و فایل مجاز، source anchors، parser/preview/review/apply و SSRF/injection protection. مشترک برای همه روش‌ها؛ هر برش بعدی template، filled demo و report خود را از همین زیرساخت اضافه می‌کند، نه renderer دوم.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): قالب خالی و fixture آزمایشی با ستون فارسی، خطاهای ردیف، missing/zero، macro/formula/zip rejection، demo isolation، checksum و same workspace. یک ReportViewModel آزمایشی صریح با داده 70/100 در هر چهار فرمت، بررسی مقادیر و provenance برابر، QA بصری RTL/PPTX و editable DOCX/XLSX، permission revoke و snapshot قدیمی. URL خصوصی/redirect/DNS rebinding و دستور داخل سند رد؛ فیلد بدون شاهد pending و apply فقط بعد از تایید/نسخه. در نبود ابزار active، preview/report آزمایشی یا داده/پروفایل مجاز؛ هیچ تحلیل آزمایشی به KPI واقعی تبدیل نشود.
- Gate/محدودیت: قفل و تست parser/renderer واقعی و مجوز؛ PDF renderer آزموده، چهار فرمت اجباری در محصول نهایی. C01/C02 زیرساخت اینجا، پذیرش تک‌تک روش‌ها در برش مالک.

### VS03 — Daily Workbench — Quick Tools, Knowledge & personalization (D2)

- پیش‌نیاز: VS01، VS02.
- قرارداد method: QT01، QT02، QT03، QT04، QT05، QT06، QT07، QT08، QT09، QT10، QT11، QT14، QT15.
- Knowledge: KN01–KN36 (تمام ۳۶ مدخل).
- مالک تحویل F/C: F-01، F-02، F-04، C-09.
- تحویل قابل استفاده: محاسبه سریع بدون ساخت شرکت، مرجع دانش فارسی/انگلیسی، علاقه‌مندی، recent/frequent و قالب شخصی؛ نتیجه در همان صفحه، ذخیره صریح در شرکت و گزارش مجاز.
- محدوده PR: ۱۳ QT اولیه، ۳۶ KN با تعریف/فرمول/مثال/محدودیت/مرجع/نسخه و پیوند؛ QT12/13 کارت planned تا VS08/10؛ scratch محاسبه قطعی در server و بدون refs/پایداری، save مجاز و محاسبه مجدد، personal preferences scoped و allowlist. سرچ alias و acronym ambiguity؛ progressive disclosure. KN مربوط به روش غیرفعال فقط مرجع، نه وعده اجرا. پروتکل F03 وظایف واقعی آغاز می‌شود (نمونه مدیران/دفترچه ۱۰ روز)، F05 pilot formative در صورت دسترسی؛ نتیجه و تصمیم نهایی VS21.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): اجرای UI همه ۱۳ QT و oracle متناظر؛ CAC=100، ROAS=3×، سربه‌سر 100، LTV=70، Payback پایان دوره 3، حجم نمونه 278/556؛ edge صفر/ارز/قیف/افق و manual ROMI conditional. search ROMI/CAC فارسی/انگلیسی و CPM دو معنی، منبع/نسخه/CTA صحیح. pin/reorder/delete، شمار رخداد واقعی، presets بدون داده شرکت؛ scratch بدون workspace و DB/log persistence؛ viewer فقط دستی، owner/editor ذخیره صریح و export snapshot. عدم فعال‌سازی full tool از QT.
- Gate/محدودیت: پذیرش scientific/UX مستقل هر QT و review هر ۳۶ KN؛ F03/F05 اگر داده انسانی ندارند NOT_RUN، نه رتبه یا زمان ساختگی.

### VS04 — تشخیص مسئله تا انتخاب استراتژیک (D3)

- پیش‌نیاز: VS01، VS02، VS03.
- قرارداد method: S01.diagnose، S03.choice.
- تحویل قابل استفاده: مدیر هدف و عملکرد را تعریف می‌کند، مسئله و فرضیه‌ها را بررسی، گزینه‌های استراتژی را مقایسه و انتخاب مستند را ثبت می‌کند.
- محدوده PR: S01 مسئله/شکاف/درخت علل و فرضیه رقیب، S03 هدف/قید/گزینه و انتخاب انسانی؛ ورودی manual یا refs معتبر، قالب و نمونه هر method، گزارش تصمیم و نسخه؛ تولید draft با AI فقط در adapter مجاز و بدون محاسبه/شاهد ساختگی. پایه StrategyResult و تصمیم، نه ST01 کامل.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): fixture gap=−30، علت بدون شاهد hypothesis، شواهد مخالف قابل دیدن؛ بودجه 100، گزینه 120 رد و 80 feasible، انتخاب هنوز draft تا owner approval. فرم question→result→decision→history→export؛ missing evidence، invalid ref، تغییر snapshot و عدم approval خودکار.
- Gate/محدودیت: گیت روش پایه و قالب/نمونه/گزارش؛ MCDA پیشرفته VS09 و recipe جامع VS18، نبود آن‌ها به‌عنوان پوشش کامل استراتژی پنهان نشود.

### VS05 — تحقیق، بخش‌بندی و جایگاه‌سازی اولیه (D3)

- پیش‌نیاز: VS01، VS02، VS03، VS04.
- قرارداد method: M01.research، M05.segments، M05.clustering، M06.positioning، M06.perceptual_map.
- تحویل قابل استفاده: طراحی تحقیق، جمع‌آوری پاسخ، تحلیل بخش‌های بازار، نقشه ادراکی معتبر و تدوین جایگاه پیشنهادی.
- محدوده PR: M01 SurveyJS Form/Creator مطابق مجوز توسعه، نسخه پرسشنامه/response، رضایت/نمونه/پیش‌آزمون، SRS و تحلیل توصیفی؛ M05 قواعد/RFM، KMeans و Gower+HDBSCAN مناسب داده؛ M06 STP، PoP/PoD و proof، PCA/MDS/CA/direct axes طبق نوع داده، گزینه جایگاه draft. قرارداد PO01/09 در این مرحله به‌صورت قابلیت پایه، پذیرش کامل PO در VS15. تحلیل survey پیچیده و choice/preference پیشرفته VS15.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): n=385 در SRS، opt-in بدون MOE احتمالی، پرسشنامه و ورود داده واقعی synthetic، RFM dedup و دو خوشه ثابت مستقل از نام label؛ mixed distance/stability و نقص داده؛ ماتریس نامتقارن رد، stress/fit/align و table fallback؛ fastest بدون proof hypothesis، هیچ map یا segment ساختگی. UI/fixture/template/report، review انسانی.
- Gate/محدودیت: core و مجوز SurveyJS؛ اگر Creator نیازمند مجوز است، بخش مشمول مجوز BLOCKED تا اخذ یا جایگزین مجاز مصوب. نسخه روش پیشرفته تا gate خودش active نشود.

### VS06 — اقتصاد مشتری، قیف و KPI پایه (D3)

- پیش‌نیاز: VS01، VS02، VS03.
- قرارداد method: B01.unit_economics، B03.funnel، B05.kpi.
- تحویل قابل استفاده: مدیر داده‌های فروش/هزینه/قیف و شاخص را وارد می‌کند و اقتصاد واحد، تبدیل، نگهداشت و انحراف KPI را با سابقه و گزارش می‌بیند.
- محدوده PR: B01 CAC paid/blended، margin، LTV مشاهده‌ای/سناریو، ROMI افزایشی؛ reuse QT methods؛ B03 dedup events، cohort funnel/retention/churn و period، B05 metric registry/target و دوره/دانه‌بندی/quality/report. B05 در MVP پایه؛ تکمیل تحلیل چندمنبع/رسانه و trend با VS11/14/12؛ CLV و churn پیش‌بینی VS17.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): margin=4000 و CAC=100؛ ROMI فقط با مبنای اثر و conditional manual؛ funnel 100→40→20، churn 10%، KPI 70/100 gap−30؛ عدم جمع کاربران یکتا یا قیف غیرتودرتو، unknown vs zero، scope/currency mismatch و duplicate event؛ drill-down evidence، template/demo/report و parity QT/full.
- Gate/محدودیت: قواعد Decimal و cohort/metric definition، scientific fixture؛ full-tool status فقط scope آماده، نه پیش‌بینی CLV/churn یا connector.

### VS07 — برنامه یکپارچه و واردسازی استراتژی قبلی (D3)

- پیش‌نیاز: VS02، VS04، VS05، VS06.
- قرارداد method: E01.plan، E01.schedule.
- مالک تحویل F/C: C-12.
- تحویل قابل استفاده: از تصمیم یا سند استراتژی قبلی یک PlanResult قابل بازبینی شامل کار، بودجه، زمان‌بندی، مسئول و KPI ساخته و با مجوز تصویب می‌شود.
- محدوده PR: E01 WBS، baseline/commitment/actual/cash/forecast، dependency DAG، calendar/CPM، RCPSP/CP-SAT با محدودیت منابع، EAC/کنترل تغییر و EVM مشروط طبق PL. C12 reuse intake VS02: سند strategy/plan → mapping source/target/KPI/actions/budget → draft S03/E01 → review/approval داخلی، version diff. PL01–04 draft scaffold فقط؛ پذیرش recipe کامل VS18. نمایش برنامه، تقویم، بودجه و export چهارفرمت.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): بودجه 100 و کار 60+50 violation=10؛ مسیر بحرانی 2+3=5 با تقویم، تشخیص cycle، resource overload و solver infeasible، independent constraint recheck، baseline immutable و rebaseline مجاز، عدم double count؛ سند approved بیرونی همچنان draft، تعارض بودجه/ارز/تاریخ و field بدون منبع review؛ انجام کامل مسیر UI تا گزارش. هیچ اقدام بیرونی خودکار.
- Gate/محدودیت: گروه optimization و API CP-SAT واقعی قبل از method activation؛ D3 milestone MVP فقط بعد از gate VS03–07 و ۸ ابزار در دامنه پایه مصوب، نه محصول نهایی.

### VS08 — Market intelligence, TAM, qualitative & PMF (D4)

- پیش‌نیاز: VS02، VS05، VS06.
- قرارداد method: M02.market_size، M03.competitors، M04.qualitative، M07.pmf، QT12.
- تحویل قابل استفاده: مدیر اندازه بازار، گزینه‌های رقابتی، نیازها و شواهد تناسب محصول را به‌صورت مستقل تحلیل می‌کند.
- محدوده PR: M02 bottom-up TAM/SAM/SOM و top-down cross-check/فرض ظرفیت، QT12؛ M03 ماتریس قیمت/ویژگی/شواهد تاریخ‌دار، PESTEL/Porter؛ M04 coding و counter-evidence، insight/needs/motivations؛ M07 cohort/repeat/feedback triangulation و time-to-event با lifelines در صورت داده، reuse B03. NLP خودکار در VS15.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): TAM 1000 و SAM 600 و SOM 100 در مثال، QT12=200000؛ ظرفیت/market definition و missing rejection؛ رقیب قیمت نامعلوم null؛ هر theme شاهد و review، متن نمونه qualitative نه prevalence؛ retention 4/10=40% نه اثبات PMF؛ censoring و گروه مقایسه در روش time-to-event. UI/guide/demo/export.
- Gate/محدودیت: lifelines/ML فقط اگر روش انتخابی نیاز دارد با lock؛ داده واقعی و شواهد ادعا، بدون ساخت سهم بازار.

### VS09 — مدل کسب‌وکار، اولویت، سناریو و GTM (D4)

- پیش‌نیاز: VS04، VS06، VS08.
- قرارداد method: S02.business_model، S04.weighted_score، S04.mcda، S05.scenarios، S05.simulation، S06.gtm.
- تحویل قابل استفاده: مدیر بوم مدل کسب‌وکار و مزیت، اولویت فرصت‌ها، سناریو و مسیر رشد/ورود به بازار را با قیود واقعی مقایسه می‌کند.
- محدوده PR: VRIO/BMC و evidence rubric، weighted sum و TOPSIS/VIKOR/PROMETHEE متناسب با مسئله، sensitivity؛ سناریو low/base/high و Monte Carlo/QMC/SALib مشروط، وابستگی پارامتر و uncertainty؛ GTM/Ansoff/ICP/offer/route-to-market و ظرفیت/اقتصاد، ارجاع S03/E01. روش‌های مالک کامل، نه recipe ST هنوز.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): rank .56/.60 و تغییر وزن .68/.50، hard constraint پیش از رتبه، missing metric no rank؛ سناریو فروش/قیمت 40/50/60 بدون probability جعلی، توزیع/وابستگی نامعتبر منع Sobol؛ GTM هزینه 150 در سقف 100 رد، CAC unknown conditional؛ fixture پایه و advanced benchmark، گزارش مقایسه و sensitivity.
- Gate/محدودیت: گروه optimization شامل PyMCDM/SALib و شرایط هر روش؛ عدم حل MCDA/شبیه‌سازی با placeholder.

### VS10 — قیمت، آزمایش و تخصیص سرمایه پایه (D4)

- پیش‌نیاز: VS02، VS06، VS09.
- قرارداد method: B02.price_scenario، B04.experiment، B06.portfolio، B06.optimization، QT13.
- تحویل قابل استفاده: مقایسه قیمت/هزینه، طراحی و تحلیل آزمایش، اولویت سرمایه‌گذاری و بهینه‌سازی با قید؛ QT13 حجم نمونه آزمایش.
- محدوده PR: B02 break-even/price scenarios و سناریوی تقاضا، B04 protocol/RCT دوگروهی/binary/continuous و power، B06 feasible comparison/LP/MILP/constraint recheck و روش گسسته/قطعه‌ای فقط داده معتبر و حسب نیاز OR-Tools؛ QT13 مستقل، KN19 link active. روش پیشرفته قیمت/forecast و causal در VS16؛ response curve به artifact VS17 وابسته است، نه فرض بازده ساختگی.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): سربه‌سر 100، سود سناریو delta=500، QT13=681 هر گروه و power>=.8 با API پین‌شده؛ risk difference=.10 و CI، بدون طرح معتبر causal_claim=false، آزمون پیوسته Welch و guardrails؛ max 3x+2y→x=y=2,obj=10، infeasible و مستقل recheck؛ بدون داده بازده، no optimum. UI/Excel fixture/report.
- Gate/محدودیت: Statsmodels/SciPy و گروه optimization در صورت نیاز؛ تحلیل علت و forecast کامل به gate VS16، مدل پاسخ رسانه VS17.

### VS11 — کمپین، رسانه، فروش و چرخه مشتری (D4)

- پیش‌نیاز: VS04، VS06، VS07، VS08، VS09، VS10.
- قرارداد method: E02.campaign، E03.channel_plan، E04.lifecycle.
- تحویل قابل استفاده: بریف کمپین، برنامه کانال/بودجه، فروش، SLA و نگهداشت مشتری با معیار سنجش و تایید مدیر.
- محدوده PR: E02 IMC/creative brief/message/proof و content/test plan؛ E03 نقش کانال، performance descriptive، تخصیص محدود و stop rules، شاخص رسانه B05، SEO/paid/social planning با داده دستی مجاز؛ E04 RFM/rules/SLA/handoff/capacity/consent و lifecycle. B05 گزارش KPI عملیاتی و segmentation داده معتبر؛ هیچ ارسال یا تغییر تبلیغ/CRM. MMM و lead scoring پیشرفته VS17.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): claim بدون proof publication_ready=false، budget 100 و کانال 60+50 رد، نبود response → test_plan نه ROI، stop rule predeclared؛ opt-out/unknown no outreach و backlog 25−20=5؛ KPI definitions، attributed vs incremental، fractional credit جدا از مشتری؛ UX و گزارش هر روش و reuse E01/B05.
- Gate/محدودیت: داده دستی و scope معتبر کافی برای برنامه؛ اتصال‌های داده VS14 و مدل‌های پیشرفته VS17، no auto-publication.

### VS12 — عملیات، منابع، ذی‌نفعان و حافظه سازمانی (D4)

- پیش‌نیاز: VS06، VS07، VS11.
- قرارداد method: E05.operations، E06.responsibility، E07.stakeholders، E08.review، E06.assignment، E08.monitor، E08.lesson.
- مالک تحویل F/C: C-04.
- تحویل قابل استفاده: مدیر فرایندها، تقسیم مسئولیت، ظرفیت، ریسک و نتایج اقدامات را کنترل و درس‌آموخته‌های شرکت را ثبت و جست‌وجو می‌کند.
- محدوده PR: E05 BPMN/process map و requirements/security matrix؛ E06 RACI/DRI و skill/capacity/assignment CP-SAT؛ E07 منافع اظهارشده، مذاکره/گزینه/ارجاع؛ E08 PDCA، KPI trend/change point، outcome/review و LessonRecord نسخه‌دار با search/tag/review/supersede و reuse زمینه‌مند. Process mining مشترک VS13؛ E08 و B05 trend با داده معتبر.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): سیستم بدون permission blocked، دو A در RACI رد، overload=2، assignment feasible/infeasible و capacity recheck، منفعت نامعلوم unknown؛ review gap−20 و علت hypothesis، change point بدون causal claim، no-data fallback؛ lesson شکست/موفقیت با refs و review/supersede، جست‌وجوی فارسی، isolation/revoke، reuse فقط با تایید. گزارش و demo برای هر method.
- Gate/محدودیت: OR-Tools و ruptures طبق lock گروه واقعی؛ حریم خصوصی و no auto employment decision. درس‌آموخته‌ها جدای KN عمومی.

### VS13 — برند، سفر مشتری، شبکه روابط و Process Mining (D4)

- پیش‌نیاز: VS05، VS06، VS08، VS11، VS12.
- قرارداد method: M08.brand_audit، M09.journey، M09.network، M09.process، E05.process_mining.
- مالک تحویل F/C: C-11.
- تحویل قابل استفاده: ممیزی هویت برند، مسیر مشتری، شبکه معرفی و کشف/تطبیق فرایند از رویدادهای مجاز، با گزارش ساختار و محدودیت.
- محدوده PR: M08 identity audit بدون ادعای ادراک، M09 journey و transition/Markov در صورت داده، SNA node/edge و graph boundary، centrality/community/cascade سناریویی؛ M09.process و E05.process_mining reuse PM4Py discovery/conformance و event schema، هیچ موتور/گراف DB موازی. مطالعه برند پیشرفته و MA/DBA در VS15؛ SNA از روابط دستی/CRM مجاز نه Facebook/Meta.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): journey A→B با event duplicate حذف، sequence و timestamp/coverage؛ graph A-B-C degree 1/2/1، density 2/3، betweenness B=1؛ directed/isolates/weights، Louvain stability، p=0/p=1 سناریو، عدم ادعای influence علّی؛ event log ناقص فقط map فرضی، discovery/conformance fixture قابل تکرار و تفاوت مدل مرجع؛ identity بدون responses → perception gap null. UI/graph/table/export و permission.
- Gate/محدودیت: PM4Py license و lock مجاز پیش از فعال‌سازی؛ اگر مجوز/داده لازم در دسترس نیست وضعیت method BLOCKED/needs_data، نه حذف از دامنه نهایی.

### VS14 — چهار اتصال داده و کیفیت گزارش چندمنبعی (D4)

- پیش‌نیاز: VS02، VS06، VS11، VS12.
- قرارداد method: —.
- مالک تحویل F/C: C-05.
- اتصال‌ها: GA4، GOOGLE_ADS، SEARCH_CONSOLE، CRM.
- تحویل قابل استفاده: کاربر چهار منبع داده مجاز را متصل، بازه و گزارش را انتخاب، sync و پوشش را کنترل و snapshot معتبر را در KPI/تحلیل استفاده می‌کند.
- محدوده PR: فقط GA4 Data API، Google Ads reporting/GAQL، Search Console Search Analytics و CRM read-only با vendor مصوب. Connection/SyncRun، secret و OAuth/least privilege، account picker، pagination/quota/retry/partial/late data، versioned normalization و reconciliation، timezone/grain/attribution، metric source lineage، B05 گزارش کامل چندمنبعی، CRM history/archived و pseudonymization. داده سایر کانال‌ها فقط دستی/CSV/XLSX. هیچ تغییر بودجه، کمپین، lead یا داده provider.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): mock هر چهار provider و live sandbox/account مجاز: pagination و repeated cursor، stream interruption، 429/401/403، late data/dedup و re-sync immutable، disconnect/revoke، mismatch و coverage واضح؛ تطبیق با report رسمی همان تعریف و دوره؛ aggregate user join ممنوع، GA4/Ads/CRM conversion جمع نشود، Search Console top-row محدودیت؛ بدون token در log/API/export، isolation. چهار CTA واقعی و خطا/آخرین sync، نه fake connection.
- Gate/محدودیت: انتخاب CRM vendor و credential/accountهای مجاز مالک، نسخه API و scope قبل از live؛ vendor_pending یا عدم دسترسی → BLOCKED_LIVE، این برش تا پذیرش اتصال CRM و سایر سه منبع کامل محسوب نمی‌شود. mock PASS کافی نیست.

### VS15 — Scientific research & full positioning library (D5)

- پیش‌نیاز: VS05، VS08، VS09، VS10، VS11، VS12، VS13.
- قرارداد method: M01.survey_analysis، M04.text_models، M06.preference_map، M06.choice_model، M08.measurement.
- Positioning: PO01، PO02، PO03، PO04، PO05، PO06، PO07، PO08، PO09، PO10، PO11، PO12، PO13، PO14.
- مالک تحویل F/C: C-07.
- تحویل قابل استفاده: مدیر مطالعه برند و بازار را از طراحی و پاسخ تا سنجش ادراک، ترجیح، دسترس‌پذیری ذهنی و گزینه جایگاه اجرا و برای تصمیم/برنامه تحویل می‌دهد.
- محدوده PR: svy/weights/design-aware uncertainty، M04 Qwen/BGE embedding و BERTopic conditional با benchmark انسانی فارسی، BCM/laddering/means-end و CEP؛ M08 CBBE/awareness/mental availability/DBA/tracking، M06 MDS/PCA/CA reuse VS05، PREFMAP vector/circular ideal/internal PCA و choice Biogeme/WTP؛ تمام PO01–14 با study/positioning artifact و UI. PO11/12 گزینه/آزمون، PO13/14 تغییر/معماری برند و tracking؛ لینک S03/E01 و E02، ST05/PL13 در VS19. هر PO مالک روش اصلی سند حفظ؛ C07 در PO05/10.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): برای هر ۱۴ PO fixture مثبت با داده کامل + no-data/invalid + UI/trace/export. MP=.6، NS=2، MMS فقط با total links، DBA fame/uniqueness جدا، نمونه غیر احتمالی no MOE، موج/پایه و weights سازگار؛ نقشه valid fit/holdout/alignment، ideal (1,2) در hull، gamma<=0 یا extrapolated → no unsupported point؛ conjoint convergence/holdout/WTP coefficient gate؛ semantic benchmark انسانی فارسی، کدگذاری review و theme evidence. perceived/preferred/desired جدا، PO12 آزمون معتبر یا draft، tracking نه علت.
- Gate/محدودیت: گروه‌های survey/nlp/choice و revision مدل مجاز؛ full-text/fit و benchmark لازم مطابق owner spec، optional challenger فقط در صورت توجیه. بدون داده کافی در run نتیجه مشروط، اما روش باید با fixture مناسب واقعاً اجرا و پذیرفته شده باشد.

### VS16 — Pricing research, demand forecast & causal analytics (D5)

- پیش‌نیاز: VS08، VS10، VS15.
- قرارداد method: B02.forecast، B02.PR01، B02.PR02، B02.PR03، B02.PR04، B02.bass، B04.causal.
- مالک تحویل F/C: C-03، C-08.
- تحویل قابل استفاده: مدیر تحقیقات قیمت و پذیرش محصول را با شواهد اجرا می‌کند، قیمت/درآمد/حاشیه سناریویی را مقایسه و اثر آزمایش یا مدل علّی معتبر را ارزیابی می‌کند.
- محدوده PR: B02 PR01 PSM/تقاطع و uncertainty، PR02 GG full-grid/monadic/adaptive bounds و isotonic، PR03 reuse M06.choice_model، PR04 reuse B04 experiment/causal؛ Naive/SeasonalNaive و StatsForecast/Statsmodels طبق سری، intermittent demand، rolling-origin و pricing elasticity فقط identification؛ Bass first adoption p/q/m و bounded fit/forecast vs scenario؛ B04 DoWhy identification/refutation و EconML DML/CATE با assumptions، no automatic price change. S06/B01/E01 consumption از artifact.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): PSM ordered thresholds و تقاطع/band/absent، GG .8/.6/.4 در 100/120/150 → revenue 80/72/60 و CM 16/24/28؛ adaptive unknown bounds؛ conjoint/experiment parity نه duplicate fit؛ forecast constant series و out-of-sample baseline/MAE، sparse/missing/seasonality; Bass N monotone≤m و t_peak≈6.19، early nonidentification→scenario; causal known synthetic effect/overlap/refutation و invalid confounding → false. داده واقعی فقط مشروط به scope؛ fixture کامل، UX curve/table/report.
- Gate/محدودیت: گروه forecast/causal و choice reuse؛ انتخاب method/fit/uncertainty و release شرط علمی، stated intent≠actual demand.

### VS17 — Customer lifetime, churn, lead & media models (D5)

- پیش‌نیاز: VS06، VS10، VS11، VS12، VS14، VS16.
- قرارداد method: B01.clv_model، B03.churn_model، E03.mmm، E04.lead_scoring.
- تحویل قابل استفاده: تحلیل پیش‌بینی ارزش/ریزش مشتری، امتیازدهی شفاف لید و تحلیل اثر و تخصیص رسانه مبتنی بر پاسخ معتبر، بدون اجرای خودکار.
- محدوده PR: B01 PyMC-Marketing CLV خانواده BG/NBD/Pareto/NBD/BG-BB/Shifted BG و Gamma-Gamma با شرط مناسب؛ B03 logistic/CatBoost/lifelines و calibration/temporal validation؛ E04 rules/logistic/CatBoost و fairness/consent؛ E03 Meridian 2.2.1 محیط جدا و PyMC-Marketing model، adstock/saturation، priors/calibration/holdout/posterior diagnostics، budget optimization reuse B06 با response curve معتبر؛ SHAP/Optuna فقط طبق شواهد. B05/B01/E03 consumption، fallback توصیفی/سناریو نه جعل مدل. اتصال live برای اجرای fixture لازم نیست؛ داده مجاز واقعی/فایل جایگزین است.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): synthetic و temporal holdout واقعی هر model family مصوب، no leakage و compare baseline، CLV PPC/convergence/interval/horizon، churn PR-AUC و calibration و censored data، lead consent/fairness و missing features، MMM calibration/identification/diagnostics و response/saturation و independent constraints، isolated Meridian imports/fit؛ insufficient data→conditional/no forecast، no causal ROI from attribution؛ UI diagnostic summary و report.
- Gate/محدودیت: گروه bayesian/ml و Meridian جدا با lock/fit واقعی و مدل مجاز؛ live C05 blocker نباید مانع آزمون fixture دستی این برش شود؛ کامل بودن محصول همچنان نیازمند C05 است.

### VS18 — Pipeline execution & common strategy/planning recipes (D5)

- پیش‌نیاز: VS04، VS05، VS06، VS07، VS08، VS09، VS10، VS11، VS12، VS13، VS15، VS16، VS17.
- قرارداد method: —.
- Strategy: ST01.
- Planning: PL01، PL02، PL03، PL04، PL05، PL06، PL07، PL08، PL09.
- تحویل قابل استفاده: مدیر یک ابزار مستقل، یک حوزه یا مسیر جامع را از سؤال تا انتخاب انسانی، برنامه و مرور اجرا می‌کند؛ استراتژی جامع و ۹ الگوی برنامه مشترک آماده‌اند.
- محدوده PR: runtime PipelineRun/Step و DAG، preview readiness/coverage، skip optional، manual evidence، pause/resume/idempotency/retry/failure، stage D/R/O/C/P/A/V و چرخه بازبینی نسخه بعد؛ catalog recipe schema/version. ST01 و PL01–08 مشترک + PL09 اجرای ST01؛ E01 integrated PlanResult و تمام budget/calendar/measurement/risk constraints. استفاده از ابزارهای کامل در همان registry، نه اجرای اجباری ۲۹ ابزار. draft/import از VS07 reuse.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): single مستقل، domain مرتبط، full relevant subset؛ preview deps، unavailable required blocked/partial و manual evidence به‌عنوان manual، independent branch ادامه، no DAG cycle S03↔E01، snapshot/resume/idempotency و scope؛ ST01 و هر PL01–09 fixture مثبت با داده مجاز، missing stage و approval، PL01 annual/PL02 rolling/PL03 calendar/PL04 cash/PL05 research/PL06 KPI/PL07 capacity/PL08 risk و PL09 one-plan cost IDs؛ خروجی strategy/plan/report چهارفرمت، هیچ هزینه/اقدام دوباره‌شماری.
- Gate/محدودیت: هر owner method موردنیاز ready در registry، optional advanced فقط با preconditions؛ C05 live برای pipeline دستی لازم نیست؛ complete فقط براساس coverage واقعی.

### VS19 — Growth, commercial & customer strategy/planning recipes (D5)

- پیش‌نیاز: VS18.
- قرارداد method: —.
- Strategy: ST02، ST03، ST04، ST05، ST06، ST13، ST14، ST15، ST16، ST17، ST18، ST19، ST20، ST23، ST24، ST26.
- Planning: PL10، PL11، PL12، PL13، PL14، PL21، PL22، PL23، PL24، PL25، PL26، PL27، PL28، PL31، PL32، PL34.
- تحویل قابل استفاده: مسیرهای تخصصی رشد، محصول، برند، قیمت، CRM، فروش، توزیع و تجربه مشتری از شواهد تا استراتژی و برنامه عملیاتی یکپارچه در دسترس‌اند.
- محدوده PR: ST02–06، ST13–20، ST23، ST24، ST26 و PL متناظر (PL=ST+8)؛ growth/GTM/PMF، ST05+PO01–14/PL13، PR/Bass، lifecycle/loyalty/CRO/e-commerce/sales/B2B/omnichannel، referral/SNA، international/localization و CX. هر recipe owner/candidate/stage/evidence rules/metric/constraints طبق بند اختصاصی ST/PL، shared pipeline و plan؛ هیچ full-tool/method دوباره پیاده نشود. داده ecommerce/email/social فقط فایل دستی، no direct sync.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): برای تک‌تک ۱۶ جفت ST/PL، descriptor مستقل و fixture مثبت با داده کافی و negative missing required، stages D/R/O/C/P/A/V معتبر، KPI/stop rules/مالک/بودجه/ظرفیت و approval؛ ST05/PL13 proof/CEP/brand tracking، ST06 قیمت و profit، ST23 شبکه نه causal، ST26 journey؛ نمونه B2B و CRM از اسناد، reverse funnel infeasible در نرخ صفر، plan consolidation no double cost. UI search/preview/coverage و گزارش هر recipe.
- Gate/محدودیت: تطبیق بندبه‌بند ۱۶+۱۶ recipe و evidence ref؛ conditional output مجاز، fake complete ممنوع.

### VS20 — Digital, communications & channel strategy/planning recipes (D5)

- پیش‌نیاز: VS18.
- قرارداد method: —.
- Strategy: ST07، ST08، ST09، ST10، ST11، ST12، ST21، ST22، ST25.
- Planning: PL15، PL16، PL17، PL18، PL19، PL20، PL29، PL30، PL33.
- تحویل قابل استفاده: مسیرهای دیجیتال، social/content، SEO، PPC، creator، بازاریابی محلی، PR و رویداد با برنامه و کنترل عملکرد آماده‌اند.
- محدوده PR: ST07–12، ST21، ST22، ST25 و PL15–20/29/30/33؛ digital/social/community/content/SEO/performance/creator/local/crisis/event؛ E02/E03 و M/B/E01 reuse، attribution/measurement/creative brief/proof/consent، budget و channel roles، Search Console/GA4/Ads فقط در صورت مجوز و snapshot سازگار. social/creator planning مصوب است ولی connector Facebook/Meta و انتشار خودکار نیست.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): هر ۹ جفت ST/PL descriptor و fixture مثبت + required missing/fallback؛ مثال digital+social و SEO+CRM محدود از سند، budget/capacity و KPI baseline vs target vs actual، CTR/ROAS توصیفی نه اثر علّی، evidence و claim review، editorial/calendar و crisis approval، no spend/publish mutations؛ همه UI/preview/coverage و report.
- Gate/محدودیت: ۹+۹ recipe تطبیق با بخش اختصاصی، no fabricated channel data، no unsupported provider.

### VS21 — Full-product acceptance, pilot & release gate (D6)

- پیش‌نیاز: VS00، VS01، VS02، VS03، VS04، VS05، VS06، VS07، VS08، VS09، VS10، VS11، VS12، VS13، VS14، VS15، VS16، VS17، VS18، VS19، VS20.
- قرارداد method: —.
- مالک تحویل F/C: F-03، F-05.
- تحویل قابل استفاده: محصول نهایی کامل و قابل استفاده در شرکت و به‌عنوان میزکار مدیر، با گزارش پذیرش قابل ردیابی و تصمیم انتشار مالک.
- محدوده PR: ممیزی پوشش ۲۹ ابزار کامل، ۷۲ قرارداد method و همه شاخه‌های مصوب owner specs، ۱۵ QT، ۳۶ KN، ۲۶ ST، ۳۴ PL، ۱۴ PO، ۱۱ C و ۵ F؛ همه ۲۴ row/۱۳ artifact و ۲۳۰ fixture پایه و fixtureهای علمی/UI جدید، چهار اتصال live مجاز و چهار فرمت گزارش. F03 شواهد فراوانی/هزینه واقعی وظایف و تصمیم مالک، F05 paired baseline/workbench شامل زمان/خطا/فهم/workload NASA-TLX و intake/export/lesson؛ امنیت، backup/restore/migration، مجوز و SBOM، performance/RTL/a11y، اصلاح failure در PR مالک یا fix محدود ردیابی‌شده، نه تغییر دامنه.
- معیار پذیرش اختصاصی (علاوه بر DoD مشترک): اجرای suite کامل و E2E واقعی روی commit/lock/schema version، pilot service/retail (B2B در صورت دسترسی) طبق اسناد، هدف طراحی ۸۰٪ success و ≥۲۰٪ کاهش زمان paired Quick/Knowledge و zero critical، بدون افت صحت/فهم؛ داده کم→inconclusive، نه PASS. تمام قابلیت‌های مصوب مسیر اجرای واقعی و fixture کامل داشته باشند؛ run needs_data صحیح≠عدم پیاده‌سازی. replay snapshot و cross-tenant/no secret leak، چهار connector evidence، QA هر چهار format، review human approvals و license release. مالک تایید نهایی پس از مشاهده شواهد؛ هیچ ادعای علمی فراتر از داده.
- Gate/محدودیت: عدم دسترسی مدیر/CRM/vendor/credential/license/مدل یا failure هر requirement → release NOT_READY/BLOCKED با علت، مالک و اقدام باقی‌مانده؛ فقط تصمیم صریح مالک می‌تواند scope نهایی را تغییر دهد.

## ۵. ماتریس پوشش صریح (منبع کنترل scope)

### ۵.۱. تمام ۷۲ قرارداد روش و ۲۹ ابزار

جدول مالک هر ابزار: ستون آخر آخرین برش دارای قرارداد method آن ابزار است؛ پذیرش کامل وابسته به تمام الزامات owner spec، نه صرف این شماره. F/C و recipeهای وابسته ممکن است در برش بعد تکمیل شوند.

| ابزار | تحویل روش پایه | همه برش‌های method/QT | آخرین برش method |
|---|---|---|---|
| S01 | VS04 | VS04 | VS04 |
| S02 | VS09 | VS09 | VS09 |
| S03 | VS04 | VS04 | VS04 |
| S04 | VS09 | VS09 | VS09 |
| S05 | VS09 | VS09 | VS09 |
| S06 | VS09 | VS09 | VS09 |
| M01 | VS05 | VS03، VS05، VS15 | VS15 |
| M02 | VS08 | VS08 | VS08 |
| M03 | VS08 | VS08 | VS08 |
| M04 | VS08 | VS08، VS15 | VS15 |
| M05 | VS05 | VS05 | VS05 |
| M06 | VS05 | VS05، VS15 | VS15 |
| M07 | VS08 | VS08 | VS08 |
| M08 | VS13 | VS13، VS15 | VS15 |
| M09 | VS13 | VS13 | VS13 |
| B01 | VS06 | VS03، VS06، VS17 | VS17 |
| B02 | VS10 | VS03، VS10، VS16 | VS16 |
| B03 | VS06 | VS03، VS06، VS17 | VS17 |
| B04 | VS10 | VS10، VS16 | VS16 |
| B05 | VS06 | VS03، VS06 | VS06 |
| B06 | VS10 | VS10 | VS10 |
| E01 | VS07 | VS07 | VS07 |
| E02 | VS11 | VS11 | VS11 |
| E03 | VS11 | VS11، VS17 | VS17 |
| E04 | VS11 | VS11، VS17 | VS17 |
| E05 | VS12 | VS12، VS13 | VS13 |
| E06 | VS12 | VS12 | VS12 |
| E07 | VS12 | VS12 | VS12 |
| E08 | VS12 | VS12 | VS12 |

نگاشت دقیق method_id به PR (هر شناسه فقط یک مالک پیاده‌سازی دارد؛ مصرف مجدد در برش‌های دیگر ممنوع نیست اما implementation تکراری ممنوع است):

| PR | method_idهای مالک | تعداد |
|---|---|---:|
| VS03 | QT01، QT02، QT03، QT04، QT05، QT06، QT07، QT08، QT09، QT10، QT11، QT14، QT15 | 13 |
| VS04 | S01.diagnose، S03.choice | 2 |
| VS05 | M01.research، M05.segments، M05.clustering، M06.positioning، M06.perceptual_map | 5 |
| VS06 | B01.unit_economics، B03.funnel، B05.kpi | 3 |
| VS07 | E01.plan، E01.schedule | 2 |
| VS08 | M02.market_size، M03.competitors، M04.qualitative، M07.pmf، QT12 | 5 |
| VS09 | S02.business_model، S04.weighted_score، S04.mcda، S05.scenarios، S05.simulation، S06.gtm | 6 |
| VS10 | B02.price_scenario، B04.experiment، B06.portfolio، B06.optimization، QT13 | 5 |
| VS11 | E02.campaign، E03.channel_plan، E04.lifecycle | 3 |
| VS12 | E05.operations، E06.responsibility، E07.stakeholders، E08.review، E06.assignment، E08.monitor، E08.lesson | 7 |
| VS13 | M08.brand_audit، M09.journey، M09.network، M09.process، E05.process_mining | 5 |
| VS15 | M01.survey_analysis، M04.text_models، M06.preference_map، M06.choice_model، M08.measurement | 5 |
| VS16 | B02.forecast، B02.PR01، B02.PR02، B02.PR03، B02.PR04، B02.bass، B04.causal | 7 |
| VS17 | B01.clv_model، B03.churn_model، E03.mmm، E04.lead_scoring | 4 |
| مجموع | ۲۹ پایه + ۲۸ پیشرفته + ۱۵ QT | ۷۲ |

### ۵.۲. همه ۷۴ قابلیت ST/PL/PO و ۳۶ مدخل KN

| PR | کتابخانه | شناسه‌های مالک پذیرش کامل | تعداد |
|---|---|---|---:|
| VS03 | KN | KN01، KN02، KN03، KN04، KN05، KN06، KN07، KN08، KN09، KN10، KN11، KN12، KN13، KN14، KN15، KN16، KN17، KN18، KN19، KN20، KN21، KN22، KN23، KN24، KN25، KN26، KN27، KN28، KN29، KN30، KN31، KN32، KN33، KN34، KN35، KN36 | 36 |
| VS15 | PO | PO01، PO02، PO03، PO04، PO05، PO06، PO07، PO08، PO09، PO10، PO11، PO12، PO13، PO14 | 14 |
| VS18 | ST | ST01 | 1 |
| VS18 | PL | PL01، PL02، PL03، PL04، PL05، PL06، PL07، PL08، PL09 | 9 |
| VS19 | ST | ST02، ST03، ST04، ST05، ST06، ST13، ST14، ST15، ST16، ST17، ST18، ST19، ST20، ST23، ST24، ST26 | 16 |
| VS19 | PL | PL10، PL11، PL12، PL13، PL14، PL21، PL22، PL23، PL24، PL25، PL26، PL27، PL28، PL31، PL32، PL34 | 16 |
| VS20 | ST | ST07، ST08، ST09، ST10، ST11، ST12، ST21، ST22، ST25 | 9 |
| VS20 | PL | PL15، PL16، PL17، PL18، PL19، PL20، PL29، PL30، PL33 | 9 |

ST01–26 و PL09–34 یک‌به‌یک با PL=ST+8، ۸ PL مشترک جدا؛ PO01–14 همگی VS15، استفاده از draft در VS05 یا VS07 مالکیت پذیرش کامل را تغییر نمی‌دهد. هر شناسه با بند اختصاصی سند و مالک اصلی method همان سند اجرا/تست می‌شود. هیچ recipe صرف کپی نام یا کاتالوگ کامل محسوب نمی‌شود.

### ۵.۳. همه تکمیل‌های Workbench/Competitive و اتصال‌ها

| شناسه | برش مالک پذیرش | برش‌های مشارکت/consumption |
|---|---|---|
| F-01 | VS03 | VS08/10 برای QT12/13، همه full tools reuse |
| F-02 | VS03 | VS08/10/15–20 CTA/status/source update |
| F-03 | VS21 | VS03 آغاز diary، VS07 checkpoint، D4/D5 ترتیب با evidence و تصمیم مالک |
| F-04 | VS03 | سایر برش‌ها از همان preferences/history |
| F-05 | VS21 | VS03 formative، VS02 و سایر برش‌ها task evidence، پایلوت نهایی |
| C-01 | VS02 | تمام ۲۹ ابزار و ۷۲ method در PR مالک template/demo/guide کامل و آزموده؛ VS21 ممیزی |
| C-02 | VS02 | همه artifactهای مجاز در PR مالک و ST/PL/PO؛ VS21 parity/visual QA |
| C-03 | VS16 | VS10 B04/B02 پایه، VS15 choice، VS19 ST06/PL14 |
| C-04 | VS12 | VS21 جست‌وجو/reuse/پایلوت، VS18–20 review |
| C-05 | VS14 | VS06/11/12 metric/permission، VS17/20 مصرف، VS21 live gate |
| C-07 | VS15 | VS05 map پایه، VS19 ST05/PL13 |
| C-08 | VS16 | VS08 market size، VS09 GTM، VS19 ST03/PL11 |
| C-09 | VS03 | VS06 B01 parity، VS17 CLV advanced |
| C-10 | VS02 | VS07 reuse intake، VS21 پذیرش UX |
| C-11 | VS13 | VS14 CRM relations مجاز، VS19 referral/CX |
| C-12 | VS07 | VS02 intake مشترک، VS18–20 recipes، VS21 UX |

| اتصال مستقیم | مالک | gate نهایی |
|---|---|---|
| GA4 | VS14 | live read-only property مجاز، reconcile |
| GOOGLE_ADS | VS14 | live read-only account مجاز، GAQL/metric/attribution |
| SEARCH_CONSOLE | VS14 | live read-only property مجاز، coverage/aggregation |
| CRM | VS14 | vendor مصوب + live read-only record/stage history/permission |

C-06 خارج از مصوبه است. هیچ provider پنجم یا Facebook/Meta در دامنه نیست. گزارش PDF/DOCX/XLSX/PPTX در VS02 مشترک و در PR مالک artifact integration و VS21 QA نهایی. scope تمام ۱۲۰ قابلیت بانک شایستگی طبق delegation taxonomy موجود است، نه ۱۲۰ ابزار یا اتوماسیون قضاوت انسانی.

### ۵.۴. ممیزی پوشش فریز

در زمان ثبت سند، نگاشت‌ها با کاتالوگ واقعی commit مبنا کنترل ساختاری شدند:

| مجموعه | تعریف موجود | مالکیت یکتا در نقشه |
|---|---:|---:|
| method | 72 | 72 |
| ST | 26 | 26 |
| PL | 34 | 34 |
| PO | 14 | 14 |
| KN | 36 | 36 |
| F/C | 16 | 16 |
| provider | 4 | 4 |
| full tools | 29 | 29 |
| fixtureهای اولیه | 230 | هر fixture از method مالک (VS21 اجرای مجموعه) |

کنترل شمارشی/شناسه‌ای و DAG برش‌ها موفق است، اما این به معنای audit علمی خط‌به‌خط تمام روش‌ها، اجرای CI، lock dependency یا پذیرش محصول نیست. برای هر fixture موجود، owner از method_id و method version catalog تعیین می‌شود و fixture جدید در همان PR با scope و version مشخص اضافه می‌شود. هر requirement جزئی اسناد مالک در PR مربوط trace شود و در VS21 بازبینی کامل انجام شود.

## ۶. معیار خروج نهایی (نه MVP)

- همه VS00–21 پذیرفته با evidence؛ تمام ۲۹ full tool و ۱۵ QT مسیر مستقل، روش‌ها و variantهای مصوب پیاده و آزموده، تمام ۷۴ recipe/capability و ۳۶ KN واقعی و قابل استفاده در شرایط معتبر؛ نه وضعیت planned بدون تصمیم مالک.
- ۴ connector read-only واقعی (CRM vendor مصوب) و ۴ فرمت گزارش؛ امنیت و مجوز و کیفیت داده/محدودیت‌ها. C01/02 در همه روش‌های فعال؛ C10/12 review و C04 حافظه با evidence.
- تمام fixtureهای ثبت‌شده و تست‌های کامل هر method، API/DB/E2E/QA و fit/validation/benchmark لازم با نتایج واقعی. گیت F03/F05 و پایلوت واقعی طبق پروتکل، شواهد کافی یا وضعیت inconclusive/BLOCKED صریح؛ پذیرش مبتنی بر evidence و تایید انسانی. اگر یک روش فقط در داده کافی قابل اجراست، مثبت علمی با fixture معتبر + رفتار needs_data در شرایط ناقص؛ این با رها کردن implementation فرق دارد.
- هیچ مانع حل‌نشده‌ای در scope مصوب برای اعلام FULL_PRODUCT_READY پذیرفته نیست. وضعیت release و مجوزهای توسعه/تجاری جداگانه ثبت شود. اعلام محصول کامل فقط پس از تایید مالک و تحقق گیت‌ها، نه صرف merge آخرین PR.

**وضعیت فعلی:** FROZEN_DESIGN؛ فقط برنامه/قرارداد ثبت شده. VS00 پیش‌تر به‌علت محیط BLOCKED؛ هیچ VS01–21 اجرا یا پذیرفته نشده. نسخه‌های مستقیم candidate و lock نهایی pending، CRM vendor و داده/افراد پایلوت و مجوزهای لازم همچنان نیازمند ورودی و دسترسی واقعی هستند. سند حاضر مجوز آغاز پیاده‌سازی یا merge PR شماره ۱ نیست؛ برنامه آماده تصمیم مالک است.
