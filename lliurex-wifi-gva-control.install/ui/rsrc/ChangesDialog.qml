import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: customDialog
    property alias dialogVisible:customDialog.visible
    property alias dialogMsg:dialogText.text
    property alias btnAcceptVisible:dialogApplyBtn.visible
    property alias btnDiscardVisible:dialogDiscardBtn.visible
    property alias btnDiscardText:dialogDiscardBtn.text
    property alias btnDiscardIcon:dialogDiscardBtn.icon.name
    property alias btnCancelText:dialogCancelBtn.text
    property alias btnCancelIcon:dialogCancelBtn.icon.name
    signal dialogApplyClicked
    signal discardDialogClicked
    signal cancelDialogClicked

    visible:dialogVisible
    modal:true
    anchors.centerIn: Overlay.overlay
    closePolicy:Popup.NoAutoClose
    background:Rectangle{
        color:"#ebeced"
        border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }
    
    contentItem: Rectangle {
        color: "#ebeced"
        implicitWidth: 420
        implicitHeight: 105
        anchors.topMargin:5
        anchors.leftMargin:5

        Image{
            id:dialogIcon
            source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"

        }
        
        Text {
            id:dialogText
            text:dialogMsg
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            width:330
            wrapMode:Text.WordWrap
            anchors.left:dialogIcon.right
            anchors.verticalCenter:dialogIcon.verticalCenter
            anchors.leftMargin:10
        
        }
      
        RowLayout {
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:15
            spacing:10

            Button {
                id:dialogApplyBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text: i18nd("lliurex-wifi-gva-control","Apply")
                visible: btnAcceptVisible 
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Keys.onReturnPressed: dialogApplyBtn.clicked()
                Keys.onEnterPressed: dialogApplyBtn.clicked()
                onClicked:{
                    dialogApplyClicked()
                }

            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text:btnDiscardText
                visible:btnDiscardVisible
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Keys.onReturnPressed: dialogDiscardBtn.clicked()
                Keys.onEnterPressed: dialogDiscardBtn.clicked()
                onClicked:{
                    discardDialogClicked()
                }


            }

            Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnCancelIcon
                text:btnCancelText 
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Keys.onReturnPressed: dialogCancelBtn.clicked()
                Keys.onEnterPressed: dialogCancelBtn.clicked()
                onClicked:{
                    cancelDialogClicked()
                }
        
            }

        }
    }
 }
