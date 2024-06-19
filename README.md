# Cryptography-Project

**Project: Confidentiality and Access Control in Amazon RDS MySQL**


## Description

This project aims to use encryption algorithms to encrypt SQL databases.

We use the AES-GCM-256 bit algorithm to encrypt key data columns in the table, with each column having a 256 bit AES key.

We then further use the CP-ABE algorithm to encrypt those 256-bit AES keys based on policies provided by the data owner.

Next, we will set permissions for data users through ABAC based on the policies and attributes provided by the data owner.

Finally, upload the encrypted data to Amazon RDS MySQL for storage.

Data users who want to query must go through 4 layers:
+ **Bcrypt**: used to authenticate passwords
+ **ABAC**: used to authenticate that user's attributes
+ **CP-ABE**: receive public key and secret key based on that user's attributes. Use these two keys to decrypt the encrypted 256-bit AES key. (Depending on the user's attributes and the encryption policy provided previously, CP-ABE will decrypt that key and the user will receive the AES key according to his attributes)
+ **AES-GCM**: after passing the above layers, users can decode the data and download it to view.

To be more intuitive, we use the **PyQT6** library to create a simple interface.

Currently, the project has only developed the ability to query encrypted data through csv files. In the future we will try to develop more missing features such as: querying that encrypted data in real time,...

<!-- 
## Authors


* [WanThinn](https://github.com/WanThinnn)
* [DduckTai](https://github.com/dducktai)
* [2uaan1ee]((https://github.com/2uaan1ee)) -->

## Contributors<!-- Required -->
<!-- 
* Without contribution we wouldn't have open source. 
* 
* Generate github contributors Image here https://contrib.rocks/preview?repo=angular%2Fangular-ja
-->

<a href="https://github.com/WanThinnn/Cryptography-Project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=WanThinnn/Cryptography-Project" />
</a>



## Demo
![Alt text](https://lh3.googleusercontent.com/pw/AP1GczMbuuQoEw4TxiolFOTM2PXTe3oEgtpS_LwrYOEMGA9poIh-BMvAQbHnuhzsy1N7L3xn34KA7nrBOa_X9v7SbT8ZQZzMF5nJf5xAhieWU1_0icO0YjFvwfuZGIusjwMgHYXPTxq7f3Z2BxmKnd5Sce3iQQ=w1544-h974-s-no)


## Dependencies
* Operating System: macOS, Linux. (Currently, we cannot develop this project on windows operating system)
* Programing Language: Python3 (version 3.10.11).
* Libraries: 
    * [openSSL](http://www.openssl.org/)
    * [PBC (latest)](http://crypto.stanford.edu/pbc/news.html)
    * [GMP 5.x](http://gmplib.org/)
    * [Charm Crypto 0.50](https://jhuisi.github.io/charm/install_source.html)
    * [Py-ABAC](https://py-abac.readthedocs.io/en/latest/)
    * [Bcrypt](https://pypi.org/project/bcrypt/)
    * [PyQt6 (for GUI)](https://pypi.org/project/PyQt6/)
    


## Installation
Make sure you have installed all libraries listed in the [Dependencies](#dependencies) section. After that, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary libraries. 

```bash
cd Cryptography-Project/main
pip install -r requirements.txt
```

## Usage
### Connecting to MySQL RDS

```python
import mysql.connector

# Connect to MySQL database on Amazon RDS
mydb = mysql.connector.connect(
  host="your-rds-endpoint",
  user="your-username",
  password="your-password",
  database="your-database"
)

# Check your database
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM your_table")
for row in mycursor.fetchall():
    print(row)

```

### Connecting to MongoDB
```bash
cd /Cryptography-Project/main/Data_User/ABAC
cd /Cryptography-Project/main/Data_Owner/ABAC
```

* Configure your MongoDB Connection in <b>config.py</b> file

* And remember to edit mysql_config in that file too

* After that, you can run this code to check your database:
```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://your-mongodb-uri")

# Select database
db = client.your_database

# Select collection
collection = db.your_collection

# Insert a document
collection.insert_one({"name": "example", "value": 42})

# Query the collection
for document in collection.find():
    print(document)

```

### Create a self-signed certificate. 
If you do not want to use the localhost ip address, you can skip this step. Conversely, after creating, put the created files into folders:
* Cryptography-Project/main/Data_Owner/DATA_OWNER_ABE
* Cryptography-Project/main/Data_User/DATA_USER_ABE
 * Cryptography-Project/main/Authority_Center

```bash
openssl ecparam -genkey -name secp384r1 -out private_key.pem
openssl req -new -sha384 -key private_key.pem -out cert.csr
openssl x509 -req -in cert.csr -signkey private_key.pem -out ecc_cert.pem -days 365 -sha256
```

### Run app
* You must first run the server for key generation and setup:
```bash
cd Cryptography-Project/main/Authority_Center/
python3 server.py
```

* Data User:
```bash
cd Cryptography-Project/main/Data_User/
python3 login_main.py
```

* Data Owner:
```bash
cd Cryptography-Project/main/Data_Owner/
python3 login_main.py
```

## Documentations
* [OpenSSL](https://www.openssl.org)
* [GNU Multiple Precision Arithmetic Library](https://en.wikipedia.org/wiki/GNU_Multiple_Precision_Arithmetic_Library)
* [The Pairing-Based Cryptography Library](https://crypto.stanford.edu/pbc/)
* [CryptoPP Library](https://cryptopp.com)
* [Advanced Encryption Standard](https://www.cryptopp.com/wiki/Advanced_Encryption_Standard)
* [AES-GCM in Python (pyca/cryptography)](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM)
* [Ciphertext-Policy Attribute-Based Encryption](https://www.cs.utexas.edu/~bwaters/publications/papers/cp-abe.pdf)
* [Fast Attribute-based Message Encryption](https://eprint.iacr.org/2017/807)
* [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)
* [Bcrypt in Python](https://github.com/pyca/bcrypt/)
* [Secure Sockets Layer andTransport Layer Security]()
* [PyQT6](https://www.pythonguis.com/pyqt6-tutorial/)
