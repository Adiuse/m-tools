# Scientific Engine & Technology Specification — M-Tools v1.5

تاریخ بازبینی روش‌شناختی و منابع رسمی: ۲۴ نوامبر ۲۰۲۶؛ نسخه 1.4. این بازبینی مستقل از CI است؛ CI فقط نصب و smoke test نرم‌افزار را می‌سنجد. مکمل [معماری فنی](marketing-system-architecture-v1.md)، [مشخصات ابزارها](marketing-tool-specifications.md) و [UX](marketing-ux-design-v1.md). سند طراحی و برنامه آزمون است؛ هیچ‌کدام از ۲۹ ابزار پیاده‌سازی یا آزمون انتهابه‌انتها نشده‌اند. نمونه‌های زیر fixture مصنوعی و خروجی مورد انتظار هستند، نه گزارش تست اجراشده. سیاست Capability-First در AGENTS.md برقرار است.

## ۱. انتخاب روش و معماری علمی

چهار موتور و ۲۹ ابزار بدون تغییر. هر ابزار از registry مشترک، یک schema ورودی/خروجی، یک روش پایه و در صورت نیاز روش پیشرفته استفاده می‌کند. سه خانواده قابلیت (محاسبه قطعی، تحلیل آماری/ML، تحلیل زبانی/تصمیم‌یار) قابلیت‌های موازی‌اند، نه سلسله‌مراتب اعتبار. AI لزوماً دقیق‌تر از فرمول نیست. وابستگی‌های پیشرفته فقط برای ابزار نیازمند آنها فعال می‌شوند.

ترتیب: کنترل داده و مجوز → انتخاب روش پایه معتبر → بررسی شرایط روش پیشرفته → مقایسه با پایه روی داده مستقل/ارزیابی انسانی → ثبت نسخه، فرض‌ها، نتیجه و عدم قطعیت → تأیید انسانی. در صورت شکست، fallback مجاز با ذکر دلیل؛ نه تغییر پنهانی روش یا جعل نتیجه. خروجی‌های observed/estimate/hypothesis/recommendation مطابق معماری مرجع. برای نتیجه مشروط، شروط صریح؛ برای داده ناکافی needs_data.

## ۲. انتخاب فناوری و سیاست نسخه

انتخاب baseline علمی برای شروع توسعه: CPython 3.12.x؛ NumPy 2.3.5، pandas 2.3.3، SciPy 1.15.3، scikit-learn 1.9.1 و Statsmodels 0.14.5 به‌عنوان candidateهای سازگار با اشتراک DoWhy 0.14، PyMC-Marketing 1.5.0 و StatsForecast 2.1.1. Google Meridian به‌دلیل تعارض ArviZ با PyMC-Marketing در محیط/worker جدا اجرا می‌شود. این baseline از روی metadata و شروط رسمی انتخاب شده و تا lockfile و اجرای مجدد resolver تأیید اجرایی نشده است. مرور پژوهش‌ها و انتخاب روش برای هر ۲۹ ابزار در [سند Evidence Review](marketing-29-tools-evidence-review.md) ثبت شده است.

| گروه | فناوری/خط نسخه هدف | وابستگی و شرایط | مرجع رسمی |
|---|---|---|---|
| هسته | Python 3.12، Decimal و stdlib | مالی دقیق؛ هیچ float برای پول به عنوان مرجع نهایی | https://docs.python.org/3/library/decimal.html |
| داده | NumPy 2.3.5، pandas 2.3.3 | در بازه NumPy<2.4 Meridian و NumPy<2.6 PyMC-Marketing؛ pandas<3 برای StatsForecast و Meridian | https://pypi.org/project/numpy/2.3.5/ ; https://pypi.org/project/pandas/2.3.3/ |
| آمار | SciPy 1.15.3، Statsmodels 0.14.5 | SciPy سقف DoWhy 0.14 در Python 3.12 را رعایت می‌کند؛ Statsmodels حداقل موردنیاز StatsForecast و Meridian را برآورده می‌کند | https://pypi.org/project/scipy/1.15.3/ ; https://pypi.org/project/statsmodels/0.14.5/ |
| ML | scikit-learn 1.9.1 | با Python 3.12، NumPy 2.3.5 و SciPy 1.15.3 و بازه EconML 0.17.1 سازگار از نظر شروط metadata | https://pypi.org/project/scikit-learn/1.9.1/ ; https://scikit-learn.org/stable/ |
| schema | Pydantic 2.x | strict validation، explicit null، JSON Schema | https://pypi.org/project/pydantic/ |
| فرم | SurveyJS Form Library + Creator، نسخه هم‌خانواده | React و بسته‌های survey-core/creator؛ مجوز توسعه و انتشار طبق سیاست | https://surveyjs.io/documentation |
| پیش‌بینی | StatsForecast 2.1.1 برای سری‌های متعدد؛ Statsmodels برای مدل‌های کلاسیک؛ Chronos-2.3.2 فقط challenger؛ بدون مدل‌وزن در runtime اصلی | StatsForecast به coreforecast و utilsforecast وابسته است؛ Numba وابستگی اجباری مستقیم نسخه 2.1.1 نیست. Chronos-forecasting 2.3.2 به torch>=2.2,<3، transformers>=4.41,<6 و accelerate>=1.1,<2 نیاز دارد | https://pypi.org/project/statsforecast/2.1.1/ ; https://pypi.org/project/chronos-forecasting/2.3.2/ ; https://github.com/amazon-science/chronos-forecasting |
| NLP | Sentence Transformers + مدل Qwen3-Embedding-0.6B به‌عنوان نامزد اول؛ BGE-M3 نامزد مقایسه؛ BERTopic 0.17.4 اختیاری | Qwen3-Embedding نیازمند transformers>=4.51 و sentence-transformers>=2.7 است؛ 100+ زبان ادعا شده اما دقت فارسی باید روی داده واقعی سنجیده شود. BERTopic 1.0.0b1 پیش‌انتشار است و baseline نیست | https://huggingface.co/Qwen/Qwen3-Embedding-0.6B ; https://huggingface.co/BAAI/bge-m3 ; https://pypi.org/project/bertopic/0.17.4/ |
| علّی | DoWhy 0.14 برای model/identify/estimate/refute؛ EconML 0.17.1 برای DML و CATE | DoWhy 0.14 در Python 3.12 به SciPy<=1.15.3 نیاز دارد؛ EconML 0.17.1 با scikit-learn 1.9.1 در بازه نسخه قرار می‌گیرد | https://pypi.org/project/dowhy/0.14/ ; https://pypi.org/project/econml/0.17.1/ ; https://www.pywhy.org/dowhy/main/ |
| بازاریابی بیزی | PyMC-Marketing 1.5.0 برای CLV و MMM سفارشی؛ Google Meridian برای MMM بسته‌بندی‌شده در worker جدا | هر دو Python 3.12 را پشتیبانی می‌کنند، اما PyMC-Marketing به ArviZ>=1.2 و Meridian به ArviZ<0.20 نیاز دارد؛ نصب در یک محیط ممکن نیست. Meridian همچنین NumPy<2.4 و pandas<3 می‌خواهد و GPU را توصیه می‌کند | https://pypi.org/project/pymc-marketing/ ; https://developers.google.com/meridian/docs/user-guide/installing |
| مدل ریزش | LogisticRegression به‌عنوان baseline؛ CatBoost 1.2.10 challenger؛ SHAP و Optuna اختیاری | CatBoost برای CPython 3.12 wheel دارد؛ SHAP سهم ویژگی در پیش‌بینی را توضیح می‌دهد نه علیت؛ Optuna فقط با validation بدون نشت داده | https://pypi.org/project/catboost/1.2.10/ ; https://shap.readthedocs.io/ ; https://optuna.readthedocs.io/ |
| حساسیت/تخصیص | NumPy/SciPy برای سناریو و Monte Carlo؛ SALib 1.6.0 فقط تحلیل حساسیت سراسری Sobol/Morris؛ SciPy HiGHS برای LP/MILP؛ OR-Tools CP-SAT برای زمان‌بندی/قیود صحیح | CP-SAT فقط ضرایب صحیح می‌پذیرد؛ SciPy milp یک wrapper بر HiGHS است؛ SALib جایگزین شبیه‌سازی عمومی Monte Carlo نیست | https://pypi.org/project/SALib/1.6.0/ ; https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html ; https://developers.google.com/optimization/cp/cp_solver/ |
| حجم بالا | Pandas ابزار پیش‌فرض؛ Polars 2.1.0 و DuckDB 2.0.1 فقط در صورت benchmark مثبت | Polars برای پردازش DataFrame؛ DuckDB برای SQL تحلیلی روی فایل/Parquet؛ هیچ‌کدام جای PostgreSQL منبع حقیقت نیستند | https://pypi.org/project/polars/2.1.0/ ; https://pypi.org/project/duckdb/2.0.1/ |
| AI | adapter اختصاصی JSON Schema؛ مدل منتخب با نسخه ثابت | ارائه‌دهنده/مدل بعد از benchmark فارسی، هزینه، latency، privacy؛ بدون عامل مستقل | سیاست AI معماری و NIST AI RMF |

