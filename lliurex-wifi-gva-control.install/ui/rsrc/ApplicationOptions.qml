import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


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
                optionIcon:"/usr/share/icons/breeze/actions/22/configure.svg"
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
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
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
                duration: 60
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 60
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

