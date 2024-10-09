Перед запуском необходимо устоновить PyQt5, pandas и PyQtWebEngine
pip install PyQt5
pip install PyQtWebEngine
pip install pandas
Главный файл пока что PyQtApp.py. При его запуске откроется окно приложения.
![image](https://github.com/user-attachments/assets/5c82f61f-8306-49ef-8fda-d54d762b07de)

Класс StationFinder в PyQtApp.py выполняет функцию связи HTML карты (а точнее JavaScript части) с файлом Stations.txt.
В Stations.txt хранятся все названия станций и их координаты. В будующем там же будет храниться список транспорта и расписание для каждого транспорта для обоих направлений.
Класс MapWindow в PyQtApp.py создаёт окно приложения с HTML картой (nyc_map.html).
Карта (файл nyc_map.html) создаётся в Map.py.
В Map.py методы exportStations, encodeUrl и getLinkList находят и экспортируют все данные станций с сайта https://satiksme.daugavpils.lv.
  Метод upddateMap создаёт новую карту или перезаписывает файл nyc_map.html.

