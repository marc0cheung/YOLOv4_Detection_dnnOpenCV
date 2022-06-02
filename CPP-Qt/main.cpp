#include "YOLOCPPSOCKETQt.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    YOLOCPPSOCKETQt w;
    w.show();
    return a.exec();
}
