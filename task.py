import zipfile
import os
import shutil
import glob
from pytk import BaseNode
os.path.exists
class dev_uninstall(BaseNode):
    """remove src and templete link"""
    def action(self):
        src = os.path.abspath("./pbs_helper")
        dest = os.path.expanduser(
            "~/.config/blender/2.80/scripts/addons/pbs_helper")
        if os.path.exists(dest) or os.path.islink(dest):
            os.remove(dest)

        src = os.path.abspath("./templete")
        dest = os.path.expanduser("~/.config/blender/2.80/scripts/startup/bl_app_templates_user/bitmap2tex_templete")
        if os.path.exists(dest) or os.path.islink(dest):
            os.remove(dest)

        src = os.path.abspath("./presets/pbs_helper")
        dest = os.path.expanduser("~/.config/blender/2.80/scripts/presets/pbs_helper")
        if os.path.exists(dest) or os.path.islink(dest):
            os.remove(dest)

class dev_install(BaseNode):
    """ln src and templete"""
    def action(self):
        src = os.path.abspath("./pbs_helper")
        dest = os.path.expanduser(
            "~/.config/blender/2.80/scripts/addons/pbs_helper")
        if os.path.exists(dest) or os.path.islink(dest):
            os.remove(dest)
        os.symlink(src, dest)

        src = os.path.abspath("./bitmap2tex_templete")
        dest = os.path.expanduser("~/.config/blender/2.80/scripts/startup/bl_app_templates_user/bitmap2tex_templete")
        if os.path.exists(dest) or os.path.islink(dest):
            os.remove(dest)
        os.symlink(src, dest)

        src = os.path.abspath("./presets/pbs_helper")
        dest = os.path.expanduser("~/.config/blender/2.80/scripts/presets/pbs_helper")
        if os.path.exists(dest) or os.path.islink(dest):
            os.remove(dest)
        os.symlink(src, dest)        

class clear(BaseNode):
    '''clear dist'''
    def action(self):
        if os.path.exists('./dist'):
            shutil.rmtree('./dist')

class package(BaseNode):
    """package prject to release file (zip)"""
    
    def checker(self):
        clear().run()
        return True

    def action(self):
        if not os.path.exists("./dist/pbs_helper"):
            os.makedirs("./dist/pbs_helper")
        # pack src
        files = glob.glob("./pbs_helper/**/*.py", recursive=True)
        files.append("./pbs_helper/data.blend")
        with zipfile.ZipFile('pbs_helper_addon.zip', 'w', zipfile.ZIP_DEFLATED) as tzip:
            for f in files:
                tzip.write(f)
            tzip.close()
        shutil.move("pbs_helper_addon.zip", "dist/pbs_helper/pbs_helper_addon.zip")

        # pack templete
        files = glob.glob("./bitmap2tex_templete/*.*", recursive=False)
        with zipfile.ZipFile('bitmap2tex_templete.zip', 'w', zipfile.ZIP_DEFLATED) as tzip:
            for f in files:
                tzip.write(f)
            tzip.close()
        shutil.move("bitmap2tex_templete.zip", "dist/pbs_helper/bitmap2tex_templete.zip")
        shutil.copyfile('./install.py','./dist/pbs_helper/install.py') # install.py
        shutil.copyfile('./uninstall.py','./dist/pbs_helper/uninstall.py') # uninstall.py
        # preset
        shutil.copytree('./presets/pbs_helper', './dist/pbs_helper/presets/pbs_helper')
        # package all
        os.chdir('./dist') 
        files = glob.glob("./pbs_helper/**", recursive=True)
        with zipfile.ZipFile('pbs_helper.zip', 'w', zipfile.ZIP_DEFLATED) as tzip: #TODO cd dist
            for f in files:
                tzip.write(f)
            tzip.close()
        #shutil.rmtree("./pbs_helper")