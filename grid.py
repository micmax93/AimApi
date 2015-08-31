__author__ = 'micmax93'

import api

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






