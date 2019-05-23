import os
import base64
import json
import random
import requests
import asyncio
from typing import Dict
from concurrent.futures import ProcessPoolExecutor
from aiohttp import web

from .worker import getImagesInfo, addVotes, getResults, PIC_LIMIT

class SiteHandler:
    def __init__(self) -> None:
        pass
        
    async def index(self, request: web.Request) -> web.Response:
        images = getImagesInfo(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img'))	

        resp_txt = '<meta charset=utf-8>' \
                   '<form action="/addVotes" method="post" accept-charset="utf-8" enctype="multipart/form-data">' \
                   '<table name="nm" border="1">'
	
        img_counter = 0		
        for img_id in images:
            img_path = images[img_id]['pic_path']
			
            resp_txt += '<tr>' \
			            '<td><img width=200px src="' + img_path + '"/></td>' \
			            '<td>'
			
            for vote_ind in range(0, PIC_LIMIT):
                resp_txt += '<input name="%d|%d" type="checkbox" autocomplete="off">vote_%d<br />' % (img_id, vote_ind, vote_ind) 
				
            resp_txt += '<input name="%d|wrong" type="checkbox" autocomplete="off">wrong_pic<br />' % (img_id) 
				
            resp_txt += '</td>'

        resp_txt += '</tr></table>'
        resp_txt += '<input style="width: 200px; height: 30px;" type="submit" value="Отправить" /><br>'
        resp_txt += '</form>'	
		
        r = web.Response(text=resp_txt)
        r.headers['content-type'] = 'text/html'
        r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        
        return r

    async def addVotes(self, request: web.Request) -> web.Response:
        data = await request.post()
	
        votes = {} 

        for v in data:
            pic_id = v.split('|')[0]
            pic_vote = v.split('|')[1]			
			
            if pic_id in votes:
                votes[pic_id].append(pic_vote)				
            else:			
                votes[pic_id] = [pic_vote]
			
        addVotes(votes)
		
        headers = {'Content-Type': 'application/json'}		
        data: Dict[str, str] = {} 	
    
        raise web.HTTPFound('/')
        
    async def results(self, request: web.Request) -> web.Response:
        print('results')		
		
        images = getResults()	
		
        print(images)
	
        resp_txt = '<meta charset=utf-8>' \
                   '<div>' \
				   '<table border="1">' \
				   
        img_counter = 0		
        for img_id in images:
            img_id_str = str(img_id)			
            img_path = images[img_id]['pic_path']
			
            img_counter_str = str(img_counter)
			
            resp_txt += '<tr>' \
			            '<td><img width=200px src="' + img_path + '"/></td>' \
			            '<td>'
			
            for vote_ind in range(0, PIC_LIMIT):
                resp_txt += '<input type="checkbox" autocomplete="off" disabled ' + ('checked' if images[img_id]['vote_%d_marked' % (vote_ind)] == True else 'unchecked') + '>vote_%d<br />' % (vote_ind) 
				
            resp_txt += '<input type="checkbox" autocomplete="off" disabled ' + ('checked' if images[img_id]['wrong_pic_marked'] == True else 'unchecked') + '>wrong_pic</td></tr>'			
		    	
        resp_txt += '</table></div>'
		
        r = web.Response(text=resp_txt)
        r.headers['content-type'] = 'text/html'
        r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        
        return r