from main import init, run_async, Account, hashit

import sys
_, username, password = sys.argv

password = hashit(password)

run_async(init())
run_async(Account(username=username, password=password).save())