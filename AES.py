import random
import copy
def hex2bin(hexa):
  return bin(int(hexa, 16))[2:].zfill(8)

def bin2hex(bina):
  return "{0:#0{1}x}".format(int(bina, 2),4)

def dec2bin(deci):
  return bin(deci)[2:].zfill(8)

def bin2dec(bina):
  return int(bina, 2)

def hex2dec(hexa):
  return int(hexa, 16)

def dec2hex(deci):
  return "{0:#0{1}x}".format(deci,4)

def XOR(a,b): # prend deux string binaires ou hexadécimales et retourne le résultat de l'opération XOR en binaire
  if a[0:2] == '0x':
    a = hex2bin(a)
  if b[0:2] == '0x':
    b = hex2bin(b)
  y = int(a, 2)^int(b,2)
  return bin(y)[2:].zfill(len(a))

# Définition des tables de mutliplications dans GF(2**8)
# Source des données: https://en.wikipedia.org/wiki/Rijndael_MixColumns

GFMult2Hex = [0x00,0x02,0x04,0x06,0x08,0x0a,0x0c,0x0e,0x10,0x12,0x14,0x16,0x18,0x1a,0x1c,0x1e,
              0x20,0x22,0x24,0x26,0x28,0x2a,0x2c,0x2e,0x30,0x32,0x34,0x36,0x38,0x3a,0x3c,0x3e,
              0x40,0x42,0x44,0x46,0x48,0x4a,0x4c,0x4e,0x50,0x52,0x54,0x56,0x58,0x5a,0x5c,0x5e,
              0x60,0x62,0x64,0x66,0x68,0x6a,0x6c,0x6e,0x70,0x72,0x74,0x76,0x78,0x7a,0x7c,0x7e,	
              0x80,0x82,0x84,0x86,0x88,0x8a,0x8c,0x8e,0x90,0x92,0x94,0x96,0x98,0x9a,0x9c,0x9e,
              0xa0,0xa2,0xa4,0xa6,0xa8,0xaa,0xac,0xae,0xb0,0xb2,0xb4,0xb6,0xb8,0xba,0xbc,0xbe,
              0xc0,0xc2,0xc4,0xc6,0xc8,0xca,0xcc,0xce,0xd0,0xd2,0xd4,0xd6,0xd8,0xda,0xdc,0xde,
              0xe0,0xe2,0xe4,0xe6,0xe8,0xea,0xec,0xee,0xf0,0xf2,0xf4,0xf6,0xf8,0xfa,0xfc,0xfe,
              0x1b,0x19,0x1f,0x1d,0x13,0x11,0x17,0x15,0x0b,0x09,0x0f,0x0d,0x03,0x01,0x07,0x05,
              0x3b,0x39,0x3f,0x3d,0x33,0x31,0x37,0x35,0x2b,0x29,0x2f,0x2d,0x23,0x21,0x27,0x25,
              0x5b,0x59,0x5f,0x5d,0x53,0x51,0x57,0x55,0x4b,0x49,0x4f,0x4d,0x43,0x41,0x47,0x45,
              0x7b,0x79,0x7f,0x7d,0x73,0x71,0x77,0x75,0x6b,0x69,0x6f,0x6d,0x63,0x61,0x67,0x65,
              0x9b,0x99,0x9f,0x9d,0x93,0x91,0x97,0x95,0x8b,0x89,0x8f,0x8d,0x83,0x81,0x87,0x85,
              0xbb,0xb9,0xbf,0xbd,0xb3,0xb1,0xb7,0xb5,0xab,0xa9,0xaf,0xad,0xa3,0xa1,0xa7,0xa5,
              0xdb,0xd9,0xdf,0xdd,0xd3,0xd1,0xd7,0xd5,0xcb,0xc9,0xcf,0xcd,0xc3,0xc1,0xc7,0xc5,
              0xfb,0xf9,0xff,0xfd,0xf3,0xf1,0xf7,0xf5,0xeb,0xe9,0xef,0xed,0xe3,0xe1,0xe7,0xe5]

