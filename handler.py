from psd_tools import PSDImage

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

    def add_bikkuri_1st(self):
        for layer, depth in self.layer_list():
            if depth == 1 and layer.name[0] != "!":
                layer.name = "!" + layer.name
        return self

    def add_star_2nd(self):
        for layer, depth in self.layer_list():
            if depth == 2 and layer.name[0] != "*":
                layer.name = "*" + layer.name
        return self

    def erase_symbol_all(self):
        for layer, _ in self.layer_list():
            name_new = layer.name
            while name_new[0:1] in ('!', '*'):
                name_new = name_new[1:]
            layer.name = name_new
        return self

    def layer_fullpath(self, layer, path = ''):
        fullpath = layer.name + path
        if layer._parent is self.psd:
            return fullpath
        else:
            return self.layer_fullpath(layer._parent, '/' + fullpath)

if __name__ == '__main__':
    ifile = './sample.psd'
    ctrl = PSDHandler(ifile)
