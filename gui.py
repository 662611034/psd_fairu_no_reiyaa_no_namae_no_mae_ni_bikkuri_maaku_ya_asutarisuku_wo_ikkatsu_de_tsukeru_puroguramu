import tkinter as tk
import tkinter.ttk as ttk

GUIDE='''
ctrl+o：ファイルを開く

ctrl+s：上書き保存 | ctrl+shift+s：別名で保存

F5：変換

ctrl+z：戻す  |  ctrl+(y/shift+z)：やり直す

ctrl+(1/2)：変換メニュー選択

ctrl+q：終了
'''

class MainFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.frame_L = ttk.Frame(self)
        self.frame_R = ttk.Frame(self)
        self.frame_L.grid(row=0, column=0, sticky='n', padx=5, pady=5)
        self.frame_R.grid(row=0, rowspan=2, column=1, padx=10, pady=10)
        self.make_frame_file().make_frame_mode().make_frame_button()
        self.make_frame_show().make_frame_help()

    def make_frame_file(self):
        self.frame_file = ttk.Frame(self.frame_L)

        self.label_msg = tk.Label(self.frame_file, text='')
        self.button_open = tk.Button(self.frame_file, text='ファイルを開く', width=12)
        self.label_filename = ttk.Label(self.frame_file, text='作業中のファイルはありません')

        self.label_msg.grid(row=0, column=0, columnspan=2, padx=12, pady=5)
        self.button_open.grid(row=1, column=0, padx=12, pady=5)
        self.label_filename.grid(row=1, column=1, padx=12, pady=5)

        self.frame_file.pack(padx=12, pady=12, anchor='w')
        return self

    def make_frame_mode(self):
        self.frame_mode = ttk.Frame(self.frame_L)
        self.subframe_mode = []
        for i in range(3):
            self.subframe_mode.append(ttk.Frame(self.frame_mode))
            self.subframe_mode[i].pack(anchor='w')

        self.var_mode = tk.IntVar()
        self.var_mode.set(0)
        self.radio_mode = []
        self.combo_symbol = []
        for i in range(2):
            self.radio_mode.append(\
                    ttk.Radiobutton(self.subframe_mode[i+1], text='', value=i, variable=self.var_mode))
            self.radio_mode[i].grid(row=0, column=0, padx=6, pady=6)

        # subframe[0]
        column = 0
        self.combo_depth = ttk.Combobox(self.subframe_mode[0], state='readonly', width=2)
        self.combo_depth.grid(row=0, column=column, pady=5)

        column += 1
        ttk.Label(self.subframe_mode[0], text='層にある、').grid(row=0, column=column, pady=5)

        column += 1
        self.entry_word = tk.Entry(self.subframe_mode[0], width=12)
        self.entry_word.grid(row=0, column=column, pady=5)

        column += 1
        self.combo_match = ttk.Combobox(self.subframe_mode[0], values=['を含む', 'と一致する'], state='readonly', width=10)
        self.combo_match.grid(row=0, column=column, pady=5)

        column += 1
        tk.Label(self.subframe_mode[0], text='名前の').grid(row=0, column=column, pady=5)
        column += 1

        self.combo_class = ttk.Combobox(\
                self.subframe_mode[0], values=['物', 'レイヤー', 'グループ', 'グループの直下の物'], state='readonly', width=18)
        self.combo_class.grid(row=0, column=column, pady=5)
        column += 1

        ttk.Label(self.subframe_mode[0], text='全て').grid(row=0, column=column, pady=5)

        # subframe[1]
        label_tmp = ttk.Label(self.subframe_mode[1], text='に')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(0))
        label_tmp.grid(row=0, column=1, pady=5)
        self.combo_symbol = ttk.Combobox(self.subframe_mode[1], values=['!', '*'], state='readonly', width=2)
        self.combo_symbol.bind('<Button-1>', lambda x: self.var_mode.set(0))
        self.combo_symbol.grid(row=0, column=2, padx=6, pady=6)
        label_tmp = ttk.Label(self.subframe_mode[1], text='をつける')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(0))
        label_tmp.grid(row=0, column=3, pady=5)
        
        # subframe[2]
        label_tmp = ttk.Label(self.subframe_mode[2], text='から「!」と「*」を消す')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(1))
        label_tmp.grid(row=0, column=1, pady=5)
        
        self.combo_match.current(0)
        self.combo_class.current(0)
        self.combo_symbol.current(0)

        self.frame_mode.pack(pady=6)
        return self

    def make_frame_button(self):
        self.frame_button = ttk.Frame(self.frame_L)
        self.subframe_button = []
        for i in range(2):
            self.subframe_button.append(ttk.Frame(self.frame_button))
            self.subframe_button[i].grid(row=i, column=0)

        text_tmp = 'なかったことにする'
        self.button_undo = tk.Button(self.subframe_button[0], state='disabled', text=text_tmp)
        text_tmp = 'なかったことにしたことをなかったことにする'
        self.button_redo = tk.Button(self.subframe_button[0], state='disabled', text=text_tmp)

        self.button_convert = tk.Button(self.subframe_button[1], text='変換', width=12)
        self.button_save_same = tk.Button(self.subframe_button[1], text='上書き保存', width=12)
        self.button_save_diff = tk.Button(self.subframe_button[1], text='別名で保存', width=12)

        self.button_undo.grid(row=0, column=0, padx=16, pady=5)
        self.button_redo.grid(row=0, column=1, padx=16, pady=5)

        self.button_convert.grid(row=0, column=0, padx=16, pady=5)
        self.button_save_same.grid(row=0, column=1, padx=16, pady=5)
        self.button_save_diff.grid(row=0, column=2, padx=16, pady=5)

        self.frame_button.pack(pady=6)
        return self

    def make_frame_show(self):
        self.frame_show = ttk.Frame(self.frame_R)

        self.text_layerview = tk.Text(self.frame_show, width=48, height=40, state='disabled')
        self.scroll_layerview_y = ttk.Scrollbar(\
                self.frame_show, orient = 'vertical', command = self.text_layerview.yview)
        self.text_layerview.config(yscrollcommand = self.scroll_layerview_y.set)
        self.scroll_layerview_x = ttk.Scrollbar(\
                self.frame_show, orient = 'horizontal', command = self.text_layerview.xview)
        self.text_layerview.config(xscrollcommand = self.scroll_layerview_x.set)

        self.text_layerview.grid(row=0, column=0, padx=0, pady=0)
        self.scroll_layerview_y.grid(row=0, column=1, padx=0, pady=0, sticky='ns')
        self.scroll_layerview_x.grid(row=1, column=0, padx=0, pady=0, sticky='ew')

        self.frame_show.pack()
        return self

    def make_frame_help(self):
        self.frame_help = ttk.Frame(self.frame_L)
        ttk.Label(self.frame_help, text=GUIDE, anchor='w', font=("", 10)).grid(row=0, column=0)
        self.button_help = tk.Button(\
                self.frame_help, text='F1：ウェブブラウザで配布ページを開く', width=36, anchor='w')
        self.button_help.grid(row=1, column=0)
        self.frame_help.pack(padx=0, pady=0)

    def unlock_text(self, con):
        self.text_layerview.config(state = 'normal' if con else 'disabled')
        return self

    def clear_text(self):
        self.unlock_text(True)
        self.text_layerview.delete("1.0", "end")
        self.unlock_text(False)
        return self

    def rewrite_text(self, content):
        self.unlock_text(True)
        self.text_layerview.delete('1.0', 'end')
        self.text_layerview.insert('end', content)
        self.unlock_text(False)
        return self

    def add_text(self, content):
        self.unlock_text(True)
        self.text_layerview.insert('end', content)
        self.unlock_text(False)
        return self

    def get_mode(self):
        # return 0 or 1 in int
        return self.var_mode.get()

    def get_condition(self):
        c_depth = self.combo_depth.current()  # c0 = depth
        c_words = self.entry_word.get()
        c_match = self.combo_match.current()  # 0: include, 1: same
        c_class = self.combo_class.current()  # 0: both, 1: layer, 2: group, 3: things under the layer
        return c_depth, c_words, c_match, c_class  # int, str, int, int

    def get_symbol(self):
        return self.combo_symbol.get()

    def unre_state(self, which, state):
        b = [self.button_undo, self.button_redo]
        b[which].config(state='normal' if state else 'disabled')
        return self


