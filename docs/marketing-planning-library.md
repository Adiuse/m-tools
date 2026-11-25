# M-Tools — Marketing Planning Library v1.0
تاریخ ۲۵ نوامبر ۲۰۲۶ | طراحی علمی و عملی برنامه بازاریابی؛ نه نرم‌افزار آماده. مکمل [Strategy Library](marketing-strategy-library.md)، [Scientific Engine](marketing-scientific-engine-specification.md)، [Evidence Review](marketing-29-tools-evidence-review.md)، [Architecture](marketing-system-architecture-v1.md) و [Tool Specifications](marketing-tool-specifications.md).

## ۱. دامنه و تصمیم
Planning Library یک catalog نسخه‌دار از ۳۴ recipe برنامه‌ریزی است: ۸ الگوی افقی (افق زمانی، بودجه، تحقیق، سنجش، منابع و ریسک) + ۲۶ الگوی تخصصی متناظر ST01–ST26. E01 مالک یکپارچه‌سازی همه برنامه‌ها؛ ابزار تخصصی مالک محتوا و فرمول مربوطه. ابزار سی‌ام، موتور پنجم، database، agent یا سرویس جدید ایجاد نمی‌شود. PL01/02/03 افق و نمای planning هستند؛ PL09–34 حوزه عمل و PL04–08 خدمات مشترک؛ این‌ها طبقات متقابلاً انحصاری نیستند. یک برنامه سالانه digital+social ممکن است چند recipe داشته باشد، نه چند بودجه مستقل. ۳۴ تعداد طراحی پیشنهادی است نه استاندارد جهانی یا حد نهایی.

Strategy انتخاب بازار/هدف/مسیر و rationale را تعیین می‌کند؛ Planning مسیر را به اقدام قابل انجام، زمان، هزینه، مالک و پذیرش تبدیل می‌کند؛ Execution به انجام واقعی توسط انسان/سامانه مجاز مربوط است؛ Control نتیجه و انحراف را می‌سنجد. هیچ برنامه‌ای تصمیم استراتژیک جدید را بدون S03 تصویب نمی‌کند. اگر strategy موجود نیست، پیش‌نویس/درخواست تصمیم، یا انتخاب Strategy Library؛ برنامه تحقیق اکتشافی می‌تواند با تصمیم مصوب تحقیق مستقل اجرا شود. قالب E01 standalone بدون pipeline کامل مجاز است.

## ۲. چرخه علمی برنامه‌ریزی
از فرایند برنامه‌ریزی مک‌دونالد و پژوهش‌های strategy implementation (P01–04)، برنامه‌ریزی هماهنگ تقاضا/عرضه S&OP (P06/P22)، راهنماهای GAO زمان و هزینه (P07–08) و RCPSP (P09–14/P28) استفاده می‌کنیم. تکمیل به موقع کار، الزاماً موفقیت بازاریابی نیست (P24). مرور ۲۰۲۶ چرخه انتخاب، برنامه و اجرا را به هم متصل می‌بیند (P25).
1. ثبت تصمیم و goal refs، baseline KPI و افق، واحد مالی/تقویم و سقف؛ مشخص کردن outcome، output و guardrail. هدف aspirational با forecast و تعهد متفاوت است.
2. ترجمه strategy به deliverable/work package، WBS و معیار پذیرش؛ هر اقدام حداقل یک هدف یا الزام کنترلی مصوب دارد. تقسیم تا سطح قابل برآورد و پاسخگویی؛ ۱۰۰٪ scope در WBS؛ والد summary است و هزینه فرزند را دوباره جمع نمی‌کند.
3. تعیین dependency، مدت/effort مستقل، مالک، مهارت، منبع و availability؛ برآورد bottom-up هزینه مستقیم/مشترک، forecast و cash phasing.
4. تخصیص اولیه طبق قیود سخت و اولویت مستند، CPM برای توالی و CP-SAT در صورت محدودیت منابع واقعی. LP/MILP فقط مدل خطی؛ MMM فقط با evidence gate. نمایش تعارض و گزینه حذف/تعویق/تغییر منابع، نه relax پنهانی.
5. طراحی plan measurement و risk/contingency، review cadence؛ هم‌ترازی با فروش، موجودی، عملیات، حقوق و مالی؛ تایید مدیر/مالک مجاز.
6. baseline مصوب immutable، نسخه اقدام‌ها، ثبت actual و تعهد؛ rolling forecast مستقل از baseline؛ change request و تصمیم جدید در صورت تغییر هدف، scope، منابع یا بودجه. توقف در پایان افق یا تصمیم مصوب. هیچ خرید/انتشار/ارسال/تغییر قیمت خودکار.

## ۳. کاتالوگ
STxx؛ ALL یعنی کاربرد در هر استراتژی مرتبط، نه اجرای همه. ابزارهای فهرست‌شده کاندید مشروط هستند؛ B04 برای طراحی آزمایش در صورت نیاز و اندازه‌گیری اثر فقط پس از داده، B05 برای baseline و review در زمان جدا. همه مسیرها E01 مشترک دارند؛ در جدول مالک تخصصی محتوا نمایش داده می‌شود.

| شناسه | برنامه | ارتباط استراتژی | مالک تخصصی |
|---|---|---|---|
| PL01 | برنامه جامع سالانه بازاریابی | ST01;ALL | E01 |
| PL02 | برنامه فصلی و rolling 90-day | ST01;ALL | E01 |
| PL03 | برنامه ماهانه، هفتگی و تقویم عملیاتی | ST01;ALL | E01 |
| PL04 | برنامه بودجه، منابع مالی و جریان نقد | ST01;ALL | E01 |
| PL05 | برنامه تحقیقات بازار و بینش مشتری | ST01,ST04,ST05,ST07,ST24,ST26 | M01 |
| PL06 | برنامه اندازه‌گیری، KPI، آزمایش و گزارش | ST01;ALL | B05 |
| PL07 | برنامه تیم، ظرفیت، پیمانکار و عملیات | ST01;ALL | E06 |
| PL08 | برنامه ریسک، تداوم و شرایط بحرانی | ST01,ST22;ALL | E08 |
| PL09 | برنامه اجرای استراتژی جامع و Marketing Mix | ST01 | E01 |
| PL10 | برنامه رشد و آزمایش فرصت | ST02 | E01 |
| PL11 | برنامه لانچ محصول و GTM | ST03 | E01 |
| PL12 | برنامه محصول، PMF و بهبود adoption | ST04 | E01 |
| PL13 | برنامه برندینگ و Brand tracking | ST05 | E02 |
| PL14 | برنامه قیمت‌گذاری و پروموشن | ST06 | E01 |
| PL15 | برنامه دیجیتال مارکتینگ | ST07 | E01 |
| PL16 | برنامه شبکه‌های اجتماعی و کامیونیتی | ST08 | E02 |
| PL17 | برنامه محتوا و تقویم تحریریه | ST09 | E02 |
| PL18 | برنامه SEO و جست‌وجوی ارگانیک | ST10 | E03 |
| PL19 | برنامه رسانه، PPC و Performance | ST11 | E03 |
| PL20 | برنامه creator، influencer و UGC | ST12 | E02 |
| PL21 | برنامه ایمیل، SMS و پیام‌رسان | ST13 | E04 |
| PL22 | برنامه CRM و Lifecycle | ST14 | E04 |
| PL23 | برنامه وفاداری، retention و win-back | ST15 | E04 |
| PL24 | برنامه CRO و بهبود قیف | ST16 | E01 |
| PL25 | برنامه E-commerce و Marketplace | ST17 | E01 |
| PL26 | برنامه فروش، درآمد و Demand generation | ST18 | E04 |
| PL27 | برنامه B2B و ABM | ST19 | E04 |
| PL28 | برنامه توزیع، Retail و Omnichannel | ST20 | E01 |
| PL29 | برنامه بازاریابی محلی | ST21 | E03 |
| PL30 | برنامه PR، اعتبار و ارتباطات بحران | ST22 | E02 |
| PL31 | برنامه شراکت، Affiliate و Referral | ST23 | E01 |
| PL32 | برنامه ورود بین‌المللی و Localization | ST24 | E01 |
| PL33 | برنامه رویداد، نمایشگاه و Sponsorship | ST25 | E02 |
| PL34 | برنامه تجربه مشتری و بهبود خدمات | ST26 | E01 |

### PL01 — برنامه جامع سالانه بازاریابی
- **استراتژی مرجع:** ST01;ALL. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S03,S04,B01,B02,B05,B06,E02,E03,E04,E06,E08.
- **ورودی:** تصمیم‌های مصوب، سال مالی، بودجه و اهداف، تقویم و ظرفیت مشترک.
- **فرایند عملی:** تقسیم اهداف به portfolio و دوره، bottom-up برآورد کار/هزینه، reconcile با سقف و عملیات، تصویب baseline.
- **تحویل:** بودجه دوره/حوزه، roadmap، WBS سطح بالا و milestone.
- **سنجش:** حاشیه، درآمد، هدف مشتری، انحراف هزینه/موعد.
- **قید/مسیر جایگزین:** جمع دوره‌ها با کل سال یکسان؛ کسری منابع به تصمیم برگردد.
- **شواهد روش برنامه‌ریزی:** P01,P02,P03,P04,P07,P08؛ شواهد تخصصی استراتژی از ST مرجع.

