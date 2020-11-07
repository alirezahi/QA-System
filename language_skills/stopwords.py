stopwords = ['﻿!',
'"',
'#',
'(',
')',
'*',
',',
'-',
'.',
'}',
'{',
'/',
':',
'[',
']',
'«',
'»',
'،',
'؛',
'؟',
'آباد',
'آخ',
'آخر',
'آخرها',
'آخه',
'آدمهاست',
'آرام',
'آرام آرام',
'آره',
'آری',
'آزادانه',
'آسان',
'آسیب پذیرند',
'آشنایند',
'آشکارا',
'آقا',
'آقای',
'آقایان',
'آمد',
'آمدن',
'آمده',
'آمرانه',
'آن',
'آن گاه',
'آنان',
'آنانی',
'آنجا',
'آنرا',
'آنطور',
'آنقدر',
'آنها',
'آنهاست',
'آنچنان',
'آنچنان که',
'آنچه',
'آنکه',
'آنگاه',
'آن‌ها',
'آهان',
'آهای',
'آور',
'آورد',
'آوردن',
'آورده',
'آوه',
'آی',
'آیا',
'آید',
'آیند',
'ا',
'اتفاقا',
'اثرِ',
'اجراست',
'احتراما',
'احتمالا',
'احیاناً',
'اخیر',
'اخیراً',
'اری',
'از',
'از آن پس',
'از جمله',
'ازاین رو',
'ازجمله',
'ازش',
'اساسا',
'اساساً',
'است',
'استفاد',
'استفاده',
'اسلامی اند',
'اش',
'اشتباها',
'اشکارا',
'اصلا',
'اصلاً',
'اصولا',
'اصولاً',
'اعلام',
'اغلب',
'افزود',
'افسوس',
'اقل',
'اقلیت',
'الا',
'الان',
'البته',
'البتّه',
'الهی',
'الی',
'ام',
'اما',
'امروز',
'امروزه',
'امسال',
'امشب',
'امور',
'امیدوارم',
'امیدوارند',
'امیدواریم',
'ان',
'ان شاأالله',
'انتها',
'اند',
'اندکی',
'انشاالله',
'انصافا',
'انطور',
'انقدر',
'انها',
'انچنان',
'انکه',
'انگار',
'او',
'اوست',
'اون',
'اکثر',
'اکثرا',
'اکثراً',
'اکثریت',
'اکنون',
'اگر',
'اگر چه',
'اگرچه',
'اگه',
'ای',
'ایا',
'اید',
'ایشان',
'ایم',
'این',
'این جوری',
'این قدر',
'این گونه',
'اینان',
'اینجا',
'اینجاست',
'ایند',
'اینطور',
'اینقدر',
'اینها',
'اینهاست',
'اینو',
'اینچنین',
'اینک',
'اینکه',
'اینگونه',
'ب ',
'با',
'بااین حال',
'بااین وجود',
'باد',
'بار',
'بارة',
'باره',
'بارها',
'باز',
'باز هم',
'بازهم',
'بازی کنان',
'بازیگوشانه',
'باش',
'باشد',
'باشم',
'باشند',
'باشی',
'باشید',
'باشیم',
'بالا',
'بالاخره',
'بالاخص',
'بالاست',
'بالای',
'بالایِ',
'بالطبع',
'بالعکس',
'باوجودی که',
'باورند',
'باید',
'بتدریج',
'بتوان',
'بتواند',
'بتوانی',
'بتوانیم',
'بجز',
'بخش',
'بخشه',
'بخشی',
'بخصوص',
'بخواه',
'بخواهد',
'بخواهم',
'بخواهند',
'بخواهی',
'بخواهید',
'بخواهیم',
'بخوبی',
'بد',
'بدان',
'بدانجا',
'بدانها',
'بدهید',
'بدون',
'بدین',
'بدین ترتیب',
'بدینجا',
'بر',
'برآنند',
'برا',
'برابر',
'برابرِ',
'براحتی',
'براساس',
'براستی',
'برای',
'برایت',
'برایش',
'برایشان',
'برایم',
'برایمان',
'برایِ',
'برخوردار',
'برخوردارند',
'برخی',
'برداری',
'برعکس',
'برنامه سازهاست',
'بروز',
'بروشنی',
'بزرگ',
'بزودی',
'بس',
'بسا',
'بسادگی',
'بسختی',
'بسوی',
'بسی',
'بسیار',
'بسیاری',
'بشدت',
'بطور',
'بطوری که',
'بعد',
'بعد از این که',
'بعدا',
'بعدازظهر',
'بعداً',
'بعدها',
'بعری',
'بعضا',
'بعضی',
'بعضی شان',
'بعضیهایشان',
'بعضی‌ها',
'بعلاوه',
'بعید',
'بفهمی نفهمی',
'بلافاصله',
'بله',
'بلکه',
'بلی',
'بماند',
'بنابراین',
'بندی',
'به',
'به آسانی',
'به تازگی',
'به تدریج',
'به تمامی',
'به جای',
'به جز',
'به خوبی',
'به درشتی',
'به دلخواه',
'به راستی',
'به رغم',
'به روشنی',
'به زودی',
'به سادگی',
'به سرعت',
'به شان',
'به شدت',
'به طور کلی',
'به طوری که',
'به علاوه',
'به قدری',
'به مراتب',
'به ناچار',
'به هرحال',
'به هیچ وجه',
'به وضوح',
'به ویژه',
'به کرات',
'به گرمی',
'بهت',
'بهتر',
'بهترین',
'بهش',
'بود',
'بودم',
'بودن',
'بودند',
'بوده',
'بودی',
'بودید',
'بودیم',
'بویژه',
'بپا',
'بکار',
'بکن',
'بکند',
'بکنم',
'بکنند',
'بکنی',
'بکنید',
'بکنیم',
'بگذاریم',
'بگو',
'بگوید',
'بگویم',
'بگویند',
'بگویی',
'بگویید',
'بگوییم',
'بگیر',
'بگیرد',
'بگیرم',
'بگیرند',
'بگیری',
'بگیرید',
'بگیریم',
'بی',
'بی آنکه',
'بی اطلاعند',
'بی تردید',
'بی تفاوتند',
'بی نیازمندانه',
'بی هدف',
'بیا',
'بیاب',
'بیابد',
'بیابم',
'بیابند',
'بیابی',
'بیابید',
'بیابیم',
'بیاور',
'بیاورد',
'بیاورم',
'بیاورند',
'بیاوری',
'بیاورید',
'بیاوریم',
'بیاید',
'بیایم',
'بیایند',
'بیایی',
'بیایید',
'بیاییم',
'بیرون',
'بیرونِ',
'بیست',
'بیش',
'بیشتر',
'بیشتری',
'بین',
'بیگمان',
'ت',
'تا',
'تازه',
'تان',
'تاکنون',
'تحت',
'تحریم هاست',
'تر',
'تر براساس',
'تریلیارد',
'تریلیون',
'ترین',
'تصریحاً',
'تعدادی',
'تعمدا',
'تقریبا',
'تقریباً',
'تلویحا',
'تلویحاً',
'تمام',
'تمام قد',
'تماما',
'تمامشان',
'تمامی',
'تند تند',
'تنها',
'تو',
'توؤماً',
'توان',
'تواند',
'توانست',
'توانستم',
'توانستن',
'توانستند',
'توانسته',
'توانستی',
'توانستیم',
'توانم',
'توانند',
'توانی',
'توانید',
'توانیم',
'توسط',
'تولِ',
'توی',
'تویِ',
'تک تک',
'ث',
'ثالثاً',
'ثانیا',
'ثانیاً',
'ج',
'جا',
'جای',
'جایی',
'جدا',
'جداً',
'جداگانه',
'جدید',
'جدیدا',
'جرمزاست',
'جریان',
'جز',
'جلو',
'جلوگیری',
'جلوی',
'جلویِ',
'جمع اند',
'جمعا',
'جمعی',
'جنابعالی',
'جناح',
'جنس اند',
'جهت',
'جور',
'ح',
'حاشیه‌ای',
'حاضر',
'حاضرم',
'حال',
'حالا',
'حاکیست',
'حتما',
'حتماً',
'حتی',
'حداقل',
'حداکثر',
'حدود',
'حدودا',
'حدودِ',
'حسابگرانه',
'حضرتعالی',
'حقیرانه',
'حقیقتا',
'حول',
'حکماً',
'خ',
'خارجِ',
'خالصانه',
'خب',
'خداحافظ',
'خداست',
'خدمات',
'خسته‌ای',
'خصوصا',
'خصوصاً',
'خلاصه',
'خواست',
'خواستم',
'خواستن',
'خواستند',
'خواسته',
'خواستی',
'خواستید',
'خواستیم',
'خواه',
'خواهد',
'خواهم',
'خواهند',
'خواهی',
'خواهید',
'خواهیم',
'خوب',
'خود',
'خود به خود',
'خودبه خودی',
'خودت',
'خودتان',
'خودتو',
'خودش',
'خودشان',
'خودم',
'خودمان',
'خودمو',
'خوش',
'خوشبختانه',
'خویش',
'خویشتن',
'خویشتنم',
'خیاه',
'خیر',
'خیره',
'خیلی',
'د',
'دا',
'داام',
'دااما',
'داخل',
'داد',
'دادم',
'دادن',
'دادند',
'داده',
'دادی',
'دادید',
'دادیم',
'دار',
'داراست',
'دارد',
'دارم',
'دارند',
'داری',
'دارید',
'داریم',
'داشت',
'داشتم',
'داشتن',
'داشتند',
'داشته',
'داشتی',
'داشتید',
'داشتیم',
'دامم',
'دانست',
'دانند',
'دایم',
'دایما',
'در',
'در باره',
'در بارهٌ',
'در ثانی',
'در مجموع',
'در نهایت',
'در واقع',
'در کل',
'در کنار',
'دراین میان',
'درباره',
'درحالی که',
'درحالیکه',
'درست',
'درست و حسابی',
'درسته',
'درصورتی که',
'درعین حال',
'درمجموع',
'درواقع',
'درون',
'دریغ',
'دریغا',
'درین',
'دسته دسته',
'دشمنیم',
'دقیقا',
'دم',
'دنبالِ',
'ده',
'دهد',
'دهم',
'دهند',
'دهی',
'دهید',
'دهیم',
'دو',
'دو روزه',
'دوباره',
'دیده',
'دیر',
'دیرت',
'دیرم',
'دیروز',
'دیشب',
'دیوانه‌ای',
'دیوی',
'دیگر',
'دیگران',
'دیگری',
'دیگه',
'ذ',
'ذاتاً',
'ر',
'را',
'راجع به',
'راحت',
'راسا',
'راست',
'راستی',
'راه',
'رسما',
'رسید',
'رسیده',
'رشته',
'رفت',
'رفتارهاست',
'رفته',
'رنجند',
'رهگشاست',
'رو',
'رواست',
'روب',
'روبروست',
'روز',
'روز به روز',
'روزانه',
'روزه ایم',
'روزه ست',
'روزه م',
'روزهای',
'روزه‌ای',
'روش',
'روی',
'رویش',
'رویِ',
'ریزی',
'ز',
'زشتکارانند',
'زمینه',
'زنند',
'زهی',
'زود',
'زودتر',
'زیاد',
'زیاده',
'زیر',
'زیرا',
'زیرِ',
'زیرچشمی',
'س',
'سابق',
'ساخته',
'ساده اند',
'سازی',
'سالانه',
'سالته',
'سالم‌تر',
'سالهاست',
'سالیانه',
'ساکنند',
'سایر',
'سخت',
'سخته',
'سر',
'سراسر',
'سرانجام',
'سراپا',
'سری',
'سریع',
'سریعا',
'سریعاً',
'سریِ',
'سعی',
'سمتِ',
'سه باره',
'سهواً',
'سوم',
'سوی',
'سویِ',
'سپس',
'سیاه چاله هاست',
'سیخ',
'ش',
'شان',
'شاهدند',
'شاهدیم',
'شاید',
'شبهاست',
'شخصا',
'شخصاً',
'شد',
'شدم',
'شدن',
'شدند',
'شده',
'شدی',
'شدید',
'شدیدا',
'شدیداً',
'شدیم',
'شش',
'شش نداشته',
'شما',
'شماری',
'شماست',
'شمایند',
'شناسی',
'شو',
'شود',
'شوراست',
'شوقم',
'شوم',
'شوند',
'شونده',
'شوی',
'شوید',
'شویم',
'شیرین',
'شیرینه',
'شیک',
'ص',
'صد',
'صددرصد',
'صرفا',
'صرفاً',
'صریحاً',
'صندوق هاست',
'صورت',
'ض',
'ضدِّ',
'ضدِّ',
'ضمن',
'ضمناً',
'ط',
'طبعا',
'طبعاً',
'طبقِ',
'طبیعتا',
'طرف',
'طریق',
'طلبکارانه',
'طور',
'طی',
'ظ',
'ظاهرا',
'ظاهراً',
'ع',
'عاجزانه',
'عاقبت',
'عبارتند',
'عجب',
'عجولانه',
'عرفانی',
'عقب',
'عقبِ',
'علاوه بر',
'علاوه بر آن',
'علاوه برآن',
'علناً',
'علّتِ',
'علی الظاهر',
'علی رغم',
'علیرغم',
'علیه',
'عمدا',
'عمداً',
'عمدتا',
'عمدتاً',
'عمل',
'عملا',
'عملاً',
'عملی اند',
'عموم',
'عموما',
'عموماً',
'عنقریب',
'عنوان',
'عنوانِ',
'عیناً',
'غ',
'غالبا',
'غزالان',
'غیر',
'غیرقانونی',
'ف',
'فاقد',
'فبها',
'فر',
'فردا',
'فعلا',
'فعلاً',
'فقط',
'فلان',
'فلذا',
'فوق',
'فکر',
'ق',
'قاالند',
'قابل',
'قاطبه',
'قاطعانه',
'قاعدتاً',
'قانوناً',
'قبل',
'قبلا',
'قبلاً',
'قبلند',
'قدر',
'قدری',
'قصدِ',
'قضایاست',
'قطعا',
'قطعاً',
'ل',
'لااقل',
'لاجرم',
'لب',
'لذا',
'لزوماً',
'لطفا',
'لطفاً',
'لیکن',
'م',
'ما',
'مادامی',
'ماست',
'مامان مامان گویان',
'مان',
'مانند',
'مانندِ',
'مبادا',
'متؤسفانه',
'متاسفانه',
'متعاقبا',
'متفاوتند',
'مثل',
'مثلا',
'مثلِ',
'مجانی',
'مجبورند',
'مجموعا',
'مجموعاً',
'محتاجند',
'محکم',
'محکم‌تر',
'مخالفند',
'مختلف',
'مخصوصاً',
'مدام',
'مدتهاست',
'مدّتی',
'مذهبی اند',
'مرا',
'مرتب',
'مردانه',
'مردم',
'مردم اند',
'مرسی',
'مستحضرید',
'مستقیما',
'مستند',
'مسلما',
'مشت',
'مشترکاً',
'مشغولند',
'مطمانا',
'مطمانم',
'مطمینا',
'مع الاسف',
'مع ذلک',
'معتقدم',
'معتقدند',
'معتقدیم',
'معدود',
'معذوریم',
'معلومه',
'معمولا',
'معمولاً',
'معمولی',
'مغرضانه',
'مفیدند',
'مقابل',
'مقدار',
'مقصرند',
'مقصری',
'ملیارد',
'ملیون',
'ممکن',
'ممیزیهاست',
'من',
'منتهی',
'منطقی',
'منی',
'مواجهند',
'موارد',
'موجودند',
'مورد',
'موقتا',
'مکرر',
'مکرراً',
'مگر',
'مگر آن که',
'مگر این که',
'مگو',
'می',
'میان',
'میلیارد',
'میلیون',
'میکند',
'میکنم',
'میکنند',
'میکنی',
'میکنید',
'میکنیم',
'می‌تواند',
'می‌خواهیم',
'می‌داند',
'می‌رسد',
'می‌رود',
'می‌شود',
'می‌کنم',
'می‌کنند',
'می‌کنیم',
'ن',
'ناامید',
'ناخواسته',
'ناراضی اند',
'ناشی',
'نام',
'ناگاه',
'ناگزیر',
'ناگهان',
'ناگهانی',
'نباید',
'نبش',
'نبود',
'نخست',
'نخستین',
'نخواهد',
'نخواهم',
'نخواهند',
'نخواهی',
'نخواهید',
'نخواهیم',
'نخودی',
'ندارد',
'ندارم',
'ندارند',
'نداری',
'ندارید',
'نداریم',
'نداشت',
'نداشتم',
'نداشتند',
'نداشته',
'نداشتی',
'نداشتید',
'نداشتیم',
'نزد',
'نزدِ',
'نزدیک',
'نزدیکِ',
'نسبتا',
'نشان',
'نشده',
'نظیر',
'نفرند',
'نماید',
'نموده',
'نمی',
'نمی‌شود',
'می‌باشد',
'نمی‌تواند',
'نمی‌باشود',
'نمی‌کند',
'نمی‌شوند',
'نمی',
'نمی‌توانند',
'نمی‌گردد',
'نمیتوانند',
'میتوانند',
'می‌بایست',
'نه',
'نه تنها',
'نهایتا',
'نهایتاً',
'نوع',
'نوعاً',
'نوعی',
'نکرده',
'نکن',
'نکند',
'نکنم',
'نکنند',
'نکنی',
'نکنید',
'نکنیم',
'نگاه',
'نگو',
'نیازمندند',
'نیز',
'نیست',
'نیستم',
'نیستند',
'نیستیم',
'نیمی',
'ه',
'ها',
'های',
'هایی',
'هبچ',
'هر',
'هر از گاهی',
'هر چند',
'هر چند که',
'هر چه',
'هرچند',
'هرچه',
'هرکس',
'هرگاه',
'هرگز',
'هزار',
'هست',
'هستم',
'هستند',
'هستی',
'هستید',
'هستیم',
'هفت',
'هق هق کنان',
'هم',
'هم اکنون',
'هم اینک',
'همان',
'همان طور که',
'همان گونه که',
'همانا',
'همانند',
'همانها',
'همدیگر',
'همزمان',
'همه',
'همه روزه',
'همه ساله',
'همه شان',
'همهٌ',
'همه‌اش',
'همواره',
'همچنان',
'همچنان که',
'همچنین',
'همچون',
'همچین',
'همگان',
'همگی',
'همیشه',
'همین',
'همین که',
'هنوز',
'هنگام',
'هنگامِ',
'هنگامی',
'هنگامی که',
'هوی',
'هی',
'هیچ',
'هیچ گاه',
'هیچکدام',
'هیچکس',
'هیچگاه',
'هیچگونه',
'هیچی',
'و',
'و لا غیر',
'وابسته اند',
'واقعا',
'واقعاً',
'واقعی',
'واقفند',
'واما',
'وای',
'وجود',
'وحشت زده',
'وسطِ',
'وضع',
'وقتی',
'وقتی که',
'وقتیکه',
'ولی',
'وگرنه',
'وگو',
'وی',
'ویا',
'ویژه',
'ّه',
'٪',
'پ',
'پارسال',
'پارسایانه',
'پاره‌ای',
'پاعینِ',
'پایین ترند',
'پدرانه',
'پرسان',
'پروردگارا',
'پریروز',
'رساند',
'گیر',
'کیری',
'مي',
'گیرد',
'خواهد_نمود',
'خواهد_شد',
'پس',
'پس از',
'پس فردا',
'پشت',
'پشتوانه اند',
'پشیمونی',
'پنج',
'پهن شده',
'پی',
'پی درپی',
'پیدا',
'پیداست',
'پیرامون',
'پیش',
'پیشاپیش',
'پیشتر',
'پیشِ',
'پیوسته',
'چ',
'چاپلوسانه',
'چت',
'چته',
'چرا',
'چرا که',
'چشم بسته',
'چطور',
'چقدر',
'چنان',
'چنانچه',
'چنانکه',
'چند',
'چند روزه',
'چندان',
'چنده',
'چندین',
'چنین',
'چه',
'چه بسا',
'چه طور',
'چهار',
'چو',
'چون',
'چکار',
'چگونه',
'چی',
'چیز',
'چیزی',
'چیزیست',
'چیست',
'چیه',
'ژ',
'ک',
'کارند',
'کاش',
'کاشکی',
'کامل',
'کاملا',
'کاملاً',
'کتبا',
'کجا',
'کجاست',
'کدام',
'کرد',
'کردم',
'کردن',
'کردند',
'کرده',
'کردی',
'کردید',
'کردیم',
'کس',
'کسانی',
'کسی',
'کل',
'کلا',
'کلی',
'کلیه',
'کم',
'کم کم',
'کمااینکه',
'کماکان',
'کمتر',
'کمتره',
'کمتری',
'کمی',
'کن',
'کنار',
'کنارش',
'کنارِ',
'کنایه‌ای',
'کند',
'کنم',
'کنند',
'کننده',
'کنون',
'کنونی',
'کنی',
'کنید',
'کنیم',
'که',
'کو',
'کَی',
'کی',
'گ',
'گاه',
'گاهی',
'گذاری',
'گذاشته',
'گذشته',
'گردد',
'گردند',
'گرفت',
'گرفتارند',
'گرفتم',
'گرفتن',
'گرفتند',
'گرفته',
'گرفتی',
'گرفتید',
'گرفتیم',
'گروهی',
'گرچه',
'گفت',
'گفتم',
'گفتن',
'گفتند',
'گفته',
'گفتی',
'گفتید',
'گفتیم',
'گه',
'گهگاه',
'گو',
'گونه',
'گوی',
'گویا',
'گوید',
'گویم',
'گویند',
'گویی',
'گویید',
'گوییم',
'گیر',
'گیرد',
'گیرم',
'گیرند',
'گیری',
'گیرید',
'گیریم',
'ی',
'یا',
'یاب',
'یابد',
'یابم',
'یابند',
'یابی',
'یابید',
'یابیم',
'یارب',
'یافت',
'یافتم',
'یافتن',
'یافته',
'یافتی',
'یافتید',
'یافتیم',
'یعنی',
'یقینا',
'یقیناً',
'یه',
'یواش یواش',
'یک',
'یک جوری',
'یک کم',
'یک کمی',
'یکدیگر',
'یکریز',
'یکسال',
'یکهزار',
'یکی',
'۰',
'۱',
'۲',
'۳',
'۴',
'۵',
'۶',
'۷',
'۸',
'۹',
'…',
'﻿و',
'شنبه',
'یکشنبه',
'خواهد_یافت',
'میرساند',
'می‌رساند',
'یک شنبه',
'دوشنبه',
'دو شنبه',
'سه شنبه',
'سهشنبه',
'چهارشنبه',
'چهار شنبه',
'پنج شنبه',
'پنجشنبه',
'جمعه',
'مهر',
'مهرماه',
'آبان',
'آبانماه',
'می‌توانند',
'ماه',
'آذر',
'اذر',
'اذرماه',
'آذرماه',
'دی',
'دیماه',
'بهمن',
'بهمنماه',
'اسفند',
'اسفندماه',
'فروردین',
'می‌باشد',
'فروردینماه',
'اردیبهشت',
'اردیبهشتماه',
'خرداد',
'خردادماه',
'تیرماه',
'تیر',
'مردادماه',
'مرداد',
'نمی‌باشد',
'می‌گیرد',
'نمی‌گیرد',
'NAV',
'بسیار',
'مهم',
'شهریور',
'شهریورماه',
'اطلاعیه',
'پایان عرضه',
'مهم',
'در',
'کالا']