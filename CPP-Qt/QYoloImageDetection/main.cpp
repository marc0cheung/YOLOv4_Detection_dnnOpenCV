#include "QYoloImageDetection.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QYoloImageDetection w;
    w.show();
    return a.exec();
}
