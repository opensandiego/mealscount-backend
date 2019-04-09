# coding: utf-8

import pandas as pd
from config import *

#
# Function: displayModelConfig
#
def display_model_config(self):
    print("\n")
    print("MealsCount Model Configuration")
    print("------------------------------")
    print("Version: {}".format(model_version_info["version"]))
    print("Model Variant: {}".format(model_version_info["model_variant"]))
    print("Default ISP Width (%): {}".format(model_version_info["isp_width_default"]))
    print("ISP Width Bundle  (%): {}".format(model_version_info["isp_width_bundle"]))
    print("Min CEP Threshold (%): {}".format(funding_rules["min_cep_thold_pct"]))
    print("Max CEP Threshold (%): {}".format(funding_rules["max_cep_thold_pct"]))
    print("CEP Rates Table:")

    df = pd.DataFrame(funding_rules["cep_rates"])
    df.set_index("region", inplace=True)
    df.index.name = None

    print(df)

#
# class MCConfig:
#     """
#     Implementation for MealsCount configuration parser and data store.
#     """
#
#     def __init__(self, cfgfile):
#         self.__err_status = False
#         self.__cfgfile = cfgfile
#         try:
#             self.__cfgdata = self.__parse(self.__cfgfile)
#         except Exception as e:
#             self.__err_status = True
#             raise e
#
#     def status(self):
#         return not self.__err_status
#
#     def version(self):
#         return self.__cfgdata["version"]
#
#     def params(self, scope=None):
#         if self.status():
#             return self.__cfgdata
#         else:
#             return None
#
#     __parse = parse_JSON
#
#
#
# class MCModelConfig(MCConfig):
#     """
#     Implementation for MealsCount Model Configuration
#     """
#
#     def __init__(self, cfgfile):
#         self.__rates_df = None
#         self.__regions = None
#         self.assistance = None
#         self.__cfgfile = cfgfile
#         try:
#             MCConfig.__init__(self, cfgfile)
#         except Exception as e:
#             raise e
#
#     def isp_width_bundle(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["isp_width_bundle"]
#
#
#     def model_variant(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["model_variant"]
#
#
#     def regions(self):
#         if self.__regions is None:
#             if self.status():
#                 self.__regions = MCConfig.params(self)["us_regions"]
#
#         return self.__regions
#
#     def performance_based_cash_assistance_per_lunch(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["performance_based_cash_assistance_per_lunch"]
#         else:
#             return -1
#
#     def max_cep_thold_pct(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["max_cep_thold_pct"]
#         else:
#             return -1
#
#     def min_cep_thold_pct(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["min_cep_thold_pct"]
#         else:
#             return -1
#
#     def monthly_lunches(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["monthly_lunches"]
#         else:
#             return -1
#
#     def monthly_breakfasts(self):
#         if self.status():
#             return MCConfig.params(self)["model_params"]["monthly_breakfasts"]
#         else:
#             return -1
#
#     def cep_rates(self, region='default'):
#         if self.__rates_df is None:
#             if self.status():
#                 self.__rates_df = pd.DataFrame(MCConfig.params(self)["model_params"]["cep_rates"])
#                 self.__rates_df.set_index("region", inplace=True)
#                 self.__rates_df.index.name = None
#
#         try:
#             cep_rates = self.__rates_df.loc[region]
#         except Exception as e:
#             # use default rates if no explicit rates found for the region
#             # specified (includes both invalid and default regions)
#             cep_rates = self.__rates_df.loc["default"]
#
#         return cep_rates
#
#     def show(self):
#         if self.status():
#             self.__show(MCConfig.params(self))
#         else:
#             print("Error: No configuration to display")
#
#     def params(self, scope='model'):
#         if self.status():
#             if scope is "model":
#                 return MCConfig.params(self)["model_params"]
#             else:
#                 return MCConfig.params(self)
#         else:
#             return None
#
#     __show = display_model_config

#
# Class: mcConfig
#
# class mcConfig:
#     """
#     Implementation for MealsCount configuration parser and data store.
#     """
#
#     def __init__(self, cfgfile):
#         self.__err_status = False
#         self.__cfgfile = cfgfile
#         try:
#             self.__cfgdata = self.__parse(self.__cfgfile)
#         except Exception as e:
#             self.__err_status = True
#             raise e
#
#     def status(self):
#         return not self.__err_status
#
#     def version(self):
#         return self.__cfgdata["version"]
#
#     def params(self, scope=None):
#         if self.status():
#             return self.__cfgdata
#         else:
#             return None
#
#     __parse = parseJSON




#
# class mcModelConfig
#
# class mcModelConfig(mcConfig):
#     """
#     Implementation for MealsCount Model Configuration
#     """
#
#     def __init__(self, cfgfile):
#         self.__rates_df = None
#         self.assistance = None
#         self.__regions = None
#         self.__cfgfile = cfgfile
#         try:
#             mcConfig.__init__(self, cfgfile)
#         except Exception as e:
#             raise e
#
#     def status(self):
#         return mcConfig.status(self)
#
#     def regions(self):
#         if self.__regions is None:
#             if self.status():
#                 self.__regions = mcConfig.params(self)["us_regions"]
#
#         return self.__regions
#
#     def model_variant(self):
#         if self.status():
#             return mcConfig.params(self)["model_params"]["model_variant"]
#
#     def isp_width(self):
#         if self.status():
#             return mcConfig.params(self)["model_params"]["isp_width_default"]
#
#     def isp_width_bundle(self):
#         if self.status():
#             return mcConfig.params(self)["model_params"]["isp_width_bundle"]
#
#     def max_cep_thold_pct(self):
#         if self.status():
#             return mcConfig.params(self)["model_params"]["max_cep_thold_pct"]
#         else:
#             return -1
#
#     def min_cep_thold_pct(self):
#         if self.status():
#             return mcConfig.params(self)["model_params"]["min_cep_thold_pct"]
#         else:
#             return -1
#
#     def cep_rates(self, region='default'):
#         if self.__rates_df is None:
#             if self.status():
#                 self.__rates_df = pd.DataFrame(mcConfig.params(self)["model_params"]["cep_rates"])
#                 self.__rates_df.set_index("region", inplace=True)
#                 self.__rates_df.index.name = None
#
#         try:
#             cep_rates = self.__rates_df.loc[region]
#         except Exception as e:
#             # use default rates if no explicit rates found for the region
#             # specified (includes both invalid and default regions)
#             cep_rates = self.__rates_df.loc["default"]
#
#         return cep_rates
#
#     def show(self):
#         if self.status():
#             self.__show(mcConfig.params(self))
#         else:
#             print("Error: No configuration to display")
#
#     def params(self, scope='model'):
#         if self.status():
#             if scope is "model":
#                 return mcConfig.params(self)["model_params"]
#             else:
#                 return mcConfig.params(self)
#         else:
#             return None
#
#     __show = displayModelConfig
