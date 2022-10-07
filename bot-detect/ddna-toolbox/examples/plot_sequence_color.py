"""
==================
Sequences by Color
==================

An example plot of :class:`digitaldna.TwitterDDNASequencer`
"""
from digitaldna import TwitterDDNASequencer
from digitaldna import SequencePlots
import numpy as np

# Generate DDNA from Twitter
model = TwitterDDNASequencer(input_file='timelines.json', alphabet='b3_type')
arr = model.fit_transform()

# Simulate bots by repeating 10 times the first timeline
nrep_arr = [10 if i == 0 else 1 for i in range(len(arr))]
arr = np.repeat(arr, nrep_arr, axis=0)
arr[:, 0] = np.random.randint(0, high=10100, size=len(arr))

# Plot results
plotter = SequencePlots(alphabet='b3_type')
plotter.plot_sequences_color(arr[:, 1])
