import datetime
import requests
import numpy as np
import math
import matplotlib.pyplot as plt

API_URL = 'https://openexchangerates.org/api/historical/'
APP_ID = '?app_id=26c729caeade49f38d235f712f317c07'


def pastWeekList():
   #return array of past 7 dates yyyy-mm-dd
   return [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(7)][::-1]   
   #return [datetime.datetime(2017, 12, 14) - datetime.timedelta(days=x) for x in range(7)][::-1]

def pastWeekData():
    #return array of json objects containing exchange data
    return [requests.get(API_URL + str(x.date()) + '.json' + APP_ID).json() for x in pastWeekList()]

def getCoordinates():
    #return x and y-coords for (day, USD to EUR)
    x = [x for x in range(1, 8)]
    y = [x['rates']['GBP'] for x in pastWeekData()]
    return [x, y]
    
def yavg(): #Y-average
    sum = 0
    for y in coord[1]:
      sum += y
    return sum / len(coord[1])
    
#Definitions    
coord = getCoordinates()


def getPoly2Curve(): #second degree polynomial curve of best fit  
    return np.polyfit(coord[0], coord[1], 2)
    
def getPoly2Derivative():
    poly = getPoly2Curve
    return [2*poly[0]*coord[0][x] + poly[1] for x in range (7)]
    
def getPoly2CurvePredictedValue(): #Y-hat
    #return array of predicted values
    poly = getPoly2Curve()
    return [poly[0]*(x**2)+poly[1]*x+poly[2] for x in coord[0]]

def getPoly2rsquared(): #return r-squared value of second degree polynomial fit
    ypred = getPoly2CurvePredictedValue()
    SStotal = 0
    for x in range (0,7):
        SSresid += (coord[1][x] - ypred[x])**2
    for x in range (0,7):
        SStotal += (coord[1][x] - yavg())**2
    return 1 - (SSresid/SStotal)


def getPoly3Curve():
    return np.polyfit(coord[0], coord[1], 3)

def getPoly3CurvePredictedValue():
    poly = getPoly3Curve()
    return [poly[0]*(x**3)+poly[1]*(x**2)+poly[2]*x+poly[3] for x in coord[0]]
    
def getPoly3rsquared():
    ypred = getPoly3CurvePredictedValue()
    SStotal = 0
    for x in range (0,7):
        SSresid += (coord[1][x] - ypred[x])**2
    for x in range (0,7):
        SStotal += (coord[1][x] - yavg())**2
    return 1 - (SSresid/SStotal)


def getPoly4Curve():
    return np.polyfit(coord[0], coord[1], 4)

def getPoly4CurvePredictedValue():
    poly = getPoly4Curve()
    return [poly[0]*(x**4)+poly[1]*(x**3)+poly[2]*(x**2)+poly[3]*x+poly[4] for x in coord[0]]
    
def getPoly4rsquared():
    ypred = getPoly4CurvePredictedValue()
    SSresid = 0
    SStotal = 0
    for x in range (0,7):
        SSresid += (coord[1][x] - ypred[x])**2
    for x in range (0,7):
        SStotal += (coord[1][x] - yavg())**2
    return 1 - (SSresid/SStotal)


def getPoly5Curve():
    return np.polyfit(coord[0], coord[1], 5)
    
def getPoly5CurvePredictedValue():
    poly = getPoly5Curve()
    return [poly[0]*(x**5)+poly[1]*(x**4)+poly[2]*(x**3)+poly[3]*(x**2)+poly[4]*x+poly[5] for x in coord[0]]
    
def getPoly5rsquared():
    ypred = getPoly5CurvePredictedValue()
    #return     SSresid = 0
    SStotal = 0
    for x in range (0,7):
        SSresid += (coord[1][x] - ypred[x])**2
    for x in range (0,7):
        SStotal += (coord[1][x] - yavg())**2
    return 1 - (SSresid/SStotal)


def getLnCurve():
    return np.polyfit(np.log(coord[0]), coord[1], 1)

def getLnDerivative():
    poly = getLnCurve()
    return [poly[0]/coord[0][x] for x in range (7)]
    
def getLnCurvePredictedValue():
    poly = getLnCurve()
    return [poly[0]*np.log(x)+poly[1] for x in coord[0]]
    
def getLnrsquared():
    ypred = getLnCurvePredictedValue()
    SSresid = 0
    SStotal = 0
    for x in range (0,7):
        SSresid += (coord[1][x] - ypred[x])**2
    for x in range (0,7):
        SStotal += (coord[1][x] - yavg())**2
    return 1 - (SSresid/SStotal)
    
   
def getExpCurve():
    return np.polyfit(coord[0], np.log(coord[1]), 1)

def getExpDerivative():
    poly = getExpCurve()
    return poly[0]*(math.exp(poly[0]*coord[0][6]+poly[1]))

def getExpCurvePredictedValue():
    poly = getExpCurve()
    return [math.exp(poly[0]*x+poly[1]) for x in coord[0]]

