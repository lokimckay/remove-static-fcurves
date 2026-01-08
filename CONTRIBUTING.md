Templated from [lokimckay/blender-extension-template](https://github.com/lokimckay/blender-extension-template)

## Requirements

- [PDM](https://pdm-project.org/en/latest/#installation)

## Contributing quickstart

### Installation

```shell
pdm install
```

### Developing

```
pdm run dev
```

Any changes made in external editors should automatically reflect in blender.

### Releasing

1. Bump version in `src/blender_manifest.toml`
2. Commit and push
3. Run `pdm run build`
4. Upload the generated zip file to `https://extensions.blender.org/add-ons/remove-static-fcurves/manage/versions/new/`

## Features

- Automatic hot-reloading in blender when changes are made
- Get if running in dev/prod environment in python via `env.py` file
- Optionally add a "dev.blend" file in the `scripts` directory to load that file when developing

## Relevant documentation

- [How to Create Extensions](https://docs.blender.org/manual/en/latest/advanced/extensions/getting_started.html)

## Troubleshooting

- Check if your extension is enabled in `Edit` -> `Preferences`
- Ensure extension names/ids match between `config.yml` and `blender_manifest.toml`
- "No module named `<your extension name>`" - ensure that the directory name under `src/my_example_extension` matches your extension name
