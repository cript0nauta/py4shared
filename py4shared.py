#-*- coding: utf-8 -*-

""" 4shared downloader
Descarga ficheros de 4shared """

import os
import sys
import json
import requests
from urllib import urlencode
from time import sleep
from urlparse import urlsplit, urljoin
from getpass import getpass
from pyquery import PyQuery as P

class FourSharedSession(object):
    def __init__(self, email, password):
        """ Se deben indicar los datos del usuario para poder descargar
        ficheros """
        self.session = requests.Session()
        post_data = urlencode(dict(
            login = email,
            password = password))
        self.session.get('http://www.4shared.com/')
        headers = {"Content-Type" : \
                "application/x-www-form-urlencoded; charset=UTF-8"}
        login = self.session.post('http://www.4shared.com/web/login/validate',
                post_data, headers = headers)
        data = json.loads(login.text)
        if not data['success']:
            # Error de login
            print data['errorMessage']
            raise ValueError
        
        # Una vez validado, hacemos el login para que nos den cookies
        data = urlencode(dict(
            login = email,
            password = password,
            returnTo = 'http://www.4shared.com/',
            remember = 'false'))
        self.session.post('http://www.4shared.com/web/login', data, 
                headers = headers)

    def url_descarga(self, url):
        """ Devuelve la URL a la que apunta el botón Descargar de la 
        url argumento """
        splitresult = urlsplit(url)
        path = splitresult.path
        split = path.split('/')
        split[1] = 'get'
        path = '/'.join(split)
        return 'http://www.4shared.com' + path

    def get_filename(self, url):
        """ Retorna el nombre del fichero subido a partir de una URL
        DE DESCARGA DIRECTA"""
        path = urlsplit(url).path
        return os.path.basename(path)

    def download_link(self, url, dirname = './'):
        """ Retorna el link de descarga a el fichero de la URL """
        self.session.get(url) # Necesario para que no nos redirija
        url = self.url_descarga(url)
        page = self.session.get(url).text

        pyquery = P(page)
        delay = pyquery('#downloadDelayTimeSec').text()
        link = pyquery('#baseDownloadLink').val()
        fileid = pyquery('#fileId').val()

        limit = self.session.get('http://www.4shared.com/web/d2/getFreeDownloadLimitInfo?fileId=' + fileid).text
        limit = json.loads(limit)
        if not(limit['status'] == 'ok' or limit['traffic']['exceeded'] == 'none'):
            print limit
            raise ValueError('Ha superado el límite de descargas')

        print 'Esperando', delay, 'segundos'
        sleep(float(delay))

        print link
        filename = dirname + self.get_filename(link)
        print 'Guardando en', filename
        with open(filename,'w') as f:
            r = self.session.get(link, stream = True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)

if __name__ == '__main__':
    email, pwd = raw_input('Email: '), getpass('Password: ')
    if len(sys.argv) != 2:
       print "Especifique como argumento el link a la descarga"
       exit()
    s = FourSharedSession(email, pwd)
    link = sys.argv[1]
    s.download_link(link)
