import os

def start_processing(r, w):
    words = []
    while True:
        data = os.read(r, 4)
        if data == b'kill':
            os.write(w, b'okay')
            return
        elif data == b'load':
            data = os.read(r, 8)
            num = int(data.decode(), 16)
            data = os.read(r, num)
            words.append(data)
            
        elif data == b'chek': 
            data = os.read(r, 8)
            num = int(data.decode(), 16)
            data = os.read(r, num)
            if data in words:
                os.write(w, b'exist')
            else:
                os.write(w, b'nonee')
def main():
    alpha = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    k = 52
    rList = []
    wList = []
    for i in range(2 * k):
        r, w = os.pipe()
        rList.append(r)
        wList.append(w)
    for i in range(k):
        pid = os.fork()
        if pid == 0:
            start_processing(rList[2 * i], wList[2 * i + 1])
            return
    while True:
        query = input()
        query = query.split()
        if query[0] == 'kill' and query[1] == 'all':
            for i in range(k):
                os.write(wList[2 * i], b'kill')
                data = os.read(rList[2 * i + 1], 4)
            return
        elif query[0] == 'load':
            word = query[1]
            i = alpha.index(word[0])
            os.write(wList[2 * i], b'load')
            os.write(wList[2 * i], bytes(hex(len(word))[2:].zfill(8), encoding='utf8'))
            os.write(wList[2 * i], bytes(word, encoding='utf8'))
        elif query[0] == 'check':
            word = query[1]
            i = alpha.index(word[0])
            os.write(wList[2 * i], b'chek')
            os.write(wList[2 * i], bytes(hex(len(word))[2:].zfill(8), encoding='utf8'))
            os.write(wList[2 * i], bytes(word, encoding='utf8'))
            if os.read(rList[2 * i + 1], 5) == b'exist':
                print('Есть слово')
            else:
                print('Нету слова')
main()
