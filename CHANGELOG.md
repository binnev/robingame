## 2.0.0 (2023-09-01)

### BREAKING CHANGE

- Font.__init__ now expects a list of images instead of a filename.

### Feat

- **font**: Font.__init__ -> from_spritesheet and from_image_sequence
- **text**: Added new font "tiny"
- **text**: changed how Font.__init__ initialises space
- **text**: Added a couple more fonts

### Fix

- **text**: Added a better test text to font_sandbox.py.

## 1.0.1 (2023-07-16)

### Fix

- **release.py**: need to add a dummy change to bump the version because testpypi also does not allow you to reupload a version :(

## 1.0.0 (2023-07-16)

### BREAKING CHANGE

- Changed the signature of load_image_sequence
- moved SpriteAnimation to new file so will break old implementations
- moved font.py and fonts.py so will break imports for old implementations.

### Feat

- **robingame.examples.hello_world.py**: Added a new example and also a corresponding docs page

### Refactor

- **robingame.image.utils**: mostly added docs, but refactored some functions
- **robingame.image**: Moved SpriteAnimation to its own file and added docs
- **robingame.text**: Moved font.py and fonts.py up one level. Added a docs section for text.

## 0.0.4 (2022-09-29)
