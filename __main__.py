'''
.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラムのトップアプリケーション定義
'''

import traceback
import webbrowser
import os
import copy
import gui
import psd_subtool
import tkinter.filedialog as fd
import tkinter.messagebox as mb

# githubページのURL
URL = 'https://github.com/662611034/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu'

def prohibit_to_doublebyte(string):
    '''
    入力文字列の中に含まれるWindowsでの禁止文字を全角に置換

    Parameters
    ----------
    string: str
        入力文字列

    Returns
    -------
    string_mod: str
        置換された文字列
    '''
    prohibitted = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    alternative = ['￥', '／', '：', '＊', '？', '”', '＜', '＞', '｜']
    string_mod = string
    for p, a in zip(prohibitted, alternative):
        string_mod = string_mod.replace(p, a)
    return string_mod


class Logger():
    '''
    「戻す」と「やり直す」のログを保存・復元するためのクラス

    Attributes
    ----------
    log_length: int
        最大保持ログ数
    logs: list
        「戻す」用のログと「やり直す」ログのリスト
        [0]が「戻す」用で[1]が「やり直す」用
        それぞれのログもリストである
    '''
    def __init__(self, length=128):
        '''
        最大保持ログ数を指定しインスタンスを初期化

        Parameters
        ----------
        length: int
            最大ログ保持数
        '''
        self.log_length = length
        self.logs = [[], []]  # 0: back, 1: fore

    def stack_at(self, instance, which=0):
        '''
        ログの最後尾に要素を追加する
        ログの個数がlog_lengthを超える場合先頭の物を削除する

        Parameters
        ----------
        instance: Object
            何らかの要素
        which: int
            過去ログかやり直しログかを選択。0が過去
        '''
        if len(self.logs[which]) > self.log_length-1:
            self.logs[which].pop(0)
        self.logs[which].append(copy.deepcopy(instance))
        return self

    def pop_from(self, which):
        '''
        ログの最後尾の要素を取り出す

        Parameters
        ----------
        which: int
            過去ログかやり直しログかを選択。0が過去

        Returns
        -------
        : Object
            whichで選択したログの最後尾のオブジェクト
            ログの長さが0の場合Noneを返す
        '''
        return self.logs[which].pop() if self.logs[which] else None

    def reset(self, which):
        '''
        whichで選択したログを空のリストに初期化する

        Parameters
        ----------
        which: int
            過去ログかやり直しログかを選択。0が過去
        '''
        self.logs[which] = []
        return self

    def is_empty(self, which):
        '''
        whichで選択したログが空かどうか判定する

        Parameters
        ----------
        which: int
            過去ログかやり直しログかを選択。0が過去
        '''
        return False if self.logs[which] else True


class PachiPakuEmbedding():
    '''
    プログラム内で生成された目パチ口パクをanmスクリプトに組み込むクラス

    Attributes
    ----------
    trackline, valueline: str
        PSDImageExtで生成されるtrackline, valueline
    pachipaku: str
        目パチ口パク補助タブの出力欄から取得した文字列
    '''

    @classmethod
    def embed(cls, trackline, valueline, pachipaku):
        '''
        わざわざインスタンス作って数行書くほどでもないため、
        処理をまとめたクラスメソッドを作って1行で書けるようにする

        Parameters
        ----------
        ClassのAttributesのままなので割愛
        '''
        instance = cls(trackline, valueline, pachipaku)
        instance.increase_tracknum().insert_valueline()
        return instance.trackline, instance.valueline

    def __init__(self, trackline, valueline, pachipaku):
        '''
        コンストラクタでは引数を受け取るだけ

        Parameters
        ----------
        ClassのAttributesのままなので割愛
        '''
        self.trackline = trackline
        self.valueline = valueline
        self.pachipaku = pachipaku

    def increase_tracknum(self):
        '''
        tracklineの数字を増やす
        (pachipakuを改行でsplitしたリストの要素数 - 1) が数字の増加量になる
        -1が必要なのはpachipakuの最後に空行が入っているため

        増やす数字の位置はfindで探してもいいけどsplitのほうがわかりやすいと思ったのでsplit採用
        また、左側からの順番で調べるとレイヤー名の「,」が入ってるときバグるため、右側から順番で特定する
        '''

        num = len(self.pachipaku.split('\n')) - 1  # 数字増加分
        splitedtrack = self.trackline.split(',')
        splitedtrack[-3] = str(int(splitedtrack[-3]) + num)  # 「,」でsplitして右から3番目要素を置換

        # つなげて終わり
        trackline_new = splitedtrack[0]
        for word in splitedtrack[1:]:
            trackline_new += ',' + word
        self.trackline = trackline_new
        return self

    def insert_valueline(self):
        '''
        pachipakuをvaluelineに挿入する
        改行でsplitして途中で差し込んで終わり
        '''
        splitedvalue = self.valueline.split('\n')
        valueline_new = splitedvalue[0] + '\n'
        valueline_new += self.pachipaku
        for line in splitedvalue[1:]:
            valueline_new += line + '\n'
        self.valueline = valueline_new[:-1] # 最後に空行が余計に1つつくことになるので削除
        return self


