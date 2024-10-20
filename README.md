# 本项目基于 PIME 移植原苹果 Mac 系统上 [哈利路亚英文输入法](https://github.com/dongyuwei/hallelujahIM) 到 Windows 平台上。

# 哈利路亚英文输入法
![Platform:windows](https://img.shields.io/badge/platform-windows-blue)
![github actions](https://github.com/dongyuwei/Hallelujah-Windows/actions/workflows/ci.yaml/badge.svg)
[![Build status](https://ci.appveyor.com/api/projects/status/ch2ojcgq10gk3622?svg=true)](https://ci.appveyor.com/project/dongyuwei/hallelujah-windows)

哈利路亚英文输入法 是一款智能英语输入法。其特性如下：

1. 离线词库较大较全，词频精准。参见 Google's [1/3 million most frequent English words](http://norvig.com/ngrams/count_1w.txt).
2. 内置拼写校正功能。不用担心拼写错误，能记住大概字形、发音，本输入法就会自动显示最可能的候选词。
3. 即时翻译功能(显示音标，及英文单词的中文释义)。
4. 支持按拼音来输出对应英文。如输入`suanfa`，输入法会候选词中会显示 `algorithm`。
5. 支持按英文单词的模糊音来输入。 如输入 `kerrage` 可以得到 `courage` 候选词，也可以输入 `aosome` 或者 `ausome` 来得 `awesome` 候选词。
6. 具备 Text-Expander 功能。 本输入法会自动读取定义在用户目录下的`C:\Users\<user>\hallelujah.json` 文件，你可以定义自己常用的词组，比如 `{"yem":"you expand me"}`，那么当输入 `yem` 时会显示 `you expand me` 。
7. 选词方式：数字键 1~9 及 `Enter` 回车键和 `Space` 空格键均可选词提交。`Space` 空格键选词默认会自动附加一个空格在单词后面。`Enter` 回车键选词则不会附加空格。

# 下载安装

-   https://github.com/dongyuwei/Hallelujah-Windows/releases

## Build and compile with Visual Studio 2019

1. 安装 cmake（tested with `cmake version 3.25.0-rc2`）
2. 项目根目录下执行 ./build.bat
3. 使用 NSIS 构建 install exe 文件：
    1. Compile NSI scripts
    2. File -> Load script... -> installer/installer.nsi
4. CI 构建可参考 appveyor.yml

## 更好的 IPC 架構

https://github.com/EasyIME/forum/issues/11

## 开发(reload ime service)

参考： https://github.com/EasyIME/PIME/issues/50
已经安装的输入法，如果需要修改生效，则结束 node 或者 python 进程即可，会自动重启新进程（在任务管理器在可以查看进程的 pid 发生了变化）。

## Log 日志(win 11 中可以搜索 `%AppData%` 快速定位到)

C:\Users\<user>\AppData\Local\PIME\Log

## pip install packages
- I use Python 3.11.1
-   python/python3/virtualenv/Scripts/python.exe -m pip install -U pyphonetics
-   python/python3/virtualenv/Scripts/python.exe -m pip freeze > requirements.txt
-   python/python3/virtualenv/Scripts/python.exe -m pip install -r requirements.txt

# 以下为 PIME 原项目文档

Implement input methods easily for Windows via Text Services Framework:

-   LibIME contains a library which aims to be a simple wrapper for Windows Text Service Framework (TSF).
-   PIMETextService contains an backbone implementation of Windows text service for using libIME.
-   The python server part requires python 3.x and pywin32 package.

All parts are licensed under GNU LGPL v2.1 license.

# Development

## Tool Requirements

-   [CMake](http://www.cmake.org/) >= 3.0
-   [Visual Studio 2019](https://visualstudio.microsoft.com/vs)
-   [git](http://windows.github.com/)

## How to Build

-   Get source from github.

        git clone https://github.com/EasyIME/PIME.git
        cd PIME
        git submodule update --init

-   Use the following CMake commands to generate Visual Studio project.

        cmake -G "Visual Studio 16 2019" -A Win32 <path to PIME source folder>
        cmake -G "Visual Studio 16 2019" -A x64 <path to PIME source folder>

-   Open generated project with Visual Studio and build it.

## TSF References

-   [Text Services Framework](http://msdn.microsoft.com/en-us/library/windows/desktop/ms629032%28v=vs.85%29.aspx)
-   [Guidelines and checklist for IME development (Windows Store apps)](http://msdn.microsoft.com/en-us/library/windows/apps/hh967425.aspx)
-   [Input Method Editors (Windows Store apps)](http://msdn.microsoft.com/en-us/library/windows/apps/hh967426.aspx)
-   [Third-party input method editors](http://msdn.microsoft.com/en-us/library/windows/desktop/hh848069%28v=vs.85%29.aspx)
-   [Strategies for App Communication between Windows 8 UI and Windows 8 Desktop](http://software.intel.com/en-us/articles/strategies-for-app-communication-between-windows-8-ui-and-windows-8-desktop)
-   [TSF Aware, Dictation, Windows Speech Recognition, and Text Services Framework. (blog)](http://blogs.msdn.com/b/tsfaware/?Redirected=true)
-   [Win32 and COM for Windows Store apps](http://msdn.microsoft.com/en-us/library/windows/apps/br205757.aspx)
-   [Input Method Editor (IME) sample supporting Windows 8](http://code.msdn.microsoft.com/windowsdesktop/Input-Method-Editor-IME-b1610980)

## Windows ACL (Access Control List) references

-   [The Windows Access Control Model Part 1](http://www.codeproject.com/Articles/10042/The-Windows-Access-Control-Model-Part-1#SID)
-   [The Windows Access Control Model: Part 2](http://www.codeproject.com/Articles/10200/The-Windows-Access-Control-Model-Part-2#SidFun)
-   [Windows 8 App Container Security Notes - Part 1](http://recxltd.blogspot.tw/2012/03/windows-8-app-container-security-notes.html)
-   [How AccessCheck Works](http://msdn.microsoft.com/en-us/library/windows/apps/aa446683.aspx)
-   [GetAppContainerNamedObjectPath function (enable accessing object outside app containers using ACL)](http://msdn.microsoft.com/en-us/library/windows/desktop/hh448493)
-   [Creating a DACL](http://msdn.microsoft.com/en-us/library/windows/apps/ms717798.aspx)

# Install

-   Copy `PIMETextService.dll` to C:\Program Files (X86)\PIME\x86\.
-   Copy `PIMETextService.dll` to C:\Program Files (X86)\PIME\x64\.
-   Copy the folder `python` to `C:\Program Files (X86)\PIME\`
-   Copy the folder `node` to `C:\Program Files (X86)\PIME\`
-   Use `regsvr32` to register `PIMETextService.dll`. 64-bit system need to register both 32-bit and 64-bit `PIMETextService.dll`

        regsvr32 "C:\Program Files (X86)\PIME\x86\PIMETextService.dll" (run as administrator)
        regsvr32 "C:\Program Files (X86)\PIME\x64\PIMETextService.dll" (run as administrator)

-   NOTICE: the `regsvr32` command needs to be run as Administrator. Otherwise you'll get access denied error.
-   In Windows 8, if you put the dlls in places other than C:\Windows or C:\Program Files, they will not be accessible in metro apps.

# Uninstall

-   Use `regsvr32` to unregister `PIMETextService.dll`. 64-bit system need to unregister both 32-bit and 64-bit `PIMETextService.dll`

        regsvr32 /u "C:\Program Files (X86)\PIME\x86\PIMETextService.dll" (run as administrator)
        regsvr32 /u "C:\Program Files (X86)\PIME\x64\PIMETextService.dll" (run as administrator)

-   Remove `C:\Program Files (X86)\PIME`

-   NOTICE: the `regsvr32` command needs to be run as Administrator. Otherwise you'll get access denied error.

# Bug Report

Please report any issue to [here](https://github.com/EasyIME/PIME/issues).
