@echo off
chcp 932
rem 「PSDファイルのレイヤーを編集」をレジストリに登録するバッチファイル

setlocal
set APP_PATH=%~dp0psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu_201207.exe
set COMMAND1=\"%APP_PATH%\"
set COMMAND2=\"%%1\"
set COMMAND3=%COMMAND1% %COMMAND2%
echo %COMMAND1% %COMMAND2%

rem reg add "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.psd\Shell\PSDファイルのレイヤーを編集" /v "Icon" /t REG_SZ /d "%APP_PATH%" /f
reg add "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.psd\Shell\PSDファイルのレイヤーを編集\command" /ve /t REG_SZ /d "%COMMAND3%" /f
