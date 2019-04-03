import zipfile
import os
import shutil
import glob
from pytk import BaseNode

class package(BaseNode):
    """package prject to release file (zip)"""

    def action(self):
        srcs = glob.glob("./bitmap2tex/**/*.py", recursive=True)
        srcs.append("./bitmap2tex/bitmap2tex_startup.blend")
        with zipfile.ZipFile('bitmap2tex.zip', 'w', zipfile.ZIP_DEFLATED) as tzip:
            for src in srcs:
                tzip.write(src)
            tzip.close()
        if not os.path.exists("./dist"):
            os.mkdir("./dist")
        shutil.move("bitmap2tex.zip", "dist/bitmap2tex.zip")
