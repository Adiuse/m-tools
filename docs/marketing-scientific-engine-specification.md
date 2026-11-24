# Scientific Engine & Technology Specification — M-Tools v1.1

تاریخ بازبینی منابع رسمی: ۲۴ نوامبر ۲۰۲۶؛ نسخه 1.1 پس از تطبیق API و فراداده انتشار. مکمل [معماری فنی](marketing-system-architecture-v1.md)، [مشخصات ابزارها](marketing-tool-specifications.md) و [UX](marketing-ux-design-v1.md). سند طراحی و برنامه آزمون است؛ هیچ‌کدام از ۲۹ ابزار پیاده‌سازی یا آزمون انتهابه‌انتها نشده‌اند. نمونه‌های زیر fixture مصنوعی و خروجی مورد انتظار هستند، نه گزارش تست اجراشده. سیاست Capability-First در AGENTS.md برقرار است.

## ۱. انتخاب روش و معماری علمی

چهار موتور و ۲۹ ابزار بدون تغییر. هر ابزار از registry مشترک، یک schema ورودی/خروجی، یک روش پایه و در صورت نیاز روش پیشرفته استفاده می‌کند. سه خانواده قابلیت (محاسبه قطعی، تحلیل آماری/ML، تحلیل زبانی/تصمیم‌یار) قابلیت‌های موازی‌اند، نه سلسله‌مراتب اعتبار. AI لزوماً دقیق‌تر از فرمول نیست. وابستگی‌های پیشرفته فقط برای ابزار نیازمند آنها فعال می‌شوند.

ترتیب: کنترل داده و مجوز → انتخاب روش پایه معتبر → بررسی شرایط روش پیشرفته → مقایسه با پایه روی داده مستقل/ارزیابی انسانی → ثبت نسخه، فرض‌ها، نتیجه و عدم قطعیت → تأیید انسانی. در صورت شکست، fallback مجاز با ذکر دلیل؛ نه تغییر پنهانی روش یا جعل نتیجه. خروجی‌های observed/estimate/hypothesis/recommendation مطابق معماری مرجع. برای نتیجه مشروط، شروط صریح؛ برای داده ناکافی needs_data.

## ۲. انتخاب فناوری و سیاست نسخه

انتخاب baseline علمی برای شروع توسعه: CPython 3.13.x؛ Django 6.1 در صورت استفاده از نسخه جدید و سازگار، PostgreSQL 18، React/TypeScript و ECharts (UI در سند دیگر)، uv و Pydantic 2. Python 3.13 انتخاب اشتراک سازگار برای DoWhy، PyMC-Marketing، EconML و پشته علمی اصلی است؛ Meridian به دلیل محدودیت Python 3.11/3.12 فقط در محیط مقایسه‌ای جدا اجرا می‌شود. نسخه‌های دقیق بعد از CI و lockfile تثبیت می‌شوند. Python 3.14/3.15 در این پروژه فعلاً baseline نیستند؛ فقط پس از عبور همه گروه‌های وابستگی از ماتریس سازگاری بررسی شوند. نسخه‌های دقیق در lockfile واقعی تعیین می‌شوند؛ اعداد نسخه پاسخ‌های قبلی یا latest متغیر جایگزین lockfile نیستند.

| گروه | فناوری/خط نسخه هدف | وابستگی و شرایط | مرجع رسمی |
|---|---|---|---|
| هسته | Python 3.13، Decimal و stdlib | مالی دقیق؛ هیچ float برای پول به عنوان مرجع نهایی | https://docs.python.org/3/library/decimal.html |
| داده | NumPy 2.5.5، pandas 2.3.3 | هر دو دارای پشتیبانی Python 3.13؛ pandas 2.3 با NumPy 2.x سازگار است و شرط pandas<3.0 موردنیاز StatsForecast را برآورده می‌کند | https://pypi.org/project/numpy/2.5.5/ ; https://pypi.org/project/pandas/2.3.3/ |
| آمار | SciPy 1.18.1، Statsmodels 0.15.0 | هر دو برای Python 3.13 قابل نصب‌اند؛ APIهای آزمون نسبت در بخش آزمون مشخص شده‌اند | https://pypi.org/project/scipy/1.18.1/ ; https://pypi.org/project/statsmodels/0.15.0/ |
| ML | scikit-learn 1.9.1 | Python >=3.11، NumPy/SciPy، Narwhals، joblib و threadpoolctl؛ با EconML 0.17.1 چون شرط sklearn <1.10 است سازگار از نظر بازه نسخه | https://pypi.org/project/scikit-learn/1.9.1/ ; https://scikit-learn.org/stable/ |
| schema | Pydantic 2.x | strict validation، explicit null، JSON Schema | https://pypi.org/project/pydantic/ |
| فرم | SurveyJS Form Library + Creator، نسخه هم‌خانواده | React و بسته‌های survey-core/creator؛ مجوز توسعه و انتشار طبق سیاست | https://surveyjs.io/documentation |
| پیش‌بینی | StatsForecast 2.1.1 برای سری‌های متعدد؛ Statsmodels برای مدل‌های کلاسیک؛ Chronos-2.3.2 فقط challenger؛ بدون مدل‌وزن در runtime اصلی | StatsForecast به coreforecast و utilsforecast وابسته است؛ Numba وابستگی اجباری مستقیم نسخه 2.1.1 نیست. Chronos-forecasting 2.3.2 به torch>=2.2,<3، transformers>=4.41,<6 و accelerate>=1.1,<2 نیاز دارد | https://pypi.org/project/statsforecast/2.1.1/ ; https://pypi.org/project/chronos-forecasting/2.3.2/ ; https://github.com/amazon-science/chronos-forecasting |
| NLP | Sentence Transformers + مدل Qwen3-Embedding-0.6B به‌عنوان نامزد اول؛ BGE-M3 نامزد مقایسه؛ BERTopic 0.17.4 اختیاری | Qwen3-Embedding نیازمند transformers>=4.51 و sentence-transformers>=2.7 است؛ 100+ زبان ادعا شده اما دقت فارسی باید روی داده واقعی سنجیده شود. BERTopic 1.0.0b1 پیش‌انتشار است و baseline نیست | https://huggingface.co/Qwen/Qwen3-Embedding-0.6B ; https://huggingface.co/BAAI/bge-m3 ; https://pypi.org/project/bertopic/0.17.4/ |
| علّی | DoWhy 0.14 برای model/identify/estimate/refute؛ EconML 0.17.1 برای DML و CATE | DoWhy 0.14 به Python <3.14 محدود است؛ EconML 0.17.1 به sklearn>=1.6,<1.10 و NumPy>=2.0.2 نیاز دارد؛ sklearn 1.9.1 در این بازه است | https://pypi.org/project/dowhy/0.14/ ; https://pypi.org/project/econml/0.17.1/ ; https://www.pywhy.org/dowhy/main/ |
| بازاریابی بیزی | PyMC-Marketing 1.5.0 انتخاب اصلی MMM/CLV؛ Google Meridian فقط گزینه مقایسه‌ای جدا | PyMC-Marketing به Python>=3.12، PyMC>=6.0، ArviZ>=1.2 و در metadata فعلی NumPy<2.6 نیاز دارد. Meridian فقط Python 3.11/3.12 را می‌پذیرد، backend پیش‌فرض JAX دارد و GPU را توصیه می‌کند؛ هم‌زمان هر دو stack را بی‌دلیل نصب نکن | https://pypi.org/project/pymc-marketing/ ; https://developers.google.com/meridian/docs/user-guide/installing |
| مدل ریزش | LogisticRegression به‌عنوان baseline؛ CatBoost 1.2.10 challenger؛ SHAP و Optuna اختیاری | CatBoost wheel برای CPython 3.13 موجود است؛ SHAP سهم ویژگی در پیش‌بینی را توضیح می‌دهد نه علیت؛ Optuna فقط با validation بدون نشت داده | https://pypi.org/project/catboost/1.2.10/ ; https://shap.readthedocs.io/ ; https://optuna.readthedocs.io/ |
| حساسیت/تخصیص | NumPy/SciPy برای سناریو و Monte Carlo؛ SALib 1.6.0 فقط تحلیل حساسیت سراسری Sobol/Morris؛ SciPy HiGHS برای LP/MILP؛ OR-Tools CP-SAT برای زمان‌بندی/قیود صحیح | CP-SAT فقط ضرایب صحیح می‌پذیرد؛ SciPy milp یک wrapper بر HiGHS است؛ SALib جایگزین شبیه‌سازی عمومی Monte Carlo نیست | https://pypi.org/project/SALib/1.6.0/ ; https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html ; https://developers.google.com/optimization/cp/cp_solver/ |
| حجم بالا | Pandas ابزار پیش‌فرض؛ Polars 2.1.0 و DuckDB 2.0.1 فقط در صورت benchmark مثبت | Polars برای پردازش DataFrame؛ DuckDB برای SQL تحلیلی روی فایل/Parquet؛ هیچ‌کدام جای PostgreSQL منبع حقیقت نیستند | https://pypi.org/project/polars/2.1.0/ ; https://pypi.org/project/duckdb/2.0.1/ |
| AI | adapter اختصاصی JSON Schema؛ مدل منتخب با نسخه ثابت | ارائه‌دهنده/مدل بعد از benchmark فارسی، هزینه، latency، privacy؛ بدون عامل مستقل | سیاست AI معماری و NIST AI RMF |