### PL02 — برنامه فصلی و rolling 90-day
- **استراتژی مرجع:** ST01;ALL. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S04,B02,B05,B06,E02,E03,E04,E08.
- **ورودی:** baseline سال، واقعیات تا cut-off، تعهدات، forecast جدید.
- **فرایند عملی:** قفل دوره بسته، بازبرآورد باقی‌مانده، اولویت مجدد و reconcile، پیشنهاد change request.
- **تحویل:** برنامه ۹۰روزه و forecast مستقل، delta نسبت به baseline.
- **سنجش:** EAC، milestone، شکاف KPI و ظرفیت.
- **قید/مسیر جایگزین:** forecast مجوز هزینه نیست؛ تغییر baseline نیازمند تایید.
- **شواهد روش برنامه‌ریزی:** P05,P06,P07,P08؛ شواهد تخصصی استراتژی از ST مرجع.

### PL03 — برنامه ماهانه، هفتگی و تقویم عملیاتی
- **استراتژی مرجع:** ST01;ALL. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E02,E03,E04,E05,E06,B05,E08.
- **ورودی:** backlog مصوب، موعد، تقویم کاری، owner و ظرفیت.
- **فرایند عملی:** تفکیک کار اجرایی و acceptance؛ ترتیب و وابستگی؛ timebox و کنترل بار؛ freeze هفته جاری مگر تغییر مصوب.
- **تحویل:** تقویم و task board با موعد و خروجی، بار تیم.
- **سنجش:** کار تکمیل‌شده قابل پذیرش، overdue، utilization و KPI هدف.
- **قید/مسیر جایگزین:** task بدون مالک یا منابع draft؛ هیچ تاریخ دلخواه به‌عنوان feasible.
- **شواهد روش برنامه‌ریزی:** P07,P09,P10,P12؛ شواهد تخصصی استراتژی از ST مرجع.

### PL04 — برنامه بودجه، منابع مالی و جریان نقد
- **استراتژی مرجع:** ST01;ALL. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: B01,B02,B06,S04,S05,E03,E06,B05,E08.
- **ورودی:** سقف، بودجه مصوب، تعهدات، actual، مالیات/FX، دوره پرداخت.
- **فرایند عملی:** cost breakdown و cash phasing؛ تفکیک هزینه و نقد؛ قیود دوره/مرکز هزینه؛ تخصیص حداقل لازم و ذخیره؛ scenario.
- **تحویل:** budget ledger، cash schedule، allocation و funding gap.
- **سنجش:** actual vs plan، EAC، تعهد باز، available balance.
- **قید/مسیر جایگزین:** هزینه نامعلوم صفر نیست؛ بودجه/نقد جدا؛ سقف و ذخیره enforce.
- **شواهد روش برنامه‌ریزی:** P08,P15,P16؛ شواهد تخصصی استراتژی از ST مرجع.

### PL05 — برنامه تحقیقات بازار و بینش مشتری
- **استراتژی مرجع:** ST01,ST04,ST05,ST07,ST24,ST26. مالک تخصصی: M01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: M04,M05,M06,S01,E01,E06,B05,E08.
- **ورودی:** سؤال تصمیم، جامعه/frame، طرح نمونه، هزینه و زمان، مجوز.
- **فرایند عملی:** انتخاب روش مناسب، نمونه/پیش‌آزمون، ابزار پرسشنامه، recruitment، fieldwork، QA، تحلیل و گزارش.
- **تحویل:** research brief، sample plan، questionnaire، fieldwork schedule و deliverables.
- **سنجش:** پوشش frame، پاسخ/عدم پاسخ، کیفیت، precision مطابق طرح.
- **قید/مسیر جایگزین:** sample غیراحتمالی بدون فرض مدل MOE معمول ندارد؛ توقف اگر طراحی نامعتبر.
- **شواهد روش برنامه‌ریزی:** P17,P03؛ شواهد تخصصی استراتژی از ST مرجع.

### PL06 — برنامه اندازه‌گیری، KPI، آزمایش و گزارش
- **استراتژی مرجع:** ST01;ALL. مالک تخصصی: B05؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: B04,S01,B01,B03,E01,E05,E08.
- **ورودی:** goal، metric definition، baseline، data source، experiment unit.
- **فرایند عملی:** metric tree، tracking QA، تعیین owner/cadence و target، طرح آزمون قبل اجرا، ثبت نتیجه.
- **تحویل:** measurement plan، protocol، dashboard dictionary و review schedule.
- **سنجش:** completeness، freshness، primary metric و guardrails.
- **قید/مسیر جایگزین:** بدون داده اثر null؛ attribution از lift جدا؛ تغییر metric بعد آزمون ثبت شود.
- **شواهد روش برنامه‌ریزی:** P18,P19,P20؛ شواهد تخصصی استراتژی از ST مرجع.

### PL07 — برنامه تیم، ظرفیت، پیمانکار و عملیات
- **استراتژی مرجع:** ST01;ALL. مالک تخصصی: E06؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E05,E07,S04,B06,E08.
- **ورودی:** skill/role، availability، cost، dependency، قرارداد و SLA.
- **فرایند عملی:** RACI/DRI، WBS، ظرفیت، make/buy، schedule و procurement، handoff و acceptance.
- **تحویل:** resource plan، assignment، vendor brief و handoff matrix.
- **سنجش:** بار/ظرفیت، milestone، SLA، defect/rework.
- **قید/مسیر جایگزین:** نقش انسانی و مجوز لازم؛ solver تصمیم استخدام نمی‌گیرد.
- **شواهد روش برنامه‌ریزی:** P07,P09,P10,P11,P12؛ شواهد تخصصی استراتژی از ST مرجع.

### PL08 — برنامه ریسک، تداوم و شرایط بحرانی
- **استراتژی مرجع:** ST01,ST22;ALL. مالک تخصصی: E08؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S05,E01,E05,E06,E07,B05.
- **ورودی:** risk register، احتمال/اثر مستند یا رتبه کیفی، trigger و owner.
- **فرایند عملی:** شناسایی ریسک عملیاتی/مالی/اعتباری؛ mitigation و contingency؛ سناریو، escalation، tabletop و بازبینی.
- **تحویل:** risk register، response matrix، reserve و continuity plan.
- **سنجش:** trigger breach، زمان پاسخ، ریسک باقی‌مانده و ذخیره.
- **قید/مسیر جایگزین:** بدون توزیع معتبر احتمال عددی نساز؛ اجرای بحران با انسان.
- **شواهد روش برنامه‌ریزی:** P07,P08,P13,P14؛ شواهد تخصصی استراتژی از ST مرجع.

### PL09 — برنامه اجرای استراتژی جامع و Marketing Mix
- **استراتژی مرجع:** ST01. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S03,S04,M05,M06,B01,E02,E03,E04,E08.
- **ورودی:** تصمیم جامع و انتخاب 4P/7P، اهداف، ظرفیت.
- **فرایند عملی:** هدف به workstream محصول/قیمت/توزیع/ترویج و خدمات؛ کنترل هم‌راستایی و اولویت.
- **تحویل:** integrated action plan و matrix goal→initiative.
- **سنجش:** KPI تجاری و هزینه هر workstream.
- **قید/مسیر جایگزین:** PL01 افق سال است؛ PL09 می‌تواند هر افق باشد؛ در یک plan تکرار نشود.
- **شواهد روش برنامه‌ریزی:** P01,P02,P03,P04؛ شواهد تخصصی استراتژی از ST مرجع.

### PL10 — برنامه رشد و آزمایش فرصت
- **استراتژی مرجع:** ST02. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S06,S04,S05,B01,B03,B04,B06,E03,E04,E08.
- **ورودی:** growth tree، bottleneck، قیود CAC/حاشیه/ظرفیت.
- **فرایند عملی:** backlog فرضیه، هزینه و زمان؛ اولویت و test design؛ scale gate.
- **تحویل:** experiment roadmap و tranche بودجه.
- **سنجش:** incremental contribution، activation، retention.
- **قید/مسیر جایگزین:** scale بدون evidence gate یا ظرفیت ممنوع.
- **شواهد روش برنامه‌ریزی:** P02,P04,P19,P20؛ شواهد تخصصی استراتژی از ST مرجع.

### PL11 — برنامه لانچ محصول و GTM
- **استراتژی مرجع:** ST03. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S06,M07,B01,B02,E02,E03,E04,E05,E06,B04,E08.
- **ورودی:** تاریخ عرضه، readiness، موجودی، فروش و پشتیبانی.
- **فرایند عملی:** backward schedule از milestone؛ آمادگی محصول/پیام/فروش/کانال/پشتیبانی؛ pilot، go/no-go.
- **تحویل:** launch checklist، rehearsal، timeline و owner.
- **سنجش:** readiness، qualified demand، adoption، service SLA.
- **قید/مسیر جایگزین:** وابستگی بیرونی/آمادگی نامعلوم gate را مسدود می‌کند.
- **شواهد روش برنامه‌ریزی:** P02,P04,P07,P09؛ شواهد تخصصی استراتژی از ST مرجع.

