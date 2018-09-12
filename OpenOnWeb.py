import subprocess
import os
import webbrowser
import sublime
import sublime_plugin

PLUGIN_NAME = 'OpenOnWeb'
GIT_COMMAND_KEY = 'git_command'
BASE_URL_KEY = 'base_url'


class OpenOnWeb(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)

        print("---------------------Loading OpenOnWeb---------------------")
        print("git_command: {}".format(self.get_setting(GIT_COMMAND_KEY)))
        print("base_url: {}".format(self.get_setting(BASE_URL_KEY)))

    def run(self):
        filename = self.window.active_view().file_name()

        # We'll deal only with /
        filename = filename.replace("\\", "/")

        if len(filename) > 0:
            git_root = self.get_git_root(filename)
            relative = get_git_relative_path(git_root, filename)

            url = self.get_setting(BASE_URL_KEY) + relative
            print(url)
            open_in_browser(url)

    def get_setting(self, key):
        settings = sublime.load_settings("OpenOnWeb.sublime-settings")
        project_data = self.window.project_data()

        if project_data is not None and project_data[PLUGIN_NAME] is not None and key in project_data[PLUGIN_NAME]:
            return project_data[PLUGIN_NAME][key]
        return settings.get(key)

    def get_git_root(self, filename):
        cwd = os.path.dirname(filename)
        psd = subprocess.Popen([self.get_setting(GIT_COMMAND_KEY), 'rev-parse', "--show-toplevel"], shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        root = str(psd.communicate()[0])

        # Path may have trailing escaped \n', remove.
        if root.endswith("\\n'"):
            root = root[:-3]
        if root.startswith("b'"):
            root = root[2:]

        # We'll deal only with /
        root = root.replace("\\", "/")

        if not os.path.exists(root):
            raise Exception("Problem determining git repo root.")
        return root


def get_git_relative_path(git_root, filename):
    # Ensure filename is under git_root. Pathlib would be the proper thing to do here, but it isn't available in Sublime Text.
    if not filename.startswith(git_root):
        print("Git root: {}\nSelected file: {}".format(git_root, filename))
        raise Exception("Selected file is not under git_root.")
    return filename[len(git_root):]


def open_in_browser(url):
    webbrowser.open_new_tab(url)