GFMult3Hex = [0x00,0x03,0x06,0x05,0x0c,0x0f,0x0a,0x09,0x18,0x1b,0x1e,0x1d,0x14,0x17,0x12,0x11,
              0x30,0x33,0x36,0x35,0x3c,0x3f,0x3a,0x39,0x28,0x2b,0x2e,0x2d,0x24,0x27,0x22,0x21,
              0x60,0x63,0x66,0x65,0x6c,0x6f,0x6a,0x69,0x78,0x7b,0x7e,0x7d,0x74,0x77,0x72,0x71,
              0x50,0x53,0x56,0x55,0x5c,0x5f,0x5a,0x59,0x48,0x4b,0x4e,0x4d,0x44,0x47,0x42,0x41,
              0xc0,0xc3,0xc6,0xc5,0xcc,0xcf,0xca,0xc9,0xd8,0xdb,0xde,0xdd,0xd4,0xd7,0xd2,0xd1,
              0xf0,0xf3,0xf6,0xf5,0xfc,0xff,0xfa,0xf9,0xe8,0xeb,0xee,0xed,0xe4,0xe7,0xe2,0xe1,
              0xa0,0xa3,0xa6,0xa5,0xac,0xaf,0xaa,0xa9,0xb8,0xbb,0xbe,0xbd,0xb4,0xb7,0xb2,0xb1,
              0x90,0x93,0x96,0x95,0x9c,0x9f,0x9a,0x99,0x88,0x8b,0x8e,0x8d,0x84,0x87,0x82,0x81,	
              0x9b,0x98,0x9d,0x9e,0x97,0x94,0x91,0x92,0x83,0x80,0x85,0x86,0x8f,0x8c,0x89,0x8a,
              0xab,0xa8,0xad,0xae,0xa7,0xa4,0xa1,0xa2,0xb3,0xb0,0xb5,0xb6,0xbf,0xbc,0xb9,0xba,
              0xfb,0xf8,0xfd,0xfe,0xf7,0xf4,0xf1,0xf2,0xe3,0xe0,0xe5,0xe6,0xef,0xec,0xe9,0xea,	
              0xcb,0xc8,0xcd,0xce,0xc7,0xc4,0xc1,0xc2,0xd3,0xd0,0xd5,0xd6,0xdf,0xdc,0xd9,0xda,	
              0x5b,0x58,0x5d,0x5e,0x57,0x54,0x51,0x52,0x43,0x40,0x45,0x46,0x4f,0x4c,0x49,0x4a,
              0x6b,0x68,0x6d,0x6e,0x67,0x64,0x61,0x62,0x73,0x70,0x75,0x76,0x7f,0x7c,0x79,0x7a,	
              0x3b,0x38,0x3d,0x3e,0x37,0x34,0x31,0x32,0x23,0x20,0x25,0x26,0x2f,0x2c,0x29,0x2a,
              0x0b,0x08,0x0d,0x0e,0x07,0x04,0x01,0x02,0x13,0x10,0x15,0x16,0x1f,0x1c,0x19,0x1a]

GFMult9Hex = [0x00,0x09,0x12,0x1b,0x24,0x2d,0x36,0x3f,0x48,0x41,0x5a,0x53,0x6c,0x65,0x7e,0x77,
              0x90,0x99,0x82,0x8b,0xb4,0xbd,0xa6,0xaf,0xd8,0xd1,0xca,0xc3,0xfc,0xf5,0xee,0xe7,
              0x3b,0x32,0x29,0x20,0x1f,0x16,0x0d,0x04,0x73,0x7a,0x61,0x68,0x57,0x5e,0x45,0x4c,
              0xab,0xa2,0xb9,0xb0,0x8f,0x86,0x9d,0x94,0xe3,0xea,0xf1,0xf8,0xc7,0xce,0xd5,0xdc,
              0x76,0x7f,0x64,0x6d,0x52,0x5b,0x40,0x49,0x3e,0x37,0x2c,0x25,0x1a,0x13,0x08,0x01,
              0xe6,0xef,0xf4,0xfd,0xc2,0xcb,0xd0,0xd9,0xae,0xa7,0xbc,0xb5,0x8a,0x83,0x98,0x91,
              0x4d,0x44,0x5f,0x56,0x69,0x60,0x7b,0x72,0x05,0x0c,0x17,0x1e,0x21,0x28,0x33,0x3a,
              0xdd,0xd4,0xcf,0xc6,0xf9,0xf0,0xeb,0xe2,0x95,0x9c,0x87,0x8e,0xb1,0xb8,0xa3,0xaa,	
              0xec,0xe5,0xfe,0xf7,0xc8,0xc1,0xda,0xd3,0xa4,0xad,0xb6,0xbf,0x80,0x89,0x92,0x9b,	
              0x7c,0x75,0x6e,0x67,0x58,0x51,0x4a,0x43,0x34,0x3d,0x26,0x2f,0x10,0x19,0x02,0x0b,
              0xd7,0xde,0xc5,0xcc,0xf3,0xfa,0xe1,0xe8,0x9f,0x96,0x8d,0x84,0xbb,0xb2,0xa9,0xa0,
              0x47,0x4e,0x55,0x5c,0x63,0x6a,0x71,0x78,0x0f,0x06,0x1d,0x14,0x2b,0x22,0x39,0x30,
              0x9a,0x93,0x88,0x81,0xbe,0xb7,0xac,0xa5,0xd2,0xdb,0xc0,0xc9,0xf6,0xff,0xe4,0xed,
              0x0a,0x03,0x18,0x11,0x2e,0x27,0x3c,0x35,0x42,0x4b,0x50,0x59,0x66,0x6f,0x74,0x7d,	
              0xa1,0xa8,0xb3,0xba,0x85,0x8c,0x97,0x9e,0xe9,0xe0,0xfb,0xf2,0xcd,0xc4,0xdf,0xd6,
              0x31,0x38,0x23,0x2a,0x15,0x1c,0x07,0x0e,0x79,0x70,0x6b,0x62,0x5d,0x54,0x4f,0x46]

