import argparse


parser = argparse.ArgumentParser()
parser.add_argument("text", help="Le texte que tu veux afficher sur la matrice de leds (Caractères acceptés : A-Za-z0-9 et l'espace)")
parser.add_argument("-rs", "--rainbowspeed", help="Modifie la vitesse de défilement des couleurs", type=int, default=8)
parser.add_argument("-d", "--duplicateframes", help="Modifie la vitesse de défilement du texte", type=int, default=1)
parser.add_argument("-o", "--out", help="Nom du fichier de sortie", default='custom.bin')
args = parser.parse_args()



message = args.text
rainbowSpeed = args.rainbowspeed
nbDuplicate = args.duplicateframes
filename = args.out



def listFromHex(h):
    tmp = '0'*(66 - len(bin(h))) + bin(h)[2:]
    return [tmp[i:i+8][::-1] for i in range(0, len(tmp), 8)][::-1]


def binaryToRGB(frame, rgb):
    _r, _g, _b = rgb
    return [[(_r*int(frame[i][j]), _g*int(frame[i][j]), _b*int(frame[i][j])) for j in range(8)]for i in range(8)]
    


alphabet = dict()


alphabet['1'] = listFromHex(0x7e1818181c181800)
alphabet['2'] = listFromHex(0x7e060c3060663c00)
alphabet['3'] = listFromHex(0x3c66603860663c00)
alphabet['4'] = listFromHex(0x30307e3234383000)
alphabet['5'] = listFromHex(0x3c6660603e067e00)
alphabet['6'] = listFromHex(0x3c66663e06663c00)
alphabet['7'] = listFromHex(0x1818183030667e00)
alphabet['8'] = listFromHex(0x3c66663c66663c00)
alphabet['9'] = listFromHex(0x3c66607c66663c00)
alphabet['0'] = listFromHex(0x3c66666e76663c00)

alphabet['A'] = listFromHex(0x6666667e66663c00)
alphabet['B'] = listFromHex(0x3e66663e66663e00)
alphabet['C'] = listFromHex(0x3c66060606663c00)
alphabet['D'] = listFromHex(0x3e66666666663e00)
alphabet['E'] = listFromHex(0x7e06063e06067e00)
alphabet['F'] = listFromHex(0x0606063e06067e00)
alphabet['G'] = listFromHex(0x3c66760606663c00)
alphabet['H'] = listFromHex(0x6666667e66666600)
alphabet['I'] = listFromHex(0x3c18181818183c00)
alphabet['J'] = listFromHex(0x1c36363030307800)
alphabet['K'] = listFromHex(0x66361e0e1e366600)
alphabet['L'] = listFromHex(0x7e06060606060600)
alphabet['M'] = listFromHex(0xc6c6c6d6feeec600)
alphabet['N'] = listFromHex(0xc6c6e6f6decec600)
alphabet['O'] = listFromHex(0x3c66666666663c00)
alphabet['P'] = listFromHex(0x06063e6666663e00)
alphabet['Q'] = listFromHex(0x603c766666663c00)
alphabet['R'] = listFromHex(0x66361e3e66663e00)
alphabet['S'] = listFromHex(0x3c66603c06663c00)
alphabet['T'] = listFromHex(0x18181818185a7e00)
alphabet['U'] = listFromHex(0x7c66666666666600)
alphabet['V'] = listFromHex(0x183c666666666600)
alphabet['W'] = listFromHex(0xc6eefed6c6c6c600)
alphabet['X'] = listFromHex(0xc6c66c386cc6c600)
alphabet['Y'] = listFromHex(0x1818183c66666600)
alphabet['Z'] = listFromHex(0x7e060c1830607e00)
alphabet[' '] = listFromHex(0x0000000000000000)
alphabet['a'] = listFromHex(0x7c667c603c000000)
alphabet['b'] = listFromHex(0x3e66663e06060600)
alphabet['c'] = listFromHex(0x3c6606663c000000)
alphabet['d'] = listFromHex(0x7c66667c60606000)
alphabet['e'] = listFromHex(0x3c067e663c000000)
alphabet['f'] = listFromHex(0x0c0c3e0c0c6c3800)
alphabet['g'] = listFromHex(0x3c607c66667c0000)
alphabet['h'] = listFromHex(0x6666663e06060600)
alphabet['i'] = listFromHex(0x3c18181800180000)
alphabet['j'] = listFromHex(0x1c36363030003000)
alphabet['k'] = listFromHex(0x66361e3666060600)
alphabet['l'] = listFromHex(0x1818181818181800)
alphabet['m'] = listFromHex(0xd6d6feeec6000000)
alphabet['n'] = listFromHex(0x6666667e3e000000)
alphabet['o'] = listFromHex(0x3c6666663c000000)
alphabet['p'] = listFromHex(0x06063e66663e0000)
alphabet['q'] = listFromHex(0xf0b03c36363c0000)
alphabet['r'] = listFromHex(0x060666663e000000)
alphabet['s'] = listFromHex(0x3e403c027c000000)
alphabet['t'] = listFromHex(0x1818187e18180000)
alphabet['u'] = listFromHex(0x7c66666666000000)
alphabet['v'] = listFromHex(0x183c666600000000)
alphabet['w'] = listFromHex(0x7cd6d6d6c6000000)
alphabet['x'] = listFromHex(0x663c183c66000000)
alphabet['y'] = listFromHex(0x3c607c6666000000)
alphabet['z'] = listFromHex(0x3c0c18303c000000)




message += "    "
message *= 100

linearframes = []

messageTotal = ["" for i in range(8)]
for i in range(8):
    for j in range(len(message)):
        messageTotal[i] += alphabet[message[j]][i]
        
r, g, b = 168, 50, 50
stage = 1


for i in range(len(messageTotal[0]) - 8):
    for _ in range(nbDuplicate):
        linearframes.append(bytes([255]))
        currFrame = binaryToRGB([messageTotal[x][i:i+8] for x in range(8)], (r, g, b))
        for l in currFrame:
            for x in l:
                linearframes.append(bytes([x[0],x[1],x[2]]))
                
        if stage == 1:
            g += rainbowSpeed
            if g >= 168:
                g = 168
                stage = 2
        elif stage == 2:
            r -= rainbowSpeed
            if r <= 50:
                r = 50
                stage = 3
        elif stage == 3:
            b += rainbowSpeed
            if b >= 168:
                b = 168
                stage = 4
        elif stage == 4:
            g -= rainbowSpeed
            if g <= 50:
                g = 50
                stage = 5
        elif stage == 5:
            r += rainbowSpeed
            if r >= 168:
                r = 168
                stage = 6
        elif stage == 6:
            b -= rainbowSpeed
            if b <= 50:
                b = 50
                stage = 1


f = open(filename, 'wb+')
f.write(b''.join(linearframes))
f.close()
    