نسخه‌ها و بازه‌های کلیدی با مستندات رسمی و metadata انتشار تطبیق داده شده‌اند. این تطبیق استاتیک است، نه نتیجه نصب و اجرای یک محیط واقعی. نسخه‌های فوق کاندیدهای تثبیت در CI هستند؛ فقط پس از حل وابستگی و smoke test در Python 3.13 به‌عنوان stack تأییدشده شناخته می‌شوند. به‌روزرسانی امنیتی و سازگاری مقدم بر انتخاب شماره نسخه بزرگ‌تر است.

### قرارداد تثبیت وابستگی

در آغاز DEV: pyproject.toml و uv.lock، نسخه Python و platform هدف، lockfile frontend، نسخه solver و مدل/وزن/پرامپت. گروه core کوچک، extras مجزا forecast/nlp/causal/bayesian/optimization؛ هر گروه مورد نیاز با هسته و گروه‌های هم‌زمان لازم resolve/install شود. آزمون import و API smoke، تست fixture، pip/uv dependency check یا معادل، گزارش امنیت و SBOM/رجیستری مجوز. اگر ترکیب ناممکن بود، نسخه سازگار یا جایگزین مجاز و دلیل ثبت شود؛ سرویس مستقل فقط در صورت ضرورت اثبات‌شده. هیچ lockfile در این PR ساخته نشده؛ مرحله DEV مسئول آن است. برای مجوز توسعه و release gate به AGENTS.md مراجعه شود.

## ۳. مشخصات علمی و فناوری ۲۹ ابزار

فیلدهای دقیق سطح معماری در سند معماری فنی، ورودی/خروجی این جدول مکمل آنهاست. حداقل داده تابع سؤال و مدل است؛ هیچ عدد عمومی برای کفایت علمی همه مسائل وجود ندارد. نمونه کوچک زیر صرفاً golden fixture برای کنترل رفتار کد است. روش پیشرفته در MVP الزام اجرا نیست.

