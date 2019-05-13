from .naive import OneToOneCEPStrategy,OneGroupCEPStrategy
from .mc_algo_v2 import AlgoV2CEPStrategy
from .binning import BinCEPStrategy
from .exhaustive import ExaustiveCEPStrategy

STRATEGIES = {
    "OneToOne":OneToOneCEPStrategy,
    "OneGroup":OneGroupCEPStrategy,
    "Binning":BinCEPStrategy,
    "AlgoV2":AlgoV2CEPStrategy,
    "Exhaustive":ExaustiveCEPStrategy
}