class AppTop(gui.RootWindow):
    '''
    .psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラムのトップアプリケーション

    Attributes
    ----------
    pas: PSDImageExt
        psdファイルインスタンス
    flag_saved: bool
        変換動作をして保存したかどうか
    flag_freeedit: bool
        今自由編集モードか否か
    logger: Logger
        「戻す」と「やり直す」用のログ管理インスタンス
    dict_names: dict
        各レイヤーの名前を保存している辞書型オブジェクト
        ログで保存する対象になる
        辞書のkeyは各レイヤーのメモリアドレスで、valueはレイヤーの名前
    '''

    def __init__(self,*args):
        '''
        トップウィンドウの生成とインスタンス変数の初期化、そしてコールバック関数のバインドを行う
        '''
        super().__init__(*args)

        self.psd = None
        self.flag_saved = True
        self.flag_freeedit = False
        self.logger = Logger()
        self.dict_names = {}

        self.bind_funcs()

    def bind_funcs(self):
        '''
        ホットキーやボタンなどにコールバック関数を紐づける
        '''
        f_open = self.make_callback(self.open_file)
        f_save = [self.make_callback(self.save_file, i) for i in range(2)]
        f_expo = [self.make_callback(self.export_script, i) for i in range(2)]

        f_conv = [self.make_callback(self.convert, i) for i in range(5)]
        f_unre = [self.make_callback(self.undoredo, i) for i in range(2)]

        f_clea = [self.make_callback(self.deal_anmlayer, i+1) for i in range(2)]  # clear 1 or all

        f_sela = [self.make_callback(self.select_all, i) for i in range(2)]  # select all

        f_fold = [self.make_callback(self.fold_all, i) for i in range(2)]

        f_fedt = self.make_callback(self.toggle_freeedit)

        self.menu_file.entryconfig(0, command=f_open)
        self.menu_file.entryconfig(1, command=f_save[0])
        self.menu_file.entryconfig(2, command=f_save[1])
        self.menu_file.entryconfig(4, command=f_expo[0])
        self.menu_file.entryconfig(5, command=f_expo[1])
        self.menu_file.entryconfig(7, command=self.quit)

        self.menu_edit.entryconfig(0, command=f_conv[0])
        self.menu_edit.entryconfig(1, command=f_conv[1])
        self.menu_edit.entryconfig(2, command=f_conv[2])
        self.menu_edit.entryconfig(4, command=f_unre[0])
        self.menu_edit.entryconfig(5, command=f_unre[1])
        self.menu_edit.entryconfig(7, command=f_fedt)

        self.menu_help.entryconfig(0, command=gui.HelpWindow)
        self.menu_help.entryconfig(1, command=lambda : webbrowser.open(URL))

        for i in range(5):
            self.button_converts[i].config(command=f_conv[i])
        for i in range(2):
            self.button_clears[i].config(command=f_clea[i])
        for i in range(2):
            self.button_exports[i].config(command=f_expo[i])
        for i in range(2):
            self.button_foldall[i].config(command=f_fold[i])
        self.button_exports[2].config(command=self.make_callback(self.export_pngs))

        self.bind_all('<Control-o>', f_open)
        self.bind_all('<Control-s>', f_save[0])
        self.bind_all('<Control-S>', f_save[1])
        self.bind_all('<Control-e>', f_expo[0])
        self.bind_all('<Control-E>', f_expo[1])
        self.bind_all('<Key-F5>', f_conv[0])
        self.bind_all('<Key-F6>', f_conv[1])
        self.bind_all('<Key-F7>', f_conv[2])
        self.bind_all('<Key-F12>', f_fedt)
        self.bind_all('<Control-z>', f_unre[0])
        self.bind_all('<Control-Z>', f_unre[1])
        self.bind_all('<Control-y>', f_unre[1])
        self.bind_all('<Control-a>', f_sela[1])
        self.bind_all('<Control-A>', f_sela[0])
        self.bind_all('<Key-F1>', lambda event: gui.HelpWindow())
        self.bind_all('<Control-q>', lambda event: self.quit())

        for i in range(1, 3):
            self.bind_all(f'<Control-Key-{i}>', self.make_callback(self.mode_select))

        return self