GFMult11Hex = [0x00,0x0b,0x16,0x1d,0x2c,0x27,0x3a,0x31,0x58,0x53,0x4e,0x45,0x74,0x7f,0x62,0x69,
              0xb0,0xbb,0xa6,0xad,0x9c,0x97,0x8a,0x81,0xe8,0xe3,0xfe,0xf5,0xc4,0xcf,0xd2,0xd9,
              0x7b,0x70,0x6d,0x66,0x57,0x5c,0x41,0x4a,0x23,0x28,0x35,0x3e,0x0f,0x04,0x19,0x12,
              0xcb,0xc0,0xdd,0xd6,0xe7,0xec,0xf1,0xfa,0x93,0x98,0x85,0x8e,0xbf,0xb4,0xa9,0xa2,
              0xf6,0xfd,0xe0,0xeb,0xda,0xd1,0xcc,0xc7,0xae,0xa5,0xb8,0xb3,0x82,0x89,0x94,0x9f,
              0x46,0x4d,0x50,0x5b,0x6a,0x61,0x7c,0x77,0x1e,0x15,0x08,0x03,0x32,0x39,0x24,0x2f,
              0x8d,0x86,0x9b,0x90,0xa1,0xaa,0xb7,0xbc,0xd5,0xde,0xc3,0xc8,0xf9,0xf2,0xef,0xe4,
              0x3d,0x36,0x2b,0x20,0x11,0x1a,0x07,0x0c,0x65,0x6e,0x73,0x78,0x49,0x42,0x5f,0x54,
              0xf7,0xfc,0xe1,0xea,0xdb,0xd0,0xcd,0xc6,0xaf,0xa4,0xb9,0xb2,0x83,0x88,0x95,0x9e,
              0x47,0x4c,0x51,0x5a,0x6b,0x60,0x7d,0x76,0x1f,0x14,0x09,0x02,0x33,0x38,0x25,0x2e,
              0x8c,0x87,0x9a,0x91,0xa0,0xab,0xb6,0xbd,0xd4,0xdf,0xc2,0xc9,0xf8,0xf3,0xee,0xe5,
              0x3c,0x37,0x2a,0x21,0x10,0x1b,0x06,0x0d,0x64,0x6f,0x72,0x79,0x48,0x43,0x5e,0x55,
              0x01,0x0a,0x17,0x1c,0x2d,0x26,0x3b,0x30,0x59,0x52,0x4f,0x44,0x75,0x7e,0x63,0x68,
              0xb1,0xba,0xa7,0xac,0x9d,0x96,0x8b,0x80,0xe9,0xe2,0xff,0xf4,0xc5,0xce,0xd3,0xd8,
              0x7a,0x71,0x6c,0x67,0x56,0x5d,0x40,0x4b,0x22,0x29,0x34,0x3f,0x0e,0x05,0x18,0x13,
              0xca,0xc1,0xdc,0xd7,0xe6,0xed,0xf0,0xfb,0x92,0x99,0x84,0x8f,0xbe,0xb5,0xa8,0xa3]

GFMult13Hex = [0x00,0x0d,0x1a,0x17,0x34,0x39,0x2e,0x23,0x68,0x65,0x72,0x7f,0x5c,0x51,0x46,0x4b,
              0xd0,0xdd,0xca,0xc7,0xe4,0xe9,0xfe,0xf3,0xb8,0xb5,0xa2,0xaf,0x8c,0x81,0x96,0x9b,
              0xbb,0xb6,0xa1,0xac,0x8f,0x82,0x95,0x98,0xd3,0xde,0xc9,0xc4,0xe7,0xea,0xfd,0xf0,
              0x6b,0x66,0x71,0x7c,0x5f,0x52,0x45,0x48,0x03,0x0e,0x19,0x14,0x37,0x3a,0x2d,0x20,
              0x6d,0x60,0x77,0x7a,0x59,0x54,0x43,0x4e,0x05,0x08,0x1f,0x12,0x31,0x3c,0x2b,0x26,
              0xbd,0xb0,0xa7,0xaa,0x89,0x84,0x93,0x9e,0xd5,0xd8,0xcf,0xc2,0xe1,0xec,0xfb,0xf6,
              0xd6,0xdb,0xcc,0xc1,0xe2,0xef,0xf8,0xf5,0xbe,0xb3,0xa4,0xa9,0x8a,0x87,0x90,0x9d,
              0x06,0x0b,0x1c,0x11,0x32,0x3f,0x28,0x25,0x6e,0x63,0x74,0x79,0x5a,0x57,0x40,0x4d,
              0xda,0xd7,0xc0,0xcd,0xee,0xe3,0xf4,0xf9,0xb2,0xbf,0xa8,0xa5,0x86,0x8b,0x9c,0x91,
              0x0a,0x07,0x10,0x1d,0x3e,0x33,0x24,0x29,0x62,0x6f,0x78,0x75,0x56,0x5b,0x4c,0x41,
              0x61,0x6c,0x7b,0x76,0x55,0x58,0x4f,0x42,0x09,0x04,0x13,0x1e,0x3d,0x30,0x27,0x2a,
              0xb1,0xbc,0xab,0xa6,0x85,0x88,0x9f,0x92,0xd9,0xd4,0xc3,0xce,0xed,0xe0,0xf7,0xfa,
              0xb7,0xba,0xad,0xa0,0x83,0x8e,0x99,0x94,0xdf,0xd2,0xc5,0xc8,0xeb,0xe6,0xf1,0xfc,
              0x67,0x6a,0x7d,0x70,0x53,0x5e,0x49,0x44,0x0f,0x02,0x15,0x18,0x3b,0x36,0x21,0x2c,
              0x0c,0x01,0x16,0x1b,0x38,0x35,0x22,0x2f,0x64,0x69,0x7e,0x73,0x50,0x5d,0x4a,0x47,
              0xdc,0xd1,0xc6,0xcb,0xe8,0xe5,0xf2,0xff,0xb4,0xb9,0xae,0xa3,0x80,0x8d,0x9a,0x97]

