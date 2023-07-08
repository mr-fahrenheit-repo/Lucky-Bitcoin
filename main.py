# import libraries
from bit import Key
import random
import requests
import multiprocessing
from eth_account import Account
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

# Loading up the text file for found list
def write_to_file(file_path, new_string):
    with open(file_path, "a") as file:
        file.write(new_string + "\n")

# Function for generate Bitcoin Hex, convert it into Bitcoin Address and seek it on text file
def my_function(key_value):
    hex = format(key_value, '064x')
    private_key = Key.from_hex(hex)
    btc_address = private_key.address
    eth_address = Account.from_key("0x" + hex).address
    btc_index = file_text.find(str(btc_address))
    eth_index = file_text.find(str(eth_address))
    if btc_index != -1:
        write_to_file("found.txt", str(f"{hex} , {btc_address} === > BTC Type"))
        try:
            telegram_send(f"FOUND!!!\nPrivate Key : {hex}\nBitcoin Address : {btc_address}")
        except:
            pass
        else:
            pass
    if eth_index != -1:
        write_to_file("found.txt", str(f"{'0x' + hex} , {eth_address} === > ETH Type"))
        try:
            telegram_send(f"FOUND!!!\nPrivate Key : {'0x' + hex}\nEthereum Address : {eth_address}")
        except:
            pass
        else:
            pass

# Split the range into 10 
def range_10():
    list_rangers = []
    start = 38211389448314344489778425052867009591436396212094718446259703836700993293138
    for x in range(10):
        end = 3821138944831434448977842505286700959143639621209471844625970383670099329313
        ranges = (start, start + end)
        start += end + 1 
        list_rangers.append(ranges)
    return list_rangers

# Multiprocessing Main Function
def main(start,end):
    num_cores = multiprocessing.cpu_count()
    iter_per_seconds = int(50000 * num_cores)
    random_number = random.randint(start, end)
    random_range = range(random_number, random_number + iter_per_seconds)
    pool = multiprocessing.Pool(processes=num_cores)
    results = pool.map(my_function, random_range)


# Looping the process for eternity :)
if __name__ == '__main__':
    multiprocessing.freeze_support()
    while True:
        range_list = range_10()
        for numb in range_list:
            main(numb[0],numb[1])