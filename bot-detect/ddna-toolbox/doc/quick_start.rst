###############
Getting started
###############

This package provides a set of utilities and algorithms for online social bot
detection based on the paper `Social Fingerprinting: Detection of Spambot Groups Through
DNA-Inspired Behavioral Modeling <https://ieeexplore.ieee.org/document/7876716>`_


1. Download and setup digitaldna
--------------------------------

To install `digitaldna`, execute::

    $ pip install digitaldna

If the installation was successful, and `digitaldna` is correctly installed, you should be able
to execute the following Python code::

    from digitaldna.lcs import LongestCommonSubsequence

    X = ['banana', 'ananan', 'anana', 'hanoi', 'banas']
    estimator = LongestCommonSubsequence()
    estimator.fit_predict(X)



2. Sequence your first Digital DNA from Twitter
-----------------------------------------------

You can sequence an array of Twitter timelines by simply passing the json filename::

    from digitaldna import TwitterDDNASequencer

    model = TwitterDDNASequencer(input_file='timelines.json', alphabet='b3_type')
    arr = model.fit_transform()

Alternatively, if you have already loaded in memory the json array you can pass it as `X` parameter::

    from digitaldna import TwitterDDNASequencer

    X = [[{'user1':'tweet1'},{'user1':'tweet2'}],[{'user2':'tweet1'}]]
    model = TwitterDDNASequencer(X)
    arr = model.fit_transform()

The `arr` variable has shape (# of users, 2), the first column will contain the user id and the second the digital DNA 

3. Write your first Bot Detector
--------------------------------

Once you have your DDNA sequences you can launch the bot detection algorithm with these few lines of code::

    from digitaldna import LongestCommonSubsequence

    X = ['AAAABBAABABBB', 'AAABAABABBB', 'BAAABAABABBA', 'ABAABBBAB']
    estimator = LongestCommonSubsequence()
    y = estimator.fit_predict(X)

The `y` variable will contain a boolean array with the same length of `X`, where bot accounts are labeled as True and real accounts as False.