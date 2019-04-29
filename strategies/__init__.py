from .base import OneToOneCEPDistrict,OneGroupCEPDistrict 
from .mc_algo_v2 import AlgoV2CEPDistrict
from .binning import BinCEPDistrict
from .exhaustive import ExaustiveCEPDistrict

STRATEGIES = {
    "OneToOne":OneToOneCEPDistrict,
    "OneGroup":OneGroupCEPDistrict,
    "Binning":BinCEPDistrict,
    "AlgoV2":AlgoV2CEPDistrict,
    "Exhaustive":ExaustiveCEPDistrict
}