نسخه‌ها و بازه‌های کلیدی با مستندات رسمی و metadata انتشار تطبیق داده شده‌اند. این تطبیق استاتیک است، نه نتیجه نصب و اجرای یک محیط واقعی. نسخه‌های فوق candidateهای تثبیت در lockfile هستند؛ فقط پس از resolver و smoke test در Python 3.12 به‌عنوان stack تأییدشده شناخته می‌شوند. به‌روزرسانی امنیتی و سازگاری مقدم بر انتخاب شماره نسخه بزرگ‌تر است.

### قرارداد تثبیت وابستگی

در آغاز DEV: pyproject.toml و uv.lock، نسخه Python و platform هدف، lockfile frontend، نسخه solver و مدل/وزن/پرامپت. گروه core کوچک، extras مجزا forecast/nlp/causal/bayesian/optimization؛ هر گروه مورد نیاز با هسته و گروه‌های هم‌زمان لازم resolve/install شود. آزمون import و API smoke، تست fixture، pip/uv dependency check یا معادل، گزارش امنیت و SBOM/رجیستری مجوز. اگر ترکیب ناممکن بود، نسخه سازگار یا جایگزین مجاز و دلیل ثبت شود؛ سرویس مستقل فقط در صورت ضرورت اثبات‌شده. هیچ lockfile در این PR ساخته نشده؛ مرحله DEV مسئول آن است. برای مجوز توسعه و release gate به AGENTS.md مراجعه شود.

## ۳. مشخصات علمی و فناوری ۲۹ ابزار

فیلدهای دقیق سطح معماری در سند معماری فنی، ورودی/خروجی این جدول مکمل آنهاست. حداقل داده تابع سؤال و مدل است؛ هیچ عدد عمومی برای کفایت علمی همه مسائل وجود ندارد. نمونه کوچک زیر صرفاً golden fixture برای کنترل رفتار کد است. روش پیشرفته در MVP الزام اجرا نیست.

