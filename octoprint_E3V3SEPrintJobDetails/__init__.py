# coding=utf-8
from __future__ import absolute_import
import re
import time
import octoprint.plugin


class E3v3seprintjobdetailsPlugin(octoprint.plugin.StartupPlugin,
                                  octoprint.plugin.EventHandlerPlugin,
                                  octoprint.plugin.SettingsPlugin,
                                  octoprint.plugin.AssetPlugin,
                                  octoprint.plugin.TemplatePlugin
                                  ):
    
    def __init__(self):
        self.total_layers = 0
        self.wasLoaded = False

    def on_after_startup(self):
        self._logger.info(">>>>>> E3v3seprintjobdetailsPlugin Loaded <<<<<<")
        
        
    def on_event(self, event, payload):
        self._logger.info(f">>>>>> E3v3seprintjobdetailsPlugin Event detected: {event}")  # Verify Events Better to comment this
        
        if event == "PrintCancelled": #clean variables after cancellation
            self.wasLoaded = False
            self.total_layers = 0
            
        
        if event == "FileSelected": # If file selected gather all data
            self.wasLoaded = True
            time.sleep(0.5)
            self.get_print_info(payload)

        if event == "PrintStarted": # If Prnt Started, check if was loaded or not to gather the data or just update the data
            time.sleep(0.5)
            if not self.wasLoaded:
                self._logger.info("Not Loaded getting all info")
                self.get_print_info(payload)
            else:    
                self.update_print_info()

        if event == "ZChange":  # Update the info every Z change
            self.update_print_info()
        
        if event == "PrintDone":# When Done change the screen and show the values
            self.send_O9000_cmd(f"UET|00:00:00")
            self.send_O9000_cmd(f"UCL|{self.total_layers}")
            self.send_O9000_cmd(f"UPP|100")
            self.send_O9000_cmd(f"PF|")
            self.wasLoaded = False
            self.total_layers = 0
            
                        
    def get_print_info(self, payload):  # Get the print info
        time.sleep(0.3)
        file_path = self._file_manager.path_on_disk("local", payload.get("path"))
        self._logger.info(f"File selected: {file_path}")
        self.total_layers = self.find_total_layers(file_path)
        
        if self.total_layers:
            self._logger.info(f"Total layers found: {self.total_layers}")

        else:
            self._logger.info("Total layers not found in the file.")
        
        file_name = self._printer.get_current_data().get("job", {}).get("file", {}).get("name", "DefaultName")
        print_time = self._printer.get_current_data().get("job", {}).get("estimatedPrintTime", "00:00:00")
        print_time_left = 0
        current_layer = 0
        progress = 0
        
        self._logger.info(f"File selected: {file_name}")
        self._logger.info(f"Print Time: {print_time}")
        self._logger.info(f"Print Time Left: {print_time_left}")
        self._logger.info(f"current layer: {current_layer}")
        self._logger.info(f"progress: {progress}")            
        
        self._logger.info(f"Print Time: {self.seconds_to_hms(print_time)}")
        self._logger.info(f"Print Time Left: {self.seconds_to_hms(print_time_left)}")
        #Send the print Info using custom O Command O9000 to the printer
        self.send_O9000_cmd(f"SFN|{file_name}")
        self.send_O9000_cmd(f"STL|{self.total_layers}")
        self.send_O9000_cmd(f"SCL|       0")
        self.send_O9000_cmd(f"SPT|{self.seconds_to_hms(print_time)}")
        self.send_O9000_cmd(f"SET|{self.seconds_to_hms(print_time)}")
        self.send_O9000_cmd(f"SPP|{progress}")
        self.send_O9000_cmd(f"SC|")        

                    
    def update_print_info(self): # Get info to Update
        self._logger.info(f">>>>>> E3v3seprintjobdetailsPlugin Update Info")  
        print_time = self._printer.get_current_data().get("job", {}).get("estimatedPrintTime", "00:00:00")          
        print_time_left = self._printer.get_current_data().get("progress", {}).get("printTimeLeft", "00:00:00")
        current_layer = self._printer.get_current_data().get("currentZ", "0")
        
        if print_time_left is None or print_time_left == 0:
            print_time_left = print_time
        
        if current_layer is None or current_layer == 0:
            current_layer = 0
        
        progress = (((print_time - print_time_left) / (print_time)) * 100  ) # Progress is kinda shitty, but its what it is
        
        self._logger.info(f"Print Time: {print_time}")
        self._logger.info(f"Print Time: {self.seconds_to_hms(print_time)}")
        self._logger.info(f"Print Time Left: {print_time_left}")
        self._logger.info(f"Print Time Left: {self.seconds_to_hms(print_time_left)}")
        self._logger.info(f"current layer: {current_layer}")
        self._logger.info(f"progress: {progress}")
        #Send the print Info using custom O Command O9000 to the printer
        self.send_O9000_cmd(f"UET|{self.seconds_to_hms(print_time_left)}") 
        self.send_O9000_cmd(f"UCL|{str(round(current_layer)).rjust(7, ' ')}")
        self.send_O9000_cmd(f"UPP|{progress}")
                 
    
    def find_total_layers(self, file_path):
        #Find the Total Layer string in GCODE
        try:
            with open(file_path, "r") as gcode_file:
                for line in gcode_file:
                    if "; total layer number:" in line:
                        # Extraer el número de capas de la línea
                        total_layers = line.strip().split(":")[-1].strip()
                        return total_layers
        except Exception as e:
            self._logger.error(f"Error reading file {file_path}: {e}")
            return None
        return None
    

    def seconds_to_hms(self, seconds_float): # Classic function to change Seconds in to hh:mm:ss
        seconds = int(round(seconds_float))
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    
    
    def send_O9000_cmd(self, value):  # Send the comand to the printer
        #self._logger.info(f"Trying to send command: O9000 {value}")
        self._printer.commands(f"O9000 {value}")
        
        
        
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "E3V3SEPrintJobDetails": {
                "displayName": "E3v3seprintjobdetails Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "navaismo",
                "repo": "OctoPrint-E3v3seprintjobdetails",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/navaismo/OctoPrint-E3v3seprintjobdetails/archive/{target_version}.zip",
            }
        }

        

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "E3v3seprintjobdetails Plugin"

__plugin_version__ = "0.0.7"
# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3
__plugin_implementation__ = E3v3seprintjobdetailsPlugin()


