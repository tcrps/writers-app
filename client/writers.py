import argparse
import requests
import os, sys
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("HOST_URL")

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--init', action='store_true', help='initialize tables')
    parser.add_argument('-s', '--show', action='store_true', help='show writers')
    parser.add_argument('-w', '--writer', dest='writer_id', help='shows data about a writer')

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    if args.init:
        res = requests.post(url + '/init')
        print(res.text)
    
    if args.show:
        res = requests.get(url + '/show')
        print(res.text)
    
    elif args.writer_id:
        res = requests.get(url + '/writers/' + args.writer_id)
        print(res.text)
        
if __name__ == '__main__':
    main()