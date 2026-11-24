# M-Tools — بررسی پژوهش و شواهد فناوری برای ۲۹ ابزار
نسخه 1.1 · تاریخ مرور و آخرین تطبیق: ۲۵ نوامبر ۲۰۲۶

این سند مرور پژوهش‌های داوری‌شده، مرورهای نظام‌مند و فراتحلیل‌ها، بنچمارک‌های عمومی، مستندات رسمی و metadata نسخه‌های منتشرشده است. هدف انتخاب روش و فناوری متناسب با هر ابزار است، نه جمع‌آوری نام کتابخانه‌ها.

## روش مرور و قواعد تصمیم
1. اولویت شواهد: مرور نظام‌مند/فراتحلیل و پژوهش داوری‌شده؛ سپس بنچمارک بازتولیدپذیر؛ سپس مستندات رسمی API، محدودیت‌ها و metadata؛ در نهایت راهنمای صنعتی.
2. «بهترین» بدون تعیین سؤال، داده، معیار خطا و محدودیت‌ها معنی ندارد. برای هر ابزار یک گزینه پیش‌فرض و در صورت ارزش واقعی یک challenger تعیین شده است.
3. بعضی ابزارها چارچوب مدیریتی‌اند، نه مسئله ML. برای آن‌ها ساخت الگوریتم یا افزودن کتابخانه تخصصی ارزش علمی ایجاد نمی‌کند.
4. روش پیشرفته فقط با برقراری پیش‌شرط داده و فرض‌های آن فعال می‌شود؛ در غیر این صورت روش پایه، طرح تحقیق یا خروجی مشروط.
5. امتیاز silhouette، AUC، R² یا fit خوب به‌تنهایی اثبات نمی‌کند که تصمیم بازاریابی سودآور یا علّی است.
6. انتخاب فنی مستقل از مجوز است. هیچ قابلیت صرفاً به دلیل مجوز یا هزینه از طراحی حذف نشده؛ بررسی حقوقی و مجوز در release gate انجام می‌شود. محدودیت مجوز فعلی باید رعایت شود و این سند مجوز استفاده ایجاد نمی‌کند.

## خلاصه انتخاب فناوری
| حوزه | انتخاب اصلی | گزینه مشروط / challenger |
|---|---|---|
| استراتژی و حل مسئله | منطق اختصاصی شفاف، Pydantic، NumPy/Decimal | pymcdm برای MCDA؛ DoWhy فقط برای سؤال علّی |
| بازار و مشتری | SurveyJS، svy، Pandas، Qwen3 Embedding، scikit-learn | Biogeme، BERTopic، clustMixType/KAMILA، lifelines، PM4Py |
| تحلیل تجاری | Decimal، Pandas، Statsmodels، scikit-learn | PyMC-Marketing، StatsForecast، DoWhy/EconML، CatBoost |
| مدیریت و اجرا | Pydantic، NetworkX، OR-Tools، Pandera | Meridian/Robyn برای MMM، PM4Py، ruptures |

---

## حوزه اول — استراتژی و حل مسئله

### S01 — تشخیص مسئله
**روش:** صورت‌بندی مسئله با هدف و متریک، مقایسه وضعیت واقعی با هدف، درخت مسئله/issue tree، ثبت فرضیه‌های رقیب و شواهد موافق/مخالف. «علت ریشه‌ای» تا وقتی طراحی شناسایی علّی و داده مناسب وجود ندارد، فقط فرضیه است.

**فناوری:** Decimal/NumPy برای محاسبه شکاف؛ Pydantic برای ثبت مسئله، شواهد، فرضیه و مالک؛ AI فقط برای پیشنهاد فرضیه و خلاصه‌سازی منابع، نه صدور علت قطعی. DoWhy در B04 استفاده می‌شود، نه برای تشخیص علّی خودکار.

