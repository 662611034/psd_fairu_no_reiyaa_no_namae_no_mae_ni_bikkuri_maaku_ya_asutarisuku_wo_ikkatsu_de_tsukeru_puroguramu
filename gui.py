'''
tkinterを用いてGUIの各パートを生成するクラスを定義している

各クラスのメソッドの中で「_tmp」付きで定義したものは
あとから参照することがないオブジェクト。
変数名を考える労力を減らすためにそういう名前になった
(改修するとき後悔するのかな)
'''

import tkinter as tk
import tkinter.ttk as ttk
import pyperclip

# 以下にはヘルプウィンドウに表示されるメッセージを定義する

FILEMSG='''
・ファイルを開くとき文字コードを指定することができます

・上書き保存の場合は文字コード選択メニューの状況によらず
　ファイルを開いた時の文字コードで保存されます

・別名で保存の場合は選択メニューで指定されている文字コードで保存されます
'''

CONVMSG = '''
・変換対象選択条件タブを切り替えて対象レイヤーの指定方式を変えることができます

・既に「!」や「*」がついているレイヤーには新しく記号をつけません

・「層」に0を指定した場合全ての層が対象になります

・「物」とはレイヤーとグループ両方を指します

・ボタンでの実行でもショートカットキーでの実行でも
　レイヤー指定条件は活性化しているタブに従います
'''

CHECKMSG='''
・shift+クリックで直下の層を全て選択します

・ctrl+shift+クリックで下位の層を全て選択します

・下位のレイヤーのチェックはクリックしたレイヤーの状態と逆になります
　例）親レイヤーをshift+クリックでチェックを外した場合、
　下位レイヤーはチェックがつけられます

・shift(+ctrl)+クリックは下位のレイヤーをチェック状況を反転するものではありません
　強制に親レイヤーと逆の状態にするものです

・最上段のチェックボックスは他のチェックボックスを操作するための物です
　選択していても変換対象にはなりません
'''

EXPORTMSG='''
・レイヤーの隣のボタンを押して出力対象グループを選択することができます

・今選択されているレイヤーは画面から左下で確認できます

・.anmファイルの書き出しボタンを押すと自動的に現在の状態で上書き保存されます
　ご注意ください

・ファイルが保存されていない場合、レイヤー構造表示領域でのレイヤー名と
　書き出し対象レイヤーリストでのレイヤー名が異なることがあります

・書き出しを実行するとレイヤー構造表示領域に表示されている名前で書き出されます

・既定の名前で書き出す場合、.psdファイルと同じフォルダの
　「(同じファイル名)(入力した末尾文字列).anm」に出力されます

・既定の名前で書き出す場合、同名ファイルが存在したら上書きします
　確認メッセージは表示されません
'''

HOTKEYS = '''
キーボードショートカット一覧

・ctrl+o：ファイルを開く

・ctrl+s / ctrl+shift+s：上書き保存 / 別名で保存

・F5 / F6 / F7：「!」をつける / 「*」をつける / 記号を消す

・ctrl+z / ctrl+(y/shift+z)：戻す / やり直す

・ctrl+(1/2)：変換するレイヤー条件を選択

・ctrl+e / ctrl+shift+e：既定の名前で / 名前を指定して.anmファイルを出力

・ctrl+a / ctrl+shift+a：全てのレイヤーにチェックを入れる / 外す

・ctrl+d：入力欄をクリア(目パチ口パク生成タブにて)

・ctrl+q：終了
'''


SCRIPTMSG = '''
目パチ口パク生成について

・基本的には公式のスクリプト生成ページと同じ文字列を生成します

・公式と異なる点は、文末に「,」がつくことと、
　画面下部の出力欄に生成されたスクリプトを貯められるところです

・出力された文字列は公式の場合と同じように.anmファイルに貼り付けて使います

・スクリプト生成のために必要なレイヤーパスは
　レイヤー名表示領域のレイヤー名をダブルクリックするとクリップボードにコピーされます

・生成されたスクリプトも、出力欄をダブルクリックすることでコピーできます

・入力欄が「開き」「ほぼ閉じ」などと分けられていますが、
　スクリプトはレイヤーの順番と個数にしか依存しないため、詰めて入力しても構いません
　例）開いた目と閉じた目のレイヤーを「開き」と「ほぼ開き」に入れても、
　　　「半開き」と「ほぼ閉じ」に入れても、「ほぼ開き」と「ほぼ閉じ」に入れても、
　　　結果は同じです

・目パチ、口パクシンプル、口パクあいうえおの入出力フォームは全て独立で機能します
'''


