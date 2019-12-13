import argparse
from types import SimpleNamespace

from signalprocessing.SignalParser import add_arguments
from signalprocessing.custompitchtracking import pitch_track

parser = argparse.ArgumentParser(description="Custom Pitch")
parser = add_arguments(parser)
args = parser.parse_args()

keys_and_times = pitch_track(args)

# this is all redundant but shows usage when not using CLI arguments

# argsdict = {
#     'name': args.name,
#     'plot': args.plot,
#     'guiplot': args.guiplot,
#     'level': args.level,
#     'window': args.window,
#     'fftsize': args.fftsize
# }
# keys_and_times = pitch_track(SimpleNamespace(**argsdict))
