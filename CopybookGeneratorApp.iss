; Copy book generator

[Setup]
AppName=字帖生成器 V1.1
AppVersion=1.1
DefaultDirName={pf}\CopybookGenerator
DefaultGroupName=字帖生成器
DisableProgramGroupPage=yes
Compression=lzma2
SolidCompression=yes
OutputDir=app_dist
OutputBaseFilename=copybook_generator_setup_v1.1

[Files]
Source: "dist\*"; DestDir: "{app}"

[Icons]
Name: "{group}\字帖生成器"; Filename: "{app}\CopybookGeneratorApp.exe"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
