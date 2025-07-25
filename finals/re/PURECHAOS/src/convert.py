import subprocess
import os, shutil, sys

args = []
for i, arg in enumerate(sys.argv[1:], start=1): 
    args.append(arg)

root = os.path.dirname(os.path.abspath(__file__))
file = args[0]
exec = [f"{root}\\{file}.exe", f"{root}\\{args[1]}.exe"]

def main():
    for i in exec:
        if os.path.exists(i): os.remove(i)

    subprocess.call(["pyinstaller", "--onefile", f"{file}.py", "-i", "NONE"])
    
    shutil.move(f"{root}\\dist\\{file}.exe", root)
    os.rename(exec[0], exec[1])
    
    for i in ["build", "dist", "__pycache__"]:
        if (os.path.exists(f"{root}\\{i}")): 
            shutil.rmtree(f"{root}\\{i}")
    
    os.remove(f"{root}\\{file}.spec")

if __name__=="__main__":
    main()