# Veddy
[![Documentation Status](https://readthedocs.org/projects/veddy/badge/?version=latest)](https://veddy.readthedocs.io/en/latest/?badge=latest)

An XML-based video editor targeted at technical presentation. No UI, seriously. Powered by [FFmpeg](https://www.ffmpeg.org).

<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/logo.svg" alt="veddy logo" width="250">

## Highlights

- Simple and versatile syntax for scene description
- Full command-line interface
- Remote preview via online streaming

## Documentation

- See https://veddy.readthedocs.io/en/latest/

## Quickstart

```
git clone https://github.com/ryichando/veddy.git
cd veddy
docker build -t veddy .
docker run -v ${PWD}:/veddy --rm veddy examples/concat.xml
```

## Remote Preview

```
PORT=8080
SERVER_HOST=localhost
docker run -p ${PORT}:8020 -v ${PWD}:/veddy --rm veddy scene.xml --preview
ffplay http://${SERVER_HOST}:${PORT}
```

## Examples

  * [Concatenation](#examplesconcatxml)
  * [Side-by-side split half](#examplessidebysidexml)
  * [Re-using the same track](#examplessidebyside-repeatxml)
  * [Text annotation](#examplessidebyside-annotatedxml)
  * [Using images](#examplesimagesxml)
  * [Stacking two videos horizontally](#exampleshstackxml)
  * [Overlaying videos and inserting audios](#examplesoverlay-narratedxml)

## Instructive Examples

  * [Crop](#crop)
  * [Trim](#trim)

#### examples/concat.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import video materials -->
   <material name="cat" path="videos/cat.mp4"/>
   <material name="dog" path="videos/dog.mp4"/>

   <!-- define video scene -->
   <stream transition="fade">
      <composite name="title-slide" text="Cat"/>
      <reference name="cat"/>
      <composite name="title-slide" text="Dog"/>
      <reference name="dog"/>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/concat.gif" alt="concat">

#### examples/sidebyside.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import image sequences -->
   <material name="mesh" path="videos/water_mesh/image_%d.jpg" fps="30"/>
   <material name="transparent" path="videos/water_transparent/image_%d.jpg" fps="30"/>

   <!-- define video scene -->
   <stream>
      <composite name="sidebyside-split">
         <reference name="mesh"/> <!-- left -->
         <reference name="transparent"/> <!-- right -->
      </composite>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/sidebyside.gif" alt="sidebyside">

#### examples/sidebyside-annotated.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import image sequences -->
   <material name="mesh" path="videos/water_mesh/image_%d.jpg" fps="30"/>
   <material name="transparent" path="videos/water_transparent/image_%d.jpg" fps="30"/>

   <!-- define video scene -->
   <stream>
      <!-- pipe enables consecutive filters -->
      <pipe>
         <composite name="sidebyside-split">
            <reference name="mesh"/>
            <reference name="transparent"/>
         </composite>
         <set name="bottom" value="0.9"/> <!-- define a local variable -->
         <composite name="drawtext" text="Mesh View" scale="0.5" shift_x="-w/4" y="$bottom*h"/>
         <composite name="drawtext" text="Transparent View" scale="0.5" shift_x="w/4" y="$bottom*h"/>
      </pipe>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/sidebyside-annotated.gif" alt="sidebyside-annotated">

#### examples/sidebyside-repeat.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import image sequences -->
   <material name="mesh" path="videos/water_mesh/image_%d.jpg" fps="60"/>
   <material name="transparent" path="videos/water_transparent/image_%d.jpg" fps="60"/>

   <!-- build comparison scene -->
   <stream name="comparison">
      <pipe>
         <composite name="sidebyside-split">
            <reference name="mesh"/>
            <reference name="transparent"/>
         </composite>
         <set name="bottom" value="0.9"/>
         <!-- draw annotation texts -->
         <composite name="drawtext" text="Mesh View" scale="0.5" shift_x="-w/4" y="$bottom*h"/>
         <composite name="drawtext" text="Transparent View" scale="0.5" shift_x="w/4" y="$bottom*h"/>
      </pipe>
   </stream>

   <!-- define main stream -->
   <stream transition="fade">
      <composite name="title-slide" text="Water Simulation"/>
      <reference name="comparison"/>
      <composite name="title-slide" text="Repeat"/>
      <pipe>
         <composite name="changespeed" factor="0.5">
            <reference name="comparison"/>
         </composite>
         <composite name="drawtext" text="Repeat (0.5x faster)" scale="0.5" x="0.05*w" y="0.05*h"/>
      </pipe>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/sidebyside-repeat.gif" alt="sidebyside-repeat">

#### examples/images.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import single images -->
   <material name="cover-1" path="images/cover-1.jpg" duration="1" fps="30"/>
   <material name="cover-2" path="images/cover-2.jpg" duration="1" fps="30"/>
   <material name="cover-3" path="images/cover-3.jpg" duration="1" fps="30"/>

   <!-- define video scene -->
   <stream transition="fade">
      <composite name="title-slide" text="Nature"/>
      <reference name="cover-1"/>
      <reference name="cover-2"/>
      <reference name="cover-3"/>
      <composite name="title-slide" text="End"/>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/images.gif" alt="images">

#### examples/hstack.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- explicitly declare video size -->
   <config name="shape" value="800x400"/>

   <!-- import image sequences -->
   <material name="implicit" path="videos/mpm/implicit/image_%d.jpg" fps="60"/>
   <material name="explicit" path="videos/mpm/explicit/image_%d.jpg" fps="60"/>

   <!-- define video scene -->
   <stream transition="fade">
      <composite name="title-slide" text="Side-by-Side Comparison"/>
      <pipe>
         <!-- stitch two videos horizontally -->
         <composite name="hstack">
            <reference name="implicit"/> <!-- left -->
            <reference name="explicit"/> <!-- right -->
         </composite>
         <set name="ceiling" value="0.1"/>
         <composite name="drawtext" text="Implicit Time Integration" scale="0.5" shift_x="-w/4" y="$ceiling*h"/>
         <composite name="drawtext" text="Explicit Time Integration" scale="0.5" shift_x="w/4" y="$ceiling*h"/>
      </pipe>
   </stream>
</root>
```
( Resources provided by Daichi Namatame )

<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/hstack.gif" alt="hstack">

#### examples/sidebyside-float.xml
```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import materials -->
   <material name="implicit" path="videos/mpm/implicit/image_%d.jpg" fps="60"/>
   <material name="explicit" path="videos/mpm/explicit/image_%d.jpg" fps="60"/>

   <!-- define video scene -->
   <stream>
      <pipe>
         <composite name="sidebyside-float">
            <reference name="implicit"/> <!-- left -->
            <reference name="explicit"/> <!-- right -->
         </composite>
         <set name="bottom" value="0.89"/>
         <composite name="drawtext" text="Implicit Time Integration" scale="0.5" shift_x="-w/4" y="$bottom*h" color="white"/>
         <composite name="drawtext" text="Explicit Time Integration" scale="0.5" shift_x="w/4" y="$bottom*h" color="white"/>
      </pipe>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/sidebyside-float.gif" alt="sidebyside-float">

#### examples/overlay-narrated.xml

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- explicitly declare video size -->
   <config name="shape" value="900x540"/>

   <!-- import videos -->
   <material name="swim" path="videos/swim.mp4" />
   <material name="fishing" path="videos/fishing.mp4" />
   <material name="grill" path="videos/grill.mp4" />

   <!-- define video scene -->
   <stream>
      <pipe>
         <!-- lay background color -->
         <composite name="color" duration="12"/>
         <composite name="overlay" x="w/5" y="h/3" scale="0.7" effect="dissolve">
            <reference name="swim"/> <!-- overlay fish video at the start -->
         </composite>
         <composite name="overlay" x="1.5*w" y="h" at="3.5" scale="0.7" effect="dissolve">
            <reference name="fishing"/> <!-- overlay fishing video at 3.5 seconds -->
         </composite>
         <composite name="overlay" x="w/5" y="1.7*h" at="7" scale="0.7" effect="dissolve">
            <reference name="grill"/> <!-- overlay grill video at 7 seconds -->
         </composite>
         <composite name="drawtext" shift_x="w/4" shift_y="0.45*h" text="Narrated by https\://ondoku3.com" color="white" scale="0.45"/>
      </pipe>
   </stream>

   <!-- insert audio narration -->
   <audiotrack>
      <insert at="0">
         <audio path="audios/swim.mp3"/>
      </insert>
      <insert at="3.5">
         <audio path="audios/fishing.mp3"/>
      </insert>
      <insert at="7">
         <audio path="audios/grilled.mp3"/>
         <audio path="audios/poor.mp3"/>
      </insert>
   </audiotrack>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/overlay-narrated.gif" alt="overlay-narrated">

[Hear the narration!](https://github.com/ryichando/veddy/blob/dev/resources/overlay-narrated.mp4)

## Instructive Examples

#### Crop

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import a video -->
   <material name="cat" path="videos/cat.mp4"/>

   <!-- define video scene -->
   <stream transition="fade">
      <composite name="title-slide" text="Original Footage"/>
      <reference name="cat"/>
      <composite name="title-slide" text="Cropped Footage"/>
      <pipe>
         <composite name="color" duration="5"/>
         <composite name="overlay" x="0.25*main_w" y="0.25*main_h">
            <composite name="crop" x="0.35*iw" y="0.35*ih" width="0.5*iw" height="0.5*ih">
               <reference name="cat"/>
            </composite>
         </composite>
         <composite name="drawtext" shift_y="0.35*h" text="Cropped" color="white" scale="0.85"/>
      </pipe>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/crop.gif" alt="crop">

#### Trim

```XML
<?xml version="1.0"?>
<root version="0.0.1">

   <!-- import a video -->
   <material name="cloud" path="videos/cloud.mp4"/>

   <!-- define video scene -->
   <stream transition="fade">
      <composite name="title-slide" text="Original (10 seconds)"/>
      <reference name="cloud"/>
      <composite name="title-slide" text="Trimmed (3 seconds)"/>
      <composite name="trim" start="5" end="8">
         <reference name="cloud"/>
      </composite>
      <composite name="color" duration="1"/>
   </stream>
</root>
```
<img src="https://raw.githubusercontent.com/ryichando/veddy/dev/resources/trim.gif" alt="trim">