class FileFrame(ttk.Frame):
    '''
    ファイルを開くボタンやファイルのパスを表示するフレーム

    Attributes
    ----------
    label_msg: tk.Label
        「ファイルを開きました」などを表示するラベル
    label_filename: tk.Label
        ファイルのパスを表示するラベル
    combo_encode: ttk.Combobox
        文字コード選択のプルダウンメニュー
    '''
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.make_self()

    def make_self(self):
        '''
        各種ウィジェットを生成・配置するメソッド
        '''
        self.label_msg = tk.Label(self, text='')
        self.label_filename = ttk.Label(self, text='作業中のファイルはありません', width=60)

        encodes = ['sjis', 'cp932', 'euc_jp', 'macroman', 'utf_8', 'utf_16', 'utf_32']
        self.combo_encode = ttk.Combobox(self, values=encodes, width=12, state='readonly')
        self.combo_encode.current(0)
        self.combo_encode.grid(row=0, column=0, padx=6, pady=6, sticky='w')

        ttk.Label(self, text='作業中のファイル:', anchor='w').grid(row=1, column=0, padx=6, pady=6)
        self.label_msg.grid(row=0, column=0, columnspan=2, padx=6, pady=6)
        self.label_filename.grid(row=1, column=1, padx=6, pady=6)

        return self

    def show_msg(self, msg):
        '''
        label_msgの表示内容を変更する

        Parameters
        ----------
        msg: str
            表示する内容
        '''
        self.label_msg.config(text=msg)
        return self

    def show_filename(self, filename):
        '''
        label_filenameの表示内容を変更する

        Parameters
        ----------
        msg: str
            表示する内容
        '''
        self.label_filename.config(text=filename)
        return self

    def get_encode(self):
        '''
        選択されている文字コードを取得する

        Returns
        -------
        : str
            文字コード('sjis'、'utf8'など)
        '''
        return self.combo_encode.get()


class CtrlFrame(ttk.Frame):
    '''
    変換条件やボタンがあるフレーム
    qc: quick convert、チェックを入れたレイヤーを返還する
    cc: convert by condition、階層やら何やら条件を指定して変換

    Attributes
    ----------
    book: ttk.Notebook
        変換条件を選ぶタブのウィジェット
    combo_level: ttk.Combobox
        階層条件を指定するプルダウンメニュー
    entry_word: tk.Entry
        レイヤーの名前の条件になる文字列を入れる入力フォーム
    combo_match: ttk.Combobox
        レイヤーの名前と文字列が「一致するか」「包含関係か」を選ぶプルダウンメニュー
    combo_class: ttk.Combobox
        レイヤー、グループ、その両方、あるいはグループ直下のものを選ぶプルダウンメニュー
    button_converts: list
        tk.Buttonの配列。「!」をつける、「*」をつける、記号を消すボタン
    
    '''
    def __init__(self, master=None, **kwargs):
        '''
        ウィジェット生成をいくつかのメソッドに小分けし
        コンストラクタ内で実行している
        self.bookはここで生成する
        '''
        super().__init__(master, **kwargs)
        ttk.Label(self, text='変換対象選択条件', font=('', 11), anchor='w').pack(anchor='w', pady=12)
        self.book = ttk.Notebook(self)
        self.book.pack(anchor='w', pady=12)
        self.make_frame_qc()
        self.make_frame_cc()
        self.make_buttons()

    def make_frame_qc(self):  # qc: quick convert
        '''
        チェックを入れたレイヤーを変換するモードのタブに置くフレームを生成
        ラベルを一つ作るだけ
        '''
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text='チェックを入れたレイヤーが変換されます', font=('', 12)).pack(pady=24)
        self.book.add(frame_tmp, text='チェックしたレイヤー')
        return self

    def make_frame_cc(self):  # cc: convert by condition
        '''
        条件指定で変換するモードのタブに置くフレームを生成
        ラベル、プルダウンメニュー、入力フォームなどを次々と置いていく
        combo_levelだけはpsdファイルが読み込まれた後に中身を入れる(最大階層がわからないため)
        '''
        frame_tmp = ttk.Frame(self)

        column = 1
        self.combo_level = ttk.Combobox(frame_tmp, state='readonly', width=18)
        self.combo_level.grid(row=0, column=column, pady=6)

        column += 1
        label_tmp = ttk.Label(frame_tmp, text='層にある、')
        label_tmp.grid(row=0, column=column, pady=6)

        column += 1
        self.entry_word = tk.Entry(frame_tmp, width=12)
        self.entry_word.grid(row=0, column=column, pady=6)

        column += 1
        self.combo_match = ttk.Combobox(frame_tmp, values=['を含む', 'と一致する'], state='readonly', width=10)
        self.combo_match.grid(row=0, column=column, pady=6)
        self.combo_match.current(0)

        column += 1
        label_tmp = ttk.Label(frame_tmp, text='名前の')
        label_tmp.grid(row=0, column=column, pady=6)
        
        column = 1
        self.combo_class = ttk.Combobox(\
                frame_tmp, values=['物', 'レイヤー', 'グループ', 'グループの直下の物'], state='readonly', width=18)
        self.combo_class.grid(row=1, column=column, pady=6)
        self.combo_class.current(0)
        column += 1

        label_tmp = ttk.Label(frame_tmp, text='全て')
        label_tmp.grid(row=1, column=column, pady=6)

        self.book.add(frame_tmp, text='条件指定')
        return self

    def make_buttons(self):
        '''
        変換ボタン3つを作る
        '''
        frame_tmp = ttk.Frame(self)

        texts = ['「!」をつける', '「*」をつける', '「!」と「*」を消す']
        self.button_converts = []
        for i in range(3):
            self.button_converts.append(tk.Button(frame_tmp, text=texts[i], width=18))
            self.button_converts[i].grid(row=0, column=i, sticky='w', padx=6, pady=6)
        
        frame_tmp.pack()
        return self

    def selected_tab(self):
        '''
        現在選択されているタブを整数で返す

        Returns
        -------
        : int
            qcなら0、ccなら1
        '''
        return self.book.index(self.book.select())

    def select_tab(self, index):
        '''
        タブを選択する

        Parameters
        ----------
        index: int
            qcなら0、ccなら1
        '''
        self.book.select(index)
        return self

    def get_condition(self):
        '''
        条件指定変換において、各選択項目の値を取得して返す

        Returns
        -------
        c_level: int
            階層
        c_words: str
            入力フォームの文字列
        c_match: int
            レイヤー名一致条件。0: 文字列を含む、1: 文字列と一致する
        c_class: int
            対象の種類。0: 物、1: レイヤー、2: グループ、3: グループ直下の物
        '''
        c_level = self.combo_level.current()
        c_words = self.entry_word.get()
        c_match = self.combo_match.current()  # 0: include, 1: same
        c_class = self.combo_class.current()  # 0: both, 1: layer, 2: group, 3: things under the layer
        return c_level, c_words, c_match, c_class  # int, str, int, int

    def set_combo_level(self, values):
        '''
        階層プルダウンメニューに値を設定する

        Parameters
        ----------
        values: list
            階層(整数)のリスト。0 ~ psdファイルのlevel_max
        '''
        self.combo_level.config(values = values)
        self.combo_level.current(0)
        return self


