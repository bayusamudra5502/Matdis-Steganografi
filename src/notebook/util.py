"""Modul Utilitas

Modul yang digunakan untuk menyimpan segala utilitas"""

from abc import ABC, abstractmethod
import numpy as np
import random

class Randomizer(ABC):
  """Base Class Randomizer"""

  @abstractmethod
  def random(self) -> int:
    pass

  @abstractmethod
  def reset():
    pass
  
class LCG(Randomizer):
  """Kelas LCG sebagai pembangkit angka acak"""

  def __init__(self, a, b, m, seed = 0) -> None:
      self.__x = seed
      self.__a = a
      self.__b = b
      self.__m = m
      self.__x0 = seed
    
  def random(self) -> int:
    """Menghasilkan angka random"""
    self.__x = (self.__a * self.__x + self.__b) % (self.__m)
  
    return self.__x
  
  def reset(self):
      self.__x = self.__x0

class NumberIterator(Randomizer):
  """Kelas Pencacah bilangan bulat"""

  def __init__(self, max, seed=0) -> None:
      self.__x = seed
      self.__m = max
      self.__x0 = seed
  
  def random(self) -> int:
      self.__x += 1
      self.__x %= self.__m

      return self.__x
  
  def reset(self):
      self.__x = self.__x0

def color_coeff(color) -> float:
  """Mengembalikan Color Coefficient dari sebuah warna. 
  Warna merupakan nilai antara 0 s.d. 255 dari sebuah kanal warna dalam pixel"""
  X_r = color/255

  if X_r <= 0.03928:
    return X_r/12.92
  else:
    return ((X_r + 0.055)/1.055)**2.

def rel_luminance(Rchannel, GChannel, BChannel) -> float:
  """Mengembalikan relative lumnance dari sebuah warna"""

  return color_coeff(Rchannel) * 0.03928 + 0.7152 * color_coeff(GChannel) + 0.0722*color_coeff(BChannel)

def contrast_ratio(color1, color2) -> float:
  """Mengembalikan contrast ratio dari dua buah warna"""

  return (rel_luminance(color1[0],color1[1], color1[2]) + 0.05)/(rel_luminance(color2[0],color2[1], color2[2]) + 0.05)

def string2list(str) -> list[int]:
  """Mengubah string menjadi list dari ascii number tiap karakter pada list"""

  res = []
  for i in str:
    res.append(ord(i))
  
  return res

def insert_message(randomizer: Randomizer, image_1d: np.ndarray, message: str, lsb_number = 1) -> tuple[np.ndarray, int]:
  """Menyisipkan pesan ke dalam gambar dengan menggunakan lsb_number digit dari tiap warna"""

  randomizer.reset()

  numlist = string2list(message + "\x00")
  filled = np.zeros(image_1d.shape, dtype=bool)
  result = image_1d.copy()
  mask = -1 ^ ((1 << lsb_number) - 1)
  bits = 0

  while(len(numlist) > 0):
    idxRandom = randomizer.random()
    
    if filled[idxRandom]:
      break
    
    result[idxRandom] &= mask
    result[idxRandom] |= numlist[0] % (1 << lsb_number)

    filled[idxRandom] = True
    numlist[0] >>= lsb_number

    bits += lsb_number
    if bits % 8 == 0:
      numlist = numlist[1:]

  
  return result, bits

def extract_message(randomizer: Randomizer, image_1d: np.ndarray, lsb_number=1) -> tuple[str, int]:
  """Mengekstraksi pesan pada stegeo-object"""

  randomizer.reset()

  filled = np.zeros(image_1d.shape, dtype=bool)
  result = ""
  idxRandom = randomizer.random()
  mask = ((1 << lsb_number) - 1)
  tmp = 0
  bits = 0

  while not filled[idxRandom]:
    tmp += (image_1d[idxRandom] & mask) << (bits % 8)
    filled[idxRandom] = True
    bits += lsb_number
    idxRandom = randomizer.random()

    if bits % 8 == 0:
      if tmp == 0:
        break
      else:
        result += chr(tmp)
        tmp = 0
  
  return result, bits

def matrixto1d(arr: np.ndarray):
  return arr.copy().flatten()

def arr1dtomatrix(arr: np.ndarray, m, n):
  return arr.copy().reshape((m,n))

def get_lowest_multiplier(m):
  isDiv4 = (m % 4 == 0)
  i = 2
  factorMultiply = 1

  while i * i <= m:
    if m % i:
      i += 1
    else:
      m //= i
      factorMultiply *= i

      while m % i == 0:
        m //= i
  
  if m > 1:
    factorMultiply *= m
  
  if isDiv4:
    factorMultiply <<= 1
  
  return factorMultiply + 1

def get_b(m):
  num = 1

  while m % num == 0:
    num = random.randint(2,m)
  
  return num

def lsb_copyer(array1d: np.ndarray, lsb_number=1):
  result = array1d.copy()
  mask = ((1 << lsb_number) - 1)

  for i in range(len(result)):
    tmp = 0
    last = result[i] & mask
    n = 0

    while n < 8:
      tmp <<= lsb_number
      tmp += last

      n += lsb_number
    
    result[i] = tmp
  
  matrix = result.reshape((863,863,3))

  r = np.copy(matrix[:,:,0])
  g = np.copy(matrix[:,:,1])
  b = np.copy(matrix[:,:,2])

  return r,g,b