| ID | داده و پیش‌شرط | روش پایه و پیاده‌سازی | روش پیشرفته مشروط | تست مرجع (ورودی → انتظار) | fallback |
|---|---|---|---|---|---|
| S01 | هدف، مشاهده هم‌تعریف، شواهد؛ حداقل یک جفت هدف/واقعی برای شکاف | Decimal؛ درخت مسئله اختصاصی، فرضیه‌های رقیب و شواهد مخالف | DoWhy فقط در B04 برای آزمون علّی قابل شناسایی؛ AI برای استخراج فرضیه | هدف 100، واقعی 70 → gap=-30؛ علت بدون شاهد hypothesis | نبود جفت معتبر: تعریف مسئله/جمع‌آوری داده |
| S02 | محصول، مشتری، مدل درآمد و هزینه؛ شواهد رقبا برای مزیت | بوم اختصاصی ۹ بخش؛ VRIO به‌صورت rubric مستند؛ ارزیابی انسان | AI ساختاردهی شواهد؛ بدون مدل ML مستقل | فروش اشتراکی ثبت شده، رقبا نامعلوم → revenue_model=subscription، advantage=unknown | بوم ناقص و فرضیه آزمون |
| S03 | هدف، مسئله، دست‌کم دو گزینه یا توضیح تک‌گزینه، قیود | فیلتر قیود سخت، مقایسه گزینه و trade-off؛ انتخاب انسانی | S04 برای امتیازدهی؛ AI فقط پیشنهاد مستند | بودجه 100، گزینه A هزینه 120، B هزینه 80 → A نامجاز؛ B نیازمند تأیید | کمبود گزینه: طرح تولید و آزمون گزینه |
| S04 | حداقل دو گزینه و معیارهای قابل مقایسه، جهت/مقیاس/وزن و قیود سخت | NumPy برای weighted-sum شفاف و sensitivity؛ pymcdm 1.4.0 برای TOPSIS/VIKOR/PROMETHEE در روش‌های پیشرفته؛ وزن‌دهی با مدیر و مستند | SALib فقط برای sensitivity مدل عددی؛ نه جایگزین MCDA؛ تحلیل پایداری رتبه اجباری | A=(.8,.2)، B=(.4,.9)، w=(.6,.4) → .56 و .60؛ با w=(.8,.2) → .68 و .50 | معیار مفقود مؤثر: بدون رتبه قطعی |
| S05 | پایه و پارامترها/دامنه سناریو؛ توزیع مشترک و وابستگی پارامترها برای شبیه‌سازی | Decimal/NumPy: سناریوی کم/پایه/زیاد و تغییر یک پارامتر | NumPy Generator برای Monte Carlo؛ scipy.stats.qmc برای quasi-Monte Carlo؛ SALib Sobol برای حساسیت جهانی با ورودی‌های مستقل و دامنه معتبر؛ ورودی‌های وابسته نیازمند روش مناسب وابستگی | قیمت 5 و حجم 8/10/12 → درآمد 40/50/60؛ توزیع نامعلوم → بدون احتمال | سناریوی قطعی یا کیفی |
| S06 | محصول، ICP/بخش، هدف، ارزش پیشنهادی، کانال، مدل فروش و ظرفیت؛ اقتصاد واحد برای تصمیم مالی | بریف GTM شامل بخش/ICP، جایگاه و پیام، route-to-market، کانال، sales motion، مراحل launch و معیار سنجش؛ Ansoff فقط چارچوب انتخاب مسیر رشد است، نه جایگزین GTM؛ مقایسه ظرفیت و هزینه با B01 | AI پیشنهاد و B06/E03 برای بهینه‌سازی دارای داده | کانال هزینه 150 در سقف 100 → خارج طرح؛ CAC نامعلوم → مشروط | طرح آزمون کوچک بدون ادعای ROI |
| M01 | سؤال، جامعه هدف، frame نمونه‌گیری، روش جذب، بودجه؛ داده پاسخ اختیاری؛ n بر اساس دقت/توان و عدم پاسخ | SurveyJS Form Library/Creator برای جمع‌آوری؛ svy 0.36.0 برای طرح پیچیده، وزن‌دهی و واریانس؛ Statsmodels/SciPy برای آزمون‌های متعارف؛ Wilson فقط برای نسبت تحت SRS | برای نمونه opt-in/non-probability بدون مدل و فرض شفاف، margin of sampling error معمول گزارش نشود؛ تحلیل کیفی M04 | SRS با p=.5,z=1.96,e=.05 → n=385 پیش از تصحیح؛ بدون پاسخ فقط طرح؛ 30/100 غیرتصادفی → 30% نمونه، نه جامعه | طرح تحقیق، مصاحبه و جمع‌آوری واقعی |
| M02 | جمعیت واجد شرایط، نرخ خرید، قیمت و قلمرو؛ هم‌واحد و هم‌افق | Decimal/Pandas: bottom-up؛ برآورد top-down مستند برای کنترل متقابل | SciPy/NumPy سناریو و عدم قطعیت دارای فرض مستند | 100×2×5=1000؛ 60 خریدار قابل خدمت → SAM=600؛ 10 قابل دستیابی → SOM=100 | مخرج نامعلوم: بدون عدد؛ دامنه مستند اگر ممکن |
| M03 | بازار، رقیب و شواهد تاریخ‌دار؛ حداقل یک رقیب برای مقایسه | ماتریس ویژگی/قیمت، PESTEL/Porter به‌صورت rubric؛ Pandas + AI مستند | استخراج متنی/جست‌وجوی مجاز؛ هر ادعا به منبع | قیمت A=10 و B=null → B مجهول، نسبت قیمت null | طرح تحقیق رقبا؛ بدون سهم بازار جعلی |
| M04 | متن واقعی و شناسه شاهد؛ مصاحبه/بازخورد و زمینه؛ حداقل یک شاهد برای یک مشاهده | کدگذاری با codebook و مرور انسان؛ Sentence Transformers با Qwen3-Embedding-0.6B candidate و BGE-M3 challenger؛ گروه‌بندی پیشنهادی، نه برچسب حقیقت | BERTopic 0.17.4 فقط corpus کافی و آزمون ثبات؛ embedding مدل ثابت؛ ارزیابی فارسی با نمونه انسانی | دو متن درباره تأخیر، یک متن کیفیت؛ هر theme دارای ref واقعی؛ متن جعلی رد | کدگذاری دستی؛ بدون شاهد فقط طرح مصاحبه |
| M05 | داده مشتری/بخش، نوع متغیرها؛ برای RFM تراکنش تاریخ‌دار و شناسه؛ ML مشروط به حجم/ثبات | Pandas RFM؛ scikit-learn KMeans برای داده عددی؛ Gower distance + HDBSCAN با metric precomputed برای داده mixed؛ clustMixType/KAMILA در R فقط challenger اختیاری | ارزیابی silhouette در صورت معتبر بودن، ثبات bootstrap، تمایز عملی و اعتبار روی نمونه مستقل؛ هیچ k اجباری | RFM تاریخ مرجع و تراکنش یکتا؛ چهار نقطه (0,0),(0,1),(10,10),(10,11)، k=2 → دو جفت مستقل از شماره label؛ fixture فقط فنی | قواعد بخش‌بندی و فرضیه بازار هدف |
| M06 | بخش هدف، گزینه‌های جایگزین، منافع و شاهد؛ نقشه ادراکی نیازمند داده واقعی | STP و بیانیه ارزش؛ sklearn MDS روی ماتریس فاصله ادراکی معتبر با stress/چند شروع؛ SurveyJS برای جمع‌آوری؛ Biogeme 3.3.5 برای conjoint و discrete choice | آزمون مفهوم/پیام B04؛ انتخاب ویژگی با تحقیق | ادعای «سریع‌ترین» بدون شاهد → hypothesis؛ ماتریس فاصله نامتقارن → رد | بیانیه مشروط و طرح آزمون |
| M07 | تعریف فعال‌سازی/نگهداشت، cohort و پنجره؛ بازخورد مستقل | Pandas cohort، تکرار خرید، قیف؛ triangulation و مرور انسان | lifelines برای time-to-churn و censoring؛ هیچ امتیاز واحد PMF یا cutoff عمومی ساخته نشود | 10 واجد شرایط، 4 بازگشته در پنجره → 40%؛ cohort ناتمام حذف/علامت؛ PMF قطعی ممنوع | طرح گردآوری شواهد و آزمون |
| M08 | هویت و پیام؛ تحقیق واقعی برای ادراک، آگاهی و تداعی | ممیزی برند؛ SurveyJS+svy برای brand tracking؛ Pandas نسبت‌ها، کدگذاری انسانی + Sentence Transformers برای متن آزاد | BERTopic/مدل طبقه‌بندی فارسی فقط با ارزیابی برچسب انسانی | بدون پاسخ ادراک → perception_gap=null؛ آگاهی 20 از 50 → 40% نمونه | ممیزی هویت بدون ادعای ادراک |
| M09 | مراحل، تماس‌ها و شواهد دارای زمان؛ case ID برای مسیر فردی | نقشه سفر کیفی؛ Pandas/Polars/DuckDB برای event log و Markov transition | PM4Py برای process discovery/conformance فقط با event log معتبر؛ AI برای متن با شواهد | A→B→B duplicate event_id → A→B؛ شکایت بی‌زمان مسیر قطعی نیست | نقشه فرضی و تحقیق کیفی |
| B01 | ارز و دوره مشترک؛ درآمد/حاشیه، هزینه جذب و مشتری جدید؛ cohort و تاریخچه خرید برای LTV؛ اثر افزایشی برای ROMI | Decimal/Pandas: contribution margin، CAC با تفکیک paid/blended و هزینه‌های منظورشده، LTV در افق مشخص با تنزیل/نگهداشت مستند، ROMI افزایشی | PyMC-Marketing: BG/NBD یا Pareto/NBD برای خرید تکراری continuous/non-contractual؛ Shifted BG یا BG/BB برای contractual/discrete متناسب با داده؛ Gamma-Gamma فقط برای مشتری دارای خرید تکراری و پس از بررسی استقلال تقریبی مبلغ متوسط خرید از frequency؛ در صورت نقض فرض، مدل جایگزین؛ holdout زمانی و posterior predictive checks | 10000−6000=4000؛ 2000/20=100؛ (1500−500)/500=2؛ مخرج صفر null | فقط شاخص‌های دارای داده؛ LTV مشاهده‌ای/سناریو |
| B02 | قیمت/هزینه و افق؛ سری زمانی منظم با تناوب/فصل‌پذیری معلوم؛ پنجره آزمون؛ کشش نیازمند تغییر قیمت قابل شناسایی | Decimal سربه‌سر؛ Naive/SeasonalNaive baseline؛ StatsForecast AutoETS/AutoARIMA و خانواده Croston/ADIDA/IMAPA/TSB برای تقاضای متناوب؛ Statsmodels ETS/SARIMAX جایگزین کلاسیک؛ rolling-origin با افق واقعی | Chronos-2 فقط challenger؛ Statsmodels رگرسیون قیمت، DoWhy/B04 برای استنتاج علّی | 100−60=40، هزینه ثابت 4000 → 100 واحد؛ سری ثابت 10 → naive=10 و MAE=0؛ حاشیه ≤0 → بدون سربه‌سر | سناریوی قیمت و حجم؛ بدون ادعای کشش علّی |
| B03 | رویداد با شناسه مشتری/مرحله/زمان، پنجره و تعریف churn؛ مدل به رخداد کافی در هر دو کلاس نیاز دارد | Pandas cohort funnel/retention؛ sklearn LogisticRegression به‌عنوان مدل پایه با جداسازی زمانی | CatBoost challenger؛ lifelines برای زمان تا churn؛ SHAP فقط توضیح مدل نه علت؛ calibration و PR-AUC/هزینه خطا | 100 واجد شرایط، 40 رسیده، رویداد تکراری → 40%؛ 10 ریزش از 100 فعال → 10% | قیف تجمیعی فقط با مخرج معتبر؛ بدون مدل پیش‌بینی |
| B04 | فرضیه، واحد تخصیص، متریک، MDE، alpha، power، نرخ پایه/واریانس؛ داده واقعی برای اثر | Statsmodels 0.14.5 power و CI؛ SciPy Welch برای متریک پیوسته؛ statsmodels proportion APIs برای نرخ‌ها؛ RCT دوگروهی | DoWhy 0.14 برای DAG/identification/refutation؛ EconML 0.17.1 برای DML/CATE فقط با overlap و فرض‌های مخدوش‌گر مستند؛ MMM در E03 | کنترل 20/100 و درمان 30/100 → RD=.10؛ بدون طرح تصادفی معتبر، causal_claim=false؛ بدون داده فقط protocol | تحلیل توصیفی/طرح آزمایش؛ عدم ادعای علت |
| B05 | تعریف KPI، داده، دانه‌بندی و دوره؛ هدف اختیاری | Pandas groupby و Decimal برای پول؛ Pandera برای schema/data quality؛ ECharts فقط نمایش | Polars و DuckDB برای حجم/SQL تحلیلی پس از benchmark؛ کنترل ناهنجاری با خط پایه معتبر | actual=70,target=100 → -30؛ target=null → deviation=null؛ صفر معتبر حفظ | گزارش مشاهده‌ای و نقص داده |
| B06 | گزینه، هزینه، بازده/حاشیه مستند، ظرفیت؛ قیود و تابع هدف | NumPy امتیازدهی؛ SciPy linprog/milp (HiGHS) فقط وقتی تابع هدف و قیود واقعاً خطی‌اند | برای بازده نزولی/تعامل گزینه‌ها، response curve یا تقریب قطعه‌ای و MILP/روش غیرخطی؛ OR-Tools برای قیود گسسته پیچیده؛ تحلیل حساسیت و feasibility مستقل | max 3x+2y، x+y≤4، x≤2، x,y≥0 → x=2,y=2,obj=10؛ ناممکن → infeasible | مقایسه گزینه یا طرح جمع‌آوری بازده؛ بدون بهینه ساختگی |
| E01 | تصمیم تأییدشده، کارها، وابستگی، بودجه، ظرفیت و موعد | WBS/CPM؛ NetworkX برای DAG و critical path؛ Decimal برای بودجه | OR-Tools CP-SAT برای resource-constrained scheduling و قیود گسسته | دو کار 60 و 50، بودجه 100 → violation=10؛ تصمیم draft → برنامه غیرقابل اجرا | پیش‌نویس یا درخواست اصلاح قیود |
| E02 | هدف، مخاطب، جایگاه، کانال، شواهد ادعا | قالب IMC/creative brief با Pydantic/JSON Schema؛ AI adapter برای draft با human review | آزمون محتوا B04؛ claim registry؛ بدون انتشار خودکار | ادعای فاقد ref در بریف → پرچم unverified، publication_ready=false | قالب بدون AI و فهرست ادعاهای نیازمند بررسی |
| E03 | بودجه، کانال، قید و شواهد عملکرد؛ تاریخچه زمانی و ترجیحاً جغرافیایی؛ تغییرات هزینه و متغیرهای مخدوش‌گر؛ مدل پاسخ معتبر | Google Meridian 2.2.1 برای MMM بسته‌بندی‌شده و budget optimization؛ در نبود داده کافی، برنامه آزمایشی/تخصیص محدود، نه ROI تخمینی | PyMC-Marketing 1.5.0 برای مدل سفارشی/CLV؛ Robyn 3.12.1 در R به‌عنوان challenger؛ کنترل DAG، prior/posterior، diagnostics، holdout، calibration آزمایش و response curves اجباری | بودجه 100 و تخصیص 60+50 → رد؛ داده عملکرد غایب → test_plan، نه ROI پیش‌بینی‌شده | تخصیص آزمایشی و قواعد توقف |
| E04 | مراحل، محصول، ظرفیت؛ داده مشتری مجاز و برچسب تبدیل برای مدل | قواعد SLA، RFM/Pandas، lead scoring شفاف؛ طرح چرخه عمر | sklearn LogisticRegression/CatBoost با validation زمانی، calibration و fairness؛ بدون تصمیم خودکار درباره افراد | lead بدون داده → unknown؛ opt-out → outreach_allowed=false؛ 20 ظرفیت در برابر 25 → backlog=5 | امتیاز قواعدی یا صف دستی |
| E05 | فرایند، سیستم‌ها، نیاز و محدودیت داده؛ event log در صورت process mining | نقشه فرایند/BPMN و ماتریس requirements؛ Pydantic/Pandera برای schema و data | PM4Py برای process discovery/conformance فقط وقتی case/activity/timestamp معتبر است | سیستم A فاقد اجازه انتقال → blocked؛ نیاز فاقد شاهد → pending | چک‌لیست و ارزیابی دستی |
| E06 | کار، نقش، ظرفیت و مهارت مستند؛ مالک و قیود | RACI/DRI و skill-capacity matrix اختصاصی؛ Pydantic برای schema | OR-Tools CP-SAT برای assignment/scheduling؛ نه رتبه‌بندی یا رد خودکار افراد | دو مالک accountable برای یک کار → رد؛ ظرفیت 8 و کار 10 → overload=2 | تقسیم کار دستی/اصلاح ظرفیت |
| E07 | موضوع، طرفین، منافع اظهارشده و قیود | نقشه ذی‌نفعان و گزینه توافق؛ AI پیش‌نویس با evidence refs | مرور انسانی؛ هیچ استنباط احساس/شخصیت قطعی | منافع طرف B ثبت نشده → unknown؛ هیچ عبارت ذهن‌خوانی به‌عنوان observed | راهنمای گفت‌وگو و ارجاع |
| E08 | هدف، نتیجه واقعی، تصمیم و ریسک؛ baseline برای مقایسه | Pandas/Statsmodels برای KPI، PDCA، کنترل روند و ثبت اصلاح | ruptures برای change-point در صورت نیاز؛ B04 برای آزمون علّی؛ AI خلاصه درس‌آموخته | هدف 100، نتیجه 80 → -20؛ بدون طرح اثر، علت hypothesis؛ اقدام جدید نیازمند تأیید | مرور توصیفی یا درخواست شاهد |

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
| V1 قابلیت نصب | resolve و نصب گروه‌ها، import/API smoke، ثبت lock و نسخه، مجوز توسعه | PASS تاریخی برای ۸ گروه و محیط ترکیبی روی Linux/Python 3.13.18؛ این اجرا baseline جدید Python 3.12 را تأیید نمی‌کند |
| V2 صحت و یکپارچگی | golden fixture هر ابزار، ورودی ناقص، ورودی ناسازگار، reproducibility، آزمون عدم نشت و خروجی بی‌شاهد؛ CI سبز | smoke/API و fixtureهای نماینده PASS؛ golden test کامل ۲۹ ابزار و آزمون‌های نشت/داده ناقص باقی است |
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

