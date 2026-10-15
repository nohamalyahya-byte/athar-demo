import numpy as np, wave, json
T=json.load(open('ad/timeline.json')); SR=44100; DUR=T['DUR']; N=int(SR*DUR)
rng=np.random.default_rng(21)
L=np.zeros(N); R=np.zeros(N); vL=np.zeros(N); vR=np.zeros(N)
def add(sig,start,gain=1.0,pan=0.0,verb=0.0):
    i=int(start*SR)
    if i>=N or i<0: return
    n=min(len(sig),N-i); s=sig[:n]*gain; l=s*np.sqrt((1-pan)/2); r=s*np.sqrt((1+pan)/2)
    L[i:i+n]+=l; R[i:i+n]+=r; vL[i:i+n]+=l*verb; vR[i:i+n]+=r*verb
def env(n,a,r):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR)); e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr); return e
def pad(freqs,ln,lvl,a=1.2,r=1.8):
    n=int(ln*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for f in freqs:
        for det in (-7,0,7):
            for k in range(1,7): s+=np.sin(2*np.pi*f*2**(det/1200)*k*tt+rng.uniform(0,6.28))/(k**1.5)
    return s*env(n,a,r)*lvl
def piano(f,g,ln=3.0):
    n=int(ln*SR); tt=np.arange(n)/SR; s=np.zeros(n)
    for k in range(1,9):
        for det in (0,1.5): s+=np.sin(2*np.pi*f*k*(1+det/1200)*tt)/(k**1.8)*np.exp(-tt*(0.9+k*0.55))
    s[:int(.004*SR)]*=np.linspace(0,1,int(.004*SR)); return s*g
def kick(g=1.0,dec=0.3):
    n=int(.45*SR); tt=np.arange(n)/SR; f=45+95*np.exp(-tt/0.045); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/dec)*g
def hat(g):
    n=int(.06*SR); x=np.diff(np.concatenate([[0],rng.normal(0,1,n)])); return x*np.exp(-np.arange(n)/SR/0.012)*g
def clap(g):
    n=int(.25*SR); x=np.diff(np.concatenate([[0],rng.normal(0,1,n)])); e=np.zeros(n)
    for o in (0,.012,.024): i=int(o*SR); e[i:]+=np.exp(-np.arange(n-i)/SR/0.05)
    return x*e*g
def pluck(f,g,dec=.16):
    n=int(.7*SR); tt=np.arange(n)/SR; return (np.sin(2*np.pi*f*tt)+.35*np.sin(4*np.pi*f*tt)+.12*np.sin(6*np.pi*f*tt))*np.exp(-tt/dec)*g
def tick(g):
    n=int(.03*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*2400*tt)*np.exp(-tt/0.004)*g
def riser(a,b,g):
    n=int((b-a)*SR); k=np.linspace(0,1,n); x=rng.normal(0,1,n); lp=np.convolve(x,np.ones(40)/40,'same')
    return ((lp*(1-k)+x*k*.5)*k**2+np.sin(2*np.pi*np.cumsum(200+1400*k**2)/SR)*k**2*.4)*g
def impact(g):
    n=int(2.8*SR); tt=np.arange(n)/SR; f=38+60*np.exp(-tt/0.08)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/0.75)+np.convolve(rng.normal(0,1,n),np.ones(25)/25,'same')*np.exp(-tt/0.35)*.8)*g
def whoosh(g,ln=.5):
    n=int(ln*SR); k=np.linspace(0,1,n); x=np.convolve(rng.normal(0,1,n),np.ones(18)/18,'same'); return x*np.sin(np.pi*k)**2*g
J0=T['j0']; JE=T['nc']; LOGO=T['logo']; HOW=T['how']; DASH=T['dash']; BEC=T['bec']; END=T['end']
# ACT 1 melancholic
A1=[[220.0,261.63,329.63],[174.61,220.0,261.63],[146.83,174.61,220.0],[164.81,207.65,246.94]]
A1r=[55.0,43.65,36.71,41.2]; MEL=[[659.25,523.25,440.0],[523.25,440.0,349.23],[587.33,698.46,440.0],[493.88,415.3,329.63]]
st=0.0; ci=0
while st<LOGO:
    ln=min(4.0,LOGO-st)+1.8; add(pad(A1[ci%4],ln,.03 if st<JE else .022),st,1,0,.6)
    n=int(ln*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*A1r[ci%4]*2*tt)*env(n,1.0,1.5)*.05,st,1,0,.1)
    if J0-.1<=st<JE:
        for j,f in enumerate(MEL[ci%4]): add(piano(f,.06),st+j*1.0,1,(-.25+.25*j),.7)
    st+=4.0; ci+=1
