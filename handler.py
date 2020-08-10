from psd_tools import PSDImage
import tkinter as tk
import tkinter.ttk as ttk

class PSDHandler():

    def __init__(self, ifile_path):
        self.psd = PSDImage.open(ifile_path)
        self.depth_max = self.find_depth_max()

    def find_depth_max(self):
        depth_max = 0
        for _, depth in self.layer_list():
            if depth > depth_max:
                depth_max = depth
        return depth_max

    def save(self, ofile_path):
        self.psd.save(ofile_path)
        return self

    def layer_list(self, layer=None, depth=1):
        if layer is None:
            layer = self.psd
        for sublayer in layer:
            yield sublayer, depth
            if sublayer.is_group():
                for subdata in self.layer_list(sublayer, depth+1):
                    yield subdata

    def export_layers(self):
        content = ''
        for layer, depth in self.layer_list():
            content += str(depth) + ' ' * 2 * depth
            if depth > 1:
                content += '|-  '
            content += '[' + layer.name + ']\n'
        return content

    def add_symbol(self, symbol, depth_target, exceptlist=['!', '*']):
        for layer, depth in self.layer_list():
            if depth == depth_target and (not layer.name[0] in exceptlist):
                layer.name = symbol + layer.name
        return self

    def erase_symbol_all(self):
        for layer, _ in self.layer_list():
            name_new = layer.name
            while name_new[0:1] in ('!', '*'):
                name_new = name_new[1:]
            layer.name = name_new
        return self

    def layer_fullpath(self, layer, path=''):
        fullpath = layer.name + path
        if layer._parent is self.psd:
            return fullpath
        else:
            return self.layer_fullpath(layer._parent, '/' + fullpath)


class LayerCL(ttk.Frame):
    def __init__(self, master, hanlder, width=240, height=720):
        super().__init__(master)

        self.handler = handler
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.frame_widgets = ttk.Frame(self.canvas)

        self.dict_widgets = {}
        self.make_widgets()

        self.make_canvas()

    def make_canvas(self):
        self.scroll_x = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.create_window(0, 0, window=self.frame_widgets)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.yview_moveto('0.0')
        self.canvas.grid(row=0, column=0)
        self.scroll_x.grid(row=1, column=0, sticky='ew')
        self.scroll_y.grid(row=0, column=1, sticky='ns')

        self.scroll_x.bind_all('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(-1*event.delta//120, 'units'))
        self.scroll_y.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-1*event.delta//120, 'units'))

    def make_widgets(self):
        ttk.Label(self.frame_widgets, text='層  レイヤー名', anchor='w').pack(anchor='w')
        for layer, depth in self.handler.layer_list():
            frame_tmp = ttk.Frame(self.frame_widgets)
            ttk.Label(frame_tmp, text=str(depth) + ' ' * 4 * depth + '|-').grid(row=0, column=0)
            bool_tmp = tk.BooleanVar()
            bool_tmp.set(False)
            check_tmp = tk.Checkbutton(frame_tmp, variable=bool_tmp)
            check_tmp.grid(row=0, column=1)
            check_tmp.bind('<Button-1>', self.make_fclicked(layer))
            entry_tmp = tk.Entry(frame_tmp, width=12)
            entry_tmp.insert(0, layer.name)
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

if __name__ == '__main__':
    ifile = r'./sample.psd'
    ifile = r'C:\Users\user\Pictures\sample.psd'
    handler = PSDHandler(ifile)
    root = tk.Tk()
    # tk.Button(root, text='jaks', command = lambda : LayerCL(root, handler).pack()).pack()
    LayerCL(root, handler).pack(padx=10, pady=10)
    root.mainloop()
