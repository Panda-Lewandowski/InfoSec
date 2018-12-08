if __name__ == '__main__':

    import os
    import time
    import sys

    import aes128
    
    way = sys.argv[1]

    input_path = sys.argv[2]
    if not os.path.isfile(input_path):
        print('The file you enter is not a file')
        exit()
    
    key = sys.argv[3]
    if len(key) > 16:
        print('Too long Key.')
        exit()
    for symbol in key:
        if ord(symbol) > 0xff:
            print('That key won\'t work. It must contain only latin alphabet and numbers')
            exit()
    
    print('\r\nPlease, wait...')

    time_before = time.time()

    # Input data
    with open(input_path, 'rb') as f:
        data = f.read()    

    if way == '-e':
        crypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                crypted_part = aes128.encrypt(temp, key)
                crypted_data.extend(crypted_part)
                del temp[:]
        else:
            #padding v1
            # crypted_data.extend(temp)

            # padding v2
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                crypted_part = aes128.encrypt(temp, key)
                crypted_data.extend(crypted_part)

        out_path = os.path.join(os.path.dirname(input_path) , os.path.basename(input_path).split('.')[0] + ".encoded")

        # Ounput data
        with open(out_path, 'wb') as ff:
            ff.write(bytes(crypted_data))

    elif way == '-d':
        decrypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                decrypted_part = aes128.decrypt(temp, key)
                decrypted_data.extend(decrypted_part)
                del temp[:] 
        else:
            #padding v1
            # decrypted_data.extend(temp)
            
            # padding v2
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                decrypted_part = aes128.encrypt(temp, key)
                decrypted_data.extend(crypted_part) 

        out_path = os.path.join(os.path.dirname(input_path) , os.path.basename(input_path).split('.')[0] + ".decoded")

        # Ounput data
        with open(out_path, 'wb') as ff:
            ff.write(bytes(decrypted_data))

    time_after = time.time()
    
print('New file here:', out_path, '--', time_after - time_before, ' seconds')
print('If smth wrong check the key you entered')