@echo off
chcp 932
rem 「PSDファイルのレイヤーを編集」をレジストリから削除するバッチファイル

setlocal

reg delete "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.psd" /f
