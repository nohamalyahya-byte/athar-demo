import numpy as np, wave
SR=44100; DUR=81.2; N=int(SR*DUR)
rng=np.random.default_rng(11)
L=np.zeros(N); R=np.zeros(N); vL=np.zeros(N); vR=np.zeros(N)
def add(sig,start,gain=1.0,pan=0.0,verb=0.0):
    i=int(start*SR)
    if i>=N: return
    n=min(len(sig),N-i); s=sig[:n]*gain; l=s*np.sqrt((1-pan)/2); r=s*np.sqrt((1+pan)/2)
    L[i:i+n]+=l; R[i:i+n]+=r; vL[i:i+n]+=l*verb; vR[i:i+n]+=r*verb
def env(n,a,r):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR)); e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr); return e
def pad(freqs,ln,lvl,a=1.2,r=1.8):
    n=int(ln*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for f in freqs:
        for det in (-7,0,7):
            ff=f*2**(det/1200)
            for k in range(1,7): s+=np.sin(2*np.pi*ff*k*tt+rng.uniform(0,6.28))/(k**1.5)
    return s*env(n,a,r)*lvl
def piano(f,g,ln=3.0):
    n=int(ln*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for k in range(1,9):
        for det in (0,1.5):
            s+=np.sin(2*np.pi*f*k*(1+det/1200)*tt)/(k**1.8)*np.exp(-tt*(0.9+k*0.55))
    s[:int(.004*SR)]*=np.linspace(0,1,int(.004*SR)); return s*g
def kick(g=1.0,dec=0.3):
    n=int(.45*SR); tt=np.arange(n)/SR; f=45+95*np.exp(-tt/0.045)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/dec)*g
def hat(g):
    n=int(.06*SR); x=np.diff(np.concatenate([[0],rng.normal(0,1,n)])); return x*np.exp(-np.arange(n)/SR/0.012)*g
def clap(g):
    n=int(.25*SR); x=np.diff(np.concatenate([[0],rng.normal(0,1,n)])); e=np.zeros(n)
    for o in (0,.012,.024): i=int(o*SR); e[i:]+=np.exp(-np.arange(n-i)/SR/0.05)
    return x*e*g
def pluck(f,g,dec=.16):
    n=int(.6*SR); tt=np.arange(n)/SR; return (np.sin(2*np.pi*f*tt)+.35*np.sin(4*np.pi*f*tt)+.12*np.sin(6*np.pi*f*tt))*np.exp(-tt/dec)*g
def tick(g):
    n=int(.03*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*2400*tt)*np.exp(-tt/0.004)*g
def riser(a,b,g):
    n=int((b-a)*SR); k=np.linspace(0,1,n); x=rng.normal(0,1,n); lp=np.convolve(x,np.ones(40)/40,'same')
    return ((lp*(1-k)+x*k*.5)*k**2+np.sin(2*np.pi*np.cumsum(200+1400*k**2)/SR)*k**2*.4)*g
def impact(g):
    n=int(2.8*SR); tt=np.arange(n)/SR; f=38+60*np.exp(-tt/0.08)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/0.75)+np.convolve(rng.normal(0,1,n),np.ones(25)/25,'same')*np.exp(-tt/0.35)*.8)*g
# ===== ACT 1 (0 - 28.8): melancholic
A1=[[220.0,261.63,329.63],[174.61,220.0,261.63],[146.83,174.61,220.0],[164.81,207.65,246.94]]
A1root=[55.0,43.65,36.71,41.2]
MEL=[[659.25,523.25,440.0],[523.25,440.0,349.23],[587.33,698.46,440.0],[493.88,415.3,329.63]]
CL1=4.0
for ci in range(8):
    st=ci*CL1
    if st>=28.8: break
    lvl=.03 if st<20 else .022
    add(pad(A1[ci%4],CL1+1.8,lvl),st,1,0,.6)
    n=int((CL1+1.5)*SR); tt=np.arange(n)/SR
    add(np.sin(2*np.pi*A1root[ci%4]*2*tt)*env(n,1.0,1.5)*.05,st,1,0,.1)
    if 4.0<=st<20.0:
        for j,f in enumerate(MEL[ci%4]): add(piano(f,.06),st+j*1.0,1,(-.25+.25*j),.7)
        add(piano(MEL[ci%4][0]/2,.035),st+3.0,1,0,.7)
# heartbeat + clock ticks during the journey
hb=4.0
while hb<20.0:
    gg=.18+.12*min(1,(hb-4)/16); add(kick(gg,.18),hb); add(kick(gg*.7,.16),hb+.24); hb+=1.05
