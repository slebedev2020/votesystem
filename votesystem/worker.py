import os
from random import randrange
from typing import Dict
from filehash import FileHash

import sqlite3 

DB_PATH = 'votesystem/db/votes.db'

PIC_LIMIT = 10
RESULTS_MARKED_COUNT = 2

def initDB():
	conn = sqlite3.connect(DB_PATH)
	conn.execute('create table if not exists pictures (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ' \
				                                      'pic_hash varchar(250), ' \
				                                      'pic_path varchar(250), ' \
				                                      'UNIQUE(pic_hash, pic_path))')
	
	conn.execute('create table if not exists votes (id INTEGER NOT NULL, ' \
				                                   'user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ' \
				                                   'vote_0 INTEGER NOT NULL, ' \
				                                   'vote_1 INTEGER NOT NULL, ' \
	                                               'vote_2 INTEGER NOT NULL, ' \
	                                               'vote_3 INTEGER NOT NULL, ' \
	                                               'vote_4 INTEGER NOT NULL, ' \
	                                               'vote_5 INTEGER NOT NULL, ' \
	                                               'vote_6 INTEGER NOT NULL, ' \
	                                               'vote_7 INTEGER NOT NULL, ' \
				 			                       'vote_8 INTEGER NOT NULL, ' \
				 			                       'vote_9 INTEGER NOT NULL, ' \
				                                   'wrong_pic INTEGER NOT NULL, ' \
												   'FOREIGN KEY (id) REFERENCES pictures(id))')
	
	conn.commit()
	conn.close()

def getImagesInfo(img_dir) -> Dict[int, Dict[str, str]]:
	img_fnames = os.listdir(img_dir)
	
	images_info : Dict[int, Dict[str, str]] = {}

	conn = sqlite3.connect(DB_PATH)	
		
	counter = 0
	for fname in img_fnames:
		print(fname)
		try:
			img_path = os.path.join(img_dir, fname)
			pic_path = '/'.join((img_dir.split('/')[-1], fname))
			pic_hash = FileHash('md5').hash_file(img_path)
			
			cursor = conn.cursor()
			
			cursor.execute('insert or ignore into pictures (pic_hash, pic_path) values (?, ?)', (pic_hash, pic_path))
					
			conn.commit()
			cursor.close()
			
		except Exception as exc:
			print(str(exc))
			pass
		
		
	cursor = conn.cursor()
	
	cursor.execute('SELECT pictures.*, COUNT(user_id) AS vote_count FROM pictures LEFT JOIN votes ON pictures.id = votes.id GROUP BY pictures.id ORDER BY vote_count LIMIT ' + str(PIC_LIMIT))
	
	rows = cursor.fetchall()
	
	for row in rows:
		images_info[row[0]] = {'pic_hash' : row[1], 'pic_path' : row[2]}
	
	print(images_info)	
			
	conn.close()
	
	return images_info

def getResults() -> Dict[int, Dict[str, str]]:
	print('getResults')
	
	images_info : Dict[int, Dict[str, str]] = {}

	conn = sqlite3.connect(DB_PATH)	
	
	cursor = conn.cursor()
	
	cursor.execute('SELECT pictures.*, ' \
					'SUM(votes.vote_0) AS vote_0_count, ' \
					'SUM(votes.vote_1) AS vote_1_count, ' \
					'SUM(votes.vote_2) AS vote_2_count, ' \
					'SUM(votes.vote_3) AS vote_3_count, ' \
					'SUM(votes.vote_4) AS vote_4_count, ' \
					'SUM(votes.vote_5) AS vote_5_count, ' \
					'SUM(votes.vote_6) AS vote_6_count, ' \
					'SUM(votes.vote_7) AS vote_7_count, ' \
					'SUM(votes.vote_8) AS vote_8_count, ' \
					'SUM(votes.vote_9) AS vote_9_count, ' \
					'SUM(votes.wrong_pic) AS wrong_pic_count ' \
					'FROM pictures LEFT JOIN votes ON pictures.id = votes.id GROUP BY pictures.id')
	
	rows = cursor.fetchall()
	
	for row in rows:
		images_info[row[0]] = {'pic_hash' : row[1], 'pic_path' : row[2], \
								'vote_0_marked' : row[3] > RESULTS_MARKED_COUNT, \
								'vote_1_marked' : row[4] > RESULTS_MARKED_COUNT, \
								'vote_2_marked' : row[5] > RESULTS_MARKED_COUNT, \
								'vote_3_marked' : row[6] > RESULTS_MARKED_COUNT, \
								'vote_4_marked' : row[7] > RESULTS_MARKED_COUNT, \
								'vote_5_marked' : row[8] > RESULTS_MARKED_COUNT, \
							  	'vote_6_marked' : row[9] > RESULTS_MARKED_COUNT, \
							   	'vote_7_marked' : row[10] > RESULTS_MARKED_COUNT, \
							  	'vote_8_marked' : row[11] > RESULTS_MARKED_COUNT, \
							   	'vote_9_marked' : row[12] > RESULTS_MARKED_COUNT, \
								'wrong_pic_marked' : row[13] > RESULTS_MARKED_COUNT
							}
		
	print(images_info)	
				
	conn.close()
	
	return images_info

def addVotes(votes) -> None:
	print('sendAllVotes')
	print(votes)
	
	conn = sqlite3.connect(DB_PATH)		

	for pic_id in votes:
		conn.execute('insert into votes (id, vote_0, vote_1, vote_2, vote_3, vote_4, vote_5, vote_6, vote_7, vote_8, vote_9, wrong_pic) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
				   (pic_id, \
					'0' in votes[pic_id], \
					'1' in votes[pic_id], \
					'2' in votes[pic_id], \
					'3' in votes[pic_id], \
					'4' in votes[pic_id], \
					'5' in votes[pic_id], \
					'6' in votes[pic_id], \
					'7' in votes[pic_id], \
					'8' in votes[pic_id], \
					'9' in votes[pic_id], \
					'wrong' in votes[pic_id]))		
		
		conn.commit()
		
	conn.close()
