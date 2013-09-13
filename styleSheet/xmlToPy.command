ABSPATH=$(cd "$(dirname "$0")"; pwd)
echo $ABSPATH
/usr/local/Cellar/pyside-tools/0.2.14/bin/pyside-rcc $ABSPATH/icons.xml -o $ABSPATH/icons.py