for i in range(6): add(whoosh(.05),T[f'j{i}']-.1,1,-.3,.3)
hb=J0
while hb<JE: g=.16+.12*(hb-J0)/(JE-J0); add(kick(g,.18),hb); add(kick(g*.7,.16),hb+.24); hb+=1.05
tk=J0
while tk<JE: add(tick(.045),tk,1,.4); tk+=1.0
n=int((LOGO-JE+1)*SR); tt=np.arange(n)/SR
add((np.sin(2*np.pi*55*tt)+.35*np.sin(2*np.pi*110*tt))*env(n,1.2,1.5)*.055,JE,1,0,.3)
add(piano(440.0,.06,4),JE+.25,1,0,.8); add(piano(392.0,.05,4),T['stat']+.4,1,0,.8); add(piano(329.63,.05,4),T['what']+.2,1,0,.8)
add(riser(LOGO-2.0,LOGO,.11),LOGO-2.0,1,0,.3); add(impact(.45),LOGO,1,0,.6)
# ACT 2 hopeful
BEAT=0.6; CL=8*BEAT; A2=[[174.61,220.0,261.63],[261.63,329.63,392.0],[196.0,246.94,293.66],[220.0,261.63,329.63]]; A2r=[43.65,65.41,49.0,55.0]
duck=np.ones(N); st=LOGO; ci=0
while st<DUR:
    add(pad(A2[ci%4],CL+1.8,.032 if st<BEC else .04),st,1,0,.55)
    n=int((CL+1.4)*SR); tt=np.arange(n)/SR; bm=((st+tt)>=HOW)&((st+tt)<BEC+.3)
    add((np.sin(2*np.pi*A2r[ci%4]*2*tt)*.9+.25*np.sin(2*np.pi*A2r[ci%4]*4*tt))*env(n,.05,.4)*bm*.09,st,1,0,.05); st+=CL; ci+=1
b=HOW
while b<BEC:
    add(kick(.55),b); i=int(b*SR); n=min(int(.35*SR),N-i); duck[i:i+n]=np.minimum(duck[i:i+n],1-.45*np.exp(-np.arange(n)/SR/0.11)); b+=BEAT
b=DASH
while b<BEC: add(hat(.10),b+BEAT/2,1,.3); add(hat(.04),b+BEAT/4,1,-.3); add(hat(.04),b+3*BEAT/4,1,-.3); b+=BEAT
b=DASH+BEAT
while b<BEC: add(clap(.09),b,1,0,.4); b+=2*BEAT
b=HOW; s=0
while b<BEC:
    c=A2[int((b-LOGO)//CL)%4]; notes=[x*2 for x in c]+[c[0]*4]; add(pluck(notes[s%4],.04),b,1,(.4 if s%2 else -.4),.5); b+=BEAT/2; s+=1
for i in range(3): add(pluck([523.25,659.25,783.99][i],.07,.35),HOW+.9+i*1.5,1,0,.7)
t30=T['timer']+2.929; add(impact(.25),t30,1,0,.5)
for i,f in enumerate([987.77,1318.5]):
    n=int(.9*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*f*tt)*np.exp(-tt/.25)*.08,t30+i*.14,1,(-.3 if i==0 else .3),.6)
for i in range(4): add(pluck([523.25,587.33,659.25,783.99][i],.045,.25),T['prio']+.5+i*.4+.3,1,.3,.6)
for i in range(3): add(pluck([659.25,783.99,1046.5][i],.055,.3),T['cons']+1.3+i*.4+.1,1,-.2,.7)
pent=[523.25,587.33,659.25,783.99,880.0,1046.5]
for i in range(6): add(pluck(pent[i],.07,.3),T['done']+1.6+i*.42+.1,1,(.5-.2*i),.7)
add(riser(END-1.7,END,.10),END-1.7,1,0,.3); add(impact(.5),END,1,0,.75)
for i,f in enumerate([698.46,880.0,1046.5,1396.9]): add(pluck(f,.05,.5),END+i*.09,1,(i-1.5)/2,.85)
L*=.6+.4*duck; R*=.6+.4*duck
irn=int(2.6*SR); tir=np.arange(irn)/SR
def ir(seed):
    r=np.random.default_rng(seed).normal(0,1,irn)*np.exp(-tir/0.6); r[:int(.02*SR)]=0; return r/np.sqrt(np.sum(r**2))
def fconv(x,h):
    m=1<<int(np.ceil(np.log2(len(x)+len(h)))); return np.fft.irfft(np.fft.rfft(x,m)*np.fft.rfft(h,m),m)[:len(x)]
L+=fconv(vL,ir(3))*.5; R+=fconv(vR,ir(4))*.5
fade=np.ones(N); fi=int(1.0*SR); fade[:fi]=np.linspace(0,1,fi); fo=int(3.5*SR); fade[-fo:]=np.linspace(1,0,fo)**1.5
L*=fade; R*=fade; mx=max(np.abs(L).max(),np.abs(R).max()); L/=mx; R/=mx
L=np.tanh(L*1.4)/np.tanh(1.4); R=np.tanh(R*1.4)/np.tanh(1.4)
with wave.open('ad/music4.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([L,R],1)*.9*32767).astype('<i2').tobytes())
print('music4 ok',DUR)
