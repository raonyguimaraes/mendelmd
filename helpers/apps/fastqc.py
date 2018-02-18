import argparse
from subprocess import run, check_output
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
        #check if package is installed
        command = 'conda list | grep fastqc'
        output = check_output(command, shell=True).decode('utf-8')
        print('output', output)
        if output == '':
            command = 'conda install -y fastqc'
            run(command, shell=True)
    def run(self, input):
        for file in input:
            command = 'fastqc input/{} -o output/'.format(file)
            print(command)
            run(command, shell=True)

if __name__ == "__main__":
    
    fastqc = FASTQC()
    
    if args.args:
        if 'install' in args.args:
            fastqc.install()
    if args.input:
        fastqc.run(args.input)