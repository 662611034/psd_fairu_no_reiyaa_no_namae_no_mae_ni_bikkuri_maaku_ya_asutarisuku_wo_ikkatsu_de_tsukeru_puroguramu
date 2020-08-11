import tkinter as tk
import tkinter.ttk as ttk

HOTKEYS = '''
キーボードショートカット一覧

・ctrl+o：ファイルを開く

・ctrl+s：上書き保存

・ctrl+shift+s：別名で保存

・F5：変換

・ctrl+z：戻す

・ctrl+(y/shift+z)：やり直す

・ctrl+(1/2)：変換するレイヤー条件を選択

・ctrl+(3/4)：変換動作を選択

・ctrl+e：.anmファイルを生成

・ctrl+q：終了
'''


HELPMSG = '''
.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラムです。


1. 変換について

・条件を指定し、その条件にあったレイヤーの名前に記号をつけたり、外したりします

・層は画面右側に表示されています

・層に0を指定した場合全ての層が対象になります

・変換をしてもすでに「!」や「*」がついているレイヤーは変換されません


2. チェックボックスについて

・shift+クリックで直下の層を全て選択します

・ctrl+shift+クリックで下位の層を全て選択します


3. .anm出力について

・チェックがついているグループを.anmファイルに出力します

・出力されるファイルは.psdファイルと同じフォルダに「(同じ名前).anm」で保存されます

・グループが4つより多く選択されている場合でも4つまでしか出力しません

・グループでないレイヤーは無視します
'''


class CtrlFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.make_frame_file().make_frame_select().make_frame_action()
        self.make_frame_button()

    def make_frame_file(self):
        self.frame_file = ttk.Frame(self)

        self.label_msg = tk.Label(self.frame_file, text='')
        self.label_filename = ttk.Label(self.frame_file, text='作業中のファイルはありません')

        ttk.Label(self.frame_file, text='作業中のファイル', anchor='w').grid(row=1, column=0, padx=6, pady=6)
        self.label_msg.grid(row=0, column=0, columnspan=2, padx=12, pady=6)
        self.label_filename.grid(row=1, column=1, padx=12, pady=6)

        self.frame_file.pack(padx=12, pady=6, anchor='w')
        return self

    def make_frame_select(self):
        self.frame_select = ttk.Frame(self)
        ttk.Label(self.frame_select, text='・レイヤー選択条件').pack(anchor='w', padx=12)

        self.var_select = tk.IntVar()
        self.var_select.set(0)

        self.subframe_select = []
        self.radio_mode = []

        for i in range(2):
            self.subframe_select.append(ttk.Frame(self.frame_select))
            self.subframe_select[i].pack(anchor='w')
            self.radio_mode.append(\
                    ttk.Radiobutton(self.subframe_select[i], text='', value=i, variable=self.var_select))
            self.radio_mode[i].grid(row=0, column=0, padx=6, pady=6)

        # subframe[0]
        column = 1
        self.combo_depth = ttk.Combobox(self.subframe_select[0], state='readonly', width=18)
        self.combo_depth.grid(row=0, column=column, pady=5)
        self.combo_depth.bind('<Button-1>', lambda x : self.var_select.set(0))

        column += 1
        label_tmp = ttk.Label(self.subframe_select[0], text='層にある、')
        label_tmp.bind('<Button-1>', lambda x : self.var_select.set(0))
        label_tmp.grid(row=0, column=column, pady=5)

        column += 1
        self.entry_word = tk.Entry(self.subframe_select[0], width=12)
        self.entry_word.grid(row=0, column=column, pady=5)
        self.entry_word.bind('<Button-1>', lambda x : self.var_select.set(0))

        column += 1
        self.combo_match = ttk.Combobox(self.subframe_select[0], values=['を含む', 'と一致する'], state='readonly', width=10)
        self.combo_match.grid(row=0, column=column, pady=5)
        self.combo_match.bind('<Button-1>', lambda x : self.var_select.set(0))

        column += 1
        label_tmp = ttk.Label(self.subframe_select[0], text='名前の')
        label_tmp.bind('<Button-1>', lambda x : self.var_select.set(0))
        label_tmp.grid(row=0, column=column, pady=5)
        
        column = 1
        self.combo_class = ttk.Combobox(\
                self.subframe_select[0], values=['物', 'レイヤー', 'グループ', 'グループの直下の物'], state='readonly', width=18)
        self.combo_class.grid(row=1, column=column, pady=5)
        self.combo_class.bind('<Button-1>', lambda x : self.var_select.set(0))
        column += 1

        label_tmp = ttk.Label(self.subframe_select[0], text='全て')
        label_tmp.bind('<Button-1>', lambda x : self.var_select.set(0))
        label_tmp.grid(row=1, column=column, pady=5)

        # subframe[1]
        label_tmp = ttk.Label(self.subframe_select[1], text='チェックが入っているレイヤー全て')
        label_tmp.bind('<Button-1>', lambda x : self.var_select.set(1))
        label_tmp.grid(row=0, column=1, pady=5)

        self.combo_match.current(0)
        self.combo_class.current(0)
        self.frame_select.pack(pady=6)
        return self

    def make_frame_action(self):
        self.frame_action = ttk.Frame(self)
        ttk.Label(self.frame_action, text='・実行内容').pack(anchor='w', padx=12)

        self.var_action = tk.IntVar()
        self.var_action.set(0)

        self.subframe_action = []
        self.radio_mode = []

        for i in range(2):
            self.subframe_action.append(ttk.Frame(self.frame_action))
            self.subframe_action[i].pack(anchor='w')
            self.radio_mode.append(\
                    ttk.Radiobutton(self.subframe_action[i], text='', value=i, variable=self.var_action))
            self.radio_mode[i].grid(row=0, column=0, padx=6, pady=6)

        # subframe[0]
        label_tmp = ttk.Label(self.subframe_action[0], text='に')
        label_tmp.bind('<Button-1>', lambda x : self.var_action.set(0))
        label_tmp.grid(row=0, column=1, pady=5)
        self.combo_symbol = ttk.Combobox(self.subframe_action[0], values=['!', '*'], state='readonly', width=4)
        self.combo_symbol.bind('<Button-1>', lambda x: self.var_action.set(0))
        self.combo_symbol.grid(row=0, column=2, padx=6, pady=6)
        label_tmp = ttk.Label(self.subframe_action[0], text='をつける')
        label_tmp.bind('<Button-1>', lambda x : self.var_action.set(0))
        label_tmp.grid(row=0, column=3, pady=5)
        
        self.combo_symbol.current(0)

        # subframe[1]
        label_tmp = ttk.Label(self.subframe_action[1], text='から「!」と「*」を消す')
        label_tmp.bind('<Button-1>', lambda x : self.var_action.set(1))
        label_tmp.grid(row=0, column=1, pady=5)

        self.frame_action.pack(pady=6, anchor='w')
        return self

    def make_frame_button(self):
        self.frame_button = ttk.Frame(self)

        self.button_convert = tk.Button(self.frame_button, text='変換', width=24)
        self.button_convert.grid(row=0, column=0, padx=16, pady=5)
        self.button_export = tk.Button(self.frame_button, text='.anmファイル出力', width=24)
        self.button_export.grid(row=0, column=1, padx=16, pady=5)

        self.frame_button.pack(pady=6)
        return self

    def get_select(self):
        # return 0 or 1 in int
        return self.var_select.get()

    def get_action(self):
        # return 0 or 1 in int
        return self.var_action.get()

    def get_condition(self):
        c_depth = self.combo_depth.current()
        c_words = self.entry_word.get()
        c_match = self.combo_match.current()  # 0: include, 1: same
        c_class = self.combo_class.current()  # 0: both, 1: layer, 2: group, 3: things under the layer
        return c_depth, c_words, c_match, c_class  # int, str, int, int

    def get_symbol(self):
        return self.combo_symbol.get()


