#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-
"""
This script runs PypeIt
"""
import argparse

from pypeit import msgs

import warnings

def parser(options=None):

    parser = argparse.ArgumentParser(description=msgs.usage('PypeIt'),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('pypeit_file', type=str,
                        help='PypeIt reduction file (must have .pypeit extension)')
    parser.add_argument('-v', '--verbosity', type=int, default=2,
                        help='Verbosity level between 0 [none] and 2 [all]')
    # JFH TODO Are the -t and -r keyword still valid given that run_pypeit no longer runs setup?
    parser.add_argument('-t', '--hdrframetype', default=False, action='store_true',
                        help='Use file headers and the instument-specific keywords to determine'
                             'the type of each frame')
    parser.add_argument('-r', '--redux_path', default=None,
                        help='Path to directory for the reduction.  Only advised for testing')
    parser.add_argument('-m', '--use_masters', default=False, action='store_true',
                        help='Load previously generated MasterFrames')
    parser.add_argument('-s', '--show', default=False, action='store_true',
                        help='Show reduction steps via plots (which will block further execution until clicked on) '
                             'and outputs to ginga. Requires remote control ginga session via "ginga --modules=RC &"')
    # JFH Should the default now be true with the new definition.
    parser.add_argument('-o', '--overwrite', default=False, action='store_true',
                        help='Overwrite any existing files/directories')
    group = parser.add_mutually_exclusive_group()
#    group.add_argument('-p', '--prep_setup', default=False, action='store_true',
#                       help='Run pypeit to prepare the setup only')
#    group.add_argument('-c', '--calcheck', default=False, action='store_true',
#                       help='Run pypeit only as a check on the calibrations')
    group.add_argument('-d', '--detector', default=None, help='Detector to limit reductions on.  If the output files exist and -o is used, the outputs for the input detector will be replaced.')

#    parser.add_argument('-q', '--quick', default=False, help='Quick reduction',
#                        action='store_true')
    parser.add_argument('-c', '--calib_only', default=False, action='store_true',
                         help='Only run on calibrations')
#    parser.print_help()

    if options is None:
        pargs = parser.parse_args()
    else:
        pargs = parser.parse_args(options)
    return pargs


def main(args):

    import os

    from pypeit import pypeit

    # Initiate logging for bugs and command line help
    # These messages will not be saved to a log file
    # Set the default variables
    qck = False
    cpu = 1
    #vrb = 2

    # Load options from command line
    splitnm = os.path.splitext(args.pypeit_file)
    if splitnm[1] != '.pypeit':
        msgs.error("Bad extension for PypeIt reduction file."+msgs.newline()+".pypeit is required")
    logname = splitnm[0] + ".log"

    # Instantiate the main pipeline reduction object
    pypeIt = pypeit.PypeIt(args.pypeit_file, verbosity=args.verbosity,
                           redux_path=args.redux_path,
                           reuse_masters=args.use_masters, overwrite=args.overwrite,
                           logname=logname, show=args.show, calib_only=args.calib_only)
    # Detector?
    if args.detector is not None:
        msgs.info("Restricting reductions to detector={}".format(args.detector))
        pypeIt.par['rdx']['detnum'] = int(args.detector)

    # Reduce
    if args.calib_only:
        pypeIt.calib_all()
    else:
        pypeIt.reduce_all()
    msgs.info('Data reduction complete')
    # QA HTML
    msgs.info('Generating QA HTML')
    pypeIt.build_qa()

    return 0