**محدودیت نهایی:** CI قبلی فقط baseline قدیمی Python 3.13 را smoke-tested کرده است؛ baseline جدید Python 3.12 و نسخه‌های پیشنهادی هنوز اجرا نشده‌اند. lockfile تولیدی، اعتبار تجربی مدل‌ها روی داده واقعی، benchmark کیفیت فارسی، fit/sampling مدل‌های MMM/CLV، اجرای Meridian 2.2.1 و پوشش end-to-end تمام ۲۹ ابزار باقی است. معیارهای پذیرش پیشرفته وابسته به داده و سؤال، قبل از هر آزمایش تعیین و مستند می‌شوند. هیچ فناوری صرفاً به علت جدید بودن یا رایگان بودن اجباری نیست.


## ۷. تطبیق دقیق با مستندات رسمی و تصمیم‌های اصلاحی — ۲۴ نوامبر ۲۰۲۶

این بخش مرجع نهایی انتخاب نسخه و API است. ترتیب اعتبار: metadata نسخه منتشرشده در PyPI و فایل pyproject همان release، سپس مستندات stable/API همان نسخه، و در آخر README یا branch اصلی. مستندات قدیمی/توسعه‌ای ممکن است با metadata release اختلاف داشته باشند.

### ۷.۱ چرا Python 3.12.x انتخاب می‌شود؟

