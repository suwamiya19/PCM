import matplotlib.pyplot as plt
import numpy as np
from pylab import *

f=eval(input('enter frequency of the message signal (20Hz to 20000Hz):'))
fs=eval(input('Enter the Sampling frequency (16kHZ to 10MHz accordingly with msg signal) for better quantisation'))
sample=8000  #number of samples
x=np.arange(sample)
y=np.sin(2*np.pi*f*x/fs) #sampling the analog message signal
print(y)

subplot(3,2,1)
plt.subplots_adjust(hspace=0.5)
plt.plot(x,y,linewidth=2)
plt.xlabel('sample(n)',fontweight='bold', fontsize=7)
plt.ylabel('amplitude(V)',fontweight='bold', fontsize=7)
plt.title('Messaage signal',fontweight='bold', fontsize=8)
plt.grid(True)

#Quantising the sampled signal
for i in range(8000):
    if (0<y[i]<0.25):
        y[i]=0.125
    if (0.25<y[i]<0.5):
        y[i]=0.375
    if (0.5<y[i]<0.75):
        y[i]=0.625
    if (0.75<y[i]<1):
        y[i]=0.875
    if (0>y[i]>-0.25):
        y[i]=-0.125
    if (-0.25>y[i]>-0.5):
        y[i]=-0.375
    if (-0.5>y[i]>-0.75):
        y[i]=-0.625
    if (-0.75>y[i]>-1):
        y[i]=-0.875    
      
    
print(y)
subplot(3,2,2)

plt.plot(x,y)
plt.xlabel('sample(n)',fontweight='bold', fontsize=7)
plt.ylabel('amplitude(V)',fontweight='bold', fontsize=7)
plt.title('Quantised message signal',fontweight='bold', fontsize=8)
plt.grid(True)


#Encoding the quantised signal
code=[]
for j in range(8000):
    if y[j]==0.125:
        code=code+[0,0,0]
    if y[j]==0.375:
        code=code+[0,0,1]
    if y[j]==0.625:
        code=code+[0,1,0]
    if y[j]==0.875:
        code=code+[0,1,1]
    if y[j]==-0.125:
        code=code+[1,0,0]
    if y[j]==-0.375:
        code=code+[1,0,1]
    if y[j]==-0.625:
        code=code+[1,1,0]
    if y[j]==-0.875:
        code=code+[1,1,1]
        
print(len(code))
subplot(3,2,3)
plt.step(range(0,len(code)),code)
plt.ylim((-2,5))
plt.xlabel('sample(n)',fontweight='bold', fontsize=7)
plt.ylabel('amplitude(V)',fontweight='bold', fontsize=7)
plt.title('Encoded signal',fontweight='bold', fontsize=8)
plt.grid(True)



# Returns XOR of 'a' and 'b' 
# (both of same length) 
def xor(a, b): 
    result = [] 
    # Traverse all bits, if bits are same, then XOR is 0, else 1 
    for i in range(1, len(b)): 
        if a[i] == b[i]: 
            result.append('0') 
        else: 
            result.append('1') 
  
    return ''.join(result) 
  
  
#Modulo-2 division 
def mod2div(divident, divisor): 
  
    # Number of bits to be XORed at a time. 
    pick = len(divisor) 
  
    # Slicing the divident to appropriate length for particular step 
    tmp = divident[0 : pick] 
  
    while pick < len(divident): 
  
        if tmp[0] == '1': 
  
            # replace the divident by the result of XOR and pull 1 bit down 
            tmp = xor(divisor, tmp) + divident[pick] 
  
        else:   # If leftmost bit is '0' 
            # If the leftmost bit of the dividend (or the part used in each step) is 0, the step cannot 
            # use the regular divisor; we need to use an all-0s divisor. 
            tmp = xor('0'*pick, tmp) + divident[pick] 
  
        pick += 1   # increment pick to move further 
  
    # For the last n bits, we have to carry it out normally as increased value of pick will cause 
    # Index Out of Bounds. 
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
  
    checkword = tmp 
    return checkword 
  
# Function used at the sender side to encode 
# data by appending remainder of modular divison 
# at the end of data. 
def encodeData(data, key): 
  
    l_key = len(key) 
  
    # Appends n-1 zeroes at end of data 
    appended_data = data + '0'*(l_key-1) 
    remainder = mod2div(appended_data, key) 
  
    # Append remainder in the original data 
    codeword = data + remainder
    #return codeword
    code2=list(codeword)
    return(code2),remainder
   
def listToString(s):
    str1="".join([str(i) for i in s])
    return(str1)
code1=listToString(code)

#Encoding the data using Cyclic Redundancy Check
key = "100000100110000010001110110110111" #standard 32 bit CRC divisor
l=len(key)
codeword,rem=encodeData(code1, key)  #codeword is the encoded data to be transmitted
lx=len(codeword)
print(len(codeword))



#on the receiver side
#to check for the errors in the bit transmitted
received_msg=listToString(codeword)
yy,Rem=encodeData(received_msg,key)

chk=''.join([str(i*0) for i in range(32)])
if(Rem==chk):
   print('No error in transmitted bit')
required_data=codeword[:lx-l]

#decoding the received message bits(data)
z=[]

for k in range(0,len(required_data),3):
    temp=code[k:k+3]
    if temp==[0,0,0]:
        z=z+[0.125]
    if temp==[0,0,1]:
        z=z+[0.375]
    if temp==[0,1,0]:
        z=z+[0.625]
    if temp==[0,1,1]:
        z=z+[0.875]
    if temp==[1,0,0]:
        z=z+[-0.125]
    if temp==[1,0,1]:
        z=z+[-0.375]
    if temp==[1,1,0]:
        z=z+[-0.625]
    if temp==[1,1,1]:
        z=z+[-0.875]    
        


print(len(z))

subplot(3,2,4)
plt.step(range(0,len(codeword)),codeword)
plt.ylim((-2,5))
plt.xlabel('sample(n)',fontweight='bold', fontsize=7)
plt.ylabel('amplitude(V)',fontweight='bold', fontsize=7)
plt.title('CRC encoded signal to be transmitted',fontweight='bold', fontsize=8)
plt.grid(True)


subplot(3,2,5)    
plt.plot(z)
plt.xlabel('sample(n)',fontweight='bold', fontsize=7)
plt.ylabel('amplitude(V)',fontweight='bold', fontsize=7)
plt.title('Decoded signal at receiver side',fontweight='bold', fontsize=8)
plt.grid(True)
plt.show()




















    
        


    