GFMult14Hex = [0x00,0x0e,0x1c,0x12,0x38,0x36,0x24,0x2a,0x70,0x7e,0x6c,0x62,0x48,0x46,0x54,0x5a,
              0xe0,0xee,0xfc,0xf2,0xd8,0xd6,0xc4,0xca,0x90,0x9e,0x8c,0x82,0xa8,0xa6,0xb4,0xba,
              0xdb,0xd5,0xc7,0xc9,0xe3,0xed,0xff,0xf1,0xab,0xa5,0xb7,0xb9,0x93,0x9d,0x8f,0x81,
              0x3b,0x35,0x27,0x29,0x03,0x0d,0x1f,0x11,0x4b,0x45,0x57,0x59,0x73,0x7d,0x6f,0x61,
              0xad,0xa3,0xb1,0xbf,0x95,0x9b,0x89,0x87,0xdd,0xd3,0xc1,0xcf,0xe5,0xeb,0xf9,0xf7,
              0x4d,0x43,0x51,0x5f,0x75,0x7b,0x69,0x67,0x3d,0x33,0x21,0x2f,0x05,0x0b,0x19,0x17,
              0x76,0x78,0x6a,0x64,0x4e,0x40,0x52,0x5c,0x06,0x08,0x1a,0x14,0x3e,0x30,0x22,0x2c,
              0x96,0x98,0x8a,0x84,0xae,0xa0,0xb2,0xbc,0xe6,0xe8,0xfa,0xf4,0xde,0xd0,0xc2,0xcc,
              0x41,0x4f,0x5d,0x53,0x79,0x77,0x65,0x6b,0x31,0x3f,0x2d,0x23,0x09,0x07,0x15,0x1b,
              0xa1,0xaf,0xbd,0xb3,0x99,0x97,0x85,0x8b,0xd1,0xdf,0xcd,0xc3,0xe9,0xe7,0xf5,0xfb,
              0x9a,0x94,0x86,0x88,0xa2,0xac,0xbe,0xb0,0xea,0xe4,0xf6,0xf8,0xd2,0xdc,0xce,0xc0,
              0x7a,0x74,0x66,0x68,0x42,0x4c,0x5e,0x50,0x0a,0x04,0x16,0x18,0x32,0x3c,0x2e,0x20,
              0xec,0xe2,0xf0,0xfe,0xd4,0xda,0xc8,0xc6,0x9c,0x92,0x80,0x8e,0xa4,0xaa,0xb8,0xb6,
              0x0c,0x02,0x10,0x1e,0x34,0x3a,0x28,0x26,0x7c,0x72,0x60,0x6e,0x44,0x4a,0x58,0x56,
              0x37,0x39,0x2b,0x25,0x0f,0x01,0x13,0x1d,0x47,0x49,0x5b,0x55,0x7f,0x71,0x63,0x6d,
              0xd7,0xd9,0xcb,0xc5,0xef,0xe1,0xf3,0xfd,0xa7,0xa9,0xbb,0xb5,0x9f,0x91,0x83,0x8d]

GFMult2Bin = []
for elem in GFMult2Hex:
  GFMult2Bin.append(bin(elem)[2:].zfill(8))
GFMult3Bin = []
for elem in GFMult3Hex:
  GFMult3Bin.append(bin(elem)[2:].zfill(8))
GFMult9Bin = []
for elem in GFMult9Hex:
  GFMult9Bin.append(bin(elem)[2:].zfill(8))
GFMult11Bin = []
for elem in GFMult11Hex:
  GFMult11Bin.append(bin(elem)[2:].zfill(8))
GFMult13Bin = []
for elem in GFMult13Hex:
  GFMult13Bin.append(bin(elem)[2:].zfill(8))
GFMult14Bin = []
for elem in GFMult14Hex:
  GFMult14Bin.append(bin(elem)[2:].zfill(8))

def hexString2Block(string): # prend une string de 32 caractères hexadécimaux (16 octets) et retourne le bloc correspondant en hexadécimal
  Hex = [[[] for j in range(4)] for i in range(4)]
  for j in range(0,4):
    for i in range(0,4):
      Hex[i][j] = '0x'+ string[2*i+8*j:2*i+8*j+2]
  return Hex

def block2HexString(block): # prend un bloc en hexadécimal et retourne la string de 32 caractères hexadécimaux (16 octets) correspondante
  string = ''
  for j in range(0,4):
    for i in range(0,4):
      if len(block[i][j]) == 3:
        string = string + '0' + block[i][j][2:]
      else:
        string = string + block[i][j][2:]
  return string

def printB(block): # prend un bloc quelconque et affiche son contenu sous la forme matricielle
  for i in range(0,4):
    print(block[i])

def printS(block): # prend un bloc en hexadécimal et affiche son contenu sous la forme d'une string hexadécimale composée de mots de quatre octets
  string = ''
  for j in range(0,4):
    for i in range(0,4):
      if len(block[i][j]) == 3:
        string = string + '0' + block[i][j][2:]
      else:
        string = string + block[i][j][2:]
    string = string + ' '
  print(string)

def hexBlockXOR(block1,block2): # prend deux blocs en binaire et retourne le résultat (sous la forme hexadécimale) de l'opération XOR
                                # des deux blocs, exécutée entrée par entrée
  hexed = copy.deepcopy(block1)
  for i in range(0,4):
    for j in range(0,4):
      hexed[i][j] = bin2hex(XOR(block1[i][j],block2[i][j]))
  return hexed

