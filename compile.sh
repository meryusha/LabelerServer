echo "Compile Qt GUI files"
pyuic5 -x src/mainwindow.ui -o src/mainwindow.py
pyrcc5 src/resources.qrc -o src/resources.py

echo "Run source"
python src/ActiveImageLabeler.py
