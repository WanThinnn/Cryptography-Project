from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07

def main():
    group = PairingGroup('SS512')
    cpabe = CPabe_BSW07(group)

    # Tạo một cặp khóa công khai và khóa bí mật
    (master_public_key, master_secret_key) = cpabe.setup()
    
    # Thuộc tính của người dùng
    attributes = ['ONE', 'TWO', 'THREE']

    # Tạo khóa bí mật cho người dùng
    user_secret_key = cpabe.keygen(master_public_key, master_secret_key, attributes)
    
    # Thông điệp cần mã hóa
    message = group.random(GT)
    
    # Chính sách truy cập
    access_policy = '((ONE and THREE) and (TWO or FOUR))'
    
    # Mã hóa thông điệp
    ciphertext = cpabe.encrypt(master_public_key, message, access_policy)
    print(ciphertext)
    
    # Giải mã thông điệp
    decrypted_message = cpabe.decrypt(master_public_key, user_secret_key, ciphertext)
    
    # Kiểm tra xem thông điệp được giải mã có khớp với thông điệp gốc
    assert message == decrypted_message, "Giải mã không thành công!"
    print("Giải mã thành công!")

if __name__ == "__main__":
    main()
