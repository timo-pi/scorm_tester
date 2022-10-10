from cryptography.fernet import Fernet
import configparser
import rsa
import base64

private_key_start_comment = '-----BEGIN RSA PRIVATE KEY-----\n'
private_key_end_comment = '\n-----END RSA PRIVATE KEY-----'
public_key_start_comment = '-----BEGIN PUBLIC KEY-----\n'
public_key_end_comment = '\n-----END PUBLIC KEY-----'

publicKey, privateKey = rsa.newkeys(256)

with open('pu.k', 'wb') as f:
    f.write(public_key_start_comment.encode())
    f.write(str(base64.b64encode(publicKey).decode()))
    f.write(public_key_end_comment.encode())

with open('pr.k', 'wb') as f:
    f.write(private_key_start_comment.encode())
    f.write(str(base64.b64encode(privateKey).decode()))
    f.write(private_key_end_comment.encode())

# this is the string that we will be encrypting
password = input("Enter Password: ")


enc_PW = rsa.encrypt(password.encode(), publicKey)
with open('p.w', 'wb') as f:
    f.write(enc_PW)

print("original string: ", password)
print("encrypted string: ", enc_PW)

# dec_PW = rsa.decrypt(enc_PW, privateKey).decode()
# print("decrypted string: ", dec_PW)


