import psd_tools
import tkinter as tk
import tkinter.ttk as ttk

class PSDImageExt(psd_tools.PSDImage):

    HEADSYMBOLS = ('!', '*')

    @classmethod
    def open(cls, filepath, encoding='sjis', **kwargs):
        psd = super(PSDImageExt, cls).open(filepath, encoding=encoding, **kwargs)
        psd.depth_max = psd.find_depth_max()
        psd.encoding = encoding
        return psd

    def find_depth_max(self):
        depth_max = 0
        for _, depth in self.all_layers():
            if depth > depth_max:
                depth_max = depth
        return depth_max

    def save(self, file_path, encoding=None, **kwargs):
        if encoding is None:
            encoding = self.encoding
        super().save(file_path, encoding=encoding, **kwargs)
        return self

    @classmethod
    def sublayers_recursive(cls, layer, depth=0):
        if layer.is_group():
            for sublayer in layer:
                subdepth = depth + 1
                yield sublayer, subdepth
                for subsublayer, subsubdepth in cls.sublayers_recursive(sublayer, subdepth):
                    yield subsublayer, subsubdepth
    
    def all_layers(self):
        for layer, depth in self.sublayers_recursive(self):
            yield layer, depth

    def export_layers(self):
        content = ''
        for layer, depth in self.all_layers():
            content += str(depth) + ' ' * 2 * depth
            if depth > 1:
                content += '|-  '
            content += '[' + layer.name + ']\n'
        return content

    def layer_fullpath(self, layer, path=''):
        if type(layer._parent) is type(self) and not (layer._parent is self):
            raise Exception('The layer is not a part of the psd')

        fullpath = layer.name + path
        if layer._parent is self:
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
    psd0 = PSDImageExt.open(ifile, encoding='sjis')
    ifile = r'C:\Users\user\Pictures\sample.psd'
    psd1 = PSDImageExt.open(ifile, encoding='sjis')
    print(type(psd0.HEADSYBMOLS))
