Installation
====================

Veddy is platform independent as it relies on a few open-source packages,
which are all in principle installable via major package managers
(e.g., apt-get or brew).
Nevertheless, we strongly recommend that you use our Dockerfile
since a set of tested FFmpeg/Python environments can be surely installed
this way\ [#docker]_.
Don't be intimidated, it won't compile anything; it will just fetch
a statically compiled binary from
`FFmpeg Static Builds <https://johnvansickle.com/ffmpeg/>`_
and do the rest of settings for you.
The whole installation procedure only takes a minutes, and your
PC stays cool.

If this sounds good to you, first make sure that you
have a latest copy of docker running via
`the official site <https://www.docker.com>`_.
Next, start with cloning the Veddy repository and move into it

.. code-block:: bash

   git clone https://github.com/ryichando/veddy.git
   cd veddy

and build the docker image

.. code-block:: bash

   docker build -t veddy .

and you are all set. You can now compile a set of examples by

.. code-block:: bash

   docker run -v ${PWD}:/veddy --rm veddy examples/*.xml

Wait for a moment while seeing the progress of video compilation.
Output videos will be generated in the ``./examples`` directory as 
things get done.
See demos and learn what Veddy can do before you proceed.

.. note::

   On Windows, be sure to use
   `PowerShell <https://docs.microsoft.com/en-us/powershell/>`_ because
   unfortunately ``${PWD}``
   is not recognizable on Windows Command Line (cmd). If you persist
   to stay with it, use ``%cd%`` instead.

Usage
-----
As indicated above, Veddy takes XML file input(s)

.. code-block:: bash

   docker run -v ${PWD}:/veddy --rm veddy <input_xml_file>

Be assured that this command comes with ``--rm`` flag, which means that
after the run, no suspended container is left; so things stay clean.
Keep in mind that you always execute Veddy in this handy manner.

Note that output path is not given via command line interface.
They are deduced by Veddy, or manually specified in the scene file
by :ref:`export` tag.

.. note::

   When only one unnamed stream is defined and no ``<export>`` tags
   are found, Veddy automatically picks the stream and
   export it to ``<filename>.mp4``\ .
   For convenience, forget everything about ``<export>`` at
   the moment.

Installing Launcher Script
------------------------------

For Linux and macOS users:
if you find that the above command is lengthy, or wish to
conveniently run Veddy anywhere outside Veddy directory,
you may create/install a launcher script

.. code-block:: bash

   # For Linux/macOS: here we create a launcher script
   # Make sure that you run this script in Veddy directory

   # Reachable port for remote preview; remember this
   PORT=8080

   # Install directory
   # Change to somewhere else (e.g., ${HOME}/bin ) if you wish
   INSTALL_DIR="/usr/local/bin"

   # Create script
   echo '#!/bin/bash
   docker run -v '${PWD}':/veddy -v ${PWD}:/mount \
   -p '${PORT}':8020 --rm veddy "$@"' > veddy
   chmod +x veddy

   # Install it to the destination path
   cp veddy ${INSTALL_DIR}; rm veddy

   # ---------------------------------------------------
   # Do not move Veddy directory hereafter.
   # If you do, just re-run this script in the new path.
   # ---------------------------------------------------

and instead run

.. code-block:: bash

   veddy <input_xml_file>

.. note::
   
   ``${PORT}`` is used for remote preview. See :ref:`Remote Preview`
   for detail.

For Windows users, you should be able to do the same by
creating ``.bat`` file and do something
(I rather leave to public web for how).

.. note::

   When specifying XML file(s) using the above command(s),
   check that all the associated files are located
   in the working directory (e.g.,\ ``${PWD}``)
   or its sub-directories.
   If some of them are outside ``${PWD}``, Veddy can't
   access them and eventually fails.

Keep Things Up-To-Date
-----------------------
If you find that your copy of Veddy is out-of-date; just run two lines

.. code-block:: bash

   git pull
   docker build -t veddy .

and your Veddy becomes fresh again.

Uninstalling Veddy
-------------------
If you exactly followed the above steps for running Veddy every time,
no containers should be left in your system.
If this is the case, simply run

.. code-block:: bash

   docker rmi veddy

If you have installed a launcher script as above, also run

.. code-block:: bash

   rm $(which veddy)

and you should have completely wiped Veddy out of your computer
(of course directory ``veddy`` still remains; be careful not to accidentally
lose what you have produced in it when deleting it).
If you believe that you have a suspended container, remove it first.

Minimal Example
====================
Working with Veddy is all about writing XML file(s).
To get a glimpse of what it looks like, let's see a minimal example that works

.. code-block:: xml

   <root version="0.0.1">
      <material name="cat" path="videos/cat.mp4"/>
      <material name="dog" path="videos/dog.mp4"/>
      <stream>
         <reference name="cat"/>
         <reference name="dog"/>
      </stream>
   </root>

This scene file loads two video footages (\ ``cat.mp4``,\ ``dog.mp4``)
and concatenates (towards time axis) them.
First, the scene file must begin
with ``<root version="0.0.1>"`` to declare the start of the scene.
Versioning number must be specified to avoid possible incompatibility
issue arising from future format change.

.. warning::

   When more than two videos are in a stream, they must have
   the same dimensions (width and height) and the FPS;
   otherwise compilation fails.

Transitions
---------------
You can easily apply transitions between video clips by adding a
``transition`` attribute to ``<stream>`` tag by

.. code-block:: xml

   <stream transition="fade">
      <reference name="cat"/>
      <reference name="dog"/>
   </stream>

where ``fade`` is a transition name. The list of available
transitions can be seen from https://trac.ffmpeg.org/wiki/Xfade

Material Import
---------------
Typically materials are imported first through :ref:`material` tag.
Several types of materials can be imported, such as regular videos,
image sequences and even URL pointed ones
(with basic password authentication).
Jump to :ref:`material` to learn how.

.. note::

   - It is not mandatory to import materials; we can improvise using
     :ref:`nullsrc` or :ref:`color` compositions, which is lightly covered
     in :ref:`Creating Solid Color Background`.

   - The path to the materials must be a relative path from the
     XML file; not from the working directory.

Declaring Movie Track
-----------------------
At least one :ref:`stream` tag must be included to dictate a video stream
to export. Multiple streams associated with a name attribute may
be declared and included (re-used) in other streams.
Please see :ref:`Re-using Streams` to know more.

Using Compositions
====================
Most of the functionality of Veddy is provided through compositions.
An example of usage is as follows

.. code-block:: xml

   <stream>
      <composite name="negate">
         <reference name="cat"/>
      </composite>
   </stream>

Here, the :ref:`negate` composition inverts the nested video source.
In general, nested inputs are passed to the parental composition and processed.
The processed outputs are then further passed to its parent
and processed likewise.
Generally, compositions take the form

.. code-block:: xml

   <composite name="(name)" param1="(value1)" param2="(value2)">
      <input1/>
      <input2/>
   </composite>

where the list of parameters and number of inputs are subject to the type
of compositions. The built-in compositions are programmed in an external
file ``functions.xml``, and their documentations are accessible
from the side menu.

.. note::

   Some compositions come with coordinate and duration parameters.
   The coordinate is in accordance with `FFmpeg <https://ffmpeg.org>`_,
   which sets the origin at the top-left corner. Unit is pixels.
   Duration is given in seconds.

Fluent Interface
----------------

When multiple compositions are applied in a nested fashion,
the above format compromises readability. For example,

.. code-block:: xml

   <stream>
      <composite name="comp_3rd">
         <composite name="comp_2nd">
            <composite name="comp_1st">
               <reference name="cat"/>
            </composite>
         </composite>
      </composite>
   </stream>

This is a valid syntax, but is also hard to follow at a glance.
To cope with the issue, Veddy provides a special tag :ref:`pipe` .
Using ``<pipe>`` , the above code can be simplified to

.. code-block:: xml

   <stream>
      <pipe>
         <reference name="cat"/>
         <composite name="comp_1st"/>
         <composite name="comp_2nd"/>
         <composite name="comp_3rd"/>
      </pipe>
   </stream>

Yes, this reads better. Using ``<pipe>`` , compositions are applied
from top to bottom in a sequential order, and subsequently passed to the parent
out of the scope when reaching ``</pipe>``. Hence, you may apply another
composition to the output such as

.. code-block:: xml

   <stream>
      <composite name="negate">
         <pipe>
            <reference name="cat"/>
            <composite name="comp_1st"/>
            <composite name="comp_2nd"/>
            <composite name="comp_3rd"/>
         </pipe>
      </composite>
   </stream>

which increases the flexibility of coding style.

Video Dimensions and FPS
======================================
Video dimensions and FPS are inferred from the output
unless explicitly specified via :ref:`config` tags. For example,

.. code-block:: xml

   <material name="cat" path="videos/cat.mp4"/>
   <stream>
      <reference name="cat"/>
   </stream>

will compile a video with both dimensions and FPS inherited from
the referenced material. On the other hand,

.. code-block:: xml

   <material name="cat" path="videos/cat.mp4"/>
   <stream>
      <!-- stitch two videos horizontally -->
      <composite name="hstack">
         <reference name="cat"/>
         <reference name="cat"/>
      </composite>
   </stream>

will double the width of the video, while retaining other
dimensions and the original FPS.
In the next section we show how to explicitly specify
dimensions and FPS.

.. note::

   When deducible, they are set as global parameters
   ``$_width_``, ``$_height_`` and ``$_fps_``.

Creating Solid Color Background
=================================
You can create a solid color canvas and play with it.
To do so, use :ref:`color` composition

.. code-block:: xml

   <config name="shape" value="900x540"/>
   <config name="fps" value="20"/>

   <stream>
      <pipe>
         <composite name="color" duration="3"/>
         <composite name="drawtext" text="Hello world!"/>
      </pipe>
   </stream>

This scene lays a solid black background of 3 seconds and draw a text
at its center. 

In this example, we specified the dimensions and FPS through :ref:`config`
tags. This is required because without it Veddy has no clue what
dimensions and FPS should be used to begin video compilation.
See :ref:`config` for detail.
For the list of configs, see :ref:`Specifying Video Settings`.
``<config>`` tags should be declared directly
under the ``<root>`` tag.

.. note::
    When video size and FPS are set through ``<config>``,
    output video must conform them.
    This is automatically done if you initialize a scene starting with
    :ref:`color` composition, like this example.

Default background color and the foreground color are set
black and white, respectively. You can change them by

.. code-block:: xml

   <root version="0.0.1">

      <global name="_bgcolor_" value="your_color"/> <!-- background -->
      <global name="_fgcolor_" value="your_color"/> <!-- foreground -->
      ...
   </root>

where ``your_color`` should be the
name of a color (e.g., ``red`` or ``blue``)
or a hex-encoded text (e.g., ``0xACF9B3`` ) according to
https://ffmpeg.org/ffmpeg-utils.html#Color.

.. note::

   ``<global>`` tags, which set global variables,
   should be placed directly under the ``<root>`` tag.
   They will be ignored if defined elsewhere.
   The same rule also applies to ``<config>`` tags.

Re-using Streams
====================
It is often a good idea to define another stream when
you plan to repeat (with some modification) the same
video track. For example,

.. code-block:: xml

   <material name="cat" path="videos/cat.mp4"/>

   <stream name="title">
      <composite name="title-slide" text="My Video Title"/>
   </stream>

   <stream>
      <reference name="title"/>
      <reference name="cat"/>
      <reference name="title"/> <!-- re-using the stream -->
   </stream>

will compile a video that starts with the title slide,
the cat video, and then the title slide again.
Notice that the stream named ``title`` was used twice
in the main stream. You may apply additional edits e.g.,

.. code-block:: xml

   <stream>
      <reference name="title"/>
      <reference name="cat"/>
      <composite name="negate">
         <reference name="title"/> <!-- negate the stream -->
      </composition>
   </stream>

.. warning::

   Be mindful not to make any recursion or loop when including
   other streams. Veddy will fail in such circumstances.

Exporting Multiple Streams
=============================
In some cases, you may wish to export multiple videos
combining same video tracks. One example would be to
export both long and short versions of a video.
Veddy facilitates this task by the use of :ref:`export` tags.
Here's how

.. code-block:: xml

   <stream name="long">
      ...
   </stream>

   <stream name="short">
      <composite name="trim" start="0" end="3">
         <reference name="long"/>
      </composite>
   </stream>

   <export stream="short" path="short.mp4"/>
   <export stream="long" path="long.mp4"/>

In this example, a short version of video is made by trimming
the long version by 3 seconds. When run,
two videos ``short.mp4`` and ``long.mp4`` will be compiled.

.. note::

   Likewise ``<global>`` and ``<config>`` tags,
   ``<export>`` tags are also
   only allowed to be defined directly in the ``<root>`` tag.
   Conventionally, ``<export>`` tags are often defined
   toward the end of ``<root>`` (that is, near ``</root>``).

Evaluating Expressions
=============================
One of the strength of Veddy is on-the-fly evaluation
of expressions. For example,

.. code-block:: xml

   <material name="cat" path="videos/cat.mp4"/>

   <stream>
      <pipe>
         <reference name="cat"/>
         <composite name="drawtext" text="eval(duration()) seconds"/>
      </pipe>
   </stream>

will draw a text telling the duration of ``cat.mp4``.
As you may deduce, ``eval()`` is a special reserved syntax that
evaluates symbolic expressions in it at runtime.
``duration()`` is a built-in function to get the duration of an
incoming video (that is, the duration of ``cat.mp4`` in this case).
The list of available built-in functions can be seen from
the side menu.

Expression Examples
--------------------------

Some examples are illustrated below. See :ref:`Debugging` for
the use of ``<print>`` and ``<exit/>`` tags.

.. code-block:: xml

   <stream>

      <!-- print the maximal duration from the nested two videos -->
      <print name="max duration" value="eval(max(durations()))">
            <reference name="cat"/>
            <reference name="dog"/>
      </print>

      <!-- print the duration sum from the nested two videos -->
      <print name="max duration" value="eval(sum(durations()))">
            <reference name="cat"/>
            <reference name="dog"/>
      </print>

      <!-- print the name and the duration of the 2nd material imported -->
      <print name="duration" value="eval(material_name(1)) = eval(material_duration(1))"/>

      <!-- calculate a mathematical expression -->
      <print name="duration" value="eval(4*3+duration())"/>

      <!-- terminate parse -->
      <exit/>

   </stream>

.. note::

   ``eval()`` is evaluated using Python3; hence, any pythonic expressions
   are valid.

Variables
========================
:ref:`set` and :ref:`global` tags allow us to define both
global and local variables. For example,

.. code-block:: xml

   <global name="hoge" value="4"/>

   <stream>
      <set name="foo" value="3"/>
      <print name="hoge" value="$hoge"/>
      <print name="foo" value="$foo"/>
      <print name="output" value="eval($hoge * $foo)"/>
   </stream>

the above scene will print

.. code-block:: bash

   hoge: 4
   foo: 3
   output: 12

To walk through the code, the stream first assigns
a global variable ``hoge`` as 4, local
variable ``foo`` as 3. :ref:`print` tag is
then used to print the value of its multiplication.
As suggested, to access variables, a prefix ``$``
shall be added to the beginning of the name.

.. note::

   -  Veddy uses FFmpeg as backend.
      For this matter, some reserved variable provided
      by FFmpeg can be also used in conjunction with
      local/global variables. These FFmpeg variables
      are available depending on which FFmpeg filter
      is internally used. To see which are available,
      find corresponding compositions from the side menu,
      or look up definitions from ``functions.xml``
   -  Note that FFmpeg variables are accessible
      without ``$`` prefix, and symbolic equations are
      evaluated without ``eval()`` syntax.
   -  Global variables are accessible from anywhere,
      while local variables are visible only from
      its scope and sub-scopes. Local variables can
      be cleared by ``<clear/>`` tag.
   -  Some variables are reserved by Veddy
      (e.g., :ref:`_width_`, :ref:`_height_`, :ref:`_fps_`).
      They are all set by Veddy, and read-only.

For example, here shows an example that uses FFmpeg variables
and expressions to draw texts

.. code-block:: xml

   <config name="shape" value="600x600"/>
   <config name="fps" value="20"/>

   <stream>
      <pipe>
         <composite name="color" duration="3"/>
         <composite name="drawtext" text="Top" shift_y="-h/4"/>
         <composite name="drawtext" text="Bottom" shift_y="h/4"/>
      </pipe>
   </stream>

Here, ``h/4`` includes FFmpeg's variable ``h``
and the expression ``shift_y="h/4"`` is handled by FFmpeg's filter.
See :ref:`drawtext` for the list of available FFmpeg's built-in variables.

Inserting Audios
====================
Veddy provides a simplified interface for inserting audio materials.
Here is an example.

.. code-block:: xml

   <audiotrack>
      <insert at="0">
         <audio path="introduction.mp3"/>
      </insert>
      <insert at="3.5">
         <audio path="method.mp3"/>
      </insert>
      <insert at="7">
         <audio path="conlusion.mp3"/>
         <audio path="acknowledgements.mp3"/>
      </insert>
   </audiotrack>

In this example, ``introduction.mp3`` is inserted at the beginning of the video.
Next, ``method.mp3`` is inserted at 3 seconds after the video starts.
Finally, ``conclusion.mp3`` is inserted at 7 seconds after the start, followed by
``acknowledgements.mp3``.

.. note::

   -  At the moment, audio is lightly supported, and is not able to
      apply complex filters.
   -  Do not import audio materials with ``<material>`` tags; they are
      reserved only for videos. Directly specify the same audio file if you
      plan to repeat it.
   -  All the audio-related tags must be written within ``<audiotrack>`` tags.

If you notice that the audio volume is slightly quiet or loud, you may
change the volume by ``volume`` attribute, e.g.,

.. code-block:: xml

   <audiotrack volume="1.5">
      ...
   </audiotrack>

In this example, the volume is increased by 50%.

Audio track is automatically selected if you only have one stream and
one audio track; however, if you have multiple streams that you plan to
export, you should also associate corresponding audio tracks for each stream.
This can be done by providing a name attribute and linking them via ``audiotrack``
attribute in ``<export>`` tags by

.. code-block:: xml

   <audiotrack name="narration">
      ...
   </audiotrack>

   <audiotrack name="testaudio">
      ...
   </audiotrack>

   <export stream="main" audiotrack="narration"/>
   <export stream="test" audiotrack="testaudio"/>

Remote Preview
====================
Previewing video is possible through HTTP streaming.
Assuming that you run Veddy on your local computer,
you can start previewing a stream by

.. code-block:: bash

   # If you plan to run on a remote server,
   # login to the server via SSH first

   # Choose a port that is reachable
   PORT=8080

   # Start video compilation on preview mode
   docker run -p ${PORT}:8020 -v ${PWD}:/veddy \
   --rm veddy scene.xml --preview

If you have installed a launcher script, you may
alternatively run

.. code-block:: bash

   # If you plan to run on a remote server,
   # login to the server via SSH first

   # Port number is embedded in the launcher script
   # Change the number in it and re-install script
   # if you need to

   # Start video compilation on preview mode
   veddy scene.xml --preview

Open a new terminal and run

.. code-block:: bash

   # This command should be run on your local machine
   # Make sure that you can reach ${SERVER_HOST}
   # and the port ${PORT}
   # Install ffplay if not available

   # Set the same port
   PORT=8080

   # Set server host
   SERVER_HOST=localhost

   # Run client and watch the preview
   ffplay http://${SERVER_HOST}:${PORT}

In this example we used ``ffplay`` as a streaming client.
If you don't have it, you may
install it via a system-provided package manager or
choose other rich clients such as `VLC <https://www.videolan.org/vlc/>`_.
If you plan to run Veddy on a remote server, change the server address and
set a reachable port.
In practice, you probably need to login to the server
via SSH first.

If you have multiple streams to export, or simply want to select
one specific stream to preview, add ``--stream`` option as

.. code-block:: bash

   docker run -p ${PORT}:8020 -v ${PWD}:/veddy \
   --rm veddy scene.xml \
   --preview \
   --stream <stream_name_to_preview>

Previewing Specific Time Range
----------------------------------
You can specify the time range of preview. This is done by

.. code-block:: bash

   docker run -p ${PORT}:8020 -v ${PWD}:/veddy \
   --rm veddy scene.xml \
   --preview \
   --starts_from <start_time_in_seconds> \
   --duration <duration_in_seconds>

Scaling Preview Size
-----------------------
If you are working on a large (in terms of dimensions) video,
you may scale the dimensions for preview, e.g.,

.. code-block:: bash

   docker run -p ${PORT}:8020 -v ${PWD}:/veddy \
   --rm veddy scene.xml \
   --preview \
   --scale 0.75

This will scale the window size 25% smaller than the actual size
(the preview is shown in 75% of the original size).

.. note::

   When previewing, time stamp is shown at
   the left-top corner.

Specifying Video Settings
============================
Global video settings are set through :ref:`config` tags.
Currently, three entries are given

  - ``shape``: the video size (width and height)
  - ``fps``: the video FPS
  - ``bitrate``: the video bitrate
  - ``pixel_format``: the video pixel format

If not given, pixel format is set ``yuv420p`` and
bitrate ``12M``.
See :ref:`config` for detail.
Shape and FPS are undefined unless inferred by Veddy.
If you would like to change some of these, specify like

.. code-block:: xml
   
   <root version="0.0.1">

      <config name="shape" value="600x400"/>
      <config name="fps" value="60"/>
      <config name="bitrate" value="3M"/>
      <config name="pixel_format" value="rgb24"/>
      ...
   </root>

.. note::

   :ref:`ffmpeg_config` may be also used to pass
   specific FFmpeg parameters.

Debugging
===============
Working with a complicated video stream is easier if you can track
the details of incoming information (e.g., video size
and duration) in the stream. This is possible by introducing
:ref:`print` and :ref:`exit` tags. Here's how

.. code-block:: xml

   <global name="hoge" value="2"/> <!-- dummy global variable -->
   <material name="cloud" path="videos/cloud.mp4"/>
   <stream>
      <set name="foo" value="2"/> <!-- dummy local variable -->
      <pipe>
         <reference name="cloud"/>
         <print name="check point 1"/>
         <composite name="trim" start="5" end="8"/>
         <set name="bar" value="my_text"/> <!-- dummy local variable -->
         <print name="check point 2"/>
         <composite name="crop" x="0" end="0" width="80" height="50"/>
         <print name="check point 3"/>
      </pipe>
      <exit/>
   </stream>

this will print (using ``videos/cloud.mp4`` contained in the repository)

.. code-block:: bash

   >>> check point 1
   arguments (global) = {'hoge': 2.0}
   arguments (local) = {'foo': 2.0}
   infos = [{'duration': 10.0, 'shape': (480, 270), 'fps': 25.0}]
   <<<
   >>> check point 2
   arguments (global) = {'hoge': 2.0}
   arguments (local) = {'foo': 2.0, 'bar': 'my_text'}
   infos = [{'duration': 3.0, 'shape': (480, 270), 'fps': 25.0}]
   <<<
   >>> check point 3
   arguments (global) = {'hoge': 2.0}
   arguments (local) = {'foo': 2.0, 'bar': 'my_text'}
   infos = [{'duration': 3.0, 'shape': (80, 50), 'fps': 25.0}]
   <<<

Notice that at the check point 1, video duration and the dimensions are

.. code-block::

   infos = [{'duration': 10.0}, 'shape': (480, 270), ... ]

After trimming the video (check point 2) the info changes to

.. code-block::

   infos = [{'duration': 3.0}, 'shape': (480, 270), ... ]

Now we can confirm that the video duration is changed
to 3 seconds. Next, let's see check point 3; just after the video
is further cropped. It is

.. code-block::

   infos = [{'duration': 3.0}, 'shape': (80, 50), ... ]

Now we can see that video dimensions are altered to 80x50.
When we focus on debugging, we won't be compiling this video.
Hence, we set ``<exit/>`` before the stream ends.
This ensures that the XML parsing terminates before starting
compiling the video.

Importing External Files
=============================
You can import external XML files by :ref:`import` tag.
For example,

.. code-block:: xml

   <root version="0.0.1">
      <import path="my_external_file.xml"/>
   </root>

.. note::

   The import path must be relative path from the
   source XML file written.

Release Dates
===============

  - 2021 July. First release.

.. [#docker] Many linux distributions provide latest packages;
   but being sure to choose right packages that are verified
   to work with by the author is much easier with docker.