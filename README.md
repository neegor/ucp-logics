# ucp-logics

Тестовая сборка Django App для проверки возможностей Block Range Index (BRIN) близко приблеженным к реальным. техника индексации данных, предназначенная для обработки больших

BRIN оперирует описаниями больших блоков данных, где хранится минимальное и максимальное значение индексируемого столбца внутри блока. Во время запросов сначала фильтруются блоки (условия запроса применяется к описанию блока). Таким образом, за небольшое число проверок сокращается набор данных, которые надо будет проверять построчно.

Для реализации используем стандартную ни чем не кастомизированную [PostgreSQL specific model indexes](https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/indexes/#brinindex). Не кастомизируем только в целях чистоты эксперимента.