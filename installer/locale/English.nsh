!define LANG "ENGLISH" ; Must be the lang name define by NSIS

!insertmacro LANG_STRING INSTALLER_LANGUAGE_TITLE "The installer language"
!insertmacro LANG_STRING INSTALL_LANGUAGE_MESSAGE "Please select the installer language"

!insertmacro LANG_STRING PRODUCT_NAME "PIME Input Methods"

!insertmacro LANG_STRING INST_TYPE_STD "Standard installation"
!insertmacro LANG_STRING INST_TYPE_FULL "Full installation"
!insertmacro LANG_STRING MB_REBOOT_REQUIRED "A reboot is required to complete the uninstallation。$\r$\nDo you want to reboot now? (Select $\"No$\" if you want to reboot at a later time)"
!insertmacro LANG_STRING PRODUCT_PAGE "PIME project home page"
!insertmacro LANG_STRING PRODUCT_PUBLISHER "PIME development team"

!insertmacro LANG_STRING AtLeastWinVista_MESSAGE "Sorry，this program currently only supports Windows Vista or later"
!insertmacro LANG_STRING REBOOT_QUESTION "The installation failed and could no be completed.$\r$\nA file may be in use, that prevents it from being deleted or overwritten.$\n$\nIt is recommended that you reboot the system and run the installer again.$\r$\nDo you want to reboot now? (Select $\"No$\" if you want to reboot at a later time)"
!insertmacro LANG_STRING INST_FAILED_MESSAGE "The installation failed and could no be completed.$\n$\rA file may be in use, that prevents it from being deleted or overwritten.$\n$\nIt is recommended that you reboot the system and run the installer again."
!insertmacro LANG_STRING UNINSTALL_OLD "An older version of PIME has been detected. Do you want to remove the old version and continue installing the new version?"
!insertmacro LANG_STRING DOWNLOAD_VCREDIST_QUESTION "This program requires the VC++ Redistributable to run. Would you like to automatically download and install it?"
!insertmacro LANG_STRING DOWNLOAD_VCREDIST_FAILED_MESSAGE "Failed to download VC++ Redistributable try again later, or install it manually"
!insertmacro LANG_STRING INST_VCREDIST_FAILED_MESSAGE "VC++ Redistributable was not installed correctly. Refer to the relevant Microsoft documentation for updates."

!insertmacro LANG_STRING SECTION_MAIN "PIME input method platform"
!insertmacro LANG_STRING PYTHON_SECTION_GROUP "Input method modules with Python"
!insertmacro LANG_STRING PYTHON_CHT_SECTION_GROUP "Traditional Chinese"
!insertmacro LANG_STRING PYTHON_CHS_SECTION_GROUP "Simplified Chinese"
!insertmacro LANG_STRING NODE_SECTION_GROUP "Input method modules with Node"
!insertmacro LANG_STRING NODE_CHT_SECTION_GROUP "Traditional Chinese"
!insertmacro LANG_STRING NODE_CHS_SECTION_GROUP "Simplified Chinese"

!insertmacro LANG_STRING CHEWING "Chewing"
!insertmacro LANG_STRING CHECJ "Cangjie"
!insertmacro LANG_STRING CHELIU "Shiamy (Required: A legal copy of the table file)"
!insertmacro LANG_STRING CHEARRAY "Array"
!insertmacro LANG_STRING CHEDAYI "Dayi"
!insertmacro LANG_STRING CHEPINYIN "Pinyin"
!insertmacro LANG_STRING CHESIMPLEX "Quick"
!insertmacro LANG_STRING CHEPHONETIC "Phonetic"
!insertmacro LANG_STRING CHEEZ "EZ Input"
!insertmacro LANG_STRING RIME "Rime"
!insertmacro LANG_STRING EMOJIME "emojime"
!insertmacro LANG_STRING CHEENG "Eng-Num"
!insertmacro LANG_STRING BRAILLE_CHEWING "Braille Chewing"
!insertmacro LANG_STRING HALLELUHAH "Hallelujah"

!insertmacro LANG_STRING SELECT_LIU_FILE "Installation of Shiamy module requires that you have a legal copy of the table file of Boshiamy input method (liu-uni.tab).$\r$\nPlease provide the location of the liu-uni.tab file."
!insertmacro LANG_STRING CANNOT_INSTALL_LIU "Without liu-uni.tab file, Shiamy input method cannot be installed."

!insertmacro LANG_STRING SecMain_DESC "Install the $(PRODUCT_NAME) main program to your computer."
!insertmacro LANG_STRING PYTHON_SECTION_GROUP_DESC "Input method modules with Python"
!insertmacro LANG_STRING PYTHON_CHT_SECTION_GROUP_DESC "Traditional Chinese"
!insertmacro LANG_STRING PYTHON_CHS_SECTION_GROUP_DESC "Simplified Chinese"
!insertmacro LANG_STRING NODE_SECTION_GROUP_DESC "Input method modules with Node"
!insertmacro LANG_STRING NODE_CHT_SECTION_GROUP_DESC "Traditional Chinese"
!insertmacro LANG_STRING NODE_CHS_SECTION_GROUP_DESC "Simplified Chinese"
!insertmacro LANG_STRING chewing_DESC "Install Chewing input method module."
!insertmacro LANG_STRING checj_DESC "Install Cangjie input method module."
!insertmacro LANG_STRING cheliu_DESC "Install Shiamy input method module."
!insertmacro LANG_STRING chearray_DESC "Install Array input method module."
!insertmacro LANG_STRING chedayi_DESC "Install Dayi input method module."
!insertmacro LANG_STRING chepinyin_DESC "Install Pinyin input method module."
!insertmacro LANG_STRING chesimplex_DESC "Install Quick input method module."
!insertmacro LANG_STRING chephonetic_DESC "Install Phonetic input method module."
!insertmacro LANG_STRING cheez_DESC "Install EZ Input method module."
!insertmacro LANG_STRING rime_DESC "Install Rime input method engine, 内含拼音、注音、仓颉、五笔、粤拼、吴语等数种输入方案。"
!insertmacro LANG_STRING emojime_DESC "Install emojime input method module."
!insertmacro LANG_STRING cheeng_DESC "Install Eng-Num input method module."
!insertmacro LANG_STRING braille_chewing_DESC "Install Braille Chewing input method module."
!insertmacro LANG_STRING hallelujah_DESC "Install Hallelujah input method module."

!insertmacro LANG_STRING SET_CHEWING "Setup Chewing input method"
!insertmacro LANG_STRING SET_CHEWING_PHRASES "Edit Chewing phrases"

!insertmacro LANG_STRING SET_CHECJ "Setup Cangjie input method"
!insertmacro LANG_STRING SET_CHELIU "Setup Shiamy input method"
!insertmacro LANG_STRING SET_CHEARRAY "Setup Array input method"
!insertmacro LANG_STRING SET_CHEDAYI "Setup Dayi input method"
!insertmacro LANG_STRING SET_CHEPINYIN "Setup Pinyin input method"
!insertmacro LANG_STRING SET_CHESIMPLEX "Setup Quick input method"
!insertmacro LANG_STRING SET_CHEPHONETIC "Setup Phonetic input method"
!insertmacro LANG_STRING SET_CHEEZ "Setup EZ Input method"
!insertmacro LANG_STRING SET_BRAILLE_CHEWING "Setup Braille Chewing input method"
!insertmacro LANG_STRING SET_HALLELUHAH "Setup Hallelujah input method"

!insertmacro LANG_STRING UNINSTALL_PIME "Uninstall PIME"