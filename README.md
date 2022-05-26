# draw_char_curve

Draw characteristic curve of tactile sensors

Procedures:

1. Get the force and sensor response time series
2. Align the two time series by peaks.
3. Resample by sliding window. It makes the two time series have the same sampling rate.
4. Generate a force-response plot.