| مؤلفه | شرط رسمی/نسخه منتشرشده | نتیجه برای M-Tools |
|---|---|---|
| CPython | Meridian installation guide، Python 3.11 یا 3.12؛ PyMC-Marketing >=3.12 | 3.12 نقطه اشتراک مستندشده |
| NumPy 2.3.5 | Meridian: >=2.0.2,<2.4؛ PyMC-Marketing 1.5.0 release: >=2.0,<2.6 | داخل هر دو بازه |
| pandas 2.3.3 | Meridian و StatsForecast: pandas<3؛ PyMC-Marketing >=2.2 | سازگار از نظر شروط اعلام‌شده |
| SciPy 1.15.3 | DoWhy 0.14 در Python<3.13: <=1.15.3؛ Meridian >=1.13.1,<2 | دقیقاً در تقاطع |
| scikit-learn 1.9.1 | EconML 0.17.1: >=1.6,<1.10 | در بازه |
| Statsmodels 0.14.5 | StatsForecast >=0.14.5؛ Meridian >=0.14.5 | حداقل رسمی مشترک |
| PyMC-Marketing 1.5.0 | Python>=3.12؛ ArviZ>=1.2؛ NumPy<2.6 | در محیط اصلی CLV/مدل سفارشی |
| Google Meridian | راهنمای نصب: Python 3.11/3.12؛ ArviZ<0.20؛ NumPy<2.4؛ pandas<3 | worker جدا به‌دلیل تعارض ArviZ با PyMC-Marketing |
| StatsForecast 2.1.1 | Python>=3.11؛ pandas<3؛ statsmodels>=0.14.5 و SciPy>=1.7.3 | در baseline پیشنهادی قرار می‌گیرد |
| EconML 0.17.1 | Python 3.12 و scikit-learn 1.9.1 در بازه metadata | سازگار از نظر شروط اعلام‌شده |
| CatBoost 1.2.10 | wheel CPython 3.12 | سازگار از نظر انتشار wheel |

