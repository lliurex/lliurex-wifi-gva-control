import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-wifi-gva-control","WIFI GVA connection configuration")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        width:parent.width-10
        anchors.left:parent.left

        Kirigami.InlineMessage {
            id: messageLabel
            visible:wifiControlBridge.showSettingsMessage[0]
            text:getMessageText(wifiControlBridge.showSettingsMessage[1])
            type:getMessageType(wifiControlBridge.showSettingsMessage[2])
            Layout.minimumWidth:490
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 4
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:50

            CheckBox {
                id:enableWifiCb
                text:i18nd("lliurex-wifi-gva-control","Activate automatic connection to the Wifi")
                checked:wifiControlBridge.isWifiEnabled
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                Keys.onReturnPressed: enableWifiCb.toggled()
                Keys.onEnterPressed: enableWifiCb.toggled()
                onToggled:{
                   wifiControlBridge.manageWifiControl(checked)
                }

                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:5
            }
            RowLayout{
                Layout.fillWidth:true
                Layout.leftMargin:26
                Text{ 
                    text:i18nd("lliurex-wifi-gva-control","Default connection:")
                    font.pointSize: 10
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.alignment:Qt.AlignLeft
                Layout.leftMargin:25

                ButtonGroup{
                    buttons:wifiOptions.children

                }

                Column{
                    id:wifiOptions
                    spacing:5
                    Layout.alignment:Qt.AlignTop

                    RadioButton{
                        id:teacherOption
                        checked:getWifiOption(1)
                        enabled:enableWifiCb.checked?true:false
                        text:"WIFI_PROF"
                        onToggled:{
                            wifiControlBridge.manageWifiOptions(1)
                            confirmPasswordValue.text=""
                        }
                    }

                    RadioButton{
                        id:aluOption
                        checked:getWifiOption(2)
                        enabled:enableWifiCb.checked?true:false
                        text:"WIFI_ALU"
                        onToggled:{
                            wifiControlBridge.manageWifiOptions(2)
                            confirmPasswordValue.text=""
                        }
                    }

                    RadioButton{
                        id:autoLoginOption
                        checked:getWifiOption(3)
                        enabled:enableWifiCb.checked?true:false
                        text:"WIFI_ALU: "+i18nd("lliurex-wifi-gva-control","automatic login with alumnat user")
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
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                }
                RowLayout{
                    TextField{
                        id:passwordValue
                        font.pointSize:10
                        horizontalAlignment:TextInput.AlignLeft
                        focus:true
                        text:wifiControlBridge.currentPassword
                        enabled:wifiControlBridge.passwordEntryEnabled
                        implicitWidth:200
                        echoMode:TextInput.Password

                        onTextChanged:{
                            wifiControlBridge.changeInPasswordEntry([passwordValue.text,confirmPasswordValue.text])
                        }
                    }

                     Button {
                        id:showPasswdBtn
                        display:AbstractButton.IconOnly
                        icon.name:getConfiguration(passwordValue.echoMode,"iconName")
                        Layout.preferredHeight: 35
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible: hovered
                        ToolTip.text:getConfiguration(passwordValue.echoMode,"toolTip")
                        visible:{
                            if ((enableWifiCb.checked) && (autoLoginOption.checked)){
                                true
                            }else{
                                false
                            }
                        }
                        enabled:{
                            if ((enableWifiCb.checked) && (autoLoginOption.checked)){
                                if (passwordValue.text!=""){
                                    true
                                }else{
                                    false
                                }
                            }else{
                                false
                            }
                        }
 
                        hoverEnabled:true
                        onClicked:{
                            if (passwordValue.echoMode==2){
                                passwordValue.echoMode=TextInput.Normal
                            }else{
                                passwordValue.echoMode=TextInput.Password
                            }

                        }
                    }

                    Button {
                        id:editPasswdBtn
                        display:AbstractButton.IconOnly
                        icon.name:"document-edit.svg"
                        Layout.preferredHeight: 35
                        visible:wifiControlBridge.showEditPasswordBtn
                        enabled:{
                            if ((enableWifiCb.checked) && (autoLoginOption.checked)){
                                if (wifiControlBridge.currentPassword!=""){
                                    true
                                }else{
                                    false
                                }
                            }else{
                                false
                            }
                        }
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible: hovered
                        ToolTip.text:i18nd("lliurex-wifi-gva-control","Click to change password")
                        hoverEnabled:true
                        onClicked:{
                            wifiControlBridge.editPasswordBtn()
                        }
                    }
                   
                }
                
                Text{
                    id:confirmPassword
                    Layout.alignment:Qt.AlignRight
                    text:i18nd("lliurex-wifi-gva-control","Confirm password:")
                    font.family: "Quattrocento Sans Bold"
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
                        text:""
                        implicitWidth:200
                        echoMode:TextInput.Password

                        onTextChanged:{
                            wifiControlBridge.changeInConfirmPasswordEntry([passwordValue.text,confirmPasswordValue.text])
                        }
                    }

                    Button {
                        id:showConfirmPasswdBtn
                        display:AbstractButton.IconOnly
                        icon.name:getConfiguration(confirmPasswordValue.echoMode,"iconName")
                        Layout.preferredHeight: 35
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible: hovered
                        ToolTip.text:getConfiguration(confirmPasswordValue.echoMode,"toolTip")
                        hoverEnabled:true
                        enabled:{
                            if (confirmPasswordValue.text!=""){
                                true
                            }else{
                                false
                            }
                        }
                        onClicked:{
                            if (confirmPasswordValue.echoMode==2){
                                confirmPasswordValue.echoMode=TextInput.Normal
                            }else{
                                confirmPasswordValue.echoMode=TextInput.Password
                            }

                        }
                    }
                }
            }

        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("lliurex-wifi-gva-control","Apply")
            Layout.preferredHeight:40
            enabled:{
                if ((wifiControlBridge.settingsWifiChanged) && (!wifiControlBridge.errorInPassword)){
                    true
                }else{
                    false
                }
            }
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                applyChanges()
                closeTimer.stop()
                wifiControlBridge.applyChanges()
                
            }
        }
        Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("lliurex-wifi-gva-control","Cancel")
            Layout.preferredHeight: 40
            enabled:{
                if (wifiControlBridge.errorInPassword){
                    true
                }else{
                    if (wifiControlBridge.settingsWifiChanged){
                        true
                    }else{
                        false
                    }
                }
            }
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                discardChanges()
                closeTimer.stop()
                wifiControlBridge.cancelChanges()
            }
        }
    } 

    ChangesDialog{
        id:wifiChangesDialog
        dialogTitle:"Lliurex Wifi GVA Control"+" - "+i18nd("lliurex-wifi-gva-control","Wifi configuration")
        dialogVisible:wifiControlBridge.showChangesDialog
        dialogMsg:i18nd("lliurex-wifi-gva-control","The are pending changes to apply.\nDo you want apply the changes or discard them?")
        Connections{
            target:wifiChangesDialog
            function onDialogApplyClicked(){
                applyChanges()
                
            }
            function onDiscardDialogClicked(){
                discardChanges()
            }
            function onCancelDialogClicked(){
                closeTimer.stop()
            }

        }
    }
    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:delayTimer
    }

    function delay(delayTime,cb){
        delayTimer.interval=delayTime;
        delayTimer.repeat=true;
        delayTimer.triggered.connect(cb);
        delayTimer.start()
    }

    Timer{
        id:waitTimer
    }

    function wait(delayTime,cb){
        waitTimer.interval=delayTime;
        waitTimer.repeat=true;
        waitTimer.triggered.connect(cb);
        waitTimer.start()
    }


    function getMessageText(code){

        var msg="";
        switch (code){
            case 10:
                msg=i18nd("lliurex-wifi-gva-control","Changes applied successfully");
                break;
            case -10:
                msg=i18nd("lliurex-wifi-gva-control","Error changing WIFI settings")
                break;
            case -20:
                msg=i18nd("lliurex-wifi-gva-control","Error changing password for autologin")
                break;
            case -30:
                msg=i18nd("lliurex-wifi-gva-control","Error changing autogin activation")
                break;
            case -40:
                msg=i18nd("lliurex-wifi-gva-control","Multiple errors have ocurred while applying changes")
            case -50:
                msg=i18nd("lliurex-wifi-gva-control","Passwords must match")
                break;
            case -60:
                msg=i18nd("lliurex-wifi-gva-control","You must enter a password")
                break;
            case -70:
                msg=i18nd("lliurex-wifi-gva-control","Error reloading configuration")
                break;
            default:
                break;
        }
        return msg;

    }

    function getMessageType(type){

        switch (type){
            case "Info":
                return Kirigami.MessageType.Information
            case "Success":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
        }

    } 

    function getWifiOption(option){

        switch (wifiControlBridge.currentWifiOption){

            case 1:
                if (option==1){
                    return true
                }else{
                    return false
                }
            case 2:
                if (option==2){
                    return true
                }else{
                    return false
                }
            case 3:
                if (option==3){
                    return true
                }else{
                    return false
                }
        }
    }

    function getConfiguration(echoMode,type){

        var msg=""
        var icon=""
        if (echoMode==0){
            msg=i18nd("lliurex-wifi-gva-control","Click to hide password")
            icon="view-hidden.svg"
        }else{
            msg=i18nd("lliurex-wifi-gva-control","Click to show password")
            icon="visibility.svg" 
        }

        if (type=="toolTip"){
            return msg
        }else{
            return icon
        }

    }

    function applyChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-wifi-gva-control", "Apply changes. Wait a moment...")
        delayTimer.stop()
        delay(500, function() {
            if (wifiControlBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()
                confirmPasswordValue.text=""
            }
        })
    } 

    function discardChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-wifi-gva-control", "Restoring previous values. Wait a moment...")
        delayTimer.stop()
        delay(1000, function() {
            if (wifiControlBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()
                confirmPasswordValue.text=""

            }
        })
    }  
} 
