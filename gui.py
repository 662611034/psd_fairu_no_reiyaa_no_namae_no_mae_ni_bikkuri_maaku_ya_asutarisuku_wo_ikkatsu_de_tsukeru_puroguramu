import tkinter as tk
import tkinter.ttk as ttk


FILEMSG='''
・ファイルを開くとき文字コードを指定することができます

・上書き保存の場合は文字コード選択メニューの状況によらず
　ファイルを開いた時の文字コードで保存されます

・別名で保存の場合は選択メニューで指定されている文字コードで保存されます
'''

CONVMSG = '''
・変換対象選択条件タブを切り替えて対象レイヤーの指定方式を変えることができます

・既に「!」や「*」がついているレイヤーは変換されません

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

・Rootのチェックボックスは他のチェックボックスを操作するための物です
　選択していても変換対象にはなりません
'''

EXPORTMSG='''
・レイヤーの隣のボタンを押して出力対象グループを選択することができます

・今選択されているレイヤーは画面から確認できます

・.anmファイルの書き出しボタンを押すと自動的に現在の状態で上書き保存されます
　ご注意ください

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

・ctrl+z / ctrl+(y/shift+z)：やり直す / やり直す

・ctrl+(1/2)：変換するレイヤー条件を選択

・ctrl+e / crrl+shift+e：既定の名前で / 名前を指定して.anmファイルを出力

・ctrl+(a / A)：全てのレイヤーにチェックを入れる / 外す

・ctrl+q：終了
'''


class FileFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.make_self()

    def make_self(self):
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
        self.label_msg.config(text=msg)
        return self

    def show_filename(self, filename):
        self.label_filename.config(text=filename)
        return self

    def get_encode(self):
        return self.combo_encode.get()


class CtrlFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        ttk.Label(self, text='変換対象選択条件', font=('', 11), anchor='w').pack(anchor='w', pady=12)
        self.book = ttk.Notebook(self)
        self.book.pack(anchor='w', pady=12)
        self.make_frame_qc()
        self.make_frame_cc()
        self.make_buttons()

    def make_frame_qc(self):  # qc: quick convert
        frame_tmp = ttk.Frame(self.book)
        ttk.Label(frame_tmp, text='チェックを入れたレイヤーが変換されます', font=('', 12)).pack(pady=24)
        self.book.add(frame_tmp, text='チェックしたレイヤー')
        return self

    def make_frame_cc(self):  # cc: convert by condition
        frame_tmp = ttk.Frame(self)

        column = 1
        self.combo_depth = ttk.Combobox(frame_tmp, state='readonly', width=18)
        self.combo_depth.grid(row=0, column=column, pady=6)

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
        frame_tmp = ttk.Frame(self)

        texts = ['「!」をつける', '「*」をつける', '「!」と「*」を消す']
        self.button_converts = []
        for i in range(3):
            self.button_converts.append(tk.Button(frame_tmp, text=texts[i], width=18))
            self.button_converts[i].grid(row=0, column=i, sticky='w', padx=6, pady=6)
        
        frame_tmp.pack()
        return self

    def selected_tab(self):
        # 0: qc, 1: cc
        return self.book.index(self.book.select())

    def select_tab(self, index):
        # 0: qc, 1: cc
        self.book.select(index)
        return self

    def get_condition(self):
        c_depth = self.combo_depth.current()
        c_words = self.entry_word.get()
        c_match = self.combo_match.current()  # 0: include, 1: same
        c_class = self.combo_class.current()  # 0: both, 1: layer, 2: group, 3: things under the layer
        return c_depth, c_words, c_match, c_class  # int, str, int, int

    def set_combo_depth(self, values):
        self.combo_depth.config(values = values)
        self.combo_depth.current(0)
        return self


class Anm_Frame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.make_self()
        self.anmlayers = []

    def make_self(self):
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
        if len(self.anmlayers) > 3:
            return self
        self.anmlayers.append(layer)
        target = self.label_anmlist[len(self.anmlayers) - 1].config(text=layer.name)
        return self

    def pop_anmlayers(self):
        if not self.anmlayers:
            return self
        self.anmlayers.pop()
        target = self.label_anmlist[len(self.anmlayers)].config(text='')
        return self

    def clear_anmlayers(self):
        self.anmlayers = []
        for label in self.label_anmlist:
            label.config(text='')
        return self

    def get_anmlayers(self):
        return self.anmlayers

    def get_anmtail(self):
        return self.entry_anmtail.get()


class LayerFrame(ttk.Frame):

    def __init__(self, master, layer, depth, **kwargs):
        super().__init__(master, **kwargs)

        frame_tmp = ttk.Frame(self)

        labelname = (str(depth) + ' ' * 4 * depth + '|-') if depth else '層'
        label_tmp = ttk.Label(frame_tmp, text=labelname)
        label_tmp.grid(row=0, column=0)

        selected_tmp = tk.BooleanVar()
        selected_tmp.set(False)

        check_tmp = tk.Checkbutton(frame_tmp, variable=selected_tmp)
        check_tmp.grid(row=0, column=1)

        entry_tmp = tk.Entry(frame_tmp, width=12)
        if depth:
            entry_tmp.insert(0, layer.name)
            entry_tmp.config(state='readonly')
            entry_tmp.grid(row=0, column=2)
        else:
            ttk.Label(frame_tmp, text='レイヤー構造').grid(row=0, column=2)

        frame_tmp.pack(anchor='w')

        self.dict = {'label': label_tmp, 'selected': selected_tmp, 'check': check_tmp, 'entry': entry_tmp}

        if layer.is_group():
            button_tmp = tk.Button(frame_tmp, text='追加', command=print)  ################need to make func
            button_tmp.grid(row=0, column=3) if depth else None
            self.dict['button'] = button_tmp

            folded_tmp = tk.BooleanVar()
            folded_tmp.set(False)
            self.dict['folded'] = folded_tmp

            subframe_tmp = ttk.Frame(self, relief='groove', padding=1)
            subframe_tmp.pack(anchor='w')
            self.dict['subframe'] = subframe_tmp


