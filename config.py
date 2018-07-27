import json


class cfg(object):
    def __init__(self, cfg_file='cfg.json'):
        super(cfg, self).__init__()
        with open(cfg_file) as ptr:
            self.js = json.load(ptr)
        self.sheet = ''

    def clear(self):
        self.sheet = ''

    @property
    def distance(self):
        return self.js['core']['distance']

    @property
    def feature(self):
        return self.js['core']['feature']

    @property
    def image_size(self):
        return self.js['gui']['image_size']

    @property
    def numbers(self):
        return self.js['gui']['start_numbers']

    @property
    def style(self):
        try:
            if self.sheet == '':
                with open(self.js['gui']['style_file']) as Ptr:
                    self.sheet = Ptr.read()
        except:
            pass
        return self.sheet

    @property
    def icon(self):
        return self.js['gui']['icon']

    @property
    def window(self):
        return self.js['gui']['window']

    @property
    def lineEdit(self):
        return self.js['gui']['line_edit']

    @property
    def margins(self):
        return self.js['gui']['margins']

    @property
    def margin(self):
        return self.js['gui']['start_margin']

    @property
    def fix(self):
        return self.js['gui']['fix_width']

    @property
    def space(self):
        return self.js['gui']['space']

    @property
    def search(self):
        return self.js['gui']['search']
