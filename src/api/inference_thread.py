from PyQt4.QtCore import QThread


class InferenceThread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        # your logic here