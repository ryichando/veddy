count() -> ``int``
======================================
Count the number of nested videos.

.. csv-table::
   :header: ,Out

   Type, ``int``
   Description, Nested video count
   Example, 2

width(``int``) -> ``int``
======================================
Return the width of an nested video.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Video Index, Width (pixels)
   Default, 0,
   Example, 0, 1280

height(``int``) -> ``int``
======================================
Return the height of an nested video.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Video Index, Height (pixels)
   Default, 0,
   Example, 0, 720

fps(``int``) -> ``int``
======================================
Return the fps of an nested video.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Video Index, FPS
   Default, 0,
   Example, 0, 24

duration(``int``) -> ``int``
======================================
Return the duration of an nested video.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Video Index, Duration (seconds)
   Default, 0,
   Example, 0, 10

widths() -> ``[int]``
======================================
Return the width list of nested videos.

.. csv-table::
   :header: ,Out

   Type, ``[int]`` (Python list)
   Description, List of widths
   Example, "[1280,1280,640]"

heights() -> ``[int]``
======================================
Return the height list of nested videos.

.. csv-table::
   :header: ,Out

   Type, ``[int]`` (Python list)
   Description, List of heights
   Example, "[720,720,640]"

fpses() -> ``[int]``
======================================
Return the fps list of nested videos.

.. csv-table::
   :header: ,Out

   Type, ``[int]`` (Python list)
   Description, List of fpses
   Example, "[24,24,24]"

durations() -> ``[int]``
======================================
Return the duration list of nested videos.

.. csv-table::
   :header: ,Out

   Type, ``[int]`` (Python list)
   Description, List of durations
   Example, "[10,20,15]"

material_width(``int``) -> ``int``
======================================
Return the width of a video material.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Material Index, Width (pixels)
   Example, 0, 1280

material_height(``int``) -> ``int``
======================================
Return the height of a video material.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Material Index, Height (pixels)
   Example, 0, 720

material_duration(``int``) -> ``int``
======================================
Return the duration of a video material.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Material Index, Duration (seconds)
   Example, 0, 12

material_fps(``int``) -> ``int``
======================================
Return the FPS of a video material.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Material Index, FPS
   Example, 0, 24

material_name(``int``) -> ``str``
======================================
Return the name of a video material.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``str``
   Description, Material Index, Name
   Example, 0, my_video

input_count() -> ``int``
======================================
Return the count of inputs.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,Out

   Type, ``int``
   Description, Count
   Example, 4

input_width(``int``) -> ``int``
======================================
Return the width of an input.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Input Index, Width (pixels)
   Default, 0,
   Example, 0, 1280

input_height(``int``) -> ``int``
======================================
Return the height of an input.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Input Index, Height (pixels)
   Default, 0,
   Example, 0, 720

input_fps(``int``) -> ``int``
======================================
Return the fps of an input.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Input Index, FPS
   Default, 0,
   Example, 0, 24

input_duration() -> ``[int]``
======================================
Return the duration of an nested video.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,In, Out

   Type, ``int``, ``int``
   Description, Input Index, Duration (seconds)
   Default, 0,
   Example, 0, 12

input_widths() -> ``[int]``
======================================
Return the width list of inputs.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,Out

   Type, ``[int]``
   Description, Width list (Python list)
   Example, "[1280,1280,640]"

input_heights() -> ``[int]``
======================================
Return the height list of inputs.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,Out

   Type, ``[int]``
   Description, Height list (Python list)
   Example, "[720,720,640]"

input_fpses() -> ``[int]``
======================================
Return the FPS list of inputs.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,Out

   Type, ``[int]``
   Description, FPS list (Python list)
   Example, "[24,24,60]"

input_durations() -> ``[int]``
======================================
Return the duration list of inputs.
Can be used only in ``<function>``.

.. csv-table::
   :header: ,Out

   Type, ``[int]``
   Description, Duration list (Python list)
   Example, "[12,12,20]"