tk=4.0
while tk<20.0: add(tick(.05),tk,1,.4); tk+=1.0
# act1 ending: low drone through stat scene, single piano notes
n=int(9*SR); tt=np.arange(n)/SR
add(np.sin(2*np.pi*55*tt)*env(n,1.5,2.5)*.06+np.sin(2*np.pi*110*tt)*env(n,1.5,2.5)*.02,20.0,1,0,.3)
for tt0,f in [(21.4,440.0),(23.0,392.0),(24.6,329.63)]: add(piano(f,.05,4),tt0,1,0,.8)
add(riser(26.6,28.8,.11),26.6,1,0,.3); add(impact(.45),28.8,1,0,.6)
# ===== ACT 2 (28.8 - 60): hopeful, building
BEAT=0.6; CL2=8*BEAT
A2=[[174.61,220.0,261.63],[261.63,329.63,392.0],[196.0,246.94,293.66],[220.0,261.63,329.63]]
A2root=[43.65,65.41,49.0,55.0]
duck=np.ones(N)
ci=0; st=28.8
while st<60:
    lvl=.032 if st<72.0 else .04
    add(pad(A2[ci%4],CL2+1.8,lvl),st,1,0,.55)
    n=int((CL2+1.4)*SR); tt=np.arange(n)/SR
    bm=((st+tt)>=33.4)&((st+tt)<72.2)
    add((np.sin(2*np.pi*A2root[ci%4]*2*tt)*.9+.25*np.sin(2*np.pi*A2root[ci%4]*4*tt))*env(n,.05,.4)*bm*.09,st,1,0,.05)
    ci+=1; st+=CL2
b=33.4
while b<72.0:
    add(kick(.55),b); i=int(b*SR); n=min(int(.35*SR),N-i); duck[i:i+n]=np.minimum(duck[i:i+n],1-.45*np.exp(-np.arange(n)/SR/0.11)); b+=BEAT
b=40.2
while b<72.0:
    add(hat(.10),b+BEAT/2,1,.3); add(hat(.04),b+BEAT/4,1,-.3); add(hat(.04),b+3*BEAT/4,1,-.3); b+=BEAT
b=40.2+BEAT
while b<72.0: add(clap(.10),b,1,0,.4); b+=2*BEAT
b=33.4; s=0
while b<72.0:
    c=A2[int((b-28.8)//CL2)%4]; notes=[x*2 for x in c]+[c[0]*4]
    add(pluck(notes[s%4],.045),b,1,(.4 if s%2 else -.4),.5); b+=BEAT/2; s+=1
# event sounds
for i,f in enumerate([987.77,1318.5]):
    n=int(.9*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*f*tt)*np.exp(-tt/.25)*.07,36.1+i*.14,1,(-.3 if i==0 else .3),.6)
add(impact(.18),36.1,1,0,.4)
for i,f in enumerate([659.25,880.0,1046.5]): add(pluck(f,.06,.35),37.8+i*.08,1,.2,.7)
pent=[523.25,587.33,659.25,783.99,880.0,1046.5]
for i in range(6): add(pluck(pent[i],.07,.3),66.8+1.6+i*.42+.1,1,(.5-.2*i),.7)
add(impact(.28),48.53,1,0,.5)
for i,f in enumerate([987.77,1318.5]):
    n=int(.9*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*f*tt)*np.exp(-tt/.25)*.08,48.53+i*.14,1,(-.3 if i==0 else .3),.6)
for i in range(5): add(pluck([523.25,311.13,587.33,659.25,783.99][i],.05 if i!=1 else .03,.25),51.0+.6+i*.42+.25,1,.3,.6)
for i in range(3): add(pluck([659.25,783.99,1046.5][i],.06,.3),57.2+1.3+i*.45+.1,1,-.2,.7)
for i in range(4): add(pluck([523.25,659.25,783.99,1046.5][i],.06,.3),62.0+.9+i*.7,1,.2*(i-1.5),.7)
add(riser(73.2,74.9,.10),73.2,1,0,.3); add(impact(.5),74.9,1,0,.75)
for i,f in enumerate([698.46,880.0,1046.5,1396.9]): add(pluck(f,.05,.5),74.9+i*.09,1,(i-1.5)/2,.85)
L*=.6+.4*duck; R*=.6+.4*duck
irn=int(2.6*SR); tir=np.arange(irn)/SR
def ir(seed):
    r=np.random.default_rng(seed).normal(0,1,irn)*np.exp(-tir/0.6); r[:int(.02*SR)]=0; return r/np.sqrt(np.sum(r**2))
def fconv(x,h):
    m=1<<int(np.ceil(np.log2(len(x)+len(h)))); return np.fft.irfft(np.fft.rfft(x,m)*np.fft.rfft(h,m),m)[:len(x)]
L+=fconv(vL,ir(3))*.5; R+=fconv(vR,ir(4))*.5
fade=np.ones(N); fi=int(1.0*SR); fade[:fi]=np.linspace(0,1,fi); fo=int(3.0*SR); fade[-fo:]=np.linspace(1,0,fo)**1.5
L*=fade; R*=fade; mx=max(np.abs(L).max(),np.abs(R).max()); L/=mx; R/=mx
L=np.tanh(L*1.4)/np.tanh(1.4); R=np.tanh(R*1.4)/np.tanh(1.4)
st=np.stack([L,R],1)*.9
with wave.open('ad/music3.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
print('music3 ok')
