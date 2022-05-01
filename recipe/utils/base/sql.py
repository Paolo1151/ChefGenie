from abc import abstractmethod
from .model import BaseObject

class SqlFilter(BaseObject):
    def __init__(self, name):
        super().__init__(name)
        self.is_last = False

    def toggle_last(self):
        self.is_last = not self.is_last

    @abstractmethod
    def to_sql():
        pass
    
    def parse_filter(self, filter_script):
        if self.is_last:
            return filter_script
        else:
            return filter_script + ' AND '