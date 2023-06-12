# import libraries
from bit import Key
import random
import requests
import multiprocessing
from termcolor import colored, cprint
from dotenv import dotenv_values

# Importing variables for telegram bot
notif_vars = dotenv_values()

# Telegram function for notification
def telegram_send(chat):
  bot_token = notif_vars["telegram_api"]
  bot_chat_id = notif_vars["telegram_chat_id"]
  chat_message = 'https://api.telegram.org./bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id +'&text=' + chat # type: ignore
  response = requests.get(chat_message)
  return response.json()

# Loading up the text file containing address list
with open("dormant_address_new.txt", 'r') as file:
    file_text = file.read()

# Function for generate Bitcoin Hex, convert it into Bitcoin Address and seek it on text file
def my_function(key_value):
    hex = format(key_value, '064x')
    private_key = Key.from_hex(hex)
    bitcoin_address = private_key.address
    index = file_text.find(str(bitcoin_address))
    if index != -1:
        with open("found.txt", 'w') as file_found:
            file_found.write(f"{private_key} , {bitcoin_address}")
            file_found.close()
        try:
            telegram_send(f"FOUND!!!\nPrivate Key : {private_key}\nBitcoin Address : {bitcoin_address}")
        except:
            pass
        
# Starting Status
cprint('Searching...', 'red', attrs=['blink'])

# Looping the process for eternity :)  
while True:
    random_number = random.randint(1, 115792089237316195423570985008687907852837564279074904382605163141518161494360)
    random_range = range(random_number, random_number + 12000)
    num_cores = 4
    pool = multiprocessing.Pool(processes=num_cores)
    results = pool.map(my_function, random_range)