**دلیل و شواهد:** issue tree روش ساختاردهی فکر است، نه الگوریتمی با winner benchmark. روش‌های causal inference نیز بدون DAG، estimand و فرض‌های شناسایی از همبستگی علت نمی‌سازند. [DoWhy — causal model, identify, estimate, refute](https://www.pywhy.org/dowhy/main/user_guide/intro.html)؛ [DoWhy v0.14](https://github.com/py-why/dowhy/releases/tag/v0.14).

### S02 — مدل کسب‌وکار
**روش:** Business Model Canvas برای توصیف مدل؛ VRIO برای ارزیابی منابع/قابلیت‌ها؛ اتصال هر خانه به فرضیه، شاهد، مالک و تاریخ بازبینی. بوم خروجی یک کارگاه یک‌باره نیست و باید در چرخه یادگیری به‌روز شود.

**فناوری:** schema اختصاصی و Pydantic؛ ML یا کتابخانه محاسباتی خاص لازم نیست. AI می‌تواند تناقض‌ها و خانه‌های خالی را علامت بزند، اما ارزش، کمیابی یا تقلیدناپذیری منبع را اثبات نمی‌کند.

**دلیل و شواهد:** مرور دامنه‌ای ۲۰۲۶ روی ۱۲۵ مطالعه BMC چهار مرحله آماده‌سازی، تسهیل، تکرار و اعتبارسنجی را برجسته می‌کند؛ ضعف‌های رایج شامل مالکیت پراکنده، بازخورد کم و مستندسازی ضعیف است. مبنای VRIO نظریه منابع بنگاه است، نه classifier. [BMC scoping review, Heliyon 2026](https://doi.org/10.1016/j.heliyon.2026.e45536)؛ [Barney, Firm Resources and Sustained Competitive Advantage (1991)](https://doi.org/10.1177/014920639101700108).

### S03 — استراتژی
**روش:** تعیین هدف و محدودیت‌های سخت، تولید حداقل دو گزینه، سنجش trade-off، انتخاب انسانی و ثبت منطق. Five Forces برای ساختار صنعت، PESTEL برای محیط کلان و Ansoff برای مسیر رشد ابزارهای مکمل‌اند؛ هیچ‌کدام به‌تنهایی موتور تولید استراتژی نیستند.

**فناوری:** قواعد شفاف و schema؛ S04 برای مقایسه چندمعیاره. AI می‌تواند گزینه و پیامد احتمالی پیشنهاد کند، ولی بدون شواهد بازار آن را تأیید نمی‌کند.

**دلیل و شواهد:** این چارچوب‌ها برای ساختاردهی تحلیل مفیدند، اما checklist بدون شواهد، اولویت‌بندی و زمینه می‌تواند سطحی بماند. [Porter, Five Competitive Forces](https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy)؛ [Using Five Forces to drive strategy (2024)](https://doi.org/10.1002/joe.22250)؛ [PESTEL systematic review (2026)](https://www.sciencedirect.com/science/article/pii/S0016328726001564)؛ [Ansoff influence review (2025)](https://doi.org/10.1002/jsc.70023).

### S04 — اولویت‌بندی فرصت
**روش:** مدل ارزش افزایشی/weighted-sum شفاف به‌عنوان default: جهت هر معیار، مقیاس ارزش، وزن، قید سخت، داده مفقود و حساسیت رتبه مشخص باشد. معیارهای همبسته دوباره‌شماری نشوند. اگر جبران‌پذیری نامناسب است، از روش outranking مانند PROMETHEE استفاده شود.

**فناوری:** NumPy برای محاسبه قابل‌ردیابی؛ pymcdm 1.4.0 برای TOPSIS، VIKOR، PROMETHEE، COPRAS و روش‌های جایگزین؛ scikit-criteria 0.9 گزینه ثانویه در اکوسیستم SciPy. کتابخانه رتبه را محاسبه می‌کند، نه وزن معتبر یا ترجیح مدیر را.

**دلیل و شواهد:** روش‌های MCDA با تغییر نرمال‌سازی، وزن یا گزینه‌ها می‌توانند رتبه‌های متفاوت بدهند؛ تحلیل حساسیت و پایداری رتبه اجباری است. [PyMCDM methods](https://pymcdm.readthedocs.io/en/master/readme_link.html)؛ [PyMCDM 1.4.0](https://pypi.org/project/pymcdm/)؛ [A robust framework for benchmarking MCDA methods (Applied Soft Computing, 2026)](https://doi.org/10.1016/j.asoc.2025.114335)؛ [Fifty years of MCDA: classical methods to robust ordinal regression (EJOR, 2025)](https://doi.org/10.1016/j.ejor.2024.07.038)؛ [Entropy and normalization in MCDA: ranking stability (2026)](https://doi.org/10.3390/e28010114)؛ [Are MCDA methods benchmarkable?](https://doi.org/10.3390/sym12091549)؛ [Scikit-Criteria 0.9](https://scikit-criteria.quatrope.org/en/stable/).

### S05 — سناریو و عدم‌قطعیت
**روش:** ابتدا سناریوهای کم/پایه/زیاد با فرض‌های صریح؛ سپس Monte Carlo وقتی توزیع ورودی‌ها و وابستگی آن‌ها قابل دفاع است؛ تحلیل حساسیت برای مشخص‌کردن driverهای نتیجه. اگر توزیع نداریم، احتمال یا confidence interval ساختگی تولید نمی‌شود.

**فناوری:** NumPy Generator برای Monte Carlo؛ scipy.stats.qmc برای quasi-Monte Carlo؛ SALib برای Sobol/Morris روی مدل قابل اجرا. Sobol کلاسیک برای ورودی‌های مستقل مناسب است؛ ورودی‌های وابسته باید با مدل وابستگی مناسب مدیریت شوند.

**شواهد/مستندات:** [SciPy QMC](https://docs.scipy.org/doc/scipy/reference/stats.qmc.html)؛ [SALib](https://salib.readthedocs.io/en/stable/)؛ [Saltelli et al., Global sensitivity analysis](https://doi.org/10.1016/j.cpc.2009.09.018).

### S06 — رشد و ورود به بازار (GTM)
**روش:** بریف GTM شامل ICP/بخش، مسئله و ارزش پیشنهادی، جایگاه و پیام، کانال، sales motion، مدل درآمد، launch، ظرفیت، معیار و حلقه یادگیری. Ansoff فقط جهت رشد محصول/بازار را دسته‌بندی می‌کند و جایگزین GTM نیست.

**فناوری:** workflow و قالب‌های Pydantic؛ محاسبات اقتصادی از B01؛ اولویت کانال از B06/E03؛ تست پیام از B04. کتابخانه تخصصی GTM وجود ندارد که با چند ورودی استراتژی معتبر و آماده اجرا تولید کند.

**دلیل و شواهد:** GTM تصمیمی چندبخشی و وابسته به بازار، ظرفیت، اقتصاد و مدل فروش است. خروجی AI باید فرضیه و برنامه آزمون باشد، نه ادعای ROI. [Ansoff strategy review (2025)](https://doi.org/10.1002/jsc.70023)؛ [Porter Five Forces](https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy).

---

## حوزه دوم — بازار و مشتری

### M01 — تحقیقات بازار
**روش:** اول estimand و جامعه هدف؛ سپس frame نمونه‌گیری، روش جذب، پرسشنامه، پیش‌آزمون، اندازه نمونه، کنترل عدم پاسخ و طرح تحلیل. نمونه احتمالی و opt-in/non-probability جدا گزارش شوند. برای نمونه غیرتصادفی، margin of sampling error معمول بدون مدل و فرض‌های صریح گزارش نشود.

**فناوری:** SurveyJS Form Library/Creator برای ساخت و اجرای پرسشنامه؛ svy 0.36.0 برای طرح نمونه‌گیری پیچیده، وزن‌دهی، raking/post-stratification و واریانس طرح‌مبنا؛ SciPy/Statsmodels برای آزمون‌های متعارف. samplics در ۱۰ مارس ۲۰۲۶ archive شده و جانشین رسمی همان نگهدارنده، svy است.

**دلیل و شواهد:** SurveyJS ابزار جمع‌آوری است، نه تضمین اعتبار پرسشنامه. AAPOR بر شفافیت frame، روش نمونه‌گیری، وزن‌ها، عدم پاسخ و طراحی اثرگذار بر واریانس تأکید دارد. مستندات svy می‌گویند هسته design/weighting/variance پایدار و production-ready است، درحالی‌که API همچنان در حال تکامل است. [AAPOR Disclosure Standards](https://aapor.org/standards-and-ethics/disclosure-standards/)؛ [svy docs](https://svylab.com/docs/svy/)؛ [svy 0.36.0](https://pypi.org/project/svy/)؛ [samplics archive/migration notice](https://github.com/samplics-org/samplics)؛ [SurveyJS Form Library](https://surveyjs.io/form-library/documentation/overview)؛ [SurveyJS Creator](https://surveyjs.io/survey-creator/documentation/overview).

### M02 — اندازه بازار
**روش:** TAM/SAM/SOM با واحد، قلمرو، بازه زمانی و تعریف مشتری روشن؛ برآورد bottom-up از تعداد مشتری واجد شرایط × نرخ خرید × قیمت، و کنترل متقابل top-down با منابع معتبر. هر ورودی منبع و تاریخ داشته باشد؛ دامنه عدم‌قطعیت جدا از عدد نقطه‌ای گزارش شود.

**فناوری:** Decimal برای پول؛ Pandas برای داده و reconciliation؛ NumPy برای سناریو. کتابخانه TAM/SAM/SOM تخصصی لازم نیست.

**دلیل و شواهد:** راهنمای CGAP/World Bank توضیح می‌دهد top-down نمای کلان می‌دهد و bottom-up جزئیات بخش را؛ ترکیب و cross-check این دو خطا و سوگیری را کاهش می‌دهد. [CGAP, Gender-Smart Market Mapping (March 2025), market sizing section](https://documents1.worldbank.org/curated/en/099033125085035069/pdf/P181362-fc7fd71d-895c-41ab-8de1-485953ff6c08.pdf).

### M03 — رقبا و محیط
**روش:** ماتریس رقیب با ویژگی، قیمت، بخش هدف، پیام، کانال و تاریخ مشاهده؛ PESTEL برای عوامل کلان و Five Forces برای ساختار صنعت. برای هر گزاره منبع و درجه اطمینان نگهداری شود. سهم بازار فقط از داده قابل اتکا، نه تخمین ظاهراً دقیق AI.

**فناوری:** رجیستری منبع/URL/تاریخ/ادعا، web retrieval مجاز، Pandas برای مقایسه و AI برای استخراج اولیه با ارجاع. کتابخانه تحلیل رقبا یا الگوریتم سهم بازار عمومی انتخاب نمی‌شود.

**دلیل و شواهد:** PESTEL یک چارچوب scan است و در مرور ۲۰۲۶ به‌عنوان checklist ساده‌ای که بدون عمق تحلیلی محدود می‌شود نقد شده است. [PESTEL systematic review (2026)](https://www.sciencedirect.com/science/article/pii/S0016328726001564)؛ [Porter Five Forces](https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy).

### M04 — شناخت مشتری و تحلیل بازخورد
**روش:** codebook و thematic analysis با شاهد قابل ردیابی، کدگذاری نمونه و مرور انسانی؛ موارد مخالف و مضمون‌های نادر نیز ثبت شوند. Embedding و topic model برای کشف/گروه‌بندی، نه جایگزین تفسیر کیفی.

**فناوری:** Sentence Transformers با Qwen3-Embedding-0.6B نامزد اصلی embedding چندزبانه؛ BGE-M3 challenger؛ BERTopic 0.17.4 برای corpus بزرگ و موضوع‌یابی اکتشافی. Qwen3 فارسی را در فهرست ۱۰۰+ زبان پشتیبانی‌شده اعلام می‌کند؛ این ادعا معادل benchmark فارسی روی داده مشتری M-Tools نیست.

**دلیل و شواهد:** مرور دامنه‌ای ۲۰۲۶ از ۷۵ مطالعه LLM در پژوهش کیفی، توافق LLM و کدگذار انسانی را از ۳۶٪ تا ۹۹٪ گزارش می‌کند و ۹۷٪ مطالعات human verification داشته‌اند. خروجی مدل باید پیشنهاد کد باشد و انسان آن را تأیید کند. [LLMs in qualitative research review (2026)](https://doi.org/10.1186/s12874-026-02913-1)؛ [Qwen3 Embedding model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)؛ [Qwen3 Embedding GitHub](https://github.com/QwenLM/Qwen3-Embedding)؛ [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3)؛ [BERTopic docs](https://maartengr.github.io/BERTopic/)؛ [BERTopic paper](https://arxiv.org/abs/2203.05794).

### M05 — بخش‌بندی و هدف‌گیری
**روش:** RFM/rule-based به‌عنوان baseline قابل فهم؛ سپس الگوریتم با نوع داده انتخاب شود: K-Means برای ویژگی‌های عددی مناسب و مقیاس‌بندی‌شده؛ K-Prototypes/K-Modes برای ترکیب عددی و categorical؛ HDBSCAN برای خوشه‌های با چگالی متفاوت و noise. پایداری، اندازه بخش، قابلیت اقدام و ارزش تجاری همراه با شاخص‌های داخلی سنجیده شوند.

**فناوری:** Pandas برای RFM؛ scikit-learn KMeans/HDBSCAN برای داده عددی؛ برای داده mixed، Gower distance و HDBSCAN با metric precomputed در Python مسیر پیش‌فرض است؛ اگر benchmark داده واقعی نشان داد این روش کافی نیست، clustMixType 0.5-2 یا KAMILA 0.2.0 در R worker به‌عنوان challenger بررسی شود. بسته Python به‌نام kmodes را به‌دلیل release قدیمی و metadata کم‌اعتماد default نمی‌کنیم. Silhouette به‌تنهایی کافی نیست و برای خوشه‌های چگالی‌محور می‌تواند گمراه‌کننده باشد.

**دلیل و شواهد:** مطالعه مقایسه‌ای ۲۰۲۵ برای داده mixed نشان می‌دهد روش‌های distance-based و probabilistic بسته به نسبت ویژگی‌های عددی/دسته‌ای، هم‌پوشانی و اندازه نمونه رفتار متفاوت دارند. [Mixed-type clustering comparative study (2025)](https://doi.org/10.1155/jpas/2242100)؛ [K-prototypes initialization study (2025)](https://doi.org/10.1007/s11634-025-00639-4)؛ [scikit-learn clustering guide](https://scikit-learn.org/stable/modules/clustering.html)؛ [HDBSCAN API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html)؛ [clustMixType 0.5-2 (CRAN, 2026)](https://cran.r-project.org/web/packages/clustMixType/index.html)؛ [KAMILA 0.2.0 (CRAN, 2026)](https://cran.r-project.org/web/packages/kamila/index.html)؛ [kmodes PyPI metadata](https://pypi.org/project/kmodes/).

### M06 — جایگاه‌یابی و ارزش پیشنهادی
**روش:** STP و بیانیه جایگاه از شواهد تمایز، منافع و بخش هدف؛ نقشه ادراکی فقط از ماتریس شباهت/عدم‌شباهت پاسخ‌دهندگان واقعی؛ برای trade-off ویژگی/قیمت، conjoint/discrete choice با طراحی آزمایش و انتخاب واقعی‌تر.

**فناوری:** scikit-learn MDS با metric precomputed و گزارش stress برای نقشه ادراکی؛ SurveyJS برای جمع‌آوری؛ Biogeme 3.3.5 برای logit/nested/mixed logit و برآورد مدل‌های انتخاب گسسته. Biogeme ابزار مدل‌سازی انتخاب است، نه تولید خودکار positioning statement.

**دلیل و شواهد:** meta-analysis سال ۲۰۲۵ در conjoint نشان می‌دهد predictive validity به incentive alignment وابسته است؛ انتخاب‌های فرضی و بدون پیامد واقعی معادل رفتار خرید نیستند. [Conjoint predictive validity meta-analysis (2025)](https://doi.org/10.1007/s11002-025-09764-8)؛ [Biogeme](https://biogeme.epfl.ch/)؛ [Biogeme PyPI](https://pypi.org/project/biogeme/)؛ [scikit-learn MDS](https://scikit-learn.org/stable/modules/manifold.html).

### M07 — تناسب محصول و بازار (PMF)
**روش:** هیچ امتیاز واحد و جهان‌شمول PMF وجود ندارد. چهار سیگنال را با هم بسنجیم: فعال‌شدن در لحظه ارزش، بازگشت/نگهداشت cohort، پرداخت/تمدید/توسعه حساب، و شواهد کیفی از مسئله و ارزش. شاخص‌ها بر اساس cadence واقعی محصول تعریف شوند؛ login یا NPS به‌تنهایی PMF نیست.

**فناوری:** Pandas برای cohort/retention/funnel؛ lifelines برای time-to-churn و داده‌های censored؛ M04 برای بازخورد و B01 برای اقتصاد واحد. cohort ناتمام باید ناتمام/سانسورشده برچسب بخورد، نه ریزش قطعی.

**دلیل و شواهد:** مرور ۲۸۴ مقاله customer insights و اعتبارسنجی با مدیران، تولید، تفسیر، به‌کارگیری و tracking insight را چرخه می‌داند. پژوهش ۲۰۲۶ startup validation قدرت شواهدی پرداخت و تعهد مالی واقعی را بالاتر از صرف علاقه و ثبت‌نام می‌داند؛ آن مطالعه exploratory است و universal cutoff نیست. [Customer insights review](https://doi.org/10.1007/s11747-024-01051-8)؛ [Validate Before You Build (2026)](https://doi.org/10.3390/computers15080535)؛ [lifelines 0.30.3](https://lifelines.readthedocs.io/en/latest/).

### M08 — برند
**روش:** ترکیب آگاهی بی‌کمک/با کمک، تداعی‌ها، تمایز، کیفیت ادراک‌شده، consideration/preference، رفتار و شاخص‌های دیجیتال. Share of Search و sentiment مکمل‌اند، نه جانشین تحقیق مخاطب. هویت/پیام و ادراک واقعی جدا گزارش شوند.

**فناوری:** SurveyJS + svy برای brand tracking؛ Pandas برای سری زمانی شاخص‌ها؛ Sentence Transformers/Qwen3 برای تحلیل متن آزاد و sentiment اکتشافی؛ codebook انسانی برای تفسیر تداعی برند. کتابخانه واحدی که brand equity را به‌طور معتبر محاسبه کند وجود ندارد.

**دلیل و شواهد:** مرور نظام‌مند ۲۰۲۴ از ۲۳ مدل واجد شرایط نتیجه می‌گیرد هیچ مدل واحدی brand equity را جامع و قابل اتکا نمی‌سنجد. پژوهش ۲۰۲۵ درباره digital brand equity توصیه می‌کند سنجه‌ها فقط social media نباشند و share-of-search، awareness و sentiment را همراه ابعاد انسانی برند ببینند. [Brand equity systematic review (2024)](https://doi.org/10.1080/23311975.2024.2433168)؛ [Digital brand equity (2025)](https://doi.org/10.1016/j.jbusres.2025.115273)؛ [B2B branding systematic review (2026)](https://www.sciencedirect.com/science/article/pii/S0019850126000490).

### M09 — تجربه و سفر مشتری
**روش:** journey map کیفی برای مراحل و احساس/اصطکاک؛ در صورت وجود event log معتبر، sessionization و تحلیل توالی، transition و مسیرهای پرتکرار. مسیر واقعی و فرضی جدا برچسب بخورند؛ Markov attribution به‌تنهایی اثر علّی کانال را ثابت نمی‌کند.

**فناوری:** Pandas/Polars/DuckDB برای event logs؛ Markov chain با NumPy/SciPy برای transition؛ PM4Py برای process discovery، conformance و BPMN وقتی event log دارای case ID، activity و timestamp معتبر است؛ BERTopic/LDA فقط برای خلاصه‌سازی sessionها در corpus مناسب.

**دلیل و شواهد:** مقاله Scientific Reports در ۲۰۲۶ روشی را با topic modeling و Markov chains برای خلاصه‌سازی session و استخراج مسیرهای دیجیتال ارائه می‌کند. این evidence از تحلیل توالی پشتیبانی می‌کند، نه مدل attribution عمومی برای همه شرکت‌ها. [Digital customer journey sequential modeling (2026)](https://doi.org/10.1038/s41598-026-43762-8)؛ [Customer journey research review (2025)](https://doi.org/10.1016/j.techfore.2024.123916)؛ [PM4Py docs](https://processintelligence.solutions/pm4py/api/index.html)؛ [PM4Py software paper](https://doi.org/10.1016/j.simpa.2023.100556).

---

## حوزه سوم — تحلیل تجاری

### B01 — اقتصاد واحد و ارزش مشتری
**روش:** محاسبات قطعی با Decimal برای gross/contribution margin، CAC paid/blended، payback و ROMI افزایشی؛ LTV در افق مشخص و بر پایه contribution margin، retention و discounting. فرمول‌ها و دامنه هزینه‌های CAC باید شفاف باشند.

**فناوری:** Decimal/Pandas برای شاخص‌ها؛ PyMC-Marketing 1.5.0 برای CLV احتمالاتی: BG/NBD یا Pareto/NBD برای خرید تکراری non-contractual؛ مدل‌های contractual/discrete مانند BG/BB یا Shifted BG متناسب با دوره تمدید؛ Gamma-Gamma فقط با خریدهای تکراری و استقلال تقریبی میان frequency و monetary value. lifelines برای مدل‌های بقا/ریزش جایگزین یا مکمل.

**دلیل و شواهد:** مدل خرید تکراری غیرقراردادی را نباید به اشتراک قراردادی تعمیم داد. Gamma-Gamma فرض‌هایی درباره رابطه frequency و مبلغ خرید دارد؛ fit ظاهری یا RFM کوتاه به‌تنهایی LTV معتبر نمی‌سازد. [PyMC-Marketing CLV docs](https://www.pymc-marketing.io/en/stable/notebooks/clv/clv_quickstart.html)؛ [PyMC-Marketing 1.5.0 (released 18 Nov 2026)](https://pypi.org/project/pymc-marketing/1.5.0/)؛ [CLV under structural breaks (2024)](https://doi.org/10.1016/j.jbusres.2024.114527)؛ [lifelines](https://lifelines.readthedocs.io/en/latest/).

### B02 — قیمت‌گذاری و پیش‌بینی
**روش:** break-even و margin به‌صورت قطعی؛ price elasticity فقط با variation قابل شناسایی (ترجیحاً experiment یا quasi-experiment) و کنترل confounding؛ choice-based pricing با Biogeme در صورت طراحی انتخاب مناسب. برای forecasting، baselineهای Naive/SeasonalNaive اجباری، سپس ETS/ARIMA و مدل‌های intermittent demand در صورت نیاز؛ ارزیابی rolling-origin با افق واقعی.

**فناوری:** Decimal برای قیمت/هزینه؛ Statsmodels برای ETS/SARIMAX و اقتصادسنجی؛ StatsForecast 2.1.1 برای AutoETS/AutoARIMA و Croston/ADIDA/IMAPA/TSB در حجم سری بالا، اما این نسخه در PyPI با Development Status=Beta است؛ sktime برای composition/backtesting؛ Chronos-2 فقط challenger zero-shot.

**بنچمارک‌ها:** M4 شامل ۱۰۰هزار سری و ۶۱ روش بود؛ ۲۷ شرکت‌کننده از ترکیب روش‌ها استفاده کردند، pure MLها در مجموع رقابتی نبودند و برنده hybrid ES-RNN بود؛ روش دوم از XGBoost برای وزن‌دهی پیش‌بینی‌های آماری استفاده کرد. M5 روی ۴۲٬۸۴۰ سری سلسله‌مراتبی خرده‌فروشی و ۳۰٬۴۹۰ سری product-store نشان داد global ML، cross-learning و متغیرهای برون‌زا می‌توانند در همان مسئله بسیار قوی باشند؛ بااین‌حال حدود ۹۲٫۵٪ شرکت‌کنندگان از بهترین benchmark ساده‌تر عبور نکردند. بنابراین برنده M5 را به همه بازارها تعمیم نمی‌دهیم. Monash repository نتایج مدل‌های کلاسیک و foundation را روی مجموعه‌داده‌های متعدد و معیارهای یکسان قابل مقایسه می‌کند. رتبه‌بندی به افق، داده و metric حساس است؛ leaderboard عمومی جای backtest کسب‌وکار را نمی‌گیرد.

**شواهد/مستندات:** [M4 competition paper](https://doi.org/10.1016/j.ijforecast.2019.04.014)؛ [M4 hybrid/combination method](https://doi.org/10.1016/j.ijforecast.2019.03.030)؛ [M5 competition paper](https://doi.org/10.1016/j.ijforecast.2021.07.007)؛ [M5 accuracy results and findings](https://doi.org/10.1016/j.ijforecast.2021.11.013)؛ [M5 metric stability analysis](https://robjhyndman.com/publications/m5evaluation/)؛ [Monash Forecasting Repository](https://forecastingdata.org/)؛ [StatsForecast 2.1.1](https://pypi.org/project/statsforecast/2.1.1/)؛ [StatsForecast](https://github.com/nixtla/statsforecast)؛ [sktime forecasting/backtesting](https://www.sktime.org/en/stable/examples/01_forecasting.html)؛ [Chronos-2 report](https://www.amazon.science/blog/introducing-chronos-2-from-univariate-to-universal-forecasting).

### B03 — قیف، تبدیل و ریزش
**روش:** قیف با شمارش یکتای شناسه و تعریف مرحله؛ نرخ‌های مرحله‌ای و cohort. برای پیش‌بینی churn، Logistic Regression baseline و CatBoost challenger؛ برای زمان تا ریزش و censoring از survival analysis. احتمال‌های پیش‌بینی باید calibrated و با split زمانی/group-aware ارزیابی شوند.

**فناوری:** Pandas/SQL برای funnel؛ scikit-learn LogisticRegression، calibration و metrics؛ CatBoost برای داده جدولی/دسته‌ای؛ lifelines برای Kaplan–Meier/Cox؛ SHAP فقط feature attribution، نه علت ریزش.

**دلیل و شواهد:** مرور نظام‌مند ۲۰۲۵ churn روش‌های ML/DL و محدودیت‌هایشان را جمع‌بندی می‌کند. مطالعه Journal of Marketing Analytics در ۲۰۲۵ نشان می‌دهد survival analysis علاوه بر احتمال ریزش، زمان و hazard را برآورد می‌کند. [Customer churn systematic review (2025)](https://doi.org/10.3390/make7030105)؛ [Survival analysis for churn (2025)](https://doi.org/10.1057/s41270-025-00450-2)؛ [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html)؛ [CatBoost docs](https://catboost.ai/docs/)؛ [lifelines](https://lifelines.readthedocs.io/en/latest/).

### B04 — آزمایش و سنجش اثر
**روش:** RCT/A-B با randomization unit درست، metric و estimand از پیش تعریف‌شده، power/MDE، sample ratio mismatch، stopping rule و کنترل multiple testing. CUPED فقط با covariateهای pre-treatment؛ post-treatment covariate ممکن است bias بسازد. برای داده مشاهده‌ای، DAG و روش شناسایی قبل از estimator.

**فناوری:** SciPy/Statsmodels برای آزمون و power؛ DoWhy برای graph → identify → estimate → refute؛ EconML برای DML/CATE و ناهمگنی اثر؛ CUPED/variance reduction مرحله طراحی آزمایش است، نه جایگزین تصادفی‌سازی؛ فقط covariateهای pre-treatment مجازند.

**دلیل و شواهد:** مقاله PMLR 2026 درباره ترکیب داده pre-experiment و in-experiment، variance reduction را بررسی می‌کند؛ این روش‌ها باید با طراحی تصادفی و covariateهای مجاز pre-treatment همراه باشند. در تبلیغات پلتفرمی، divergent delivery ممکن است حتی A/B ظاهراً تصادفی را مخدوش کند. [DoWhy causal workflow](https://www.pywhy.org/dowhy/main/user_guide/intro.html)؛ [EconML](https://www.microsoft.com/en-us/research/project/econml/)؛ [CUPED original paper (KDD 2013)](https://doi.org/10.1145/2487575.2488217)؛ [Variance reduction with pre-experiment and in-experiment data (PMLR 2026)](https://proceedings.mlr.press/v323/lin26a.html)؛ [Learning from Many Experiments (2026)](https://thearf-org-unified-admin.s3.amazonaws.com/MSI/2026/MSI_Report_26-107.pdf)؛ [Where A/B Testing Goes Wrong (Journal of Marketing, 2025)](https://doi.org/10.1177/00222429241275886)؛ [Statsmodels power](https://www.statsmodels.org/stable/stats.html).

### B05 — KPI و گزارش عملکرد
**روش:** metric registry با تعریف، واحد، منبع، owner، grain، cadence، numerator/denominator و قواعد null؛ کنترل کیفیت و reconciliation قبل از داشبورد؛ anomaly flag فقط پس از baseline و فصل‌مندی.

**فناوری:** Pandas برای محاسبه اصلی؛ DuckDB برای SQL تحلیلی روی Parquet/فایل؛ Polars برای DataFrame/lazy pipelines در حجم بالا؛ Pandera برای schema و data validation روی pandas/polars؛ PostgreSQL همچنان منبع حقیقت.

**دلیل و شواهد:** Data validation باید قبل از تحلیل انجام شود. Pandera backendهای pandas، polars و دیگر DataFrameها را پشتیبانی می‌کند. DuckDB و Polars از طریق Arrow قابل اتصال‌اند. [Pandera 0.36.0](https://pandera.readthedocs.io/en/stable/)؛ [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview)؛ [DuckDB–Polars integration](https://duckdb.org/docs/stable/guides/python/polars)؛ [Polars user guide](https://docs.pola.rs/).

### B06 — سبد و سرمایه‌گذاری
**روش:** ابتدا محاسبه contribution، ظرفیت و قیود؛ سپس optimization. LP فقط برای هدف و قیود خطی؛ MILP برای تصمیم‌های گسسته؛ response curve/تقریب قطعه‌ای یا مدل nonlinear برای diminishing returns و تعامل کانال‌ها. امکان‌پذیری قیود باید جدا از optimality گزارش شود.

**فناوری:** SciPy linprog/milp با HiGHS برای LP/MILP؛ OR-Tools CP-SAT برای انتخاب‌های صحیح/Boolean و قیود ترکیبی؛ NumPy برای سناریو و sensitivity. PyPortfolioOpt ابزار پرتفوی مالی است و مستقیماً برای سبد بازاریابی انتخاب نمی‌شود.

**شواهد/مستندات:** [SciPy linprog](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)؛ [SciPy milp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html)؛ [Google OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver/).

---

## حوزه چهارم — مدیریت و اجرا

### E01 — برنامه و بودجه
**روش:** WBS، وابستگی کارها، critical path، owner، مدت و بودجه؛ برای محدودیت منابع، resource-constrained project scheduling. PERT وقتی مدت‌ها احتمالی‌اند؛ CPM برای مدت‌های قطعی. بودجه با Decimal.

**فناوری:** NetworkX برای DAG، topological sort و critical path؛ OR-Tools CP-SAT برای زمان‌بندی منابع محدود و precedence constraints؛ Decimal/Pydantic برای بودجه و schema.

**دلیل و شواهد:** مرور نظام‌مند ۲۰۲۶ روی ۲۶۸ مقاله RCPSP نشان می‌دهد مسئله منابع محدود NP-hard است و فرض‌های ساده CPM/RCPSP همیشه با پروژه واقعی منطبق نیستند. [RCPSP systematic review (2026)](https://doi.org/10.1080/00207543.2026.2683116)؛ [OR-Tools job-shop scheduling](https://developers.google.com/optimization/scheduling/job_shop)؛ [NetworkX DAG/critical path](https://networkx.org/documentation/stable/reference/algorithms/dag.html).

### E02 — کمپین و محتوا
**روش:** creative brief ساختاریافته: هدف، مخاطب، insight، پیام، proof, CTA، کانال، قالب، ادعاهای مجاز، معیار و نسخه. IMC باید پیام و کانال‌ها را هماهنگ کند؛ اثر محتوا با آزمون سنجیده شود. تولید محتوا با انتشار خودکار یکی نیست.

**فناوری:** Pydantic/JSON Schema برای brief و خروجی ساختاریافته؛ AI adapter قابل تعویض برای ایده و draft؛ asset/claim registry برای اتصال هر ادعا به شاهد؛ B04 برای آزمون creative. کتابخانه علمی اختصاصی برای «خوب بودن محتوا» وجود ندارد.

**دلیل و شواهد:** مرور نظام‌مند IMC دیجیتال در ۲۰۲۶ پنج بعد مخاطب/سفر، پیام، هماهنگی کانال، governance و evaluation را شناسایی می‌کند، اما framework پیشنهادی را causal-validated معرفی نمی‌کند. [Digital IMC systematic review (2026)](https://www.online-journal.unja.ac.id/mankeu/article/view/61397)؛ [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/).

### E03 — کانال و تخصیص رسانه / MMM
**روش:** برای داده ناکافی، طرح آزمایش و بودجه محدود با stop rule؛ نه ROI تخمینی. برای MMM پیشرفته، مدل باید carryover/adstock، saturation، trend/seasonality، کنترل‌ها، causal DAG، prior و experiment calibration، posterior diagnostics و holdout را پوشش دهد.

**انتخاب فناوری بر اساس مرور ۲۰۲۶:**
- **Google Meridian 2.2.1 (۱۹ نوامبر ۲۰۲۶):** انتخاب اول برای MMM بسته‌بندی‌شده و budget optimization وقتی داده زمانی/geo و توان محاسباتی کافی داریم. راهنمای رسمی Python 3.11/3.12 و GPU را توصیه می‌کند؛ JAX backend از نسخه 2.0 پیش‌فرض است و TensorFlow backend قدیمی deprecated شده است.
- **PyMC-Marketing 1.5.0:** گزینه انعطاف‌پذیر برای مدل سفارشی Bayesian، time-varying media و یکپارچگی با CLV؛ برای زنجیره کامل MMM و بودجه‌ریزی به کدنویسی/تخصص بیشتر نیاز دارد.
- **Meta Robyn 3.12.1:** challenger پایدار در R، با ridge regression، evolutionary optimization و budget allocation. Python port آن رسماً Beta و LLM-translated اعلام شده؛ بنابراین نسخه Python را production انتخاب نمی‌کنیم.

**محدودیت زیرساخت:** Meridian و PyMC-Marketing نباید کورکورانه در یک environment نصب شوند؛ metadata نسخه Meridian 2.2.1 بازه ArviZ کمتر از 0.20 می‌خواهد، درحالی‌که PyMC-Marketing 1.5.0 به ArviZ 1.2 یا بالاتر متکی است. اگر هر دو انتخاب شوند، worker/environment جدا لازم است. این جداسازی به‌دلیل dependency واقعی است، نه سلیقه معماری.

**دلیل و شواهد:** مرور ۲۰۲۶ مقایسه مستقیم سه پروژه را ارائه می‌کند: Robyn خودکارتر، Meridian بسته‌بندی‌شده‌تر با گزینه‌های budget optimization گسترده‌تر، PyMC-Marketing انعطاف‌پذیرتر برای متخصص Bayesian. هیچ‌کدام فرض causal را حذف نمی‌کنند. [Runge & Pauwels, Open-Source Media and MMM (2026)](https://doi.org/10.1007/s40547-026-00161-4)؛ [Meridian installation](https://developers.google.com/meridian/docs/user-guide/installing)؛ [Meridian causal assumptions](https://developers.google.com/meridian/docs/causal-inference/about-mmm-causal-inference-methodology)؛ [Meridian model debugging](https://developers.google.com/meridian/docs/post-modeling/model-debugging)؛ [PyMC-Marketing](https://www.pymc-marketing.io/en/stable/)؛ [Robyn stable R 3.12.1](https://cran.r-project.org/web/packages/Robyn/index.html)؛ [Robyn Python Beta status](https://facebookexperimental.github.io/Robyn/docs/robyn-api/)؛ [Robyn docs](https://facebookexperimental.github.io/Robyn/).

### E04 — فروش و چرخه مشتری
**روش:** تعریف lifecycle و SLA، lead qualification شفاف، تحویل MQL/SQL، follow-up و retention؛ rules-first. Lead scoring تنها وقتی ارزش دارد که برچسب outcome، زمان، هزینه مداخله و feedback loop وجود داشته باشد.

**فناوری:** Pandas/SQL برای funnel؛ LogisticRegression baseline؛ CatBoost برای داده جدولی/دسته‌ای؛ calibration و fairness checks؛ lifelines برای زمان تا renewal/churn؛ SHAP برای توضیح سهم ویژگی، نه علت رفتار. ارسال پیام یا اقدام مشتری بدون رضایت و مجوز لازم ممنوع است.

**شواهد:** [Customer churn systematic review (2025)](https://doi.org/10.3390/make7030105)؛ [Survival analysis for churn (2025)](https://doi.org/10.1057/s41270-025-00450-2)؛ [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html)؛ [CatBoost docs](https://catboost.ai/docs/).

### E05 — عملیات و فناوری
**روش:** process map دستی/BPMN برای وضع موجود و مطلوب؛ process mining فقط وقتی event log دارای case/activity/timestamp و کیفیت کافی وجود دارد؛ سپس conformance و bottleneck. انتخاب ابزار بر اساس requirement، integration، security، cost و maintainability.

**فناوری:** PM4Py برای process discovery، conformance checking و event log؛ NetworkX برای graph ساده؛ Pydantic برای connector schema؛ Pandera برای data validation. PM4Py قابلیت process mining است، نه جایگزین تحلیل نیازمندی و معماری سیستم.

**شواهد:** [PM4Py software paper (2023)](https://doi.org/10.1016/j.simpa.2023.100556)؛ [PM4Py docs](https://processintelligence.solutions/pm4py/api/index.html)؛ [Pandera](https://pandera.readthedocs.io/en/stable/).

### E06 — تیم و پیمانکار
**روش:** RACI/DRI برای مسئولیت؛ skill/capacity matrix برای کار و ظرفیت؛ برنامه توسعه و feedback. Solver فقط برای تطبیق کار، نقش، ظرفیت و موعد، نه برای ارزش‌گذاری شخصیت یا تصمیم خودکار استخدام.

**فناوری:** OR-Tools CP-SAT برای assignment و scheduling با متغیرهای صحیح/Boolean؛ Pydantic برای نقش/مهارت/ظرفیت؛ RACI به‌صورت schema و workflow اختصاصی.

**شواهد:** [OR-Tools employee scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling)؛ [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver/).

### E07 — ذی‌نفعان و تعارض
**روش:** stakeholder register و نقشه قدرت/مشروعیت/فوریت؛ جداسازی موضع اظهارشده از منفعت/نگرانی تأییدشده؛ ثبت توافق، تعارض و تصمیم. ویژگی روان‌شناختی افراد از متن یا داده رفتاری به‌عنوان حقیقت استنباط نشود.

**فناوری:** schema اختصاصی/Pydantic و ثبت تصمیم؛ AI برای خلاصه‌سازی دیدگاه‌های مستند، بدون امتیازدهی شخصیت. کتابخانه علمی اختصاصی لازم نیست.

**شواهد:** نظریه salience میچل، اگل و وود سه ویژگی power، legitimacy و urgency را برای اولویت توجه مدیر تعریف می‌کند؛ این چارچوب تصمیم است، نه طبقه‌بند قطعی انسان. [Mitchell, Agle & Wood (1997)](https://doi.org/10.5465/AMR.1997.9711022105)؛ [Stakeholder influence systematic review (2024)](https://doi.org/10.1016/j.emj.2023.08.004).

### E08 — کنترل و یادگیری
**روش:** PDCA و review cadence؛ metric owner، target، baseline، variance، علت احتمالی، اقدام و نتیجه بعدی. Control chart برای process stability؛ change-point detection برای کشف تغییر ساختاری؛ تحلیل علّی فقط از مسیر B04.

**فناوری:** Pandas/Statsmodels برای KPI و سری زمانی؛ ruptures برای offline change-point detection در صورت نیاز؛ SciPy برای آزمون و confidence interval؛ Pydantic برای action log. anomaly detection به‌تنهایی علت یا اقدام را تعیین نمی‌کند.

**شواهد/مستندات:** [ruptures — offline change-point detection](https://centre-borelli.github.io/ruptures-docs/)؛ [Statsmodels](https://www.statsmodels.org/stable/)؛ [DoWhy causal refutation](https://www.pywhy.org/dowhy/main/user_guide/intro.html).

---

## تصمیم نهایی فناوری و سازگاری نسخه‌ها

### baseline مشترک پیشنهادی برای هسته Python
مرور metadata رسمی نشان می‌دهد baseline قبلی Python 3.13 / NumPy 2.5.5 / SciPy 1.18.1 / Statsmodels 0.15.0 برای مجموعه هدف مناسب نیست: PyMC-Marketing 1.5.0 در release metadata به NumPy کمتر از 2.6 نیاز دارد؛ Google Meridian 2.2.1 به NumPy کمتر از 2.4، pandas کمتر از 3، SciPy کمتر از 2 و Statsmodels کمتر از 0.15 نیاز دارد؛ و DoWhy 0.14 در Python 3.12 سقف SciPy برابر 1.15.3 دارد. برای هم‌پوشانی این اجزا، baseline محافظه‌کارانه‌تر زیر پیشنهاد می‌شود:

| جزء | baseline پیشنهادی | دلیل |
|---|---|---|
| CPython | 3.12.x | اشتراک مستندشده PyMC-Marketing و Meridian و پشتیبانی کتابخانه‌های اصلی |
| NumPy | 2.3.5 | در بازه کمتر از 2.4 Meridian و کمتر از 2.5 PyMC-Marketing |
| pandas | 2.3.3 | کمتر از 3.0 برای StatsForecast و Meridian |
| SciPy | 1.15.3 | سقف DoWhy 0.14 در Python 3.12؛ حداقل نیازهای SciPy سایر اجزا را برآورده می‌کند |
| scikit-learn | 1.9.1 | نسخه stable؛ سازگار با Python 3.12 و نیاز EconML کمتر از 1.10 |
| Statsmodels | 0.14.5 | در بازه کمتر از 0.15 Meridian و حداقل 0.14.5 StatsForecast |

این‌ها **نسخه‌های candidate برای resolver/lockfile هستند، نه نسخه‌های نصب‌شده و تأییدشده در این commit**. هیچ ادعای CI یا runtime PASS برای این baseline جدید وجود ندارد؛ اعتبار CI قبلی فقط به commit و نسخه‌های همان اجرا مربوط است.

### جداسازی‌های واقعی و ضروری
1. Meridian و PyMC-Marketing 1.5.0 به‌دلیل بازه‌های متضاد ArviZ در یک محیط Python مشترک قابل نصب نیستند؛ در صورت استفاده هم‌زمان، محیط/worker مجزا لازم است.
2. Chronos-2، BERTopic، embedding models، PM4Py و MMM sampling باید به‌صورت optional/lazy و فقط در ابزارهای نیازمندشان بارگذاری شوند.
3. StatsForecast 2.1.1 در PyPI با Development Status = Beta منتشر شده؛ استفاده از آن باید با baselineهای Statsmodels و backtest مقایسه شود.
4. svy 0.36.0 نیز در سطح package در حال توسعه است؛ مستندات پروژه هسته design/weighting/variance را stable و production-ready معرفی می‌کنند، اما APIها را همچنان در حال تکامل می‌دانند.
5. هیچ lockfile قطعی، نصب ترکیبی جدید یا اجرای تست پس از این بازبینی ادعا نمی‌شود؛ GitHub Actions فعلاً به‌دلیل محدودیت اعتبار CI در دسترس نیست.

### مراجع نسخه و metadata
- [NumPy 2.3.5 release notes](https://numpy.org/doc/stable/release/2.3.5-notes.html)
- [pandas 2.3 installation/dependencies](https://pandas.pydata.org/pandas-docs/version/2.3/getting_started/install.html)
- [scikit-learn dependency table](https://scikit-learn.org/stable/min_dependency_table.html)
- [DoWhy v0.14 release notes](https://github.com/py-why/dowhy/releases/tag/v0.14)
- [EconML 0.17.1](https://pypi.org/project/econml/0.17.1/)
- [PyMC-Marketing 1.5.0 metadata](https://pypi.org/project/pymc-marketing/1.5.0/) و [pyproject at the exact 1.5.0 build commit](https://github.com/pymc-labs/pymc-marketing/blob/ede5d75a0d1ba880c61467aaaa7760182b00e1de/pyproject.toml)
- [Google Meridian 2.2.1 (released 19 Nov 2026)](https://pypi.org/project/google-meridian/2.2.1/)؛ [Meridian installation requirements](https://developers.google.com/meridian/docs/user-guide/installing)؛ [dependency metadata](https://github.com/google/meridian/blob/v2.2.1/pyproject.toml)
- [StatsForecast 2.1.1 metadata](https://pypi.org/project/statsforecast/2.1.1/)
- [Statsmodels 0.14.5](https://pypi.org/project/statsmodels/0.14.5/)؛ [SciPy 1.15.3](https://pypi.org/project/scipy/1.15.3/)؛ [NumPy 2.3.5](https://pypi.org/project/numpy/2.3.5/)؛ [pandas 2.3.3](https://pypi.org/project/pandas/2.3.3/)
- [PyMCDM 1.4.0](https://pypi.org/project/pymcdm/)؛ [clustMixType 0.5-2](https://cran.r-project.org/web/packages/clustMixType/index.html)؛ [KAMILA 0.2.0](https://cran.r-project.org/web/packages/kamila/index.html)
- [svy 0.36.0](https://pypi.org/project/svy/)
- [Biogeme](https://pypi.org/project/biogeme/)
- [BERTopic 0.17.4](https://pypi.org/project/bertopic/0.17.4/)
- [lifelines 0.30.3](https://lifelines.readthedocs.io/en/latest/)
- [PM4Py release history](https://pypi.org/project/pm4py/)؛ [Meta Robyn 3.12.1 stable R package](https://cran.r-project.org/web/packages/Robyn/index.html)؛ [Robyn Python beta status](https://facebookexperimental.github.io/Robyn/docs/robyn-api/)
- [Pandera](https://pandera.readthedocs.io/en/stable/)
- [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview)
- [Polars](https://docs.pola.rs/)

## جمع‌بندی
برای ۲۹ ابزار، روش و فناوری منتخب همراه با شواهد و محدودیت‌های آن‌ها مشخص شد. نتیجه، نصب ۲۹ نرم‌افزار یا استفاده اجباری از ML نیست؛ یک موتور تصمیم‌سازی ترکیبی است: فرمول‌های دقیق برای محاسبات، روش‌های آماری برای استنباط، مدل‌های ML فقط برای مسئله مناسب، و چارچوب انسانی برای تصمیم‌های استراتژیک و اجرایی. انتخاب‌های این سند مبنای DEV هستند؛ تست محدود در DEV باید صحت اتصال API و fixtureهای هر ابزار را بررسی کند، نه اینکه پژوهش‌های منتشرشده را از صفر بازتولید کند.
