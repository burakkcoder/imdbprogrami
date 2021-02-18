import sys
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets

class IMDB(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.imdb_veriler()

    def init_ui(self):
        self.arama_alani = QtWidgets.QLineEdit()
        self.ara = QtWidgets.QPushButton("Ara")
        self.top250 = QtWidgets.QPushButton("TOP 250")
        self.sonuc = QtWidgets.QTextEdit()
        self.temizle = QtWidgets.QPushButton("Temizle")

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.arama_alani)
        h_box.addWidget(self.ara)
        h_box.addWidget(self.temizle)
        h_box.addWidget(self.top250)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addWidget(self.sonuc)

        self.setLayout(v_box)

        self.setWindowTitle("IMDB Programı")

        self.ara.clicked.connect(self.arama)
        self.top250.clicked.connect(self.top)
        self.temizle.clicked.connect(self.temiz)

        self.show()

    def imdb_veriler(self):
        url = "https://www.imdb.com/chart/top/"

        self.response = requests.get(url)

        self.html_icerik = self.response.content

        self.soup = BeautifulSoup(self.html_icerik, "html.parser")

    def arama(self):
        try:
            ara = float(self.arama_alani.text())
            basliklar = self.soup.find_all("td", {"class": "titleColumn"})
            ratingler = self.soup.find_all("td", {"class": "ratingColumn imdbRating"})
            for baslik, rating in zip(basliklar, ratingler):
                baslik = baslik.text
                rating = rating.text

                baslik = baslik.strip()
                baslik = baslik.replace("\n", "")
                rating = rating.strip()
                rating = rating.replace("\n", "")

                if float(rating) > ara:
                    self.sonuc.append("Film İsmi : {} Filmin Ratingi : {}".format(baslik, rating))
        except:
            self.sonuc.setText("Lütfen Ratingi Doğru Şekilde Giriniz. Örnek: 8.5")

    def temiz(self):
        self.sonuc.clear()

    def top(self):
        basliklar = self.soup.find_all("td", {"class": "titleColumn"})
        ratingler = self.soup.find_all("td", {"class": "ratingColumn imdbRating"})
        eklenenler = []
        for baslik, rating in zip(basliklar, ratingler):
            baslik = baslik.text
            rating = rating.text

            baslik = baslik.strip()
            baslik = baslik.replace("\n", "")
            rating = rating.strip()
            rating = rating.replace("\n", "")
            self.sonuc.append("Film İsmi : {} Filmin Ratingi : {}".format(baslik, rating))

app = QtWidgets.QApplication(sys.argv)
imdb = IMDB()
sys.exit(app.exec_())




