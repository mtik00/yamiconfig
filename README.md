# yamiconfig -- Yet Another Configuration library

## Usage
1.  Create a YAML template file
1.  During installation of your app:
```python
from yamiconfig import initialize_settings_file_from_file
initialize_settings_file_from_file(path_to_settings_template)
```

That will store a config file at `~/.config/my-app/config.yaml`.  This file will be used the next time you call `Config(app_name="my-app")` in your application.

## Advanced Usage

### Multiple files
This package supports multiple configuration files.  For example, you may store system settings in `/etc/my-app/config.yaml`, and user settings in `~/.config/my-app/config.yaml`.  In this case, the _user_ file should take precedence over the system settings.