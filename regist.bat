@echo off
chcp 932
rem �uPSD�t�@�C���̃��C���[��ҏW�v�����W�X�g���ɓo�^����o�b�`�t�@�C��

setlocal
set APP_PATH=%~dp0psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu_220811.exe
set COMMAND1=\"%APP_PATH%\"
set COMMAND2=\"%%1\"
set COMMAND3=%COMMAND1% %COMMAND2%
echo %COMMAND1% %COMMAND2%

rem reg add "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.psd\Shell\PSD�t�@�C���̃��C���[��ҏW" /v "Icon" /t REG_SZ /d "%APP_PATH%" /f
reg add "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.psd\Shell\PSD�t�@�C���̃��C���[��ҏW\command" /ve /t REG_SZ /d "%COMMAND3%" /f
