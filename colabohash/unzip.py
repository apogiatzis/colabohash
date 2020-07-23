import zipfile
import platform
import os.path as path
import os
import stat

def unzip_chromediver():
    base_dir = path.join(path.dirname(path.abspath(__file__)), "bin")

    os_type = platform.system()
    bin_path = path.join(base_dir, "chromedriver")

    if not path.isfile(bin_path):
        if os_type == "Windows":
            filename = "chromedriver_win32.zip"
        elif os_type == "Linux":
            filename = "chromedriver_linux64.zip"
        elif os_type == "Darwin":
            filename = "chromedriver_mac64.zip"    

        zip_path = path.join(base_dir, filename)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
        
        st = os.stat(bin_path)
        os.chmod(bin_path, st.st_mode | stat.S_IEXEC)

    return path.join(base_dir, "chromedriver")
    