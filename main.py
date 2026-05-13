### project -->> CURD OPERATION

from pathlib import Path 

def readfileandfolder():
    p = Path('')
    items = list(p.rglob('*'))
    for index ,file in enumerate(items):
        print(f'{index+1} - {file}')


def create_file():
    readfileandfolder()
   # C:\Users\HP\Desktop\file handling\hello.txt
    file_name = input('enter name of your file:')
    p = Path(file_name)
    if p.exists():
        print('FILE ALREADY EXISTS')
    else:
        with open(file_name,'w') as file:
            content = input('enter your file content:')
            file.write(content)
            print('FILE ADDED !')
            pass

def read_file():
    readfileandfolder()
    file_name = input('enter your name of your file:')
    p = Path(file_name)
    if p.exists():
        with open(file_name,'r') as file:
            print(file.read())
    else:
        print('FILE NOT FOUND!')

def update_file():
    readfileandfolder()
    file_name = input('enter your name of file to update')
    p = Path(file_name)
    if p.exists():
        with open(file_name,'a') as file:
            content = input('enter content to update')
            file.write(content)
            print('FILE UPDATED SUCCECCFULLY')
    else:
        print('file not found!')





print("press 1 for creating a file")
print("press 2 for reading a file ")
print("press 3 for updating a file")
print("press 4 for deleting a file")

option = int (input("enter your choice:"))
if option == 1:
    create_file()
elif option == 2:
    read_file()
elif option == 3:
    update_file()

