import tkinter as tk
import tkinter.ttk as ttk

GUIDE='''
ctrl+o：ファイルを開く

ctrl+s：上書き保存

ctrl+shift+s：別名で保存

F5：変換

ctrl+1/2/3/4：変換メニュー選択

F1：配布ページに移動（ウェブブラウザが開きます）
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

        self.var_mode = tk.IntVar()
        self.var_mode.set(0)
        self.subframe_mode = []
        self.radio_mode = []
        for i in range(4):
            self.subframe_mode.append(ttk.Frame(self.frame_mode))
            self.radio_mode.append(\
                    ttk.Radiobutton(self.subframe_mode[i], text='', value=i, variable=self.var_mode))
            self.radio_mode[i].grid(row=0, column=0, padx=5, pady=12)
            self.subframe_mode[i].bind('<Button-1>', lambda x, i=i: self.var_mode.set(i))
            self.subframe_mode[i].pack(anchor='w')

        # subframe 0
        column = 1
        self.combo_depth = ttk.Combobox(self.subframe_mode[0], state='readonly', width=2)
        self.combo_depth.bind('<Button-1>', lambda x : self.var_mode.set(0))
        self.combo_depth.grid(row=0, column=column, pady=5)
        column += 1
        label_tmp = ttk.Label(self.subframe_mode[0], text='層にある、')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(0))
        label_tmp.grid(row=0, column=column, pady=5)
        column += 1
        self.entry_word = tk.Entry(self.subframe_mode[0], width=12)
        self.entry_word.bind('<Button-1>', lambda x : self.var_mode.set(0))
        self.entry_word.grid(row=0, column=column, pady=5)
        column += 1
        self.combo_match = ttk.Combobox(self.subframe_mode[0], values=['を含む', 'と一致する'], state='readonly', width=8)
        self.combo_match.bind('<Button-1>', lambda x : self.var_mode.set(0))
        self.combo_match.grid(row=0, column=column, pady=5)
        column += 1
        label_tmp = ttk.Label(self.subframe_mode[0], text='名前の')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(0))
        label_tmp.grid(row=0, column=column, pady=5)
        column += 1
        self.combo_class = ttk.Combobox(\
                self.subframe_mode[0], values=['物', 'レイヤー', 'グループ', 'グループの直下の物'], state='readonly', width=18)
        self.combo_class.bind('<Button-1>', lambda x : self.var_mode.set(0))
        self.combo_class.grid(row=0, column=column, pady=5)
        column += 1
        label_tmp = ttk.Label(self.subframe_mode[0], text='全てに')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(0))
        label_tmp.grid(row=0, column=column, pady=5)
        column += 1
        self.combo_symbol = ttk.Combobox(self.subframe_mode[0], values=['!', '*'], state='readonly', width=2)
        self.combo_symbol.bind('<Button-1>', lambda x : self.var_mode.set(0))
        self.combo_symbol.grid(row=0, column=column, pady=5)
        column += 1
        label_tmp = ttk.Label(self.subframe_mode[0], text='をつける')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(0))
        label_tmp.grid(row=0, column=column, pady=5)
        
        self.combo_match.current(0)
        self.combo_class.current(0)
        self.combo_symbol.current(0)

        # subframe 1
        label_tmp = ttk.Label(self.subframe_mode[1], text='最上位階層の全ての物に「!」をつける')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(1))
        label_tmp.grid(row=0, column=1)

        # subframe 1
        label_tmp = ttk.Label(self.subframe_mode[2], text='階層2の全ての物に「*」をつける')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(2))
        label_tmp.grid(row=0, column=1)

        # subframe 3
        label_tmp = ttk.Label(self.subframe_mode[3], text='頭の「！」と「＊」を全て消す')
        label_tmp.bind('<Button-1>', lambda x : self.var_mode.set(3))
        label_tmp.grid(row=0, column=1)

        self.frame_mode.pack()
        return self

    def make_frame_button(self):
        self.frame_button = ttk.Frame(self.frame_L)

        self.button_convert = tk.Button(self.frame_button, text='変換', width=12)
        self.button_save_same = tk.Button(self.frame_button, text='上書き保存', width=12)
        self.button_save_diff = tk.Button(self.frame_button, text='別名で保存', width=12)

        self.button_convert.grid(row=0, column=0, padx=16, pady=5)
        self.button_save_same.grid(row=0, column=1, padx=16, pady=5)
        self.button_save_diff.grid(row=0, column=2, padx=16, pady=5)

        self.frame_button.pack()
        return self

    def make_frame_show(self):
        self.frame_show = ttk.Frame(self.frame_R)

        self.text_layerview = tk.Text(self.frame_show, width=48, height=40, state='disabled')
        self.scroll_layerview_v = ttk.Scrollbar(\
                self.frame_show, orient = 'vertical', command = self.text_layerview.yview)
        self.text_layerview.config(yscrollcommand = self.scroll_layerview_v.set)
        self.scroll_layerview_h = ttk.Scrollbar(\
                self.frame_show, orient = 'horizontal', command = self.text_layerview.xview)
        self.text_layerview.config(xscrollcommand = self.scroll_layerview_h.set)

        self.text_layerview.grid(row=0, column=0, padx=0, pady=0)
        self.scroll_layerview_v.grid(row=0, column=1, padx=0, pady=0, sticky='ns')
        self.scroll_layerview_h.grid(row=1, column=0, padx=0, pady=0, sticky='ew')

        self.frame_show.pack()
        return self

    def make_frame_help(self):
        self.frame_help = ttk.Frame(self.frame_L)
        ttk.Label(self.frame_help, text=GUIDE, anchor='w', font=("", 10)).grid(row=0, column=0)
        self.button_help = tk.Button(self.frame_help, text='ウェブブラウザで配布ページを開く', width=36)
        self.button_help.grid(row=1, column=0)
        self.frame_help.pack(padx=12, pady=12)

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
        # return 1~4 in int
        return self.var_mode.get()

    def get_condition(self):
        c_depth = self.combo_depth.current()  # c0 = depth
        c_words = self.entry_word.get()
        c_match = self.combo_match.current()  # 0: include, 1: same
        c_class = self.combo_class.current()  # 0: both, 1: layer, 2: group, 3: things under the layer
        return c_depth, c_words, c_match, c_class  # int, str, int, int

    def get_symbol(self):
        return self.combo_symbol.get()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('PSDのレイヤー名変換')
    x = MainFrame(root)
    x.pack()
    x.combo_depth.config(values = list(range(5)))
    x.button_save_same.config(command=lambda :print(type(x.get_condition()[0]), flush=True))
    root.mainloop()
