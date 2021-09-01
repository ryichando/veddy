Using FFmpeg's Filters
======================

Veddy can be seen as an XML-wrapper to FFmpeg.
For this reason, Veddy naturally supports FFmpeg filters.
For example,

.. code-block:: xml

    <material name="video" path="video.mp4">
    <stream>
        <filter name="avgblur">
            <variable name="sizeX" value="5"/>
            <variable name="sizeY" value="5"/>
            <reference name="video"/>
        </filter>
    </stream>

will filter an input video that corresponds to the command

.. code-block::

    ffmpeg -i video.mp4 -vf avgblur=sizeX=5:sizeY=5 <filename>.mp4

However, it should be noted that when using FFmpeg's filter,
any dimensional, FPS, and the duration changes must
be explicitly declared as filter's attributes. For example,

.. code-block:: xml

    <pipe>
        <reference name="video"/>
        <filter name="trim" duration="3">
            <variable name="start" value="0"/>
            <variable name="end" value="3"/>
        </filter>
        <filter name="setpts">
            <variable value="PTS-STARTPTS"/>
        </filter>
    </pipe>

This operation changes the duration of a source video.
As you may infer, such a change of duration is dictated
in an attribute ``<filter>`` as ``duration="3"``.
Note that without the declaration, Veddy has no way of
detecting such duration change, and results in
mis-calculation of timings.
Here's the list of attributes
that must be declared in ``<filter>`` when changes
are expected

  - duration
  - fps
  - shape (or width, height)

For detail and examples, please see ``functions.xml``.
In general, the ``<filter>`` takes the form

.. code-block:: xml

    <filter name="filter_name">
        <variable value="value0"/>
        <variable name="var1" value="value1"/>
        <variable name="var2" value="value2"/>
    </filter>

This will be translated to

.. code-block:: bash

    ffmpeg ... -vf filter_name=value0:var1=value1:var2=value2 ...

.. note::

    Although it is still possible to directly use
    FFmpeg's filters as above, we strongly recommend
    using built-in compositions instead.
    This is because the use of filters needs
    careful checks of any changes of video size,
    FPS and duration.
    Compositions on the other hand
    take care such changes for you.

Defining New Composition
==========================
Composition delivers
high-level functionality of Veddy.
All the built-in compositions are defined in ``functions.xml``,
and you can define your own compositions to
further strengthen Veddy for your best needs.

As a good example, let's turn the above filter example
into a useful trim composition. Here's the result

.. code-block:: xml

    <function name="trim">
        <default name="start" value="0"/>
        <default name="end" value="3"/>
        <pipe>
            <input/>
            <filter name="trim" duration="eval($end-$start)">
                <variable name="start" value="$start"/>
                <variable name="end" value="$end"/>
            </filter>
            <filter name="setpts">
                <variable value="PTS-STARTPTS"/>
            </filter>
        </pipe>
    </function>

Let's examine the above code line by line.

  - The first tag ``<function>``
    declares a composition.
  - ``<default>`` tag defines arguments that can
    be passed through attributes.
    When the argument was not specified, declared
    default values are used.
    Arguments can be accessed with ``$`` prefix,
    like :ref:`Variables`. 
  - ``<input/>`` tag insert an input reference
    specified through the composition call.
    If multiple inputs are given, you can specify
    which to insert by ``<input index="(number)"/>``.
    If you want to simply insert them all, you can
    do it by ``<all_inputs/>``.
    See :ref:`input`, :ref:`all_inputs` for detail.

Now you can use the composition like

.. code-block:: xml

    <composite name="trim" start="2" end="3">
        <reference name="my_video"/>
    </composite>

which looks consistent with what you learned
in :ref:`Using Compositions`.