class Anm_Frame(ttk.Frame):
    '''
    .anmファイルの書き出し機能関連ウィジェットのフレーム

    Attributes
    ----------
    anmlayers: list
        .anmファイルに書き出すレイヤーグループのリスト
    label_anmlist: list
        書き出し対象レイヤーの名前を表示するラベルのリスト
    button_clears: list
        書き出し対象レイヤーを「1つ外す」「全部外す」ボタンのリスト
    entry_anmtail: tk.Entry
        既定の名前で書きだす場合ファイル名の末尾に加える文字列を入力するためのフォーム
    button_exports: list
        「既定の名前で書き出す」「名前を指定して書き出す」のボタンのリスト
    '''
    def __init__(self, master, **kwargs):
        '''
        ウィジェットの生成とanmlayersの定義
        '''
        super().__init__(master, **kwargs)
        self.make_self()
        self.anmlayers = []

    def make_self(self):
        '''
        各種ウィジェットの生成と配置メソッド
        '''
        ttk.Label(self, text='・.anm書き出し', font=('', 11), anchor='w').grid(row=0, column=0, columnspan=2, sticky='w', padx=6, pady=6)

        #subframe 0
        subframe_tmp = ttk.Frame(self)
        ttk.Label(subframe_tmp, text='書き出し対象レイヤー').grid(row=0, column=0, columnspan=2, padx=6, pady=6)
        self.label_anmlist = []
        for i in range(4):
            ttk.Label(subframe_tmp, text=f'track{i}:').grid(row=i+1, column=0, padx=6, pady=6)
            self.label_anmlist.append(tk.Label(subframe_tmp, text='', anchor='w'))
            self.label_anmlist[i].grid(row=i+1, column=1, padx=6, pady=6, sticky='w')
        subframe_tmp.grid(row=1, column=0, padx=6, pady=6)
        self.button_clears = []
        texts = ['1つ外す', '全部外す']
        for i in range(2):
            self.button_clears.append(tk.Button(subframe_tmp, text=texts[i], width=12))
            self.button_clears[i].grid(row=5, column=i, padx=6, pady=6)
        #subframe 0

        ttk.Separator(self, orient='vertical').grid(row=1, column=1, sticky='ns', padx=32)

        #subframe 1
        subframe_tmp = ttk.Frame(self)
        ttk.Label(subframe_tmp, text='書き出し先指定').grid(row=0, column=0, columnspan=2, padx=6, pady=6)
        ttk.Label(subframe_tmp, text='末尾文字列').grid(row=1, column=0, padx=6, pady=6)

        self.entry_anmtail = tk.Entry(subframe_tmp, width=12)
        self.entry_anmtail.grid(row=1, column=1, padx=6, pady=6)
        
        self.button_exports = []
        texts = ['既定の名前で書き出し', '名前を指定して書き出し']
        for i in range(2):
            self.button_exports.append(tk.Button(subframe_tmp, text=texts[i], width=24))
            self.button_exports[i].grid(row=i+2, column=0, columnspan=2, padx=6, pady=6)
        subframe_tmp.grid(row=1, column=2, padx=6, pady=6)
        #subframe 1
        return self

    def stack_anmlayers(self, layer):
        '''
        書き出し対象レイヤーをanmlayersに追加し、それを表示する(ラベルの文字列を変更する)
        リストの要素数が4つ以上であればなにもしない

        Parameters
        ----------
        layer: psd_tools.api.layers.Group
            対象のレイヤーグループ
        '''
        if len(self.anmlayers) > 3:
            return self
        self.anmlayers.append(layer)
        target = self.label_anmlist[len(self.anmlayers) - 1].config(text=layer.name)
        return self

    def pop_anmlayers(self):
        '''
        書き出し対象レイヤーをanmlayersから一つ外し、それを表示する(ラベルの文字列を変更する)
        リストの要素数が0であればなにもしない
        '''
        if not self.anmlayers:
            return self
        self.anmlayers.pop()
        target = self.label_anmlist[len(self.anmlayers)].config(text='')
        return self

    def clear_anmlayers(self):
        '''
        anmlayersを空リストに初期化し、それを表示する
        '''
        self.anmlayers = []
        for label in self.label_anmlist:
            label.config(text='')
        return self

    def get_anmlayers(self):
        '''
        書き出し対象レイヤーを返す

        Returns
        -------
        anmlayers: list
            書き出し対象レイヤーのリスト
        '''
        return self.anmlayers

    def get_anmtail(self):
        '''
        anmtailに入力されている文字列を返す

        Returns
        -------
        : str
            入力内容の文字列
        '''
        return self.entry_anmtail.get()


