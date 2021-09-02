.. |AllowedLoc| replace:: Allowed Location
.. |CanHaveNested| replace:: Can Have Nested Tags
.. |CanBeInPipe| replace:: Can Be In ``<pipe>``

stream
======

Define video tracks. See :ref:`Declaring Movie Track` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, Yes, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Name of a stream, my_stream, Not required
   transition, Name of a transition from `this link <https://trac.ffmpeg.org/wiki/Xfade>`_, fade, Not required
   extended, Use ``<transition>`` if set 0 ``<extended_transition>`` otherwise, 0, Not required
   duration, Transition duration, 1, Not required

export
======

Define a stream to export. See :ref:`Exporting Multiple Streams` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   stream, Name of a stream to export, my_stream, Yes
   path, File path to export, output.mp4, Yes
   audiotrack, Name of an audiotrack to attach, my_audiotrack, Not required
   timestamp, "1 or 0, indicating if timestamp is shown", 1, Not required

material
========

Define a material to import. See :ref:`Material Import` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

Depending on the type of materials, required tags change.

*  If you plan to import a video (e.g., ``.mp4``, ``.mov`` ``.avi``),

.. csv-table::
   :header: Attribute, Description, Example, Required
   
   name, Reference name to assign, my_video, Yes
   path, Path to the material, video.mp4, Yes

*  If you plan to import a sequence of images,

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Reference name to assign, my_video, Yes
   path, Path to the images, images_%d.png, Yes
   fps, FPS for the material, 60, Yes

*  If you plan to import a URL video material,

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Reference name to assign, my_video, Yes
   url, URL to the video, http://svr.com/video.mp4, Yes
   username, Username for basic authentication, user, Not required
   password, Password for basic authentication, passwd, Not required

reference
=========

Define reference to a material or a stream.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, No, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Name to a reference defined by ``<material>`` or ``<stream>``, my_video, Yes

pipe
======

Enter fluent interface. See :ref:`Fluent Interface` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

group
=======

Group nested references as an a set of inputs.
This is used to provide multiple inputs in ``<pipe>``.
See an example code below.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Only in ``<pipe>``, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

Using ``<group>``,

.. code-block:: xml

    <stream>
        <composite name="comp2">
            <composite name="comp1">
                <reference name="ref1"/>
                <reference name="ref2"/>
            </composite>
        </composite>
    </stream>

is equivalent to

.. code-block:: xml

    <stream>
        <pipe>
            <group>
                <reference name="ref1"/>
                <reference name="ref2"/>
            </group>
            <composite name="comp1"/>
            <composite name="comp2">
        </pipe>
    </stream>

rolling
=======

Do rolling window calculation on incoming inputs
provided by ``<pipe>``.
This is often used together with ``<group>`` tag.
Windows size is currently fixed to two.
See an example code below.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Only in ``<pipe>``, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

For example, the code below

.. code-block:: xml

    <stream>
        <composite name="transition" type="fade"/>
            <composite name="transition" type="fade"/>
                <composite name="transition" type="fade"/>
                    <reference name="ref1"/>
                    <reference name="ref2"/>
                </composite>
                <reference name="ref3"/>
            <composite/>
            <reference name="ref4"/>
        <composite/>
    </stream>

is equivalent to

.. code-block:: xml

    <stream>
        <pipe>
            <group>
                <reference name="ref1"/>
                <reference name="ref2"/>
                <reference name="ref3"/>
                <reference name="ref4"/>
            </group>
            <rolling>
                <composite name="transition" type="fade"/>
            </rolling>
        </pipe>
    </stream>

and it turns out that, using ``transiion`` attribute in ``<stream>``,
this is simply written as

.. code-block:: xml

    <stream transition="fade" extended="0">
        <reference name="ref1"/>
        <reference name="ref2"/>
        <reference name="ref3"/>
        <reference name="ref4"/>
    </stream>

for_each
========
Process each input using a same rule.
Used together with ``<group>`` tag.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Only in ``<pipe>``, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

