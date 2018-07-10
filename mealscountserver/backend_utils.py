
# coding: utf-8
#
#  Meals Count Backend Utilities
#

import sys
import os
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod

#
# GLOBAL CONSTANTS (DO NOT MODIFY)
#

# these are used to identify data rows
# level 1 header
DATA_L1_HDR_KEYS = ['Non-Charter School(s)','Charter School(s)']
# level 2 header
DATA_L2_HDR_KEYS = ['School Code','School Name','Total Enrollment','Free & Reduced Meal Program: 181/182',
                    'Foster','Homeless(1)','Migrant Program: 135','Direct Certification',
                    'Unduplicated Eligible Free/Reduced Meal Counts','EL Funding Eligible (2)',
                    'Total Unduplicated FRPM/EL Eligible (3)']
# keywords for aggregated rows
DATA_SUM1_KEYS = ['TOTAL - Selected Schools']
DATA_SUM2_KEYS = ['TOTAL LEA']

# these are used for recoding header names/col values where applicable
DATA_L1_HDR_DICT = {'Non-Charter School(s)':'non-charter','Charter School(s)':'charter'}
DATA_L2_HDR_DICT = {'School Code':'school_code','School Name':'school_name','Total Enrollment':'total_enrolled',
                    'Free & Reduced Meal Program: 181/182':'frpm','Foster':'foster','Homeless (1)':'homeless',
                    'Migrant Program: 135':'migrant','Direct Certification':'direct_cert',
                    'Unduplicated Eligible Free/Reduced Meal Counts':'frpm_nodup',
                    'EL Funding Eligible (2)':'el', 'Total Unduplicated FRPM/EL Eligible (3)':'frpm_el_nodup'}
DATA_SUM_DICT = {'TOTAL - Selected Schools':'total','TOTAL LEA':'total'}

# these are used for recoding specific col values
INVALID_SCHOOL_CODE = 9999999
ALL_SCHOOL_TYPE = 'lea'

# these are used to identify metadata rows
METADATA_KEYS = ['Academic Year','View','As Of','Gender','School Type','School','User ID',
                 'Created Date','LEA']
# these are used to identify cols corresponding to
# metadata key-value pairs
METADATA_KEY_COLS = [0,2,4]
METADATA_VAL_COLS = [1,3,5]

#
# CLASS: mcSchoolDistInput
#
# Abstract base class to specify API for MealsCount school district input
# data instances
#
class mcSchoolDistInput(ABC):
    """
    Base class for school district input.
    """
    # dataframe for school district data
    d_df = pd.DataFrame()
    # dictionary for school district metadata
    md_dict = {}

    def __init__(self):
        pass

    @abstractmethod
    def to_frame(self):
        pass

    @abstractmethod
    def metadata(self):
        pass

#
# Function to extract and return a dataframe from the input
# dataframe and the row and col indices specified. Additionally
# a column for school type is added with the specified value as
# well as a column (called 'index') with the original row indices.
#
def extract_df(df,row_idx,col_idx,school_type):

    data = df.loc[row_idx,:].values
    cols = df.loc[col_idx].values
    ext_df = pd.DataFrame(data=data,columns=cols)

    ext_df['school_type'] = school_type
    ext_df['index'] = row_idx

    ext_df.dropna(axis=1,how='all',inplace=True)
    ext_df.dropna(axis=0,how='all',inplace=True)

    return ext_df