class ToggleFrame(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bool_packed = False

    def pack(self, *args, anchor='w', **kwargs):
        if self.bool_packed:
            return None
        super().pack(*args, anchor=anchor, **kwargs)
        self.bool_packed = True
        return None

    def pack_forget(self, *args, **kwargs):
        if not self.bool_packed:
            return None
        super().pack_forget(*args, **kwargs)
        self.bool_packed = False
        return None

    def toggle(self, event=None):
        if self.bool_packed:
            self.pack_forget()
        else:
            self.pack()
        return 'break'


class LayerFrame(ttk.Frame):
    '''
    レイヤー構造表示領域においてレイヤーごとに生成されるフレーム
    レイヤーの階層、枝分かれ記号、名前、グループであれば追加ボタンなどが配置される
    グループの折りたたみをtkinterのpackとpack_forgetで処理するために各レイヤーごとにフレームを生成し、
    もしグループであればグループに属するレイヤーはグループが表示されるレイヤーの上に
    別のレイヤーを作ってpackする

    構造図解
    master: ShowFrame.canvas、あるいは上位グループのsubframe_tmp
        |- self
            |- frame_tmp: ここにレイヤー名やボタンなどが配置される
            |- subframe_tmp: このサブフレームが下層レイヤーにとってのmasterになる

    グループでない場合無駄にフレームを二つ作ることになるが、場合分けすると頭が痛くなるため妥協
    gridを使ってうまい感じcolumnを指定すればスマートにできる気もするが、頭が痛くなるため妥協
    packを使ってフレームの入れ子構造にするとreliefの視覚的効果で「同じグループがまとまってる感」も
    出るのでこのままでいいと思う

    Attributes
    ----------
    dict: dict
        あとから参照する必要があるオブジェクトを辞書型で保存
        label: 枝分かれ記号の表示部分。押したとき下位レイヤー表示を折りたたむ機能を後でバインドする
        selected: チェックボックスにチェックが入ってるかの真理値
        check: チェックボックス。shift+clickで一括チェックする機能をあとでバインドする
        entry: レイヤー名が入ってるreadonly入力フォーム。レイヤー名変換をしたとき中身を編集する

        button: .anm書き出し対象に追加するボタン
        folded: 下位レイヤーの表示が折りたたまれているかを保存する真理値
        subframe: 下位レイヤーを配置するフレーム
    '''

    def __init__(self, master, layer, **kwargs):
        '''
        レイヤーオブジェクトと階層を受け取ってウィジェットを生成する
        level=0、すなわちpsdファイル自身は表示内容が特別であるため(枝分かれ記号を表示しないとか)
        if level文を多用している。もっとスマートにできないものか

        各ウィジェットはdictでまとめるためメソッド内では全て_tmpつきのローカル変数になっている

        Parameters
        ----------
        master: tkinter object
            ウィジェットを配置できるtkinterオブジェクト。Tk、Frame、Canvasなど
        layer: psd_tools.api.layers.Group / PixelLayer
            レイヤー
        level: int
            レイヤーの階層
        '''
        super().__init__(master, **kwargs)

        frame_tmp = ttk.Frame(self)

        labelname = (str(layer.level) + ' ' * 4 * layer.level + '|-') if layer.level else '層'
        label_tmp = ttk.Label(frame_tmp, text=labelname)
        label_tmp.grid(row=0, column=0)

        selected_tmp = tk.BooleanVar()
        selected_tmp.set(False)

        check_tmp = tk.Checkbutton(frame_tmp, variable=selected_tmp)
        check_tmp.grid(row=0, column=1)

        entry_tmp = tk.Entry(frame_tmp, width=12)
        if layer.level:
            entry_tmp.insert(0, layer.name)
            entry_tmp.config(state='readonly')
            entry_tmp.bind('<Double-Button-1>', lambda event: pyperclip.copy('v1.' + layer.fullpath))
            entry_tmp.grid(row=0, column=2)
        else:
            ttk.Label(frame_tmp, text='レイヤー構造').grid(row=0, column=2)

        frame_tmp.pack(anchor='w')

        self.dict = {'label': label_tmp, 'selected': selected_tmp, 'check': check_tmp, 'entry': entry_tmp}

        if layer.is_group():
            button_tmp = tk.Button(frame_tmp, text='追加')
            button_tmp.grid(row=0, column=3) if layer.level else None
            self.dict['button'] = button_tmp

            folded_tmp = tk.BooleanVar()
            folded_tmp.set(False)
            self.dict['folded'] = folded_tmp

            subframe_tmp = ToggleFrame(self, relief='groove', padding=1)
            subframe_tmp.pack()
            label_tmp.bind('<Button-1>', subframe_tmp.toggle)
            self.dict['subframe'] = subframe_tmp


class ShowFrame(ttk.Frame):
    '''
    レイヤー構造表示領域のフレーム
    中にLayerFrameを再帰的に大量に生成する

    tkinter.Frameでは固定サイズにしてスクロールバーで表示を移動することができないらしくてcanvasを使っている
    canvasの大きさを親フレームに合わせて変える方法も調べたがうまくいかなかったため固定サイズになっている

    Attributes
    ----------
    dict_widgets: dict
        各レイヤーのLayerFrame.dictをまとめた辞書
        keyとしてレイヤーオブジェクトのメモリアドレス(id)を使っている
        layerオブジェクトにすると名前変えたとき正常に認識しない
        レイヤー名は重複することがあるため使えない
        リストにして番号で割りふることも考えたがその番号をどこかに保存してなければならない
        ということでidをkeyとしている
    width: int
        canvasの幅。新しいファイルを開いてcanvasを作り直すとき使いまわすために保存しておく
    height: int
        canvasの高さ。新しいファイルを開いてcanvasを作り直すとき使いまわすために保存しておく
    canvas: tk.Canvas
        ここにLayerFrameを置いていく
    frame_hierarchy: tk.Frame
        レイヤー構造表示フレームのうち最上位の物
    scroll_x: tk.Scrollbar
        canvasの横方向スクロールバー
    scroll_y: tk.Scrollbar
        canvasの縦方向スクロールバー
    '''

    def __init__(self, master, width=240, height=720):
        '''
        いくつかのインスタンス変数の初期
        そして空のframe_hierarchyを生成したりスクロールバーを配置する

        Parameters
        ----------
        master: tkinter object
            ウィジェットを配置できるtkinterオブジェクト。Tk、Frame、Canvasなど
        width: int
            canvasの幅
        height: int
            canvasの高さ
        '''
        super().__init__(master)
        self.dict_widgets = {}
        self.width = width
        self.height = height
        
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.frame_hierarchy = ttk.Frame(self.canvas)

        self.set_canvas().make_scrolls().make_buttons()

    def set_canvas(self):
        '''
        canvasの初期設定
        意味はよくわからないが、frame_hierarchyをおいて表示させたりするのに必要
        '''
        self.canvas.create_window(0, 0, window=self.frame_hierarchy, anchor='n')
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.xview_moveto('0.0')
        self.canvas.yview_moveto('0.0')

        self.canvas.grid(row=0, column=0, columnspan=2)
        return self

    def remake_canvas(self, psd):
        '''
        psdファイルを開いたときもともとあったウィジェットを全て破壊して
        新しく作り直すメソッド

        Parameters
        ----------
        pad: PSDImageExt
            対象のpsdファイルのオブジェクト
        '''
        self.frame_hierarchy.destroy()
        self.canvas.destroy()
        self.scroll_x.destroy()
        self.scroll_y.destroy()

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)

        self.frame_hierarchy = self.make_widgets_recursive(self.canvas, psd)
        self.set_canvas().make_scrolls()

    def make_scrolls(self):
        '''
        スクロールバーを作ってcanvasの表示と連動させるメソッド
        '''
        self.scroll_x = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.scroll_x.bind_all('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(-1*event.delta//120, 'units'))
        self.scroll_y.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-1*event.delta//120, 'units'))

        self.scroll_x.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.scroll_y.grid(row=0, column=2, sticky='ns')
        return self

    def make_buttons(self):
        self.button_foldall = []
        text = ['全て展開', '全て畳む']
        for i in range(2):
            self.button_foldall.append(tk.Button(self, text=text[i]))
            self.button_foldall[i].grid(row=2, column=i, padx=6, pady=6)
        return self

    def make_widgets_recursive(self, master, layer=None):
        '''
        レイヤーオブジェクトを受け取って再帰的にLayerFrameのインスタンスを作るメソッド
        layerがNoneの場合の処理はコンストラクタで使うために定義したけど特に意味がなかった模様
        基本的にはlayer=psdファイルオブジェクトを渡して全レイヤー構造を表示させるために使う

        動き:
        渡されたlayerとlevelからLayerFrameを生成し、そのdictをdict_widgetsに追加
        生成したLayerFrameをpackしたあと、もしlayerがグループであればその下位レイヤーをを
        引数としてmake_widgets_recursiveを実行し、返還されるフレームをpackしていく
        この時masterにはdict['subframe']を、levelには1増えたlevelを与える

        Parameters
        ----------
        master: tkinter object
            ウィジェットを配置できるtkinterオブジェクト。Tk、Frame、Canvasなど
        layer: psd_tools.api.layers.Group / PixelLayer
            レイヤー
        level: int
            レイヤーの階層

        Returns
        -------
        frame_tmp: tk.Frame
            再帰的に配置されたレイヤー構造ウィジェットの最上位フレーム
        '''
        if not layer:
            return ttk.Frame(master)
        
        frame_tmp = LayerFrame(master, layer)
        self.dict_widgets[id(layer)] = frame_tmp.dict
        frame_tmp.pack(anchor='w')

        if layer.is_group():
            for sublayer in layer:
                self.make_widgets_recursive(frame_tmp.dict['subframe'], sublayer).pack()

        return frame_tmp


class EntryFrameSimple(ttk.Frame):
    '''
    変換条件やボタンがあるフレーム
    mp: 目パチ
    kp: 口パク

    Attributes
    ----------
    combo_level: ttk.Combobox
        階層条件を指定するプルダウンメニュー
    entry_word: tk.Entry
        レイヤーの名前の条件になる文字列を入れる入力フォーム
    combo_match: ttk.Combobox
        レイヤーの名前と文字列が「一致するか」「包含関係か」を選ぶプルダウンメニュー
    combo_class: ttk.Combobox
        レイヤー、グループ、その両方、あるいはグループ直下のものを選ぶプルダウンメニュー
    button_converts: list
        tk.Buttonの配列。「!」をつける、「*」をつける、記号を消すボタン
    
    '''
    def __init__(self, master=None, **kwargs):
        '''
        ウィジェット生成をいくつかのメソッドに小分けし
        コンストラクタ内で実行している
        self.bookはここで生成する
        '''
        super().__init__(master, **kwargs)
        self.make_widgets()

    def make_widgets(self):
        annotation = ['開き', 'ほぼ開き', '半開き', 'ほぼ閉じ', '閉じ']
        self.entry_path = []
        self.button_clearline = []
        for i in range(5):
            self.entry_path.append(tk.Entry(self, width=48))

            self.entry_path[i].bind('<Control-d>', self.make_func_clear_line(i))
            self.entry_path[i].bind('<Control-a>', self.make_func_select_line(i))
            self.entry_path[i].bind('<Shift-ISO_Left_Tab>', self.make_func_move_to(i, 5, 0))
            self.entry_path[i].bind('<Tab>', self.make_func_move_to(i, 5, 1))

            self.button_clearline.append(tk.Button(self, text='クリア', command=self.make_func_clear_line(i)))

            ttk.Label(self, text=annotation[i]).grid(row=i, column=0, padx=6, pady=6)
            self.entry_path[i].grid(row=i, column=1, padx=6, pady=6)
            self.button_clearline[i].grid(row=i, column=2, padx=6, pady=6)
        return self

    def make_func_clear_line(self, i):
        def func_clear_line(event=None):
            self.entry_path[i].delete(0, 'end')
            return 'break'
        return func_clear_line

    def make_func_select_line(self, i):
        def func_select_line(event=None):
            self.entry_path[i].select_range(0, 'end')
            self.entry_path[i].icursor('end')
            return 'break'
        return func_select_line

    def make_func_move_to(self, now, total, direction):
        '''
        direction: 1-next, 0-back
        '''
        if direction:
            next_num = now+1 if now < total-1 else 0
        else:
            next_num = now-1 if now > 0 else total-1

        def func_move_to_back(event=None):
            self.entry_path[next_num].focus_set()
            self.make_func_select_line(next_num)()
            return 'break'

        return func_move_to_back

    def make_layer_blanket(self):
        sep = ''
        script = '{'
        for i in range(4, -1, -1):
            str_got = self.entry_path[i].get().strip()
            if str_got:
                script += f'{sep}"{str_got}"'
                sep = ','
        script += '}'
        return script


class EntryFrameAIUEO(EntryFrameSimple):

    def make_widgets(self):
        annotation = ['あ', 'い', 'う', 'え', 'お', 'ん']
        self.entry_path = []
        self.button_clearline = []
        for i in range(6):
            self.entry_path.append(tk.Entry(self, width=48))

            self.entry_path[i].bind('<Control-d>', self.make_func_clear_line(i))
            self.entry_path[i].bind('<Control-a>', self.make_func_select_line(i))
            self.entry_path[i].bind('<Shift-ISO_Left_Tab>', self.make_func_move_to(i, 6, 0))
            self.entry_path[i].bind('<Tab>', self.make_func_move_to(i, 6, 1))

            self.button_clearline.append(tk.Button(self, text='クリア', command=self.make_func_clear_line(i)))

            ttk.Label(self, text=annotation[i]).grid(row=i, column=0, padx=6, pady=6)
            self.entry_path[i].grid(row=i, column=1, padx=6, pady=6)
            self.button_clearline[i].grid(row=i, column=2, padx=6, pady=6)
        return self

    def make_layer_blanket(self):
        chars = ['a', 'i', 'u', 'e', 'o', 'N']
        sep = ''
        script = '{'
        for char, entry in zip(chars, self.entry_path):
            str_got = entry.get().strip()
            if str_got:
                script += f'{sep}{char}="{str_got}"'
                sep = ','
        script += '}'
        return script


class TextFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.make_widgets()
        self.text.bind('<Double-Button-1>', self.copytext)

    def make_widgets(self):
        self.text = tk.Text(self, width=72, height=6, state='disabled')
        self.text.grid(row=0, column=0, columnspan=3, padx=6, pady=6)

        self.button_copytext = tk.Button(self, text='コピー', command=self.copytext)
        self.button_copytext.grid(row=1, column=0, padx=6, pady=6)

        self.button_del1line = tk.Button(self, text='1行削除', command=self.del1line_text)
        self.button_del1line.grid(row=1, column=1, padx=6, pady=6)

        self.button_cleartext = tk.Button(self, text='クリア', command=self.clear_text)
        self.button_cleartext.grid(row=1, column=2, padx=6, pady=6)
        return self

    def copytext(self, event=None):
        content = self.text.get('1.0', 'end-1c')
        pyperclip.copy(content)
        return 'break'

    def del1line_text(self, event=None):
        self.text.config(state='normal')
        self.text.delete('end-2l', 'end-1c')
        self.text.config(state='disabled')
        return 'break'
        
    def clear_text(self, event=None):
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.config(state='disabled')
        return 'break'

    def addline(self, line):
        self.text.config(state='normal')
        self.text.insert('end', line+'\n')
        self.text.config(state='disabled')
        return self


class MPOptionFrame(ttk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.make_widgets()

    def make_widgets(self):
        ttk.Label(self, text='間隔(秒)').grid(row=0, column=0, padx=6, pady=6)
        ttk.Label(self, text='            速さ').grid(row=0, column=2, padx=6, pady=6)
        ttk.Label(self, text='            オフセット').grid(row=0, column=4, padx=6, pady=6)

        self.entry_option = []
        options = [4, 1, 0]
        for i in range(3):
            self.entry_option.append(tk.Entry(self, width=3))
            self.entry_option[i].grid(row=0, column=2*i+1, padx=6, pady=6)
            self.entry_option[i].insert(0, str(options[i]))

        return self

    def get_option(self):
        option = ''
        for entry in self.entry_option:
            option += ',' + entry.get().strip()
        return option
        

class KPOptionFrame(ttk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.make_widgets()

    def make_widgets(self):
        ttk.Label(self, text='子音処理').grid(row=0, column=0, padx=6, pady=6)
        self.entry_consonant = tk.Entry(self, width=3)
        self.entry_consonant.insert(0, '1')
        self.entry_consonant.grid(row=0, column=1, padx=6, pady=6)
        self.bool_option = tk.BooleanVar()
        self.bool_option.set(True)
        ttk.Label(self, text='                        ').grid(row=0, column=2, padx=2, pady=6)
        tk.Checkbutton(self, variable=self.bool_option).grid(row=0, column=3, padx=2, pady=6)
        ttk.Label(self, text='口パク準備がなくても有効').grid(row=0, column=4, padx=2, pady=6)

        return self

    def get_option(self):
        option = f',{self.entry_consonant.get().strip()},{"true" if self.bool_option.get() else "false"}'
        return option

class ScriptBook(ttk.Notebook):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.make_tabs()

    def make_tabs(self):
        title = ['目パチ生成', '口パク生成', 'あいうえお口パク生成']

        entryframe = [EntryFrameSimple, EntryFrameSimple, EntryFrameAIUEO]
        optionframe = [MPOptionFrame, KPOptionFrame, KPOptionFrame]

        self.frame_entry = []
        self.frame_option = []
        self.button_addline = []
        self.frame_text = []

        for i in range(3):
            subframe = ttk.Frame(self)
            ttk.Label(subframe, text=title[i]).pack(padx=6, pady=6, anchor='w')
            self.frame_entry.append(entryframe[i](subframe))
            self.frame_entry[i].pack(padx=6, pady=6)
            self.frame_option.append(optionframe[i](subframe))
            self.frame_option[i].pack(padx=6, pady=6)
            self.button_addline.append(tk.Button(subframe, text='行生成', width=24, command = self.make_func_addline(i)))
            self.button_addline[i].pack(padx=6, pady=6)
            self.frame_text.append(TextFrame(subframe))
            self.frame_text[i].pack(padx=6, pady=6)

            self.add(subframe, text=12*' '+title[i]+12*' ')
        return self

    def make_func_addline(self, i):
        option = ['Blinker', 'LipSyncSimple', 'LipSyncLab']
        def func_addline(event=None):
            script = f'  require("PSDToolKit").{option[i]}'
            script += f'.new({self.frame_entry[i].make_layer_blanket()}{self.frame_option[i].get_option()}),'
            self.frame_text[i].addline(script)
            return 'break'
        return func_addline


class HelpWindow(tk.Toplevel):
    '''
    Helpを押したとき表示されるウィンドウ
    インスタンスメソッドは項目別のタブにヘルプ文字列を配置するだけ

    Attributes
    ----------
    book: ttk.Notebook
        各項目別のフレームを配置するタブメニュー
    '''

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.book = ttk.Notebook(self)
        self.book.pack(anchor='w')
        self.make_tab_file()
        self.make_tab_convert()
        self.make_tab_check()
        self.make_tab_export()
        self.make_tab_hotkeys()
        self.make_tab_script()

    def make_tab_file(self):
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text=FILEMSG, font=('', 10), anchor='w').pack(padx=6, pady=6)
        self.book.add(frame_tmp, text='ファイル')
        return self

    def make_tab_convert(self):
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text=CONVMSG, font=('', 10), anchor='w').pack(padx=6, pady=6)
        self.book.add(frame_tmp, text='変換')
        return self

    def make_tab_check(self):
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text=CHECKMSG, font=('', 10), anchor='w', justify='left').pack(padx=6, pady=6)
        self.book.add(frame_tmp, text='チェックボックスの動き')
        return self

    def make_tab_export(self):
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text=EXPORTMSG, font=('', 10), anchor='w', justify='left').pack(padx=6, pady=6)
        self.book.add(frame_tmp, text='.anmの書き出し')
        return self

    def make_tab_hotkeys(self):
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text=HOTKEYS, font=('', 10), anchor='w', justify='left').pack(padx=6, pady=6)
        self.book.add(frame_tmp, text='ショートカットキー')
        return self

    def make_tab_script(self):
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text=SCRIPTMSG, font=('', 10), anchor='w', justify='left').pack(padx=6, pady=6)
        self.book.add(frame_tmp, text='目パチ口パク')
        return self


