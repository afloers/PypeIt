#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-


"""
This script runs PypeIt
"""

from pypeit.scripts import ql_keck_mosfire
import sys

if __name__ == '__main__':
    args = ql_keck_mosfire.parser()
    rtval = ql_keck_mosfire.main(args)
    sys.exit(rtval)