# FIXME: refactor code in here
#
# Function to parse MealsCount school district input data in Excel file format
# A successful execution will result in the d_df and md_dict variables of the
# mcXLSchoolDistInput instance to be populated with data from the Excel file.
#
# Any errors during parsing wlll result in an exception
#
def parseXL(self,xlfile):

    try:
        xl = pd.ExcelFile(xlfile)
        tmpdf = xl.parse(xl.sheet_names[0])

        # get the indices for the rows where the L1 headers are present
        data_l1 = tmpdf.index[tmpdf[tmpdf.isin(DATA_L1_HDR_KEYS)].notnull().any(axis=1)].tolist()
        # get indices for rows where the L2 headers are present
        # these will indicate the beginning of data
        data_l2_begin = tmpdf.index[tmpdf[tmpdf.isin(DATA_L2_HDR_KEYS)].notnull().any(axis=1)].tolist()
        # get indices for the rows where the misc headers are present
        # these will indicate the end of data
        data_l2_end = tmpdf.index[tmpdf[tmpdf.isin(DATA_SUM1_KEYS)].notnull().any(axis=1)].tolist()
        # get indices for any other keys that are part of data
        data_other = tmpdf.index[tmpdf[tmpdf.isin(DATA_SUM2_KEYS)].notnull().any(axis=1)].tolist()

        # generate indices of non-data rows
        metadata_idx = list(range(0,data_l1[0]))
        n = len(DATA_L1_HDR_KEYS)

        # TODO: malformed files may have any of the keys missing resulting in
        # empty lists of indices

        for i in range(0,n):
            metadata_idx += list(range(data_l1[i]+1,data_l2_begin[i]))
            if i < n-1:
                metadata_idx += list(range(data_l2_end[i]+1,data_l1[i+1]))

        metadata_idx += list(range(data_l2_end[n-1]+1,data_other[0]))
        metadata_idx += list(range(data_other[-1]+1,tmpdf.shape[0]))

        # copy metadata rows to its own dataframe
        tmpdf_md = tmpdf.loc[metadata_idx,:]
        # clean-up
        tmpdf_md.dropna(axis=1,how='all',inplace=True)
        tmpdf_md.dropna(axis=0,how='all',inplace=True)

        # purge metadata rows (copied above) from the data df
        tmpdf.drop(metadata_idx,inplace=True)
        # clean-up
        tmpdf.dropna(axis=1,how='all',inplace=True)
        tmpdf.dropna(axis=0,how='all',inplace=True)

        # collect l1 header names
        # needed because we don't know the order in which the l1 headers occur in data
        df_l1 = tmpdf.loc[data_l1]
        df_l1 = df_l1.loc[:,df_l1.notnull().any()]
        l1_hdrs = df_l1.T.unstack().tolist()
        l1_hdrs = [s for s in l1_hdrs if str(s) != 'nan']

        # drop all l1 headers
        # we will be using a single-level index for the final df
        # l1 headers will be used to populate a categorical var instead
        tmpdf.drop(data_l1,inplace=True)

        # create a new ddtaframe for each school type
        df_list = []
        for i in range(0,n):

            row_idx = list(range(data_l2_begin[i]+1,data_l2_end[i]+1))
            col_idx = data_l2_begin[i]
            school_type = l1_hdrs[i]

            df_list.append(extract_df(tmpdf,row_idx,col_idx,school_type))

            # if this the last of the school types we need to append
            # the aggregated lea rows. we do this as a separate df containing
            # data_other rows.
            if (i==n-1):
                row_idx = data_other
                df_list.append(extract_df(tmpdf,row_idx,col_idx,np.nan))

        # we have a df with all data for all school types including aggregated
        # rows at this point
        df_full = pd.concat(df_list,axis=0,ignore_index=True)

        # recode column names
        df_full.rename(columns=DATA_L2_HDR_DICT,inplace=True)
        # recode school_type
        df_full['school_type'] = df_full['school_type'].map(DATA_L1_HDR_DICT)
        # recode other fields
        cond = df_full['index'].isin(data_l2_end + data_other)
        df_full.loc[cond,'school_name'] = df_full[cond]['school_code'].map(DATA_SUM_DICT)
        df_full.loc[cond,'school_code'] = INVALID_SCHOOL_CODE
        cond = df_full['index'].isin(data_other)
        df_full.loc[cond,'school_type'] = ALL_SCHOOL_TYPE

        df_full.drop(['index'],axis=1,inplace=True)
        # re-arrange cols to original order
        df_full = df_full[list(DATA_L2_HDR_DICT.values()) + ['school_type']]

        #
        # METADATA
        #

        # add appropriate prefix and suffix to metadata keys
        md_keys = ['   ' + s + ':' for s in METADATA_KEYS]
        # get indices for rows where the metadata keywords are present
        md_idx = tmpdf_md.index[tmpdf_md[tmpdf_md.isin(md_keys)].notnull().any(axis=1)].tolist()

        # extract non-null cols only for those rows containing metadata keys
        tmpdf_md = tmpdf_md.loc[md_idx,:]
        tmpdf_md.dropna(axis=1,how='all',inplace=True)
        tmpdf_md.dropna(axis=0,how='all',inplace=True)
        tmpdf_md.columns = list(range(0,tmpdf_md.shape[1]))

        # extract metadata keys
        md_keys = list(tmpdf_md.loc[:,METADATA_KEY_COLS].unstack().values)
        md_keys = list(map(str.strip,md_keys))
        md_keys = list(map(str.lower,md_keys))
        md_keys = [s.replace(' ','_') for s in md_keys]
        md_keys = [s[:-1] for s in md_keys]

        # extract metadata values
        md_vals = list(tmpdf_md.loc[:,METADATA_VAL_COLS].unstack().values)
        md_vals = [s.lower() if isinstance(s, str) else s for s in md_vals]

        md_dict = dict(zip(md_keys, md_vals))

        # store only at the end when we have successfully completed all steps
        # for both data and metadata
        self.d_df = df_full
        self.md_dict = md_dict

    except Exception as e:
        raise e

#
# CLASS: mcXLSchoolDistInput
#
# Abstract base class to specify API for MealsCount school district input
# data instances
#
class mcXLSchoolDistInput(mcSchoolDistInput):
    """
    Implementation for MealsCount Excel format school district input. Expects input
    to be a file stored on the backend.
    """

    def __init__(self, datafile):
        mcSchoolDistInput.__init__(self)
        self.__datafile = datafile
        try:
            self.__parse(self.__datafile)
        except Exception as e:
            raise e

    def to_frame(self):
        return self.d_df

    def metadata(self):
        return self.md_dict

    __parse = parseXL