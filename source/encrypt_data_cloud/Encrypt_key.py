from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07

# Khởi tạo nhóm ghép cặp
group = PairingGroup('MNT224')  # Bạn có thể thay đổi loại của nhóm ghép cặp tùy thuộc vào nhu cầu của bạn

# Khởi tạo hệ thống CP-ABE
cpabe = CPabe_BSW07(group)

# Tạo khóa công khai và khóa bí mật
(pk, mk) = cpabe.setup()

# Định nghĩa các thuộc tính và chính sách truy cập
attributes = ['age', 'country', 'salary']
policy = '((country == US) and (age >= 18)) or (salary > 50000)'

# Mã hóa một tin nhắn với chính sách truy cập
ct = cpabe.encrypt(pk, policy, b'my secret message')

# Giải mã tin nhắn
pt = cpabe.decrypt(pk, mk, ct)
print(pt)
