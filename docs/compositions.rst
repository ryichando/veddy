color
======================
Create a solid color canvas. See :ref:`Creating Solid Color Background` for detail.

- ``$_width_``, ``$_height_`` and ``$_fps_`` are automatically set
  according to the video size and fps if deducible (See :ref:`Video Dimensions and FPS`).
- If not, they must be defined explicitly via ``<config>``
  (See an example code in :ref:`Creating Solid Color Background`).
- Same rule applies to the other compositions below.

.. csv-table::
   :header: Attribute, Description, Default

   color, Color name in `this form <https://ffmpeg.org/ffmpeg-utils.html#Color>`_, $\ :ref:`_bgcolor_`
   duration, "Duration in seconds. Empty for infinite."
   width, Width, $\ :ref:`_width_`
   height, Height, $\ :ref:`_height_`
   fps, FPS, $\ :ref:`_fps_`
   alpha, Opacity, 1.0

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   0, 1, `color <https://ffmpeg.org/ffmpeg-filters.html#allrgb_002c-allyuv_002c-color_002c-haldclutsrc_002c-nullsrc_002c-pal75bars_002c-pal100bars_002c-rgbtestsrc_002c-smptebars_002c-smptehdbars_002c-testsrc_002c-testsrc2_002c-yuvtestsrc>`_

.. code-block:: xml

   <config name="shape" value="900x540"/>
   <config name="fps" value="20"/>

   <stream>
      <composite name="color" duration="3"/>
   </stream>

nullsrc
======================
Create a null source canvas.

.. csv-table::
   :header: Attribute, Description, Default

   duration, "Duration in seconds. Empty for infinite."
   width, Width, $\ :ref:`_width_`
   height, Height, $\ :ref:`_height_`
   fps, FPS, $\ :ref:`_fps_`

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   0, 1, `nullsrc <https://ffmpeg.org/ffmpeg-filters.html#allrgb_002c-allyuv_002c-color_002c-haldclutsrc_002c-nullsrc_002c-pal75bars_002c-pal100bars_002c-rgbtestsrc_002c-smptebars_002c-smptehdbars_002c-testsrc_002c-testsrc2_002c-yuvtestsrc>`_

.. code-block:: xml

   <config name="shape" value="900x540"/>
   <config name="fps" value="20"/>

   <stream>
      <composite name="nullsrc" duration="3"/>
   </stream>


trim
======================
Trim a video with time.

.. csv-table::
   :header: Attribute, Description, Default

   start, Start time in seconds, 0
   end, End time in seconds, 3

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, "`trim <https://ffmpeg.org/ffmpeg-filters.html#trim>`_, `setpts <https://ffmpeg.org/ffmpeg-filters.html#setpts>`_"

.. code-block:: xml

   <material name="video" path="video.mp4"/>
   <stream>
      <!-- remove first and last 2 seconds -->
      <composite name="trim" start="2" end="eval(duration())-2">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="start" value="0"/>
.. <default name="end" value="3"/>

vstack
======================
Vertically stack videos.

.. csv-table::
   :header: Attribute, Description, Default

   N/A, N/A, N/A

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   any, 1, `vstack <https://ffmpeg.org/ffmpeg-filters.html#vstack>`_

.. code-block:: xml

   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <material name="video_3" path="video_3.mp4"/>
   <stream>
      <composite name="vstack">
         <reference name="video_1"/>
         <reference name="video_2"/>
         <reference name="video_3"/>
      </composite>
   </stream>

hstack
======================
Horizontally stack videos.

.. csv-table::
   :header: Attribute, Description, Default

   N/A, N/A, N/A

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   any, 1, `hstack <https://ffmpeg.org/ffmpeg-filters.html#hstack>`_

.. code-block:: xml
   
   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <material name="video_3" path="video_3.mp4"/>
   <stream>
      <composite name="hstack">
         <reference name="video_1"/>
         <reference name="video_2"/>
         <reference name="video_3"/>
      </composite>
   </stream>

crop
======================
Crop a video.

.. csv-table::
   :header: Attribute, Description, Default

   x, Horizontal origin, 0
   y, Vertical origin, 0
   width, Crop width, 0.5 * iw
   height, Crop height, 0.5 * ih

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `crop <https://ffmpeg.org/ffmpeg-filters.html#crop>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="crop" x="0.1*iw" y="0.1*ih" width="0.8*iw" height="0.8*ih">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="x" value="0"/>
.. <default name="y" value="0"/>
.. <default name="width" value="0.5*iw"/>
.. <default name="height" value="0.5*ih"/>

join
======================
Concatenate videos in time.

.. csv-table::
   :header: Attribute, Description, Default

   N/A, N/A, N/A

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   any, 1, `concat <https://ffmpeg.org/ffmpeg-filters.html#concat>`_