| ID | داده و پیش‌شرط | روش پایه و پیاده‌سازی | روش پیشرفته مشروط | تست مرجع (ورودی → انتظار) | fallback |
|---|---|---|---|---|---|
| S01 | هدف، مشاهده هم‌تعریف، شواهد؛ حداقل یک جفت هدف/واقعی برای شکاف | Decimal؛ درخت مسئله اختصاصی، فرضیه‌های رقیب و شواهد مخالف | DoWhy فقط در B04 برای آزمون علّی قابل شناسایی؛ AI برای استخراج فرضیه | هدف 100، واقعی 70 → gap=-30؛ علت بدون شاهد hypothesis | نبود جفت معتبر: تعریف مسئله/جمع‌آوری داده |
| S02 | محصول، مشتری، مدل درآمد و هزینه؛ شواهد رقبا برای مزیت | بوم اختصاصی ۹ بخش؛ VRIO به‌صورت rubric مستند؛ ارزیابی انسان | AI ساختاردهی شواهد؛ بدون مدل ML مستقل | فروش اشتراکی ثبت شده، رقبا نامعلوم → revenue_model=subscription، advantage=unknown | بوم ناقص و فرضیه آزمون |
| S03 | هدف، مسئله، دست‌کم دو گزینه یا توضیح تک‌گزینه، قیود | فیلتر قیود سخت، مقایسه گزینه و trade-off؛ انتخاب انسانی | S04 برای امتیازدهی؛ AI فقط پیشنهاد مستند | بودجه 100، گزینه A هزینه 120، B هزینه 80 → A نامجاز؛ B نیازمند تأیید | کمبود گزینه: طرح تولید و آزمون گزینه |
| S04 | حداقل دو گزینه و یک معیار قابل مقایسه، کران و وزن صریح | NumPy: نرمال‌سازی و جمع وزنی؛ تحلیل سناریوی وزن با grid ساده و بررسی ثبات رتبه؛ SALib فقط اگر مدل عددی پیوسته و ورودی‌های دارای دامنه معتبر باشد | SALib فقط برای مدل عددی با دامنه/توزیع معتبر؛ نه جایگزین rubric | A=(.8,.2)، B=(.4,.9)، w=(.6,.4) → .56 و .60؛ با w=(.8,.2) → .68 و .50 | معیار مفقود مؤثر: بدون رتبه قطعی |
| S05 | پایه و پارامترها/دامنه سناریو؛ توزیع و وابستگی برای شبیه‌سازی | Decimal/NumPy: سناریوی کم/پایه/زیاد و تغییر یک پارامتر | NumPy Generator یا scipy.stats.qmc/distributions برای Monte Carlo با seed؛ SALib Sobol فقط برای تحلیل حساسیت مدل روی دامنه‌های معتبر | قیمت 5 و حجم 8/10/12 → درآمد 40/50/60؛ توزیع نامعلوم → بدون احتمال | سناریوی قطعی یا کیفی |
| S06 | محصول، بخش، هدف، کانال و ظرفیت؛ اقتصاد واحد برای تصمیم مالی | قالب GTM/Ansoff؛ مقایسه ظرفیت و هزینه با B01 | AI پیشنهاد و B06/E03 برای بهینه‌سازی دارای داده | کانال هزینه 150 در سقف 100 → خارج طرح؛ CAC نامعلوم → مشروط | طرح آزمون کوچک بدون ادعای ROI |
| M01 | سؤال، جامعه، روش، بودجه؛ داده پاسخ اختیاری؛ برای استنباط n از دقت/توان | SurveyJS Creator + Form Library؛ SciPy/Statsmodels؛ پرسشنامه نسخه‌دار، آمار توصیفی، SRS و Wilson | طرح پیچیده با وزن/خوشه فقط پس از بررسی متخصص؛ تحلیل کیفی M04 | SRS با p=.5,z=1.96,e=.05 → n=385 پیش از تصحیح؛ بدون پاسخ فقط طرح؛ 30/100 غیرتصادفی → 30% نمونه، نه جامعه | طرح تحقیق، مصاحبه و جمع‌آوری واقعی |
| M02 | جمعیت واجد شرایط، نرخ خرید، قیمت و قلمرو؛ هم‌واحد و هم‌افق | Decimal/Pandas: bottom-up؛ برآورد top-down مستند برای کنترل متقابل | SciPy/NumPy سناریو و عدم قطعیت دارای فرض مستند | 100×2×5=1000؛ 60 خریدار قابل خدمت → SAM=600؛ 10 قابل دستیابی → SOM=100 | مخرج نامعلوم: بدون عدد؛ دامنه مستند اگر ممکن |
| M03 | بازار، رقیب و شواهد تاریخ‌دار؛ حداقل یک رقیب برای مقایسه | ماتریس ویژگی/قیمت، PESTEL/Porter به‌صورت rubric؛ Pandas + AI مستند | استخراج متنی/جست‌وجوی مجاز؛ هر ادعا به منبع | قیمت A=10 و B=null → B مجهول، نسبت قیمت null | طرح تحقیق رقبا؛ بدون سهم بازار جعلی |
| M04 | متن واقعی و شناسه شاهد؛ مصاحبه/بازخورد و زمینه؛ حداقل یک شاهد برای یک مشاهده | کدگذاری با codebook و مرور انسان؛ Sentence Transformers با Qwen3-Embedding-0.6B candidate و BGE-M3 challenger؛ گروه‌بندی پیشنهادی، نه برچسب حقیقت | BERTopic 0.17.4 فقط corpus کافی و آزمون ثبات؛ embedding مدل ثابت؛ ارزیابی فارسی با نمونه انسانی | دو متن درباره تأخیر، یک متن کیفیت؛ هر theme دارای ref واقعی؛ متن جعلی رد | کدگذاری دستی؛ بدون شاهد فقط طرح مصاحبه |
| M05 | داده مشتری/بخش، معیار و تعریف؛ برای RFM تراکنش تاریخ‌دار و شناسه؛ ML مشروط به حجم/ثبات | Pandas RFM/قواعد؛ sklearn Pipeline+StandardScaler+KMeans و sklearn.cluster.HDBSCAN (اختیاری؛ بدون نیاز به بسته جداگانه hdbscan) | ارزیابی silhouette در صورت معتبر بودن، ثبات bootstrap، تمایز عملی و اعتبار روی نمونه مستقل؛ هیچ k اجباری | RFM تاریخ مرجع و تراکنش یکتا؛ چهار نقطه (0,0),(0,1),(10,10),(10,11)، k=2 → دو جفت مستقل از شماره label؛ fixture فقط فنی | قواعد بخش‌بندی و فرضیه بازار هدف |
| M06 | بخش هدف، گزینه‌های جایگزین، منافع و شاهد؛ نقشه ادراکی نیازمند رتبه‌بندی واقعی | STP و بیانیه ارزش؛ AI مستند؛ sklearn MDS روی ماتریس فاصله معتبر | آزمون مفهوم/پیام B04؛ انتخاب ویژگی با تحقیق | ادعای «سریع‌ترین» بدون شاهد → hypothesis؛ ماتریس فاصله نامتقارن → رد | بیانیه مشروط و طرح آزمون |
| M07 | تعریف فعال‌سازی/نگهداشت، cohort و پنجره؛ بازخورد مستقل | Pandas cohort، تکرار خرید، قیف؛ triangulation و مرور انسان | مدل بقا با داده censoring معتبر؛ اختیاری و پس از بررسی روش | 10 واجد شرایط، 4 بازگشته در پنجره → 40%؛ cohort ناتمام حذف/علامت؛ PMF قطعی ممنوع | طرح گردآوری شواهد و آزمون |
| M08 | هویت و پیام؛ تحقیق واقعی برای ادراک، آگاهی و تداعی | ممیزی برند؛ Pandas نسبت‌های پیمایش، کدگذاری انسانی + Sentence Transformers | BERTopic/مدل طبقه‌بندی فارسی فقط با ارزیابی برچسب انسانی | بدون پاسخ ادراک → perception_gap=null؛ آگاهی 20 از 50 → 40% نمونه | ممیزی هویت بدون ادعای ادراک |
| M09 | مراحل، تماس‌ها و شواهد دارای زمان؛ شناسه برای مسیر فردی | Pandas ترتیب رویدادها، دسته‌بندی شکایت و فراوانی با مخرج؛ نقشه سفر | AI گروه‌بندی متن؛ خوشه‌بندی فقط در صورت ارزیابی | A→B→B duplicate event_id → A→B؛ شکایت بی‌زمان مسیر قطعی نیست | نقشه فرضی و تحقیق کیفی |
| B01 | ارز و دوره مشترک؛ درآمد، هزینه، مشتری جدید؛ cohort برای LTV و اثر افزایشی برای ROMI | Decimal/Pandas: margin، CAC، LTV افق ثابت، ROMI طبق قرارداد | PyMC-Marketing 1.5.0 BG/NBD و Gamma-Gamma برای مشتریان غیرقراردادی با داده تکرار خرید؛ مدل قراردادی برای اشتراک؛ holdout زمانی و posterior checks | 10000−6000=4000؛ 2000/20=100؛ (1500−500)/500=2؛ مخرج صفر null | فقط شاخص‌های دارای داده؛ LTV مشاهده‌ای/سناریو |
| B02 | قیمت/هزینه و افق؛ سری منظم زمانی برای پیش‌بینی؛ پنجره آزمون؛ کشش نیازمند شناسایی | Decimal سربه‌سر؛ StatsForecast 2.1.1 Naive/SeasonalNaive به‌عنوان benchmark، AutoETS/AutoARIMA و Croston برای تقاضای متناوب؛ Statsmodels SARIMAX/ETS جایگزین کلاسیک؛ rolling origin | Chronos-2 فقط challenger؛ Statsmodels رگرسیون قیمت، DoWhy/B04 برای استنتاج علّی | 100−60=40، هزینه ثابت 4000 → 100 واحد؛ سری ثابت 10 → naive=10 و MAE=0؛ حاشیه ≤0 → بدون سربه‌سر | سناریوی قیمت و حجم؛ بدون ادعای کشش علّی |
| B03 | رویداد با شناسه مشتری/مرحله/زمان، پنجره و تعریف churn؛ مدل به رخداد کافی در هر دو کلاس نیاز دارد | Pandas cohort funnel/retention؛ sklearn LogisticRegression به‌عنوان مدل پایه با جداسازی زمانی | CatBoost challenger؛ SHAP فقط توضیح مدل نه علت؛ calibration و PR-AUC/هزینه خطا | 100 واجد شرایط، 40 رسیده، رویداد تکراری → 40%؛ 10 ریزش از 100 فعال → 10% | قیف تجمیعی فقط با مخرج معتبر؛ بدون مدل پیش‌بینی |
| B04 | فرضیه، واحد تخصیص، متریک، MDE، alpha، power، نرخ پایه/واریانس؛ داده واقعی برای اثر | Statsmodels 0.15.0 power و CI؛ SciPy Welch برای متریک پیوسته؛ statsmodels proportion APIs برای نرخ‌ها؛ RCT دوگروهی | DoWhy 0.14 برای DAG/identification/refutation؛ EconML 0.17.1 برای DML/CATE فقط با overlap و فرض‌های مخدوش‌گر مستند؛ MMM در E03 | کنترل 20/100 و درمان 30/100 → RD=.10؛ بدون طرح تصادفی معتبر، causal_claim=false؛ بدون داده فقط protocol | تحلیل توصیفی/طرح آزمایش؛ عدم ادعای علت |
| B05 | تعریف KPI، داده، دانه‌بندی و دوره؛ هدف اختیاری | Pandas groupby و Decimal برای پول؛ روند و انحراف؛ ECharts فقط نمایش | Polars یا DuckDB بعد از benchmark بر داده حجیم؛ کنترل ناهنجاری با خط پایه معتبر | actual=70,target=100 → -30؛ target=null → deviation=null؛ صفر معتبر حفظ | گزارش مشاهده‌ای و نقص داده |
| B06 | گزینه، هزینه، بازده/حاشیه مستند، ظرفیت؛ قیود و تابع هدف | NumPy امتیازدهی؛ SciPy linprog/milp HiGHS در حالت مدل خطی معتبر | تحلیل حساسیت؛ OR-Tools برای قیود گسسته پیچیده فقط در نیاز | max 3x+2y، x+y≤4، x≤2، x,y≥0 → x=2,y=2,obj=10؛ ناممکن → infeasible | مقایسه گزینه یا طرح جمع‌آوری بازده؛ بدون بهینه ساختگی |
| E01 | تصمیم تأییدشده، کارها، بودجه، ظرفیت، موعد | WBS، جمع Decimal، کنترل قیود، زمان‌بندی ساده | SciPy milp یا OR-Tools CP-SAT برای زمان‌بندی گسسته در صورت نیاز | دو کار 60 و 50، بودجه 100 → violation=10؛ تصمیم draft → برنامه غیرقابل اجرا | پیش‌نویس یا درخواست اصلاح قیود |
| E02 | هدف، مخاطب، جایگاه، کانال، شواهد ادعا | قالب IMC/brief اختصاصی + AI با schema و مرور انسان | آزمون محتوا B04؛ بدون ابزار انتشار خودکار | ادعای فاقد ref در بریف → پرچم unverified، publication_ready=false | قالب بدون AI و فهرست ادعاهای نیازمند بررسی |
| E03 | بودجه، کانال، قید و شواهد عملکرد؛ مدل پاسخ معتبر برای بهینه‌سازی | Decimal بودجه؛ SciPy linprog در بازده خطی؛ طرح آزمایشی در نبود داده | PyMC-Marketing 1.5.0 به‌عنوان انتخاب اصلی؛ Meridian فقط مقایسه جدا (یکی) برای MMM با داده زمانی/جغرافیایی، کنترل confounding، اعتبارسنجی و کالیبراسیون آزمایش | بودجه 100 و تخصیص 60+50 → رد؛ داده عملکرد غایب → test_plan، نه ROI پیش‌بینی‌شده | تخصیص آزمایشی و قواعد توقف |
| E04 | مراحل، محصول، ظرفیت؛ داده مشتری مجاز و برچسب تبدیل برای مدل | قواعد SLA، RFM/Pandas، lead scoring شفاف؛ طرح چرخه عمر | sklearn LogisticRegression/CatBoost با validation زمانی، calibration و fairness؛ بدون تصمیم خودکار درباره افراد | lead بدون داده → unknown؛ opt-out → outreach_allowed=false؛ 20 ظرفیت در برابر 25 → backlog=5 | امتیاز قواعدی یا صف دستی |
| E05 | فرایند، سیستم‌ها، نیاز و محدودیت داده | نقشه فرایند اختصاصی، ماتریس requirements و کنترل مجوز | AI خلاصه مستندات؛ بدون اتوماسیون یا اتصال مستقل | سیستم A فاقد اجازه انتقال → blocked؛ نیاز فاقد شاهد → pending | چک‌لیست و ارزیابی دستی |
| E06 | کار، نقش، ظرفیت و مهارت مستند؛ مالک و قیود | RACI اختصاصی؛ تخصیص ظرفیت با قواعد؛ OPM ساختار ارزیابی | OR-Tools CP-SAT برای تخصیص گسسته، نه انتخاب/رد خودکار افراد | دو مالک accountable برای یک کار → رد؛ ظرفیت 8 و کار 10 → overload=2 | تقسیم کار دستی/اصلاح ظرفیت |
| E07 | موضوع، طرفین، منافع اظهارشده و قیود | نقشه ذی‌نفعان و گزینه توافق؛ AI پیش‌نویس با evidence refs | مرور انسانی؛ هیچ استنباط احساس/شخصیت قطعی | منافع طرف B ثبت نشده → unknown؛ هیچ عبارت ذهن‌خوانی به‌عنوان observed | راهنمای گفت‌وگو و ارجاع |
| E08 | هدف، نتیجه واقعی، تصمیم و ریسک؛ baseline برای مقایسه | Pandas/Decimal تحلیل شکاف، PDCA و ثبت اصلاح | B04 برای آزمون علّی و B05 روند؛ AI خلاصه درس‌آموخته | هدف 100، نتیجه 80 → -20؛ بدون طرح اثر، علت hypothesis؛ اقدام جدید نیازمند تأیید | مرور توصیفی یا درخواست شاهد |

