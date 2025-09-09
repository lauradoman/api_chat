import base64

texto = "XK8bEAZ=lEX>K54GBz_aWiw_lHDod|Wi~Q3Wi~ZqI5{ygIW#t9F*h~"
caracteres = len(texto)
print(f'el texto tiene = {caracteres} caracteres')

original = base64.b85decode(texto)
print(original)