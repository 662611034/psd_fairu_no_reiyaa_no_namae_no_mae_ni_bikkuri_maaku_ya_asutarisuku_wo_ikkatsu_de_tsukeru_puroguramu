# 「.psdファイルのレイヤーの名前の前に「!」や「*」を一括で付けるプログラム」を簡単にexe化するためのMakefile
# command: make exe
# Git Bashではデフォルトで"mingw32-make"という長ったらしい名前になっているため、エイリアスを作っておくと楽
# 日付部分も自動で処理するようになっているけれど、regist.bat内の日付は変わらないのでそこだけ手動

# 日付部分を取得しておく
today = ${shell date '+%y%m%d'}
title = psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu_${today}.exe

exe:
	pyinstaller -F --noupx --clean __main__.py --name ${title}
	mv --update --verbose ./dist/${title} .
