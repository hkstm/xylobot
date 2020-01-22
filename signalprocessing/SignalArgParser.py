import argparse


def add_arguments(parser):
    parser.add_argument('-n', '--name', default='scale3', help="Name of audio file")
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('-g', '--guiplot', action='store_true')
    parser.add_argument('-r', '--raw', action='store_true', help='Return data so it can be used for analysis')
    parser.add_argument('-w', '--window', default='blackman', choices=['bartlett', 'blackman', 'hamming', 'hanning'],
                        help="Type of windowing function")
    parser.add_argument('-s', '--fftsize', default=512, type=int, help="FFT size")
    parser.add_argument('-l', '--level', nargs='?', default='error',
                        choices=['critical', 'error', 'warning', 'info', 'debug'], type=str.lower, help='Levels of logger')
    parser.add_argument('-t', '--topindex', nargs='?', default='1', type=int)
    parser.add_argument('-f', '--loudnessfactor', nargs='?', default='0.4', type=float)
    return parser