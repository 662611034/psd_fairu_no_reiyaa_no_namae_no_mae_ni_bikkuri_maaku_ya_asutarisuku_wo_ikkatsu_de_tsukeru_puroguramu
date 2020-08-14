# import traceback
import webbrowser
import os
import copy
import gui
import psd_subtool
import tkinter.filedialog as fd
import tkinter.messagebox as mb

URL = 'https://github.com/662611034/psd_fairu_no_reiyaa_no_namae_no_mae_ni_bikkuri_maaku_ya_asutarisuku_wo_ikkatsu_de_tsukeru_puroguramu'


class Logger():
    def __init__(self, length=128):
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


class AppTop(gui.RootWindow):

    def __init__(self,*args):
        super().__init__(*args)

        self.psd = None
        self.logger = Logger()
        self.dict_names = {}

        self.bind_funcs()

    def bind_funcs(self):
        f_open = self.make_callback(self.open_file)
        f_save = [self.make_callback(self.save_file, i) for i in range(2)]
        f_expo = [self.make_callback(self.export_script, i) for i in range(2)]

        f_conv = [self.make_callback(self.convert, i) for i in range(3)]
        f_unre = [self.make_callback(self.undoredo, i) for i in range(2)]

        f_clea = [self.make_callback(self.deal_anmlayer, i+1) for i in range(2)]  # clear 1 or all

        f_sela = [self.make_callback(self.select_all, i) for i in range(2)]  # select all

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

        self.menu_help.entryconfig(0, command=gui.HelpWindow)
        self.menu_help.entryconfig(1, command=lambda : webbrowser.open(URL))

        for i in range(3):
            self.button_converts[i].config(command=f_conv[i])
        for i in range(2):
            self.button_clears[i].config(command=f_clea[i])
        for i in range(2):
            self.button_exports[i].config(command=f_expo[i])

        self.bind_all('<Control-o>', f_open)
        self.bind_all('<Control-s>', f_save[0])
        self.bind_all('<Control-S>', f_save[1])
        self.bind_all('<Control-e>', f_expo[0])
        self.bind_all('<Control-E>', f_expo[1])
        self.bind_all('<Key-F5>', f_conv[0])
        self.bind_all('<Key-F6>', f_conv[1])
        self.bind_all('<Key-F7>', f_conv[2])
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
        def f_callback(event=None):
            try:
                func(event, *mode)
                return 'break'
            except Exception as e:
                mb.showerror('エラーが発生しました', str(e))
                # mb.showerror('エラーが発生しました', str(traceback.format_exc()))

        return f_callback

    def open_file(self, event):
        ifile_path = fd.askopenfilename(filetypes=[('psd files', '*.psd')])
        if not ifile_path:
            return 'break'
        if ifile_path[-4:] != '.psd':
            raise Exception('.psdファイルではありません')
        
        self.open_subfunc(ifile_path)
        self.unre_state(0, 0).unre_state(1, 0)

        self.show_filename(self.ifile_path)
        self.show_msg('ファイルを開きました')

        return self

    def save_file(self, event, mode):
        # 0: 上書き, 1: 別名
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
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

        self.save_subfunc(ofile_path, encoding)

        self.show_filename(self.ifile_path)
        self.show_msg(msg)
        return self

    def export_script(self, event, mode):
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        if mode == 0:
            efile_path = self.ifile_path[:-4] + self.get_anmtail() + '.anm'
        elif mode == 1:
            efile_path = fd.asksaveasfilename(filetypes=[('anm files', '*.anm')])
            if not efile_path:
                return 'break'
            if efile_path[-4:] != '.anm':
                efile_path += '.anm'

        self.export_subfunc(efile_path)
        self.show_msg('.anmファイルを出力しました')

        return self

    def undoredo(self, event, mode):
        # 0: undo, 1: redo
        if self.logger.is_empty(mode):
            return 'break'

        self.cache_names()
        self.logger.stack_at(self.dict_names, 1-mode)

        self.dict_names = self.logger.pop_from(mode)
        self.refresh_names()
        
        self.unre_state(1-mode, 1)  # enable redo button

        if self.logger.is_empty(mode):
            self.unre_state(mode, 0)
        return self

    def convert(self, event, mode):
        # action 0: 「!」をつける, 1: 「*」をつける, 2: 消す
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        self.cache_names()
        self.logger.stack_at(self.dict_names, 0)
        self.logger.reset(1)

        for layer, depth in self.psd.all_layers():
            if self.make_condition(layer, depth, self.selected_tab()):
                self.convert_subfunc(layer, mode)

        self.unre_state(0, 1).unre_state(1, 0)
        return self

    def mode_select(self, event):
        index = int(event.keysym) - 1
        self.select_tab(index)
        return self

    def deal_anmlayer(self, event, mode, layer=None):
        # 0: stack, 1: pop, 2: clear
        if mode == 0:
            self.stack_anmlayers(layer)
        elif mode == 1:
            self.pop_anmlayers()
        elif mode == 2:
            self.clear_anmlayers()
        return self

    def select_all(self, event, mode):
        if not self.psd:
            mb.showwarning('ファイルがありません', 'まずはファイルを開いてください')
            return 'break'

        for layer, _ in self.psd.all_layers():
            self.frame_show.dict_widgets[id(layer)]['selected'].set(bool(mode))
        return self

