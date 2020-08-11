import webbrowser
import copy
import gui
import handler
import tkinter.filedialog as fd
import tkinter.messagebox as mb

tk = gui.tk
ttk = gui.ttk
URL = 'https://github.com/662611034/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu'


class Logger():
    def __init__(self, length=65536):
        self.log_length = length
        self.logs = [[], []]  # 0: back, 1: fore

    def stack_at(self, instance, which=0):
        if len(self.logs[which]) > self.log_length-1:
            self.logs[which].pop(0)
        self.logs[which].append(copy.deepcopy(instance))
        return self

    def pop_from(self, which):
        return self.logs[which].pop() if self.logs[which] else None

    def reset(self, which):
        self.logs[which] = []
        return self

    def is_empty(self, which):
        return False if self.logs[which] else True


class AppTop(gui.TkWithMenu):

    def __init__(self,*args):
        super().__init__(*args)
        self.handler = None
        self.logger = Logger()
        self.dict_widgets = {}
        self.dict_names = {}

        self.bind_funcs()
        self.title('.psdファイルのレイヤーの名前の前に「!」や「*」を一括でつけるプログラム')

    def bind_funcs(self):
        self.menu_file.entryconfig(0, command=self.open)
        self.menu_file.entryconfig(1, command=self.save_same)
        self.menu_file.entryconfig(2, command=self.save_diff)
        self.menu_file.entryconfig(3, command=self.export)
        self.menu_file.entryconfig(5, command=self.quit)

        self.menu_edit.entryconfig(0, command=self.convert)
        self.menu_edit.entryconfig(1, command=self.undo)
        self.menu_edit.entryconfig(2, command=self.redo)

        self.menu_help.entryconfig(0, command=self.open_help)
        self.menu_help.entryconfig(1, command=self.open_github)

        self.frame_ctrl.button_convert.config(command=self.convert)
        self.frame_ctrl.button_export.config(command=self.export)

        self.bind_all('<Control-o>', self.open)
        self.bind_all('<Control-s>', self.save_same)
        self.bind_all('<Control-S>', self.save_diff)
        self.bind_all('<Control-e>', self.export)
        self.bind_all('<Key-F5>', self.convert)
        self.bind_all('<Control-z>', self.undo)
        self.bind_all('<Control-Z>', self.redo)
        self.bind_all('<Control-y>', self.redo)
        self.bind_all('<Key-F1>', self.open_help)
        self.bind_all('<Control-q>', lambda event: self.quit())

        for i in range(1, 5):
            self.bind_all(f'<Control-Key-{i}>', self.mode_select)

        return self

# callback from here
    def callback(func):
        def f_decorated(self, event=None):
            # try:
            if True:
                return func(self, event=event)
            else:
            # except Exception as e:
                mb.showerror('エラーが発生しました', str(e))
        return f_decorated

    @callback
    def open(self, event):
        ifile_path = fd.askopenfilename(filetypes=[('psd files', '*.psd')])
        if not ifile_path:
            return 'break'
        if ifile_path[-4:] != '.psd':
            raise Exception('.psdファイルではありません')
        
        self.open_subfunc(ifile_path)
        return self

    @callback
    def save_same(self, event):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.save_subfunc(self.ifile_path)
        self.frame_ctrl.label_msg.config(text='保存されました')
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

        self.save_subfunc(ofile_path)

        self.ifile_path = ofile_path
        self.frame_ctrl.label_msg.config(text='別名で保存されました')
        self.frame_ctrl.label_filename.config(text=self.ifile_path)

        return self

    @callback
    def export(self, event):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.export_subfunc(self.ifile_path[:-4] + '.anm')
        self.frame_ctrl.label_msg.config(text='.anmファイルを出力しました')
        # webbrowser.open(self.ifile_path[:-4] + '.anm')
        webbrowser.open('C:\\')

        return self

    @callback
    def undo(self, event):
        if self.logger.is_empty(0):
            return 'break'

        self.cache_names()

        self.logger.stack_at(self.dict_names, 1)
        self.dict_names = self.logger.pop_from(0)

        self.refresh_names()
        
        self.unre_state(1, 1)  # enable redo button

        if self.logger.is_empty(0):
            self.unre_state(0, 0)
        return self

    @callback
    def redo(self, event):
        if self.logger.is_empty(1):
            return 'break'

        self.cache_names()

        self.logger.stack_at(self.dict_names, 0)
        self.dict_names = self.logger.pop_from(1)

        self.refresh_names()
        
        self.unre_state(0, 1)  # enable redo button

        if self.logger.is_empty(1):
            self.unre_state(1, 0)

        return self

    @callback
    def convert(self, event):
        if not self.handler:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.cache_names()
        self.logger.stack_at(self.dict_names, 0)
        self.logger.reset(1)

        for layer, depth in self.handler.layer_list():
            if self.make_condition(layer, depth, self.frame_ctrl.get_select()):
                self.convert_subfunc(layer, self.frame_ctrl.get_action())

        self.unre_state(0, 1).unre_state(1, 0)
        return self

    @callback
    def mode_select(self, event):
        num = int(event.keysym)
        if num < 3:
            self.var_select.set(int(event.keysym) - 1)
        else:
            self.var_action.set(int(event.keysym) - 3)
        return self

    @callback
    def open_github(self, event):
        webbrowser.open(URL)
        return self

    @callback
    def open_help(self, event=None):
        gui.HelpWindow()
        return self
