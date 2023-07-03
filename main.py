# import libraries
from bit import Key
import random
import requests
import multiprocessing
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
with open("dormant_address.txt", 'r') as file:
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

def main():
    num_cores = multiprocessing.cpu_count()
    iter_per_seconds = int(50000 * num_cores)
    random_number = random.randint(51650883406386744564, 66408278665354385868)
    random_range = range(random_number, random_number + iter_per_seconds)
    pool = multiprocessing.Pool(processes=num_cores)
    results = pool.map(my_function, random_range)


# Looping the process for eternity :)
if __name__ == '__main__':
    multiprocessing.freeze_support()
    while True:
        main()
        
# from eth_account import Account       
# hex = format(key_value, '064x')
# btc_address = Key.from_hex(hex).address
# eth_address = Account.from_key("0x" + hex).address

# print("BTC & ETH Hex Private Key :", hex)
# print("ETH Address :", eth_address)
# print("BTC Address :", btc_address)