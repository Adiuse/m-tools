# M-Tools — Development Baseline & Architecture Freeze v1.0

**شناسه:** MT-DEV-BASELINE-V1  
**تاریخ:** 2026-11-25  
**وضعیت:** FROZEN_DESIGN / RUNTIME_LOCK_PENDING / NOT_IMPLEMENTED  
**مبنای طراحی:** c155952829c158fbdaca4280168fb8c030944776 و تکمیل‌های همین PR.  
**تصمیم مالک:** Python + Django برای backend و موتورهای علمی؛ React + TypeScript برای frontend. سازگاری و کیفیت علمی مقدم بر یکسان‌سازی زبان دو سمت.

## ۱. دامنه و مرجع تصمیم

چهار موتور، ۲۹ ابزار کامل، MVP هشت ابزار S01/S03/M01/M05/M06/B01/B03/E01 به‌علاوه B05 پایه، ۲۶ ST، ۳۴ PL، ۱۴ PO، ۱۵ QT (۱۳ اولیه، QT12/13 بعدی)، ۳۶ KN، F01–05 و C01–05/C07–12 حفظ می‌شوند. C06 و اتصال مستقیم خارج از GA4، Google Ads، Search Console و CRM مصوب نیستند. CRM vendor انتخاب نشده است. هیچ توسعه قابلیت جدید، تغییر الگوریتم صرفاً به‌خاطر زبان، microservice، agent مستقل، DB دوم یا pipeline اجباری در این فریز وجود ندارد.

مرجع محصول و امنیت: [معماری سیستم](marketing-system-architecture-v1.md). مرجع روش: [Scientific Engine](marketing-scientific-engine-specification.md) و [Evidence Review](marketing-29-tools-evidence-review.md). مرجع UX و قابلیت‌ها: [Workbench](marketing-workbench-design.md)، [UX](marketing-ux-design-v1.md)، [Competitive Enhancements](marketing-competitive-enhancements.md)، [Strategy](marketing-strategy-library.md)، [Planning](marketing-planning-library.md) و [Positioning](marketing-positioning-library.md). در موضوع نسخه‌های هدف، قرارداد قابل اجرا و ترتیب توسعه، این الحاقیه و فایل‌های ماشین‌خوان زیر مقدم‌اند؛ محدودیت‌های علمی، مجوز، پیش‌شرط، شواهد و پذیرش اسناد اصلی همچنان معتبرند.

## ۲. پشته توسعه

| لایه | انتخاب و نسخه مستقیم هدف | وضعیت |
|---|---|---|
| Backend/runtime | CPython 3.12.16، Django 5.2.19 (LTS)، DRF 3.18.3، psycopg 3.3.9 | تصمیم معماری قطعی؛ نسخه‌ها candidate تا resolver/test |
| Storage | PostgreSQL 17.12، schema relational + JSONB، migration Django | خط نسخه هدف؛ اتصال و migration در DEV |
| Science core | NumPy 2.3.5، pandas 2.3.3، SciPy 1.15.3، scikit-learn 1.9.1، Statsmodels 0.14.5؛ Decimal برای پول | حفظ baseline علمی قبلی؛ lock pending |
| Contract / quality | Pydantic 2.14.4، jsonschema 4.26.0، Pandera 0.36.0، NetworkX 3.7 | direct pins |
| Frontend | React/React DOM 19.3.1، TypeScript 7.0.2، Vite 8.3.8، ECharts 6.1.0، SurveyJS Form 2.5.48 | direct pins؛ peer check/lock pending |
| ابزار ساخت | uv 0.13.10، Node 24.22.3 LTS، pnpm 11.29.0 | Node فقط build/dev، نه backend |
| اسناد و ورود داده | openpyxl، XlsxWriter، python-docx، python-pptx، pypdf، defusedxml با نسخه‌های pyproject | import/API check و QA فارسی بعدی |
| Optional science | ده گروه در deps/science-groups.json | فقط گروه مورد نیاز؛ ترکیب واقعی باید resolve شود |
| Meridian | 2.2.1 در deps/meridian/pyproject.toml؛ environment جدا | تعارض ArviZ با PyMC-Marketing از قبل مستند است |

