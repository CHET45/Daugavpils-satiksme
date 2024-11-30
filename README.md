Перед запуском необходимо устоновить folium, branca, PyQt5 и PyQtWebEngine

pip install folium
pip install branca
pip install PyQt5
pip install PyQtWebEngine

Главный файл пока что PyQtApp.py. При его запуске откроется окно приложения.

![image](https://github.com/user-attachments/assets/5c82f61f-8306-49ef-8fda-d54d762b07de)

Класс StationFinder в PyQtApp.py выполняет функцию связи HTML карты (а точнее JavaScript части) с файлом Stations.txt.

В Stations.txt хранятся сид(id) станций их названия, их координаты, какой транспорт ходит через эту станцию и рассписание.
Структура файла:
{sid:{'name':name, 'pos':pos, 'transport':transport}}
transport = {transportName:[wtime,htime]}
wtime,htime = ["time","time"]
{sid:{'name':name, 'pos':pos, 'transport':{transportName:[["time","time",...],["time","time",...]],...},...},...}


Класс MapWindow в PyQtApp.py создаёт окно приложения с HTML картой (nyc_map.html).

Карта (файл nyc_map.html) создаётся в Map.py.

В Map.py методы checkForSimilarCords, exportStations, encodeUrl, checkForExtraLink, busOrTrain и getLinkList (8 - 109 строки) находят и экспортируют все данные станций с сайта https://satiksme.daugavpils.lv.

  Метод upddateMap создаёт новую карту или перезаписывает файл nyc_map.html.
  Первая часть метода(до переменной menu) создаёт маркеры и всплывающие названия станций.
  Большую часть занимает переменна я menu(156 - 385 строки). В menu создаётся боковое меню и описывается основная логика программы, в том числе и связь с .py файлом.

