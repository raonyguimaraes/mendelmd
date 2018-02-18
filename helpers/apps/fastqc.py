import argparse
from subprocess import run
import sys

sys.path.append('$HOME/miniconda/bin')

parser = argparse.ArgumentParser()
parser.add_argument('args', nargs='?')
parser.add_argument('-i', '--input', nargs='+', help='input')
args = parser.parse_args()
print(args)

class FASTQC():
    def __init__(self):
        pass
    def install(self):
        command = 'conda install -y fastqc'
        run(command, shell=True)
    def run(self, input):
        for file in input:
            command = 'fastqc input/{} -o output/'.format(file)
            run(command, shell=True)

if __name__ == "__main__":
    # execute only if run as a script
    fastqc = FASTQC()
    
    if args.args:
        fastqc.install()

    fastqc.run(args.input)