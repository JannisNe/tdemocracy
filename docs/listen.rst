Listening to the Kafka stream
=============================


You can set up your own `Hopskotch`_ client and listen to the messages sent over the corresponding Kafka topic.

.. _Hopskotch: https://scimma.org/hopskotch

There is a lightweight function that does all that for you if you want to offload these 20 lines:

.. autofunction:: tdemocracy.listen.listen_to_nuclear_stream


Iterate through the generator to start listening:::

    for report in listen_to_nuclear_stream():
        # run your classification
        ...