**تصمیم:** baseline candidate برای DEV برابر CPython 3.12، NumPy 2.3.5، pandas 2.3.3، SciPy 1.15.3، scikit-learn 1.9.1 و Statsmodels 0.14.5 است. دلیل انتخاب SciPy 1.15.3 این است که DoWhy 0.14 در Python 3.12 سقف همین نسخه را دارد؛ دلیل انتخاب NumPy 2.3.5 نیز قرار گرفتن هم‌زمان در بازه Meridian و PyMC-Marketing است. این انتخاب static metadata resolution است و تا زمانی که CI/uv resolver در دسترس نباشد، نباید PASS اجرایی اعلام شود.

### ۷.۲ اصلاحات مهم در انتخاب الگوریتم و API

1. **S04/S05 — امتیازدهی، سناریو و حساسیت:** امتیاز وزنی با فرمول شفاف NumPy و grid sensitivity انجام می‌شود. شبیه‌سازی تصادفی با `numpy.random.default_rng(seed)` یا `scipy.stats.qmc` انجام می‌شود. SALib برای شاخص‌های حساسیت جهانی Sobol/Morris روی یک مدل قابل اجراست؛ SALib ابزار عمومی تولید سناریو یا جایگزین Monte Carlo نیست.
2. **M04/M08 — متن فارسی:** Sentence Transformers فقط runtime embedding است، نه تضمین کیفیت. مدل اولیه آزمایش Qwen3-Embedding-0.6B با پشتیبانی اعلام‌شده 100+ زبان و context تا 32k است؛ BGE-M3 challenger. مدل منتخب فقط پس از آزمون روی مجموعه برچسب‌خورده فارسی تثبیت می‌شود. BERTopic 0.17.4 نسخه stable موجود در PyPI است؛ 1.0.0b1 پیش‌انتشار است و در baseline استفاده نمی‌شود. خوشه/موضوع بدون مرور انسانی، یافته قطعی نیست.
3. **M05 — خوشه‌بندی:** `sklearn.cluster.HDBSCAN` از scikit-learn 1.3 به بعد داخل خود sklearn است؛ بسته مجزای `hdbscan` لازم نیست. در sklearn، `min_samples` خود نقطه را می‌شمارد و با بسته contrib از نظر مقدار یکسان نیست. KMeans با `random_state` و `n_init` صریح اجرا شود. هیچ الگوریتمی بدون داده کافی یا تفسیرپذیری تجاری به‌زور انتخاب نشود.
4. **B02 — پیش‌بینی:** StatsForecast API واقعی `StatsForecast(models=[...], freq=...)`, `fit(df)`, `predict(h=...)` یا `forecast(df=..., h=...)` و `cross_validation(...)` دارد. Naive/SeasonalNaive baseline، AutoETS/AutoARIMA گزینه‌های کلاسیک و Croston/ADIDA/TSB برای تقاضای متناوب‌اند. نسخه 2.1.1 در metadata PyPI با وضعیت Beta برچسب خورده؛ CI نصب و API smoke را PASS کرده؛ فعال‌سازی production همچنان مشروط به backtest خارج از نمونه و مقایسه با baseline است. metadata نسخه 2.1.1 وابستگی اجباری مستقیم Numba را فهرست نمی‌کند؛ به همین دلیل Numba به‌زور به گروه forecast اضافه نمی‌شود. Chronos-2.3.2 مدل foundation challenger است؛ `Chronos2Pipeline.from_pretrained(...)` و `predict_df(...)` API رسمی دارد، اما وزن مدل، latency، CPU/GPU و دقت در داده کسب‌وکار باید جداگانه آزموده شود.
5. **B04 — آزمایش و علیت:** برای RCT نرخ‌ها از روش‌های نسبت Statsmodels و برای میانگین پیوسته Welch استفاده شود. API `confint_proportions_2indep` در مستندات 0.15.0 experimental علامت‌گذاری شده؛ نسخه روش `newcomb` صریح و regression-test شود. DoWhy جریان model → identify → estimate → refute را فراهم می‌کند؛ refutation آزمون استحکام فرض‌هاست، نه اثبات علیت. EconML برای DML/CATE فقط با overlap، تعریف treatment/outcome و فرض‌های شناسایی مناسب.
6. **B01/E03 — CLV و MMM:** PyMC-Marketing 1.5.0 برای CLV غیرقراردادی BG/NBD/Pareto-NBD و Gamma-Gamma فقط با فرض‌های سازگار مناسب است؛ Gamma-Gamma نیازمند خرید تکراری و نبود رابطه مهم میان frequency و متوسط monetary value است. برای اشتراک قراردادی Shifted BG/BG-BB یا مدل بقا متناسب با دوره تمدید. در E03، Meridian 2.2.1 انتخاب اول MMM بسته‌بندی‌شده و budget optimization است؛ PyMC-Marketing برای مدل سفارشی challenger است. Meridian و PyMC-Marketing به‌دلیل تعارض ArviZ در یک environment مشترک نصب نمی‌شوند؛ worker جدا لازم است.
7. **B06/E01/E06 — بهینه‌سازی:** `scipy.optimize.linprog` برای LP و `scipy.optimize.milp` برای MILP خطی؛ هر دو بر HiGHS. OR-Tools CP-SAT برای تخصیص/زمان‌بندی با متغیرهای صحیح/Boolean مناسب است و همه ضرایب/قیود باید integer شوند. اگر مسئله continuous است CP-SAT انتخاب اول نیست.
8. **B03/E04 — پیش‌بینی مشتری:** LogisticRegression baseline، CatBoost challenger برای داده جدولی و دسته‌ای. split زمانی/group-aware و calibration الزامی. SHAP feature attribution است، نه causal explanation؛ Optuna فقط با validation داخلی و بدون دست‌زدن به test set.
9. **B05 — داده حجیم:** Pandas مبنا می‌ماند. Polars و DuckDB فقط پس از benchmark روی داده نماینده و بررسی null، decimal، timezone و سازگاری خروجی افزوده می‌شوند؛ پایگاه اصلی داده همچنان PostgreSQL است.

### ۷.۳ APIهای پوشش‌داده‌شده در smoke test

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
| NLP | `SentenceTransformer("Qwen/Qwen3-Embedding-0.6B").encode` | embedding finite و benchmark فارسی؛ وزن‌ها cache شوند؛ کیفیت فارسی با benchmark انسانی سنجیده شود |
| Topic model | `BERTopic.fit_transform` | موضوع‌ها، outlier و ثبات؛ فقط corpus کافی |
| Sobol | `SALib.sample.sobol.sample` + `SALib.analyze.sobol.analyze` | indices با Ishigami test function |
| CP-SAT | `ortools.sat.python.cp_model` | status=OPTIMAL/FEASIBLE و قیود رعایت شوند |
| Analytical data | `duckdb.sql`, `polars.DataFrame` | query و aggregation نتیجه دقیق |

### ۷.۴ وضعیت اعتبارسنجی