def bin2hexaBlock(block): # prend un bloc en binaire et le retourne sous forme hexacédimale
  hexBlock = copy.deepcopy(block)
  for i in range(len(block)):
    for j in range(len(block[i])):
      hexBlock[i][j]= bin2hex(block[i][j])
  return hexBlock

def hex2binBlock(block): # prend un bloc en hexadécimale et le retourne sous forme binaire
  binaryBlock = copy.deepcopy(block)
  for i in range(len(block)):
    for j in range(len(block[i])):
      binaryBlock[i][j]= hex2bin(block[i][j])
  return binaryBlock

def words2Block(string): # prend une string hexadécimale composée de mots de quatre octets et retourne le bloc correspondant en hexadécimale
  Hex = [[[] for j in range(4)] for i in range(4)]
  for j in range(0,4):
    for i in range(0,4):
      Hex[i][j] = '0x'+ string[2*i+9*j:2*i+9*j+2]
  return Hex

def block2Words(block): # prend un bloc en hexadécimale et retourne la string hexadécimale correspondante composée de mots de quatre octets 
  string = ''
  for j in range(0,4):
    for i in range(0,4):
      if len(block[i][j]) == 3:
        string = string + '0' + block[i][j][2:]
      else:
        string = string + block[i][j][2:]
    if j < 3:  
      string = string + ' '
  return string

rcon = [['0x01', '0x00', '0x00', '0x00'],
        ['0x02', '0x00', '0x00', '0x00'],
        ['0x04', '0x00', '0x00', '0x00'],
        ['0x08', '0x00', '0x00', '0x00'],
        ['0x10', '0x00', '0x00', '0x00'],
        ['0x20', '0x00', '0x00', '0x00'],
        ['0x40', '0x00', '0x00', '0x00'],
        ['0x80', '0x00', '0x00', '0x00'],
        ['0x1b', '0x00', '0x00', '0x00'],
        ['0x36', '0x00', '0x00', '0x00']]

def RotWord(word): # prend un vecteur de dimension 4 et retourne le vecteur résultant de l'opération RotWord telle que décrite ci-dessus
  rotated = copy.deepcopy(word)
  for i in range(0,4):
    rotated[i] = word[(i+1)%4]
  return rotated

def SubWord(word): # prend un vecteur de dimension 4 et retourne le vecteur résultant de l'opération SubWord telle que décrite ci-dessus
  subbed = copy.deepcopy(word)
  for i in range(0,4):
    subbed[i] = Sbox[int(word[i],2)] 
  return subbed

def KeyExpansion(key): # prend une clé de type AES-128, AES-192 ou AES-256 (sous la forme d'une string hexadécimale) et retourne la clé étendue correspondante
                       # sous la forme d'une liste de mots en hexadécimale, de 4 octes chacun
  N = int((len(key))/8)
  K = []
  for i in range(0,N):
    temp = []
    for j in range(0,4):
      temp.append('0x' + key[i*8+2*j:i*8+2*(j+1)])
    K.append(temp)

  if N == 4:
    R = 11
  elif N == 6:
    R = 13
  elif N == 8:
    R = 15
  
  W = []
  for i in range(0,4*R):
    if i < N:
      tot = []
      for j in range(0,4):
        tot.append(hex2bin(K[i][j]))
      W.append(tot)
    elif i >= N and i%N == 0:
      mod = SubWord(RotWord(W[i-1]))
      tot = []
      for j in range(0,4):
        tot.append(XOR(XOR(W[i-N][j],mod[j]), rcon[int(i/N)-1][j]))
      W.append(tot)
    elif i >= N and N > 6 and  i%N == 4:
      mod = SubWord(W[i-1])
      tot = []
      for j in range(0,4):
        tot.append(XOR(W[i-N][j],mod[j]))
      W.append(tot)
    else:
      tot = []
      for j in range(0,4):
        tot.append(XOR(W[i-N][j],W[i-1][j]))
      W.append(tot)

  return W

def AddRoundKey(roundKey, block): # Prends deux blocs de 16 octets et retourne le résultat de l'addition XOR, bits par bits, 
                                  # entrée par entrée, sous la convention que le premier bloc est donné en column major
  cypher = copy.deepcopy(block)
  for i in range(0,4):
    for j in range(0,4):
      cypher[i][j] = XOR(roundKey[j][i],block[i][j]) # L'inversion de i et j dans roundKey est la bonne selon la convention column major utilisée par AES
  return cypher

  # Rijndael S-Box
# Source des données: https://en.wikipedia.org/wiki/Rijndael_S-box

