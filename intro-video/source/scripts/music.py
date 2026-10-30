"""Synthesize an original ambient score for the intro video (no samples, no licensing)."""
import sys
import wave
import numpy as np

SR = 48000
DUR = 69.5
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(11)


def hz(note):
    names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    n, o = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o + 1) - 69) / 12)


# (start, end, pad voicing, bass root, arp tones)
CHORDS = [
    (0, 6, ['D3', 'A3', 'C#4', 'E4', 'F#4'], 'D2', ['D4', 'F#4', 'A4', 'C#5', 'E5']),
    (6, 12, ['B2', 'F#3', 'A3', 'D4', 'C#4'], 'B1', ['B3', 'D4', 'F#4', 'A4', 'C#5']),
    (12, 18, ['G2', 'D3', 'F#3', 'B3', 'A3'], 'G1', ['G3', 'B3', 'D4', 'F#4', 'A4']),
    (18, 24, ['A2', 'E3', 'B3', 'C#4', 'E4'], 'A1', ['A3', 'C#4', 'E4', 'B4', 'C#5']),
    (24, 30, ['D3', 'A3', 'C#4', 'E4', 'F#4'], 'D2', ['D4', 'F#4', 'A4', 'C#5', 'E5']),
    (30, 36, ['B2', 'F#3', 'A3', 'D4', 'C#4'], 'B1', ['B3', 'D4', 'F#4', 'A4', 'C#5']),
    (36, 42, ['G2', 'D3', 'F#3', 'B3', 'A3'], 'G1', ['G3', 'B3', 'D4', 'F#4', 'A4']),
    (42, 48, ['A2', 'E3', 'B3', 'C#4', 'E4'], 'A1', ['A3', 'C#4', 'E4', 'B4', 'C#5']),
    (48, 54, ['B2', 'F#3', 'A3', 'D4', 'C#4'], 'B1', ['B3', 'D4', 'F#4', 'A4', 'C#5']),
    (54, 60, ['G2', 'D3', 'F#3', 'B3', 'A3'], 'G1', ['G3', 'B3', 'D4', 'F#4', 'A4']),
    (60, 63, ['A2', 'E3', 'B3', 'C#4', 'E4'], 'A1', ['A3', 'C#4', 'E4', 'B4', 'C#5']),
    (63, DUR, ['D3', 'A3', 'C#4', 'E4', 'F#4'], 'D2', ['D4', 'F#4', 'A4', 'C#5', 'E5']),
]


def env(n, attack, release, sustain_len):
    """Linear-ish attack, hold, then cosine release; length n samples."""
    e = np.ones(n)
    a = int(attack * SR)
    r = int(release * SR)
    if a > 0:
        e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    s_end = int(sustain_len * SR)
    if s_end < n:
        rl = min(r, n - s_end)
        e[s_end:s_end + rl] = np.cos(np.linspace(0, np.pi / 2, rl)) ** 2
        e[s_end + rl:] = 0
    return e


L = np.zeros(N)
R = np.zeros(N)


def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i < 0:
        sig, i = sig[-i:], 0
    j = min(N, i + len(sig))
    if j <= i:
        return
    lg = np.cos((pan + 1) * np.pi / 4) * gain
    rg = np.sin((pan + 1) * np.pi / 4) * gain
    L[i:j] += sig[:j - i] * lg
    R[i:j] += sig[:j - i] * rg


# --- Pad: detuned additive voices, slow swell, overlapping chord changes
for (s, e, voicing, bass, _) in CHORDS:
    length = (e - s) + 2.2
    n = int(length * SR)
    tt = np.arange(n) / SR
    en = env(n, 1.6, 2.2, e - s)
    for k, note in enumerate(voicing):
        f = hz(note)
        voice = np.zeros(n)
        for det in (-0.006, 0.0, 0.0065):
            ff = f * (1 + det)
            ph = rng.uniform(0, 2 * np.pi)
            for h, amp in ((1, 1.0), (2, 0.32), (3, 0.12), (4, 0.05)):
                voice += amp * np.sin(2 * np.pi * ff * h * tt + ph * h)
        trem = 1 + 0.12 * np.sin(2 * np.pi * (0.13 + 0.03 * k) * tt + k)
        add(voice * en * trem / 3, s - 0.4, pan=(k - 2) * 0.28, gain=0.030)
    # Bass: warm sine with a touch of 2nd harmonic
    fb = hz(bass)
    bs = (np.sin(2 * np.pi * fb * tt) + 0.25 * np.sin(4 * np.pi * fb * tt)) * env(n, 0.8, 2.0, e - s)
    add(bs, s - 0.2, gain=0.045)

