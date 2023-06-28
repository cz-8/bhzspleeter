from multiprocessing import freeze_support
from spleeter.separator import Separator
import os
def spleet_stems(selec,*cfg):
	config_list = []
	
	if selec == 1:
		for arg in cfg:
			config_list.append(arg)

		print(config_list)
		class separator_jobs(Separator):

			def close_pool(self):
				if self._pool:
					self._pool.close()
					self._pool.terminate()
		separator = separator_jobs(f"spleeter:{config_list[0]}stems")

		separator.separate_to_file(f'{config_list[3]}',
								destination=f'{config_list[4]}',
	                            bitrate=config_list[1],
	                            codec=config_list[2])

		# Wait for batch to finish and terminate pool
		separator.join()
		separator.close_pool()

		with open(f"{os.getcwd()}/finishedtoken.token", 'w+') as config_file:
			config_file.write("1")
		with open(f"{os.getcwd()}/finishedtoken1.token", 'w+') as config_file:
			config_file.write("1")

	if selec == 0:
		for arg in cfg:
			config_list.append(arg)

		
		class separator_jobs(Separator):

			def close_pool(self):
				if self._pool:
					self._pool.close()
					self._pool.terminate()
		separator = separator_jobs(f"{config_list[0]}")

		separator.separate_to_file(f'{config_list[1]}',
								destination=f'{config_list[2]}',)

		# Wait for batch to finish and terminate pool
		separator.join()
		separator.close_pool()

		with open(f"{os.getcwd()}/finishedtoken.token", 'w+') as config_file:
			config_file.write("1")
		with open(f"{os.getcwd()}/finishedtoken1.token", 'w+') as config_file:
			config_file.write("1")

if __name__ == "__main__":
	pass