# from here, callback funcs
    def make_callback(self, func, *mode):
        '''
        コールバック関数を生成する
        以降で定義している「ファイル保存」などのメソッドはコールバック関数として使うとき
        エラーが出たらメッセージボックスで表示する機能をつけたい
        全てのメソッドにtry:~except文を入れるよりは
        このメソッドを使って生成するほうが効率的と判断した
        また、functool.partialを使うことなくモードも同時に指定できるメリットがある

        Parameters
        ----------
        func: function
            コールバック関数にしたいメソッド
        mode: int
            一部、モード引数によって動作を変える関数があるため指定

        Returns
        -------
        f_callback: function
            デコレートされたメソッド

        Notes
        -----
        デコレーターとして定義しなかったのは、modeの指定が必要だから
        event引数は必要としないメソッドがほとんどだが、一部押されたキーを
        判定して動作するメソッドがあるため、コールバック関数に使われる
        全てのメソッドはeventを引数として受け取るように定義した
        '''

        def f_callback(event=None):
            try:
                func(event, *mode)
                return 'break'
            except Exception as e:
                # mb.showerror('エラーが発生しました', str(e))
                mb.showerror('エラーが発生しました', str(traceback.format_exc()))

        return f_callback

    def open_file(self, event):
        '''
        ファイルを開くコールバック
        ファイルを開く動作の主体はsubfuncである
        プログラムテストのときいちいちファイルダイアログが開かれると面倒なため
        ファイル名指定部分は分離させた

        Parameters
        ----------
        event: tk.Event
            このメソッドでは使われない
        '''
        ifile_path = fd.askopenfilename(filetypes=[('psd files', '*.psd')])
        if not ifile_path:
            return 'break'
        if ifile_path[-4:] != '.psd':
            raise Exception('.psdファイルではありません')  # .psdファイルでない場合エラー
        
        self.open_subfunc(ifile_path)
        self.show_filename(self.ifile_path)
        self.show_msg('ファイルを開きました')

        return self

    def save_file(self, event, mode):
        '''
        ファイルを保存する
        保存した後メッセージを表示する
        上書き保存の場合ofile_pathとencodingを今のself.psdから参照する
        別名の場合GUIから受け取る

        Parameters
        ----------
        event: tk.Event
            使われない
        mode: int
            上書き保存なら0, 別名で保存なら1
        '''

        # ファイルが開かれた状態でなければ何もしない
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        if self.flag_freeedit:
            self.show_msg('自由編集中は保存できません')
            return 'break'

        if mode == 0:
            ofile_path = self.ifile_path
            msg = '上書き保存されました'
            encoding = self.psd.encoding
        elif mode == 1:
            ofile_path = fd.asksaveasfilename(filetypes=[('psd files', '*.psd')])
            if not ofile_path:
                return 'break'
            if ofile_path[-4:] != '.psd':
                ofile_path += '.psd'
            msg = '別名で保存されました'
            encoding = self.get_encode()

        self.save_subfunc(ofile_path, encoding)  # subfuncはこれが定義されている部分で説明
        self.show_filename(self.ifile_path)
        self.show_msg(msg)
        return self

    def export_script(self, event, mode):
        '''
        .anmファイルを書き出す

        Parameters
        ----------
        event: tk.Event
            使われない
        mode: int
            0: 既定の名前、1: 名前を指定
        '''
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        if self.flag_freeedit:
            self.show_msg('自由編集中は書き出しできません')
            return 'break'

        if not self.flag_saved:
            self.save_file(None, 0)

        anmlayers = self.get_anmlayers()
        if not anmlayers:
            self.show_msg('書き出し対象グループがありません')
            return self

        if mode == 0:
            efile_path = self.ifile_path[:-4] + self.get_anmtail() + '.anm'
        elif mode == 1:
            efile_path = fd.asksaveasfilename(filetypes=[('anm files', '*.anm')])
            if not efile_path:
                return 'break'
            if efile_path[-4:] != '.anm':
                efile_path += '.anm'

        track_destination = [-1, -1, -1]
        if self.bool_pachipaku.get():
            dialog = gui.TrackNumberDialog(master=self, groups=anmlayers)
            dialog.wait_window()
            track_destination = dialog.getTracksNumber()
            if not dialog.is_ok:
                self.show_msg('.anmファイルの書き出しを中断しました')
                return self

        self.export_subfunc(efile_path, anmlayers, track_destination)
        self.show_msg('.anmファイルを出力しました')

        return self


    def export_pngs(self, event):
        '''
        .pngファイルを書き出す

        Parameters
        ----------
        event: tk.Event
            使われない
        '''
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        if self.flag_freeedit:
            self.show_msg('自由編集中は書き出しできません')
            return 'break'

        if not self.flag_saved:
            self.save_file(None, 0)

        layergroups = self.get_anmlayers()
        if not layergroups:
            return self

        index_savedir = self.ifile_path.rfind('/')
        dir_save_root = self.ifile_path[:index_savedir+1] + f'png_exported'

        for group in layergroups:
            dir_save = f'{dir_save_root}/{prohibit_to_doublebyte(group.name)}'
            os.makedirs(dir_save, exist_ok=True)
            for layer, _ in self.psd.sublayers_recursive(group):
                if not layer.is_group():
                    image = layer.topil()
                    image.save(f'{dir_save}/{prohibit_to_doublebyte(layer.name)}.png')

        self.show_msg('.pngファイルを出力しました')

        return self

    def undoredo(self, event, mode):
        '''
        「戻す」と「やり直し」
        cache_nameで現在表示されているレイヤー名をdict_namesに保存する
        modeによってloggerのどちらかの配列に加える
        ログの状態によって「戻す」と「やり直す」のメニューの状態を更新する
        例）何らかの変更をしたら「やり直す」を非活性化にするなど
        「戻す」と「やり直す」も変換の1種であるためflag_savedをFalseにする
        ただし、1回戻して1回やり直して元の状態になったような場合でもflag_savedはfalseになる。
        (そういう状況までいちいち確認させるのは面倒だしあまり意味もないと思うため)

        Parameters
        ----------
        event: tk.Event
            使われない
        mode: int
            0: 戻す、1: やり直し
        '''
        # 0: undo, 1: redo
        if self.logger.is_empty(mode):
            return 'break'
        if self.flag_freeedit:
            self.show_msg('自由編集中その操作はできません')
            return 'break'

        self.cache_names()
        self.logger.stack_at(self.dict_names, 1-mode)

        self.dict_names = self.logger.pop_from(mode)
        self.refresh_names()
        
        self.unre_state(1-mode, 1)  # enable redo button

        if self.logger.is_empty(mode):
            self.unre_state(mode, 0)

        self.flag_saved = False
        return self

    def convert(self, event, mode):
        '''
        レイヤー名の変換を行う
        このメソッドではpsdファイルのインスタンスには触らず、
        レイヤー構造表示領域に表示されている文字列だけを編集する
        編集前後で「戻す」と「やり直す」のログも適切に編集する

        Parameters
        ----------
        event: tk.Event
            使われない
        mode: int
            0: 「!」をつける、1: 「*」をつける、2: 記号を消す
        '''
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'
        if self.flag_freeedit:
            self.show_msg('自由編集中は変換できません')
            return 'break'

        self.cache_names()
        self.logger.stack_at(self.dict_names, 0)
        self.logger.reset(1)

        for layer in self.psd.all_layers():
            if self.make_condition(layer, self.selected_tab()):
                self.convert_subfunc(layer, mode)

        self.unre_state(0, 1).unre_state(1, 0)

        self.flag_saved = False
        return self

    def mode_select(self, event):
        '''
        変換条件タブ(チェック入りレイヤーか、条件指定か)を切り替える

        Parameters
        ----------
        event: tk.Event
            Ctrl+1, 2で切り替えるため、eventのkeysymの数字に応じてタブを選択させる
        '''
        index = int(event.keysym) - 1
        self.select_tab(index)
        return self

    def deal_anmlayer(self, event, mode, layer=None):
        '''
        .anm書き出し対象レイヤーを追加したり外したりする

        Parameters
        ----------
        event: tk.Event
            使われない
        mode: int
            0: 追加、1: 1個外す、2: 全部外す
        layer: psd_tools.api.layers.group
            mode=0のとき、追加するレイヤー
        '''
        # 0: stack, 1: pop, 2: clear
        if mode == 0:
            self.stack_anmlayers(layer)
        elif mode == 1:
            self.pop_anmlayers()
        elif mode == 2:
            self.clear_anmlayers()
        return self

    def select_all(self, event, mode):
        '''
        レイヤー構造表示領域の全てのチェックボックスにチェックを入れたり外したりする
        
        Parameters
        ----------
        event: tk.Event
            使われない
        mode: int
            0: 外す、1: つける
        '''
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        for layer in self.psd.all_layers():
            self.frame_show.dict_widgets[id(layer)]['selected'].set(bool(mode))
        return self

    def fold_all(self, event, mode):
        '''
        全て畳む/展開するメソッドを生成
        tk.Buttonのcommandに割り当てるためにメソッドを変換するようにしてる
        '''
        for layer in self.psd.all_layers():
            if layer.is_group():
                target = self.frame_show.dict_widgets[id(layer)]['subframe']
                target.pack_forget() if mode else target.pack()
        return 'break'

    def toggle_freeedit(self, event):
        '''
        自由編集モードの切り替え
        レイヤー名のentryを全てstate=normalにするだけ
        自由編集モードに入るとき現在の状態をバックログに保存する
        '''
        if not self.psd:
            return 'break'

        if self.flag_freeedit:
            for layer in self.psd.all_layers():
                entry_target = self.frame_show.dict_widgets[id(layer)]['entry']
                entry_target.config(state='readonly')
            self.unre_state(0, 1).unre_state(1, 0)

        else:
            self.cache_names()
            self.logger.stack_at(self.dict_names, 0)
            self.logger.reset(1)
            for layer in self.psd.all_layers():
                entry_target = self.frame_show.dict_widgets[id(layer)]['entry']
                entry_target.config(state='normal')
            self.unre_state(0, 0).unre_state(1, 0)

        self.flag_saved = False
        self.flag_freeedit = not self.flag_freeedit

        return 'break'
