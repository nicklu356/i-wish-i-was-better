"""
Generates the game's sound effects in game/audio/sfx/.

Every sound is synthesized from scratch here (sine waves, filtered noise and
envelopes), so they are original works made for this game, with no samples or
third-party recordings involved. They are released under CC0.

Needs numpy and ffmpeg (with libvorbis). Run from the project root:

    python3 tools/make_sfx.py
"""

import os
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "game", "audio", "sfx")

rng = np.random.default_rng(1234)


def t_axis(dur):
    return np.arange(int(SR * dur)) / SR


def fade(x, fin=0.004, fout=0.01):
    """Short fades so nothing clicks at the ends."""
    x = x.copy()
    a, b = int(SR * fin), int(SR * fout)
    if a:
        x[:a] *= np.linspace(0, 1, a)
    if b:
        x[-b:] *= np.linspace(1, 0, b)
    return x


def place(buf, x, at):
    i = int(SR * at)
    buf[i:i + len(x)] += x[:len(buf) - i]


def sweep(f0, f1, dur, shape="exp"):
    """A sine whose pitch glides from f0 to f1."""
    t = t_axis(dur)
    if shape == "exp":
        f = f0 * (f1 / f0) ** (t / dur)
    else:
        f = f0 + (f1 - f0) * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def bandpass_noise(dur, centers, q=4.0):
    """White noise through a band-pass whose center moves along `centers`."""
    n = int(SR * dur)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    # State-variable filter, retuned every sample.
    low = band = 0.0
    fc = np.interp(np.arange(n), np.linspace(0, n - 1, len(centers)), centers)
    for i in range(n):
        f = 2 * np.sin(np.pi * fc[i] / SR)
        high = noise[i] - low - band / q
        band += f * high
        low += f * band
        out[i] = band
    return out


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def bell(freq, dur, tau):
    """A soft bell / glass tone."""
    t = t_axis(dur)
    x = (np.sin(2 * np.pi * freq * t)
         + 0.35 * np.sin(2 * np.pi * freq * 2.0 * t) * np.exp(-t / (tau * 0.5))
         + 0.12 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t / (tau * 0.3)))
    return fade(x * np.exp(-t / tau), 0.003)


def marimba(freq, dur):
    t = t_axis(dur)
    x = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.22)
         + 0.25 * np.sin(2 * np.pi * freq * 3.93 * t) * np.exp(-t / 0.03)
         + 0.08 * np.sin(2 * np.pi * freq * 9.2 * t) * np.exp(-t / 0.01))
    return fade(x, 0.002)


def normalize(x, peak):
    return x / np.max(np.abs(x)) * peak


# Sounds ######################################################################

def message():
    """Incoming text notification: two rising chime notes."""
    buf = np.zeros(int(SR * 0.9))
    place(buf, bell(987.77, 0.7, 0.22), 0.0)      # B5
    place(buf, bell(1318.51, 0.75, 0.28), 0.11)   # E6
    return normalize(fade(buf), 0.6)


def pop():
    """A chat bubble from the other person appearing."""
    dur = 0.11
    t = t_axis(dur)
    x = sweep(950, 520, dur) * np.exp(-t / 0.035)
    return normalize(fade(x, 0.002, 0.02), 0.35)


def send():
    """The player sending a message: a short upward swoosh."""
    dur = 0.24
    t = t_axis(dur)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    air = bandpass_noise(dur, [700, 1600, 3200], q=3.0) * env
    blip = sweep(620, 1050, dur) * np.exp(-((t - 0.14) / 0.05) ** 2)
    x = normalize(air, 1.0) * 0.7 + blip * 0.35
    return normalize(fade(x), 0.35)


def ringtone():
    """A marimba ringtone, two seconds, loops seamlessly."""
    buf = np.zeros(int(SR * 2.0))
    notes = [659.25, 830.61, 987.77, 1318.51, 987.77, 830.61, 987.77, 1318.51]
    for i, f in enumerate(notes):
        place(buf, marimba(f, 0.6), i * 0.13)
    return normalize(fade(buf, 0.002, 0.05), 0.55)


def vibrate():
    """A phone buzzing on a table: two buzzes."""
    buf = np.zeros(int(SR * 0.95))
    dur = 0.36
    t = t_axis(dur)
    motor = np.tanh(3 * np.sin(2 * np.pi * 165 * t))
    rattle = bandpass_noise(dur, [2400], q=2.0) * (0.5 + 0.5 * np.sin(2 * np.pi * 165 * t))
    burst = lowpass(motor + 0.25 * normalize(rattle, 1.0), 3000)
    burst = fade(burst, 0.02, 0.03)
    place(buf, burst, 0.0)
    place(buf, burst, 0.52)
    return normalize(buf, 0.55)


def heartbeat():
    """Three nervous heartbeats, fading out."""
    def thump(f0, f1, decay, gain):
        dur = 0.22
        t = t_axis(dur)
        x = sweep(f0, f1, dur) * np.exp(-t / decay)
        # A little drive so it is still heard on small speakers.
        return fade(np.tanh(2.5 * x) * gain, 0.003, 0.03)

    buf = np.zeros(int(SR * 2.6))
    for i, g in enumerate([1.0, 0.85, 0.65]):
        at = i * 0.8
        place(buf, thump(90, 48, 0.07, g), at)
        place(buf, thump(105, 58, 0.05, g * 0.7), at + 0.26)
    return normalize(lowpass(buf, 900), 0.8)


SOUNDS = {
    "message": message,
    "pop": pop,
    "send": send,
    "ringtone": ringtone,
    "vibrate": vibrate,
    "heartbeat": heartbeat,
    }


def write_ogg(name, x):
    os.makedirs(OUT, exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav = f.name

    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    path = os.path.join(OUT, name + ".ogg")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav,
         "-c:a", "libvorbis", "-q:a", "5", "-map_metadata", "-1", path],
        check=True)
    os.unlink(wav)
    print(os.path.normpath(path))


if __name__ == "__main__":
    for name, make in SOUNDS.items():
        write_ogg(name, make())