## ۴. قواعد عددی و استنباطی مشترک

- محاسبات پایه همان فرمول‌های نسخه‌دار معماری و مشخصات ابزار: TAM=خریدار×تعداد خرید×قیمت؛ SAM/SOM زیرمجموعه هم‌تعریف؛ حاشیه=درآمد خالص−هزینه متغیر؛ CAC=هزینه جذب/مشتری جدید؛ LTV=مجموع حاشیه مورد انتظار هر مشتری در افق با روش تنزیل مستند در صورت نیاز؛ ROMI=(حاشیه افزایشی پیش از هزینه کمپین−هزینه کمپین)/هزینه کمپین؛ سربه‌سر=ceil(هزینه ثابت/حاشیه واحد مثبت)؛ conversion=تعداد مشتری یکتای رسیده در cohort/واجد شرایط همان cohort؛ churn=ریزش/فعال ابتدای دوره. مخرج صفر یا گمشده null. ارز، افق، دانه‌بندی، cohort و منبع هم‌تعریف.
- وزن‌دهی: جهت معیار و کران ثابت، نرمال‌سازی، جمع وزن=۱، مقایسه حساسیت؛ رتبه بدون داده مؤثر ممنوع. در بهینه‌سازی: تابع هدف و قیود، solver success، feasibility با محاسبه مستقل و gap در مدل گسسته؛ ناممکن/نامحدود به‌صراحت گزارش شود.
- پیمایش: طرح احتمالی ساده فقط در فرض SRS؛ n=ceil(z²p(1−p)/e²)، تصحیح جامعه محدود و عدم پاسخ بر حسب طرح. حجم آزمون از alpha/power/MDE و نرخ پایه/واریانس؛ طرح خوشه‌ای/وزن‌دار به بازبینی نیاز دارد. RCT دوگروهی مستقل، تحلیل intention-to-treat در صورت تناسب، اختلاف نسبت/میانگین و CI 95% پیش‌تعریف‌شده؛ کنترل آزمون متعدد. به عنوان مثال Statsmodels confint_proportions_2indep (Newcombe برای اختلاف نسبت‌ها) و SciPy ttest_ind (equal_var=False) برای Welch تحت فرض مناسب؛ API در CI بررسی شود.
- پیش‌بینی: rolling-origin با افق واقعی، حداقل ۳ پنجره ارزیابی پیشنهادی (نه قانون علمی)، MAE در واحد هدف؛ naive و seasonal-naive مبنا. مدل پیشرفته فقط با عملکرد خارج نمونه بهتر و عدم نقض calibration/ظرفیت؛ حاشیه بهبود معنادار تجاری قبل از آزمون تعیین شود. فصل‌پذیری تنها با دوره‌های کامل و کافی. مدل پایه نیز با داده ناکافی به سناریو تنزل یابد.
- ML: split زمانی/گروهی پیش از preprocessing، عدم استفاده از داده آینده یا ویژگی پس از outcome، داده آزمون دست‌نخورده، انتخاب آستانه/پارامتر تنها روی train/validation، PR-AUC برای کلاس نادر همراه نرخ پایه، calibration/Brier، هزینه خطا و بازبینی زیرگروه در صورت نمونه کافی. هیچ آستانه عمومی برای حجم داده یا accuracy؛ وجود موارد هر دو کلاس در fold و کفایت نمونه نسبت به پیچیدگی ضروری است. برای clustering، ثبات و تفسیرپذیری عملی مهم‌تر از silhouette تنهاست.
- استنتاج علّی: تعریف treatment/outcome/estimand و زمان، DAG یا طرح شناسایی مستند، بررسی confounder/overlap، فرض عدم مداخله و sensitivity متناسب. Refutation در DoWhy اثبات صحت علیت نیست. EconML فقط برای اثر ناهمگن قابل شناسایی. MMM با تاریخچه کافی، تغییرات هزینه، کنترل روند/فصل/متغیرهای مخدوشگر، holdout و posterior predictive check، کالیبراسیون آزمایش در صورت امکان؛ طول سری از پیچیدگی مدل و تنوع مؤثر تعیین می‌شود، نه عدد ثابت. گزارش predictive vs causal جدا.
- AI/NLP: داده واقعی با evidence ref؛ JSON validation؛ مدل چندزبانه ابتدا روی نمونه فارسی و اصطلاحات صنعت ارزیابی شود. تشابه برداری یا خوشه متن معادل حقیقت، شیوع یا احساس قطعی نیست. golden set با برچسب انسانی، بررسی موارد مخالف، نرخ ادعای بی‌منبع و پوشش شواهد؛ صفر ادعای observed بدون ref معتبر شرط سخت. بدون AI قالب دستی قابل استفاده باشد.
- ثبت هر run: input snapshot/hash، نسخه schema و method، کتابخانه و مدل/seed، داده/تقسیم، معیار و نتیجه پایه/پیشرفته، فرض‌ها، خطا و fallback reason؛ حفظ محرمانگی، بدون لاگ داده خام حساس.

