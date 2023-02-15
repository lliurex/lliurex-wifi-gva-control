import QtQuick 2.15      
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3


Dialog {
    id: customDialog
    property alias dialogTitle:customDialog.title
    property alias dialogVisible:customDialog.visible
    property alias dialogMsg:dialogText.text
    property alias btnAcceptVisible:dialogApplyBtn.visible
    property alias btnDiscardText:dialogDiscardBtn.text
    property alias btnDiscardIcon:dialogDiscardBtn.icon.name
    signal dialogApplyClicked
    signal discardDialogClicked
    signal cancelDialogClicked

    visible:dialogVisible
    title:dialogTitle
    modality:Qt.WindowModal

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
            anchors.left:dialogIcon.right
            anchors.verticalCenter:dialogIcon.verticalCenter
            anchors.leftMargin:10
        
        }
      
        DialogButtonBox {
            buttonLayout:DialogButtonBox.KdeLayout
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:15

            Button {
                id:dialogApplyBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text: i18nd("lliurex-wifi-gva-control","Apply")
                visible: btnAcceptVisible 
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                Keys.onReturnPressed: dialogApplyBtn.clicked()
                Keys.onEnterPressed: dialogApplyBtn.clicked()

            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text:btnDiscardText
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
                Keys.onReturnPressed: dialogDiscardBtn.clicked()
                Keys.onEnterPressed: dialogDiscardBtn.clicked()


            }

            Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel.svg"
                text: i18nd("lliurex-wifi-gva-control","Cancel")
                focus:true
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                Keys.onReturnPressed: dialogCancelBtn.clicked()
                Keys.onEnterPressed: dialogCancelBtn.clicked()
        
            }

            onApplied:{
                dialogApplyClicked()
            }

            onDiscarded:{
                discardDialogClicked()
            }

            onRejected:{
                cancelDialogClicked()
            }
        }
    }
 }
