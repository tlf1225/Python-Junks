from time import time

print(int(time() / 86400 / 365) + 1970)  # year
print(int(time() / 86400 % 365))  # day