| نوع بررسی | وضعیت |
|---|---|
| تطبیق شروط نسخه و Python از PyPI metadata | انجام شده برای اجزای اصلی |
| بررسی APIهای رسمی و نمونه‌های مستند | انجام شده برای روش‌های بالا |
| نصب جداگانه ۸ گروه علمی در Python 3.13 | PASS؛ ۸ از ۸ |
| نصب ترکیبی همه وابستگی‌های منتخب + pip check | PASS؛ بدون تعارض اعلام‌شده در محیط Linux/Python 3.13 |
| smoke test ترکیبی APIها و fixtureهای نماینده | PASS؛ شامل هسته، forecast، causal، Bayesian import، optimization، analytics، ML و NLP import |
| دانلود وزن Qwen3-Embedding-0.6B و تولید embedding فارسی روی CPU | PASS؛ خروجی ۳ متن با ابعاد (3, 1024). کیفیت معنایی هنوز benchmark نشده؛ Chronos-2 و Meridian اجرا نشده‌اند |
| benchmark فارسی و داده واقعی کسب‌وکار | انجام نشده |
| ارزیابی علمی مدل‌های MMM/CLV و causal روی داده واقعی | انجام نشده |

آخرین CI موفق در commit `ceb1d861ecbe9e94709e01b4329171cbdbdbb71f` روی Linux و CPython 3.13.18، ۹ job از ۹ job را PASS کرده است: ۸ گروه مجزا و یک محیط ترکیبی. در محیط ترکیبی، نصب همه وابستگی‌های منتخب، `pip check` و اجرای smoke suiteهای نماینده موفق بوده‌اند. job NLP نیز وزن Qwen3-Embedding-0.6B را دانلود و برای سه جمله فارسی embedding با ابعاد `(3, 1024)` تولید کرده است. این نتیجه سازگاری نصب/API و fixtureهای نماینده را ثابت می‌کند؛ نه اعتبار علمی روی داده واقعی، کیفیت معنایی فارسی، اجرای end-to-end تمام ۲۹ ابزار یا fit/sampling مدل‌های Bayesian.

### ۷.۵ منابع رسمی بررسی‌شده

- Python 3.15 release: https://docs.python.org/3.15/whatsnew/3.15.html
- Django 6.1 Python compatibility: https://docs.djangoproject.com/en/6.1/releases/6.1/
- NumPy 2.3.5: https://pypi.org/project/numpy/2.3.5/ و https://numpy.org/news/
- pandas 2.3.3: https://pandas.pydata.org/docs/whatsnew/ و https://pandas.pydata.org/docs/getting_started/install
- SciPy 1.15.3: https://pypi.org/project/scipy/1.15.3/ و https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
- scikit-learn 1.9.1: https://scikit-learn.org/stable/ و https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html
- Statsmodels 0.14.5: https://pypi.org/project/statsmodels/0.14.5/ و https://www.statsmodels.org/stable/
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

**جمع‌بندی تاریخی:** پشته قبلی روی Linux/Python 3.13 به‌صورت گروهی و در محیط مشترک smoke test شد. این اجرا baseline جدید Python 3.12 را تأیید نمی‌کند. هنوز lockfile قطعی، ماتریس Windows/macOS، benchmark کیفیت معنایی فارسی، fit و posterior diagnostics مدل‌های Bayesian، backtest پیش‌بینی، و اعتبارسنجی علی/تجاری روی داده واقعی لازم‌اند.


### اصلاح تعارض Pandas و StatsForecast

آزمون resolver قبلی نشان داد StatsForecast 2.1.1 شرط pandas<3.0.0 دارد؛ بنابراین Pandas 3.x در محیط مشترک مناسب نیست. Pandas 2.3.3 حفظ می‌شود. baseline جدید Python 3.12/NumPy 2.3.5/SciPy 1.15.3 هنوز resolver/CI مجدد نگرفته و تأیید اجرایی ندارد.


### ۷.۶ نتیجه CI واقعی

