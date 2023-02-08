import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami


Rectangle{
    visible: true
    Layout.fillWidth:true
    Layout.fillHeight: true
    color:"transparent"

    GridLayout{
        id: loadGrid
        rows: 3
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible: wifiControlBridge.showSpinner

            Rectangle{
                color:"transparent"
                width:30
                height:30
                
                AnimatedImage{
                    source: "/usr/share/lliurex-wifi-gva-control/rsrc/loading.gif"
                    transform: Scale {xScale:0.45;yScale:0.45}
                }
            }
        }

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible: wifiControlBridge.showSpinner
            Text{
                id:loadtext
                text:i18nd("lliurex-wifi-gva-control", "Loading. Wait a moment...")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }

        Kirigami.InlineMessage {
            id: errorLabel
            visible:!wifiControlBridge.showSpinner
            text:i18nd("lliurex-wifi-gva-control","Error loading configuration")
            type:Kirigami.MessageType.Error;
            Layout.minimumWidth:640
            Layout.fillWidth:true
            Layout.rightMargin:15
            Layout.leftMargin:15
        }
    }
}
