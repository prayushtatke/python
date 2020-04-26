#!/usr/local/bin/python3
from ftplib import FTP
import re
from sortedcontainers import SortedList
from datetime import datetime
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from config import *


def to_datetime(ts_str, PATTERN):
	if (not ts_str) or (not PATTERN):
		return None

	return datetime.strptime(ts_str, PATTERN)

def datetime_tostr(dt, PATTERN):
	if (not dt) or (not PATTERN):
		return None
	return dt.strftime(PATTERN)

class FileInfo:
	def __init__(self, filename, file_attr, file_name_pat=None, file_name_ts_pat='%Y%m%d%H%M%S', file_mod_ts_pat='%Y%m%d%H%M%S'):
		self.file_name = filename
		self.file_size = file_attr.get('size')
		self.file_type = file_attr.get('type')
		self.file_mod_ts_str = file_attr.get('modify')
		self.file_mod_ts = to_datetime(self.file_mod_ts_str, file_mod_ts_pat )
		self.file_name_ts_str = self.__fetch_filename_ts(self.file_name, file_name_pat)
		self.file_name_ts = to_datetime(self.file_name_ts_str, file_name_ts_pat)


	def __fetch_filename_ts(self, filename, file_name_pattern):
		if filename == "." or filename == ".." or file_name_pattern is None:
			return None

		match = re.search(file_name_pattern, filename)
		if not match:
			print('match is none for:', filename)
			return None

		return match.group(1)

	def __str__(self):
		return f'Name:{self.file_name}, ModificationTS: {self.file_mod_ts_str}, Size: {self.file_size}'


def get_last_stored_ts():
	try:
		with open(LOCAL_TS_FILE, 'r') as ltf:
			ts_str = str(ltf.read()).strip()
			last_ts = to_datetime(ts_str, FILE_DATE_PATTERN)
			print('Last Timestamp Stored: ', last_ts)
			return last_ts
	except Exception:
		return None

def set_last_stored_ts(ts):
	print('Storing last timestamp: ', ts )
	ts_str = datetime_tostr(ts, FILE_DATE_PATTERN)
	try:
		with open(LOCAL_TS_FILE, 'w') as ltf:
			ltf.write(ts_str)
	except Exception:
		pass


def filter_by_time(fileinfo, ts_from, ts_to=None, use_filename_ts=False):

	file_time = fileinfo.file_name_ts if use_filename_ts or USE_FILENAME_TS else fileinfo.file_mod_ts

	# when last ts is not provided, include all files
	if not ts_from:
		return fileinfo

	if ts_to:
		if file_time and file_time > ts_from and file_time < ts_to:
			return fileinfo
	else:
		if file_time and file_time > ts_from:
			return fileinfo

	return None

def get_ftp_client(host=None, user=None, passwd=None):
	ftp = FTP(host,user, passwd)
	# ftp.login(user, passwd)
	return ftp


def find_files_to_dwnld(fetch_nmin=False, last_nmin=None):
	if fetch_nmin:
		last_ntime = datetime.now() - timedelta(minutes=LAST_NMINUTES)
	else:
		last_stored_ts = get_last_stored_ts()

	ftp = get_ftp_client(FTP_HOST, FTP_USER, FTP_PASSWD)
	sl = SortedList(key=lambda fi: fi.file_name_ts if USE_FILENAME_TS else fi.file_mod_ts)
	print('Fetching List from FTP Server')
	# mlsd = list(ftp.mlsd(FTP_DIR))
	# print('total files to be scaned:', len(mlsd))
	# for fn, fct in mlsd:

	# gen = ( FileInfo(fn, fattr, FILE_PATTERN, FILE_DATE_PATTERN, FILE_DATE_PATTERN) for fn, fattr in ftp.mlsd(FTP_DIR))
	# for fi in gen:
	for fn, fattr in ftp.mlsd(FTP_DIR):
		print (fn, fattr)
		fi = FileInfo(fn, fattr, FILE_PATTERN, FILE_DATE_PATTERN, FILE_DATE_PATTERN)
		if fetch_nmin:
			fi = filter_by_time(fi, last_ntime, use_filename_ts=USE_FILENAME_TS)
		else:
		    fi = filter_by_time(fi, last_stored_ts, use_filename_ts=USE_FILENAME_TS)

		if fi:
			print(fn, fattr)
			sl.add(fi)

	ftp.quit()
	return sl


def create_file_group(files, num_threads):
	file_grp = [[] for i in range(num_threads)]
	it = iter(file_grp)
	for fi in files:
		try:
			next(it).append(fi)
		except StopIteration:
			it = iter(file_grp)
			next(it).append(fi)

	return file_grp


# This Method will work as Thread
def download_files(files=[], download_path=".", threadname=''):
	print(f'Starting Thread {threadname}, files to download: {len(files)}')
	ftp = get_ftp_client(FTP_HOST, FTP_USER, FTP_PASSWD)
	dwnlded_files = []
	failed_files = []
	for fi in files:
		try:
			download_file(fi.file_name, download_path, ftp)
			dwnlded_files.append(fi)
		except:
			failed_files.append(fi)

	ftp.quit()
	return dwnlded_files, failed_files


def download_file(file, download_path, ftp_client):
	print('downloading...: ', file)
	# with open(download_path +'/'+file, 'wb') as fp:
	# 	ftp_client.retrbinary('RETR '+ FTP_DIR+'/'+file, fp.write)


def main():
	files = find_files_to_dwnld(FETCH_NMIN, LAST_NMINUTES)
	if not files:
		print ('No files to download.')
		return

	print('Number Of Files:',len(files))
	num_files = len(files)
	num_threads = num_files if num_files < MAX_CONNECTIONS else MAX_CONNECTIONS
	files_grp = create_file_group(files, num_threads)

	succ_dwnld = SortedList(key=lambda fi: fi.file_name_ts if USE_FILENAME_TS else fi.file_mod_ts)
	failed_dwnld = SortedList(key=lambda fi: fi.file_name_ts if USE_FILENAME_TS else fi.file_mod_ts)
	futures = []
	with ThreadPoolExecutor(max_workers=num_threads) as executor:
		for i in range(num_threads):
			fut = executor.submit(download_files, files_grp[i], LOCAL_CUST_DIR, threadname=str(i))
			futures.append(fut)

	for fut in futures:
		suc, fail = fut.result()
		succ_dwnld.update(suc)
		failed_dwnld.update(fail)

	print(f'Successful Downloads: {len(succ_dwnld)}, Failed_download: {len(failed_dwnld)}.')
	# store last timestamp only if FETCH_NMIN is set to false
	if not FETCH_NMIN:
		ts = succ_dwnld[-1].file_name_ts if USE_FILENAME_TS else succ_dwnld[-1].file_mod_ts
		set_last_stored_ts(ts)


# ------- MAIN -------- #
if __name__ == '__main__':
	main()
