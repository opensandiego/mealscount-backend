from .base import OneToOneCEPDistrict,OneGroupCEPDistrict 
from .mc_algo_v2 import AlgoV2CEPDistrict
from .binning import BinCEPDistrict

STRATEGIES = {
    "OneToOne":OneToOneCEPDistrict,
    "OneGroup":OneGroupCEPDistrict,
    "Binning":BinCEPDistrict,
    "AlgoV2":AlgoV2CEPDistrict,
}