class ShowFrame(ttk.Frame):
    def __init__(self, master, width=240, height=720):
        super().__init__(master)
        self.dict_widgets = {}
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.frame_hierarchy = ttk.Frame(self.canvas)

        self.set_canvas().make_scrolls()

    def set_canvas(self):
        self.canvas.create_window(0, 0, window=self.frame_hierarchy, anchor='n')
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.xview_moveto('0.0')
        self.canvas.yview_moveto('0.0')

        self.canvas.grid(row=0, column=0)
        return self

    def remake_canvas(self, psd):
        self.frame_hierarchy.destroy()
        self.canvas.destroy()
        self.scroll_x.destroy()
        self.scroll_y.destroy()

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)

        self.frame_hierarchy = self.make_widgets_recursive(self.canvas, psd, 0)
        self.set_canvas().make_scrolls()

    def make_scrolls(self):
        self.scroll_x = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.scroll_x.bind_all('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(-1*event.delta//120, 'units'))
        self.scroll_y.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-1*event.delta//120, 'units'))

        self.scroll_x.grid(row=1, column=0, sticky='ew')
        self.scroll_y.grid(row=0, column=1, sticky='ns')
        return self

    def make_widgets_recursive(self, master, layer=None, depth=0):
        if not layer:
            return ttk.Frame(master)
        
        frame_tmp = LayerFrame(master, layer, depth)
        self.dict_widgets[id(layer)] = frame_tmp.dict
        frame_tmp.pack(anchor='w')

        if layer.is_group():
            # frame_tmp.dict['check'].bind('<Button-1>', self.make_fcheck(layer))
            # frame_tmp.dict['label'].bind('<Button-1>', self.make_ffold(layer)) if depth else None
            for sublayer in layer:
                self.make_widgets_recursive(frame_tmp.dict['subframe'], sublayer, depth+1).pack(anchor='w')

        return frame_tmp


class HelpWindow(tk.Toplevel):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.book = ttk.Notebook(self)
        self.book.pack(anchor='w')
        self.make_tab_file()
        self.make_tab_convert()
        self.make_tab_check()
        self.make_tab_export()
        self.make_tab_hotkeys()

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


class RootWindow(tk.Tk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_menu()
        self.make_widgets()
        self.alias_obj()
        self.title('.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラム')

    def make_widgets(self):
        frame_L = ttk.Frame(self)
        self.frame_file = FileFrame(frame_L)
        self.frame_file.pack(anchor='w')

        ttk.Separator(frame_L, orient='horizontal').pack(fill='both', expand=True, pady=32)

        self.frame_ctrl = CtrlFrame(frame_L)
        self.frame_ctrl.pack(anchor='w')

        ttk.Separator(frame_L, orient='horizontal').pack(fill='both', expand=True, pady=32)

        self.frame__anm = Anm_Frame(frame_L)
        self.frame__anm.pack(anchor='w')

        frame_L.grid(row=0, column=0, sticky='n', padx=12, pady=12)
        ttk.Separator(self, orient='vertical').grid(row=0, column=1, sticky='ns', padx=16)

        self.frame_show = ShowFrame(self)
        self.frame_show.grid(row=0, column=2, padx=12, pady=12)

    def alias_obj(self):
        self.show_msg = self.frame_file.show_msg
        self.show_filename = self.frame_file.show_filename
        self.get_encode = self.frame_file.get_encode

        self.selected_tab = self.frame_ctrl.selected_tab
        self.select_tab = self.frame_ctrl.select_tab
        self.set_combo_depth = self.frame_ctrl.set_combo_depth
        self.get_condition = self.frame_ctrl.get_condition
        self.button_converts = self.frame_ctrl.button_converts

        self.stack_anmlayers = self.frame__anm.stack_anmlayers
        self.pop_anmlayers = self.frame__anm.pop_anmlayers
        self.clear_anmlayers = self.frame__anm.clear_anmlayers
        self.get_anmlayers = self.frame__anm.get_anmlayers
        self.get_anmtail = self.frame__anm.get_anmtail
        self.button_clears = self.frame__anm.button_clears
        self.button_exports = self.frame__anm.button_exports

        return self

    def make_menu(self):
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
        # 0: 戻す, 1: やり直す
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
    # ShowFrame(root).grid(row=0, column=1, rowspan=3)
    # FileFrame(root).grid(row=0, column=0)
    # CtrlFrame(root).grid(row=1, column=0)
    # Anm_Frame(root).grid(row=2, column=0)
    # test()
    # root.mainloop()
    print(test().func(2))
