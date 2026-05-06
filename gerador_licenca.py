import hashlib
import random
import string

SEGREDO = "autofill_pro_2026"

def gerar_hash(chave):
    return hashlib.sha256((chave + SEGREDO).encode()).hexdigest()

def gerar_licenca():
    while True:
        chave = "AUTOFILL-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if gerar_hash(chave).startswith("00"):
            return chave

if _name_ == "_main_":
    for _ in range(5):
        print(gerar_licenca())
