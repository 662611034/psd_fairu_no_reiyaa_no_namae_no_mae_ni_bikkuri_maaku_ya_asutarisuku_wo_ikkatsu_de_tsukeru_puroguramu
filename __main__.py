import webbrowser
import gui
import handler
import tkinter.filedialog as fd
import tkinter.messagebox as mb

tk = gui.tk
URL = "https://github.com/662611034/kigo_tsukeru"

class Top(gui.MainFrame):

    def __init__(self, master=None):
        super().__init__(master)
        self.handler = None
        self.bind_funcs()

    def bind_funcs(self):
        self.button_open.config(command = self.open)
        self.button_convert.config(command = self.convert)
        self.button_save_same.config(command = self.save_same)
        self.button_save_diff.config(command = self.save_diff)
        self.button_help.config(command = lambda : webbrowser.open(URL))

        self.bind_all('<Control-o>', self.open)
        self.bind_all('<Key-F5>', self.convert)
        self.bind_all('<Control-s>', self.save_same)
        self.bind_all('<Control-S>', self.save_diff)
        self.bind_all('<Key-F1>', lambda x :webbrowser.open(URL))
        for i in range(1, 5):
            self.bind_all(f'<Control-Key-{i}>', self.select_mode)
        return self

    def open(self, event=None):
        self.ifile_path = fd.askopenfilename(filetypes=[('psd files', '*.psd')])
        if not self.ifile_path:
            return 'break'
        if self.ifile_path[-4:] != '.psd':
            mb.showerror('ファイル形式エラー', 'PSDファイルではありません')
            return 'break'

        self.handler = handler.PSDHandler(self.ifile_path)
        self.def_convert_funcs()

        self.combo_depth.config(values=list(range(self.handler.depth_max+1)))
        self.combo_depth.current(0)

        self.label_msg.config(text='ファイルを開きました')
        self.label_filename.config(text=self.ifile_path)
        self.rewrite_text('層  レイヤー名\n\n'+self.handler.export_layers())

        return 'break'

    def save_same(self, event=None):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.handler.save(self.ifile_path)
        self.label_msg.config(text='保存されました')
        return 'break'

    def save_diff(self, event=None):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        ofile_path = fd.asksaveasfilename(filetypes=[('psd files', '*.psd')])

        if not ofile_path:
            return 'break'
        if ofile_path[-4:] != '.psd':
            ofile_path += '.psd'

        self.handler.save(ofile_path)

        self.ifile_path = ofile_path
        self.label_msg.config(text='別名で保存されました')
        self.label_filename.config(text=self.ifile_path)

        return 'break'

    def convert(self, event=None):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.convert_funcs[self.get_mode()]()

        self.rewrite_text('層  レイヤー名\n\n'+self.handler.export_layers())
        return 'break'

    def select_mode(self, event=None):
        self.var_mode.set(int(event.keysym) - 1)
        return 'break'

# from here, funcs need for conversion
    def def_convert_funcs(self):
        self.convert_funcs = []
        self.convert_funcs.append(self.add_symbol)
        self.convert_funcs.append(self.handler.add_bikkuri_1st)
        self.convert_funcs.append(self.handler.add_star_2nd)
        self.convert_funcs.append(self.handler.erase_symbol_all)
        return self

    def add_symbol(self):
        for layer, parent, depth in self.handler.layer_list():
            if self.make_condition(layer, parent, depth):
                layer.name = self.get_symbol() + layer.name
        return self

    def make_condition(self, layer, parent, depth):
        c_depth, c_words, c_match, c_class = self.get_condition()
        condition = True

        if c_class == 3:  # under the layer
            if c_depth > 0:
                condition = condition and ((c_depth+1) == depth)

            if c_match == 0:
                condition = condition and (c_words in parent.name)
            elif c_match == 1:
                condition = condition and (c_words == parent.name)
        else:
            if c_depth > 0:
                condition = condition and (c_depth == depth)

            if c_match == 0:
                condition = condition and (c_words in layer.name)
            elif c_match == 1:
                condition = condition and (c_words == layer.name)

            if c_class == 1:
                condition = condition and (not layer.is_group())
            elif c_class == 2:
                condition = condition and (layer.is_group())

        return condition and (not layer.name[0] in ['!', '*'])


root = tk.Tk()
root.title('.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラム')
Top(root).pack()
root.mainloop()
