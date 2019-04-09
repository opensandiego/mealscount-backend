from ..national_program_algorithm import CEPSchoolGroupGenerator
import unittest
from config import *
from ..national_program_algorithm import mcAlgorithmV2
import mealscountserver.backend_utils as bu
from pathlib import Path


class TestCEPSchoolGroupGenerator(unittest.TestCase):
    def setUp(self):
        self.strategy = mcAlgorithmV2()
        self.data = bu.dataFrameAndMetadataFromXL(Path('mealscountserver/static/csv/calpads_sample_data.xlsx'))

    def test_init_problems(self):
        with self.assertRaises(ValueError):
            a = CEPSchoolGroupGenerator()
        with self.assertRaises(ValueError):
            b = CEPSchoolGroupGenerator(cfg='', strategy='')
        with self.assertRaises(ValueError):
            c = CEPSchoolGroupGenerator(cfg="something's_wrong", strategy="something's_wrong")

    def test_real_init(self):
        grouped_data = CEPSchoolGroupGenerator(funding_rules, self.strategy)
        self.assertNotEqual(grouped_data, None)

    def test_groupgen_output(self):

        grouped_data = list(CEPSchoolGroupGenerator(funding_rules, self.strategy).get_groups(self.data))
        self.assertIsNotNone(grouped_data)