def getExprsquared():
    ypred = getExpCurvePredictedValue()
    SSresid = 0
    SStotal = 0
    for x in range (0,7):
        SSresid += (coord[1][x] - ypred[x])**2
    for y in range (0,7):
        SStotal += (coord[1][y] - yavg())**2
    return 1 - (SSresid/SStotal)


def betterCurve ():
    Exp = getExprsquared()
    Ln = getLnrsquared()
    Expbool = False
    Lnbool = False
    if (Exp > Ln):
        Expbool = True
    elif (Ln > Exp):
        Lnbool = True
    else:
        Lnbool = True
    if (Expbool):
       return Exp
    else:
       return Ln



#print(pastWeekList())
#print(getCoordinates())
#print(yavg())
#print(getLnCurve())
#print(getPoly2Curve())
#print(getPoly3Curve())
#print(getPoly5Curve())
#print(getExpCurve())
#print(getLnCurvePredictedValue())
#print(getPoly2CurvePredictedValue())
#print(getPoly3CurvePredictedValue())
#print(getPoly5CurvePredictedValue())
#print(getExpCurvePredictedValue())
print(getLnrsquared())
#print(getPoly2rsquared())
#print(getPoly3rsquared())
#print(getPoly4rsquared())
#print(getPoly5rsquared())
print(getExprsquared())
print(betterCurve())    
#print(getLnDerivative())
#print(getPoly2Derivative())
#print(getPoly3Derivative())
#print(getPoly4Derivative())
#print(getPoly5Derivative())
#print(getExpDerivative())

x_new = np.linspace(coord[0][0], coord[0][-1], 50)
fPoly2 = np.poly1d(getPoly2Curve())
fPoly3 = np.poly1d(getPoly3Curve())
fPoly4 = np.poly1d(getPoly4Curve())
fPoly5 = np.poly1d(getPoly5Curve())
fLn = np.poly1d(getLnCurve())
fExp = np.poly1d(getExpCurve())

y_Poly2 = fPoly2(x_new)
y_Poly3 = fPoly3(x_new)
y_Poly4 = fPoly4(x_new)
y_Poly5 = fPoly5(x_new)
y_Ln = fLn(x_new)
y_Exp = fExp(x_new)

plt.plot(coord[0],coord[1],'o', x_new, y_Ln)#raw x-value, raw y-value, circle, evenly spaced x, curve of best fit of x
plt.xlim(coord[0][0]-1, coord[0][-1] + 1)
plt.show()



#r^2 value calculator done for ln
#polyfit with better r^2 gets chosen 
def isDerivativePosToZero():
    Exp = getExprsquared()
    Ln = getLnrsquared()
    Expbool = False
    Lnbool = False
    if (Exp > Ln):
        Expbool = True
    elif (Ln > Exp):
        Lnbool = True
    else:
        Lnbool = True
    if (Expbool):
        deriv = getExpDerivative()
    else:
        deriv = getLnDerivative()
    return (deriv[6] > 0 and deriv[6] < 0.0005)

def isDerivativeNegToZero():
    Exp = getExprsquared()
    Ln = getLnrsquared()
    Expbool = False
    Lnbool = False
    if (Exp > Ln):
        Expbool = True
    elif (Ln > Exp):
        Lnbool = True
    else:
        Lnbool = True
    if (Expbool):
        deriv = getExpDerivative()
    else:
        deriv = getLnDerivative()
    return (deriv[6] < 0 and deriv[6] > -0.0005)

def isDerivativePos():
    Exp = getExprsquared()
    Ln = getLnrsquared()
    Expbool = False
    Lnbool = False
    if (Exp > Ln):
        Expbool = True
    elif (Ln > Exp):
        Lnbool = True
    else:
        Lnbool = True
    if (Expbool):
        deriv = getExpDerivative()
    else:
        deriv = getLnDerivative()
    return (deriv > 0)

def isDerivativeNeg():
    Exp = getExprsquared()
    Ln = getLnrsquared()
    Expbool = False
    Lnbool = False
    if (Exp > Ln):
        Expbool = True
    elif (Ln > Exp):
        Lnbool = True
    else:
        Lnbool = True
    if (Expbool):
        deriv = getExpDerivative()
    else:
        deriv = getLnDerivative()
    return (deriv < 0)
    
def checkDerivativeSign():
    if isDerivativePosToZero():
        return '+d0'
    elif isDerivativePos():
        return '+d'
    if isDerivativeNegToZero():
        return '-d0'
    elif isDerivativeNeg():
        return '-d'

def warningSystem():
	if checkDerivativeSign() == '+d0':
		return 'Drop in Dollar value expected; exchange currency into Euros.'
	if checkDerivativeSign() == '+d':
		return 'Value of Dollar increasing'
	if checkDerivativeSign() == '-d0':
		return 'Spike in Dollar value expected; exchange currency into Dollars.'
	if checkDerivativeSign() == '-d':
		return 'Value of Dollar decreasing'

print(warningSystem())

# By Sam, Jarod, Raymond