class RootWindow(tk.Tk):
    '''
    アプリのトップウィンドウ

    Attributes
    ----------
    frame_file: FileFrame
        ファイル関連ウィジェットが配置されたフレーム
    frame_ctrl: CtrlFrame
        変換関連ウィジェットが配置されたフレーム
    frame__anm: Anm_Frame
        .anmファイル書き出し関連ウィジェットが配置されたフレーム
    frame_show: ShowFrame
        レイヤー構造表示領域のフレーム
    '''

    def __init__(self, **kwargs):
        '''
        小分けした初期化メソッドをまとめて実行し、ウィンドウの表示名を変える
        '''
        super().__init__(**kwargs)
        self.make_menu()
        self.make_widgets()
        self.alias_widgets()
        self.title('.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラム')

    def make_widgets(self):
        '''
        各フレームを生成して配置する
        '''
        frame_L = ttk.Frame(self)
        self.frame_file = FileFrame(frame_L)
        self.frame_file.pack(anchor='w')

        # ttk.Separator(frame_L, orient='horizontal').pack(fill='both', expand=True, pady=32)
        book_tmp = ttk.Notebook(frame_L)
        book_tmp.pack()

        frame_convert = ttk.Frame(book_tmp)

        self.frame_ctrl = CtrlFrame(frame_convert)
        self.frame_ctrl.pack(anchor='w')

        ttk.Separator(frame_convert, orient='horizontal').pack(fill='both', expand=True, pady=32)

        self.frame__anm = Anm_Frame(frame_convert)
        self.frame__anm.pack(anchor='w')

        book_tmp.add(frame_convert, text='レイヤー名変換')

        book_tmp.add(ScriptBook(self), text='目パチ口パク生成')

        frame_L.grid(row=0, column=0, sticky='n', padx=12, pady=12)
        ttk.Separator(self, orient='vertical').grid(row=0, column=1, sticky='ns', padx=16)

        self.frame_show = ShowFrame(self)
        self.frame_show.grid(row=0, column=2, padx=12, pady=12)
        return self

    def alias_widgets(self):
        '''
        下位フレームのインスタンスメソッドを自らのインスタンスメソッドとして定義する
        '''
        self.show_msg = self.frame_file.show_msg
        self.show_filename = self.frame_file.show_filename
        self.get_encode = self.frame_file.get_encode

        self.selected_tab = self.frame_ctrl.selected_tab
        self.select_tab = self.frame_ctrl.select_tab
        self.set_combo_level = self.frame_ctrl.set_combo_level
        self.get_condition = self.frame_ctrl.get_condition
        self.button_converts = self.frame_ctrl.button_converts

        self.stack_anmlayers = self.frame__anm.stack_anmlayers
        self.pop_anmlayers = self.frame__anm.pop_anmlayers
        self.clear_anmlayers = self.frame__anm.clear_anmlayers
        self.get_anmlayers = self.frame__anm.get_anmlayers
        self.get_anmtail = self.frame__anm.get_anmtail
        self.button_clears = self.frame__anm.button_clears
        self.button_exports = self.frame__anm.button_exports

        self.button_foldall = self.frame_show.button_foldall

        return self

    def make_menu(self):
        '''
        トップバーメニューを生成する
        書き出しや変換メニューは最初は非活性化の状態にしておく
        '''
        self.menu_root = tk.Menu(self)

        self.menu_file = tk.Menu(self.menu_root, tearoff=0)
        self.menu_file.add_command(label='開く', accelerator='Ctrl+O')
        self.menu_file.add_command(label='上書き保存', accelerator='Ctrl+s')
        self.menu_file.add_command(label='別名で保存', accelerator='Ctrl+Shift+s')
        self.menu_file.add_separator()
        self.menu_file.add_command(label='既定の名前で書き出す', accelerator='Ctrl+e')
        self.menu_file.add_command(label='名前を指定して書き出す', accelerator='Ctrl+Shift+e')
        self.menu_file.add_separator()
        self.menu_file.add_command(label='終了', accelerator='Ctrl+q')
        for i in [1, 2, 4, 5]:
            self.menu_file.entryconfig(i, state='disabled')

        self.menu_edit = tk.Menu(self.menu_root, tearoff=0)
        self.menu_edit.add_command(label='「!」をつける', accelerator='F5')
        self.menu_edit.add_command(label='「*」をつける', accelerator='F6')
        self.menu_edit.add_command(label='記号を外す', accelerator='F7')
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='戻す', accelerator='Ctrl+z')
        self.menu_edit.add_command(label='やり直す', accelerator='Ctrl+y / Ctrl+Shift+z')
        for i in [0, 1, 2, 4, 5]:
            self.menu_edit.entryconfig(i, state='disabled')

        self.menu_help= tk.Menu(self.menu_root, tearoff=0)
        self.menu_help.add_command(label='ヘルプを開く', accelerator='F1')
        self.menu_help.add_command(label='githubページを開く')

        self.menu_root.add_cascade(label='ファイル', menu=self.menu_file)
        self.menu_root.add_cascade(label='編集', menu=self.menu_edit)
        self.menu_root.add_cascade(label='ヘルプ', menu=self.menu_help)

        self.config(menu=self.menu_root)
        return self

    def unre_state(self, which, state):
        '''
        「戻す」と「やり直す」メニューは変換ログの状態によって頻繁に活性化・非活性化状態を変える
        そのため、簡単に制御できるようにメソッドとして定義する

        Parameters
        ----------
        which: int
            どのメニューを指定するか。0: 戻す、1: やり直す
        state: int
            させたい状態。0: 非活性化、1: 活性化
        '''
        self.menu_edit.entryconfig(which+4, state='normal' if state else 'disabled')
        return self


class test():
    x = 0
    @classmethod
    def func(cls, i):
        if test.x > 100:
            return test.x
        else:
            test.x += i
            return test.func(i)

if __name__ == '__main__':
    root = RootWindow()
    # test
    root.mainloop()
