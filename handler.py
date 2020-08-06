from psd_tools import PSDImage
import re

class PSDHandler():

    def __init__(self, ifile_path):
        self.psd = PSDImage.open(ifile_path)
        self.depth_max = self.find_depth_max()

    def find_depth_max(self):
        depth_max = 0
        for _, _, depth in self.layer_list():
            if depth > depth_max:
                depth_max = depth
        return depth_max

    def save(self, ofile_path):
        self.psd.save(ofile_path)
        return self

    def layer_list(self):
        for layer in self.psd:
            for element in self.layer_sweeper(layer, self.psd, 1):
                yield element

    @staticmethod
    def layer_sweeper(layer, parent, depth=1):
        yield layer, parent, depth
        if layer.is_group():
            for sublayer in layer:
                for element in PSDHandler.layer_sweeper(sublayer, layer, depth+1):
                    yield element

    def export_layers(self):
        content = ''
        for layer, parent, depth in self.layer_list():
            content += ' ' * depth
            if depth:
                content += '|- '
            content += layer.name + '\n'
        return content

    def add_bikkuri_1st(self):
        for layer, parent, depth in self.layer_list():
            if depth == 1 and layer.name[0] != "!":
                layer.name = "!" + layer.name
        return self

    def add_star_2nd(self):
        for layer, parent, depth in self.layer_list():
            if depth == 2 and layer.name[0] != "*":
                layer.name = "*" + layer.name
        return self

    def erase_symbol_all(self):
        for layer, _, _ in self.layer_list():
            match_sym = re.match('(\*|\!)+', layer.name)
            if match_sym:
                layer.name = layer.name[match_sym.end():]
        return self


if __name__ == '__main__':
    ifile = './im5467479.psd'
    ctrl = PSDHandler(ifile)
    print(ctrl.export_layers())
