# ダウンロード
最新版は[こちら](https://github.com/662611034/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu/releases/download/201002/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu_201002.zip)のリンクからダウンロードできます。容量が大きくて(84MBほど)githubにアップロードできませんでした。   
過去バージョンはアップデート履歴からダウンロードできます。

# このプログラムについて
.psdファイルのレイヤーの名前の先頭に「!」や「\*」を一括でつけるプログラムです。.anmファイルへの書き出しもできます。

## .exeの動作環境
64bitのWindows10での動作を確認できました。ビルドに用いたツールの仕様上32bit Windowsでは動作しません。   
非Windows環境では.pyファイルをダウンロードしPythonで実行することができますが、クリックなどの操作のプログラム内での挙動がWindowsと異なるため正常に動作しません。

## アップデート履歴
- [2020.08.06](https://drive.google.com/file/d/1jxZIbeXXMJca6zSsArGFlmtMsuSjPM71/view?usp=sharing)
  - 初版をアップロードしました
- [2020.08.07](https://drive.google.com/file/d/1TT511MpYgO7yTWXClm4BHvN2bvpA3hUr/view?usp=sharing)
  - 「戻す」「やり直す」機能を実装しました
  - 正規表現パッケージを使わないようにしました
  - GUIにボタンを追加したり、ウィジェットの大きさを変えるなどの変更を加えました
- [2020.08.08](https://drive.google.com/file/d/1QOtrYraZOFFy9SuCn0YoWNfRjK2iNef1/view?usp=sharing)
  - 固定条件の変換メニューを廃止しました
  - 削除対象も条件を指定できるようにしました
  - 以上に伴いGUIに変更を加えました
  - 変換時スクロール位置がリセットされないようにしました(昼上げなおしver.)
- [2020.08.15](https://drive.google.com/file/d/1VJp48N6k1W63HtVY4Dgde4jVFb_y72NG/view?usp=sharing)
  - 一部のボタンを上段メニューバーに変更しました
  - ファイルを開くときと保存するとき文字コードを指定できるようにしました
  - 変換対象レイヤーをチェックボックスで選択できるようにしました
  - 変換項目を「!」をつける、「\*」をつける、それらを消すの3つに変更しました
  - .anmファイルの書き出し機能を追加しました
  - 以上に伴いGUIに変更を加えました
  - psdファイルを扱うためのクラスが大幅に変更されました
- [2020.08.25](https://drive.google.com/file/d/1uP40FkmhM3ZPyu3QOFARdCOSLCOpVcLd/view?usp=sharing)
  - .anmファイルの書き出しを行う際、自動で上書き保存されるように変更しました
- [2020.09.06](https://drive.google.com/file/d/1ig9vFRNgkwyo1KVHxzOwVLjOg668jw-Y/view?usp=sharing)
  - ヘルプの文章の誤字を修正しました
  - .exe形式だとアンチウイルスソフトによってダウンロードできない場合があるとのことなので.zip形式でアップロードしました
- 2020.09.11
  - ~~目パチ口パクのスクリプト生成をちょっとだけ楽にする機能のベータ版を配布します~~元のプログラムと統合したため別配布はもうしません
- [2020.09.15](https://drive.google.com/file/d/1N4xCn3g-Hns69BhBDgUo-9fOdT6T_UpS/view?usp=sharing)
  - 目パチと口パクスクリプト作成補助機能を追加しました
- [2020.09.21](https://drive.google.com/file/d/1_F1Vqqie_UBKHRNkFBNMCXZobgjFKSkP/view?usp=sharing)
  - .png抽出機能（仮）を追加しました
- [2020.09.29](https://drive.google.com/file/d/1lXuv_mEhp3UUJhaKZIHje-j0l1GCjdkI/view?usp=sharing)
  - 一部特殊文字を含むレイヤーを.anmに出力するときエラーが発生する問題を修正していただきました(イスターリャ様)
- [2020.10.02](https://drive.google.com/file/d/1Fyso2LRvkjxQCPhRJmeDkpK4pz5dhxE6/view?usp=sharing)
  - .anmファイル出力時に目パチ口パク生成タブで生成したスクリプトを組み込めるように改善していただきました(イスターリャ様)
  - ファイルを開いたとき口パク目パチ生成タブの内容及び.anmファイル書き出し対象レイヤーリストをクリアするように修正しました
- [2020.10.03](https://github.com/662611034/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu/releases/download/201002/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu_201002.zip)
  - プログラムの更新はありませんが、ダウンロードリンクをgithubに一元化しました
  - 今後の更新履歴はgithubのreleaseの方にアップロードされます
 
  
# 使い方
ダウンロードしたzipファイルを解凍し、中の.exeファイルを実行します。  
上段の「ファイル」メニューから編集したい.psdファイルを開くと以下のような画面になります。   
ちなみに起動には少々時間がかかります。

![hoge](https://user-images.githubusercontent.com/48207892/95672858-fa01cf80-0bde-11eb-942e-6eb4456a7be2.png)

名前を変更したいレイヤーのチェックボックスにチェックを入れ、「!」をつける、「\*」をつける、「!」と「\*」を消すボタンを押すとその通りに名前が変換されます。   
目パチ、口パクのスクリプトを生成する場合、「作業中のファイル」すぐ下のタブを切り替えてスクリプト生成メニューに切り替えることができます。  
以下ではプログラムの各動作におけるより詳細な説明が続きます。


## ファイルを開く・保存する
- 画面上段左側のプルダウンメニューでファイルを開くとき使う文字コードを選ぶことができます。
- ファイルを上書き保存するときは開いたときの(もし別名保存していればその時用いた)文字コードで保存されます
- 別名で保存する場合は選択されている文字コードで保存されます

## レイヤー名の変換
- チェックを入れたレイヤーの名前が変換されます
- レイヤー名にすでに「!」か「\*」の**どちらかが**ついている場合、追加で「!」や「\*」をつけることはありません
- ただし全角記号は「!」や「\*」としてみなしません
- 「!」と「\*」を外す場合、「!」や「\*」が複数つけられていたらそれらを全て消します
- 変換メニュー選択条件のタブを切り替えることによって旧版で使っていた条件指定の変換を行うことができます
- 変換をボタンで実行する場合でもショートカットキーで実行する場合でも対象レイヤーは今選ばれているタブに従います
- 「前/後ろにつける」ボタンで任意文字列を挿入することができます
-  任意文字列を一括で削除する機能はないため、慎重に行ってください(戻す/やり直すは可能です)
-  F12キーによって自由編集モードを開始/終了できます
-  自由編集モードでは保存、変換、戻す、.anm書き出しなどの機能が制限されます

### 条件を指定して変換
- レイヤーの層、名前と一致条件、レイヤーの種類を指定して変換を行います
- レイヤーの層は右側のレイヤー表示領域で確認することができます
- 「0層」は特定の層ではなく全ての層を指定する特殊例です
- レイヤー名の一致条件の「含む」や「一致する」は融通が利かず、一言一句違わず同じ文字列だけを検索します
  - 文字と小文字、ひらがなとカタカナ、全角と半角は別の文字として認識します
  - 空白文字も一致していなければなりません
    - 例）「ああ　ついでに」は「あつい」を含んでいるとはみなしません
- 変換対象のプルダウンメニューの「物」はレイヤーとグループ両方に対して変換を行うことを意味します

## .anmファイルの書き出し
- レイヤー表示領域に表示されている「追加」ボタンをクリックすることで.anmファイルに書き出すグループを選択することができます
- .anmファイルはshift-jisで作成されます
- 書き出し対象レイヤーの「1つ外す」は最後に追加されたレイヤーから順に適用されます
- 既に選択されているレイヤーの順番を変えることはできないため、一旦対象から外した後追加しなおさなければなりません
- 規定の名前であれ別名であれ、書き出しを実行すればその時点で.psdファイルが上書きされます
- 「既定の名前で書き出す」と元の.psdファイルと同じフォルダに「同じ名前+末尾文字列.anm」のファイルに出力されます
- 「既定の名前で書き出す」は同名ファイルが既に存在していても確認を行うことなく上書きします
- 「目パチ口パクを含めて書き出す」にチェックを入れると、目パチや口パクのタブで行生成済みのスクリプトを挿入、トラックの値も処理された状態で出力できます (by istallia)
  - トラック番号入力ダイアログを右上のxボタンで閉じると.anmファイルの出力が中断されます
-  書き出し対象レイヤー左の「深」にチェックを入れると、グループ直下の物ではなく、グループに含まれるすべての「グループでないレイヤー」が書き出し対象になります

## .pngファイルの抽出（仮）
- .anmファイル書き出し対象のグループに含まれるレイヤーをそれぞれ.pngファイルに書き出すことができます
- 直下のレイヤーだけでなく、対象グループの下層にあるレイヤーのうち、グループでないものを全て抽出します
- .pngファイルの保存先は.psdファイルのある位置の「png_exported」フォルダで、中にグループ名と同名のフォルダを生成して保存します
- Windowsでファイル名に使えない文字は全角文字に置換されます
- 同名ファイルが発生してしまった場合上書きされます
  - 例）「目」の下の「赤目」グループの「開き」と「青目」グループの「開き」は両方「開き.png」というファイル名になるため片方のみ保存されます

## レイヤー表示領域

### レイヤー表示の折り畳み
- チェックボックスの左側の、枝別れを表示している空間をクリックすることでグループの表示を折りたたんだり展開することができます
  - 下の「全て展開」「全て畳む」で一括で操作することもできます  

### チェックボックス
- グループのレイヤーのチェックボックスはShift+クリック、あるいはctrl+shift+クリックで下位のレイヤーを一括で選択することができます
  - shift+クリックでは直下のレイヤーが一括で選択されます
  - ctrl+shift+クリックでは下位のレイヤー全てが選択されます
- 下位レイヤーの一括選択はクリックしたレイヤーの選択状況と逆の状態として選択されます
  - 例）チェックが入っているグループをshift+クリックしてチェックを外すと、直下のレイヤーはチェックが入った状態に変更されます
  - このとき、既にチェックが入っていた直下のレイヤーは状態が反転することなくチェックが入ったままになります
- 最上段のチェックボックス(「層」と「レイヤー構造」の間)は1層のレイヤーを一括で選択するためだけのものであり、変換動作とは関係ありません
  - ここにチェックが入っていても全てのレイヤー名が変換されるようなことはありません
  
### レイヤーパスのコピー
  - レイヤー名をダブルクリックすると目パチや口パク生成に必要なレイヤーのパスがクリップボードにコピーされます

## 「戻す」と「やり直し」
- それぞれ128回までの記録ができます

## 目パチ口パクの生成
- 基本的に公式チュートリアルのスクリプト生成ページと同じ使い方になります
- あくまでもスクリプトを生成するだけであり、そのスクリプトを.anmファイルに貼り付けトラックの数字を変える作業は自分でしなければなりません
- 生成されるスクリプトは公式で生成した文字列の、文頭に半角スペースが2つ、文末に「,」が付いたものになります
- それぞれの入力欄にレイヤーのパスを入力し、「行作成」を押すと下の出力欄にスクリプトが生成されます
  - レイヤーのパスはUI右側のレイヤー構造表示領域のレイヤー名をダブルクリックすることでクリップボードにコピーできます
- 行は生成するたびに出力欄に累積します
- 出力欄下の「1行削除」や「クリア」ボタンで間違えた行を消すことができます
- 出力欄下の「コピー」ボタンを押すか出力欄をダブルクリックすることで生成されたスクリプトをクリップボードにコピーします
- 「目パチ」「口パク」「あいうえお口パク」でそれぞれの入力欄と出力欄は独立しており、タブを切り替えても現在の状態は維持されます

## ショートカットキー
- ctrl+o：ファイルを開く
- ctrl+s / ctrl+shift+s：上書き保存 / 別名で保存
- F5 / F6 / F7：「!」をつける / 「\*」をつける / 「!」と「\*」を消す
- ctrl+z / ctrl+yあるいはctrl+shift+z：戻す / やりなおす
- ctrl+1 / ctrl+2：「変換対象選択条件」の切り替え(チェックしたレイヤー / 条件指定)
- ctrl+e / ctrl+shift+e：.anmファイルを既定の名前で書き出す / 名前を指定して書き出す
- ctrl+a / ctrl+shift+a：全てのレイヤーにチェックを入れる / 外す
- ctrl+d：(目パチ口パク生成タブにおいて)現在選択している入力欄をクリアする
- ctrl+q：プログラムのを終了する

## 既知の問題
- 容量がかなり大きいです
- ウィンドウの大きさを変えてもレイヤー表示領域の大きさは変わりません
- レイヤー名に特定の文字が入っている場合.anmファイルが正常に動かない場合があります
  - 例えばレイヤー名に入っている半角スペースは「%20」にしなければpsdtoolkitでは正しく認識されません
  - 半角スペースは対応済みですが、他の文字で同様のトラブルがあった場合psdtoolkitで「レイヤーをクリップボードにコピー」したとき得られる文字列を参考に.anmファイルを修正する必要があります
  - (2020.09.29) これは「全角チルダ問題」と言うようです。[参考ページ](https://qiita.com/motoki1990/items/fd7473f4d1e28c6a3ed6)に記載されていた文字に関しては置き換え処理を追加しました (by istallia)

# フィードバックについて
ツイッター( https://twitter.com/662611034 )の方でも受け付けます。

# プログラムの中身について

## 構成
以下の3つのファイルで構成されています。
- psd_subtool.py：pipでインストールしたpsd_toolsを用いて、psdを読み込んだりレイヤー名を変えたりするクラスを定義しています。
- gui.py：GUIの見た目の部分と、選択した項目の情報を出力するクラスを定義しています。Python標準ライブラリのtkinterを用いました。
- \_\_main\_\_.py：上記のhandler.pyとgui.pyをまとめて新しいメソッドを定義したりボタンに関数をバインドしたりしています。ウェブページを開くためにPython標準ライブラリのwebbrowserを用いています。
Windows以外の環境の方はこれらのファイルと必要なパッケージをダウンロードしてご利用いただくこともできます。Windows以外の環境でこのプログラムが必要な場合があるかは甚だ疑問ですが。

## ビルド
pyinstallerを用いて64bit Windows 10でビルドしました。
