# yamiconfig -- Yet Another Configuration library

## Usage
1.  Create a YAML template file
1.  During installation of your app:
```python
from yamiconfig import initialize_settings_file_from_file
initialize_settings_file_from_file(path_to_settings_template)
```

That will store a config file at `~/.config/my-app/my-app-config.yaml`.  This file will be used the next time you call `Config(app_name="my-app")` in your application.

## Advanced Usage

### Multiple settings files
This package supports multiple configuration files.  For example, you may store system settings in `/etc/my-app/my-app-config.yaml`, and user settings in `~/.config/my-app/my-app-config.yaml`.  In this case, the _user_ file should take precedence over the system settings.

The order of these files is important.  The _system_ file, e.g. `/etc/my-app/my-app-config.yaml`, is considered the least important settings file.  You can then use the `search_dirs` parameter to add increasingly-important folders to load settings from.

Here's a complete example:
```python
from yamiconfig import Config
c = Config(
    app_name="my-app",
    system_dir="/etc/my-app",
    search_dirs=["~/.config/my-app", "./instance"]
)
```

This creates an object where `./instance/my-app-config.yaml` overrides `~/.config/my-app/my-app-config.yaml` that overrides `/etc/my-app/my-app-config.yaml`.

**WARNING**: The example above would need write permissions to `/etc/`, which is normally reserved for the `root` user.

You are not required to pass in _any_ directories.  The default config directory is `~/.config/my-app`.  You can simply use the following code:
```python
from yamiconfig import Config
c = Config(app_name="my-app)
```

This will attempt to load `~/.config/my-app/my-app-config.yaml`.