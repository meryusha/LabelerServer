echo "Compile Qt GUI files"
pyuic5 -x src/gui/mainwindow.ui -o src/gui/mainwindow.py
pyrcc5 src/resources.qrc -o src/resources.py

echo "Build distribution"
rm -r dist
rm -r build
pyinstaller -F src/ActiveImageLabeler.py

echo "Run distribution"
./dist/ActiveImageLabeler