### PL12 — برنامه محصول، PMF و بهبود adoption
- **استراتژی مرجع:** ST04. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: M07,M04,M09,S04,B03,B04,E05,E08.
- **ورودی:** فرصت محصول، evidence، capacity، cohort.
- **فرایند عملی:** ترجمه insight به backlog و acceptance؛ اولویت و iteration؛ نمونه/آزمایش؛ rollout.
- **تحویل:** roadmap، sprint-ready backlog و release gate.
- **سنجش:** activation، retention، adoption و guardrail.
- **قید/مسیر جایگزین:** امتیاز PMF جهان‌شمول و وعده adoption ممنوع.
- **شواهد روش برنامه‌ریزی:** P02,P04,P19؛ شواهد تخصصی استراتژی از ST مرجع.

### PL13 — برنامه برندینگ و Brand tracking
- **استراتژی مرجع:** ST05. مالک تخصصی: E02؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: M08,M06,M01,E01,E03,B04,B05,E08.
- **ورودی:** brand platform، پیام، دارایی، مخاطب و baseline ادراک.
- **فرایند عملی:** asset audit، creative briefs، تولید/بازبینی حقوق، rollout، موج سنجش.
- **تحویل:** brand rollout، asset register، calendar و survey plan.
- **سنجش:** awareness، consideration، associations.
- **قید/مسیر جایگزین:** فقدان survey به معنای ادراک صفر نیست.
- **شواهد روش برنامه‌ریزی:** P03,P17,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL14 — برنامه قیمت‌گذاری و پروموشن
- **استراتژی مرجع:** ST06. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: B02,B01,M06,E02,E03,E04,B04,B05,E08.
- **ورودی:** price decision، cost، inventory، calendar، حد حاشیه.
- **فرایند عملی:** قیمت/تخفیف، eligibility و period، سناریو و تست؛ آماده‌سازی کانال، rollback.
- **تحویل:** price calendar، promo brief، rules و approval.
- **سنجش:** margin، net sales، conversion، returns.
- **قید/مسیر جایگزین:** قیمت‌گذاری/تخفیف خودکار ممنوع؛ cannibalization و ظرفیت کنترل.
- **شواهد روش برنامه‌ریزی:** P04,P08,P19,P20؛ شواهد تخصصی استراتژی از ST مرجع.

### PL15 — برنامه دیجیتال مارکتینگ
- **استراتژی مرجع:** ST07. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E02,E03,E04,E05,B01,B03,B04,B05,E08.
- **ورودی:** digital strategy، tracking، channel role، بودجه/ظرفیت.
- **فرایند عملی:** تقسیم workstream paid/owned/earned، dependencies و tagging، production/launch، test/review.
- **تحویل:** channel action matrix، media/content calendar، KPI و budget.
- **سنجش:** qualified lead، CAC، contribution و conversion.
- **قید/مسیر جایگزین:** بدون داده بازده، pilot سقف‌دار نه optimization ظاهری.
- **شواهد روش برنامه‌ریزی:** P03,P04,P15,P18,P19؛ شواهد تخصصی استراتژی از ST مرجع.

### PL16 — برنامه شبکه‌های اجتماعی و کامیونیتی
- **استراتژی مرجع:** ST08. مالک تخصصی: E02؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E03,E04,E06,B04,B05,E08.
- **ورودی:** platform role، content pillars، format، moderation SLA و capacity.
- **فرایند عملی:** تولید batch، review، تقویم به timezone، moderation/response rota، experiment و crisis escalation.
- **تحویل:** post calendar، asset briefs، community shifts.
- **سنجش:** qualified engagement، reach، response SLA، outcomes.
- **قید/مسیر جایگزین:** فرکانس ثابت جهانی ممنوع؛ محدودیت تیم و دسترسی پلتفرم.
- **شواهد روش برنامه‌ریزی:** P03,P04,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL17 — برنامه محتوا و تقویم تحریریه
- **استراتژی مرجع:** ST09. مالک تخصصی: E02؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,M04,M09,E03,E06,B04,B05,E08.
- **ورودی:** topic map، هدف، منابع، asset rights و format.
- **فرایند عملی:** موضوع→brief→draft→review→approval→distribution→refresh؛ برآورد effort؛ reuse مشترک.
- **تحویل:** editorial calendar، brief queue، asset status و owner.
- **سنجش:** تحویل پذیرفته‌شده، qualified consumption، conversion.
- **قید/مسیر جایگزین:** ادعای بی‌شاهد/حقوق نامشخص blocked؛ output count هدف تجاری نیست.
- **شواهد روش برنامه‌ریزی:** P04,P07,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL18 — برنامه SEO و جست‌وجوی ارگانیک
- **استراتژی مرجع:** ST10. مالک تخصصی: E03؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E02,E05,B03,B05,E08.
- **ورودی:** audit، page/query، technical access، priority و baseline.
- **فرایند عملی:** اولویت fixes، mapping intent→page، محتوا/technical dependency، QA و release، review.
- **تحویل:** SEO backlog، page-level acceptance، measurement windows.
- **سنجش:** index eligibility، clicks، CTR، conversion.
- **قید/مسیر جایگزین:** index/rank تضمین نیست؛ تغییر سایت با تایید.
- **شواهد روش برنامه‌ریزی:** P07,P21,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL19 — برنامه رسانه، PPC و Performance
- **استراتژی مرجع:** ST11. مالک تخصصی: E03؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,B01,B02,B04,B05,B06,E02,E08.
- **ورودی:** media objective، سقف spend، creative و tracking، response evidence.
- **فرایند عملی:** flight schedule، media mix، bid/creative brief، test cells، cost bounds، pacing/stop و reallocation proposal.
- **تحویل:** media plan با channel/time/cost، experiment و stop rules.
- **سنجش:** spend pace، CAC، attributed ROAS، lift در صورت اعتبار.
- **قید/مسیر جایگزین:** نرخ بازده تاریخی ثابت فرض نشود؛ خرید خودکار ممنوع.
- **شواهد روش برنامه‌ریزی:** P08,P15,P16,P19,P20؛ شواهد تخصصی استراتژی از ST مرجع.

### PL20 — برنامه creator، influencer و UGC
- **استراتژی مرجع:** ST12. مالک تخصصی: E02؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E03,E06,E07,B04,B05,E08.
- **ورودی:** shortlist، deliverables، قرارداد/حقوق، budget و brand safety.
- **فرایند عملی:** evaluation و selection انسانی، قرارداد، review و disclosure، انتشار و tracking.
- **تحویل:** creator calendar، deliverable/rights checklist، payment milestones.
- **سنجش:** qualified reach/action، cost، attributed outcome.
- **قید/مسیر جایگزین:** بدون حقوق/افشا تایید انتشار ممنوع.
- **شواهد روش برنامه‌ریزی:** P04,P07,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL21 — برنامه ایمیل، SMS و پیام‌رسان
- **استراتژی مرجع:** ST13. مالک تخصصی: E04؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E02,E05,B03,B04,B05,E08.
- **ورودی:** consent، segment، suppression، lifecycle event و deliverability.
- **فرایند عملی:** trigger matrix، precedence، quiet hours/frequency، QA، holdout، review.
- **تحویل:** message journey، eligibility و suppression rules، calendar.
- **سنجش:** delivery، clicks، conversion، complaints/unsubscribe.
- **قید/مسیر جایگزین:** بدون مجوز/opt-out مسدود؛ open proxy تشخیصی.
- **شواهد روش برنامه‌ریزی:** P04,P19,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL22 — برنامه CRM و Lifecycle
- **استراتژی مرجع:** ST14. مالک تخصصی: E04؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E05,E06,M09,B03,B05,E08.
- **ورودی:** stage/CRM schema، owner، consent، integration و SLA.
- **فرایند عملی:** mapping event/ID، handoff، migration/QA، workflow و training، acceptance.
- **تحویل:** CRM roadmap، integration requirements و stage SLA.
- **سنجش:** data completeness، SLA، stage conversion و retention.
- **قید/مسیر جایگزین:** شناسه و مجوز نامعتبر مانع انتقال؛ plan نه تغییر CRM.
- **شواهد روش برنامه‌ریزی:** P04,P06,P07؛ شواهد تخصصی استراتژی از ST مرجع.

### PL23 — برنامه وفاداری، retention و win-back
- **استراتژی مرجع:** ST15. مالک تخصصی: E04؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,B01,B03,M09,E02,B04,B05,E08.
- **ورودی:** cohort و churn، intervention، incentive budget و eligibility.
- **فرایند عملی:** تعیین گروه، طراحی intervention، هزینه و margin، holdout، pilot و scale.
- **تحویل:** retention calendar، offer rules، service recovery و measurement.
- **سنجش:** retention، churn، incremental margin، cost.
- **قید/مسیر جایگزین:** در cohort ناتمام ریزش قطعی نساز؛ incentive زیان‌ده ممنوع.
- **شواهد روش برنامه‌ریزی:** P04,P19,P20؛ شواهد تخصصی استراتژی از ST مرجع.