.. code-block:: xml
   
   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <material name="video_3" path="video_3.mp4"/>
   <stream>
      <pipe>
         <composite name="join">
            <reference name="video_1"/>
            <reference name="video_2"/>
            <reference name="video_3"/>
         </composite>
         <composite name="drawtext" text="Hello World"/>
      </pipe>
   </stream>

split
======================
Duplicate videos.
This is only used in composition, when one needs
to re-use the same ``<input/>`` multiple times.

.. csv-table::
   :header: Attribute, Description, Default

   count, Duplicate count, 2

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, any, `split <https://ffmpeg.org/ffmpeg-filters.html#split_002c-asplit>`_

.. code-block:: xml
   
   <function name="my_repeat_twice">
      <pipe>
         <composite name="split" count="2">
            <input/>
            <input/>
         </composite>
         <composite name="join"/>
      </pipe>
   </function>

scale
=====================
Re-scale video size.

.. csv-table::
   :header: Attribute, Description, Default

   scale, Scale ratio, 0.5

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `scale <https://ffmpeg.org/ffmpeg-filters.html#scale-1>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="scale" scale="0.8">
         <reference name="video"/>
      </composite>
   </stream>
   
.. <default name="scale" value="0.5"/>
.. <default name="width" value="$scale*iw"/>
.. <default name="height" value="$scale*ih"/>

fps
======================
Change the video fps.

.. csv-table::
   :header: Attribute, Description, Default

   fps, FPS, eval(fps())

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `fps <https://ffmpeg.org/ffmpeg-filters.html#fps>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="fps" fps="24">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="fps" value="eval(input_fps())"/>

format
======================
Change the video format.

.. csv-table::
   :header: Attribute, Description, Default

   format, New format, yuva444p

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `format <https://ffmpeg.org/ffmpeg-filters.html#format>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="format" format="yuv420p">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="format" value="yuva444p"/>

fade
======================
Apply fade transition.

.. csv-table::
   :header: Attribute, Description, Default

   type, "Type, in or out", in
   at, When to start, 0
   duration, Duration in seconds, 3
   alpha, "If set one, only alpha channel fades", 1
   color, Fade color (set alpha 0 if use color),

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `fade <https://ffmpeg.org/ffmpeg-filters.html#fade>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="fade" color="black">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="type" value="in"/>
.. <default name="at" value="0"/>
.. <default name="duration" value="3"/>
.. <default name="alpha" value="1"/>
.. <default name="color" value=""/>

extend
======================
Extend a video from both back and front sides.
In other words, insert freeze frames at front and back.

.. csv-table::
   :header: Attribute, Description, Default

   start_duration, Duration to freeze at front, 0
   end_duration, Duration to freeze at back, 0

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, many

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <!-- freeze both back and front for 1 second -->
      <composite name="extend" start_duration="1" end_duration="1">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="start_duration" value="0"/>
.. <default name="end_duration" value="0"/>

overlay
======================
Overlay a video onto another video.

.. csv-table::
   :header: Attribute, Description, Default

   x, Horizontal position, 0
   y, Vertical position, 0
   at, Time to start overlay, 0
   for, Duration to overlay (empty for infinite),
   scale, Scaling of video to be overlaid, 1.0
   shortest, truncate the whole videos when any terminates (0 or 1), 0
   effect, In and out effect, pop
   duration, duration for the effect, 1

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   2, 1, `overlay <https://ffmpeg.org/ffmpeg-filters.html#overlay-1>`_ and many others

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <pipe>
         <!-- lay background color -->
         <composite name="color" duration="12"/>
         <composite name="overlay" x="w/5" y="h/3" scale="0.7" effect="dissolve">
            <reference name="video"/> <!-- overlay video at the start -->
         </composite>
      </pipe>
   </stream>

.. <default name="x" value="0"/>
.. <default name="y" value="0"/>
.. <default name="at" value="0"/>
.. <default name="for" value=""/>
.. <default name="scale" value="1.0"/>
.. <default name="shortest" value="0"/>
.. <default name="duration" value="1"/>
.. <default name="effect" value="pop"/>

transition
======================
Apply a transition over two videos.

.. csv-table::
   :header: Attribute, Description, Default

   duration, Transition duration, 1
   type, Type of transition, fade

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   2, 1, `xfade <https://ffmpeg.org/ffmpeg-filters.html#xfade>`_

.. code-block:: xml
   
   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <stream>
      <composite name="transition" duration="1" type="smoothleft">
         <reference name="video_1"/>
         <reference name="video_2"/>
      </composite>
   </stream>

.. <default name="duration" value="1"/>
.. <default name="type" value="fade"/>

extended_transition
======================
Apply a transition over two videos (a more high-level composition to :ref:`transition`).

.. csv-table::
   :header: Attribute, Description, Default

   duration, Transition duration, 1
   pause, Duration to pause, 1
   color, Solid color between videos (empty to skip),
   type, Type of transition, fade

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   2, 1, `xfade <https://ffmpeg.org/ffmpeg-filters.html#xfade>`_ and many others

