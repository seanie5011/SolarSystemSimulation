from vpython import *

##Solar System with 2 bodies
t = 0
dt = 100
G = 6.6741*(10**(-11))

#sun body
xS = 0
yS = 0
MS = 1.989*(10**30)
RS = 696340000

#earth body
vxE = 0
xE = 149600000000
vyE = 30000
yE = 0
ME = 5.972*(10**24)
RE = 6371000

#jupiter body
vxJ = 0
xJ = 763210000000
vyJ = 13000
yJ = 0
MJ = 1.898*(10**27)
RJ = 69911000

sun = sphere(pos = vector(xS,yS,0), radius = 10*RS, color = color.yellow)
earth = sphere(pos = vector(xE,yE,0), radius = 200*RE, color = color.blue, make_trail = True, retain = 150)
jupiter = sphere(pos = vector(xJ,yJ,0), radius = 50*RJ, color = color.red, make_trail = True, retain = 300)

while True:
  rate(1 * 60 * 60 * 24 * 365) #31536000 calculations per second allowed
    
  vxE = vxE - dt * ( ((G*MS*xE)/(((xE**2 + yE**2)**0.5)**3)) + ((G*MJ*(xE - xJ))/((((xE - xJ)**2 + (yE - yJ)**2)**0.5)**3)) )
  xE = xE + vxE * dt
  vyE = vyE - dt * (((G*MS*yE)/(((xE**2 + yE**2)**0.5)**3)) + ((G*MJ*(yE - yJ))/((((xE - xJ)**2 + (yE - yJ)**2)**0.5)**3)))
  yE = yE + vyE * dt
  earth.pos = vector(xE, yE, 0)
    
  vxJ = vxJ - dt * (((G*MS*xJ)/(((xJ**2 + yJ**2)**0.5)**3)) + ((G*ME*(xJ - xE))/((((xJ - xE)**2 + (yJ - yE)**2)**0.5)**3)))
  xJ = xJ + vxJ * dt
  vyJ = vyJ - dt * (((G*MS*yJ)/(((xJ**2 + yJ**2)**0.5)**3)) + ((G*ME*(yJ - yE))/((((xJ - xE)**2 + (yJ - yE)**2)**0.5)**3)))
  yJ = yJ + vyJ *dt
  jupiter.pos = vector(xJ, yJ, 0)

  t = t + dt

print(t)