class ShowFrame(ttk.Frame):
    def __init__(self, master, width=240, height=720):
        super().__init__(master)
        self.make_canvas(width, height)
        self.width = width
        self.height = height

    def make_canvas(self, width, height):
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.frame_hierarchy = ttk.Frame(self.canvas)

        self.canvas.create_window(0, 0, window=self.frame_hierarchy)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.scroll_x = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.scroll_x.bind_all('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(-1*event.delta//120, 'units'))
        self.scroll_y.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-1*event.delta//120, 'units'))

        self.canvas.yview_moveto('0.0')

        self.canvas.grid(row=0, column=0)
        self.scroll_x.grid(row=1, column=0, sticky='ew')
        self.scroll_y.grid(row=0, column=1, sticky='ns')
        return self

    def remake_frame(self):
        x_position = str(self.scroll_x.get()[0])
        y_position = str(self.scroll_y.get()[0])

        self.frame_hierarchy.destroy()
        self.canvas.destroy()
        self.make_canvas(self.width, self.height)
        self.frame_hierarchy = ttk.Frame(self.canvas)

        yield self.frame_hierarchy
        
        self.canvas.create_window(0, 0, window=self.frame_hierarchy)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.xview_moveto(x_position)
        self.canvas.yview_moveto(y_position)
        return self

    def make_widgets(self):
        self.dict_widgets = {}
        ttk.Label(self.frame_hierarchy, text='層  レイヤー名', anchor='w').pack(anchor='w')
        for layer, depth in self.handler.layer_list():
            frame_tmp = ttk.Frame(self.frame_hierarchy)
            ttk.Label(frame_tmp, text=str(depth) + ' ' * 4 * depth + '|-').grid(row=0, column=0)
            bool_tmp = tk.BooleanVar()
            bool_tmp.set(False)
            check_tmp = tk.Checkbutton(frame_tmp, variable=bool_tmp)
            check_tmp.grid(row=0, column=1)
            check_tmp.bind('<Button-1>', self.make_fclicked(layer))
            entry_tmp = tk.Entry(frame_tmp, width=12)
            entry_tmp.insert(0, layer.name)
            entry_tmp.config(state='readonly')
            entry_tmp.grid(row=0, column=2)
            self.dict_widgets[layer] = {'bool': bool_tmp, 'entry': entry_tmp}
            frame_tmp.pack(anchor='w')
        return self

    def make_fclicked(self, layer):
        def clicked(event=None):
            # event.state: click-8, shift click-9, ctrl shict click=13
            bool_got = self.dict_widgets[layer]['bool'].get()
            if event.state == 9 and layer.is_group():
                checkrange = layer
            elif event.state == 13 and layer.is_group():
                checkrange = [sublayer for sublayer, _ in self.handler.layer_list(layer)]
            else:
                checkrange = []
            for sublayer in checkrange:
                self.dict_widgets[sublayer]['bool'].set(not bool_got)
        return clicked


class HelpWindow(tk.Toplevel):

    def __init__(self, master=None, *args):
        super().__init__(master, *args)
        self.book = ttk.Notebook(self)
        self.book.pack(anchor='w')
        self.make_tab_helpmsg()
        self.make_tab_hotkeys()

    def make_tab_helpmsg(self):
        frame = ttk.Frame(self.book)
        ttk.Label(frame, text=HELPMSG, font=('', 10), anchor='w').pack(padx=6, pady=6)
        self.book.add(frame, text='使い方')
        return self

    def make_tab_hotkeys(self):
        frame = ttk.Frame(self.book)
        ttk.Label(frame, text=HOTKEYS, font=('', 10), anchor='w', justify='left').pack(padx=6, pady=6)
        self.book.add(frame, text='ショートカットキー一覧')
        return self


class TkWithMenu(tk.Tk):

    def __init__(self, *args):
        super().__init__(*args)
        self.make_widgets()
        self.make_menu()

    def make_widgets(self):
        self.frame_ctrl = CtrlFrame(self)
        self.frame_show = ShowFrame(self)

        self.frame_ctrl.grid(row=0, column=0, padx=6, pady=0, sticky='n')
        ttk.Separator(self, orient='vertical').grid(row=0, column=1, sticky='ns')
        self.frame_show.grid(row=0, column=2, padx=6, pady=0)
        return self

    def make_menu(self):
        self.menu_root = tk.Menu(self)

        self.menu_file = tk.Menu(self.menu_root, tearoff=0)
        self.menu_file.add_command(label='開く', accelerator='Ctrl+O')
        self.menu_file.add_command(label='上書き保存', accelerator='Ctrl+s')
        self.menu_file.add_command(label='別名で保存', accelerator='Ctrl+Shift+s')
        self.menu_file.add_command(label='.anm出力', accelerator='Ctrl+e')
        self.menu_file.add_separator()
        self.menu_file.add_command(label='終了', accelerator='Ctrl+q')
        for i in range(1, 4):
            self.menu_file.entryconfig(i, state='disabled')

        self.menu_edit = tk.Menu(self.menu_root, tearoff=0)
        self.menu_edit.add_command(label='変換', accelerator='F5')
        self.menu_edit.add_command(label='戻す', accelerator='Ctrl+z')
        self.menu_edit.add_command(label='やり直す', accelerator='Ctrl+y / Ctrl+Shift+z')
        for i in range(3):
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
        self.menu_edit.entryconfig(which+1, state='normal' if state else 'disabled')
        return self


class test(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)
        self.i = 0
        self.frame = tk.Frame(self)
        tk.Label(self.frame, text=str(self.i)).pack(padx=10, pady=10)
        self.create_window(0, 0, window=self.frame)
        self.update_idletasks()
        self.configure(scrollregion=self.bbox('all'))

    def func(self, event=None):
        self.frame.destroy()
        self.i = self.i + 1
        self.frame = tk.Frame(self)
        tk.Label(self.frame, text=str(self.i)).pack(padx=10, pady=10)
        self.create_window(0, 0, window=self.frame)
        self.update_idletasks()

if __name__ == '__main__':
    root = TkWithMenu()
    # root = tk.Tk()
    # root.title('PSDのレイヤー名変換')
    # c = ShowFrame(root)
    # c.pack(padx=10, pady=10)
    root.mainloop()
