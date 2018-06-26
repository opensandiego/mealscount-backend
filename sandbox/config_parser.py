
# coding: utf-8

# MealsCount Config Parser
#
# Functionality to parse the MealsCount configuration file (in JSON format).
#

import sys
import os
import json
import pandas as pd
import numpy as np

# TODO: Add documentation

#
# Function: parseJSON
#

def parseJSON(self,cfgfile):

    try:
        with open(cfgfile) as f:
            jsondata = json.load(f)
    except ValueError as ve:
        print("Failed to parse {}".format(cfgfile))
        raise ve
    except Exception as e:
        raise e

    return jsondata

#
# Class: mcConfig
#
class mcConfig:
    """
    Implementation for MealsCount configuration parser and data store.
    """

    def __init__(self, cfgfile):
        self.__err_status = False
        self.__cfgfile = cfgfile
        try:
            self.__cfgdata = self.__parse(self.__cfgfile)
        except Exception as e:
            self.__err_status = True
            raise e

    def status(self):
        return not self.__err_status

    def version(self):
        return self.__cfgdata["version"]

    def params(self, scope=None):
        if self.status():
            return self.__cfgdata
        else:
            return None

    __parse = parseJSON

#
# Function: displayModelConfig
#
def displayModelConfig(self,cfgdata):

    print("\n")
    print("MealsCount Model Configuration")
    print("------------------------------")
    print("Version: {}".format(cfgdata["version"]))
    print("Model Variant: {}".format(cfgdata["model_params"]["model_variant"]))
    print("Default ISP Width (%): {}".format(cfgdata["model_params"]["isp_width_default"]))
    print("Min CEP Threshold (%): {}".format(cfgdata["model_params"]["min_cep_thold_pct"]))
    print("Max CEP Threshold (%): {}".format(cfgdata["model_params"]["max_cep_thold_pct"]))
    print("CEP Rates Table:")

    df = pd.DataFrame(cfgdata["model_params"]["cep_rates"])
    df.set_index("region",inplace=True)
    df.index.name=None

    print(df)

#
# class mcModelConfig
#
class mcModelConfig(mcConfig):
    """
    Implementation for MealsCount Model Configuration
    """

    def __init__(self, cfgfile):
        self.__rates_df = None
        self.__regions = None
        self.__cfgfile = cfgfile
        try:
            mcConfig.__init__(self,cfgfile)
        except Exception as e:
            raise e

    def status(self):
        return mcConfig.status(self)

    def regions(self):
        if self.__regions is None:
            if self.status():
                self.__regions = mcConfig.params(self)["us_regions"]

        return self.__regions
    
    def model_variant(self):
        if self.status():
            return mcConfig.params(self)["model_params"]["model_variant"]
    
    def isp_width(self):
        if self.status():
            return mcConfig.params(self)["model_params"]["isp_width_default"]        

    def max_cep_thold_pct(self):
        if self.status():
            return mcConfig.params(self)["model_params"]["max_cep_thold_pct"]
        else:
            return -1
    def min_cep_thold_pct(self):
        if self.status():
            return mcConfig.params(self)["model_params"]["min_cep_thold_pct"]
        else:
            return -1

    def cep_rates(self,region='default'):
        if self.__rates_df is None:
            if self.status():
                self.__rates_df = pd.DataFrame(mcConfig.params(self)["model_params"]["cep_rates"])
                self.__rates_df.set_index("region",inplace=True)
                self.__rates_df.index.name=None

        try:
            cep_rates = self.__rates_df.loc[region]
        except Exception as e:
            # use default rates if no explicit rates found for the region
            # specified (includes both invalid and default regions)
            cep_rates = self.__rates_df.loc["default"]

        return cep_rates

    def show(self):
        if self.status():
            self.__show(mcConfig.params(self))
        else:
            print("Error: No configuration to display")

    def params(self,scope='model'):
        if self.status():
            if scope is "model":
                return mcConfig.params(self)["model_params"]
            else:
                return mcConfig.params(self)
        else:
            return None

    __show = displayModelConfig
