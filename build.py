import os, sys
import platform
import shutil
import subprocess

if __name__=="__main__":

    print("** clean up build directory **")
    # ディレクトリが存在するか確認して削除
    if os.path.exists("./dist"): shutil.rmtree("./dist")

    print("** build app **")
    if os.name == "nt":
        output_path = "./dist/win"
        # ディレクトリが存在しない場合は作成
        if not os.path.exists(output_path): os.makedirs(output_path)
        result = subprocess.run("pyinstaller --windowed --distpath={} --onefile --noconsole --name main ./src/main.py --collect-data TkEasyGUI -y".format(output_path), shell=True)
    else:
        output_path = "./dist/mac"
        # ディレクトリが存在しない場合は作成
        if not os.path.exists(output_path): os.makedirs(output_path)
        result = subprocess.run(["pyinstaller --windowed --distpath={} --onefile --noconsole --name main ./src/main.py --collect-data TkEasyGUI -y".format(output_path)], shell=True)

    if (result.returncode != 0):
        print("** build error **")
        sys.exit()

    print("** clean up the directory **")
    is_file = os.path.isfile("./*.spec")
    if is_file: os.remove("./*.spec")

    is_dir = os.path.isdir("./build")
    if is_dir: shutil.rmtree('./build')
