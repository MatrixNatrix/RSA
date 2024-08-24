# -*- coding: utf-8 -*-
from __future__ import print_function  # Импорт функции print из будущих версий Python
import math  # Импорт модуля math
import random  # Импорт модуля random

def main():  # Определение основной функции
    # Запрос у пользователя ввода текста для шифрования
    user_text = input("Введите текст для шифрования: ")
    with open("plainText.txt", "w") as file:  # Открытие файла plainText.txt для записи
        file.write(user_text)  # Запись введенного текста в файл

    # Инициализация переменных modulus и public_exponent
    keys = []  # Список для хранения текста из key_generator.txt
    with open("key_generator.txt", 'r') as file:
        for line in file:
            for a in line.split():  # Разделение текста по пробелам
                keys.append(a)  # Добавление текста в список keys
    modulus = int(keys[2])  # Получение значения n
    public_exponent = int(keys[4])  # Получение значения e


    # Генерация ключей RSA

    generate_keys = input("Создать новые ключи? (y/n) ")  # Запрос у пользователя, нужно ли генерировать новые ключи
    if generate_keys.lower() == "y":  # Если пользователь ответил "y"
        prime1, prime2, modulus, public_exponent, private_exponent = generate_keys_rsa()  # Генерация ключей RSA
        print("Новые ключи созданы и добавлены в фаил key_generator.txt")  # Вывод сообщения
    else:
        print("Генерация новых ключей пропущена.")  # Вывод сообщения
        # Ввод пользователем ключей
        prime1 = int(input("Введите простое число p: "))
        prime2 = int(input("Введите простое число q: "))
        public_exponent = int(input("Введите открытую экспоненту e: "))
        modulus = prime1*prime2
        totient = (prime1 - 1) * (prime2 - 1)
        private_exponent = get_get_private_exponent(public_exponent, totient)
        while private_exponent < 0:  # Если закрытая экспонента отрицательная
            private_exponent += totient  # Добавление функции Эйлера

    write_keys_to_file(prime1, prime2, modulus, public_exponent, private_exponent)  # Запись ключей в файл

    # Шифрование текста
    encrypt_text(modulus, public_exponent)  # Вызов функции шифрования текста
    print("Текст зашифрован и добавлен в фаил encryptedText.txt")  # Вывод сообщения

    # Расшифровка текста
    decrypt_text(private_exponent, modulus)  # Вызов функции расшифрования текста
    print("Текст дешифрован и добавлен в фаил decryptText.txt")  # Вывод сообщения

  # def generate_keys_rsa(p, q, e):  # Функция генерации ключей RSA
      #  modulus = p * q  # Вычисление модуля n
      #  totient = (p - 1) * (q - 1)  # Вычисление функции Эйлера
      #  public_exponent = e  # Открытая экспонента
      #  get_private_exponent = get_get_private_exponent(public_exponent, totient)  # Получение закрытой экспоненты
      #  while get_private_exponent < 0:  # Если закрытая экспонента отрицательная
      #      get_private_exponent += totient  # Добавление функции Эйлера
      #  return p, q, modulus, public_exponent, get_private_exponent  # Возврат ключей

  # def main():  # Определение основной функции
  # Запрос у пользователя ввода текста для шифрования
  #     user_text = input("Введите текст для шифрования: ")
  #     with open("plainText.txt", "w") as file:  # Открытие файла plainText.txt для записи
  #        file.write(user_text)  # Запись введенного текста в файл

       # Генерация ключей RSA
       # prime1, prime2, modulus, public_exponent, get_private_exponent = generate_keys_rsa(p, q, e)  # Генерация ключей RSA

def write_keys_to_file(p, q, n, e, d):  # Функция записи ключей в файл
    p_str = "p = " + str(p) + "\n"  # Формирование строки с значением p
    q_str = "q = " + str(q) + "\n"  # Формирование строки с значением q
    n_str = "n = " + str(n) + "\n"  # Формирование строки с значением n
    e_str = "e = " + str(e) + "\n"  # Формирование строки с значением e
    d_str = "d = " + str(d) + "\n"  # Формирование строки с значением d
    public_key = "Public key( " + str(n) + " , " + str(e) + " )\n"  # Формирование строки с открытым ключом
    private_key = "Private key( " + str(n) + " , " + str(d) + " )\n"  # Формирование строки с закрытым ключом

    file = open("key_generator.txt", "w")  # Открытие файла key_generator.txt для записи
    file.write(public_key)  # Запись открытого ключа в файл
    file.write(private_key)  # Запись закрытого ключа в файл
    file.write(p_str)  # Запись значения p в файл
    file.write(q_str)  # Запись значения q в файл
    file.write(n_str)  # Запись значения n в файл
    file.write(e_str)  # Запись значения e в файл
    file.write(d_str)  # Запись значения d в файл
    file.close()  # Закрытие файла

