from winreg import OpenKeyEx, QueryValueEx, CloseKey, HKEY_LOCAL_MACHINE, KEY_READ, REG_BINARY

if __name__ == '__main__':
    try:
        key = OpenKeyEx(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, KEY_READ)
        value, regtype = QueryValueEx(key, "DigitalProductId")
        CloseKey(key)
        value = bytearray(value)
        if regtype == REG_BINARY:
            keyOffset = 52
            i = 24
            # noinspection SpellCheckingInspection
            chars = "BCDFGHJKMPQRTVWXY2346789"
            after = (value[66] // 6) & 1
            value[66] = (value[66] & 0xF7) | ((after & 2) * 4)
            out = ""
            last = 0
            while i >= 0:
                cur = 0
                x = 14
                while x >= 0:
                    cur *= 256
                    cur += value[x + keyOffset]
                    value[x + keyOffset] = (cur // 24)
                    cur %= 24
                    x -= 1
                i -= 1
                out = chars[cur] + out
                last = cur
            if after:
                part = out[1:last + 1]
                insert = "N"
                replace = part + insert
                out = out.replace(part, replace)
                if last == 0:
                    out = insert + out
            print("-".join([out[1:6], out[6:11], out[11:16], out[16:21], out[21:26]]))
    except OSError as e:
        print(e)
