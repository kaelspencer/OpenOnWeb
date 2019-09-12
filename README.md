# OpenOnWeb
A Sublime Text 3 plugin to open your current file on its backing source control's web view (e.g., GitHub, VSTS).

## Project Settings
Add a `git_command` and `base_url` to your project settings. The URL is a format string with `branch` and `path` as format arguments. `branch` is taken from the current branch in the repo; `path` is a relative path to the current file from the root of the repo.

Samples:

```
"OpenOnWeb":
{
    "base_url": "https://github.com/kaelspencer/OpenOnWeb/blob/{branch}/{path}",
    "git_command": "c:\\program files\\git\\cmd\\git.exe"
}


"OpenOnWeb":
{
    "base_url": "https://microsoft.visualstudio.com/_git/os?version=GB{branch}&path={path}",
    "git_command": "c:\\program files\\git\\cmd\\git.exe"
}
```
