import sublime, sublime_plugin, subprocess, os


# ----------------------------------------------------------------------------
def output_to_panel(edit, text):
	panel_name = 'source_depot'
	window = sublime.active_window()
	panel = window.get_output_panel(panel_name)
	panel.insert(edit, panel.size(), text)
	window.run_command('show_panel', {'panel': 'output.' + panel_name})

# ----------------------------------------------------------------------------
def run_cmd(edit, command, directory, show_output=True):
	proc = subprocess.Popen("cmd.exe /c " + command,
							cwd=directory,
							shell=True, 
							stdout=subprocess.PIPE, 
							stderr=subprocess.PIPE, 
							universal_newlines=True)

	if show_output:
		output, error = proc.communicate()
		if len(error) == 0:
			output_to_panel(edit, output)
		else:
			output_to_panel(edit, "ERROR:\n" + error)


# ----------------------------------------------------------------------------
class SdAddCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dir, file = os.path.split(self.view.file_name())
		run_cmd(edit, "sd add " + file, dir)

# ----------------------------------------------------------------------------
class SdEditCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dir, file = os.path.split(self.view.file_name())
		run_cmd(edit, "sd edit " + file, dir)

# ----------------------------------------------------------------------------
class SdRevertCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dir, file = os.path.split(self.view.file_name())
		run_cmd(edit, "sd revert " + file, dir)

# ----------------------------------------------------------------------------
class SdChangesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dir, file = os.path.split(self.view.file_name())
		run_cmd(edit, "sd changes " + file, dir)

# ----------------------------------------------------------------------------
class SdOpenedCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		dir, file = os.path.split(self.view.file_name())
		run_cmd(edit, "sd opened", dir)




#TODO
#	one command with an argument called from the other file
# 	diff