### PL24 — برنامه CRO و بهبود قیف
- **استراتژی مرجع:** ST16. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: B03,B04,M09,E02,E05,B05,E08.
- **ورودی:** funnel validated، bottleneck، hypothesis، dev capacity.
- **فرایند عملی:** prioritize backlog؛ design/QA؛ sample and duration؛ guardrail؛ rollout/revert.
- **تحویل:** experiment queue، implementation ticket و report.
- **سنجش:** conversion، contribution per eligible unit، error/return.
- **قید/مسیر جایگزین:** توقف زودهنگام آماری بدون روش معتبر ممنوع.
- **شواهد روش برنامه‌ریزی:** P07,P19,P20؛ شواهد تخصصی استراتژی از ST مرجع.

### PL25 — برنامه E-commerce و Marketplace
- **استراتژی مرجع:** ST17. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: B01,B02,B03,E02,E03,E04,E05,B05,E08.
- **ورودی:** catalog، stock، fees، returns، supply/fulfillment و campaign dates.
- **فرایند عملی:** category plan، inventory/demand reconciliation، PDP/price/promo، logistics و post-sale.
- **تحویل:** merchandising calendar، stock/fulfillment gate، channel plan.
- **سنجش:** net revenue، contribution، stockout، returns.
- **قید/مسیر جایگزین:** GMV معادل revenue نیست؛ stock و service limits.
- **شواهد روش برنامه‌ریزی:** P06,P22,P08؛ شواهد تخصصی استراتژی از ST مرجع.

### PL26 — برنامه فروش، درآمد و Demand generation
- **استراتژی مرجع:** ST18. مالک تخصصی: E04؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,B01,B02,B03,E02,E03,E06,B05,E08.
- **ورودی:** sales target، stage history، pipeline، capacity و sales cycle.
- **فرایند عملی:** reverse funnel با نرخ cohort معتبر؛ demand vs capacity؛ handoff و activity plan، reconcile forecast/target.
- **تحویل:** sales plan، pipeline targets، activity/owner/SLA.
- **سنجش:** qualified pipeline، win rate، cycle، booked/recognized revenue.
- **قید/مسیر جایگزین:** نرخ مجهول → scenario نه forecast؛ ظرفیت bottleneck.
- **شواهد روش برنامه‌ریزی:** P06,P22,P23؛ شواهد تخصصی استراتژی از ST مرجع.

### PL27 — برنامه B2B و ABM
- **استراتژی مرجع:** ST19. مالک تخصصی: E04؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,M05,S04,E02,E03,E06,B04,B05,E08.
- **ورودی:** account tiers، buying groups مستند، sales owner و budget.
- **فرایند عملی:** account work packages، touchpoints مجاز، sales alignment، capacity scheduling و pilot.
- **تحویل:** account calendar، meeting/asset plan، review cadence.
- **سنجش:** qualified accounts، meetings، pipeline، contribution.
- **قید/مسیر جایگزین:** مالکیت و privacy؛ احتمال خرید حدسی ممنوع.
- **شواهد روش برنامه‌ریزی:** P03,P04,P06؛ شواهد تخصصی استراتژی از ST مرجع.

### PL28 — برنامه توزیع، Retail و Omnichannel
- **استراتژی مرجع:** ST20. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S06,B01,B02,B06,E03,E04,E05,E06,B05,E08.
- **ورودی:** channel contract، stock، geography، SLA، supply/cost.
- **فرایند عملی:** route-to-market actions، rollout، replenishment، handoff، conflict review.
- **تحویل:** channel rollout، distribution milestones و supply plan.
- **سنجش:** coverage، sell-through، availability، contribution.
- **قید/مسیر جایگزین:** sell-in/out جدا؛ عرضه بیش از ظرفیت ممنوع.
- **شواهد روش برنامه‌ریزی:** P06,P22,P08؛ شواهد تخصصی استراتژی از ST مرجع.

### PL29 — برنامه بازاریابی محلی
- **استراتژی مرجع:** ST21. مالک تخصصی: E03؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E02,E04,E05,B04,B05,E08.
- **ورودی:** locations، ساعات و ظرفیت، local intent، داده تماس/رزرو.
- **فرایند عملی:** per-location checklist، profile/asset، local campaign calendar، geo test و reporting.
- **تحویل:** location action plan، ownership و budget lines.
- **سنجش:** qualified bookings، contribution/location، availability.
- **قید/مسیر جایگزین:** رتبه/footfall تضمین نیست؛ داده location مجاز.
- **شواهد روش برنامه‌ریزی:** P04,P21,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL30 — برنامه PR، اعتبار و ارتباطات بحران
- **استراتژی مرجع:** ST22. مالک تخصصی: E02؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E06,E07,E08,B05.
- **ورودی:** stakeholders، evidence، spokesperson، risks و approval.
- **فرایند عملی:** هدف→audience→message→channel→output/outcome؛ media calendar، escalation، response rehearsal.
- **تحویل:** communication plan، approval matrix، crisis protocol.
- **سنجش:** quality coverage، recall، trust/outcome با روش معتبر.
- **قید/مسیر جایگزین:** AVE معادل اثر نیست؛ پاسخ بحران با انسان.
- **شواهد روش برنامه‌ریزی:** P04,P13,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL31 — برنامه شراکت، Affiliate و Referral
- **استراتژی مرجع:** ST23. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S06,E02,E03,E04,E07,B01,B04,B05,E08.
- **ورودی:** partner selection، terms، commission، rights و capacity.
- **فرایند عملی:** onboarding، tracking rules، deliverables و payment، fraud checks، pilot و exit.
- **تحویل:** partner launch checklist، commission ledger و review.
- **سنجش:** qualified referral، net margin، refund/fraud.
- **قید/مسیر جایگزین:** عدم دوباره‌شماری attribution؛ قرارداد و disclosure gate.
- **شواهد روش برنامه‌ریزی:** P04,P08,P19؛ شواهد تخصصی استراتژی از ST مرجع.

### PL32 — برنامه ورود بین‌المللی و Localization
- **استراتژی مرجع:** ST24. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: S05,S06,B01,B02,B06,E02,E03,E04,E05,E06,E08.
- **ورودی:** market decision، local requirements، FX/landed cost، partners و lead times.
- **فرایند عملی:** milestones قانونی/فنی، localization QA، fulfillment، FX scenario، pilot و approval.
- **تحویل:** country rollout، localization calendar، budget و dependencies.
- **سنجش:** local contribution، service SLA، qualified demand.
- **قید/مسیر جایگزین:** مقررات/پرداخت/حقوق نیازمند تایید متخصص؛ سناریوی ارزی نه پیش‌بینی قطعی.
- **شواهد روش برنامه‌ریزی:** P04,P07,P08,P13؛ شواهد تخصصی استراتژی از ST مرجع.

### PL33 — برنامه رویداد، نمایشگاه و Sponsorship
- **استراتژی مرجع:** ST25. مالک تخصصی: E02؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: E01,E03,E04,E06,E07,B05,E08.
- **ورودی:** event date، venue/contract، capacity، budget، consent.
- **فرایند عملی:** backward plan، logistics، staffing، rehearsal، lead capture و follow-up؛ cancellation contingency.
- **تحویل:** event run sheet، critical milestones، owners و follow-up.
- **سنجش:** qualified leads/meetings، cost، pipeline.
- **قید/مسیر جایگزین:** حضور یا AVE به معنی ROI نیست؛ تعهدات و ایمنی gate.
- **شواهد روش برنامه‌ریزی:** P07,P08,P09,P18؛ شواهد تخصصی استراتژی از ST مرجع.

### PL34 — برنامه تجربه مشتری و بهبود خدمات
- **استراتژی مرجع:** ST26. مالک تخصصی: E01؛ E01 مالک برنامه یکپارچه است. ابزارهای منتخب: M09,E04,E05,E06,B03,B04,B05,E08.
- **ورودی:** journey friction، SLA، resources، evidence و capacity.
- **فرایند عملی:** service blueprint، handoff fixes، training، pilot، rollout و review.
- **تحویل:** CX improvement backlog، service standard، training plan.
- **سنجش:** resolution time، CSAT با response rate، retention.
- **قید/مسیر جایگزین:** ظرفیت واقعی و privacy؛ رضایت نمونه کل جامعه نیست.
- **شواهد روش برنامه‌ریزی:** P04,P06,P07,P19؛ شواهد تخصصی استراتژی از ST مرجع.


## ۴. قرارداد برنامه و مدل داده (طرح فنی)
بدون جدول دامنه جدید برای هر PL. recipe در catalog کد (Pydantic) با id/version، title/alias، applicable_strategy_ids، owner_tool_id، required_fields_by_stage، stage_templates، conditional_tools، deliverables، metric_refs، source_ids، limits و feature availability. PipelineRun.recipe_id/version برای ST یا PL به صورت namespace شناسه؛ mode همچنان single/domain/full طبق معماری، اگر single از E01 مستقیم است metadata recipe می‌تواند در AnalysisRun باشد. همان API پیش‌نمایش/ایجاد/توقف/ادامه/بازبینی موجود. PlanResult یک artifact نسخه‌دار از AnalysisRun E01 یا گزارش PipelineRun؛ در PostgreSQL با شناسه و schema_version موجود. Action/Goal/Decision/Outcome/MetricDefinition/AuditEvent از معماری reuse؛ budget lines، resources و dependencyها در snapshot ساختارمند یا child rows در همان ماژول مطابق schema design، بدون سرویس یا دیتابیس جدید.

