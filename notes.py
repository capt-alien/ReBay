# hash notes
# useing hashlib in python
# pwd = 'launchCode'
# hashlib.sha256(str.encode(pwd)).hexdigest()
# hashlib.sha256() --> calls the hash function
# str.encode(pwd)  -->
# .hexdigest()     --> turns hashed object into a string

import hashlib

salt = "dickhead"

def make_pw_hash(password):
    return hashlib.sha256(str.encode(password+salt)).hexdigest()

def check_pw_hash(password, hash):
    if make_pw_hash(password) == hash:
        return True
    return False

code ="mcalsdcasdmcalsdcasdmcalsdcasd"
entry ="1234"

a86bf36baa32424e083333cd0549ec28da9dabeaff0148ef47174fee7b1295


hashA = make_pw_hash(code)

print(code)
print(code+salt)
print(hashA)
print("PW Match:")
print(check_pw_hash(entry, hashA))
