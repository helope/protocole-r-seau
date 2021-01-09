import radio
import microbit
from microbit import sleep

radio.on()

crypt = False
chan = False
key = "IY546G6ZAubNFiua4zhef78p4afeaZRG"

class Msg:
    def __init__(self):
        self.msg = ""
        self.type = ""

def parse(msg):
    l = len(msg) - 1
    print("length: ", l)
    i = 0
    parse_msg = Msg()
    while i <= l:
        print("i", i)
        if i < 3:
            parse_msg.type += msg[i]
        if i  >= 3:
            parse_msg.msg += msg[i]
        i += 1
    return parse_msg

def reverse(msg, i):
    translated = ''
    while i >= 0:
        translated = translated + msg[i]
        i = i - 1
    return translated

def cipher_key(msg, key):
    result = ""
    key_tmp = str(key)
    while len(key) < len(msg):
        key_tmp = str(key_tmp) + str(key)

    key2 = ''
    for i in range(len(msg)):
        key2 += key_tmp[i]

    bin_msg = map(bin,bytearray(msg))
    bin_key = map(bin,bytearray(key2))
    bin_key = list(bin_key)
    i = 0
    for bit_msg in list(bin_msg):
        bit_msg = int(bit_msg)
        bit_key = int(bin_key[i])
        tmp = bit_msg ^ bit_key
        result += chr(tmp)
        i += 1
    return result

def encrypt(msg):
    i =  len(msg) - 1
    msg = reverse(msg, i)
    msg = cipher_key(msg, key)
    return msg

def decrypt(msg):
    i =  len(msg) - 1
    msg = cipher_key(msg, key)
    msg = reverse(msg, i)
    return msg
    
def send(msg):
    radio.send_bytes(msg)
    
def send_key(key):
    radio.send_value("key",key)

while True:
    if microbit.button_a.is_pressed():
        send_msg="key"+key
        radio.send(send_msg)
    receivedMsg = radio.receive()
    if receivedMsg:
        p_msg = parse(receivedMsg)
        if p_msg.type == "key":
            microbit.display.scroll("Key Ok", wait=False, loop=False)
            msg = encrypt("10")
            send_msg="chan"+msg
            radio.send(send_msg)
            microbit.display.scroll("Send", wait=False, loop=False)
        if p_msg.type == "chan":
            msg = decrypt(p_msg.msg)
            radio.config(channel=10)
            microbit.display.scroll("Channel OK", wait=False, loop=False)
