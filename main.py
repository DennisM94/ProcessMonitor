import psutil
import datetime
from tabulate import tabulate
import os
import time

def get_processes():
	procs = []
	for p in psutil.process_iter():
		with p.oneshot():
			pid = p.pid
			if pid == 0:
				#SYSTEM IDLE PROCESS
				continue
			name = p.name()
			try:
				create_time = datetime.datetime.fromtimestamp(p.create_time())
			except OSError:
				create_time = datetime.datetime.fromtimestamp(psutil.boot_time())

			cpu_usage = p.cpu_percent()
			try:
				cup_affinity = len(p.cpu_affinity())
				# LISTE aus verwendeten Kernen

			except psutil.AccessDenied:
				cpu_affinity = 0

			try:
				memory = p.memory_full_info().uss
			except psutil.AccessDenied:
				memory = 0

			try:
				user = p.username()
			except psutil.AccessDenied:
				user = "N/A"


			status = p.status()
		procs.append({"Pid": pid, "Name":name, "create_time": create_time, "cpu_usage": cpu_usage, "status": status, "memory:":get_size(memory), "user":user})
	return procs

def print_processes(ps):
	print(tabulate(ps, headers="keys", tablefmt="github"))

def get_size(bytes):
	for i in ["", "K", "M", "T", "P", "E"]:
		if bytes < 1024:
			return f"{bytes:2f}{i}B"
		bytes /= 1024

procs = get_processes()
while True:
	print_processes(procs)
	time.sleep(1)
	procs = get_processes()
	if "nt" in os.name:
		os.system("cls")
	else:
		os.system("clear")
