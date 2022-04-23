



import obspython as obs
import subprocess

amount_of_commands = 1
commands = None

def script_description():
	return """Enables execution of shell commands from obs and autostart them.
Autostart happens on script load (startup or reload) or on stream start.

e.g.: run Python script:
    \"python C:\path\\to\script.py\"

e.g.: start new cmd and execute command there:
    \"cmd /k <cmd to execute>\"
    
e.g.: start new powershell and execute command there:
    \"powershell -noexit -Command <cmd to execute>"\"

by Tobd"""



def script_update(settings):
    global amount_of_commands
    global commands

    amount_of_commands   = obs.obs_data_get_int(settings, "amount_of_commands")
    commands         = list()

    for i in range(1, amount_of_commands+1):
        cmd = dict()
        cmd["cmd_list"] = obs.obs_data_get_string(settings, f"cmd_{i}").split()
        cmd["start_load"] = obs.obs_data_get_bool(settings, f"cmd_autostart_load_{i}")
        cmd["start_stream"] = obs.obs_data_get_bool(settings, f"cmd_autostart_stream_{i}")
        
        commands.append(cmd)

    
def start_process(cmd_list:list):
    print(f"Starting \"{' '.join(cmd_list)}\"")

    proc = subprocess.Popen(cmd_list, creationflags=subprocess.CREATE_NEW_CONSOLE)

def start_process_btn(props, prop):
    index = int(obs.obs_property_name(prop).split("_")[-1]) -1
    start_process(commands[index]["cmd_list"])

def script_load(settings):
    script_update(settings)
    obs.obs_frontend_add_event_callback(on_event)
    for cmd in commands:
        if cmd["start_load"]:
            start_process(cmd["cmd_list"])

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        streaming_started()

def streaming_started():
    for cmd in commands:
        if cmd["start_stream"]:
            start_process(cmd["cmd_list"])


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "amount_of_commands", "Amount of Scripts", 1, 10, 1)

    for i in range(1, amount_of_commands+1):
        obs.obs_properties_add_text(props, f"cmd_{i}", f"Command {i}", obs.OBS_TEXT_DEFAULT)
        obs.obs_properties_add_bool(props, f"cmd_autostart_load_{i}", f"Command {i}: Execute on load")
        obs.obs_properties_add_bool(props, f"cmd_autostart_stream_{i}", f"Command {i}: Execute on stream start")

        obs.obs_properties_add_button(props, f"start_btn_{i}", f"Start Script {i}", start_process_btn)

    return props
