import os, sys
import platform
import shutil
import subprocess

if __name__=="__main__":

    print("** clean up build directory **")
    # ディレクトリが存在するか確認して削除
    if os.path.exists("./dist"): shutil.rmtree("./dist")

    print("** build app **")
    app_name = "afu"
    if os.name == "nt":
        app_name = "{}-windows.exe".format(app_name)
        output_path = "./dist/win"
        # ディレクトリが存在しない場合は作成
        if not os.path.exists(output_path): os.makedirs(output_path)
        result = subprocess.run("pyinstaller --windowed --distpath={} --onefile --noconsole --name afu-windows.exe ./src/main.py --collect-data tkinterdnd2 --collect-data simpleaudio -y".format(output_path), shell=True)
    else:
        app_name = "{}-mac".format(app_name)
        output_path = "./dist/mac"
        # ディレクトリが存在しない場合は作成
        if not os.path.exists(output_path): os.makedirs(output_path)
        result = subprocess.run(["pyinstaller --windowed --distpath={} --onefile --noconsole --name afu-macos ./src/main.py --collect-data tkinterdnd2 --collect-data simpleaudio -y".format(output_path)], shell=True)

    if (result.returncode != 0):
        print("** build error **")
        sys.exit()

    print("** clean up the directory **")
    is_file = os.path.isfile("{}.spec".format(app_name))
    if is_file: os.remove("{}.spec".format(app_name))

    is_dir = os.path.isdir("./build")
    if is_dir: shutil.rmtree('./build')