# to here, callback funcs

# from here, funcs need for open
# コールバック関数の内部で使われる関数
# 実は各subfuncと上位メソッドの線引きは明確ではない。直したほうがいいかなと思ってる

    def open_subfunc(self, ifile_path):
        '''
        ファイルを開く動作の内部処理
        プログラムテスト時にいちいちファイル開くのがめんどくさくて、
        ファイルダイアログは表示させず開く動作だけ分離させるために実装

        ファイルのパスを受け取って
        ・psdファイルインスタンス生成
        ・レイヤー構造表示領域の再生成
        ・階層選択のプルダウンメニューの中身の更新
        ・dict_namesの初期化
        ・最初は非活性化されてた「変換」などのメニューを活性化
        ・「戻す」「やり直す」ログを初期化
        ・目パチ口パク補助タブ入力欄を消去
        などする

        Parameters
        ----------
        ifile_path: str
            開くファイルのパス
        '''
        self.ifile_path = ifile_path
        self.psd = psd_subtool.PSDImageExt.open(self.ifile_path, self.get_encode())

        self.remake_frame_show()

        self.set_combo_level(list(range(self.psd.level_max+1)))

        self.dict_names = {}
        for layer in self.psd.all_layers():
            self.dict_names[id(layer)] = layer.name

        self.logger.reset(0).reset(1)

        for i in [1, 2, 4, 5]:
            self.menu_file.entryconfig(i, state='normal')
        for i in [0, 1, 2, 4, 5, 7]:
            self.menu_edit.entryconfig(i, state='normal')

        self.unre_state(0, 0).unre_state(1, 0)

        self.flag_saved = True  # 開いた直後は保存されたファイルと現在の表示状態が同じであるためTrue
        self.deal_anmlayer(None, 2)
        self.book_script.reset_form()
        return self

    def remake_frame_show(self):
        '''
        レイヤー構造表示領域を作り直す
        まずはframe_show.remake_canvasを使ってウィジェットを生成する
        そのあと各チェックボックスににはshift+click、ctrl+shift+clickでの挙動を割り当て
        「追加」ボタンや折りたたみ機能もバインドさせる

        .anm書き出し対象に追加はmake_callbackで作るが、
        折りたたみや一括チェック機能のメソッドを生成するメソッドは別途下で定義している
        '''
        self.frame_show.remake_canvas(self.psd)

        # psd.all_layers()メソッドからできるレイヤーリストにpsdファイル自身は入らない
        # だから領域の一番上のチェックボックスは別途bindを実行する必要がある
        self.frame_show.dict_widgets[id(self.psd)]['check'].bind('<Button-1>', self.make_fcheck(self.psd))

        for layer in self.psd.all_layers():
            if layer.is_group():
                dict_tmp = self.frame_show.dict_widgets[id(layer)]
                dict_tmp['button'].config(command=self.make_callback(self.deal_anmlayer, 0, layer))
                dict_tmp['check'].bind('<Button-1>', self.make_fcheck(layer))

        return self

    # make functions to bind at widgets on frame_show
    def make_fcheck(self, layer):
        '''
        shift+clickやctrl+shift+clickで一括チェックを入れるコールバック関数を生成
        dict_rangeはチェックを入れる対象レイヤーリストを要素として持つ辞書である
        event.stateをkeyにしてそれぞれのリストを呼び出すことができる
        各リストは
        click: 下位レイヤーは触らないため空
        shift+click: 直下レイヤーのメモリアドレスのリスト
        ctrl+shift+click: 下位の全てのレイヤーのメモリアドレス
        となる。dict_widgetsのkeyがメモリアドレスであるためレイヤーのリストにする必要はない

        Parameters
        ----------
        layer: psd_tools.api.layers.group
            対象レイヤー(グループ)

        Returns
        -------
        fcheck: function
            下位レイヤーのチェックボックスを一括でチェック入れたり外したりする
            eventを受け取り、それに対応する対象レイヤーリストをdict_rangeから選ぶ
            そしてそれらのレイヤーのチェック状態を、クリックしたレイヤーのチェック状態を元に制御する
            例）上位レイヤーにチェックを入れたら下位は外す
        
        Notes
        -----
        click、shift+click、ctrl+shift+clickのそれぞれのevent.stateが整数の8、9、13である

        tkinterではチェックボックスをクリックすると、状態を取得した後チェックの有無が変わる
        そのため、下位レイヤーのチェック状態は上位レイヤーから取得したチェック状態と同じにする必要がある
        例）チェックされてない上位レイヤーをクリックすると
        ・チェックされてない(False)ことを取得
        ・上位レイヤーにチェックが入る
        ようになる。この時下位レイヤーはチェックを外すようにしたいため、Falseを反転せずそのまま適用する
        '''
        dict_range = {8: [], \
                9: [id(sublayer) for sublayer in layer], \
                13 : [id(sublayer) for sublayer, _ in self.psd.sublayers_recursive(layer)]}
        id_tmp = id(layer)

        def fcheck(event=None):
            try:
                bool_got = self.frame_show.dict_widgets[id_tmp]['selected'].get()
                for id_layer in dict_range[event.state]:
                    self.frame_show.dict_widgets[id_layer]['selected'].set(bool_got)

            except Exception as e:
                mb.showerror('エラーが発生しました', str(e))

        return fcheck