# callback to here

    def open_subfunc(self, ifile_path):
        self.ifile_path = ifile_path
        self.handler = handler.PSDHandler(self.ifile_path)

        self.frame_ctrl.combo_depth.config(values=list(range(self.handler.depth_max+1)))
        self.frame_ctrl.combo_depth.current(0)

        self.logger.reset(0).reset(1)

        self.remake_hierarchy_frame()

        self.frame_ctrl.label_msg.config(text='ファイルを開きました')
        self.frame_ctrl.label_filename.config(text=self.ifile_path)

        for i in range(3):
            self.menu_file.entryconfig(i+1, state='normal')
            self.menu_edit.entryconfig(i, state='normal')

        return self

    def save_subfunc(self, ofile_path):
        for layer, _ in self.handler.layer_list():
            layer.name = self.dict_widgets[id(layer)]['entry'].get()

        self.handler.save(ofile_path)
        return self

    def export_subfunc(self, ofile_path):
        tracknum = 0
        tracklines = ''
        valuelines = ''

        for layer, _ in self.handler.layer_list():
            if self.dict_widgets[id(layer)]['bool'].get() and layer.is_group():
                trackline, valueline = self.handler.export_anmscript(layer, tracknum) 
                tracklines += trackline
                valuelines += valueline + '\n'

                if tracknum == 3:
                    break
                else:
                    tracknum += 1

        with open(ofile_path, mode='w', encoding='cp932') as fout:
            fout.write(tracklines + '\n')
            fout.write(valuelines)
        return self

# from here, funcs need for conversion
    def convert_subfunc(self, layer, mode):
        target = self.dict_widgets[id(layer)]['entry']
        target.config(state='normal')
        if mode == 0:
            if not (target.get()[0] in self.handler.EXCEPTLIST):
                target.insert(0, self.frame_ctrl.combo_symbol.get())
        elif mode == 1:
            while target.get()[0:1] in self.handler.EXCEPTLIST:
                target.delete(0, 1)
        target.config(state='readonly')
        return self


    def make_condition(self, layer, depth, mode):
        if mode == 0:
            c_depth, c_words, c_match, c_class = self.frame_ctrl.get_condition()
            condition = True

            select_target = layer._parent if c_class == 3 else layer
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

            return condition

        elif mode == 1:
            return self.dict_widgets[id(layer)]['bool'].get()

    def cache_names(self):
        for layer, _ in self.handler.layer_list():
            self.dict_names[id(layer)] = self.dict_widgets[id(layer)]['entry'].get()
        return self

    def refresh_names(self):
        for layer, _ in self.handler.layer_list():
            target = self.dict_widgets[id(layer)]['entry']
            target.config(state='normal')
            target.delete(0, 'end')
            target.insert(0, self.dict_names[id(layer)])
            target.config(state='readonly')
        return self
# to here, funcs need for conversion

# from here, make hierarchy view
    def remake_hierarchy_frame(self):
        for frame in self.frame_show.remake_frame():
            self.make_hierarchy_widgets(frame)
        return self

    def make_hierarchy_widgets(self, master):
        self.dict_widgets = {}
        self.dict_names = {}

        frame_tmp = ttk.Frame(master)
        ttk.Label(frame_tmp, text='層  ', anchor='w').grid(row=0, column=0)

        bool_tmp = tk.BooleanVar()
        bool_tmp.set(False)
        self.dict_widgets[id(self.handler.psd)] = {'bool': bool_tmp}

        check_tmp = tk.Checkbutton(frame_tmp, variable=bool_tmp)
        check_tmp.grid(row=0, column=1)
        check_tmp.bind('<Button-1>', self.make_func_clicked(self.handler.psd))

        ttk.Label(frame_tmp, text='レイヤー名', anchor='w').grid(row=0, column=2)

        frame_tmp.pack(anchor='w')

        for layer, depth in self.handler.layer_list():
            frame_tmp = ttk.Frame(master)

            ttk.Label(frame_tmp, text=str(depth) + ' ' * 4 * depth + '|-').grid(row=0, column=0)

            bool_tmp = tk.BooleanVar()
            bool_tmp.set(False)

            check_tmp = tk.Checkbutton(frame_tmp, variable=bool_tmp)
            check_tmp.grid(row=0, column=1)
            check_tmp.bind('<Button-1>', self.make_func_clicked(layer))

            entry_tmp = tk.Entry(frame_tmp, width=12)
            entry_tmp.insert(0, layer.name)
            entry_tmp.config(state='readonly')
            entry_tmp.grid(row=0, column=2)

            self.dict_names[id(layer)] = layer.name
            self.dict_widgets[id(layer)] = {'bool': bool_tmp, 'entry': entry_tmp}

            frame_tmp.pack(anchor='w')
        return self

    def make_func_clicked(self, layer):
        def func_clicked(event=None):
            # event.state: click-8, shift click-9, ctrl shict click=13
            bool_got = self.dict_widgets[id(layer)]['bool'].get()
            if event.state == 9 and layer.is_group():
                checkrange = layer
            elif event.state == 13 and layer.is_group():
                checkrange = [sublayer for sublayer, _ in self.handler.layer_list(layer)]
            else:
                checkrange = []
            for sublayer in checkrange:
                self.dict_widgets[id(sublayer)]['bool'].set(not bool_got)
        return func_clicked


root = AppTop()
ifile_path = './sample.psd'
ifile_path = r'C:\Users\user\Pictures\sample.psd'
root.open_subfunc(ifile_path)
root.mainloop()
