echo "Compile Qt GUI files"
pyuic5 -x src/mainwindow.ui -o src/mainwindow.py

echo "Run source"
python src/ActiveImageLabeler.py