# to here, funcs need for open

    def save_subfunc(self, ofile_path, encoding):
        '''
        ファイル保存のための内部処理
        行う処理においてsave_fileとの明確な線引きはない。直さないと・・・

        レイヤー構造表示領域に表示されているレイヤー名を取得してpsdファイルオブジェクトのレイヤー名を更新する
        (このプログラムの「変換」は表示されてる文字列を変えるだけで実際ファイルを制御しているわけではない)
        更新した後保存する

        Parameters
        ----------
        ofile_path: str
            保存する先のファイルパス
        encoding: str
            保存するとき使う文字コード
        '''
        for layer in self.psd.all_layers():
            layer.name = self.frame_show.dict_widgets[id(layer)]['entry'].get()

        self.psd.save(ofile_path, encoding)

        self.flag_saved = True
        self.ifile_path = ofile_path
        self.psd.encoding = encoding

        return self

    def export_subfunc(self, efile_path, anmlayers=[], track_destination=[-1, -1, -1]):
        '''
        .anmファイル書き出しの内部処理
        例のごとくexport_scriptと明確な線引きはない

        frame__anmから書き出し対象レイヤーのリストを抽出し、
        PSDImageExtのexport_anmscriptでそれぞれのレイヤーのtracklineとvaluelineを生成する
        いったんそれら文字列は配列に保存しておいて、後でファイルに書き出す
        psdtoolkitの仕様上、文字コードはshift-jisを使う
        cp932でも大丈夫みたいだけど、違いはよく分からない

        Parameters
        ----------
        efile_path: str
            書き出す.anmファイルのパス
        '''
        
        # bool_deeplayerによってanmscriptのメソッドが変わる

        tracklines, valuelines = '', ''

        for tracknum, layer in enumerate(anmlayers):
            func_anmscript = \
                    self.psd.export_anmscript_deep if self.bool_deeplayer[tracknum].get() \
                    else self.psd.export_anmscript

            trackline, valueline = func_anmscript(layer, tracknum)
            for which, destination in enumerate(track_destination):
                # which: 0-目パチ、1-口パクシンプル、2-口パクあいうえお
                if destination == tracknum:
                    trackline, valueline = \
                            PachiPakuEmbedding.embed(trackline, valueline, self.get_script_text(which))
            tracklines += trackline
            valuelines += '\n' + valueline

        with open(efile_path, mode='w', encoding='sjis') as fout:  # or cp932
            fout.write(tracklines)
            fout.write(valuelines)

        return self