# --- Arpeggio: soft bell/piano plucks on eighth notes
BEAT = 60 / 80
STEP = BEAT / 2
PATTERN = [0, 2, 4, 1, 3, 2, 4, 3]


def pluck(f, dur=1.6, bright=1.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    sig = (np.sin(2 * np.pi * f * tt) + 0.35 * bright * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 3)
           + 0.12 * bright * np.sin(6 * np.pi * f * tt) * np.exp(-tt * 6))
    a = int(0.004 * SR)
    sig[:a] *= np.linspace(0, 1, a)
    return sig * np.exp(-tt * 2.6)


step_i = 0
tcur = 6.0
while tcur < 63.0:
    chord = next(c for c in CHORDS if c[0] <= tcur < c[1])
    tones = chord[4]
    f = hz(tones[PATTERN[step_i % 8]])
    if step_i % 16 >= 8 and PATTERN[step_i % 8] in (3, 4):
        f *= 2  # lift the top of every other phrase an octave
    vel = 0.75 + 0.25 * np.sin(step_i * 1.7) ** 2
    if step_i % 2 == 0:
        vel *= 1.12
    ramp = min(1.0, (tcur - 6.0) / 3.0)
    add(pluck(f), tcur + rng.uniform(-0.006, 0.006), pan=0.35 * np.sin(step_i * 0.9), gain=0.05 * vel * ramp)
    step_i += 1
    tcur += STEP

# Outro: slower, resolving arpeggio on D
for i, note in enumerate(['D4', 'F#4', 'A4', 'C#5', 'E5', 'A5']):
    add(pluck(hz(note), 3.5, 0.8), 63.0 + i * BEAT * 0.75, pan=-0.4 + i * 0.16, gain=0.05)

# --- Accents: low swell + shimmer on the name reveal and the outro
def boom(dur=3.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 55 * np.exp(-tt * 0.6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.6) * np.minimum(1, tt / 0.02)


def shimmer(dur=3.0, base=1760):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * base * m * tt + m) for m in (1, 1.5, 2.0, 2.5)) / 4
    return sig * np.exp(-tt * 1.5) * np.minimum(1, tt / 0.3)


def riser(dur=1.8):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    # crude low-pass by moving average, opening up over time
    out = np.convolve(noise, np.ones(24) / 24, mode='same')
    return out * np.linspace(0, 1, n) ** 2.2


for at in (1.1, 63.0):
    add(boom(), at, gain=0.16)
    add(shimmer(), at, pan=-0.3, gain=0.018)
    add(shimmer(base=2217), at + 0.05, pan=0.3, gain=0.014)
for at in (6.0, 40.5, 57.0):
    add(riser(), at - 1.8, gain=0.028)

# --- Reverb: FFT convolution with decaying stereo noise IR
def ir(seed, length=2.8):
    g = np.random.default_rng(seed)
    n = int(length * SR)
    tt = np.arange(n) / SR
    h = g.standard_normal(n) * np.exp(-tt * 2.4)
    h = np.convolve(h, np.ones(8) / 8, mode='same')  # darken the tail
    h[:int(0.012 * SR)] = 0
    return h / np.sqrt(np.sum(h ** 2))


def convolve(x, h):
    m = len(x) + len(h) - 1
    size = 1 << (m - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(h, size), size)[:len(x)]
    return y


wetL = convolve(L, ir(1))
wetR = convolve(R, ir(2))
outL = L * 0.72 + wetL * 0.38
outR = R * 0.72 + wetR * 0.38

# Master fades
fade_in = np.minimum(1, t_all / 1.2)
fade_out = np.clip((DUR - t_all) / 3.0, 0, 1) ** 1.5
outL *= fade_in * fade_out
outR *= fade_in * fade_out
peak = max(np.abs(outL).max(), np.abs(outR).max())
outL, outR = outL / peak * 0.89, outR / peak * 0.89

stereo = np.empty(N * 2, dtype=np.int16)
stereo[0::2] = (outL * 32767).astype(np.int16)
stereo[1::2] = (outR * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())
print('wrote', sys.argv[1], f'{DUR}s')