پلتفرم آزمون نخست Linux x86_64 است؛ این انتخاب به معنی الزام سیستم‌عامل میزبانی یا سازگاری تأییدشده سایر پلتفرم‌ها نیست. Django 5.2 LTS برای ثبات API و Python 3.12 انتخاب شده؛ انتخاب نسخه release/security مستقیم بر اساس اطلاعات انتشار در تاریخ بررسی است، نه انتخاب خودکار latest. برای APIهای وابسته، معیار metadata رسمی، wheel/peer availability، مجوز و نتیجه اجرای واقعی است. منابع: [Python 3.12.16](https://www.python.org/downloads/release/python-31216/)، [Django releases](https://www.djangoproject.com/download/)، [Django 5.2 release notes](https://docs.djangoproject.com/en/5.2/releases/5.2/)، [DRF](https://pypi.org/project/djangorestframework/)، [PostgreSQL versioning](https://www.postgresql.org/support/versioning/)، [Node releases](https://nodejs.org/en/about/previous-releases)، [SurveyJS](https://www.npmjs.com/package/survey-react-ui)، [uv](https://pypi.org/project/uv/). نسخه‌های مستقیم frontend در package.json با npm metadata بررسی شده‌اند؛ dependency graph هنوز حل نشده است.

**منبع واحد نسخه‌ها:** [pyproject.toml](../pyproject.toml)، [.python-version](../.python-version)، [frontend/package.json](../frontend/package.json)، [frontend/.node-version](../frontend/.node-version)، [science-groups.json](../deps/science-groups.json)، [Meridian pyproject](../deps/meridian/pyproject.toml). Pin مستقیم به معنی lock انتقالی یا سازگاری اثبات‌شده نیست. در صورت شکست resolver، خروجی conflict واقعی و اصلاح کمینه با دلیل ثبت شود؛ از تغییر بی‌دلیل نسخه یا تنزل روش علمی اجتناب شود. نسخه‌ها پس از نصب و smoke موفق freeze اجرایی شوند. گروه‌های optional به‌صورت ترکیب مورد استفاده با core قفل شوند، نه به‌عنوان ده محیط دائمی؛ فقط Meridian از ابتدا جداسازی ضروری دارد. PM4Py و Survey Creator و استفاده تجاری مجاز، مدل/وزن/پرامپت AI، browser renderer PDF، API version چهار connector و CRM vendor دارای gate اختصاصی پیش از فعال‌سازی‌اند؛ مجوزها طبق AGENTS، بدون دانلود یا خرید خودکار. انتخاب مدل/renderer را بدون benchmark و نیاز واقعی قطعی نکنید.

## ۳. معماری اجرایی

- Django modular monolith، DRF REST، یک PostgreSQL، ۴ ماژول دامنه و core مشترک. Python مالک محاسبه، inference، تحلیل، اعتبارسنجی و ذخیره نتیجه است. React UI و TypeScript برای فرم و نمایش؛ محاسبات مالی/علمی authoritative در frontend تکرار نشوند. Vite build static و همان origin در production؛ Django auth/session با HttpOnly/Secure/SameSite و CSRF؛ ورود/بازنشانی امن و تأیید ایمیل طبق نیاز DEV، هیچ سرویس خارجی auth یا ایمیل بدون تصمیم مستدل الزامی نیست.
- چیدمان هدف: backend/config، backend/core (accounts/workspaces/evidence/datasets/runs/jobs/artifacts)، backend/tools/{strategy,market,business,execution}، frontend/src، contracts، tests. registry واحد از method_id/version و schema؛ method dispatch و validation در server، نه نام تابع دلخواه client.
- مراحل تراکنش: بررسی auth/عضویت/نقش → preflight schema/semantic/refs → snapshot ورودی و hash canonical → محاسبه یا job → validate output → ذخیره immutable و state → تأیید انسانی در endpoint جدا. job طولانی فقط worker همان codebase با DB queue، claim اتمیک و lease/timeout/retry محدود؛ اجرای Meridian با adapter نسخه‌دار، بدون دسترسی مستقیم worker به DB مشتری؛ فقط payload مجاز و نتیجه validate شده. تکرار با idempotency_key و hash در همان workspace؛ payload متفاوت با کلید تکراری → 409. لغو/retry نباید تصمیم، هزینه یا انتشار بیرونی ایجاد کند.
- Scope: Workspace/Membership/CompanyProfile version، سپس Evidence/Dataset/MetricObservation، سپس AnalysisRun/Job/Artifact/version، سپس Decision/Plan/Action/Outcome/Lesson و Connection/SyncRun/Report. FK tenant-safe با unique key (workspace_id, id[, version]) و constraint مرکب DB؛ اگر Django ORM به تنهایی کافی نبود migration RunSQL و آزمون SQL لازم است، نه اتکا به فیلتر UI. Account preferences فقط catalog ID/settings عمومی، بدون ref شرکت. Scratch authenticated بدون Workspace و بدون persistence ضمنی؛ save صریح پس از authorization. جداسازی اطلاعات کاربران و deny-by-default؛ test cross-workspace همه read/write/export/ref endpoints. فایل private، کنترل upload/SSRF، token در secret storage و عدم log/return credential. PostgreSQL test واقعی، backup/restore، migration forward و rollback/recovery strategy قبل از release.

## ۴. قرارداد ابزارها و آزمون‌ها

[analysis.v1.schema.json](../contracts/analysis.v1.schema.json) JSON Schema 2020-12: ۷۲ method/version متعلق به ۲۹ ابزار (۲۹ روش پایه، ۲۸ روش پیشرفته و ۱۵ QT)، ۲۴ row schema، ۱۳ artifact type، envelopes RunRequest/RunResult/ScratchRequest/ScratchResult/DatasetPayload/ArtifactEnvelope و ۲۹ method dataset binding. همه methodها availability=planned. Schema ورودی/خروجی بسته و نوع‌دار؛ هیچ dispatch با input object آزاد خارج از catalog. DTO داخلی Connection و SyncRun با public response جدا؛ credential_ref و secret هرگز به client نرسند.

- method_id + method_version صریح؛ input schema مطابق registry. ورود ناقص معتبر ساختاری به preflight می‌رود؛ required_for_primary و release_gate شرط معنایی هستند، نه ادعای اجرای validation در JSON Schema. قبل از اجرا: grain/period/timezone/cohort/currency، count vs rate/amount، مجوز، نسخه dataset/artifact، روش/نمونه/fit/عدم قطعیت، وابستگی و شواهد را کنترل کنید. داده ناشناخته یا مخرج صفر صفر ساختگی نیست. HTTP: 400 parse، 401 unauthenticated، 403 forbidden، 404 scoped missing، 409 conflict، 422 invalid schema/semantic input، 429 limit، 503 unavailable service. خطاهای boundary fixture در service contract ثبت‌اند. خروجی نیازمند داده به معنی خطای transport نیست.
- دو محور وضعیت: run queued/running/succeeded/failed و analysis ready/conditional/needs_data/error (null پیش از تحلیل). succeeded صرفاً تکمیل پردازش است؛ شرط scientific readiness جداست. نتیجه دارای input_hash، evidence_refs، محدودیت‌ها، assumptions، findings نوع‌دار، next_action. مشاهده فقط با شاهد مجاز؛ فرضیه/estimate با scope و شرایط؛ draft/partial و approval انسانی جدا. Structured artifacts طبق schema و owner spec، بدون approval از client یا خودکار. داده و خروجی ثابت بعد از اجرا؛ تغییر → نسخه جدید.
- [fixtures.v1.json](../contracts/fixtures.v1.json): ۲۳۰ fixture مصنوعی (۷۲ reference + ۷۲ missing_data + ۷۲ invalid_input + ۱۴ semantic boundary). reference output نمونه قراردادی و قابل بررسی است؛ مورد پیشرفته‌ای که داده ندارد، مرجع نیازمند داده است، نه fit موفق. assertionها، tolerance و gate علمی، مقایسه مستقل، edge، ضد نشت و آزمون واقعی هر روش هنگام DEV تکمیل/اجرا شوند. برای artifactهای تخصصی و modelهای وابسته به dataset، داده مصنوعی کامل و انتظار fit/benchmark باید پیش از active شدن آن روش ساخته و اجرا شود؛ وجود نمونه no-data جایگزین آزمون مدل نیست.
- [tests/reference_calculations.py](../tests/reference_calculations.py): ۲۲ oracle عددی مستقل با stdlib، بدون نیاز به Django، نه آزمون کد محصول. [tests/contract_schema_check.py](../tests/contract_schema_check.py): checker استاندارد schema و fixture، شامل envelope و scope connector؛ اجرای آن در baseline هدف هنوز pending است. [tests/scientific_stack_smoke.py](../tests/scientific_stack_smoke.py): نصب/API نماینده، نه اثبات fit/validity. آزمون unit بر method واقعی با fixture، integration REST/DB، authorization و failure/recovery؛ end-to-end UI و import/export فارسی/RTL؛ سپس pilot.

## ۵. Gate سازگاری و اجرای محلی

پس از فراهم بودن شبکه مجاز، Linux x86_64، Python 3.12.16، uv 0.13.10، Node 24.22.3 و pnpm 11.29.0، در checkout تمیز همین branch:

```bash
python3 scripts/verify_stack.py
# فقط وقتی منابع کافی و گروه‌های پیشرفته لازم هستند:
python3 scripts/verify_stack.py --profile full
# نمونه برای گروه‌های معین:
python3 scripts/verify_stack.py --groups forecast causal
```

[scripts/verify_stack.py](../scripts/verify_stack.py) ایجاد/بررسی uv.lock و pnpm-lock.yaml، نصب frozen، pip check، آزمون schema/oracle، import و API پایه، CLI frontend، و در profile منتخب resolve ترکیبی با core constraints و lock دارای hash؛ Meridian پروژه جدا. نسخه‌های lock جدید فقط پس از بررسی نتیجه و diff ثبت شوند. فایل evidence محلی .stack-check/report.json و lockها؛ گزارش کامل شامل commit، platform، versions، logs، scope، hash و وضعیت PASS/FAIL/BLOCKED/NOT_RUN نگهداری شود. CI قبلی برای doc-change خودکار اجرا نشود؛ workflow موجود manual-only شده و dispatch جدید انجام نشده است. اجرا اختیاری با منابع مجاز مالک، ترجیحاً local. Core بدون model download؛ full نصب/آزمون optional است، دانلود وزن و fit نیست.

**وضعیت واقعی این مرحله:** در محیط فعلی Python 3.13.5، uv 0.10.0 و Node 22.16.0 موجود بود؛ Python 3.12.16 و pnpm در دسترس نبودند. DNS برای pypi.org و registry.npmjs.org شکست خورد (curl 6) و uv lock --offline --python 3.12.16 با exit 2 به دلیل نبود interpreter شکست خورد. بنابراین هیچ uv.lock/pnpm-lock.yaml معتبر تولید و هیچ سازگاری مشترک جدیدی تأیید نشده است. این blocker محیط است، نه کشف conflict جدید کتابخانه. اجرای مستقل ۲۲ oracle روی Python 3.13.5: ۲۲/۲۲ PASS؛ QT13 با Statsmodels محلی 0.14.6: n=680.3526619، ceil=681، توان 0.8003728؛ فقط شاهد مرجع و نه PASS نسخه پین‌شده 0.14.5. کنترل ساختاری اولیه در محیط ابزار روی کاتالوگ و نمونه‌های اصلی انجام شد؛ checker استاندارد و runner جدید هنوز اجرا نشده‌اند. CI قبلی ۹/۹ روی Python 3.13.18 (commit ceb1d861ecbe9e94709e01b4329171cbdbdbb71f، run 45445594222) تاریخی است و این baseline را تأیید نمی‌کند.

## ۶. نقشه توسعه کامل محصول (مصوبه مالک)

[Full Product Vertical Slice Development Plan v1.0](marketing-full-product-development-plan.md) مرجع حاکم ترتیب، محدوده PR، وابستگی و معیار پذیرش مستقل است. دامنه تحویل کل محصول نهایی است؛ MVP فقط milestone میانی و نه نقطه پایان. ۷ فاز، ۲۲ PR برنامه‌ریزی‌شده VS00–VS21؛ ۱۹ برش تحویلی قابلیت‌محور VS02–VS20، دو مرحله gate/زیرساخت و یک مرحله پذیرش نهایی.

| فاز | PR plan | شرط خروج |
|---|---|---|
| D0 — Stack gate | VS00 | core resolve/lock/install/test و PostgreSQL/driver واقعی؛ فعلاً BLOCKED |
| D1 — Foundation & IO | VS01–02 | حساب، workspace، registry و قرارداد مشترک؛ داده، template/demo، گزارش ۴ فرمت و intake پروفایل |
| D2 — Daily workbench | VS03 | ۱۳ QT اولیه، ۳۶ KN، شخصی‌سازی، scratch/save |
| D3 — MVP milestone | VS04–07 | ۸ ابزار پایه مصوب S01/S03/M01/M05/M06/B01/B03/E01 و B05 پایه، برنامه یکپارچه و import استراتژی؛ پایان MVP نیست |
| D4 — Full tool expansion & connections | VS08–14 | روش پایه همه ۲۹ ابزار، QT12/13، حافظه سازمانی، SNA/process، ۴ اتصال داده مصوب |
| D5 — Advanced science & full libraries | VS15–20 | همه روش‌های مصوب با gate علمی، PO01–14، ST01–26، PL01–34 و pipeline یکپارچه؛ readiness نهایی ابزارها |
| D6 — Full-product acceptance | VS21 | همه VSها، F03/F05 و pilot واقعی، scientific/functional/security/license gates؛ تایید مالک برای release |

هر ۷۲ method و همه شناسه‌های ST/PL/PO/KN/F/C و providerها مالک تحویل صریح در سند تفصیلی دارند. برای هر برش، scope و نتیجه قابل استفاده، آزمون مثبت/منفی و محدودیت مشخص شده است؛ هیچ قابلیت مصوب در backlog نامعلوم رها نشود. تغییر ترتیب صرفاً با evidence و تایید مالک، نه تغییر دامنه. D0 precondition پذیرش کد وابسته است؛ optional group قبل از اجرای method مربوط lock/test شود. همه فازها برنامه‌اند؛ هیچ برش DEV اجرا یا merge نشده است. اگر داده، مجوز، CRM vendor یا pilot لازم در دسترس نباشد، وضعیت gate مربوط BLOCKED/NOT_READY و سایر برش‌های مستقل فقط طبق نقشه ادامه می‌یابند. انتشار محصول کامل منوط به پذیرش همه VS00–21 و تایید مالک است.

## ۷. وضعیت فریز و پذیرش

| سطح | وضعیت |
|---|---|
| V0 طراحی، انتخاب زبان/معماری، کاتالوگ قرارداد و برنامه توسعه | FROZEN_DESIGN؛ قراردادها و fixtureها ثبت شده‌اند |
| V1 resolve/install/lock/compatibility روی نسخه‌های هدف | BLOCKED / NOT VERIFIED |
| V2 implementation + golden unit/integration + actual UI | NOT_IMPLEMENTED / NOT_RUN |
| V3 validation علمی/کاربردی، F03/F05 و pilot | NOT_RUN |

فریز تصمیم طراحی به معنی اثبات سازگاری تمام کتابخانه‌ها یا اعتبار علمی محصول نیست. قبل از active، evidence قابل بازبینی برای همان method/version و قبل از انتشار، gateهای علمی، کاربردی، مجوز و امنیت لازم است. دامنه بدون تصمیم صریح مالک توسعه داده نشود. تغییر بعدی فقط اصلاح شواهدمحور و ثبت دلیل، نه بازطراحی خودسرانه.