.. code-block:: xml
   
   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <stream>
      <composite name="extended_transition" duration="1" type="smoothleft">
         <reference name="video_1"/>
         <reference name="video_2"/>
      </composite>
   </stream>

.. <default name="duration" value="1"/>
.. <default name="pause" value="1"/>
.. <default name="color" value=""/>
.. <default name="type" value="fade"/>

sidebyside-split
======================
Lay a split side-by-side comparison.

.. csv-table::
   :header: Attribute, Description, Default

   border_width, Border width at the center, 4
   border_color, Border color, $\ :ref:`_bgcolor_`
   direction, Vertical or horizontal, vertical
   shortest, Terminate the whole video if any terminates, 0

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   2, 1, many

.. code-block:: xml
   
   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <stream>
      <composite name="sidebyside-split">
         <reference name="video_1"/>
         <reference name="video_2"/>
      </composite>
   </stream>

.. <default name="border_width" value="4"/>
.. <default name="border_color" value="$_bgcolor_"/>
.. <default name="direction" value="vertical"/>
.. <default name="shortest" value="0"/>

sidebyside-float
======================
Lay a floating side-by-side comparison.

.. csv-table::
   :header: Attribute, Description, Default

   margin, Horizontal margin ratio, 0.1
   head, Top margin, 0.1
   foot, Bottom margin, 0.25
   color, Background color, $\ :ref:`_bgcolor_`
   shortest, Terminate the whole video if any terminates, 0

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   2, 1, many

.. code-block:: xml
   
   <material name="video_1" path="video_1.mp4"/>
   <material name="video_2" path="video_2.mp4"/>
   <stream>
      <composite name="sidebyside-float">
         <reference name="video_1"/>
         <reference name="video_2"/>
      </composite>
   </stream>

.. <default name="margin" value="0.1"/>
.. <default name="head" value="0.1"/>
.. <default name="foot" value="0.25"/>
.. <default name="color" value="$_bgcolor_"/>
.. <default name="shortest" value="0"/>

drawtext
======================
Draw a text onto a video.

.. csv-table::
   :header: Attribute, Description, Default

   text, Text to draw, hello
   font, Optional font path,
   scale, Font scale, 1.0
   size, Absolute font size, eval(width()*0.06*$scale)
   color, Font color, black
   x, Horizontal position, (w-text_w)/2
   y, Vertical position, (h-text_h)/2
   shift_x, Horizontal shift to ``x`` variable, 0
   shift_y, Vertical shift to ``y`` variable, 0

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `drawtext <https://ffmpeg.org/ffmpeg-filters.html#drawtext>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="drawtext" text="Hello World">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="text" value="hello"/>
.. <default name="font" value=""/>
.. <default name="scale" value="1.0"/>
.. <default name="size" value="eval(input_width()*0.06*$scale)"/>
.. <default name="color" value="black"/>
.. <default name="x" value="(w-text_w)/2"/>
.. <default name="y" value="(h-text_h)/2"/>
.. <default name="shift_x" value="0"/>
.. <default name="shift_y" value="0"/>

title-slide
======================
Create a title slide.

.. csv-table::
   :header: Attribute, Description, Default

   text, Text to draw, hello
   font, Optional font path,
   scale, Font scale, 1.0
   size, Absolute font size, eval(width()*0.06*$scale)
   color, Font color, black
   x, Horizontal position, (w-text_w)/2
   y, Vertical position, (h-text_h)/2
   shift_x, Horizontal shift to ``x`` variable, 0
   shift_y, Vertical shift to ``y`` variable, 0

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   0, 1, `drawtext <https://ffmpeg.org/ffmpeg-filters.html#drawtext>`_ and many others

.. <default name="text" value="(Your text here)"/>
.. <default name="color" value="$_bgcolor_"/>
.. <default name="duration" value="1"/>
.. <default name="width" value="$_width_"/>
.. <default name="height" value="$_height_"/>
.. <default name="fps" value="$_fps_"/>

changespeed
======================
Change the video speed.

.. csv-table::
   :header: Attribute, Description, Default

   factor, Speed factor, 0.5

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, many

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="changespeed">
         <reference name="video"/>
      </composite>
   </stream>

.. <default name="factor" value="0.5"/>

negate
======================
Invert color of an input video.

Change the video speed.

.. csv-table::
   :header: Attribute, Description, Default

   N/A, N/A, N/A

.. csv-table::
   :header: Number of inputs, Number of outputs, Used FFmpeg filters

   1, 1, `negate <https://ffmpeg.org/ffmpeg-filters.html#negate>`_

.. code-block:: xml
   
   <material name="video" path="video.mp4"/>
   <stream>
      <composite name="negate">
         <reference name="video"/>
      </composite>
   </stream>