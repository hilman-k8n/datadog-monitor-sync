from datadog import initialize, api
import time, json

class DatadogMonitor:
	def initialize(config):
		initialize(**config)
	
	def get_all_monitors():
		return(api.Monitor.get_all())

	def create_monitor(json_monitor):
		# Create single monitor from json
		if type(json_monitor) is dict:
			# check required field to create a monitor
			monitor = {}
			if 'name' not in json_monitor:
				raise KeyError('name is required')
			if 'query' not in json_monitor:
				raise KeyError('query is required!')
			if 'type' not in json_monitor:
				raise KeyError('type is required!')
			if 'message' not in json_monitor:
				raise KeyError('message is required!')
		
			monitor['name'] = json_monitor['name']
			monitor['query'] = json_monitor['query']
			monitor['message'] = json_monitor['message']
			monitor['type'] = json_monitor['type']
			if 'tags' in json_monitor:
				monitor['tags'] = json_monitor['tags']
			if 'options' in json_monitor:
				monitor['options'] = json_monitor['options']

			try:
				result = api.Monitor.create(**monitor)

				print('Monitor created')
				print('{} - {}'.format(result['id'], result['name']))
				print('https://app.datadoghq.com/monitors/{} - {}'.format(result['id'], result['name']))

			except:
				raise KeyError('Error! Failed to create monitor: {}'.format(i['name']))

		# Create multiple monitors from list of json monitor
		elif type(json_monitor) is list:

			# loop to create monitor
			for i in json_monitor:
				monitor = {}
				if 'name' not in i:
					raise KeyError('name is required')
				if 'query' not in i:
					raise KeyError('query is required!')
				if 'type' not in i:
					raise KeyError('type is required!')
				if 'message' not in i:
					raise KeyError('message is required!')
			
				monitor['name'] = i['name']
				monitor['query'] = i['query']
				monitor['message'] = i['message']
				monitor['type'] = i['type']
				if 'tags' in i:
					monitor['tags'] = i['tags']
				if 'options' in i:
					monitor['options'] = i['options']

				try:
					result = api.Monitor.create(**monitor)
					print('Monitor created: https://app.datadoghq.com/monitors/{} - {}'.format(result['id'], result['name']))
					
				except:
					raise KeyError('Error! Failed to create monitor: {}'.format(i['name']))
		else:
			raise Exception('not valid .monitor file format')
			
	def update_monitor(json_monitor):
		# Update a single monitor from a json
		if type(json_monitor) is dict:
			# Update multiple monitors from list of json
			monitor = {}
			if 'name' not in json_monitor:
				raise KeyError('name is required')
			if 'query' not in json_monitor:
				raise KeyError('query is required!')
			if 'type' not in json_monitor:
				raise KeyError('type is required!')
			if 'message' not in json_monitor:
				raise KeyError('message is required!')
		
			monitor['name'] = json_monitor['name']
			monitor['query'] = json_monitor['query']
			monitor['message'] = json_monitor['message']
			monitor['type'] = json_monitor['type']
			if 'tags' in json_monitor:
				monitor['tags'] = json_monitor['tags']
			if 'options' in json_monitor:
				monitor['options'] = json_monitor['options']

			try:
				result = api.Monitor.update(json_monitor['id'], **monitor)
				
			except:
				raise KeyError('Error')

			# get last 5 minutes time in epoch and current time in epoch (in miliseconds)
			now = time.time() + 1
			last_5m = now - 5*60
			now = int(now * 1000)
			last_5m = int(last_5m * 1000)

			if 'errors' not in result:
				print('Monitor updated')
				print('{} - {}'.format(result['id'], result['name']))
				print('https://app.datadoghq.com/event/stream?query=tags%3Aaudit%2Cmonitor_id%3A{}%20modified&from_ts={}&to_ts={}\n'.format(json_monitor['id'], last_5m, now))
			else:
				raise Exception('Failed to update {}'.format(json_monitor['id']))
	

		elif type(json_monitor) is list:
			for item in json_monitor:
				monitor = {}
				if 'name' not in item:
					raise KeyError('name is required')
				if 'query' not in item:
					raise KeyError('query is required!')
				if 'type' not in item:
					raise KeyError('type is required!')
				if 'message' not in item:
					raise KeyError('message is required!')

				monitor['name'] = item['name']
				monitor['query'] = item['query']
				monitor['message'] = item['message']
				monitor['type'] = item['type']
				if 'tags' in item:
					monitor['tags'] = item['tags']
				if 'options' in item:
					monitor['options'] = item['options']

				try:
					result = api.Monitor.update(item['id'], **monitor)
					
				except:
					raise KeyError('Error')

				# get last 5 minutes time in epoch and current time in epoch (in miliseconds)
				now = time.time() + 1
				last_5m = now - 5*60
				now = int(now * 1000)
				last_5m = int(last_5m * 1000)
				
				if 'errors' not in result:
					print('Monitor updated')
					print('{} - {}'.format(result['id'], result['name']))
					print('https://app.datadoghq.com/event/stream?query=tags%3Aaudit%2Cmonitor_id%3A{}%20modified&from_ts={}&to_ts={}\n'.format(item['id'], last_5m, now))
				else:
					raise Exception('Failed to update {}'.format(json_monitor['id']))
		
	
		else:
			raise Exception('not valid json format')
