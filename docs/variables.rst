_bgcolor_
====================
Background color.

.. csv-table::
   :header: Type, Default, Overwritable

   Global, black, Yes

_fgcolor_
====================
Foreground color.

.. csv-table::
   :header: Type, Default, Overwritable

   Global, white, Yes

_width_
====================
Width of the previously processed video.
For example,

.. code-block:: xml

   <stream>
      <composite name="color" width="720"/>
      <print value="$_width_"> <!-- this will print 720 -->
   </stream>

.. csv-table::
   :header: Type, Default, Overwritable

   Global, N/A, No

_height_
====================
Height of the previously processed video.
For example,

.. code-block:: xml

   <stream>
      <composite name="color" height="480"/>
      <print value="$_height_"> <!-- this will print 480 -->
   </stream>

.. csv-table::
   :header: Type, Default, Overwritable

   Global, N/A, No

_fps_
====================
FPS of the previously processed video.
For example,

.. code-block:: xml

   <stream>
      <composite name="color" fps="24"/>
      <print value="$_fps_"> <!-- this will print 24 -->
   </stream>

.. csv-table::
   :header: Type, Default, Overwritable

   Global, N/A, No