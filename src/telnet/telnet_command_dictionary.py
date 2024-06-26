# dictiorary of commands and their descriptions for omron LD-250. Generated from the telnet server, so these are specific to the LD-250. 

commands_dict = {
    "addCustomCommand": "Adds a custom command that'll send a message out ARCL when called",
    "addCustomStringCommand": "Adds a custom string command that'll send a message out ARCL when called",
    "analogInputList": "Lists the named analog inputs",
    "analogInputQueryRaw": "Queries the state of an analog input by raw",
    "analogInputQueryVoltage": "Queries the state of an analog input by voltage",
    "applicationBlockDrivingClear": "Clears an application blockDriving [abdc]",
    "applicationBlockDrivingSet": "Sets an application blockDriving [abds]",
    "applicationFaultClear": "Clears an application fault [afc]",
    "applicationFaultQuery": "Gets the list of any application faults currently triggered [afq]",
    "applicationFaultSet": "Sets an application fault [afs]",
    "arclSendText": "Sends the given message to all ARCL clients",
    "arclStat": "Show ARCL status [ast]",
    "centralServer": "Gets information about the central server connection",
    "connectOutgoing": "(re)connects a socket to the given outside server",
    "createInfo": "creates a piece of information",
    "dock": "Sends the robot to the dock",
    "doTask": "does a task",
    "doTaskInstant": "does an instant task (doesn't interrupt modes)",
    "echo": "with no args gets echo, with args sets echo",
    "enableMotors": "Enables the motors so the robot can drive again",
    "executeMacro": "executes a given macro",
    "executeMacroTemplate": "executes a specified macro template with the given parameters",
    "extIOAdd": "Adds the external digital inputs and outputs [eda]",
    "extIOInputUpdate": "Updates the external digital inputs [ediu]",
    "extIOInputUpdateBit": "Updates an external digital input bit, e.g. bit 32 most significant bit, bit 1 least [edib]",
    "extIOInputUpdateByte": "Updates an external digital input byte, e.g. byte 4 in a 32-bit bank is most significant [edi8]",
    "extIOOutputUpdate": "Updates the external digital outputs [edou]",
    "extIOOutputUpdateBit": "Updates an external digital output bit, e.g. bit 32 most significant bit, bit 1 least [edob]",
    "extIOOutputUpdateByte": "Updates an external digital output byte, e.g. byte 4 in a 32-bit bank is most significant [edo8]",
    "extIORemove": "Removes the external digital inputs and outputs [edr]",
    "faultsGet": "Gets the list of any faults currently triggered [fg]",
    "getConfigSectionInfo": "Gets the info about a section of the config",
    "getConfigSectionList": "Gets the list of sections in the config",
    "getConfigSectionValues": "Gets the values in a section of the config",
    "getDataStoreFieldInfo": "Gets the info on a field in the Data Store [dsfi]",
    "getDataStoreFieldList": "Gets the list of field names in the Data Store [dsfl]",
    "getDataStoreFieldValues": "Gets the values of a field in the Data Store [dsfv]",
    "getDataStoreGroupInfo": "Gets the info on a group in the Data Store [dsgi]",
    "getDataStoreGroupList": "Gets the list of groups in the Data Store [dsgl]",
    "getDataStoreGroupValues": "Gets the values of a group in the Data Store [dsgv]",
    "getDataStoreTripGroupList": "Gets the list of groups with trip values in the Data Store [dstgl]",
    "getDateTime": "gets the date and time",
    "getGoals": "gets a list of goals in the map (for use with goto)",
    "getInfo": "Gets a piece of information",
    "getInfoList": "Gets the list of info available from 'getInfo'",
    "getMacros": "gets a list of macros in the map (for use with executeMacro)",
    "getMacroTemplates": "gets a list of macro templates in the map (for use with executeMacroTemplates)",
    "getPoseEncoder": "Gets the encoder pose of the robot",
    "getRoutes": "gets the routes the robot has",
    "go": "Stops the robot from any wait it is doing then resume patrolling or makes the robot idle 2 minutes so that it will resume doing queued jobs (with the right parameters).  See also stay.",
    "goalDistanceRemaining": "Gets the distance remaining to robots goals",
    "goalDistanceRemainingLocal": "Gets the distance remaining to this robot's goal",
    "help": "gives the listing of available commands (optionally with prefix)",
    "inputList": "Lists the named digital inputs [inL]",
    "inputQuery": "Queries the state of a named digital input [inQ]",
    "localizeAtGoal": "Localizes to a given goal [lag]",
    "log": "Logs the message to the normal log file",
    "mapObjectInfo": "Gets the information about a map object specified by name.",
    "mapObjectList": "Gets a list the map objects of a given type.",
    "mapObjectTypeInfo": "Gets information about a particular type of map object.",
    "mapObjectTypeList": "Gets a list of the types of map objects in the map.",
    "mapObjectUpdate": "Creates or updates a map object with the specified data.",
    "modeLock": "Locks the current mode",
    "modeQuery": "Queries the current mode and its lock status",
    "modeUnlock": "Unlocks the current mode",
    "newConfigParam": "Adds a new param to the config (shows up in MP)",
    "newConfigParamEnd": "Finishes adding multiple params to the config. Must be paired with a newConfigParamStart.",
    "newConfigParamStart": "Starts adding multiple params to the config. Optional. If specified, must be followed by a newConfigParamEnd.",
    "newConfigSectionComment": "Adds a comment to a section (shows up in MP)",
    "odometer": "Shows the robot trip odometer",
    "odometerReset": "Resets the robot trip odometer",
    "oneLineStatus": "Gets the status of the robot on one line",
    "outputList": "Lists the named outputs [outL]",
    "outputOff": "Turns off a named digital output [outOff]",
    "outputOn": "Turns on a named digital output [outOn]",
    "outputQuery": "Queries the state of a named output [outQ]",
    "patrol": "patrols the given route",
    "patrolOnce": "Patrols the given route once, starts at optional index",
    "patrolResume": "Resumes the last patrol",
    "play": "Plays the given wave file already on the robot",
    "popupSimple": "Creates a simple popup",
    "queryDockStatus": "Gets the docking status",
    "queryMotors": "Queries the state of the motors",
    "quit": "closes this connection to the server",
    "say": "Says the given string",
    "shutdown": "shuts down the robot",
    "status": "Gets the status of the robot",
    "stay": "Makes the robot wait for a minute, then resume patrol or become idle 2 minutes so that it will resume queued jobs (with the right parameters).  See also go.",
    "stop": "Stops the robot",
    "tripReset": "Resets the trip values in the Data Store [tr]",
    "undock": "Undocks the robot (done automatically too)",
    "updateInfo": "updates a piece of information",
    "waitTaskCancel": "Cancels the wait task (if it's active, causing it to succeed)",
    "waitTaskFail": "Fails the wait task (if it's active)",
    "waitTaskState": "Gets the state of the wait task"
}
