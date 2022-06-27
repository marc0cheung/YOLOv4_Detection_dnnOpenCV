#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_YOLOCPPSOCKETQt.h"

class YOLOCPPSOCKETQt : public QMainWindow
{
    Q_OBJECT

public:
    YOLOCPPSOCKETQt(QWidget *parent = Q_NULLPTR);
    void showStartupConfig();
public slots:
    int on_StartBtn_Clicked();
    void on_pauseBtn_Clicked();
    void on_ExitBtn_Clicked();
    void on_clearBtn_Clicked();
    void socketInitialization();

    void on_saveAddrBtn_Clicked();
    void on_saveVideoSizeBtn_Clicked();
    void on_saveThresholdBtn_Clicked();

    void on_cfgFileBtn_Clicked();
    void on_weightsFileBtn_Clicked();
    void on_namesFileBtn_Clicked();

    void on_writeJsonCheckBox_Changed(int state);
    void on_logJsonCheckBox_Changed(int state);
    void on_openSocketCheckBox_Changed(int state);
    void on_logSocketCheckBox_Changed(int state);
    void on_videoStreamCheckBox_Changed(int state);
    void on_videoFlipCheckBox_Changed(int state);
    void on_BoxXCheckBox_Changed(int state);
    void on_runtimeCheckBox_Changed(int state);
    void on_useGPUCheckBox_Changed(int state);
    void on_BBoxCheckBox_Changed(int state);
    void on_NameConfCheckBox_Changed(int state);
    void on_ObjIndexCheckBox_Changed(int state);
private:
    Ui::YOLOCPPSOCKETQtClass ui;
};
