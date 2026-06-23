import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami

Rectangle{
    id: rectLayout
    color:"transparent"

    Timer{
        id:debounceTimer
        interval:500
        repeat:false
        property var callback
        onTriggered: if (callback) callback()
    }
    
    ColumnLayout{
        id:generalLayout
        anchors.top:parent.top
        anchors.left:parent.left
        anchors.right:parent.right
        anchors.bottom:btnBox.top

        anchors.leftMargin:5
        anchors.rightMargin:15
        anchors.bottomMargin:25
        spacing: 10
        
        Text{ 
            text:i18nd("lliurex-wifi-gva-control","WIFI GVA connection configuration")
            font.pointSize: 16
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible:wifiControlBridge.showSettingsMessage.show
            text:getMessageText(wifiControlBridge.showSettingsMessage.msgCode)
            type:getTypeMessage(wifiControlBridge.showSettingsMessage.type)
            Layout.fillWidth:true
        }

        ColumnLayout{
            id: optionsGrid
            spacing:5

            CheckBox {
                id:enableWifiCb
                text:i18nd("lliurex-wifi-gva-control","Activate automatic connection to the Wifi (WIFI_EDU) at login")
                checked:wifiControlBridge.isWifiEnabled
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                Keys.onReturnPressed: enableWifiCb.toggled()
                Keys.onEnterPressed: enableWifiCb.toggled()
                onToggled:{
                   wifiControlBridge.manageWifiControl(checked)
                   confirmPasswordValue.text=""
                }

                Layout.alignment:Qt.AlignLeft
            }

            Text{ 
                text:i18nd("lliurex-wifi-gva-control","Access mode:")
                font.pointSize: 10
                Layout.leftMargin:25
                Layout.fillWidth:true
            }

            ColumnLayout{
                id:wifiOptions
                spacing:5
                Layout.leftMargin:25
                Layout.alignment:Qt.AlignLeft | Qt.AlingTop

                ButtonGroup{
                    buttons:wifiOptions.children

                }

                RadioButton{
                    id:defaultOption
                    checked:getWifiOption(1)
                    enabled:enableWifiCb.checked
                    text:i18nd("lliurex-wifi-gva-control","Access using user credentials")
                    onToggled:{
                        wifiControlBridge.manageWifiOptions(1)
                        confirmPasswordValue.text=""
                    }
                }

                RadioButton{
                    id:autoLoginOption
                    checked:getWifiOption(3)
                    enabled:enableWifiCb.checked
                    text:i18nd("lliurex-wifi-gva-control","Automatic login with alumnat user")
                    onToggled:{
                        wifiControlBridge.manageWifiOptions(3)
                        confirmPasswordValue.text=""
                    }
                }
            }
        }

        GridLayout{
            id: passwordGrid
            columns: 2
            flow: GridLayout.LeftToRight
            Layout.alignment:Qt.AlignHCenter
            Layout.leftMargin:50
            
            Text{
                id:password
                Layout.alignment:Qt.AlignRight
                text:i18nd("lliurex-wifi-gva-control","Password:")
                font.pointSize: 10
            }
            
            RowLayout{
                TextField{
                    id:passwordValue
                    font.pointSize:10
                    horizontalAlignment:TextInput.AlignLeft
                    focus:true
                    text:wifiControlBridge.currentPassword
                    readOnly:!wifiControlBridge.passwordEntryEnabled
                    implicitWidth:200
                    echoMode:TextInput.Password

                    onTextChanged:{
                        debounceTimer.callback= ()=>wifiControlBridge.changeInPasswordEntry({"password":passwordValue.text,"confirmPassword":confirmPasswordValue.text})
                        debounceTimer.restart()
                    }
                }

                Button {
                    id:showPasswdBtn
                    display:AbstractButton.IconOnly
                    icon.name:getConfiguration(passwordValue.echoMode,"iconName")
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:getConfiguration(passwordValue.echoMode,"toolTip")
                    hoverEnabled:true
                    visible:enableWifiCb.checked && autoLoginOption.checked
                    enabled: visible && passwordValue.text!==""
                    onClicked:{
                        passwordValue.echoMode=(passwordValue.echoMode===TextInput.Password)
                        ? TextInput.Normal
                        :TextInput.Password
                    }
                }

                Button {
                    id:editPasswdBtn
                    display:AbstractButton.IconOnly
                    icon.name:!wifiControlBridge.passwordEntryEnabled?"document-edit":"dialog-cancel"
                    visible:wifiControlBridge.showEditPasswordBtn
                    hoverEnabled:true
                    enabled: enableWifiCb.checked && autoLoginOption.checked
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text: !wifiControlBridge.passwordEntryEnabled
                                   ?i18nd("lliurex-wifi-gva-control","Click to edit password")
                                   :i18nd("lliurex-wifi-gva-control","Click to cancel password editing")
                    onClicked:{
                        wifiControlBridge.editPasswordBtn()
                    }
                }

                Button {
                    id:clearPasswdBtn
                    display:AbstractButton.IconOnly
                    icon.name:"edit-clear"
                    visible:wifiControlBridge.showClearPasswordBtn
                    enabled:true
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("lliurex-wifi-gva-control","Click to clear password")
                    hoverEnabled:true
                    onClicked:{
                        clearPasswordDialog.open()
                    }
                }
            }
                
            Text{
                id:confirmPassword
                text:i18nd("lliurex-wifi-gva-control","Confirm password:")
                font.pointSize: 10
                visible: wifiControlBridge.showConfirmPassword
            }
                
            RowLayout{
                id:confirmPasswordRow
                visible: wifiControlBridge.showConfirmPassword
                
                TextField{
                    id:confirmPasswordValue

                    font.pointSize:10
                    horizontalAlignment:TextInput.AlignLeft
                    focus:true
                    implicitWidth:200
                    echoMode:TextInput.Password

                    onVisibleChanged:{
                        confirmPasswordValue.text=""
                    }

                    onTextChanged:{
                        
                        if (confirmPasswordValue.text===""){
                            return   
                        }

                        debounceTimer.callback= ()=>wifiControlBridge.changeInConfirmPasswordEntry({"password":passwordValue.text,"confirmPassword":confirmPasswordValue.text})
                        debounceTimer.restart()
                    }
                }

                Button {
                    id:showConfirmPasswdBtn
                    display:AbstractButton.IconOnly
                    icon.name:getConfiguration(confirmPasswordValue.echoMode,"iconName")
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:getConfiguration(confirmPasswordValue.echoMode,"toolTip")
                    hoverEnabled:true
                    enabled:confirmPasswordValue.text!==""?true:false
                    onClicked:{
                       confirmPasswordValue.echoMode=(confirmPasswordValue.echoMode===TextInput.Password)
                          ?TextInput.Normal
                          :TextInput.Password
                    }
                }
            }
        }

        Item { Layout.fillHeight: true }

    }

    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.margins:15
        spacing:10

        Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok"
            text:i18nd("lliurex-wifi-gva-control","Apply")
            enabled:wifiControlBridge.changesInWifiSettings 
                    ?true
                    :false
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                closeTimer.stop()
                wifiControlBridge.applyChanges()
                
            }
        }

        Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel"
            text:i18nd("lliurex-wifi-gva-control","Cancel")
            enabled:wifiControlBridge.changesInWifiSettings
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                closeTimer.stop()
                wifiControlBridge.cancelChanges()
            }
        }
    } 

    ChangesDialog{
        id:wifiChangesDialog
        dialogVisible:wifiControlBridge.showChangesDialog
        dialogMsg:i18nd("lliurex-wifi-gva-control","The are pending changes to apply.\nDo you want apply the changes or discard them?")
        btnAcceptVisible:true
        btnDiscardText:i18nd("lliurex-wifi-gva-control","Discard")
        btnDiscardVisible:true
        btnDiscardIcon:"delete"
        btnCancelText:i18nd("lliurex-wifi-gva-control","Cancel")
        btnCancelIcon:"dialog-cancel"
        Connections{
            target:wifiChangesDialog
            function onDialogApplyClicked(){
                wifiControlBridge.manageChangesDialog("Accept")
            }
            function onDiscardDialogClicked(){
                wifiControlBridge.manageChangesDialog("Discard")
            }
            function onRejectDialogClicked(){
                closeTimer.stop()
                wifiControlBridge.manageChangesDialog("Cancel")
            }

        }
    }

    ChangesDialog{
        id:clearPasswordDialog
        dialogVisible:false
        dialogMsg:i18nd("lliurex-wifi-gva-control","Do you want to delete the password for alumnat user?")
        btnAcceptVisible:false
        btnDiscardVisible:true
        btnDiscardText:i18nd("lliurex-wifi-gva-control","Accept")
        btnDiscardIcon:"dialog-ok"
        btnCancelText:i18nd("lliurex-wifi-gva-control","Cancel")
        btnCancelIcon:"dialog-cancel"
        Connections{
            target:clearPasswordDialog
            function onDiscardDialogClicked(){
                clearPasswordDialog.close()
                wifiControlBridge.clearPassword()
            }
            function onRejectDialogClicked(){
                clearPasswordDialog.close()
            }

        }
    }
    ChangesDialog{
        id:cdcWarning
        dialogVisible:wifiControlBridge.showCDCWarning
        dialogMsg:i18nd("lliurex-wifi-gva-control","It is necessary to activate the integration with Digital Identitiy to be able to log in with WIFI GVA")
        btnAcceptVisible:false
        btnDiscardVisible:false
        btnCancelText:i18nd("lliurex-wifi-gva-control","Close")
        btnCancelIcon:"dialog-close"
        Connections{
            target:cdcWarning
            function onRejectDialogClicked(){
                wifiControlBridge.manageCDCWarning()
            }

        }
    }

    CustomPopup{
        id:synchronizePopup
    }

    function getMessageText(code){

        switch (code){
            case 10:
                return i18nd("lliurex-wifi-gva-control","Changes applied successfully");
            case 20:
                return i18nd("lliurex-wifi-gva-control","It is necessary to activate the integration with Digital Identity to be able to log in with WIFI GVA")
            case -10:
                return i18nd("lliurex-wifi-gva-control","Error changing WIFI settings")
            case -20:
                return i18nd("lliurex-wifi-gva-control","Error changing password for autologin")
            case -30:
                return i18nd("lliurex-wifi-gva-control","Error changing autogin activation")
            case -40:
                return i18nd("lliurex-wifi-gva-control","Multiple errors have ocurred while applying changes")
            case -50:
                return i18nd("lliurex-wifi-gva-control","Passwords must match")
            case -60:
                return i18nd("lliurex-wifi-gva-control","You must enter a password")
            case -70:
                return i18nd("lliurex-wifi-gva-control","Error reloading configuration")
            default:
                return ""
        }

    }

    function getTypeMessage(msgType) {
        switch (msgType) {
            case 0:
                return Kirigami.MessageType.Positive
            case 1:
                return Kirigami.MessageType.Error
            case 2:
                return Kirigami.MessageType.Warning
            case 3:
                return Kirigami.MessageType.Information
           default:
                return Kirigami.MessageType.Information
        }
    }

    function getWifiOption(option){

        const currentOption=wifiControlBridge.currentWifiOption

        if (currentOption === 1 || currentOption === 2){
            return option === 1
        }

        if (currentOption === 3){
            return option === 3
        }

        return false
       
    }

    function getConfiguration(echoMode,type){

        const isPasswordHidden= (echoMode===TextInput.Password)

        if (type=="toolTip"){
            return isPasswordHidden
                ? i18nd("lliurex-wifi-gva-control","Click to show password")
                : i18nd("lliurex-wifi-gva-control","Click to hide password")
        }

        return isPasswordHidden?"visibility":"view-hidden"
        
    }

} 
