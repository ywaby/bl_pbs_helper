import zipfile
import os
import shutil
import glob
from pytk import BaseNode

class dev_install(BaseNode):
    """ln src and templete"""
    def action(self):
        src = os.path.abspath("src")
        target = os.path.expanduser(
            "~/.config/blender/2.80/scripts/addons/pbs_helper")
        if os.path.exists(target):
            os.remove(target)
        os.symlink(src, target)

        src = os.path.abspath("./templete")
        target = os.path.expanduser("~/.config//blender/2.80/scripts/startup/bl_app_templates_user/texture_generate_templete")
        if os.path.exists(target):
            os.remove(target)
        os.symlink(src, target)

        src = os.path.abspath("./presets/pbs_helper")
        target = os.path.expanduser("~/.config//blender/2.80/scripts/presets/pbs_helper")
        if os.path.exists(target):
            os.remove(target)
        os.symlink(src, target)        

class clear(BaseNode):
    '''clear dist'''
    def action(self):
        shutil.copytree('~/.config/blender/2.80/scripts/presets/pbs_helper/bake_type', './presets/pbs_helper/preset')

class package(BaseNode):
    """package prject to release file (zip)"""
    
    def checker(self):
        clear().run()
        return True

    def action(self):
        # pack src
        files = glob.glob("./src/**/*.py", recursive=True)
        files.append("./src/data.blend")
        with zipfile.ZipFile('pbs_helper_addon.zip', 'w', zipfile.ZIP_DEFLATED) as tzip:
            for f in files:
                tzip.write(f)
            tzip.close()
        if not os.path.exists("./dist/pbs_helper"):
            os.makedirs("./dist/pbs_helper")
        shutil.move("pbs_helper_addon.zip", "dist/pbs_helper/pbs_helper_addon.zip")

        # pack templete
        files = glob.glob("./templete/*.*", recursive=False)
        with zipfile.ZipFile('texture_generate_templete.zip', 'w', zipfile.ZIP_DEFLATED) as tzip:
            for f in files:
                tzip.write(f)
            tzip.close()
        shutil.move("texture_generate_templete.zip", "dist/pbs_helper/texture_generate_templete.zip")
        shutil.copyfile('./install.py','./dist/pbs_helper/install.py') # install.py
        shutil.copytree('./presets', './dist/pbs_helper/presets') # preset
        # package all
        os.chdir('./dist') 
        files = glob.glob("./pbs_helper/**", recursive=True)
        with zipfile.ZipFile('pbs_helper.zip', 'w', zipfile.ZIP_DEFLATED) as tzip: #TODO cd dist
            for f in files:
                tzip.write(f)
            tzip.close()
        #shutil.rmtree("./pbs_helper") # remove code for test install