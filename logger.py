import os
import re

__author__ = 'se416237'


class CsvLogger(object):
    def __init__(self, filename, schema=None, sep=';'):
        if schema is None:
            with open(filename, 'r') as f:
                header = f.readline()
                schema = header.rstrip().split(';')
        else:
            assert isinstance(schema, list)
            header = sep.join(schema)
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write('sep=' + sep + "\n")
                    f.write(header + "\n")
            else:
                with open(filename, 'r') as f:
                    h = f.readline().rstrip()
                    mo = re.match("^sep=(.)", h)
                    if mo is not None:
                        sep = mo.group(1)
                        header = sep.join(schema)
                        h = f.readline().rstrip()
                    assert h == header
        self.schema = schema
        self.width = len(schema)
        self.csv = open(filename, 'a')
        self.sep = sep

    def __del__(self):
        self.csv.close()

    def write(self, line):
        self.csv.write(str(line).encode('string-escape') + "\n")

    def write_row(self, row):
        assert len(row) == self.width
        self.write(self.sep.join(str(i) for i in row))

    def write_obj(self, obj):
        if isinstance(obj, dict):
            data = obj
        elif isinstance(obj, object):
            data = obj.__dict__
        else:
            raise ValueError("obj must be an object or dict")
        row = []
        for k in self.schema:
            row.append(str(data[k]))
        self.write_row(row)
