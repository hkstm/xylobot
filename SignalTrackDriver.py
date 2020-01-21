import argparse
from types import SimpleNamespace

from signalprocessing.SignalArgParser import add_arguments
from signalprocessing.SignalTrack import pitch_track_wrap, pitch_track_wav

parser = argparse.ArgumentParser(description="Custom Pitch")
parser = add_arguments(parser)
args = parser.parse_args()

key_and_times = pitch_track_wrap(args)
# pitchtrackresults = pitch_track_wav(
#     args, is_logging=False)
# print(pitchtrackresults.key_and_times)

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