class TkWithMenu(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.make_menu()

    def make_menu(self):
        self.menu_root = tk.Menu(self)

        self.menu_file = tk.Menu(self.menu_root, tearoff=0)
        self.menu_file.add_command(label='開く', accelerator='Ctrl+O')
        self.menu_file.add_command(label='上書き保存', accelerator='Ctrl+s')
        self.menu_file.add_command(label='別名で保存', accelerator='Ctrl+Shift+s')
        self.menu_file.add_separator()
        self.menu_file.add_command(label='終了', accelerator='Ctrl+q')

        self.menu_edit = tk.Menu(self.menu_root, tearoff=0)
        self.menu_edit.add_command(label='変換', accelerator='F5')
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='戻す', accelerator='Ctrl+z')
        self.menu_edit.add_command(label='やり直す', accelerator='Ctrl+y / Ctrl+Shift+z')

        self.menu_help= tk.Menu(self.menu_root, tearoff=0)
        self.menu_help.add_command(label='githubページを開く', accelerator='F1')

        self.menu_root.add_cascade(label='ファイル', menu=self.menu_file)
        self.menu_root.add_cascade(label='編集', menu=self.menu_edit)
        self.menu_root.add_cascade(label='ヘルプ', menu=self.menu_help)

        self.config(menu=self.menu_root)
        return self

if __name__ == '__main__':
    root = TkWithMenu()
    root.title('PSDのレイヤー名変換')
    x = MainFrame(root)
    x.pack()
    x.combo_depth.config(values = list(range(5)))
    x.button_save_same.config(command=lambda :print(type(x.get_condition()[0]), flush=True))
    root.mainloop()
