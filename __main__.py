import webbrowser
import copy
import gui
import handler
import tkinter.filedialog as fd
import tkinter.messagebox as mb

tk = gui.tk
URL = 'https://github.com/662611034/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu'
LOG_LENGTH = 32

def callback(func):
    def f_decorated(self, event=None):
        try:
            return func(self, event=event)
        except Exception as e:
            mb.showerror('エラーが発生しました', str(e))
    return f_decorated

class Top(gui.MainFrame):

    def __init__(self, master=None):
        super().__init__(master)
        self.handler = None
        self.bind_funcs()
        master.bind_all('<Control-q>', lambda event: master.quit())
        self.log_fore = []
        self.log_back = []
        self.logs = [self.log_back, self.log_fore]

    def bind_funcs(self):
        self.button_open.config(command = self.open)
        self.button_save_same.config(command = self.save_same)
        self.button_save_diff.config(command = self.save_diff)
        self.button_undo.config(command = self.undo)
        self.button_redo.config(command = self.redo)
        self.button_help.config(command = self.open_help)
        self.button_convert.config(command = self.convert)

        self.bind_all('<Control-o>', self.open)
        self.bind_all('<Control-s>', self.save_same)
        self.bind_all('<Control-S>', self.save_diff)
        self.bind_all('<Control-z>', self.undo)
        self.bind_all('<Control-Z>', self.redo)
        self.bind_all('<Control-y>', self.redo)
        self.bind_all('<Key-F1>', self.open_help)
        self.bind_all('<Key-F5>', self.convert)
        for i in range(1, 5):
            self.bind_all(f'<Control-Key-{i}>', self.select_mode)

        return self

    @callback
    def open(self, event):
        self.ifile_path = fd.askopenfilename(filetypes=[('psd files', '*.psd')])
        if not self.ifile_path:
            return 'break'
        if self.ifile_path[-4:] != '.psd':
            raise Exception('.psdファイルではありません')

        self.handler = handler.PSDHandler(self.ifile_path)

        self.combo_depth.config(values=list(range(self.handler.depth_max+1)))
        self.combo_depth.current(0)

        self.log_fore = []
        self.log_back = []

        self.label_msg.config(text='ファイルを開きました')
        self.label_filename.config(text=self.ifile_path)
        self.show_layer()

        return self

    @callback
    def save_same(self, event):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.handler.save(self.ifile_path)
        self.label_msg.config(text='保存されました')
        return self

    @callback
    def save_diff(self, event):
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

        return self

    @callback
    def undo(self, event):
        self.stack_at(self.log_fore)
        self.pop_from(self.log_back)
        self.unre_state(1, 1)  # enable redo button
        if len(self.log_back) == 0:
            self.unre_state(0, 0)
        self.show_layer()
        return self

    @callback
    def redo(self, event):
        self.stack_at(self.log_back)
        self.pop_from(self.log_fore)
        self.unre_state(0, 1)  # enable redo button
        if len(self.log_fore) == 0:
            self.unre_state(1, 0)
        self.show_layer()
        return self

    @callback
    def convert(self, event):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.stack_at(self.log_back)
        self.log_fore = []
        self.unre_state(0, 1).unre_state(1, 0)

        # self.convert_funcs[self.get_mode()]()
        mode = self.get_mode()
        if mode == 0:
            self.add_symbol()
        elif mode == 1:
            self.handler.add_bikkuri_1st()
        elif mode == 2:
            self.handler.add_star_2nd()
        elif mode == 3:
            self.handler.erase_symbol_all()

        self.show_layer()
        return self

    @callback
    def select_mode(self, event):
        self.var_mode.set(int(event.keysym) - 1)
        return self

    @callback
    def open_help(self, event):
        webbrowser.open(URL)
        return self

# from here, funcs need for conversion
    def add_symbol(self):
        for layer, parent, depth in self.handler.layer_list():
            if self.make_condition(layer, parent, depth):
                layer.name = self.get_symbol() + layer.name
        return self

    def make_condition(self, layer, parent, depth):
        c_depth, c_words, c_match, c_class = self.get_condition()
        condition = True

        select_target = parent if c_class == 3 else layer
        c_depth_target = c_depth + (1 if c_class == 3 else 0)

        if c_depth > 0:
            condition = condition and (c_depth_target == depth)

        if c_match == 0:
            condition = condition and (c_words in select_target.name)
        elif c_match == 1:
            condition = condition and (c_words == select_target.name)

        if c_class == 1:
            condition = condition and (not layer.is_group())
        elif c_class == 2:
            condition = condition and (layer.is_group())

        return condition and (not layer.name[0] in ['!', '*'])

    def stack_at(self, log):
        log.append(copy.deepcopy(self.handler))
        if len(log) > LOG_LENGTH:
            log.pop(0)
        return self

    def pop_from(self, log):
        if log:
            self.handler = log.pop()
        return self

    def show_layer(self):
        self.rewrite_text('層  レイヤー名\n\n'+self.handler.export_layers())
        return self


root = tk.Tk()
root.title('.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラム')
Top(root).pack()
root.mainloop()