tempSbox = [0x63,	0x7c,	0x77,	0x7b,	0xf2,	0x6b,	0x6f,	0xc5,	0x30,	0x01,	0x67,	0x2b,	0xfe,	0xd7,	0xab,	0x76,
	0xca,	0x82,	0xc9,	0x7d,	0xfa,	0x59,	0x47,	0xf0,	0xad,	0xd4,	0xa2,	0xaf,	0x9c,	0xa4,	0x72,	0xc0,
	0xb7,	0xfd,	0x93,	0x26,	0x36,	0x3f,	0xf7,	0xcc,	0x34,	0xa5,	0xe5,	0xf1,	0x71,	0xd8,	0x31,	0x15,
	0x04,	0xc7,	0x23,	0xc3,	0x18,	0x96,	0x05,	0x9a,	0x07,	0x12,	0x80,	0xe2,	0xeb,	0x27,	0xb2,	0x75,
	0x09,	0x83,	0x2c,	0x1a,	0x1b,	0x6e,	0x5a,	0xa0,	0x52,	0x3b,	0xd6,	0xb3,	0x29,	0xe3,	0x2f,	0x84,
	0x53,	0xd1,	0x00,	0xed,	0x20,	0xfc,	0xb1,	0x5b,	0x6a,	0xcb,	0xbe,	0x39,	0x4a,	0x4c,	0x58,	0xcf,
	0xd0,	0xef,	0xaa,	0xfb,	0x43,	0x4d,	0x33,	0x85,	0x45,	0xf9,	0x02,	0x7f,	0x50,	0x3c,	0x9f,	0xa8,
	0x51,	0xa3,	0x40,	0x8f,	0x92,	0x9d,	0x38,	0xf5,	0xbc,	0xb6,	0xda,	0x21,	0x10,	0xff,	0xf3,	0xd2,
	0xcd,	0x0c,	0x13,	0xec,	0x5f,	0x97,	0x44,	0x17,	0xc4,	0xa7,	0x7e,	0x3d,	0x64,	0x5d,	0x19,	0x73,
	0x60,	0x81,	0x4f,	0xdc,	0x22,	0x2a,	0x90,	0x88,	0x46,	0xee,	0xb8,	0x14,	0xde,	0x5e,	0x0b,	0xdb,
	0xe0,	0x32,	0x3a,	0x0a,	0x49,	0x06,	0x24,	0x5c,	0xc2,	0xd3,	0xac,	0x62,	0x91,	0x95,	0xe4,	0x79,
	0xe7,	0xc8,	0x37,	0x6d,	0x8d,	0xd5,	0x4e,	0xa9,	0x6c,	0x56,	0xf4,	0xea,	0x65,	0x7a,	0xae,	0x08,
	0xba,	0x78,	0x25,	0x2e,	0x1c,	0xa6,	0xb4,	0xc6,	0xe8,	0xdd,	0x74,	0x1f,	0x4b,	0xbd,	0x8b,	0x8a,
	0x70,	0x3e,	0xb5,	0x66,	0x48,	0x03,	0xf6,	0x0e,	0x61,	0x35,	0x57,	0xb9,	0x86,	0xc1,	0x1d,	0x9e,
	0xe1,	0xf8,	0x98,	0x11,	0x69,	0xd9,	0x8e,	0x94,	0x9b,	0x1e,	0x87,	0xe9,	0xce,	0x55,	0x28,	0xdf,
	0x8c,	0xa1,	0x89,	0x0d,	0xbf,	0xe6,	0x42,	0x68,	0x41,	0x99,	0x2d,	0x0f,	0xb0,	0x54,	0xbb,	0x16]
Sbox = []
for elem in tempSbox:
  Sbox.append(bin(elem)[2:].zfill(8))

tempInvSbox = [0x52,	0x09,	0x6a,	0xd5,	0x30,	0x36,	0xa5,	0x38,	0xbf,	0x40,	0xa3,	0x9e,	0x81,	0xf3,	0xd7,	0xfb,
0x7c,	0xe3,	0x39,	0x82,	0x9b,	0x2f,	0xff,	0x87,	0x34,	0x8e,	0x43,	0x44,	0xc4,	0xde,	0xe9,	0xcb,
0x54,	0x7b,	0x94,	0x32,	0xa6,	0xc2,	0x23,	0x3d,	0xee,	0x4c,	0x95,	0x0b,	0x42,	0xfa,	0xc3,	0x4e,
0x08,	0x2e,	0xa1,	0x66,	0x28,	0xd9,	0x24,	0xb2,	0x76,	0x5b,	0xa2,	0x49,	0x6d,	0x8b,	0xd1,	0x25,
0x72,	0xf8,	0xf6,	0x64,	0x86,	0x68,	0x98,	0x16,	0xd4,	0xa4,	0x5c,	0xcc,	0x5d,	0x65,	0xb6,	0x92,
0x6c,	0x70,	0x48,	0x50,	0xfd,	0xed,	0xb9,	0xda,	0x5e,	0x15,	0x46,	0x57,	0xa7,	0x8d,	0x9d,	0x84,
0x90,	0xd8,	0xab,	0x00,	0x8c,	0xbc,	0xd3,	0x0a,	0xf7,	0xe4,	0x58,	0x05,	0xb8,	0xb3,	0x45,	0x06,
0xd0,	0x2c,	0x1e,	0x8f,	0xca,	0x3f,	0x0f,	0x02,	0xc1,	0xaf,	0xbd,	0x03,	0x01,	0x13,	0x8a,	0x6b,
0x3a,	0x91,	0x11,	0x41,	0x4f,	0x67,	0xdc,	0xea,	0x97,	0xf2,	0xcf,	0xce,	0xf0,	0xb4,	0xe6,	0x73,
0x96,	0xac,	0x74,	0x22,	0xe7,	0xad,	0x35,	0x85,	0xe2,	0xf9,	0x37,	0xe8,	0x1c,	0x75,	0xdf,	0x6e,
0x47,	0xf1,	0x1a,	0x71,	0x1d,	0x29,	0xc5,	0x89,	0x6f,	0xb7,	0x62,	0x0e,	0xaa,	0x18,	0xbe,	0x1b,
0xfc,	0x56,	0x3e,	0x4b,	0xc6,	0xd2,	0x79,	0x20,	0x9a,	0xdb,	0xc0,	0xfe,	0x78,	0xcd,	0x5a,	0xf4,
0x1f,	0xdd,	0xa8,	0x33,	0x88,	0x07,	0xc7,	0x31,	0xb1,	0x12,	0x10,	0x59,	0x27,	0x80,	0xec,	0x5f,
0x60,	0x51,	0x7f,	0xa9,	0x19,	0xb5,	0x4a,	0x0d,	0x2d,	0xe5,	0x7a,	0x9f,	0x93,	0xc9,	0x9c,	0xef,
0xa0,	0xe0,	0x3b,	0x4d,	0xae,	0x2a,	0xf5,	0xb0,	0xc8,	0xeb,	0xbb,	0x3c,	0x83,	0x53,	0x99,	0x61,
0x17,	0x2b,	0x04,	0x7e,	0xba,	0x77,	0xd6,	0x26,	0xe1,	0x69,	0x14,	0x63,	0x55,	0x21,	0x0c,	0x7d]
InvSbox = []
for elem in tempInvSbox:
  InvSbox.append(bin(elem)[2:].zfill(8))

