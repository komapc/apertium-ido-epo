#!/usr/bin/env python3
import unittest
from date_normalizer import normalize_ido_dates_line, normalize_esperanto_numbers_line


class TestDateNormalizer(unittest.TestCase):
    def test_ordinals_basic(self):
        self.assertEqual(normalize_ido_dates_line('26ma'), '26-a')
        self.assertEqual(normalize_ido_dates_line('1ma 2ma 31ma'), '1-a 2-a 31-a')
        self.assertEqual(normalize_ido_dates_line('10-ma'), '10-a')

    def test_day_di_month(self):
        s = normalize_ido_dates_line('la 26-a di julio')
        self.assertEqual(s, 'la 26-a de julio')

    def test_month_mapping(self):
        self.assertEqual(normalize_ido_dates_line('mayo'), 'majo')
        self.assertEqual(normalize_ido_dates_line('Marzo'), 'Marto')
        self.assertEqual(normalize_ido_dates_line('agosto'), 'aŭgusto')

    def test_century(self):
        self.assertEqual(normalize_ido_dates_line('17ma yarcento'), '17-a jarcento')
        self.assertEqual(normalize_ido_dates_line('17ma jarcento'), '17-a jarcento')
        self.assertEqual(normalize_ido_dates_line('yarcento'), 'jarcento')

    def test_yara(self):
        self.assertEqual(normalize_ido_dates_line('35-yara'), '35-jara')
        self.assertEqual(normalize_ido_dates_line('yara periodo'), 'jara periodo')

    def test_eo_post_removes_stars(self):
        self.assertEqual(normalize_esperanto_numbers_line('*1806'), '1806')
        self.assertEqual(normalize_esperanto_numbers_line('*26-a'), '26-a')
        self.assertEqual(normalize_esperanto_numbers_line('*35-jara'), '35-jara')
        self.assertEqual(normalize_esperanto_numbers_line('*12'), '12')

    def test_pipeline_example(self):
        s = normalize_ido_dates_line('Ye la 26ma di julio 1581 en 17ma yarcento, 35-yara periodo')
        self.assertEqual(s, 'Ye la 26-a de julio 1581 en 17-a jarcento, 35-jara periodo')
        eo = normalize_esperanto_numbers_line('*26-a de julio *1581 *17-a jarcento *35-jara periodo')
        self.assertEqual(eo, '26-a de julio 1581 17-a jarcento 35-jara periodo')


if __name__ == '__main__':
    unittest.main()


