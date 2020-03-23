import os
import requests
import shutil
from shutil import make_archive
from zipfile import ZipFile 
import urllib.request, json 
    #get download files

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def change_setup_url_in_mu_plugin(file, id):
    fp = open(file, "r+")
    contents = fp.read(os.path.getsize(file))
    newContent = contents.replace("http://json.testing.threeelements.de/data.json", "http://json.testing.threeelements.de/"+str(id))
    fp.seek(0)
    fp.truncate()
    fp.write(newContent)
    fp.close()

def create_instance(id, setup):
   

    print (os.getcwd())
    root_path = os.getcwd()+'/wp'
    os.chdir(root_path)
    path = str(id)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    path = os.getcwd()+'/'+str(id)
    os.chdir(path)
    root_path = os.getcwd()
    url = "https://de.wordpress.org/latest-de_DE.zip"
    download_url(url, path+ '/wp.zip', chunk_size=128)

    with ZipFile(path+ '/wp.zip', 'r') as zipObj:
    # Extract all the contents of zip file in current directory
        zipObj.extractall()
    os.remove(path+ '/wp.zip')

    path = root_path+'/wordpress/wp-content/plugins'
    os.chdir(path)

    os.remove(path+'/hello.php')
    shutil.rmtree(path+'/akismet/', ignore_errors=True)
    url = 'https://raw.githubusercontent.com/3ele-projects/eleAutomaticsAutoInstaller/master/eleAutomaticsInstaller.php'
    download_url(url, 'eleAutomaticsInstaller.php', chunk_size=128)
    for plugin in setup['plugins']:
        url = 'https://downloads.wordpress.org/plugin/'+plugin['path']+'.zip'
        target = path+'/'+plugin['path']+'.zip'
        download_url(url,target, chunk_size=128)
        with ZipFile(target, 'r') as zipObj:
            zipObj.extractall()
        os.remove(target)
        shutil.rmtree(target, ignore_errors=True)

            
    path = root_path+'/wordpress/wp-content/'
    print (path)
    os.chdir(path)  

    path = "mu-plugins"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    path = root_path+'/wordpress/wp-content/mu-plugins'
    os.chdir(path)
    url = 'https://raw.githubusercontent.com/3ele-projects/mu-plugin-autoInstaller/master/eleAutomaticsInstaller.php'
    download_url(url, 'eleAutomaticsInstaller.php', chunk_size=128)
    change_setup_url_in_mu_plugin('eleAutomaticsInstaller.php', id)
    path = root_path+'/wordpress/wp-content/themes'
    os.chdir(path)
    for theme in setup['themes']:
        url = 'https://downloads.wordpress.org/theme/'+theme['name']+'.zip'
        target = path+'/'+theme['name']+'.zip'
        download_url(url,target, chunk_size=128)
        with ZipFile(target, 'r') as zipObj:
            zipObj.extractall()
        os.remove(target)
        shutil.rmtree(target, ignore_errors=True)
    


if __name__ == "__main__":
    print ('start')
    
    root_path = os.getcwd()+'/wp'
    with urllib.request.urlopen("http://json.testing.threeelements.de/") as url:
        setups = json.loads(url.read().decode())
        for s in setups:
            with urllib.request.urlopen("http://json.testing.threeelements.de/"+str(s['id'])) as url:
                configdata = json.loads(url.read().decode())
                setup = configdata['setup']
            create_instance(s['id'], setup)
            os.chdir(root_path+'/'+str(s['id']))
            shutil.make_archive('wordpress', 'zip','wordpress')  
            os.chdir(root_path)      







