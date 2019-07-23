#!/usr/bin/env python3

import json, sys, argparse, os
from DatadogMonitor import DatadogMonitor
import JenkinsMonitorsParser

def sync_monitor(args):
	if args['datadog_monitors_root'] is None:
		print('\n--datadog-monitors-root is not defined')
		exit(0)

	all_monitors = JenkinsMonitorsParser.get_all_monitors(args['datadog_monitors_root'])
	DatadogMonitor.update_monitor(all_monitors)

def main_program():
	parser = argparse.ArgumentParser(description='Datadog Monitor Tools')
	subparsers = parser.add_subparsers()

	parser_sync = subparsers.add_parser('sync', help='sync monitor from local to datadog (used by Jenkins)')	
	parser_sync.add_argument('--datadog-monitors-root', help='directory to root of .monitor file')
	parser_sync.add_argument('--api-key', default='', help='datadog API key')
	parser_sync.add_argument('--app-key', default='', help='datadog APP key')
	parser_sync.set_defaults(func=sync_monitor)
	
	# create the parser for create command
	parser_deploy = subparsers.add_parser('deploy', help='create a monitor from a json file')	
	parser_deploy.add_argument('json_monitor_file', type=str, help='json formated monitor')
	parser_deploy.add_argument('--api-key', default='', help='datadog API key')
	parser_deploy.add_argument('--app-key', default='', help='datadog APP key')
	parser_deploy.set_defaults(func=deploy_monitor)

	# parse argument
	args = parser.parse_args()
	
	# Check if valid arguments
	arguments = vars(args)

	if arguments:
		if arguments['api_key'] == '':
			try:
				arguments['api_key'] = os.environ['DATADOG_API_KEY']
			except:
				print('\n--api-key is not defined\n')
				exit(1)

		if arguments['app_key'] == '':
			try:
				arguments['app_key'] = os.environ['DATADOG_APP_KEY']
			except:
				print('\n--app-key is not defined\n')
				exit(1)

		try:		
			DatadogMonitor.initialize(arguments)
		except Exception:
			raise('Invalid datadog app/api key')
		
		args.func(arguments)
	
	else:
		print_help()


def print_help():
	print('\n\nUsage: {} -h\n'.format(sys.argv[0]))
	
# Deploy Monitor
def deploy_monitor(args):
	result = {}
	json_monitor = {}
	with open(args['json_monitor_file']) as f:
		json_monitor = json.load(f)

	for i in json_monitor:
		if 'id' not in i:
			DatadogMonitor.create_monitor(i)
		else:
			DatadogMonitor.update_monitor(i)

if __name__ == '__main__':
	main_program()