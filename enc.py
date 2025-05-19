import os
import sys
import zlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import subprocess
import base64
import marshal
import shutil
import re
import glob
import hashlib
import time
import tempfile
import platform

def kgfısk(filename):
    name = re.sub(r'[^a-zA-Z0-9_]', '', filename.replace('.py', '').replace(' ', '_').lower())
    return name + '.py'

def xjklq(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = [line.expandtabs(4).rstrip() + '\n' for line in lines]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

def pqzmw(working_dir, level):
    loader_code = f"""
# cython: language_level=3
cdef public void dummy_{level}():
    cdef int i
    for i in range(1000):
        i = (i * 7 + 13) % 256
"""
    loader_path = os.path.join(working_dir, f'loader_{level}.pyx')
    with open(loader_path, 'w') as f:
        f.write(loader_code)
    
    result = subprocess.run(['cythonize', '-i', loader_path], capture_output=True, text=True)
    if result.returncode != 0:
        
        sys.exit(1)

    if platform.system() == 'Windows':
        so_pattern = loader_path.replace('.pyx', '*.pyd')
    else:
        so_pattern = loader_path.replace('.pyx', '*.so')
    
    so_files = glob.glob(so_pattern)
    if not so_files:
        sys.exit(1)
    
    compiled_loader = so_files[0]
    return compiled_loader

def vbnrt(data, aes_keys, ivs, noise_len=64):
    encrypted = data
    for aes_key, iv in zip(aes_keys, ivs):
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        encrypted = iv + cipher.encrypt(pad(encrypted, AES.block_size))
    
    noise = get_random_bytes(noise_len)
    tail_noise = get_random_bytes(noise_len)
    mixed_data = noise + encrypted + tail_noise
    return zlib.compress(mixed_data), noise_len

def hjuyr(salt, iteration):
    base_key = hashlib.sha512(salt + str(iteration).encode()).digest()
    return hashlib.pbkdf2_hmac('sha256', base_key, b"secret_salt", 200000, 32)

def main():
    file_path = input("Şifrelenecek Python dosyasının yolunu girin: ").strip()
    if not os.path.isfile(file_path):
        
        sys.exit(1)
    if not os.access(file_path, os.R_OK):
        sys.exit(1)

    working_dir = os.getcwd()
    sanitized_name = kgfısk(os.path.basename(file_path))
    sanitized_path = os.path.join(working_dir, sanitized_name)
    shutil.copy(file_path, sanitized_path)
    
    xjklq(sanitized_path)
    
    with open(sanitized_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    base64_encoded_source = base64.b64encode(source_code.encode('utf-8')).decode('utf-8')
    base64_wrapper = f"""
import base64
import sys
import os
import importlib.util

def load_script():
    try:
        decoded_script = base64.b64decode('{base64_encoded_source}').decode('utf-8')
        exec(decoded_script, globals())
    except Exception as e:
        print(f"çalıştırma hatası: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    load_script()
"""
    
    code_obj = compile(base64_wrapper, sanitized_path, 'exec')
    bytecode = marshal.dumps(code_obj)
    
    kjfsl = get_random_bytes(16)
    pqwxz = get_random_bytes(16)
    zxmnb = get_random_bytes(16)
    
    rtyui = [hjuyr(kjfsl, i) for i in range(7)]
    ghjkl = [get_random_bytes(16) for _ in range(7)]
    encrypted_script, noise_len_script = vbnrt(bytecode, rtyui, ghjkl)
    
    vbnmq = [hjuyr(pqwxz, i) for i in range(4)]
    asdfg = [get_random_bytes(16) for _ in range(4)]
    lkjhg = [hjuyr(zxmnb, i) for i in range(4)]
    yuiop = [get_random_bytes(16) for _ in range(4)]
    
    mnbvc = pqzmw(working_dir, 1)
    cxzkl = pqzmw(working_dir, 2)
    
    with open(mnbvc, 'rb') as f:
        loader1_data = f.read()
    with open(cxzkl, 'rb') as f:
        loader2_data = f.read()
    
    encrypted_loader1, noise_len_loader1 = vbnrt(loader1_data, vbnmq, asdfg)
    encrypted_loader2, noise_len_loader2 = vbnrt(loader2_data, lkjhg, yuiop)
    
    inner_code = f"""
import base64
import os
import tempfile
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import marshal
import ctypes
import zlib
import hashlib
import time
import sys
import platform

def fghjk(salt, iteration):
    base_key = hashlib.sha512(salt + str(iteration).encode()).digest()
    return hashlib.pbkdf2_hmac('sha256', base_key, b"secret_salt", 200000, 32)

def zxcvb(data, aes_keys, noise_len):
    try:
        mixed_data = zlib.decompress(data)
        encrypted = mixed_data[noise_len:-noise_len]
        
        for aes_key in reversed(aes_keys):
            iv = encrypted[:16]
            cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            encrypted = unpad(cipher.decrypt(encrypted[16:]), AES.block_size)
        return encrypted
    except Exception as e:
        print(f"Şifre çözme hatası: {{e}}")
        sys.exit(1)

def qwert(loader_path, encrypted_data, aes_keys, level, noise_len):
    try:
        lib = ctypes.CDLL(loader_path)
        if level == 1:
            lib.dummy_{1}()
        elif level == 2:
            lib.dummy_{2}()
        return zxcvb(encrypted_data, aes_keys, noise_len)
    except Exception as e:
        sys.exit(1)

def ytrew():
    try:
        kjfsl = {repr(kjfsl)}
        pqwxz = {repr(pqwxz)}
        zxmnb = {repr(zxmnb)}
        
        rtyui = [fghjk(kjfsl, i) for i in range(7)]
        vbnmq = [fghjk(pqwxz, i) for i in range(4)]
        lkjhg = [fghjk(zxmnb, i) for i in range(4)]
        
        xcvbn = os.path.join(tempfile.gettempdir(), 'temp_loader2_{os.getpid()}.so')
        edcrf = os.path.join(tempfile.gettempdir(), 'temp_loader1_{os.getpid()}.so')
        
        
        asdfg = base64.b64decode('{base64.b64encode(encrypted_loader2).decode('utf-8')}')
        hjklz = zxcvb(asdfg, lkjhg, {noise_len_loader2})
        
        with open(xcvbn, 'wb') as f:
            f.write(hjklz)
        if platform.system() != 'Windows':
            os.chmod(xcvbn, 0o755)
        
        qazws = base64.b64decode('{base64.b64encode(encrypted_loader1).decode('utf-8')}')
        wsxed = qwert(xcvbn, qazws, vbnmq, 2, {noise_len_loader1})
        
        with open(edcrf, 'wb') as f:
            f.write(wsxed)
        if platform.system() != 'Windows':
            os.chmod(edcrf, 0o755)
        
        plmok = base64.b64decode('{base64.b64encode(encrypted_script).decode('utf-8')}')
        okmij = qwert(edcrf, plmok, rtyui, 1, {noise_len_script})
        
        code_obj = marshal.loads(okmij)
        exec(code_obj)
        
        time.sleep(1)
        if os.path.exists(edcrf):
            os.remove(edcrf)
        if os.path.exists(xcvbn):
            os.remove(xcvbn)
    except Exception as e:
        print(f"Çalıştırma hatası: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    ytrew()
"""
    inner_code_bytes = inner_code.encode('utf-8')
    base64_encoded_inner = base64.b64encode(inner_code_bytes).decode('utf-8')
    
    outer_code = f"""import sys
import base64
import os
import time

nmjkl = '.ninjapy'
hgfds = '{base64_encoded_inner}'
try:
    with open(nmjkl, 'wb') as qwsaz:
        qwsaz.write(base64.b64decode(hgfds))
    os.system('python3 ' + nmjkl + ' ' + ' '.join(sys.argv[1:]))
except Exception as plmok:
    print(f"Dış katman hatası: {{plmok}}")
finally:
    time.sleep(1)
    if os.path.exists(nmjkl):
        os.remove(nmjkl)
"""

    with open('@konusurlar_enc.py', 'w') as f:
        f.write(outer_code)
    
    if os.path.exists(sanitized_path):
        os.remove(sanitized_path)
    if os.path.exists(mnbvc):
        os.remove(mnbvc)
    if os.path.exists(cxzkl):
        os.remove(cxzkl)
    if os.path.exists(os.path.join(working_dir, 'loader_1.pyx')):
        os.remove(os.path.join(working_dir, 'loader_1.pyx'))
    if os.path.exists(os.path.join(working_dir, 'loader_2.pyx')):
        os.remove(os.path.join(working_dir, 'loader_2.pyx'))
    
    print("DOSYANIZ ŞİFRELENDİ. Şifreli dosya adı = @konusurlar_enc.py")

if __name__ == "__main__":
    main()
