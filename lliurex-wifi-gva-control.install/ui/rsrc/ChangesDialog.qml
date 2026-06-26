import QtQuick 2.15      
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3
import org.kde.kirigami 2.16 as Kirigami


Dialog {
    id: customDialog
    property bool dialogVisible: false
    property string dialogTitle:""
    property string dialogMsg: ""
    property bool btnAcceptVisible: true
    property string btnAcceptText: ""
    property string btnDiscardText: ""
    property bool btnDiscardVisible: true
    property string btnDiscardIcon: ""
    property string btnCancelText: ""
    property string btnCancelIcon: ""

    signal dialogApplyClicked()
    signal discardDialogClicked()
    signal rejectDialogClicked()

    title: customDialog.dialogTitle
    modality: Qt.WindowModal
    visible:customDialog.dialogVisible

    contentItem: Rectangle {
        color: "#ebeced"
        implicitWidth: 460
        implicitHeight: 115


        RowLayout {
            id: contentLayout
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 0
            spacing: 15

            Kirigami.Icon {
                id: dialogIcon
                source: "dialog-warning"
                Layout.preferredWidth: 64
                Layout.preferredHeight: 64
                visible: status === Image.Ready
            }

            Text {
                id: dialogText
                text: customDialog.dialogMsg
                font.pointSize: 10
                Layout.fillWidth: true
                Layout.rightMargin:10
                wrapMode: Text.WordWrap
            }
        }
      
        DialogButtonBox {
            buttonLayout: DialogButtonBox.KdeLayout
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 10

            Button {
                id:dialogApplyBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok"
                text: i18nd("lliurex-wifi-gva-control","Apply")
                visible: btnAcceptVisible 
                focus:true
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                onClicked: customDialog.dialogApplyClicked()
            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text:btnDiscardText
                visible:btnDiscardVisible
                focus:true
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
                onClicked: customDialog.discardDialogClicked()
            }

            Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnCancelIcon
                text:btnCancelText 
                focus:true
                font.pointSize: 10
                DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
                onClicked: {
                    customDialog.rejectDialogClicked()
                }
        
            }
        }

    }
 }