### ۴.۱ قرارداد حداقل
| ساختار | فیلدهای ضروری |
|---|---|
| PlanHeader | plan_id, version, parent_version?, workspace_id, strategy_ref/version یا decision_ref/version, recipe_ids/versions, as_of, start/end, timezone, working_calendar_ref, fiscal_calendar_ref?, currency, reporting basis, goal_refs, evidence_refs, scope, state, approver_ref?, approval_at? |
| GoalTarget | goal_ref, metric_ref/version, scope/cohort/grain, baseline/value/date/source?, target/value/horizon, target_kind (approved/proposed), guardrail, owner_ref, cadence, attribution_window? |
| WorkPackage/Action | id, parent_id?, recipe_refs[], goal_refs[], deliverable, acceptance, accountable_owner_ref?, assigned_resource_refs[], priority/ref, dependency_refs[], duration/time_unit, effort_hours per resource, earliest_start?, fixed_window?, due_at?, location/channel?, planned_start/end?, actual_start/end?, status, cost_line_refs[], evidence_refs, gate_refs[] |
| Dependency | predecessor_id, successor_id, type (MVP finish-to-start), lag>=0 in agreed working unit, external milestone status/source if applicable |
| ResourceCapacity | resource/role_id, skill tags, availability by period/calendar, already_committed_effort, remaining_capacity, cost basis, assignment constraint, timezone |
| CostLine | unique id, parent/plan scope, category, action_refs, currency, quantity, unit_cost, estimate/min/max?, tax/FX basis and rate date, cost_period, payment_period/schedule, approved_amount?, commitment_refs, actual_refs, reserve flag, source, cost_owner |
| Measurement | goal/metric refs, collection source, baseline/target, cadence, data quality check, protocol_ref?, owner, guardrail, result refs |
| Risk | id, description, cause assumption, impact dimensions, probability/ordinal likelihood with basis, trigger, prevention, contingency, owner, response cost refs, residual risk, status |
| ChangeRequest | id, baseline_version, requested delta, reason/evidence, effect on goals/cost/cash/capacity/schedule/risk, approval and effective date |
| PlanResult | coverage, assumptions, unknowns, options, feasible schedule? allocations?, constraint_violations[], solver metadata?, plan_ref/version, decision/approval, report refs |

Nullable fields for draft only where permitted. Required scope/owner/date/cost/acceptance/permission for release of action. Cost and duration can be zero only if explicit, e.g. milestone; unknown null. Schema cross-ref verifies same workspace/version. A shared action/cost has one canonical ID; multiple PL/ST refs do not clone it. PII minimization and consent/scope inherited. Roles are not individual sensitive labels.

### ۴.۲ مراحل و وضعیت
Plan draft → feasibility checked (all hard constraints pass or explicit blocked) → submitted → approved baseline → active (human records start) → completed/closed or superseded/cancelled. These are plan lifecycle attributes, not new AnalysisRun execution statuses. Tool/pipeline existing status codes unchanged. Action draft/ready/in_progress/blocked/done/cancelled per existing action state mapping; done requires acceptance evidence. Only authorized human approves; optimistic version check prevents race/double approval; cancellation releases only uncommitted cost, commitments remain until cancelled/settled. approved plan is immutable; edit produces revision and diff; changes to approved amount, scope, deadline, owner/resource assignment where material require change approval. Partial output cannot be execution-ready. Actuals on dated ledger append, correction/reversal with audit, no rewrite baseline. Repeated runs reuse exact input+version, never duplicate cost/action IDs.

DAG for pipeline stages (data → option estimate → S03 approval ref → E01 plan → specialty drafts → reconciliation → plan approval → monitoring) is separate from work dependency DAG (tasks within plan). If specialty output is needed for feasibility, preliminary E02/E03/E04 draft before E01 final; one reconciliation pass then explicit revision if changes, no cycle. No stage waits on actual outcome from same unexecuted plan. In multi-recipe mode shared work/cost merge by canonical IDs, not title similarity; conflicting assumptions, dates or budgets flagged for owner.

## ۵. موتور محاسباتی و انتخاب کتابخانه

### ۵.۱ روش پیش‌فرض و تصمیم ارتقا
| مسئله | روش پایه و انتخاب فناوری | ارتقا و شرط | دلیل عدم استفاده بی‌مورد |
|---|---|---|---|
| WBS و قواعد | Python/Pydantic؛ Decimal؛ ساختار hierarchy | بدون solver | کار و acceptance انسانی است |
| وابستگی/CPM | NetworkX 3.7 candidate: is_directed_acyclic_graph, topological_sort؛ forward/backward pass برای node duration | تقویم واقعی و resource loading قبل از اعلام feasible | dag_longest_path به تنهایی CPM کامل یا resource schedule نیست |
| منابع محدود/موعد | E01/E06؛ load check و serial scheduling شفاف در نمونه ساده | OR-Tools CP-SAT 9.15.6755 candidate؛ interval, no_overlap, cumulative, optional interval و assignment | solver برای تقویم ساده لازم نیست؛ feasible ≠ optimal |
| انتخاب پروژه/بودجه | Decimal و قواعد min/max، کنترل دستی؛ SciPy linprog برای متغیر پیوسته خطی | SciPy milp برای binary/integer؛ CP-SAT اگر قیود ترکیبی/زمانی integer | objective بی‌شاهد یا curve غیرخطی با LP غلط |
| بودجه رسانه | سقف pilot و scenario؛ E03 | Meridian یا PyMC-Marketing طبق قرارداد موتور، response curves و posterior/risk، در محدوده معتبر | ROAS تاریخی اثر افزایشی نیست |
| تقاضا/فروش | B02/B03، scenario یا baseline naive/seasonal naive؛ Statsmodels | StatsForecast/مدل challenger طبق سند علمی، rolling-origin | forecast هدف/تعهد نیست؛ series کافی لازم |
| زمان/هزینه نامطمئن | low/base/high و sensitivity S05 | NumPy/SciPy Monte Carlo joint distribution مستند؛ SALib Sobol فقط ورودی مستقل | PERT یا شبیه‌سازی با احتمال اختراعی ممنوع |
| هزینه/KPI/کیفیت | Decimal, Pandas, SQL, Pandera مشروط | DuckDB/Polars برای حجم بالا طبق موتور | PostgreSQL منبع حقیقت |
| تقویم/نمایش | datetime/zoneinfo استاندارد، تقویم کاری workspace و نمایش محلی، ECharts یا جدول existing UI | CSV/XLSX/ICS export پس از DEV با timezone و schema، UI Gantt فقط اگر نیاز | تقویم نمایشی موتور زمان‌بندی نیست |
| AI | adapter موجود برای WBS/brief draft، خلاصه و پیشنهاد | human approval، Pydantic schema | AI مرجع تاریخ/پول/قید/feasibility نیست |

P26–30 مستند API/metadata و بنچمارک؛ نسخه‌های NetworkX و OR-Tools کاندید همان خانواده‌های فناوری موجودند، وابستگی جدید خارج از معماری اضافه نمی‌کنند. هسته CPython 3.12 و نسخه‌های candidate قبلی موتور بدون تغییر؛ compatibility با وابستگی انتقالی/lock در DEV. API stable/latest ممکن است با release pin متفاوت باشد، ابتدا API همان release بررسی شود. گزینه تجاری (مثل solver حرفه‌ای) در صورت نیاز واقعی و benchmark قابل بررسی با سیاست Capability-First؛ نه برنده جهانی یا الزام خرید. PSPLIB برای مقایسه‌های منتشرشده معتبر است؛ P28 نتایج solverهای SAT را گزارش می‌کند و برتری عمومی OR-Tools را اثبات نمی‌کند. این طراحی بازتولید بنچمارک نمی‌کند؛ فقط الگوی متناسب و ابزار معتبر را انتخاب می‌کند.

### ۵.۲ CPM و تقویم
برای DAG finish-to-start و مدت d_i (عدد صحیح غیرمنفی در واحد کاری واحد)، lag_ji>=0:
- ES_i=max(release_i, max(EF_j+lag_ji)); EF_i=ES_i+d_i. منبع بدون predecessor در release؛ sink پایان پروژه برابر max EF. برای یک deadline ثابت D: LF_i=min(deadline_i if exists, min(LS_k-lag_ik), D for sink)؛ LS_i=LF_i-d_i؛ total float=LS_i-ES_i. deadline از earliest completion کمتر → منفی و violation. اگر deadline نیست D=earliest completion؛ zero float نشان مسیر بحرانی همان baseline ساده، با deadline آزاد ممکن است float مثبت باشد.
- محاسبه topological forward/backward. اگر از weighted edge longest path استفاده شد node duration با node-splitting/edge weights معادل تبدیل شود؛ فقط longest path خام کافی نیست. چند مسیر بحرانی ممکن است.
- فرض این CPM بدون قید ظرفیت مشترک و با calendar همگن است. برای calendar متفاوت، shift/holiday، ساعات کاری و resource availability از time slots مشترک یا تبدیل معتبر استفاده شود؛ weekend و timezone/DST صریح، ذخیره timestamps UTC با timezone نمایش. تقویم شمسی در نمایش/ورودی با تبدیل تست‌شده، موتور تاریخ canonical؛ هیچ تاریخ اشتباه به علت تبدیل. fixed event milestone و external approval باید constraint باشند؛ circular dependencies رد.
- duration elapsed/working با effort ساعت انسانی یکی نیست. یک کار ۳ روزه ممکن است ۴ ساعت effort داشته باشد. ظرفیت = ساعات قابل کار − تعهدات قبلی − زمان غیرقابل دسترس (بدون دوباره‌شماری). assignment across plans جمع شود.

