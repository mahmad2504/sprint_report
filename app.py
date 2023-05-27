import os 
import json
import argparse

p={
"image_name":"sprint_report",
"commit":"df75a4a6dca5705ae9c724ffec37b7c2b2e85865",
"docker_registry":"harbor.xcr.svcs01eu.prod.eu-central-1.kaas.sws.siemens.com/eps",
"code_repository":"https://github.com/mahmad2504/sprint_report.git"
}

#docker build . --build-arg COMMIT=%commit%  -t %image_name%

try:
    f = open('parameters.json')
    p = json.load(f)
except:
    with open('parameters.json', 'w') as f:
        json.dump(p, f)


# Construct the argument parser and parse the arguments
arg_desc = '''\
        This program Generates Sprint Reports!
        --------------------------------
        
        '''
        
parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,description= arg_desc)
parser.add_argument('target',   help='build, package, debug , run')
parser.add_argument('--sprint',   help='sprint name required for debug and run command')
parser.add_argument('--verbose',   action='store_true', help='sprint name required for debug and run command')

args = parser.parse_args()


def mprint(message,force=0):
    if force:
         print(message)
    else:
        if args.verbose: 
            print(message)
            
match args.target:
    case 'build':
        cmd=f'docker   build . --build-arg COMMIT={p["commit"]} --build-arg CODE_REPOSITORY={p["code_repository"]} -t {p["image_name"]}'
        mprint(cmd)
        os.system(cmd)
    case 'package':
        cmd=f'docker tag {p["image_name"]}:latest {p["docker_registry"]}/{p["image_name"]}:latest'
        mprint(cmd)
        os.system(cmd)
        cmd=f'docker push {p["docker_registry"]}/{p["image_name"]}:latest'
        os.system(cmd)
    case 'debug':
        if args.sprint:
            cmd=f'docker run -it --rm -w /app -v {os.getcwd()}:/app {p["image_name"]}:latest python3 main.py "{args.sprint}"'
            mprint(cmd)
            os.system(cmd)
        else:
            mprint("sprint argument missing",1)
    case 'run':
        if args.sprint:
            cmd=f'docker run -it --rm -w /src  {p["docker_registry"]}/{p["image_name"]}:latest python3 main.py "{args.sprint}"'
            mprint(cmd)
            os.system(cmd)
        else:
            mprint("sprint argument missing",1)
  


