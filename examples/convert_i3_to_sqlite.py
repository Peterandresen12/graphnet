"""Minimum working example (MWE) to use SQLiteDataConverter."""

import logging
import os

from graphnet.utilities.logging import get_logger

from graphnet.data.extractors import (
    I3FeatureExtractorIceCube86,
    I3FeatureExtractorIceCubeUpgrade,
    I3RetroExtractor,
    I3TruthExtractor,
    I3SplineMPEICExtractor,
)
from graphnet.data.sqlite.sqlite_dataconverter import SQLiteDataConverter

logger = get_logger(level=logging.DEBUG)


def main_icecube86():
    """Main script function."""
    paths = [
        "/data/user/sschindler/zeuthenCluster_moonL4_exp13_01/"
    ]
    pulsemap = "TWSRTHVInIcePulses"
    gcd_rescue = None
    outdir = "/data/user/pa000/MoonPointing/sschindler_data_with_reco_and_new_pulsemap"

    converter = SQLiteDataConverter(
        [
            I3TruthExtractor(),
            I3SplineMPEICExtractor(),
            I3FeatureExtractorIceCube86(pulsemap),
        ],
        outdir,
        gcd_rescue,
    )
    converter(paths)
    converter.merge_files('/data/user/pa000/MoonPointing/sschindler_data_with_reco_and_new_pulsemap/Merged_database/moonL4_segspline_exp13_01_merged_with_time_and_reco_and_new_pulsemap.db')

def main_icecube_upgrade():
    """Main script function."""
    basedir = "/groups/icecube/asogaard/data/IceCubeUpgrade/nu_simulation/detector/step4/"
    paths = [os.path.join(basedir, "step4")]
    gcd_rescue = os.path.join(
        basedir, "gcd/GeoCalibDetectorStatus_ICUpgrade.v55.mixed.V5.i3.bz2"
    )
    outdir = "/groups/icecube/asogaard/temp/sqlite_test_upgrade"
    workers = 10

    converter = SQLiteDataConverter(
        [
            I3TruthExtractor(),
            I3RetroExtractor(),
            I3FeatureExtractorIceCubeUpgrade(
                "I3RecoPulseSeriesMapRFCleaned_mDOM"
            ),
            I3FeatureExtractorIceCubeUpgrade(
                "I3RecoPulseSeriesMapRFCleaned_DEgg"
            ),
        ],
        outdir,
        gcd_rescue,
        workers=workers,
        nb_files_to_batch=1000,
        # sequential_batch_pattern="temp_{:03d}",
        input_file_batch_pattern="[A-Z]{1}_[0-9]{5}*.i3.zst",
        verbose=1,
    )
    converter(paths)


if __name__ == "__main__":
    main_icecube86()
    #main_icecube_upgrade()
