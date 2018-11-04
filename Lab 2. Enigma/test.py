from machine import EnigmaMachine

if __name__ == "__main__":
    machine = EnigmaMachine(
       rotors='II IV V',
       reflector='B',
       ring_settings=[1, 20, 11],
       plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

    machine.set_display('WXC')

    msg_key = machine.process_text('KCH')
    machine.set_display(msg_key)

    ciphertext = 'NIBLFMYMLLUFWCASCSSNVHAZ'
    plaintext = machine.process_text(ciphertext)

    print(plaintext)
    machine.set_display(msg_key)
    print(machine.process_text(plaintext))
