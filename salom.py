import math  as m
a,b=input("sin/cos/tg/ctg burchak: ").split()
r=m.radians(float(b))
print(m.sin(r) if a=="sin" else m.cos(r) if a=="cos" else m.tan(r) if a=="tg" else 1/m.tan(r))

     