- Workflow: [Scientific stack compatibility — run 45445594222](https://github.com/Adiuse/m-tools/actions/runs/45445594222)
- Commit آزموده‌شده: `ceb1d861ecbe9e94709e01b4329171cbdbdbb71f`؛ CPython 3.13.18 روی Ubuntu runner.
- نتیجه: ۹ job از ۹ job موفق (۸ گروه جداگانه + یک محیط ترکیبی). در job ترکیبی نصب تمام وابستگی‌های منتخب، `pip check` و اجرای suiteهای نماینده موفق شدند.
- Qwen3-Embedding-0.6B روی CPU بارگذاری شد و سه متن فارسی embedding با ابعاد `(3, 1024)` تولید کردند؛ benchmark کیفیت معنایی و latency/GPU هنوز لازم است.
- PyMC-Marketing فقط import و دسترسی به کلاس‌های MMM/CLV را گذراند؛ sampling و posterior diagnostics انجام نشده‌اند. BERTopic import شد، اما fit روی corpus واقعی انجام نشده است.
- این run شامل دانلود/آزمون Chronos-2 یا Google Meridian نیست؛ این دو در نقش گزینه‌های اختیاری/مقایسه‌ای باقی می‌مانند.

### ۷.۷ ممیزی روش‌شناختی مستقل از CI — ۲۴ نوامبر ۲۰۲۶

این ممیزی می‌سنجد آیا روش انتخابی برای سؤال درست است؛ موفقیت CI فقط نصب و اجرای API را نشان می‌دهد و شاهد اعتبار علمی نیست.

**اصلاحات روش‌شناختی اعمال‌شده**
1. **S06/GTM:** Ansoff ماتریس مسیرهای رشد است، نه روش کامل Go-to-Market. GTM باید ICP/بخش، جایگاه و پیام، کانال، sales motion، launch و سنجش را پوشش دهد.
2. **S05/عدم قطعیت:** Monte Carlo معمولی (numpy.random.Generator) از quasi-Monte Carlo (scipy.stats.qmc) جدا شد. Sobol کلاسیک برای ورودی‌های مستقل مناسب است؛ وابستگی ورودی‌ها باید مدل شود و شاخص حساسیت متناسب انتخاب شود.
3. **M01/پیمایش:** Wilson فقط برای نسبت تحت فرض طرح ساده مناسب است. برای طرح طبقه‌ای/خوشه‌ای/وزن‌دار باید واریانس و design effect مطابق طرح محاسبه شود. برای نمونه opt-in و غیر احتمالی، margin of sampling error معمولی نباید بدون مدل و فرض‌های صریح گزارش شود.
4. **M05/بخش‌بندی:** KMeans برای داده عددی مقیاس‌بندی‌شده و خوشه‌های نسبتاً فشرده است؛ روش پیش‌فرض برای داده مختلط/دسته‌ای نیست. HDBSCAN گزینه چگالی‌محور و دارای برچسب نویز است، نه راه‌حل عمومی برای هر داده.
5. **M06/جایگاه‌یابی:** MDS فقط وقتی معنا دارد که ماتریس فاصله/عدم‌شباهت از ادراک واقعی مخاطبان یا داده معتبر ساخته شده باشد. stress، چند initialization و seed ثبت شوند؛ نمودار بدون این کنترل‌ها شاهد جایگاه برند نیست.
6. **B01/CLV:** BG/NBD و Pareto/NBD برای خریدهای تکراری غیرقراردادی در زمان پیوسته‌اند؛ مدل‌های contractual/discrete مانند Shifted BG یا BG/BB برای اشتراک و تمدید دوره‌ای مناسب‌ترند. Gamma-Gamma فقط با حداقل یک خرید تکراری و استقلال تقریبی متوسط ارزش خرید از frequency استفاده شود. برای CAC، ارزش مشتری بر مبنای contribution margin از درآمد ناخالص مناسب‌تر است.
7. **B02/Forecast:** StatsForecast 2.1.1 در PyPI با Development Status = Beta منتشر شده است. قابلیت‌های آن مفیدند، اما این نسخه صرفاً به دلیل سرعت یا PASS نصب نباید baseline تولید تلقی شود. Naive/SeasonalNaive و Statsmodels ETS/SARIMAX باید baselineهای مستقل بمانند؛ انتخاب نهایی با rolling-origin backtest و پایداری نسخه انجام شود.
8. **B06/E03/Optimization و MMM:** LP/MILP فقط وقتی درست است که تابع هدف و قیود خطی باشند؛ بازده نزولی رسانه نیازمند response curve/تقریب قطعه‌ای یا مدل غیرخطی است. MMM از داده مشاهده‌ای اثر علّی را فقط تحت فرض‌های شناسایی (به‌ویژه کنترل confounders) تخمین می‌زند؛ fit پیش‌بینی خوب به‌تنهایی صحت ROI را ثابت نمی‌کند. Meridian 2.2.1 انتخاب بسته‌بندی‌شده؛ PyMC-Marketing 1.5.0 مدل سفارشی؛ Robyn R challenger است.

**نتیجه ممیزی:** معماری کلی و تفکیک محاسبه قطعی، آمار/ML، شواهد و قضاوت انسانی درست است؛ اما «۲۹ الگوریتم قطعی و آماده» نداریم. تعدادی از ابزارها چارچوب تصمیم و rubric هستند و باید همین‌طور باقی بمانند. روش‌های پیشرفته فقط وقتی فعال شوند که پیش‌شرط داده و فرض‌هایشان برقرار باشد.

**مواردی که همچنان باید در توسعه/پایلوت اثبات شوند:** حجم و کیفیت نمونه برای هر تحقیق؛ اعتبار/ثبات خوشه‌ها؛ اعتبارسنجی پیش‌بینی روی چند پنجره و چند کسب‌وکار؛ fit، convergence و posterior predictive checks برای CLV/MMM؛ مقایسه MMM با آزمایش دارای estimand سازگار؛ کالیبراسیون و fairness مدل lead scoring؛ و آزمون‌های مستقل فرمول‌ها و قیود هر ۲۹ ابزار.

**منابع رسمی افزوده‌شده به ممیزی**
- PyMC-Marketing CLV Quickstart (نوع مدل‌ها و پیش‌شرط BG/NBD/Gamma-Gamma): https://www.pymc-marketing.io/en/stable/notebooks/clv/clv_quickstart.html
- Google Meridian — causal assumptions of MMM: https://developers.google.com/meridian/docs/causal-inference/about-mmm-causal-inference-methodology
- Google Meridian — model fit and causal interpretation: https://developers.google.com/meridian/docs/post-modeling/model-fit
- AAPOR — disclosure standards for probability/non-probability samples and design effects: https://aapor.org/standards-and-ethics/disclosure-standards/
- scikit-learn — MDS, dissimilarity and stress: https://scikit-learn.org/stable/modules/manifold.html
- scikit-learn — HDBSCAN: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html
- StatsForecast 2.1.1 — release metadata and development status: https://pypi.org/project/statsforecast/2.1.1/
- Forecasting: Principles and Practice — rolling-origin evaluation: https://otexts.com/fpp3/tscv.html


## ۸. پیوند به مرور پژوهش ۲۹ ابزار

روش‌شناسی، پژوهش‌های داوری‌شده، بنچمارک‌ها، انتخاب کتابخانه و محدودیت هر ۲۹ ابزار در [marketing-29-tools-evidence-review.md](marketing-29-tools-evidence-review.md) ثبت شده است. این سند برای انتخاب الگوریتم و شواهد، مرجع مکمل و لازم‌الاجراست؛ این سند حاضر برای API، وابستگی، baseline و قرارداد فنی موتور علمی مرجع است.


## مصرف موتور علمی در کتابخانه استراتژی
[Strategy Library](marketing-strategy-library.md) مسیرهای کاربردی ۲۶ استراتژی بر ۲۹ ابزار را تعریف می‌کند. روش‌ها و وابستگی‌ها از همین قرارداد علمی و [مرور شواهد](marketing-29-tools-evidence-review.md) reuse می‌شوند؛ recipeها الگوریتم یا runtime تازه نیستند. KPI و قواعد مالی/causal از B01–B06 و قیود مدل از موتور مشترک. هیچ هدف یا نرخ جهانی، اثر علّی از attribution، رتبه قطعی با داده ناقص، یا بودجه بهینه از داده ناکافی تولید نشود. هیچ تغییر نسخه کتابخانه یا CI جدید برای این افزوده لازم نیست؛ فقط تست اتصال recipe، coverage، قیود و fixtureهای آن هنگام DEV.


## موتور علمی برنامه‌ریزی E01
[Planning Library](marketing-planning-library.md) قرارداد محاسبات CPM forward/backward، RCPSP، بودجه/تعهد/نقد، EAC، EVM اختیاری، reverse funnel، risk و rolling forecast را تکمیل می‌کند. از NetworkX (3.7 candidate) برای DAG، OR-Tools CP-SAT (9.15.6755 candidate) برای منابع محدود، SciPy linprog/milp برای هدف/قیود خطی، Decimal برای پول و B02/B03/B04/E03 برای مدل‌های تخصصی استفاده شود. metadata این دو candidate و منابع روش بررسی شده‌اند؛ lockfile و runtime تأیید نشده. CPM بدون ظرفیت، تقویم feasible نیست؛ solver status/constraint recheck الزامی؛ forecast مجوز بودجه نیست. هیچ تغییر در baseline علمی و وابستگی خارج معماری لازم نیست. fixtureهای محدود سند در DEV، بدون CI جدید در این مرحله.
