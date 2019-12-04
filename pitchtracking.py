import argparse
from signalprocessing.custompitchtracking import pitch_track
from types import SimpleNamespace

parser = argparse.ArgumentParser(description="Custom Pitch")
parser.add_argument('-n', '--name', help="Name of audio file")
parser.add_argument('-p', '--plot', action='store_true')
parser.add_argument('-g', '--guiplot', action='store_true')
parser.add_argument('-l', '--level', nargs='?', default='Error',
                    choices=['Critical', 'Error', 'Warning', 'Info', 'Debug'], help='Levels of logger')
args = parser.parse_args()

# this is all redundant but shows usage when not using CLI arguments
name = args.name
plot = args.plot
guiplot = args.guiplot
level = args.level
argsdict = {
    'name': name,
    'plot': plot,
    'guiplot': guiplot,
    'level': level,
}
keys_and_times = pitch_track(SimpleNamespace(**argsdict))
