## Схема решения
1. Пользователь загружает изображение.
2. Изображение передается в систему детекции и распознавания логотипов.
3. Выполняется детекция объектов, похожих на логотипы.
4. Сверяются распознанные логотипы с базой данных. Находится косинусное расстояние между эмбеддингом распознанного логотипа и каждым эмбеддингом базы логотипов. Система проверяет, есть ли среди распознанных логотипы конкурентов, мошеннических организаций или запрещенная символика.
5. Если такие логотипы найдены, они выводятся на сайте.
Иначе выводится надпись, что ничего не найдено.

## Метрики
Мы должны вычислять как можно больше нежелательных логотипов, чтобы они не портили репутацию как Авито, так и добросовестных продавцов и работодателей, а также не привели к нарушению действующих законов. 
С другой стороны, мы не должны отклонять объявления честных продавцов по причине неточности модели.
- **Бизнес-метрика:** жалобы на нежелательный контент.  

Мы должны минимизировать эту метрику при незначительном изменении (<1%) числа ложно отклонённых объявлений. Успех - если число жалоб на нежелательный контент уменьшится на 5%. 

## Метрики машинного обучения
Данная задача разделяется на 2 задачи машинного обучения: детекция и классификация. Соответственно нужно учитывать метрики обеих задач. 
1) Метрики детекции: mAP, IoU
2) Метрики классификации: accuracy, f1-score

Так как с задачей детекции логотипов модель справляется достаточно хорошо, для оптимизации бизнес-метрик будем опираться на метрики классификации, так как они вносят значительный вклад в точность предсказаний.