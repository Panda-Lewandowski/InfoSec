from machine import EnigmaMachine, EnigmaError
import sys
import base64

if __name__ == "__main__":
   machine = EnigmaMachine(
      rotors='II IV V',
      reflector='B',
      ring_settings=[1, 20, 11],
      plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

   if sys.argv[1] != '-s':
      raise EnigmaError("Invalid command!")
   else:
      msg_key = sys.argv[2]

   machine.set_display(msg_key)

   mode = sys.argv[3]

   with open(sys.argv[4], 'rb') as file:
      if mode == '-e':
         plaintext = base64.b32encode(file.read()).decode("ascii")
         ciphertext = machine.process_text(plaintext)
         
         with open(sys.argv[4].split('.')[0] + ".encoded", 'wb') as cipherfile:
            cipherfile.write(base64.b32decode(ciphertext))

      elif mode == '-d':
         ciphertext = base64.b32encode(file.read()).decode("ascii")
         plaintext = machine.process_text(ciphertext)

         with open(sys.argv[4].split('.')[0] + ".decoded", 'wb') as file:
            file.write(base64.b32decode(plaintext))
