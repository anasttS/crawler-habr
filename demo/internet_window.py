from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QMainWindow


class InternetWindow(QMainWindow):
    def __init__(self, link, *args, **kwargs ):
        self.link = link
        super(InternetWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.link))
        self.setCentralWidget(self.browser)