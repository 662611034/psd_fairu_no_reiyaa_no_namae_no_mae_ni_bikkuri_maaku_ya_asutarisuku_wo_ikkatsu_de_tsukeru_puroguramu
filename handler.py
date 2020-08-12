from psd_tools import PSDImage
import tkinter as tk
import tkinter.ttk as ttk


class PSDHandler():
    EXCEPTLIST = ('!', '*')

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

    def add_symbol(self, layer, symbol, condition, exceptlist=EXCEPTLIST):
        if condition and (not layer.name[0] in exceptlist):
            layer.name = symbol + layer.name
        return self

    def erase_symbol(self, layer, condition, symbollist=EXCEPTLIST):
        if condition:
            name_new = layer.name
            while name_new[0:1] in symbollist:
                name_new = name_new[1:]
            layer.name = name_new
        return self

    def layer_fullpath(self, layer, path=''):
        fullpath = layer.name + path
        if layer._parent is self.psd:
            return fullpath
        else:
            return self.layer_fullpath(layer._parent, '/' + fullpath)

    def export_anmscript(self, layer, tracknum=0):
        if not layer.is_group():
            return '\n', '\n'

        trackline = f'--track{tracknum}:{layer.name},0,{len(layer)},0,1\n'
        valueline = 'local values = {\n'
        for sublayer in layer:
            valueline += f'  "v1.{self.layer_fullpath(sublayer)}",\n'
        valueline += '}\n'
        valueline += f'PSD:addstate(values, obj.track{tracknum})\n'

        return trackline, valueline



if __name__ == '__main__':
    ifile = r'./sample.psd'
    ifile = r'C:\Users\user\Pictures\sample.psd'
    handler = PSDHandler(ifile)
    x = {handler.psd[0]: 1}
    print(handler.psd[0].is_group())
    for i in handler.psd[0]:
        print(i)