### ۵.۳ مدل RCPSP و انتخاب portfolio
start/end integer slot، end_i=start_i+duration_i؛ precedence start_j>=end_i+lag؛ هر منبع تجدیدپذیر r در هر slot: sum demand_i,r روی کارهای فعال <= available_r,t؛ تقویم متغیر با interval blocks یا time-indexed formulation صحیح. NoOverlap برای منبع انحصاری، Cumulative برای ظرفیت؛ optional interval/Boolean برای کار اختیاری و alternative assignment؛ skill matching و mandatory constraints. غیرتجدیدپذیر مثل پول، constraint مجموع. deadline/release/approval hard; preference نرم با penalty تاییدشده. برای مدل‌های دارای کار اختیاری، حذف کار ضروری ممنوع؛ ابتدا feasibility، سپس هدف مصوب (کمینه تاخیر/makespan/cost یا بیشینه value مستند)، tie-break ثابت. اگر value قابل مقایسه نیست weighted profit خیالی نساز؛ trade-off و feasible options. ثبت status OPTIMAL/FEASIBLE/INFEASIBLE/UNKNOWN و bound/gap اگر موجود، wall time، seed و input version. UNKNOWN بدون جواب feasible تاییدشده = بدون schedule؛ FEASIBLE با محدودیت وقت ادعای optimum نیست. بعد solver، independent check تمام قیود، currency rounding و deadlines. در infeasible فهرست conflict یا بررسی سناریوی تغییر constraint، هیچ relax خودکار. CP-SAT integer-only: scale صحیح slot/پول کوچک‌ترین واحد، کنترل overflow؛ SciPy float solution برای پول با Decimal و constraint recheck.

Budget allocation: x_i>=0، min/max واقعی، sum x + reserve <= approved cap، سقف دوره/کانال/منبع و تعهدات. برای کار binary z_i، fixed cost_i*z_i و dependencies. اگر response_i(x) خطی معتبر، LP/MILP؛ در اشباع یا تعامل، curve معتبر و optimizer مناسب E03؛ bounds مدل و cost per media unit/flight فرض‌های آینده ثبت شوند. اگر هدف profit است از contribution افزایشی قبل از spend منهای spend استفاده شود، نه maximize revenue یا ROAS به جای profit. در نبود evidence فقط هزینه/feasibility، pilot و مقایسه سناریو.

### ۵.۴ هزینه، تعهد، نقد و کنترل پیشرفت
cost_line planned=quantity×unit_cost + taxes/fees in scope (بدون دوباره‌شماری)، currency Decimal و نرخ/تاریخ FX؛ مقادیر actual accrued و paid cash جدا، payment milestone/schedule. بودجه مصوب شامل reserve؛ uncommitted reserve تنها با تایید استفاده. برای cut-off:
- AC = actual recognized cost تا تاریخ؛ OC = outstanding committed cost هنوز در AC شناسایی نشده؛ ETC_uncommitted = برآورد کار باقی بدون تعهد؛ ETC_committed = برآورد هزینه باقیمانده تعهد (ممکن است با OC تفاوت داشته باشد، دلیل ثبت شود).
- EAC=AC+ETC_committed+ETC_uncommitted. Available_to_commit=approved_cap−AC−OC−protected_reserve (actual و OC بدون overlap). gap نسبت به EAC و نسبت به cash cap هر دوره گزارش؛ accrual و cash در یک مخرج مخلوط نشوند. هزینه shared بر اساس قاعده تخصیص مستند یا یک line مشترک؛ subtotals تفکیکی reconcile با کل.
- variance_cost=AC−planned_cost_to_date (positive overspend)، target variance=actual KPI−target با جهت metric، forecast gap=forecast−target. اگر scope یا period متفاوت، null. EVM اختیاری برای work package دارای baseline و پیشرفت عینی: PV=budgeted cost of planned work، EV=budgeted cost of accepted performed work، AC=actual cost; CV=EV−AC، SV=EV−PV، CPI=EV/AC، SPI=EV/PV. این SV واحد پول است نه روز تاخیر؛ EVM فقط پیشرفت تحویل، نه ROI/ارزش مشتری. denominator صفر null. EAC ساده ETC از کار باقی؛ برون‌یابی CPI فقط با فرض ادامه عملکرد و برچسب estimate.
- Forecast_sales از B02 با interval در صورت امکان؛ target عدد مطلوب؛ capacity feasibility constraint. reverse funnel: required_stage=ceil(required_next/rate) با rate معتبر همان cohort و افق و capacity/lag؛ اگر rate=0 و هدف مثبت infeasible، missing → scenario. پیش‌بینی portfolio: کل با اجزا reconcile، وابستگی و cannibalization بررسی؛ sum quantiles مستقل بدون مدل مشترک ممنوع. منابع مشترک ممکن است مانع جمع ساده ظرفیت شوند.

### ۵.۵ ریسک و بازبینی
risk trigger قابل مشاهده، owner، mitigation cost، response، residual risk؛ احتمال/اثر ordinal فقط اولویت کیفی نه expected loss. Expected loss=p×impact تنها با probability و consequence هم‌تعریف و داده/فرض دفاع‌پذیر؛ sum تحت دامنه و overlap مشخص. PERT (a+4m+b)/6 یک heuristic وابسته به سه نقطه و فرض؛ از آن probability deadline بدون model نساز؛ joint simulation برای dependence، ذخیره از risk appetite و داده/سناریو مصوب نه درصد ثابت. B04/B05/E08 review: کار تحویل‌شده، spend، committed، outcome و guardrails؛ تعیین action hold/repair/scale/stop به صورت پیشنهاد با مالک و تایید. Cadence پیش‌فرض طراحی قابل تنظیم: سالانه تصمیم و بودجه، فصلی rolling review، ماهانه cost/forecast، هفتگی capacity/blockers؛ فرکانس به شدت ریسک و سرعت داده وابسته است. Period close immutable؛ forecast جدید هر cut-off؛ rebaseline تنها change request. بودجه یا هدف خودکار از forecast تغییر نکند.

## ۶. تجربه کاربری و خروجی
در همان «ابزارها و پایپلاین‌ها» تب/فیلتر برنامه‌ها کنار استراتژی‌ها؛ همچنین CTA «تدوین برنامه» در تصمیم S03 مصوب و E01. انتخاب strategy existing یا draft، حوزه/افق، سقف و تقویم، profile data reuse؛ سؤال مفقود فقط. Preview recipe و نیازمندی، وضعیت ابزارهای فعال، انتخاب اختیاری، پیش‌نویس. سه نمای ساده از یک dataset: (۱) خلاصه هدف، بودجه، موعد و blockers؛ (۲) جدول actions/owner/status/وابستگی با تقویم یا Gantt اختیاری؛ (۳) بودجه/منابع و KPI/measurement. Drill-down به شواهد و solver assumptions اختیاری. Empty/unknown/infeasible جدا. نشان دادن plan vs actual vs forecast در ستون‌های جدا. تایید plan و تغییرات در تصمیم‌ها؛ نسخه‌ها و تاریخچه در history؛ هیچ منوی اصلی جدید.
خروجی قابل استفاده: executive plan، WBS و milestones، جدول اقدام با معیار پذیرش، تقویم اجرایی، budget/cash و منابع، KPI dictionary و experiment protocols، ریسک و contingency، approval log و version diff. Export PDF/DOCX/XLSX/PPTX مدیریتی طبق قرارداد C-02 و CSV/ICS در صورت نیاز و DEV؛ همه از snapshot واحد، بدون ادعای اتصال به سرویس خارجی. MVP همان ۸ ابزار S01,S03,M01,M05,M06,B01,B03,E01 و B05 ثبت پایه. E01 می‌تواند plan اولیه از decision مصوب و داده دستی تاییدشده بسازد؛ قابلیت تکمیل E02/E03/E04/E06/B04 و ... تا زمان پیاده‌سازی به‌صراحت unavailable/partial. افزودن recipe به catalog به معنی فعال بودن همه مراحل نیست. اجرای مشترک ۲۶ حوزه یا ساخت UI جدا برای هرکدام الزامی نیست.

## ۷. نمونه عملی و fixture (مصنوعی)

