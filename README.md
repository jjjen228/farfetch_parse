Завдання виконано за допомогою бібліотеки Селеніум 4.20.0.

!важливо - перед компіляцією обов'язково перевірте свою версію браузера та шлях до драйвера. Нажаль це є мінусом Селеніуму, але він мені зручніший бо я працював з автоматизацією.

На жаль у мене були проблеми з сумісністю Селеніуму та Тензорфлоу, коли я викликав presence_of_element_located, тому я використав звичайний тайм сліп, щоб дочекатися виконання анімації появи розмірів, так як там нічого не завантажується а дані просто приховані анімацією без дісплей стилів, то можна загалом використати і таймсліп на 20 мс, завчасно прошу вибачення за це, бо це груба помилка яка не передбачає завантаження елементу на сторінці, просто через особисті проблеми у мене не було часу шукати рішення. Це нетипова проблема, що виникає конфлікт під час використання саме цієї функції, тому рішень на виду немає. 

Також використав lxml для створення гугл мерчант фіду у xml форматі.

Унікальні айді товару це просто груп_айді + розмір, як я зрозумів це правильне рішення за умовами завдання. MPN у нас немає. Розмір також виведено у окрему категорію.

Гугл категорія була зроблена на основі вашого посилання у завданні, я взяв звідти бажану нам категорію та зробив невелику логічну умову для її присвоєння, я не робив на цьому важливий акцент бо ми парсимо сторінку з жіночими платтями, в разі парсингу загальних сторінок можна умпортувати окремо файл що ви додавали та перевіряти по ньому.

У коментарях у коді додав варіанти очікування завантаження елемента.

Доступність перевірив створивши умову що є розміри та ціна, та дата-лоадед == тру, так як у нас не було у коді сторінки явного показника доступності, то логічну умову такого формату можна вважати перевіркою доступності. Якщо нема розмірів то виходячи з перегляду сайту це Промо, адже недоступні товари не відображаються на сторінці.

Ліміт стоїть 120 елементів, як вказано в завданні. Кожен розмір - окремий товар.

Гендер береться з посилання, адже категорія по гендеру завжди там вказана.