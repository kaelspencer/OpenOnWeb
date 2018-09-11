import subprocess
import os
import webbrowser
import sublime
import sublime_plugin


class OpenOnWeb(sublime_plugin.WindowCommand):
    def __init__(self, arg):
        sublime_plugin.WindowCommand.__init__(self, arg)
        self.config = []

    def run(self):
        filename = self.window.active_view().file_name()

        # We'll deal only with /
        filename = filename.replace("\\", "/")

        if len(filename) > 0:
            self.get_config()
            git_root = self.get_git_root(filename)
            relative = self.get_git_relative_path(git_root, filename)

            url = self.config["base_url"] + relative
            print(url)
            self.open_in_browser(url)

    def get_config(self):
        # TODO: Coalesce with global settings.
        self.config = self.window.project_data()["OpenOnWeb"]
        print(self.config)

    def get_git_root(self, filename):
        cwd = os.path.dirname(filename)
        psd = subprocess.Popen([self.config["git_command"], 'rev-parse', "--show-toplevel"], shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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

    def get_git_relative_path(self, git_root, filename):
        # Ensure filename is under git_root. Pathlib would be the proper thing to do here, but it isn't available in Sublime Text.
        if not filename.startswith(git_root):
            print("Git root: {}\nSelected file: {}".format(git_root, filename))
            raise Exception("Selected file is not under git_root.")
        return filename[len(git_root):]

    def open_in_browser(self, url):
        # command = "{} {}".format("chrome.exe", url)
        webbrowser.open_new_tab(url)