## ۵. برنامه اثبات کارکرد و معیار پذیرش

چهار مرحله، بدون زیرساخت تست پیچیده:

| مرحله | معیار عبور | وضعیت فعلی |
|---|---|---|
| V0 مستندات | ۲۹ شناسه منطبق، روش/فناوری/شرایط/fixture/fallback برای هر ابزار | پوشش سند بررسی‌شده؛ انتخاب علمی نیازمند بازبینی تخصصی |
| V1 قابلیت نصب | resolve و نصب گروه‌ها، import/API smoke، ثبت lock و نسخه، مجوز توسعه | انجام نشده |
| V2 صحت و یکپارچگی | golden fixture هر ابزار، ورودی ناقص، ورودی ناسازگار، reproducibility، آزمون عدم نشت و خروجی بی‌شاهد؛ CI سبز | انجام نشده |
| V3 اعتبار علمی و کاربردی | مقایسه با روش پایه/محاسبه مستقل، مرور خبره، پایلوت داده واقعی مجاز با معیار پیشینی، امنیت و release gate | انجام نشده |

آزمون قطعی: Decimal دقیق تا مقیاس ارز، نرخ/float با tolerance ثبت‌شده (پیشنهاد برای fixture ساده 1e-8)، نتیجه گسسته دقیق، خوشه مستقل از نام label. آزمون AI: نه تطبیق کلمه‌به‌کلمه، بلکه schema، شاهد، پوشش و rubric از پیش نوشته‌شده. برای هر ابزار دست‌کم fixture مثبت، نقص داده و ناسازگاری؛ مدل پیشرفته علاوه بر این، مقایسه مستقل با پایه. نتیجه هر تست باید به commit، lockfile و داده fixture نسخه‌دار وصل شود. گزارش PASS فقط بعد از اجرا، FAIL و NOT_RUN آشکار.

