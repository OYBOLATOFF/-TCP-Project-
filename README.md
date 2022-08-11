# Задача коммивояжёра
Проект TCP Project это решение знаменитой задачи коммивояжёра, в которой почтальону нужно обойти все города-узлы и вернуться в исходный город, затратив на всю дорогу наименьшее возможное расстояние

Использование:
  [1] Первым делом при запуске программа просит пользователя ввести название файла, в котором хранится информация о всех городах
  Если человек желает вбить информацию вручную без файла, то необходимо просто нажать Enter
  
  [2] Информация о городах записывается в следующем формате: человек через пробел вводит 3 параметра - город А, город Б и расстояние между ними
  Таким образом последовательно составляется матрица связей, что-то типа графа, пример:
  [Откуда] [Куда] [Цена проезда]: А Б 3 (из города А в Б 3 километра)<br><hr>
  [Откуда] [Куда] [Цена проезда]: Б С 10.5 (из города Б в С 10.5 километров)
  [Откуда] [Куда] [Цена проезда]: С А 7 (из города С в А 7 километров)
  
  [3] На финальном этапе программа спрашивает у человека номер города, с которого отправляется в путешествие коммивояжёр. Затем выводится ответ в виде визуального графа
  Программа генерирует 3 графа:
  • Обычный граф со всеми городами и расстояниями между ними (схема, карта)
  • Тот же граф, поверх которого подсвечена самая оптимальная траектория (по методу ближайшего соседа)
  • Тот же граф, поверх которого подсвечена самая оптимальная траеткория (по переборному решению)
  
  ВНИМАНИЕ: По условию задачи все города попарно связаны, а значит, что если человек забудет указать связь между двумя существущими городами - программа об этом скажет, никаких проблем не возникнет
