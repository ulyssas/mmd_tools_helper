# MMD Tools Helper

mmd_tools (UuuNyaa fork) must be installed for this add-on to work.

All of the operators in this add-on have "flexible selection". An MMD model has a root/empty object, an armature object, and one or more mesh objects. It does not matter which of these is selected to be the active object. All operators in this mmd_tools_helper add-on are programmed to automatically find the correct part of the MMD model that it should operate on.

## Panels and buttons

### Add foot leg IK to MMD model

Convenient one-click adding of IK bones and constraints to an MMD model, a useful time-saver when converting models to MMD from other software. If the model already has foot-leg IK, the IK will be removed and replaced with new IK, so this operator can also be used to automatically fix foot-leg IK errors of an MMD model. The model must have MMD standard names of leg and foot bones.

### Add Hand Arm IK to MMD model

Adds hand-arm IK to an MMD model. Please note that this operator has the following limitations:
The model must have MMD standard names of arm and hand bones.
It won't work correctly if an arm-twist bone is a parent bone of one of the arm bones.
If an MMD model has hand-arm IK, its arm bones cannot be animated by normal VMD animations.

### Armature Diagnostic

Select a bone map from the list menu, then click the button. A list of the bone names, which are missing from the armature, is printed to the Blender System Console.

### Bones Renamer

Select the source and destination armature types. Then click the button to do a mass renaming of bones from one armature type to another. After renaming a diagnostic list or missing bone names is printed to the Blender System Console. A time-saver when converting models or animations from one format to another. There are 15 supported armature types.

### Reverse Japanese and English names

Reverses the Japanese and English names of bones, shape keys and materials. The Japanese names become English names and the English names become Japanese names. If a Japanese name has no English name, it just stays the same. For someone who does not know Japanese, this operator can make it easier to edit an MMD model in Blender.

### Convert MMD Camera to Blender Camera button

An mmd_tools "MMD camera" is child of an "MMD camera" empty object and it is also different from a normal Blender camera in other ways. You can convert all "MMD cameras" in the scene back to normal Blender cameras by clicking this button.

### MMD Create Toon Material Nodes button

Adds node editor material nodes for the rendering of Toon Textures in Blender for an MMD model which has been imported with mmd_tools(powroupi fork).

### Miscellaneous Tools Panel

4 tools which may be helpful time-savers when converting character models to MMD. These 4 tools are:

### Combine 2 bones

Combines a parent-child pair of bones and their vertex groups to 1 bone and 1 vertex group.
For this operator to run, exactly 2 bones must be selected, and one bone must be parent of the other bone.

### Delete unused bones and unused vertex groups

Deletes all bones and all vertex groups which have the word 'unused' (or Unused or UnUsEd or etc.) in them.

### All materials MMD ambient color white

Change the MMD ambient color of all materials to maximum white.

### Correct MMD Root and Center bones

This correction only works on a model which has mmd_english bone names, so you may need to do a mass renaming of bones to mmd_english before running this operator. If an MMD model has no root bone (a.k.a. mother bone a.k.a. master parent bone), a root bone is added to it. If an MMD model's center bone has a vertex group, the center bone is renamed and converted to a lower body bone, followed by adding a new center bone. If an MMD model has no center bone, a center bone is added to it. In these operations, all of the correct bone parent-child relations are also added.

## Changes

changed in mmd_tools_helper 2.4:

Added a new operator (button) "Copy Blender bone names to Japanese bone names".
This operator is useful if you are doing a mass renaming of bones of a .pmx model which you have imported into Blender with mmd_tools. In that case, you should select "Copy Blender bone names to Japanese bone names" as the final step before exporting the model to a .pmx file.

(When mmd_tools exports a .pmx model, it looks at the Japanese bone name of each bone. If a bone does not have a Japanese bone name, it copies the Blender bone name to be the Japanese bone name. But if the bone already has a Japanese bone name, the Japanese bone name stays the same, and all of the renaming of Blender bone names which you have done in Blender will be lost and will not be exported.)

## Notice

This repository contains components adapted from [MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools), licensed under the GNU General Public License v3 (GPLv3).