### مسیرهای انتهابه‌انتها (داده مصنوعی)

- خدماتی: M01 سؤال و طرح تحقیق → پاسخ واقعی آزمایشیِ برچسب‌خورده → M05 بخش‌بندی → M06 جایگاه → S03 تصمیم → E01 برنامه. انتظار: شواهد در هر مرحله منتقل، انتخاب هدف و تصمیم انسان، هزینه‌ها در سقف.
- فروشگاهی: ۱۰۰ مشتری واجد شرایط، ۴۰ تبدیل، هزینه جذب ۲۰۰۰ و ۲۰ مشتری جدید → B03 conversion=.4 و B01 CAC=100 → S01 شکاف هدف/واقعی → B04 پروتکل → B05 ثبت نتیجه. انتظار: شمارش cohort صحیح، علت فرضیه و عدم ادعای اثربخشی بدون داده آزمون.
- پایپلاین جامع با M01 بدون پاسخ و B01 بدون هزینه: مراحل وابسته blocked/needs_data، شاخه مستقل ادامه، خروجی ناقص صریح؛ pause/resume بدون تکرار مرحله موفق و با workspace isolation. هیچ هزینه یا انتشار بیرونی خودکار.
- MVP همان ۸ ابزار تعریف‌شده (S01,S03,M01,M05,M06,B01,B03,E01) و ثبت KPI پایه است؛ ۲۱ ابزار دیگر در طرح کامل موجود ولی اجرا پس از ساخت/آزمون. فعال‌سازی هر روش پیشرفته مستقل از فعال‌سازی ابزار پایه.

## ۶. منابع روش‌شناختی و API

علاوه بر منابع علمی معماری مرجع (AAPOR، Magenta Book، OpenStax و FPP3)، منابع بررسی API در این بازبینی:
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html و https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html — حل خطی و mixed-integer؛ آزمون feasible/infeasible.
- https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html — clustering با noise؛ نیازمند داده مناسب.
- https://www.statsmodels.org/stable/_modules/statsmodels/stats/proportion.html — روش‌های نسبت و CI؛ انتخاب روش بر مبنای طرح.
- https://surveyjs.io/survey-creator/documentation/overview و https://surveyjs.io/form-library/documentation/overview — طراحی و رندر فرم، نه اعتبار خودکار پرسشنامه.
- https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html و https://sbert.net/docs/sentence_transformer/pretrained_models.html — embeddings/تشابه چندزبانه.
- https://pypi.org/project/statsforecast/ ، https://pypi.org/project/dowhy/ ، https://pypi.org/project/econml/ ، https://pypi.org/project/pymc-marketing/ — قابلیت خانواده مدل‌ها؛ نه اثبات صحت روی داده M-Tools.

**محدودیت نهایی:** این سند مرجع انتخاب و معیار اثبات است؛ اعتبار تجربی محصول، سازگاری دقیق نسخه‌ها و اجرای تست‌ها همچنان NOT_RUN هستند. معیارهای پذیرش پیشرفته وابسته به داده و سؤال، قبل از هر آزمایش تعیین و مستند می‌شوند. هیچ فناوری صرفاً به علت جدید بودن یا رایگان بودن اجباری نیست.


## ۷. تطبیق دقیق با مستندات رسمی و تصمیم‌های اصلاحی — ۲۴ نوامبر ۲۰۲۶

این بخش مرجع نهایی انتخاب نسخه و API است. ترتیب اعتبار: metadata نسخه منتشرشده در PyPI و فایل pyproject همان release، سپس مستندات stable/API همان نسخه، و در آخر README یا branch اصلی. مستندات قدیمی/توسعه‌ای ممکن است با metadata release اختلاف داشته باشند.

### ۷.۱ چرا Python 3.13.x انتخاب می‌شود؟

| مؤلفه | شرط رسمی/نسخه منتشرشده | نتیجه برای M-Tools |
|---|---|---|
| NumPy 2.5.5 | Python 3.12 تا 3.15 | سازگار |
| SciPy 1.18.1 | Python >=3.12؛ wheelهای 3.12 موجود | سازگار |
| pandas 2.3.3 | Python 3.13؛ NumPy >=1.23.2 | سازگار با NumPy 2.5.5 و شرط pandas<3.0 در StatsForecast |
| scikit-learn 1.9.1 | Python >=3.11؛ NumPy >=1.24.1 و SciPy >=1.10 | سازگار |
| Statsmodels 0.15.0 | wheel برای CPython 3.13؛ API stable docs | سازگار |
| DoWhy 0.14 | Python >=3.9 و <3.14؛ برای Python<3.13، SciPy<=1.15.3؛ برای Python>=3.13، SciPy>=1.15 | 3.13 با SciPy 1.18.1 سازگار؛ 3.12 با آن ناسازگار |
| EconML 0.17.1 | wheel CPython 3.13؛ scikit-learn >=1.6 و <1.10 | sklearn 1.9.1 در بازه |
| PyMC-Marketing 1.5.0 | Python >=3.12؛ PyMC >=6.0 و ArviZ >=1.2؛ NumPy <2.6 در pyproject فعلی | NumPy 2.5.5 در بازه |
| Google Meridian | فقط Python 3.11 یا 3.12؛ JAX backend پیش‌فرض | خارج از محیط اصلی 3.13؛ در صورت نیاز، worker/محیط مقایسه‌ای Python 3.12 جدا |
| StatsForecast 2.1.1 | Python >=3.11؛ pandas<3.0؛ statsmodels >=0.14.5 و SciPy >=1.7.3 | Python 3.13 + pandas 2.3.3 سازگار از نظر شروط اعلام‌شده |
| Numba 0.68.1 | Python 3.10 تا قبل از 3.16؛ NumPy 2.0 تا قبل از 2.6 | با NumPy 2.5.5 سازگار |
| DuckDB 2.0.1 | Python >=3.11؛ wheel cp312-abi3 | سازگار |
| Polars 2.1.0 | Python >=3.11 | سازگار |
| CatBoost 1.2.10 | wheelهای CPython 3.13 برای Windows/Linux/macOS | سازگار |
| Sentence Transformers | Python >=3.10، PyTorch >=1.11 و Transformers >=4.41؛ Qwen3 model نیازمند Transformers >=4.51 | 3.13 سازگار؛ وزن مدل جداگانه benchmark شود |

