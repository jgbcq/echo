import numpy as np

h = []
prime = [2,3,5,7,11,13,17,19]
for p in prime:
  const = ''
  rest = np.sqrt(p)
  for i in range(1,9):
    rest = ((rest % 1)*16)
    const = const + hex(int(rest//1))[2:]
  h.append(const)

k = []
prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
        197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]
for p in prime:
  const = ''
  rest = np.cbrt(p)
  for i in range(1,9):
    rest = ((rest % 1)*16)
    const = const + hex(int(rest//1))[2:]
  k.append(const)

def string2hex(line): # prend une string et retourne la string hexadécimale correspondante selon le standard ASCII
  hexString = ''
  for char in line:
    hexString = hexString + hex(ord(char))[2:].zfill(2)
  
  return hexString

def padding(string): # prend une string en forme hexadécimale et retourne la version avec le padding SHA-256

  stringR = string + '80'
  length = (len(stringR) + 16) % 128

  if length == 0:
    paddingL = 0
  else:
    paddingL = (128 - length)
  
  stringR = stringR + paddingL*'0'

  return stringR + hex(len(string)*4)[2:].zfill(16)

def str2Block(string): # prend une string en forme hexadécimale et retourne une liste de ses blocs de 64 octets
  blocks = []
  for i in range(len(string)//128):
    blocks.append(string[i*128:(i+1)*128])
  return blocks

def block2words(block): # prend une string en forme hexadécimale de 64 octets et retourne une liste de ses 16 mots de 4 octets en forme hexadécimale
  words = []
  for i in range(0,16):
    words.append(block[i*8:(i+1)*8])
  return words

def STRhex2bin(word): # prend une string hexadécimale et retourne sa forme binaire.
  binSTR = ''
  for i in range(len(word)):
    binSTR = binSTR + bin(int(word[i:(i+1)], 16))[2:].zfill(4)
  return binSTR

def STRbin2hex(word): # prend une string binaire et retourne sa forme hexadécimale. Restriction: la longueur de string originale en bits doit être un multiple de 4
  hexSTR = ''
  for i in range(len(word)//4):
    hexSTR = hexSTR + hex(int(word[i*4:(i+1)*4], 2))[2:]
  return hexSTR

def XOR(a,b,c=''): # prend 2 ou 3 string hexadecimales de même longeur et retourne la string hexadécimale correspondant au résultat de l'opération XOR
  a = STRhex2bin(a)
  b = STRhex2bin(b)
  c = STRhex2bin(c)

  res = ''
  if len(c)>0:
    for i in range(len(a)):
      res = res + str((int(a[i])+int(b[i])+int(c[i]))%2)
  else:
    for i in range(len(a)):
      res = res + str((int(a[i])+int(b[i]))%2)
  return STRbin2hex(res)  

def AND(a,b): # prend 2 string hexadécimales de même longeur et retourne la string hexadécimale correspondant au résultat de l'opération AND
  a = STRhex2bin(a)
  b = STRhex2bin(b)

  res = ''
  for i in range(len(a)):
    res = res + str(int(a[i])*int(b[i]))

  return STRbin2hex(res)  

def NOT(a): # prend 1 string hexadécimale et retourne la string hexadécimale correspondant au résultat de l'opération NOT
  a = STRhex2bin(a)
  res = ''
  for char in a:
    res = res + str((int(char)+1)%2)

  return STRbin2hex(res)  

def rightrotate(a,n): # prend une string hexadécimale a et un entier n et retourne la string hexadécimal correspondant au résultat de l'addition rightrotate x
  a = STRhex2bin(a)
  res = ''
  for i in range(len(a)):
    res = res + a[i-n]
  return STRbin2hex(res) 

def rightshift(a,n): # prend une string hexadécimale a et un entier n et retourne la string hexadécimale correspondant au résultat de l'addition rightshift x
  a = STRhex2bin(a)
  res = ''
  for i in range(len(a)):
    if i < n:
      res = res + '0'
    else:  
      res = res + a[i-n]
  return STRbin2hex(res)  

def SHA256(string):

  # On liste les valeurs de hachage initiales calculées précédemment:
  hash = ['6a09e667', 'bb67ae85', '3c6ef372', 'a54ff53a', '510e527f', '9b05688c', '1f83d9ab','5be0cd19']

  # On liste les constantes de ronde calculées précédemment:
  k = ['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',
       'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',
       'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',
       '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
       '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85',
       'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070',
       '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',
       '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2']

  hexed = string2hex(string)
  # Padding du message
  padded = padding(hexed)

  # Division du message paddé en bloc
  blocks = str2Block(padded)

  for block in blocks:
    # Division du bloc en mots
    words = block2words(block)

    for i in range(16,64):
        s0 = XOR(rightrotate(words[i-15],7), rightrotate(words[i-15],18), rightshift(words[i-15],3)) 
        s1 = XOR(rightrotate(words[i-2],17), rightrotate(words[i-2],19), rightshift(words[i-2],10)) 
        word = hex(int(words[i-16], 16) + int(s0, 16) + int(words[i-7], 16) + int(s1, 16))[2:].zfill(8)[-8:]
        words.append(word)
    
    a = hash[0]
    b = hash[1]
    c = hash[2]
    d = hash[3]
    e = hash[4]
    f = hash[5]
    g = hash[6]
    h = hash[7]

    for i in range(0,64):
      S1 = XOR(rightrotate(e, 6), rightrotate(e, 11), rightrotate(e, 25))
      ch = XOR(AND(e,f),AND(NOT(e),g))
      t1 = hex(int(h, 16) + int(S1, 16) + int(ch, 16) + int(k[i], 16) + int(words[i], 16))[2:].zfill(8)[-8:]
      S0 = XOR(rightrotate(a, 2), rightrotate(a, 13), rightrotate(a, 22))
      m = XOR(AND(a,b), AND(a,c), AND(b,c))
      t2 = hex(int(S0, 16) + int(m, 16))[2:].zfill(8)[-8:]

      h = g
      g = f
      f = e
      e = hex(int(d, 16) + int(t1, 16))[2:].zfill(8)[-8:]
      d = c
      c = b
      b = a
      a = hex(int(t1, 16) + int(t2, 16))[2:].zfill(8)[-8:]    

      
    #print(block)
    hash[0] = hex(int(hash[0], 16) + int(a, 16))[2:].zfill(8)[-8:]
    hash[1] = hex(int(hash[1], 16) + int(b, 16))[2:].zfill(8)[-8:]
    hash[2] = hex(int(hash[2], 16) + int(c, 16))[2:].zfill(8)[-8:]
    hash[3] = hex(int(hash[3], 16) + int(d, 16))[2:].zfill(8)[-8:]
    hash[4] = hex(int(hash[4], 16) + int(e, 16))[2:].zfill(8)[-8:]
    hash[5] = hex(int(hash[5], 16) + int(f, 16))[2:].zfill(8)[-8:]
    hash[6] = hex(int(hash[6], 16) + int(g, 16))[2:].zfill(8)[-8:]
    hash[7] = hex(int(hash[7], 16) + int(h, 16))[2:].zfill(8)[-8:]

  return hash[0]+hash[1]+hash[2]+hash[3]+hash[4]+hash[5]+hash[6]+hash[7]

SHA256(string2hex("The mystery of life isn't a problem to solve, but a reality to experience."))