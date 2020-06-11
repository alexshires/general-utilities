#! /usr/bin/env python3
"""
utilty to reliably SCP using Python
"""

import os
import subprocess
import argparse
import glob
import logging
import shlex

logger = logging.getLogger(__name__)
logging.basicConfig(level=10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=None, type=str)
    parser.add_argument("-o", "--output", default=None, type=str)
    parser.add_argument("-l", "--limit", default=1000, type=str)
    parser.add_argument("-d", "--dryrun", action="store_true", default=False)
    options = parser.parse_args()
    # TODO: add verbose logging and configuration

    logger.debug("config: %s", options)

    # get list of files - TODO use pathlib?
    file_list = glob.glob(options.input + "/*")
    file_list = sorted(file_list)

    success_dict = dict()

    for filename in file_list:
        base, filestr = os.path.split(filename)
        outputfile = os.path.join(options.output, filestr)
        logger.debug("copying file %s to %s", filename, options.output)
        scp_cmd = f"scp -l {options.limit} {filename} {outputfile}"
        logger.debug(scp_cmd)

        if not options.dryrun:
            logger.debug("running command")
            try:
                subprocess.run(shlex.split(scp_cmd), shell=True, check=True)
            except subprocess.CalledProcessError as e:
                logger.error(e)

        if os.path.exists(outputfile):
            logger.debug("file copied")
            # TODO : add has cehck here
            success_dict[filename] = True
        else:
            logger.error("file failed: %s", filename)
            success_dict[filename] = False

    logger.debug(success_dict)
    # TODO add report of success / filed files