# to here, callback funcs

# from here, funcs need for open
    def open_subfunc(self, ifile_path):
        self.ifile_path = ifile_path
        self.psd = psd_subtool.PSDImageExt.open(self.ifile_path, self.get_encode())

        self.remake_frame_show()

        self.set_combo_depth(list(range(self.psd.depth_max+1)))

        self.dict_names = {}
        for layer, _ in self.psd.all_layers():
            self.dict_names[id(layer)] = layer.name

        self.logger.reset(0).reset(1)

        for i in [1, 2, 4, 5]:
            self.menu_file.entryconfig(i, state='normal')
        for i in [0, 1, 2, 4, 5]:
            self.menu_edit.entryconfig(i, state='normal')

        return self

    def remake_frame_show(self):
        self.frame_show.remake_canvas(self.psd)

        self.frame_show.dict_widgets[id(self.psd)]['check'].bind('<Button-1>', self.make_fcheck(self.psd))

        for layer, _ in self.psd.all_layers():
            if layer.is_group():
                dict_tmp = self.frame_show.dict_widgets[id(layer)]
                dict_tmp['button'].config(command=self.make_callback(self.deal_anmlayer, 0, layer))
                dict_tmp['label'].bind('<Button-1>', self.make_ffold(layer))
                dict_tmp['check'].bind('<Button-1>', self.make_fcheck(layer))

        return self

    # make functions to bind at widgets on frame_show
    def make_ffold(self, layer):

        def ffold(event=None):
            try:
                dict_target = self.frame_show.dict_widgets[id(layer)]
                flag = dict_target['folded'].get()
                if flag:
                    dict_target['subframe'].pack()
                else:
                    dict_target['subframe'].pack_forget()
                dict_target['folded'].set(not flag)
                return 'break'

            except Exception as e:
                mb.showerror('エラーが発生しました', str(e))

        return ffold

    def make_fcheck(self, layer):
        # event.state: click-8, shift click-9, ctrl shict click=13
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
        for layer, _ in self.psd.all_layers():
            layer.name = self.frame_show.dict_widgets[id(layer)]['entry'].get()

        self.psd.save(ofile_path, encoding)
        self.ifile_path = ofile_path
        self.psd.encoding = encoding
        return self

    def export_subfunc(self, efile_path):
        anmlayers = self.get_anmlayers()

        tracklines, valuelines = '', ''
        for tracknum, layer in enumerate(anmlayers):
            trackline, valueline = self.psd.export_anmscript(layer, tracknum)
            tracklines += trackline
            valuelines += '\n' + valueline

        with open(efile_path, mode='w', encoding='sjis') as fout:  # or cp932
            fout.write(tracklines)
            fout.write(valuelines)

        return self

# from here, funcs need for conversion
    def convert_subfunc(self, layer, mode):
        entry_target = self.frame_show.dict_widgets[id(layer)]['entry']
        entry_target.config(state='normal')
        symbols = self.psd.HEADSYMBOLS  # ('!', '*')

        if mode in [0, 1] and not (entry_target.get()[0] in symbols):
            entry_target.insert(0, symbols[mode])
        elif mode == 2:
            while entry_target.get()[0:1] in symbols:
                entry_target.delete(0, 1)
        entry_target.config(state='readonly')
        return self

    def make_condition(self, layer, depth, mode):
        # 0: チェックを入れたレイヤー, 1: 条件指定

        if mode == 0:
            return self.frame_show.dict_widgets[id(layer)]['selected'].get()

        elif mode == 1:
            c_depth, c_words, c_match, c_class = self.get_condition()
            condition = True

            id_layer = id(layer._parent if c_class == 3 else layer)
            entry_target = self.frame_show.dict_widgets[id_layer]['entry']
            c_depth_target = c_depth + (1 if c_class == 3 else 0)

            if c_depth > 0:
                condition = condition and (c_depth_target == depth)

            if c_match == 0:
                condition = condition and (c_words in entry_target.get())
            elif c_match == 1:
                condition = condition and (c_words == entry_target.get())

            if c_class == 1:
                condition = condition and (not layer.is_group())
            elif c_class == 2:
                condition = condition and (layer.is_group())

            return condition
# to here, funcs need for conversion

    def cache_names(self):
        for layer, _ in self.psd.all_layers():
            self.dict_names[id(layer)] = self.frame_show.dict_widgets[id(layer)]['entry'].get()
        return self

    def refresh_names(self):
        for layer, _ in self.psd.all_layers():
            entry_target = self.frame_show.dict_widgets[id(layer)]['entry']
            entry_target.config(state='normal')
            entry_target.delete(0, 'end')
            entry_target.insert(0, self.dict_names[id(layer)])
            entry_target.config(state='readonly')
        return self


root = AppTop()
ifile_path = './sample.psd'
# ifile_path = r'C:\Users\user\Pictures\sample.psd'
# root.open_subfunc(ifile_path)
root.mainloop()
