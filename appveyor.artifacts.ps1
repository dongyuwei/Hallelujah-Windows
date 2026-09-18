$version = Get-Content version.txt
$filename = "Hallelujah-PIME-$version-setup.exe"
Push-AppveyorArtifact "installer\$filename" -FileName $filename
