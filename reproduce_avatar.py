
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtCore import QUrl, QTimer

app = QApplication(sys.argv)
manager = QNetworkAccessManager()

# Test URL (Gravatar - usually works)
test_url = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"

def on_finished(reply):
    if reply.error() == QNetworkReply.NetworkError.NoError:
        print(f"Success! Downloaded {len(reply.readAll())} bytes")
    else:
        print(f"Error: {reply.errorString()}")
    app.quit()

req = QNetworkRequest(QUrl(test_url))
# Simulating the missing User-Agent (which is the current state)
# req.setRawHeader(b"User-Agent", b"Mozilla/5.0 ...") 

print(f"Testing URL: {test_url}")
reply = manager.get(req)
reply.finished.connect(lambda: on_finished(reply))

# Timeout
QTimer.singleShot(5000, app.quit)

app.exec()
