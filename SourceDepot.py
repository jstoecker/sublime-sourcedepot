import sublime
import sublime_plugin
import subprocess
import threading
import os

# Replace these with your own %SDXROOT%
# TODO: there's got to be a better way than this, but launching a new razzle is
# too slow.
sd_path = "s:\\fbl_grfx_dev\\tools\\amd64\\sd"
sdv_path = "s:\\fbl_grfx_dev\\tools\\x86\\sdv"

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

def WriteToPanel(edit, text):
    panel_name = "source_depot"
    window = sublime.active_window()
    panel = window.get_output_panel(panel_name)
    panel.insert(edit, panel.size(), text)
    window.run_command("show_panel", {"panel": "output." + panel_name})

def RunSdvCommand(command, directory, file=""):
    subprocess.Popen(
        "cmd.exe /c %s %s %s" % (sdv_path, command, file),
        cwd = directory,
        shell = True,
        universal_newlines = True)

def RunSdvCommandOnFile(command, filename):
    directory, file = os.path.split(filename)
    RunSdvCommand(command, directory, file)

def RunSdvCommandOnDirectory(command, filename):
    directory, file = os.path.split(filename)
    RunSdvCommand(command, directory)

def RunSdCommandOnFile(command, filename):
    directory, file = os.path.split(filename)
    proc = subprocess.Popen(
        "cmd.exe /c %s %s %s" % (sd_path, command, file),
        cwd = directory,
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)
    output, error = proc.communicate()
    result = output if len(error) == 0 else error
    return result

# ------------------------------------------------------------------------------
# SD Commands
# ------------------------------------------------------------------------------

class SdEditCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        result = RunSdCommandOnFile("edit", self.view.file_name())
        WriteToPanel(edit, result)

class SdRevertCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        result = RunSdCommandOnFile("revert", self.view.file_name())
        WriteToPanel(edit, result)

class SdAddCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        result = RunSdCommandOnFile("add", self.view.file_name())
        WriteToPanel(edit, result)

# ------------------------------------------------------------------------------
# SDV Commands
# ------------------------------------------------------------------------------

class SdvChangesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        RunSdvCommandOnFile("changes", self.view.file_name())

class SdvGraphCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        RunSdvCommandOnFile("graph", self.view.file_name())

class SdvOpenedCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        RunSdvCommandOnDirectory("opened", self.view.file_name())