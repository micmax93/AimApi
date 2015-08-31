__author__ = 'micmax93'

import api
from datetime import datetime

child = api._age_child
young = api._age_young
adult = api._age_older
senior = api._age_older

male = api._gender_male
female = api._gender_female

unknown = 0


class AgeGenderGrid(object):
    row_dict = {child: 0, young: 1, adult: 2, senior: 3,
                'child': 0, 'young': 1, 'adult': 2, 'senior': 3}
    col_dict = {male: 0, female: 1, 'm': 0, 'f': 1}

    def __init__(self, value=None):
        self.table = [[value for x in range(2)] for x in range(4)]

    def clear(self, value=None):
        self.__init__(value)

    def _set_col(self, row, gender, cb):
        gender = self.col_dict[gender]
        if gender != 0:
            self.table[row][self.col_dict[gender]] = cb(self.table[row][gender])
        else:
            for i in range(len(self.table[row])):
                self.table[row][i] = cb(self.table[row][i])

    def set(self, age, gender, cb):
        age = self.row_dict[age]
        if age != 0:
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


class SubscribersGrid(AgeGenderGrid):
    def __init__(self):
        AgeGenderGrid.__init__(self, value=[])

    @staticmethod
    def _get_cb(subscriber):
        def _cb(old_arr):
            if subscriber in old_arr:
                return old_arr
            else:
                return old_arr + [subscriber]
        return _cb

    def add(self, age, gender, subscriber):
        self.set(age, gender, cb=self._get_cb(subscriber))


class SubscribersList():
    def __init__(self, subscribers_grid):
        self.subscribers = {}
        assert isinstance(subscribers_grid, SubscribersGrid)
        self.grid = subscribers_grid.table
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                for k in range(len(self.grid[i][j])):
                    self.add(self.grid[i][j][k])

    def add(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers[subscriber] = {'sub': subscriber, 'viewers': 0, 'selected': False, 'date': datetime.now()}

    def clear_viewings(self):
        for s in self.subscribers:
            self.subscribers[s]['viewers'] = 0

    def clear_selection(self):
        for s in self.subscribers:
            self.subscribers[s]['selections'] = False

    def update_viewers(self, viewers_grid):
        self.clear_viewings()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                for k in range(len(self.grid[i][j])):
                    self.subscribers[self.grid[i][j][k]] += viewers_grid.table[i][j]

    def choose_subscriber(self, targeted_alg=True):
        subs = filter(lambda s: not s['selected'], self.subscribers.values())
        if len(subs) == 0:
            self.clear_selection()
            subs = self.subscribers.values()
        val = max(s['viewers'] for s in subs)
        if val == 0 and targeted_alg:
            self.clear_selection()
            subs = self.subscribers.values()
            val = max(s['viewers'] for s in subs)
        subs = filter(lambda s: s['viewers'] == val, subs)
        subs = sorted(subs, key=lambda s: s['date'])
        return subs[0]['sub']

    def select_subscriber(self, viewers_grid, targeted_alg=True):
        assert isinstance(viewers_grid, ViewersGrid)
        self.update_viewers(viewers_grid)
        sub = self.choose_subscriber(targeted_alg)
        self.subscribers[sub]['selected'] = True
        self.subscribers[sub]['date'] = datetime.now()
        return sub




