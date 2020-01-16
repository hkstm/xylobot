import argparse
from types import SimpleNamespace

from signalprocessing.SignalArgParser import add_arguments
from signalprocessing.SignalTrack import pitch_track_wrap

parser = argparse.ArgumentParser(description="Custom Pitch")
parser = add_arguments(parser)
args = parser.parse_args()

keys_and_times = pitch_track_wrap(args)

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
