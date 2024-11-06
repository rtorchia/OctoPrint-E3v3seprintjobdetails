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

**TODO:** 

 * Support Files from Other slicer rathen than just OrcaSlicer.