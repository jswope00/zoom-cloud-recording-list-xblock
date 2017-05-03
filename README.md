# zoom-cloud-recording-list-xblock
An embeddable xblock to allow students to view ZOOM cloud recordings list for a ZOOM account

Installation
------------

Make sure that `ALLOW_ALL_ADVANCED_COMPONENTS` feature flag is set to `True` in `cms.env.json`.

Get the source to the /edx/app/edxapp/ folder and execute the following command:

```bash
sudo -u edxapp /edx/bin/pip.edxapp install zoom-cloud-recording-list-xblock/
```

To upgrade an existing installation of this XBlock, fetch the latest code and then type:

```bash
sudo -u edxapp /edx/bin/pip.edxapp install -U --no-deps zoom-cloud-recording-list-xblock/
```

Configuration
-------------

Added following two keys in `lms.auth.json` and `cms.auth.json`

```
"ZOOM_API_KEY":"YOUR_ZOOM_API_KEY",
"ZOOM_API_SECRET":"YOUR_ZOOM_API_SECRET"
```

Added following lines in `edx-platform/lms/envs/aws.py` and `edx-platform/cms/envs/aws.py`

```
ZOOM_API_KEY = AUTH_TOKENS.get("ZOOM_API_KEY")
ZOOM_API_SECRET = AUTH_TOKENS.get("ZOOM_API_SECRET")
```

Added following lines in `edx-platform/lms/envs/common.py` and `edx-platform/cms/envs/common.py`

```
ZOOM_API_KEY = None
ZOOM_API_SECRET = None
```

Enabling in Studio
------------------

You can enable the zoom-cloud-recording-list XBlock in studio through the advanced
settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add
   `"zoomcloudrecording"` to the policy value list.
3. Click the "Save changes" button.