**تصمیم:** baseline توسعه و CI برابر CPython 3.13.x است. NumPy 2.5.5، pandas 2.3.3، SciPy 1.18.1، scikit-learn 1.9.1 و Statsmodels 0.15.0 کاندیدهای pin اولیه‌اند. DoWhy 0.14 و EconML 0.17.1 نیز در Python 3.13 قرار می‌گیرند؛ DoWhy 0.14 برای Python<3.13 سقف SciPy<=1.15.3 دارد، اما برای Python>=3.13 به SciPy>=1.15 نیاز دارد. این جدول تطبیق شروط رسمی است و هنوز جایگزین اجرای resolver و تست نصب نیست. دلیل انتخاب 3.13 نیز در CI آشکار شد: DoWhy 0.14 در Python 3.12 به SciPy<=1.15.3 محدود می‌شود و با SciPy 1.18.1 تعارض دارد؛ Python 3.13 قید متفاوت و سازگار دارد.

### ۷.۲ اصلاحات مهم در انتخاب الگوریتم و API

1. **S04/S05 — امتیازدهی، سناریو و حساسیت:** امتیاز وزنی با فرمول شفاف NumPy و grid sensitivity انجام می‌شود. شبیه‌سازی تصادفی با `numpy.random.default_rng(seed)` یا `scipy.stats.qmc` انجام می‌شود. SALib برای شاخص‌های حساسیت جهانی Sobol/Morris روی یک مدل قابل اجراست؛ SALib ابزار عمومی تولید سناریو یا جایگزین Monte Carlo نیست.
2. **M04/M08 — متن فارسی:** Sentence Transformers فقط runtime embedding است، نه تضمین کیفیت. مدل اولیه آزمایش Qwen3-Embedding-0.6B با پشتیبانی اعلام‌شده 100+ زبان و context تا 32k است؛ BGE-M3 challenger. مدل منتخب فقط پس از آزمون روی مجموعه برچسب‌خورده فارسی تثبیت می‌شود. BERTopic 0.17.4 نسخه stable موجود در PyPI است؛ 1.0.0b1 پیش‌انتشار است و در baseline استفاده نمی‌شود. خوشه/موضوع بدون مرور انسانی، یافته قطعی نیست.
3. **M05 — خوشه‌بندی:** `sklearn.cluster.HDBSCAN` از scikit-learn 1.3 به بعد داخل خود sklearn است؛ بسته مجزای `hdbscan` لازم نیست. در sklearn، `min_samples` خود نقطه را می‌شمارد و با بسته contrib از نظر مقدار یکسان نیست. KMeans با `random_state` و `n_init` صریح اجرا شود. هیچ الگوریتمی بدون داده کافی یا تفسیرپذیری تجاری به‌زور انتخاب نشود.
4. **B02 — پیش‌بینی:** StatsForecast API واقعی `StatsForecast(models=[...], freq=...)`, `fit(df)`, `predict(h=...)` یا `forecast(df=..., h=...)` و `cross_validation(...)` دارد. Naive/SeasonalNaive baseline، AutoETS/AutoARIMA گزینه‌های کلاسیک و Croston/ADIDA/TSB برای تقاضای متناوب‌اند. نسخه 2.1.1 در metadata PyPI با وضعیت Beta برچسب خورده؛ تا عبور از CI و backtest، فعال‌سازی production آن مشروط است. metadata نسخه 2.1.1 وابستگی اجباری مستقیم Numba را فهرست نمی‌کند؛ به همین دلیل Numba به‌زور به گروه forecast اضافه نمی‌شود. Chronos-2.3.2 مدل foundation challenger است؛ `Chronos2Pipeline.from_pretrained(...)` و `predict_df(...)` API رسمی دارد، اما وزن مدل، latency، CPU/GPU و دقت در داده کسب‌وکار باید جداگانه آزموده شود.
5. **B04 — آزمایش و علیت:** برای RCT نرخ‌ها از روش‌های نسبت Statsmodels و برای میانگین پیوسته Welch استفاده شود. API `confint_proportions_2indep` در مستندات 0.15.0 experimental علامت‌گذاری شده؛ نسخه روش `newcomb` صریح و regression-test شود. DoWhy جریان model → identify → estimate → refute را فراهم می‌کند؛ refutation آزمون استحکام فرض‌هاست، نه اثبات علیت. EconML برای DML/CATE فقط با overlap، تعریف treatment/outcome و فرض‌های شناسایی مناسب.
6. **B01/E03 — CLV و MMM:** PyMC-Marketing 1.5.0 یک مجموعه تخصصی بازاریابی است؛ برای CLV غیرقراردادی BG/NBD و Gamma-Gamma فقط با فرض‌های سازگار و داده RFM معتبر، برای اشتراک قراردادی مدل متناسب با قرارداد/ریزش. برای MMM، PyMC-Marketing انتخاب اول است چون MMM، CLV و budget optimization را در یک کتابخانه عرضه می‌کند. Google Meridian گزینه مقایسه‌ای است؛ به Python 3.11/3.12 و JAX backend متکی است و GPU را توصیه می‌کند. هر دو را از ابتدا هم‌زمان نصب نکنیم.
7. **B06/E01/E06 — بهینه‌سازی:** `scipy.optimize.linprog` برای LP و `scipy.optimize.milp` برای MILP خطی؛ هر دو بر HiGHS. OR-Tools CP-SAT برای تخصیص/زمان‌بندی با متغیرهای صحیح/Boolean مناسب است و همه ضرایب/قیود باید integer شوند. اگر مسئله continuous است CP-SAT انتخاب اول نیست.
8. **B03/E04 — پیش‌بینی مشتری:** LogisticRegression baseline، CatBoost challenger برای داده جدولی و دسته‌ای. split زمانی/group-aware و calibration الزامی. SHAP feature attribution است، نه causal explanation؛ Optuna فقط با validation داخلی و بدون دست‌زدن به test set.
9. **B05 — داده حجیم:** Pandas مبنا می‌ماند. Polars و DuckDB فقط پس از benchmark روی داده نماینده و بررسی null، decimal، timezone و سازگاری خروجی افزوده می‌شوند؛ پایگاه اصلی داده همچنان PostgreSQL است.

