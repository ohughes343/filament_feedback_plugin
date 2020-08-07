# coding=utf-8
from __future__ import absolute_import

import logging
import time
import os
import sys

import octoprint.plugin
import octoprint.settings

import measure

__plugin_name__ = "Filament Feedback"
__plugin_version__ = "1.0"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_init__():
    global _plugin
    global __plugin_hooks__

    global __plugin_implementation__
    __plugin_implementation__ = FilamentFeedbackPlugin()
    
    __plugin_hooks__ = {
        #"octoprint.comm.protocol.action": __plugin_implementation__.hook_actioncommands, 
        "octoprint.comm.protocol.action": __plugin_implementation__.update_extrusion_rate,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

class FilamentFeedbackPlugin(octoprint.plugin.TemplatePlugin,
              octoprint.plugin.AssetPlugin,
              octoprint.plugin.SettingsPlugin):

    DELAY = 84000 #delay in e-steps from detection to hot end
    FEEDRATE
    
    def update_extrusion_rate(self,command):
        
        #get the command from commander.py
        rate=measure.change_extrusion_rate() 

        if command == None:
            return

        else:
            try:
                this_command = self.command_definitions[command]
                self._logger.info("Command found for 'action:%s'" % (command))
            except:
                self._logger.error("No command found for 'action:%s'" % command)
                return (None,)
        
        if this_command["enabled"] == True:
            self._logger.info("Command 'action:%s' is enabled" % command)

        if rate=None:
            return
        else:
            self._logger.info("Executing printer command '%s'" % ('M221 S%d'%(rate)))
            self._logger.info('M117 Extrusion rate=%d'%(rate)) #sets LCD message
            self._printer.commands('M221 S%d'%(rate)) #ex: "M221 S150" sets extrusion rate to 150% 

    
    
    def __init__(self):
        self.command_definitions = {}

    def on_settings_initialized(self):
        self.reload_command_definitions()

    def reload_command_definitions(self):
        self.command_definitions = {}

        command_definitions_tmp = self._settings.get(["command_definitions"])
        self._logger.debug("command_definitions: %s" % command_definitions_tmp)

        for definition in command_definitions_tmp:
            self.command_definitions[definition['action']] = dict(type=definition['type'], command=definition['command'], enabled=definition['enabled'])
            self._logger.info("Add command definition 'action:%s' = %s" % (definition['action'], definition['command']))

    def get_settings_defaults(self):
        return dict(
            command_definitions = []
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.reload_command_definitions()

    def get_template_configs(self):
        return [
            dict(type="settings", name="Filament Feedback", custom_bindings=True)
        ]

    def get_assets(self):
        return {
            "js": ["js/actioncommands.js"]
        } 

    def get_update_information(self):
        return dict(
        actioncommands=dict(
        displayName="Filament Feedback",
        displayVersion=self._plugin_version,
        
        # version check: github repository
        type="github_release",
        user="ohughes343",
        repo="filament_feedback",
        current=self._plugin_version,
        
        # update method: pip w/ dependency links
        pip="https://github.com/ohughes343/filament_feedback/archive/{target_version}.zip"
        )
    )

    

    def hook_actioncommands(self, comm, line, command):
        self._logger.info("Command received: 'action:%s'" % (command))
        
        if command == None:
            return

        else:
            try:
                this_command = self.command_definitions[command]
                self._logger.info("Command found for 'action:%s'" % (command))
            except:
                self._logger.error("No command found for 'action:%s'" % command)
                return (None,)

        if this_command["enabled"] == True:
            self._logger.info("Command 'action:%s' is enabled" % command)
            
        else:
            self._logger.info("Command 'action:%s' is disabled" % command)
            return (None,)

        if this_command["type"] == "gcode":
            self._logger.info("Command 'action:%s' is type 'gcode'" % (command))
            self._logger.info("Executing printer command '%s'" % (this_command["command"]))
            self._printer.commands(this_command["command"].split(";")) #pretty sure this line sends gcode command

            
        else:
            self._logger.error("Command type not found or not known for 'action:%s'" % command)
            return (None,)