def SubBytes(block): # prend un bloc en forme binaire et retourne le résultat en binaire de l'opération SubBytes
  subbed = copy.deepcopy(block)
  for i in range(0,4):
    for j in range(0,4):
      subbed[i][j]= Sbox[int(block[i][j],2)]
  return subbed

def InvSubBytes(block): # prend un bloc en forme binaire et retourne le résultat en binaire de l'inverse de l'opération SubBytes
  subbed = copy.deepcopy(block)
  for i in range(0,4):
    for j in range(0,4):
      subbed[i][j]= InvSbox[int(block[i][j],2)]
  return subbed

def ShiftRows(block): # prend un bloc et retourne le résultat de l'opération ShiftRows
  shifted = copy.deepcopy(block)
  for i in range(1,4):
    for j in range(0,4):
      shifted[i][j]=block[i][(j+i)%4]
  return shifted

def InvShiftRows(block): # prend un bloc et retourne le résultat de l'opération InvShiftRows
  shifted = copy.deepcopy(block)
  for i in range(1,4):
    for j in range(0,4):
      shifted[i][j]=block[i][(j-i)%4]
  return shifted

def MixColumns(block): # prend un bloc en binaire et retourne le résultat de l'opération MixColumns en binaire
  # ref https://en.wikipedia.org/wiki/Rijndael_MixColumns
  mixed = copy.deepcopy(block)
  for j in range(0,4):
    mixed[0][j]= XOR(XOR(XOR(GFMult2Bin[int(block[0][j],2)], GFMult3Bin[int(block[1][j],2)]),block[2][j]),block[3][j])
    mixed[1][j]= XOR(XOR(XOR(block[0][j], GFMult2Bin[int(block[1][j],2)]),GFMult3Bin[int(block[2][j],2)]),block[3][j])
    mixed[2][j]= XOR(XOR(XOR(block[0][j], block[1][j]),GFMult2Bin[int(block[2][j],2)]),GFMult3Bin[int(block[3][j],2)])
    mixed[3][j]= XOR(XOR(XOR(GFMult3Bin[int(block[0][j],2)], block[1][j]),block[2][j]),GFMult2Bin[int(block[3][j],2)])
  return mixed

def InvMixColumns(block): # prend un bloc en binaire et retourne le résultat de l'opération InvMixColumns en binaire
  # ref https://en.wikipedia.org/wiki/Rijndael_MixColumns
  mixed = copy.deepcopy(block)
  for j in range(0,4):
    mixed[0][j]= XOR(XOR(XOR(GFMult14Bin[int(block[0][j],2)], GFMult11Bin[int(block[1][j],2)]),GFMult13Bin[int(block[2][j],2)]),GFMult9Bin[int(block[3][j],2)])
    mixed[1][j]= XOR(XOR(XOR(GFMult9Bin[int(block[0][j],2)], GFMult14Bin[int(block[1][j],2)]),GFMult11Bin[int(block[2][j],2)]),GFMult13Bin[int(block[3][j],2)])
    mixed[2][j]= XOR(XOR(XOR(GFMult13Bin[int(block[0][j],2)], GFMult9Bin[int(block[1][j],2)]),GFMult14Bin[int(block[2][j],2)]),GFMult11Bin[int(block[3][j],2)])
    mixed[3][j]= XOR(XOR(XOR(GFMult11Bin[int(block[0][j],2)], GFMult13Bin[int(block[1][j],2)]),GFMult9Bin[int(block[2][j],2)]),GFMult14Bin[int(block[3][j],2)])
  return mixed

def AES_encrypt(inputHex, key, security): # prend un bloc de 16 octets en forme hexadécimale, une clé en forme de string hexadécimale
                                          # et un entier représentant le niveau de sécurité (128, 192 ou 256), et retourne la version chiffrée
                                          # sous forme hexadécimale du bloc original

  if (len(key))*4 != security:
    print('La longueur de la clé (' + str((len(key)-2)*4) + ' bits) ne correspond pas à AES-' + str(security))
  else:

    inputBin = hex2binBlock(inputHex)

    keyExp = KeyExpansion(key)
    cypher = AddRoundKey(keyExp[0:4], inputBin)

    if security == 128:
      R = 9
    if security == 192:
      R = 11
    if security == 256:
      R = 13
    for i in range(1,R+1):
      subbed = SubBytes(cypher)
      shifted = ShiftRows(subbed)
      mixed = MixColumns(shifted)
      cypher = AddRoundKey(keyExp[4*i:4*(i+1)], mixed)

    cypher = AddRoundKey(keyExp[4*(R+1):], ShiftRows(SubBytes(cypher)))
    return bin2hexaBlock(cypher)