### ۷.۳ APIهای مشخصی که باید در smoke test اجرا شوند

| بخش | API واقعی | انتظار تست |
|---|---|---|
| محاسبه و قیود | `scipy.optimize.milp` | جواب optimal و infeasible را درست تشخیص دهد |
| HDBSCAN | `sklearn.cluster.HDBSCAN.fit_predict` | labels و noise را بر fixture جداشده تولید کند |
| KMeans | `sklearn.cluster.KMeans(..., random_state=..., n_init=...)` | clustering تکرارپذیر |
| A/B proportion | `statsmodels.stats.proportion.confint_proportions_2indep(..., method="newcomb")` | CI finite و شامل/حول اختلاف مشاهده‌شده |
| Forecast | `StatsForecast.fit` و `predict(h)` | تعداد سطرهای افق درست و خروجی finite |
| Causal | `CausalModel.identify_effect`, `estimate_effect`, `refute_estimate` | estimand/estimate/refutation ثبت شود |
| DML | `econml.dml.LinearDML.fit` و `effect` | شکل و مقدار خروجی معتبر |
| MMM | `pymc_marketing.mmm.MMM` با GeometricAdstock/LogisticSaturation | import و ساخت مدل؛ fit فقط با fixture و کنترل همگرایی |
| CLV | `pymc_marketing.clv.BetaGeoModel` | import، ساخت و fit روی RFM fixture سازگار |
| NLP | `SentenceTransformer("Qwen/Qwen3-Embedding-0.6B").encode` | embedding finite و benchmark فارسی؛ وزن‌ها از قبل cache شوند |
| Topic model | `BERTopic.fit_transform` | موضوع‌ها، outlier و ثبات؛ فقط corpus کافی |
| Sobol | `SALib.sample.sobol.sample` + `SALib.analyze.sobol.analyze` | indices با Ishigami test function |
| CP-SAT | `ortools.sat.python.cp_model` | status=OPTIMAL/FEASIBLE و قیود رعایت شوند |
| Analytical data | `duckdb.sql`, `polars.DataFrame` | query و aggregation نتیجه دقیق |

### ۷.۴ وضعیت اعتبارسنجی

| نوع بررسی | وضعیت |
|---|---|
| تطبیق شروط نسخه و Python از PyPI metadata | انجام شده برای اجزای اصلی |
| بررسی APIهای رسمی و نمونه‌های مستند | انجام شده برای روش‌های بالا |
| نصب همه گروه‌ها در Python 3.13 | منتظر CI |
| resolver و lockfile ترکیبی | منتظر DEV |
| اجرای smoke test API | منتظر CI |
| دانلود و آزمون وزن Qwen3/Chronos | انجام نشده؛ آزمون مدل جداگانه |
| benchmark فارسی و داده واقعی کسب‌وکار | انجام نشده |
| ارزیابی علمی مدل‌های MMM/CLV و causal روی داده واقعی | انجام نشده |

تا وقتی CI موفق نشده، هیچ ردیف را «واقعاً اجراشده و PASS» گزارش نکن. برای APIهای experimental، پیش‌انتشار، مدل‌وزن و الگوریتم‌های داده‌محور، وضعیت جداگانه نگه‌دار.

### ۷.۵ منابع رسمی بررسی‌شده

- Python 3.15 release: https://docs.python.org/3.15/whatsnew/3.15.html
- Django 6.1 Python compatibility: https://docs.djangoproject.com/en/6.1/releases/6.1/
- NumPy 2.5.5: https://numpy.org/news/ و https://pypi.org/project/numpy/2.5.5/
- pandas 2.3.3: https://pandas.pydata.org/docs/whatsnew/ و https://pandas.pydata.org/docs/getting_started/install
- SciPy 1.18.1: https://scipy.org/news/ و https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
- scikit-learn 1.9.1: https://scikit-learn.org/stable/ و https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html
- Statsmodels 0.15.0: https://www.statsmodels.org/stable/ و https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.confint_proportions_2indep.html
- StatsForecast 2.1.1: https://pypi.org/project/statsforecast/2.1.1/ و https://github.com/Nixtla/statsforecast
- DoWhy: https://pypi.org/project/dowhy/0.14/ و https://www.pywhy.org/dowhy/main/
- EconML 0.17.1: https://pypi.org/project/econml/0.17.1/ و https://github.com/py-why/EconML
- PyMC-Marketing 1.5.0: https://pypi.org/project/pymc-marketing/ و https://www.pymc-marketing.io/en/stable/
- Meridian: https://developers.google.com/meridian/docs/user-guide/installing
- Chronos-2: https://huggingface.co/amazon/chronos-2 و https://github.com/amazon-science/chronos-forecasting
- Sentence Transformers: https://sbert.net/docs/ و https://pypi.org/project/sentence-transformers/
- Qwen3 Embedding: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- BERTopic: https://bertopic.readthedocs.io/en/latest/ و https://pypi.org/project/bertopic/
- CatBoost: https://catboost.ai/docs/en/concepts/python-installation
- Numba compatibility: https://numba.readthedocs.io/en/stable/user/installing.html
- SALib: https://salib.readthedocs.io/en/stable/api.html
- OR-Tools CP-SAT: https://developers.google.com/optimization/cp/cp_solver/
- Polars: https://pypi.org/project/polars/2.1.0/
- DuckDB: https://duckdb.org/docs/current/clients/python/overview
- SurveyJS: https://surveyjs.io/form-library/documentation/overview

**جمع‌بندی:** انتخاب اصلی M-Tools اکنون بر یک پشته سازگار Python 3.13 و کتابخانه‌های تخصصی با نقش مشخص استوار است. این تطبیق، خطاهای شناخته‌شده طراحی را رفع می‌کند؛ تأیید عملی نهایی منوط به اجرای workflow سازگاری و آزمون مدل‌هاست.


### اصلاح تعارض Pandas و StatsForecast

آزمون resolver در Python 3.13 نشان داد StatsForecast 2.1.1 شرط `pandas<3.0.0` دارد. بنابراین Pandas 3.1.1 با این نسخه قابل نصب در یک محیط واحد نیست. انتخاب baseline به Pandas 2.3.3 تغییر کرد؛ این نسخه Python 3.13 و NumPy 2.5.5 را پشتیبانی می‌کند و با حداقل pandas اعلام‌شده PyMC-Marketing و DoWhy نیز سازگار است. Pandas 3.x فقط زمانی به baseline برمی‌گردد که نسخه StatsForecast انتخابی شرط آن را بردارد و CI مشترک سبز شود.
