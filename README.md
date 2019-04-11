**PBS Helper** is a blender2.8+ addon.  
is design for make blender to realtime render workflow smooth.  
**LICENES under LGPL3**

<!-- reference images -->

features
- bake image from shader editor
- bake pbr image from shader editor
- merge multi material to one
- merge mesh to one
- pbr paint helper

design for smooth workflow
- pbr texture genarater.
- pbr paint
- export asset to game engine
- simple material

improve render speed
- disable modify
- fast cycle render settings

## install
- application templete
- addon
- presets

```sh
blender --background -P install.py
```

purge uninstall
```sh
blender --background -P install.py -U
```

## usage
templete

image bake

shader bake

### preset
use preset img

preset manager img
add preset
1. make ..
2. make material
3. add and name
ovriwrite same name


## workflow
### generate pbr texture from image
append generate scene

选择图片，清晰，无方向光 repeat texture
composition workflow
1. init project
2. save blend file
3. edit bitmap image
4. adjust material
5. texture generate
6. adjust texture 
   1. paint basecolor with krita 
7.  regenerate texture

### PBR paint

## reference
- [Blending in Detail](https://blog.selfshadow.com/publications/blending-in-detail/)

## support project
blender market
spa
itch.io


