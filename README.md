# ダウンロード
最新版は[こちら](https://drive.google.com/file/d/1o9iAOm7YzKWD_353Jui339XMydosRV6g/view?usp=sharing)のリンクからダウンロードできます。容量が83MBあってgithubにアップロードできませんでした。   
過去バージョンはアップデート履歴からダウンロードできます。

# このプログラムについて
.psdファイルのレイヤーの名前の先頭に「!」や「\*」を一括でつけるプログラムです。

## .exeの動作環境
64bitのWindows10での動作を確認できました。ビルドに用いたツールの仕様上32bit Windowsでは動作しません。   

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
  
# 使い方
ダウンロードした.exeを実行すると以下のようなウィンドウが表示されます。ちなみに立ち上がるまで少々時間を要します。   
編集したい.psdファイルを開いて適用したい項目を選んで変換すると右側の空間に変換後のレイヤー構造が表示されます。   
必要な変換が終わったら上書き保存、あるいは別名で保存します。   

![Ee0p7qUU0AAE3uU](https://user-images.githubusercontent.com/48207892/89659491-f023cd80-d90a-11ea-82ce-8059d65f4f5c.png)

## 変換メニューについて
大体文章に書いてあるそのままの変換を行います。   
例えば1つ目のメニューは指定した条件に合うレイヤーやグループをフィルタリングして名前の先頭に「!」や「\*」を加えます。このとき、名前の先頭が「!」か「\*」のレイヤーやグループは変換されません。   
レイヤーの絞り込みには4つの条件を指定することができます。
- 層：レイヤーの階層を指していて、最上位階層を「1層」として定義しています。例えば、どのグループにも属さいないレイヤーは1層、どのグループにも属さないグループに属するレイヤーは2層です。そして0層は特定位の階層ではなく「全ての層」を指定します
- レイヤーやグループの名前に含まれる言葉
- 一致条件：「含む」か「一致する」を選ぶことができます。どちらも融通が利かないので、ローマ字の大文字と小文字、全角半角、ひらがなとカタカナも全て違う言葉として扱い、「一言一句違わず含まれる・一致する」名前だけをフィルタリングします。例えば、「ああついでに氷をいれてくれ」というレイヤーがあったとして「アツイ」を含んでいるとはみなしません。
- 検索対象の種類：検索対象がレイヤーかそれともグループかを指定します。ここで「物」を選んだ場合両方とも変換します。「グループの直下の物」の場合、指定する条件に合致するグループを探し、その直下にあるレイヤーとグループを全て変換します

## ショートカットキー
プログラムに記載している通りのショートカットキーが使えます。

## 「戻す」と「やり直し」の回数制限
この二つの機能はそれぞれ最大32回分までしか記録を保存しません。1回あたりMB単位でメモリーを消費すると考えられるためこの制限を設けました。   
ショートカットキーを押しっぱなしにしていると変換が連続で実行されるので気を付けてください。

## 既知の問題
- 容量がかなり大きいです
- ウィンドウの大きさを変えてもレイヤー表示領域の大きさは変わりません

# フィードバックについて
ツイッター( https://twitter.com/662611034 )の方でも受け付けます。

# プログラムの中身について

## 構成
以下の3つのファイルで構成されています。
- handler.py：psdを読み込んだりレイヤー名を変えたりするクラスを定義しています。Python標準ライブラリのreと、pipからインストールしたpsd_toolsを用いています。
- gui.py：GUIの見た目の部分と、選択した項目の情報を出力するクラスを定義しています。Python標準ライブラリのtkinterを用いました。
- \_\_main\_\_.py：上記のhandler.pyとgui.pyをまとめて新しいメソッドを定義したりボタンに関数をバインドしたりしています。ウェブページを開くためにPython標準ライブラリのwebbrowserを用いています。
Windows以外の環境の方はこれらのファイルと必要なパッケージをダウンロードしてご利用いただくこともできます。Windows以外の環境でこのプログラムが必要な場合があるかは甚だ疑問ですが。

## ビルド
pyinstallerを用いて64bit Windows 10でビルドしました。
