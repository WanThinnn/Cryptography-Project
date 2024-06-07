import bcrypt
password = "password123"
byte_pwd = password.encode('utf-8')
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(byte_pwd, salt)
print(hashed_password)
print(hashed_password.decode('utf-8'))
if bcrypt.checkpw(byte_pwd, '$2b$12$VwY0Eyq5Y1J9bwMeYDIxTuYAA12nyteQWgxV475Nbp6GRr6GNmwxq'.encode('utf-8')):
   print("Password is correct")
else:
   print("Password is incorrect")