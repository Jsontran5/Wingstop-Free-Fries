import os
from dotenv import load_dotenv

dotenv_path = '/etc/secrets/.env' #for render.com
load_dotenv(dotenv_path=dotenv_path) #for render.com

# load_dotenv()


def runcmd():
    print("Running command")
    os.system('/opt/render/project/bin/yogo inbox show wffpandaexpress1 1')
    print("Ran command")
    return 0


def main():
    runcmd()

if __name__ == '__main__':
    main()