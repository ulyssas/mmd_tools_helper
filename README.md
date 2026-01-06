# MMD Tools Helper

[MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools/) must be installed for this add-on to work.

All of the operators in this add-on have "flexible selection". An imported MMD model has a root/empty object, an armature object, and one or more mesh objects. It does not matter which of these is selected to be the active object. All operators in MMD Tools Helper are programmed to automatically find the correct part of the MMD model that it should operate on.

## Bone Tools

### Add leg IK to MMD model

Convenient one-click adding of IK bones and constraints to an MMD model, a useful time-saver when converting models to MMD from other software. If the model already has foot-leg IK, the IK will be removed and replaced with new IK, so this operator can also be used to automatically fix foot-leg IK errors of an MMD model.

The model must have MMD standard names of leg and foot bones.

### Add arm IK to MMD model

Adds hand-arm IK to an MMD model. Please note that this operator **DOES NOT** produce "standard MMD arm IK" from [IK Maker X](https://paperguitar.com/mmd-related-items/134-ik-makerx.html), which means it won't work correctly if the model has arm-twist bone.

The model must have MMD standard names of arm and hand bones.

### Armature Diagnostic

Select a bone map from the list menu, then click the button. A list of the bone names, which are missing from the armature, will be shown in the popup.

## Rename Tools

### Replace bone names

Finds the specified word in the bone names, and then replaces them. It's "find & replace" for the bone names. Useful for mass renaming names.

### Batch rename bones

Select the source and destination armature types. Then click the button to do a mass renaming of bones from one armature type to another. After renaming a diagnostic list or missing bone names is printed to the Blender System Console. A time-saver when converting models or animations from one format to another. There are 15 supported armature types.

### Swap Japanese & English names

Swaps the Japanese and English names of bones, shape keys and materials. The Japanese names become English names and the English names become Japanese names. If a Japanese name has no English name, it just stays the same. For someone who does not know Japanese, this operator can make it easier to edit an MMD model in Blender.

## Miscellaneous Tools

### MMD Camera to Blender

An MMD Tools "MMD camera" is child of an "MMD camera" empty object and it is also different from a normal Blender camera in other ways. You can convert all "MMD cameras" in the scene back to normal Blender cameras by clicking this button.

### MMD Toon to Toon Shader

Converts MMD material into actual toon shader. It can convert toon texture to make more accurate toon shading.

### Miscellaneous Tools dropdown

4 tools which may be helpful time-savers when converting character models to MMD. These 4 tools are:

### Combine 2 bones

Combines a parent-child pair of bones and their vertex groups to 1 bone and 1 vertex group.
For this operator to run, you must be in Pose Mode, exactly 2 bones must be selected, and one bone must be parent of the other bone.

### Delete unused bones and unused vertex groups (NOT TESTED)

Deletes all bones and all vertex groups which have the word 'unused' (or Unused or UnUsEd or etc.) in them.

### Whiten ambient color

Change the MMD ambient color of all materials to pure white.

### Correct MMD Root and Center bones (NOT TESTED)

This correction only works on a model which has mmd_english bone names, so you may need to do a mass renaming of bones to mmd_english before running this operator. If an MMD model has no root bone (a.k.a. mother bone a.k.a. master parent bone), a root bone is added to it. If an MMD model's center bone has a vertex group, the center bone is renamed and converted to a lower body bone, followed by adding a new center bone. If an MMD model has no center bone, a center bone is added to it. In these operations, all of the correct bone parent-child relations are also added.

## Notice

This repository contains components adapted from [MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools), licensed under the GNU General Public License v3 (GPLv3).