For example,

.. code-block:: xml

    <stream>
        <composite name="negate">
            <reference name="ref1"/>
        </composite>
        <composite name="negate">
            <reference name="ref2"/>
        </composite>
        <composite name="negate">
            <reference name="ref3"/>
        </composite>
        <composite name="negate">
            <reference name="ref4"/>
        </composite>
    </stream>

can be simplified to

.. code-block:: xml

    <stream>
        <pipe>
            <group>
                <reference name="ref1"/>
                <reference name="ref2"/>
                <reference name="ref3"/>
                <reference name="ref4"/>
            </group>
            <for_each>
                <composite name="negate"/>
            <for_each/>
        </pipe>
    </stream>

import
======

Import external XML files. See :ref:`Importing External Files` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   path, Path to an XML file , dir/myfile.xml, Yes

set
===

Define a local variable. See :ref:`Variables` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, No, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

global
======

Define a global variable. See :ref:`Variables` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A


config
======

Specify a video setting. See :ref:`Specifying Video Settings` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Configuration name, shape, Yes
   value, Value, 620x480, Yes

Currently, following name/value pairs are valid

.. csv-table::
   :header: Name, Description, Default, Example

    shape, Video size, N/A,1280x720
    fps, Video FPS, N/A, 24
    pixel_format, Pixel format, yuv420p, yuv420p
    bitrate, Video bitrate, 12M, 400k

ffmpeg_config
=============

Specify a FFmpeg setting.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

For example,

.. code-block:: xml

    <stream>
        <ffmpeg_config name="pix_fmt" value="yuv420p"/>
        <ffmpeg_config name="b:v" value="1200k"/>
    </stream>

audiotrack
==========

Define an audiotrack. See :ref:`Inserting Audios` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, No, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Name of the audiotrack, my_audiotrack, No
   volume, Audio volume. Default is 1.0., 1.25, No

print
=====

Print a variable or expression. See :ref:`Debugging` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Label name, checkpoint 1, No
   value, What to print, eval($var+1), No

assert
=======

Assert check an expression.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Label name, checkpoint 1, Yes
   value, What to verify, eval($var+1 > 10), Yes

exit
====

Terminate parsing. See :ref:`Debugging` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, No, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

if
==
Do ``if`` statement branch. See example codes below.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, Yes, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, branch type, equal, Yes

.. code-block:: xml

    <stream>
        <set name="var" value="4"/>
        <if name="equal">
            <variable value="$var"/>
            <variable value="4"/>
            <then>
                ...
            </then>
            <else>
                ...
            </else>
        </if>
    </stream>

.. code-block:: xml

    <stream>
        <if name="equal">
            <variable value="eval(get_material_duration() < 4)"/>
            <variable value="True"/>
            <then>
                ...
            </then>
            <else>
                ...
            </else>
        </if>
    </stream>

.. code-block:: xml

    <stream>
        <if name="switch">
            <variable value="$var"/>
            <case value="1">
                ...
            </case>
            <case value="2">
                ...
            </case>
            <otherwise>
                ...
            </otherwise>
        </if>
    </stream>

clear
=====
Clear local variables. See :ref:`Variables` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<stream>`` and in its nested, No, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A

function
========
Define a new composition. See :ref:`Defining New Composition` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   Just in ``<root>`` not in its nested, Yes, No

.. csv-table::
   :header: Attribute, Description, Example, Required

   name, Composition name, my_composition, Yes

input
======
Insert an input. Used when defining a composition.
See :ref:`Defining New Composition` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<function>`` and in its nested, No, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   index, Numbered index starting from 0, 0, No

all_inputs
===========
Insert all the inputs. Used when defining a composition.
See :ref:`Defining New Composition` for detail.

.. csv-table::
   :header: |AllowedLoc|, |CanHaveNested|, |CanBeInPipe|

   In ``<function>`` and in its nested, No, Yes

.. csv-table::
   :header: Attribute, Description, Example, Required

   N/A, No attribute is available, N/A, N/A