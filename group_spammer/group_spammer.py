import requests
import time
from dialogs import Menu, Option
import dialogs
import json

token = open("token.txt", "r").read()
channels_url = "https://discord.com/api/v9/users/@me/channels"

headers = {
	"Authorization" : token
}

def rate_limit(js):
	if js['message'] == 'You are being rate limited.':
		sleep_time = js['retry_after']
		print(f"Sleeping for {sleep_time}s (Ctrl + C) to exit.")
		time.sleep(sleep_time)

def create_group(users):
	resp = requests.post(channels_url, headers=headers, json={
			"recipients" : users
		})
	return resp

def leave_group(channel_id):
	url = f"https://discord.com/api/v9/channels/{channel_id}"
	resp = requests.delete(url, headers=headers)
	return resp

def kick_user(channel_id, user_id):
	url = f"https://discord.com/api/v9/channels/{channel_id}/recipients/{user_id}"
	resp = requests.delete(url, headers=headers)
	return resp

loop_counter = 10
delay = 500

def manage_channel(channel_id, users_json):
	
	# kick users
	for user in users_json:
		if user['kick']:
			resp = kick_user(channel_id, user['id'])

			if resp.status_code != 200 and resp.status_code != 204:
				return resp

			time.sleep(1)

	# leave group
	resp = leave_group(channel_id)

	if resp.status_code != 200 and resp.status_code != 204:
		return resp

	return None

def run(caller):
	
	for loop in range(loop_counter):
		users_json = json.loads(open("users.json", "r").read())

		resp = create_group([x['id'] for x in users_json])

		if resp.status_code == 200:
			print("Creating group -> success")
			channel_id = resp.json()['id']

			time.sleep(delay/float(1000))

			resp2 = manage_channel(channel_id, users_json)
			
			if resp2 is None:
				print("Managing channel -> success")

			else:
				print("Managing channel -> error: " + resp2.text)
				rate_limit(resp2.json())

		else:
			print("Creating group -> error: " + resp.text)
			rate_limit(resp.json())

		if loop != loop_counter - 1: time.sleep(delay/float(1000))

	caller.print()
	caller.get_input()

def loop_count(caller):
	try:
		count = int(input("Type your loop count\n > "))
		global loop_counter
		loop_counter = count
		print(f"\nSetting loop count to {count}\n")
	
	except ValueError:
		print("\nInvalid number\n")

	caller.print()
	caller.get_input()

def set_delay(caller):
	
	try:
		count = int(input("Type your delay (ms)\n > "))
		global delay
		delay = count
		print(f"\nSetting delay to {count}\n")
	
	except ValueError:
		print("\nInvalid number\n")

	caller.print()
	caller.get_input()

def main():
	dialogs.enable_colors()

	menu = Menu(help=False)
	menu.add_option(Option("Set loop count", "", loop_count, color="blue"))
	menu.add_option(Option("Set delay", "", set_delay, color="red"))
	menu.add_option(Option("Run", "", run, color="underline;yellow"))
	menu.print()
	menu.get_input()

if __name__ == "__main__":
	main()
