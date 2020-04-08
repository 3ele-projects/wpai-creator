# flask_web/app.py
from datetime import datetime
from flask import Flask
from flask import jsonify
app = Flask(__name__)
import os
import requests
import shutil
from shutil import make_archive
from zipfile import ZipFile 
import urllib.request, json 
    #get download files
from flask import request
def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        print (save_path)
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

def create_instance(id, setup,root_path):
   

    print (root_path)
    os.chdir(root_path)
    path = str(id)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        shutil.rmtree(path, ignore_errors=True)

        os.mkdir(path)


    else:
        print ("Successfully created the directory %s " % path)
    path = os.getcwd()+'/'+str(id)
    os.chdir(path)
    instance_path = os.getcwd()
    url = "https://de.wordpress.org/latest-de_DE.zip"
    download_url(url, path+ '/wp.zip', chunk_size=128)
    unzip(path+ '/wp.zip')
    os.remove(path+ '/wp.zip')

    path = instance_path+'/wordpress/wp-content/plugins'
    os.chdir(path)

    os.remove(path+'/hello.php')
    shutil.rmtree(path+'/akismet/', ignore_errors=True)
    for plugin in setup['plugins']:
        url = plugin['download_url']
        zip_file = path+'/'+plugin['path']+'.zip'
        download_url(url,zip_file, chunk_size=128)
        unzip(zip_file)
        os.remove(zip_file)
        shutil.rmtree(zip_file, ignore_errors=True)

            
    path = instance_path+'/wordpress/wp-content/'
    os.chdir(path)  

    path = "mu-plugins"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    path = instance_path+'/wordpress/wp-content/mu-plugins'
    os.chdir(path)
    url = 'https://raw.githubusercontent.com/3ele-projects/mu-plugin-autoInstaller/master/eleAutomaticsInstaller.php'
    download_url(url, 'eleAutomaticsInstaller.php', chunk_size=128)
    change_setup_url_in_mu_plugin('eleAutomaticsInstaller.php', id)
    path = instance_path+'/wordpress/wp-content/themes'
    os.chdir(path)
    for theme in setup['themes']:
        url = theme['download_url']
        zip_file = path+'/'+theme['name']+'.zip'       
        download_url(url,zip_file, chunk_size=128)
        unzip(zip_file)
        os.remove(zip_file)
        shutil.rmtree(zip_file, ignore_errors=True)
    

def unzip(zip_file):
    try:
        with ZipFile(zip_file, 'r') as zipObj:
            zipObj.extractall()
    except (RuntimeError, TypeError, NameError):
        print ("unzip of the directory %s failed" % zip_file)
    else:
        print ("Successfully unzip the directory %s " % zip_file)
        pass
        
        


    






@app.route('/build/<id>', methods=['GET'])
def home(id):
    print (id) 
    data = {}
    root_path = os.getcwd()+'/wp'
    with urllib.request.urlopen("http://json.testing.threeelements.de/"+str(id)) as url:
        configdata = json.loads(url.read().decode())
        setup = configdata['setup']
        try:
            create_instance(id, setup, root_path)
        #     create_instance(24, setup, root_path)


        except (RuntimeError, TypeError, NameError) as e:
            print ("Creation of the WP Instance %s failed" % id)
            print (e)
            data['sucess'] = e
            pass
        else:
            print ("Successfully created the WP Instance %s " % id)
            os.chdir(root_path+'/'+str(id))
            shutil.make_archive('wordpress', 'zip','wordpress')  
            

            filesize = os.path.getsize(root_path+'/'+str(id)+'/wordpress.zip')

            
            now = datetime.now()

            data['sucess'] = True


        data['id'] = id
        data['size'] = filesize
        data['create_date'] = str(now)
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
