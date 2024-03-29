__author__ = 'micmax93'

import api
from datetime import datetime

child = api._age_child
young = api._age_young
adult = api._age_older
senior = api._age_senior

male = api._gender_male
female = api._gender_female

unknown = 0


class AgeGenderGrid(object):
    row_dict = {0: -1, child: 0, young: 1, adult: 2, senior: 3,
                'child': 0, 'young': 1, 'adult': 2, 'senior': 3,
                'all': -1, 'any': -1, '*': -1, '': None, '0': None}
    col_dict = {0: -1, male: 0, female: 1, 'm': 0, 'f': 1, 'M': 0, 'F': 1,
                'all': -1, 'any': -1, '*': -1, '1': -1, '': None, '0': None}

    def __init__(self, value=None):
        self.table = [[value for x in range(2)] for x in range(4)]

    def clear(self, value=None):
        self.__init__(value)

    def _set_col(self, row, gender, cb):
        gender = self.col_dict[gender]
        if gender is None:
            return
        if gender != -1:
            self.table[row][self.col_dict[gender]] = cb(self.table[row][gender])
        else:
            for i in range(len(self.table[row])):
                self.table[row][i] = cb(self.table[row][i])

    def set(self, age, gender, cb):
        age = self.row_dict[age]
        if age is None:
            return
        if age != -1:
            self._set_col(age, gender, cb)
        else:
            for i in range(len(self.table)):
                self._set_col(i, gender, cb)


class ViewersGrid(AgeGenderGrid):
    def __init__(self):
        AgeGenderGrid.__init__(self, value=0)

    @staticmethod
    def _cb(old_val):
        return old_val+1

    def add(self, age, gender):
        self.set(age, gender, cb=self._cb)


class PublishersGrid(AgeGenderGrid):
    def __init__(self):
        AgeGenderGrid.__init__(self, value=[])

    @staticmethod
    def _get_cb(publisher):
        def _cb(old_arr):
            if publisher in old_arr:
                return old_arr
            else:
                return old_arr + [publisher]
        return _cb

    def add(self, age, gender, publisher):
        self.set(age, gender, cb=self._get_cb(publisher))


class PublishersList():
    def __init__(self, publishers_grid):
        self.publishers = {}
        assert isinstance(publishers_grid, PublishersGrid)
        self.grid = publishers_grid.table
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                for k in range(len(self.grid[i][j])):
                    self.add(self.grid[i][j][k])

    def add(self, publisher):
        if publisher not in self.publishers:
            self.publishers[publisher] = {'pub': publisher, 'viewers': 0, 'selected': False, 'date': datetime.now()}

    def clear_viewings(self):
        for s in self.publishers:
            self.publishers[s]['viewers'] = 0

    def clear_selection(self):
        for s in self.publishers:
            self.publishers[s]['selections'] = False

    def update_viewers(self, viewers_grid):
        self.clear_viewings()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                for k in range(len(self.grid[i][j])):
                    self.publishers[self.grid[i][j][k]]['viewers'] += viewers_grid.table[i][j]

    def choose_publisher(self, targeted_alg=True):
        pubs = filter(lambda s: not s['selected'], self.publishers.values())
        if len(pubs) == 0:
            self.clear_selection()
            pubs = self.publishers.values()
        val = max(s['viewers'] for s in pubs)
        if val == 0 and targeted_alg:
            self.clear_selection()
            pubs = self.publishers.values()
            val = max(s['viewers'] for s in pubs)
        pubs = filter(lambda s: s['viewers'] == val, pubs)
        pubs = sorted(pubs, key=lambda s: s['date'])
        return pubs[0]['pub']

    def select_publisher(self, viewers_grid, targeted_alg=True):
        assert isinstance(viewers_grid, ViewersGrid)
        self.update_viewers(viewers_grid)
        pub = self.choose_publisher(targeted_alg)
        self.publishers[pub]['selected'] = True
        self.publishers[pub]['date'] = datetime.now()
        return pub