# from here, funcs need for conversion
    def convert_subfunc(self, layer, mode):
        '''
        レイヤー名変換の内部処理
        convertメソッドは複数レイヤーを条件によって変換し、その前後処理をする
        このメソッドは引数のレイヤー一つに対して名前変換を行うメソッドである

        まずはlayerのメモリアドレスから該当する表示欄を調べる(dict_widgetsより)
        readonly状態だと中身が変えられないのでいったん活性化させる
        modeによって中身の文字列を編集したら入力欄をreadonlyに戻す

        if文を減らすためにHEADSYMBOLSなどのタプルを利用したりした

        Parameters
        ----------
        layer: psd_tools.api.layers.Group / PixelLayer
            対象レイヤー
        mode: int
            変換モード。0: 「!」をつける、1: 「*」をつける、2: 記号を消す
            3: 任意文字列を前に挿入、4: 任意文字列を後ろに挿入

        Notes
        -----
        modeのif-else文、もう少しスマートにできないものだろうか
        '''
        entry_target = self.frame_show.dict_widgets[id(layer)]['entry']
        entry_target.config(state='normal')
        symbols = self.psd.HEADSYMBOLS  # ('!', '*')

        if mode in [0, 1] and not (entry_target.get()[0] in symbols):
            entry_target.insert(0, symbols[mode])
        elif mode == 2:
            while entry_target.get()[0:1] in symbols:
                entry_target.delete(0, 1)
        elif mode == 3:
            entry_target.insert(0, self.get_str_arbitrary())
        elif mode == 4:
            entry_target.insert('end', self.get_str_arbitrary())
        entry_target.config(state='readonly')
        return self

    def make_condition(self, layer, mode):
        '''
        レイヤー名変換対象レイヤーか否かを判断しその真理値を返す
        modeの値によってチェックボックスで判断するか条件指定か選ぶ

        mode=0の場合
        layerのメモリアドレスでdict_widgetsから該当するチェック状態の値を調べるだけ

        mode=1の場合
        c_level、c_words、c_match、c_classを取得する(詳細はgui.pyのCtrlFrame参照)
        それぞれの値を元に条件を判定する

        Parameters
        ----------
        layer: psd_tools.api.layers.Group / PixelLayer
            判断したいレイヤー
        level: int
            レイヤーの階層
        mode: int
            判断をチェックでするかか条件指定でするか
            0: チェックの入ったレイヤー、1: 条件指定

        Returns
        -------
        : bool
            引数のレイヤーが変換対象であるか否か。
            これがTrueだとレイヤー名が変換される
        '''

        if mode == 0:
            return self.frame_show.dict_widgets[id(layer)]['selected'].get()

        elif mode == 1:
            c_level, c_words, c_match, c_class = self.get_condition()
            condition = True

            # c_class=3は「直下の物」
            # つまりレイヤー自身ではなくその親レイヤーの階層や名前を確認する必要があるため、場合分けする
            id_layer = id(layer._parent if c_class == 3 else layer)

            entry_target = self.frame_show.dict_widgets[id_layer]['entry']

            # これも、c_classだと親レイヤーの階層を見なきゃならないためその補正をかけてる
            c_level_target = c_level + (1 if c_class == 3 else 0)

            if c_level > 0:  # c_levelが0なら階層条件がない
                condition = condition and (c_level_target == layer.level)

            # ここでは名称の条件を処理
            if c_match == 0:
                condition = condition and (c_words in entry_target.get())
            elif c_match == 1:
                condition = condition and (c_words == entry_target.get())

            # c_class=0なら条件を付けない、3でもレイヤーかグループかは重要ではない。1と2のときだけ判定
            if c_class == 1:
                condition = condition and (not layer.is_group())
            elif c_class == 2:
                condition = condition and (layer.is_group())

            return condition
# to here, funcs need for conversion

    def cache_names(self):
        '''
        レイヤー名の一覧をself.dict_namesに保存するメソッド
        '''
        for layer in self.psd.all_layers():
            self.dict_names[id(layer)] = self.frame_show.dict_widgets[id(layer)]['entry'].get()
        return self

    def refresh_names(self):
        '''
        loggerから取り出した辞書を参考にレイヤー構造表示領域の表示内容を更新する
        '''
        for layer in self.psd.all_layers():
            entry_target = self.frame_show.dict_widgets[id(layer)]['entry']
            entry_target.config(state='normal')
            entry_target.delete(0, 'end')
            entry_target.insert(0, self.dict_names[id(layer)])
            entry_target.config(state='readonly')
        return self


AppTop().mainloop()
