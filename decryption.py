import rsa
import base64

pub_key = ''
private_key = ''

with open('pu.k', 'rb') as f:
    pub_key = f.read()

with open('pr.k', 'rb') as f:
    private_key = f.read()

pw = ''
with open('p.w', 'rb') as f:
    pw = f.read()

print(pw)
print(pub_key)
print(private_key)

prk = rsa.PrivateKey.load_pkcs1(private_key)
# puk = rsa.PublicKey._load_pkcs1_pem(pub_key)


dec_PW = rsa.decrypt(pw, prk)
print(dec_PW)