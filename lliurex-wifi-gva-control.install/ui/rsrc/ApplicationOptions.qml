import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:160
        Layout.minimumHeight:370
        Layout.preferredHeight:370
        Layout.fillHeight:true
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:2 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:wifiItem
                optionText:i18nd("lliurex-wifi-gva-control","Configuration")
                optionIcon:"/usr/share/icons/breeze/actions/16/configure.svg"
                optionEnabled:true
                Connections{
                    function onMenuOptionClicked(){
                        wifiControlBridge.manageTransitions(0)
                    }
                }
            }

            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("lliurex-wifi-gva-control","Help")
                optionIcon:"/usr/share/icons/breeze/actions/16/help-contents.svg"
                Connections{
                    function onMenuOptionClicked(){
                        wifiControlBridge.openHelp();
                    }
                }
            }
        }
    }

    StackView{
        id: optionsView
        property int currentIndex:wifiControlBridge.currentOptionsStack
        Layout.fillWidth:true
        Layout.fillHeight: true
        Layout.alignment:Qt.AlignHCenter
       
        initialItem:wifiView

        onCurrentIndexChanged:{
            switch (currentIndex){
                case 0:
                    optionsView.replace(wifiView)
                    break;
             }
        }

        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 600
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 600
            }
        }

        Component{
            id:wifiView
            WifiOptions{
                id:wifiOptions
            }
        }

    }
}

