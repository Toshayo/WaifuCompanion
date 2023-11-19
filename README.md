# Waifu Companion

This is the core app of the desktop companion that flies or walks
around your screen.

## Assets

To avoid copyright issues, assets are not included in this repository.
Assets are stored in ``assets/models/`` folder. Each companion model is stored
in a different folder, for example, ``assets/models/companion1/``. The
model folder should contain a **manifest.json** file that will describe
the sprite-sheet, size and so on.

Here is an example manifest :
```json
{
  "name": "Companion 1",
  "inverted": true,
  "scale": 1,
  "language": "en",
  "canFly": true,
  "aabb": {
    "x": 0,
    "y": 0,
    "width": 264,
    "height": 220
  },
  "sprite": {
    "meta": {
      "image": "companion.png",
      "format": "RGBA8888",
      "size": {
        "w": 300,
        "h": 500
      },
      "scale": 1
    },
    "spriteCount": {
      "w": 1,
      "h": 1
    }
  }
}
```
The file consists of :
- **name** - is the name of the model that will be displayed in the tray menu.
- **inverted** - used to invert the sprite-sheet so the character moves in
the right direction.
- **scale** - used to scale the sprite.
- **language** - used in some plugins, for example, DialogFlow Integration plugin.
- **canFly** - used to define if the character can walk or fly.
- **aabb** - used to redefine character bounding box.
- **sprite** - sprite definition which consists of :
    - **meta** - sprite-sheet file, format, size and scale.
    Format and scale are usually not changed.
    - **spriteCount** - number of horizontal and vertical sprites.
    The sprite-sheet is walked from the left to the right, from up to down.

## Plugins
The app has a plugin system that allows to add more functionality to
your characters. Plugins are located in ``plugins/`` folder.

If the plugin requires specific python packages, they can be defined in
the plugin folder with a **requirements.txt** file. It will be automatically
installed on core app install.

[Prompt Plugin]() is an example of a plugin (though very simple and not
showing event usage as it was created as a dependency for other plugins)
