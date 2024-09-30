import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
import os

from pandas.io.json import to_json


class StationFinder(QObject):

    def readFile(self):
        try:
            # Чтение файла "Stations.txt"
            with open('Stations.txt', 'r', encoding='utf-8') as file:
                data = file.read()
            return data
        except Exception as e:
            return str(e)

    @pyqtSlot(str,result=list)
    def findStation(self,station=None):
        if "\""in station:
            station=station.replace("\"","*")
        try:
            stations=eval(self.readFile())
            if station in stations.keys():
                return stations[station]
            else:
                print("No station")
                return []
        except Exception as e:
            print(f"Error occurred: {e}")
            return []

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создаем веб-виджет для отображения карты
        self.browser = QWebEngineView()

        # Получаем абсолютный путь к файлу
        map_path = os.path.abspath("nyc_map.html")
        self.browser.setUrl(QUrl.fromLocalFile(map_path))

        # Настраиваем веб-канал для взаимодействия с JavaScript
        self.channel = QWebChannel()
        self.station_finder = StationFinder()
        self.channel.registerObject('station_finder', self.station_finder)
        self.browser.page().setWebChannel(self.channel)

        # Добавляем веб-виджет на главный экран
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Карта Folium в PyQt5")
        self.resize(800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
