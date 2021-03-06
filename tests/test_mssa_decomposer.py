# -*- coding: utf-8 -*-

import pytest
import csv
import sys
import os
from filecmp import cmp
from feature_eng.feature_eng import FeatureEng

__author__ = "Harvey Bastidas"
__copyright__ = "Harvey Bastidas"
__license__ = "mit"

class Conf:
    """ This method initialize the configuration variables for a plugin """
    
    def __init__(self):
        """ Component Tests Constructor """
        fname = os.path.join(os.path.dirname(__file__), "data/test_input.csv")
        self.input_file = fname
        """ Test dataset filename """
        fname = os.path.join(os.path.dirname(__file__), "data/test_output.csv")
        self.output_file = fname
        """ Output dataset filename """
        self.list_plugins = False
        self.core_plugin = "mssa_decomposer"
        self.num_components = 5
        self.group_similar = True
        self.window_size = 30

class TestMSSADecomposer:
    """ Component Tests  """

    def setup_method(self, test_method):
        """ Component Tests Constructor """
        self.conf = Conf()
        self.rows_d, self.cols_d = self.get_size_csv(self.conf.input_file)
        """ Get the number of rows and columns of the test dataset """
        try:
            os.remove(self.conf.output_file)
        except:
            print("No test output file found.")
            pass

    def get_size_csv(self, csv_file):
        """ Get the number of rows and columns of a test dataset, used in all tests.

        Args:
        csv_file (string): Path and filename of a test dataset

        Returns:
        (int,int): number of rows, number of columns
        """
        rows = list(csv.reader(open(csv_file)))
        return (len(rows), len(rows[0]))


    def test_C03T01_core(self):
        """ Loads plugin from FeatureEng using parameters from setup_method() and Asses that output file has 1 column and num_ticks - forward_ticks """
        self.fe = FeatureEng(self.conf)
        # get the number of rows and cols from out_file
        rows_o, cols_o = self.get_size_csv(self.conf.output_file)
        # assertion
        assert (cols_o == self.fe.ep_core.cols_d * self.conf.num_components)

    def test_C03T02_cmdline(self):
        """ same as C03T02, but via command-line """
        os.system("feature_eng --core_plugin mssa_decomposer --input_file "
            + self.conf.input_file
            + " --output_file "
            + self.conf.output_file
            + " --num_components "
            + str(self.conf.num_components)
        )
        # get the size of the output dataset
        rows_d, cols_d = self.get_size_csv(self.conf.input_file)
        # get the size of the output dataset
        rows_o, cols_o = self.get_size_csv(self.conf.output_file)
        # assert if the number of rows an colums is less than the input dataset and > 0
        assert (cols_o == self.cols_d * self.conf.num_components)
