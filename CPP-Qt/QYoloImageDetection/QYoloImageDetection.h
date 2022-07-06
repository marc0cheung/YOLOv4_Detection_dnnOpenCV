#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_QYoloImageDetection.h"

class QYoloImageDetection : public QMainWindow
{
    Q_OBJECT

public:
    QYoloImageDetection(QWidget *parent = nullptr);
    void Socket_SendCoord(std::string sendData);
    ~QYoloImageDetection();

public slots:
    // For Buttons
    void on_SelcPathBtn_Selected();
    void on_detect_btn_Selected();
    void on_saveThresholdBtn_Selected();
    void on_SavePathBtn_Selected();

    void on_save_cap_Selected();
    void on_segment_save_Selected();
    
    void on_cfgFileBtn_Selected();
    void on_namesFileBtn_Selected();
    void on_weightsFileBtn_Selected();

    void on_loopBtn_Selected();

    // For CheckBox
    void on_showNames_checkbox_Changed(int state);
    void on_objIndex_checkbox_Changed(int state);
    void on_showBBox_checkbox_Changed(int state);
    void on_openSocketCheckbox_Changed(int state);
    
private:
    Ui::QYoloImageDetectionClass ui;
};
