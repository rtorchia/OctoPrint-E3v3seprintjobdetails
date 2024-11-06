# OctoPrint-E3v3seprintjobdetails

This Plugin enable the communication with [the modified firmware of the Ender 3V3SE](https://github.com/navaismo/Ender-3V3-SE/tree/OctoPrintDetailsPageinLCD) and Octoprint to Render in the Printer's LCD the current print JOB.
For this was created a custom Command O9000 to send and update the job details.

<br />


  ![Octorpint Print Job Detai](https://i.imgur.com/Ir8u0tD.jpeg)


<br />


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/navaismo/OctoPrint-E3v3seprintjobdetails/archive/main.zip

## Dependiencies

To work correctly this plugin depends on the below 3rd party plugins:

- Dashboard.
- GcodeViewer.
- PrintTimeGenius.

<br>


To see correctly the layer progress you must wait till GcodeViewer analyse the file, after that you can start the print.
PrintTime Genius Provides the Estimated Print Time.

Usualy I load the file and when I see the screen in the LCD I check if gcodeviewer finished and then I press print to start the job.


## Fine tunning for canceling and pausing/resuming jobs
To have a better controel of messages and printer moves you may want to add this block codes to the GCODE SCRIPTS section of Octoprint settings:


### After print Job is Cancelled 
```C
; relative moving
G91
; move head 10mm up
G1 Z10 F800
; absolute moving
G90

; move print head out of the way
G1 X0 Y220 F3000

; disable motors
M84

; disable all heaters
{% snippet 'disable_hotends' %}
M104 S0 ; Set Hotend to 0

{% snippet 'disable_bed' %}
M140 S0 ; Set Bed to 0

;disable fan
M106 S0

; send message to printer.
M117 Print is cancelled
```

### After print Job is Paused 
```C
{% if pause_position.x is not none %}
; relative XYZE
G91
M83

; retract filament of 0.8 mm up, move Z slightly upwards and 
G1 Z+5 E-0.8 F4500

; absolute XYZE
M82
G90

; move to a safe rest position, adjust as necessary
G1 X0 Y220
{% endif %}
```

### Before print Job is Resumed 
```C
{% if pause_position.x is not none %}
; relative extruder
M83

; prime nozzle
G1 E-0.8 F4500
G1 E0.8 F4500
G1 E0.8 F4500

; absolute E
M82

; absolute XYZ
G90

; reset E
G92 E{{ pause_position.e }}

; WARNING!!! - use M83 or M82(extruder absolute mode) according what your slicer generates
M83 ; extruder relative mode

; move back to pause position XYZ
G1 X{{ pause_position.x }} Y{{ pause_position.y }} Z{{ pause_position.z }} F4500

; reset to feed rate before pause if available
{% if pause_position.f is not none %}G1 F{{ pause_position.f }}{% endif %}
{% endif %}
```


**TODO:** 

 * Support Files from Other slicer rathen than just OrcaSlicer.