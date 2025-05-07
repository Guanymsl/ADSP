## Requirements

```bash
python3 -m venv adsp
source adsp/bin/activate
pip3 install -r requirements.txt
```

---

## Usage

```bash
python getmusic.py \
    --score <note1> <note2> ...    \
    --beat  <beat1> <beat2> ...    \
    --name  <output-name>          \
    [--bpm <bpm>]                  \
    [--key <key>]                  \
    [--octave <octave>]            \
    [--mode <mode>]                \
    [--volume <0.0–1.0>]           \
    [--standard <Hz>]
```

* `--score`
  A sequence of integers (1–7) representing scale degrees; use `0` for rest.  
  **Example:** `--score 1 1 5 5 6 6 5`
* `--beat`
  A sequence of floats/ints (same length as `--score`) indicating each note’s duration in quarter-note units.  
  **Example:** `--beat 1 1 1 1 1 1 2`
* `--name`
  Output filename (without `.wav`), saved to `./results/<name>.wav`.  
  **Default:** `"default"`
* `--bpm` *(optional)*
  Tempo in beats per minute.  
  **Default:** `120.0`
* `--key` *(optional)*
  Musical key, one of `C, C#, D, D#, E, F, F#, G, G#, A, A#, B`.  
  **Default:** `C`
* `--octave` *(optional)*
  Octave number (1–7).  
  **Default:** `4`
* `--mode` *(optional)*
  Scale mode, one of `Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian`.  
  **Default:** `Ionian`
* `--volume` *(optional)*
  Volume level (0.0–1.0).  
  **Default:** `1.0`
* `--standard` *(optional)*
  Reference frequency for C4 in Hz.  
  **Default:** `261.63`

---

## Examples

**“Twinkle Twinkle Little Star”**

```bash
python getmusic.py \
    --score 1 1 5 5 6 6 5 4 4 3 3 2 2 1 \
    --beat  1 1 1 1 1 1 2 1 1 1 1 1 1 2 \
    --name  twinkle \
    --bpm   100
```

Generates `./results/twinkle.wav` at 100 BPM.

---