### A. برنامه دیجیتال و شبکه اجتماعی ۳۰ روزه
از ST07/ST08 مصوب، PL15/16/03/04/06. هدف افزایش مشتری جدید سودآور، سقف ۱۰۰۰، حاشیه قبل از جذب ۴۰ واحد/سفارش، ظرفیت ۶۰ سفارش اضافه. داده پاسخ کانال نداریم. تاریخ‌های نسبی slot کاری و مالک‌های نمونه فرضی‌اند؛ تطبیق با تقویم واقعی لازم.
| Action | Deliverable / acceptance | مالک نقش | وابستگی | روزهای کاری (بازه نیمه‌باز) | هزینه |
|---|---|---|---|---|---:|
| A1 | tracking QA، رویداد تست و منبع معتبر | analytics | — | [0,2) | 100 |
| A2 | دو brief و assets تاییدشده | content | — | [0,4) | 200 |
| A3 | search pilot فقط پس از A1,A2 و تایید | ads | A1,A2 | [4,14) | 300 |
| A4 | social paid pilot فقط پس از A1,A2 و تایید | social | A1,A2 | [4,14) | 200 |
| A5 | review و گزارش با attribution جدا | analytics | A3,A4 | [14,16) | 0 (هزینه افزایشی صریح؛ effort جدا) |
| RES | ذخیره حفاظت‌شده | manager | approval to release | — | 200 |
جمع ۱۰۰۰. CPM earliest پایان slot16، مسیر A2→A3/A4→A5. اگر A3/A4 یک مسئول انحصاری با effort تمام slot داشته باشند، موازی غیرممکن؛ ترتیب A3[4,14),A4[14,24),A5[24,26) با finish 26. deadline=20 → infeasible بدون منابع بیشتر/کاهش دامنه مصوب. اگر تیم دو منبع واجد شرایط دارد یا demand کمتر است schedule امکان‌پذیر باید check شود. ۳۰ روز تقویمی لزوماً ۳۰ slot کاری نیست. KPI اصلی در صورت design معتبر incremental contribution؛ در غیر این صورت attributed CAC و contribution غیرعلّی. سقف ۶۰ و ۱۰۰۰. اگر spend=300 و ۱۰ مشتری منتسب، CAC=30، حاشیه 400 قبل و 100 بعد از media با فرض یک سفارش و سایر هزینه‌ها خارج scope؛ ROMI null. هیچ خرید واقعی.

### B. برنامه سالانه، rolling و cash
بودجه مصوب ۱۲۰۰۰، چهار فصل ۳۰۰۰ (هر فصل شامل ۳۰۰ reserve در این مثال). در پایان Q1 AC=۲۴۰۰، outstanding commitment برای آینده=۵۰۰؛ ذخیره محافظت‌شده باقی=۹۰۰؛ ETC_committed=۵۰۰ و ETC_uncommitted=۸۰۰۰. EAC=۱۰۹۰۰؛ uncommitted available=۱۲۰۰۰−۲۴۰۰−۵۰۰−۹۰۰=۸۲۰۰. slack EAC=۱۱۰۰ که شامل reserve محافظت‌شده است؛ آزاد واقعی با همین فرض ۲۰۰. Q1 cost variance=AC−planned_cost_to_date؛ اگر planned accrual ۲۷۰۰ (reserve هزینه برنامه‌ریزی‌شده نیست) → −۳۰۰. اگر Q2 payment ۳۵۰۰ و cash limit ۳۰۰۰، funding gap=۵۰۰ حتی اگر سقف سال رعایت شده. forecast جدید مجوز پرداخت نیست. تغییر schedule/commitment به approval. در دو recipe هزینه تولید مشترک ۲۰۰ یک cost_id؛ جمع آن ۲۰۰، نه ۴۰۰.

### C. برنامه فروش B2B و ظرفیت
هدف مصوب ۱۲ قرارداد در cohort با win rate فرصت→برد ۰٫۲۵ و meeting→فرصت ۰٫۵ از دوره هم‌تعریف، فرض ثبات. نیاز ۴۸ فرصت و ۹۶ meeting. تیم ظرفیت ۶۰ جلسه در افق؛ under current assumptions حداکثر expected wins=۶۰×۰٫۵×۰٫۲۵=۷٫۵ (انتظار، نه ۷ یا ۸ قطعی) و gap هدف/ظرفیت واضح. تغییر ظرفیت، افق یا هدف با S03/E01؛ هیچ نرخ بالاتر از داده برای پر کردن شکاف ساخته نشود. اگر چرخه فروش از افق عبور می‌کند، همین مدل ساده نامعتبر و forecast cohort lagged لازم است. برنامه outcome درآمد از B02، نه sum خام pipeline.

### D. نمونه کوچک CPM/EVM و ریسک
A=2، B=4، C=3 بعد A و B، D=1 بعد C؛ ES A=0,B=0,C=4,D=7؛ finish=8، float A=2 و B/C/D=0 در deadline 8، deadline 7 منفی. cycle D→A رد. PV=400، EV=300، AC=350 → SV=−100 واحد پول، CV=−50، SPI=.75، CPI=.857142...؛ به معنای اثر تجاری نیست. یک ریسک delay دارای احتمال نامعلوم و impact ۵ روز: فقط scenario، expected delay null. تاریخ milestone با calendar و capacity بعد CPM بررسی شود.

## ۸. معیار پذیرش محدود پیاده‌سازی
1. ۳۴ شناسه یکتا؛ ۲۶ ST دقیقاً یک PL تخصصی متناظر (PL09–34)، ۸ الگوی مشترک؛ owner و tool refs معتبر، source refs resolve؛ recipe version و availability درست.
2. decision approval معتبر برای active، draft با تصمیم نامصوب؛ owner/cost/acceptance/permission مفقود مانع readiness. حفظ workspace isolation و audit؛ no external action.
3. DAG forward/backward fixture D؛ cycle و predecessor ناموجود رد؛ fixed deadline منفی گزارش. ظرفیت نمونه A: 16 بدون قید، 26 با منبع انحصاری، deadline20 infeasible. solver unknown بدون جواب، هیچ schedule تاییدشده. independent recheck.
4. budget fixture A/B: جمع ۱۰۰۰ و ۱۲۰۰۰، عدم دوباره‌شماری reserve/shared، EAC=10900 و available=8200، cash gap=500؛ AC/OC overlap reject. money scale/FX/date missing flagged.
5. funnel fixture C: 48،96، capacity60 violation؛ نرخ صفر/ناموجود رفتار صحیح. EVM fixture D و zero denominator null. Attribution و incrementality جدا.
6. immutable baseline؛ forecast revision no authority; approval race/idempotency؛ partial blocked/independent branches continue؛ same action/cost ID across recipes. تاریخ تعطیل، timezone/DST، fiscal boundary، calendar conversion fixture.
7. نمایش UI با ۸ ابزار موجود؛ coverage لازم غیرفعال = partial؛ source/KPI missing unknown. Export از همان version و permission. سناریو فرضی برچسب دارد. عدم ادعای PASS تا اجرا.
آزمون محدود کد/API/fixture در DEV، نه بازتولید پژوهش‌ها و نه اجرای CI پولی در این نوبت. هیچ مدل، solver یا runtime جدید در این commit اجرا نشده؛ این مثال‌ها محاسبات طراحی‌اند.

