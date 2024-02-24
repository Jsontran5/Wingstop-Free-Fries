import os

def runcmd():
    print("Running command")
    os.system('cmd /c "yogo inbox show wffpandaexpress1 1"')
    print("Ran command")
    return 0


def main():
    runcmd()

if __name__ == '__main__':
    main()