def AES_decrypt(inputHex, key, security): # prend un bloc de 16 octets en forme hexadécimale, une clé en forme de string hexadécimale
                                          # et un entier représentant le niveau de sécurité (128, 192 ou 256), et retourne la version déchiffrée
                                          # sous forme hexadécimale du bloc original


  if (len(key))*4 != security:
    print('La longueur de la clé (' + str((len(key)-2)*4) + ' bits) ne correspond pas à AES-' + str(security))
  else:

    inputBin = hex2binBlock(inputHex)
    
    if security == 128:
      R = 9
    if security == 192:
      R = 11
    if security == 256:
      R = 13

    keyExp = KeyExpansion(key)
    cypher = AddRoundKey(keyExp[4*(R+1):], inputBin)
    mixed = cypher

    for i in range(R,0,-1):
      shifted = InvShiftRows(mixed)
      subbed = InvSubBytes(shifted)
      cypher = AddRoundKey(keyExp[4*i:4*(i+1)], subbed)
      mixed = InvMixColumns(cypher)

    shifted = InvShiftRows(mixed)
    subbed = InvSubBytes(shifted)
    cypher = AddRoundKey(keyExp[0:4], subbed)

    return bin2hexaBlock(cypher)

def hex2string(line): # prend une string hexadécimale et retourne la string ASCII correspondante (chaque paire de deux chiffres hexadécimaux est traduite en un caractère ASCII)
  hexString = ''
  for char in line:
    if char not in " ":
        hexString = hexString + char
  return bytes.fromhex(hexString).decode('ascii')

def string2hex(line): # prend une string et retourne la string hexadécimale correspondante selon le standard ASCII
  hexString = ''
  for char in line:
    hexString = hexString + hex(ord(char))[2:].zfill(2)
  
  return hexString

def CBC_encrypt(string, key, security): # prend une string de texte, une clé en forme de string hexadécimale
                                        # et un entier représentant le niveau de sécurité (128, 192 ou 256), 
                                        # et retourne en string hexadécimale la version chiffrée de la string originale
  hexString = string2hex(string)
  L = len(hexString)//32
  r = len(hexString)%32

  # Ajout du vecteur d'initialisation
  randomIV = ''
  for i in range(16):
    randomIV = randomIV + hex(random.randint(0,255))[2:].zfill(2)

  plaintextHex=[randomIV]

  # Création de la liste de string hexadécimales correspondant au message à chiffrer, sans le dernier bloc
  for i in range(0,L):
    plaintextHex.append(hexString[32*i:32*(i+1)])

  # Padding du dernier bloc
  if r != 0:
    lastBlock = hexString[32*L:]
    padding = hex((32-r)//2)[2:].zfill(2)
    for j in range(0,(32-r)//2):
      lastBlock = lastBlock + padding
    plaintextHex.append(lastBlock)

  # Création de la série de blocs à chiffrer
  plaintextBlock = []
  for block in plaintextHex:
    plaintextBlock.append(hexString2Block(block))

  # Chiffrement CBC
  cypherBlock = []
  for i in range(len(plaintextBlock)):
    if i > 0:
      currentBlock = hexBlockXOR(cypherBlock[i-1],plaintextBlock[i])
    else:
      currentBlock = plaintextBlock[0]
    cypherBlock.append(AES_encrypt(currentBlock, key, security))

  # Écriture de la string chiffrée
  cypher = ''
  for block in cypherBlock:
    cypher = cypher + block2HexString(block)

  return cypher

def CBC_decrypt(cypher, key, security): # prend une string hexadécimale, une clé en forme de string hexadécimale
                                        # et un entier représentant le niveau de sécurité (128, 192 ou 256), 
                                        # et retourne en string textuelle la version déchiffrée de la string originale

  L = len(cypher)//32

  # Création de la liste de blocs à déchiffrer
  cyphertextHex = []
  for i in range(0,L):
    cyphertextHex.append(cypher[32*i:32*(i+1)])

  cyphertextBlock = []
  for block in cyphertextHex:
    cyphertextBlock.append(hexString2Block(block))

  # Déchiffrement CBC
  plaintextBlock = []
  for i in range(1,len(cyphertextBlock)):
    currentBlock = AES_decrypt(cyphertextBlock[i], key, security)
    plaintextBlock.append(hexBlockXOR(currentBlock,cyphertextBlock[i-1]))

  # Création de la string hexadécimale du message déchiffré
  plaintextHex = ''
  for block in plaintextBlock:
    plaintextHex = plaintextHex + block2HexString(block)

  # Élimination du padding
  potPadding = int('0x'+ plaintextHex[-2:], 16)
  if potPadding < 16 and plaintextHex[-2*potPadding:-2*potPadding+2] == plaintextHex[-2:]:
    decoded = plaintextHex[:-2*potPadding]
  else: 
    decoded = plaintextHex

  # Traduction du message déchiffrer selon le standard ASCII
  return hex2string(decoded)