def encrypt_text(n, e):  # Функция шифрования текста
    encrypted_message = open("encryptedText.txt", 'w')  # Открытие файла encryptedText.txt для записи
    with open("plainText.txt") as new_file:  # Открытие файла plainText.txt для чтения
        string =0
        for word in new_file:  # Перебор слов в файле
            for char in word:  # Перебор символов в слове
                string = string * (2**16) + ord(char)
        # Шифрование string и запись в файл
        encrypted_string = ""
        while string != 0 :
            encrypted_string = chr(rsa_encryption(string % (2**12), e, n)) + encrypted_string
            string = string // (2**12)
        print(encrypted_string, file=encrypted_message)
        print(n, file=encrypted_message)  # Запись значения n в файл
        print(e, file=encrypted_message)  # Запись значения e в файл
    encrypted_message.close()

def decrypt_text(d, n):  # Функция расшифровки текста
    keys = []  # Список для хранения ключей
    # with open("key_generator.txt", 'r') as file:  # Открытие файла key_generator.txt для чтения
    #    for line in file:  # Перебор строк в файле
    #        for a in line.split():  # Разделение строки на элементы
    #            keys.append(a)  # Добавление элемента в список keys
   # encrypted_data = []  # Список для хранения зашифрованных данных
    f = open("encryptedText.txt", 'r')  # Открытие файла encryptedText.txt для чтения
    decrypted = 0
    for l in f.readline() :  # Перебор строк в файле
            decrypted = (2**12)*decrypted + rsa_decrypt(ord(l), d, n)  # Добавление числа в список encrypted_data
    decrypted_message = ""
    while decrypted != 0 :
        decrypted_message = chr(decrypted % (2**16)) + decrypted_message
        decrypted = decrypted // 16

    g = open("decryptText.txt", 'w')  # Открытие файла decryptText.txt для записи
    print(decrypted_message, file = g)  # Перебор элементов списка encrypted_data
    f.close()
    g.close()

def get_prime():  # Функция получения простого числа
    prime_numbers = []  # Список для хранения простых чисел
    for num in range(1000, 10000 + 1):  # Перебор чисел в диапазоне
        if num > 1:  # Проверка на простое число
            for i in range(2, num):  # Перебор делителей
                if (num % i) == 0:  # Если число делится на делитель
                    break  # Выход из цикла
            else:  # Если число не делится ни на один делитель
                prime_numbers.append(num)  # Добавление числа в список
    prime_count = len(prime_numbers)  # Длина списка prime_numbers
    random_index = random.randint(1, prime_count-1)  # Генерация случайного индекса
    return prime_numbers[random_index]  # Возврат случайного простого числа

def generate_keys_rsa():  # Функция генерации ключей RSA
    prime1 = get_prime()  # Получение первого простого числа
    prime2 = get_prime()  # Получение второго простого числа
    modulus = prime1 * prime2  # Вычисление модуля n
    totient = (prime1 - 1) * (prime2 - 1)  # Вычисление функции Эйлера
    public_exponent = get_public_exponent(totient)  # Получение открытого экспоненты
    get_private_exponent = get_get_private_exponent(public_exponent, totient)  # Получение закрытого экспоненты
    while get_private_exponent < 0:  # Если закрытая экспонента отрицательная
        get_private_exponent += totient  # Добавление функции Эйлера
    return prime1, prime2, modulus, public_exponent, get_private_exponent  # Возврат ключей

def get_public_exponent(m):  # Функция получения открытой экспоненты
    public_exponent = get_prime()  # Получение случайного простого числа
    while gcd(public_exponent, m) != 1:  # Пока НОД не равен 1
        public_exponent += 1  # Увеличение открытой экспоненты
    return public_exponent  # Возврат открытой экспоненты

def gcd(a, b):  # Функция вычисления НОД
    while b > 0:  # Пока b не равно 0
        a, b = b, a % b  # Обновление a и b
    return a  # Возврат НОД

def get_get_private_exponent(e, m):  # Функция получения закрытой экспоненты
    x = lasty = 0  # Инициализация переменных
    lastx = y = 1
    while m != 0:  # Пока m не равно 0
        q = e // m  # Вычисление частного
        e, m = m, e % m  # Обновление e и m
        x, lastx = lastx - q*x, x  # Обновление x и lastx
        y, lasty = lasty - q*y, y  # Обновление y и lasty
    return lastx  # Возврат закрытой экспоненты

def rsa_encryption(m, e, n):  # Функция шифрования RSA
    x = pow(m, e, n)  # Вычисление зашифрованного значения
    return x  # Возврат зашифрованного значения

def rsa_decrypt(c, d, n):  # Функция расшифрования RSA
    x = pow(c, d, n)  # Вычисление расшифрованного значения
    return x  # Возврат расшифрованного значения

if __name__ == "__main__":  # Проверка, является ли модуль основным
    main()  # Вызов основной функции