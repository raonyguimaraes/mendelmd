from subprocess import run, check_output
import os
import json

class B2():
    def __init__(self):
        pass
    def main(self):
        print('main')

    def install(self):
        # Newline-separated shell script: each line ran independently (no '&&',
        # failures did not stop later lines). 'cd' becomes cwd= for the later steps.
        run(['git', 'clone', 'https://github.com/Backblaze/B2_Command_Line_Tool.git'])
        run(['python', 'setup.py', 'build'], cwd='B2_Command_Line_Tool')
        run(['python', 'setup.py', 'install'], cwd='B2_Command_Line_Tool')
        run(['b2', 'authorize-account'], cwd='B2_Command_Line_Tool')

    def upload(self, source, dest):

        output = check_output(['b2', 'upload-file', 'rockbio', str(source), str(dest)]).decode('utf-8')
        output = output.splitlines()
        print(output)
        results = ''.join(output[2:])
        print('results', results)
        results = json.loads(results)
        results[output[0].split(':',1)[0]] = output[0].split(':',1)[1:] 
        results[output[1].split(':',1)[0]] = output[1].split(':',1)[1:] 
        
        return(results)      

        # {
        # "action": "upload",
        # "fileId": "4_z9c8c149aa77346e564160516_f109f885ab1209044_d20180131_m235956_c000_v0001058_t0036",
        # "fileName": "test",
        # "size": 0,
        # "uploadTimestamp": 1517443196000
        # }

    def download(self, bucket, file):

        basename = os.path.basename(file)
        run(['b2', 'download-file-by-name', 'rockbio', str(file), str(file)])