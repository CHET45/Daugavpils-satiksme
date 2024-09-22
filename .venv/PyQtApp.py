import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Создаем веб-виджет для отображения карты
        self.browser = QWebEngineView()

        # Получаем абсолютный путь к файлу
        map_path = os.path.abspath("nyc_map.html")
        self.browser.setUrl(QUrl.fromLocalFile(map_path))

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
