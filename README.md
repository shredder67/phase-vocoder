## About

A small program written as a test case during application to VK Marusya team. Program can be used as a console line tool to stretch/compress audio file without change of pitch by use of _phase vocoder_. In detail it consists of 3 following stages:

1. Analysis - Short-Time Fourier Transform
2. Processing - correction of phase values
3. Synthesis - Inverse STFT and summing up windows over new audio length

## Install and run

```
git clone git@github.com:shredder67/vocoder.git
cd vocoder
```

To run, simply copy this:

```
./run.sh [input_file.wav] [output_file.wav] [stretch_ratio]
```

## References

1. Guitar Pitch Tutorial Algorithm description [[url](https://www.guitarpitchshifter.com/algorithm.html)]
2. Awesome video on intuition behind FT in general [[url](https://www.youtube.com/watch?v=KxRmbtJWUzI)]