## ۹. رجیستری شواهد و سطح اتکا
مرور هدفمند منابع بنیادی و پژوهش‌های تازه ۲۰۲۵–۲۰۲۶، بنچمارک PSPLIB و مستندات رسمی؛ نه systematic review مستقل PRISMA. رکورد/چکیده و صفحات آنلاین قابل دسترس بررسی شدند؛ متن کامل همه پژوهش‌ها مطالعه نشده. P19/P20 از مرور علمی قبلی به ارث رسیده‌اند؛ ادعای بازبینی مستقل متن کامل نداریم. مطالعات روش/تجربی و مرورها پشتیبان انتخاب طراحی‌اند؛ راهنماهای حرفه‌ای/فنی قواعد اجرا را پشتیبانی می‌کنند و نتیجه تجاری را تضمین نمی‌کنند. شواهد خاص هر حوزه (social/SEO/brand/CRM و غیره) از ST متناظر و موتور علمی reuse؛ از یک مطالعه اجرایی به همه حوزه‌ها تعمیم علّی نمی‌دهیم. اعداد جدید نسخه‌ها صرفاً کاندید؛ نیازی به تغییر baseline علمی قبلی به خاطر این سند نیست.
| ID | منبع | لینک | کاربرد/محدودیت |
|---|---|---|---|
| P01 | McDonald, The Marketing Planning Process: Main Steps (2016) | https://doi.org/10.1002/9781119309895.ch2 | کتاب تخصصی؛ چرخه تحلیل، هدف، راهبرد، بودجه و برنامه؛ چارچوب طراحی نه آزمایش علّی. |
| P02 | Morgan et al., Research in marketing strategy (2019), JAMS | https://doi.org/10.1007/s11747-018-0598-1 | مرور دامنه استراتژی و اجرای برنامه بازاریابی؛ هماهنگی اجزا. |
| P03 | Marketing Planning Best Practice (2001) | https://doi.org/10.1362/1469347012863871 | پژوهش/راهنمای فرایند هماهنگ برنامه‌ریزی؛ بدون تضمین نتیجه. |
| P04 | Morgan, Menon et al., Marketing strategy implementation: Why is it so hard? (2025), JBR | https://www.sciencedirect.com/science/article/pii/S0148296325000542 | پژوهش جدید اجرا؛ شکاف میان تخصیص طراحی‌شده و اجرای واقعی؛ اهمیت زمینه، منابع و مسئولیت. |
| P05 | Henttu-Aho, The role of rolling forecasting in budgetary control systems (2018) | https://doi.org/10.1007/s00187-018-00273-6 | مطالعه چند موردی؛ rolling forecast مکمل کنترل/بودجه، نه تغییر خودکار مجوز هزینه. |
| P06 | Thomé et al., Sales and operations planning: A research synthesis (2012) | https://www.sciencedirect.com/science/article/pii/S0925527311004907 | مرور پژوهش S&OP و هماهنگی تقاضا، عملیات و مالی. |
| P07 | GAO Schedule Assessment Guide (2015) | https://www.gao.gov/products/gao-16-89g | راهنمای حرفه‌ای دولتی؛ توالی، منابع، baseline، critical path، ریسک و پیشرفت؛ اقتباس متناسب. |
| P08 | GAO Cost Estimating and Assessment Guide (2020) | https://www.gao.gov/products/gao-20-195g | استاندارد عملی برآورد هزینه، WBS، عدم قطعیت، actuals و EVM؛ نه معیار ROI بازاریابی. |
| P09 | Review of recent advances on the resource-constrained project scheduling problem (2026) | https://doi.org/10.1080/00207543.2026.2683116 | مرور نظام‌مند ۲۶۸ مقاله؛ محدودیت منابع، چندمهارتی و عدم قطعیت، چندپروژه. |
| P10 | Fifty years of research on resource-constrained project scheduling (2026) | https://doi.org/10.1016/j.ejor.2025.03.024 | مرور علمی؛ دسته‌بندی روش‌ها و مسائل RCPSP. |
| P11 | Kolisch & Sprecher, PSPLIB (1997) | https://www.sciencedirect.com/science/article/abs/pii/S0377221796001701 | بنچمارک استاندارد RCPSP؛ نمونه‌های https://www.om-db.wi.tum.de/psplib/ ؛ نتایج همه solverها یکسان نیست. |
| P12 | Google OR-Tools CP-SAT / scheduling | https://developers.google.com/optimization/cp/cp_solver/ | مستند رسمی قید صحیح، solver status؛ job shop https://developers.google.com/optimization/scheduling/job_shop و employee scheduling https://developers.google.com/optimization/scheduling/employee_scheduling . |
| P13 | Managing uncertainties within S&OP: systematic literature review (2025) | https://doi.org/10.1080/16258312.2025.2526321 | مرور عدم قطعیت و محدودیت‌های پژوهش؛ سناریو و هماهنگی. |
| P14 | Multi-project scheduling under uncertainty and resource flexibility: systematic literature review (2024) | https://doi.org/10.1080/21693277.2024.2319574 | مرور مدیریت عدم قطعیت در منابع مشترک؛ نمی‌توان یک تقویم قطعی را تضمین کرد. |
| P15 | Meridian — budget optimization scenarios and future planning | https://developers.google.com/meridian/docs/post-modeling/scenario-planning-and-future-budget-optimization | مستند رسمی؛ فرض‌های آینده، قید spend، flighting و response؛ رجوع به https://developers.google.com/meridian/docs/user-guide/budget-optimization-scenarios . |
| P16 | PyMC-Marketing — BudgetOptimizer | https://www.pymc-marketing.io/en/stable/api/generated/pymc_marketing.mmm.budget_optimizer.BudgetOptimizer.html | مستند رسمی؛ هدف مطلوبیت، قید و posterior؛ API نسخه انتخابی در DEV تطبیق شود. |
| P17 | AAPOR Disclosure Standards | https://aapor.org/standards-and-ethics/disclosure-standards/ | استاندارد روش، جامعه، نمونه، وزن و گزارش؛ در M01 اعمال شود. |
| P18 | AMEC Integrated Evaluation Framework | https://amecorg.com/amecframework/ | راهنمای هدف، output، outtake، outcome و impact؛ برای ارتباطات، نه اثبات causal. |
| P19 | Lewis & Rao (2015), Unfavorable Economics of Measuring Returns to Advertising | https://doi.org/10.1093/qje/qjv023 | آزمایش‌های میدانی و عدم قطعیت سنجش بازده؛ از مرور Strategy Library به ارث رسیده. |
| P20 | Where A/B Testing Goes Wrong (2025), Journal of Marketing | https://doi.org/10.1177/00222429241275886 | مرجع پیشین موتور برای محدودیت آزمایش؛ B04 حاکم است. |
| P21 | Google Search Central SEO Starter Guide | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | مستند عملی اصلاح و ارزیابی سایت، نه تضمین رتبه. |
| P22 | Adapting sales and operations planning to dynamic and complex supply chains (2025) | https://doi.org/10.1007/s11846-025-00894-x | پژوهش سازگاری برنامه با تقاضا و ظرفیت در محیط پویا. |
| P23 | Forecasting: Principles and Practice, 3rd edition | https://otexts.com/fpp3/ | مرجع پیش‌بینی، ارزیابی rolling origin و سازگاری پیش‌بینی سلسله‌مراتبی. |
| P24 | From outputs to outcomes: project management success and long-term impact (2025) | https://doi.org/10.1016/j.ijproman.2025.102789 | مطالعه تجربی دو مجموعه پروژه؛ تحویل به موقع/بودجه به تنهایی معادل ارزش بلندمدت نیست. |
| P25 | Project management: A review of selection, planning, and execution (2026) | https://www.sciencedirect.com/science/article/pii/S037722172600860X | مرور ساختاریافته ۱۴۵ مقاله از ۲۰۱۴–۲۰۲۶؛ تصمیم در طول چرخه پروژه. |
| P26 | NetworkX DAG documentation | https://networkx.org/documentation/stable/reference/algorithms/dag.html | مستند topological_sort و weighted edge longest path؛ CPM node-duration نیازمند تبدیل درست. |
| P27 | SciPy MILP documentation | https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html | مستند solver خطی mixed integer؛ version-specific API بررسی شود. |
| P28 | Comparing and extending satisfiability solution methods for RCPSP (2026) | https://www.sciencedirect.com/science/article/pii/S0305054825003375 | مقایسه روش‌های SAT بر نمونه‌های benchmark، از جمله PSPLIB؛ دلیل بررسی CP/SAT، نه ادعای برتری OR-Tools در همه مسائل. |
| P29 | OR-Tools 9.15.6755 package release metadata | https://pypi.org/project/ortools/9.15.6755/ | نسخه کاندید با wheel CPython 3.12؛ نه نصب یا سازگاری کامل. |
| P30 | NetworkX 3.7 package metadata | https://pypi.org/project/networkx/3.7/ | نسخه کاندید با classifier Python 3.12؛ نه lockfile نهایی. |

## ۱۰. مراحل DEV
اول E01 common plan contract + محاسبات بودجه/قید/تقویم و PL01/02/03/04 draft روی ابزارهای MVP؛ سپس specialty recipeها فقط به میزان ابزار فعال و با reuse. در مرحله توسعه بعدی، E02/E03/E04/E06/B04 و B05 کامل به برنامه اضافه می‌شوند؛ ترکیب چند recipe و solver محدود منابع در صورت نیاز. مرجع ترتیب تحویل [Full Product Vertical Slice Development Plan](marketing-full-product-development-plan.md) است: VS07 پایه E01 و PL01–04 draft؛ VS18 پذیرش PL01–09، VS19 پذیرش PL10–14/PL21–28/PL31/PL32/PL34، VS20 پذیرش PL15–20/PL29/PL30/PL33. تمام ۳۴ PL در محصول نهایی الزامی‌اند؛ MVP صرفاً milestone. ترتیب مصوب بدون اجازه تغییر نمی‌کند. هیچ فناوری یا نسخه صرفاً برای «جدید بودن» اضافه نمی‌شود. مرجع متد و شواهد این سند، قرارداد runtime موتور علمی، و انتخاب استراتژی سند ST است.

## ۱۱. اتصال PL13 به جایگاه‌سازی و tracking
PL13 و در صورت نیاز PL15/16/19/34 از [Positioning Library](marketing-positioning-library.md) و PositioningResult مصوب برای message architecture، CEP/asset plan، proof/offer/service changes، brand tracking، آزمون پیام و guardrail استفاده می‌کنند. E01 همان برنامه یکپارچه، owner/زمان/هزینه/ظرفیت و gate را نگه می‌دارد؛ هر کار/هزینه مشترک یک ID. baseline/target/actual و forecast جدا، change request برای تغییر جایگاه مصوب. هیچ مسیر PL اضافه نشده و برنامه جایگزین تحقیق ادراک نیست.

## تکمیل رقابتی در Planning Library

[C-01/C-02/C-04/C-05/C-10/C-12 و روش‌های تخصصی](marketing-competitive-enhancements.md): template Excel و نمونه مجاز برای E01/PLهای فعال، خروجی ReportViewModel چهارفرمت از PlanResult و baseline version؛ واردسازی برنامه یا سند استراتژی به draft با source anchors، تطبیق بودجه/واحد/هدف/KPI/actions/dependencies و review انسانی. متن approved در سند به approval داخلی تبدیل نمی‌شود. درس‌آموخته‌های E08 با context و evidence، reuse اختیاری برای review/contingency؛ چهار اتصال داده فقط GA4/Google Ads/Search Console/CRM و manual/CSV/XLSX سایر منابع. مصرف PR/Bass/PREFMAP/SNA در PL متناظر فقط از artifact معتبر مالک؛ سناریو یا فرضیه جای forecast/واقعیت نیست. ۳۴ PL و MVP کامل ثابت؛ no new engine، no actual execution.
