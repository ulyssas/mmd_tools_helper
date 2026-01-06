import math

import bpy

from .. import model, register_wrap


def clear_IK(context):
    IK_target_bones = []
    IK_target_tip_bones = []
    context.view_layer.objects.active = model.findArmature(context.active_object)
    bpy.ops.object.mode_set(mode="POSE")
    english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
    japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
    japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]
    leg_foot_bones = english + japanese + japanese_L_R
    for b in context.active_object.pose.bones.keys():
        if b in leg_foot_bones:
            for c in context.active_object.pose.bones[b].constraints:
                if c.type == "IK":
                    print("c.target = ", c.target)
                    if c.target == context.view_layer.objects.active:
                        if c.subtarget is not None:
                            print("c.subtarget = ", c.subtarget)
                            if c.subtarget not in IK_target_bones:
                                IK_target_bones.append(c.subtarget)
    for b in IK_target_bones:
        for c in context.active_object.pose.bones[b].children:
            if c.name not in IK_target_tip_bones:
                IK_target_tip_bones.append(c.name)
    bones_to_be_deleted = set(IK_target_bones + IK_target_tip_bones)
    print("bones to be deleted = ", bones_to_be_deleted)
    bpy.ops.object.mode_set(mode="EDIT")
    for b in bones_to_be_deleted:
        context.active_object.data.edit_bones.remove(context.active_object.data.edit_bones[b])
    bpy.ops.object.mode_set(mode="POSE")
    for b in context.active_object.pose.bones.keys():
        if b in leg_foot_bones:
            for c in context.active_object.pose.bones[b].constraints:
                context.active_object.pose.bones[b].constraints.remove(c)
                # if c.type == "IK":
                # context.active_object.pose.bones[b].constraints.remove(c)
                # if c.type == "LIMIT_ROTATION":
                # context.active_object.pose.bones[b].constraints.remove(c)

    bpy.ops.object.mode_set(mode="OBJECT")


def main(context):
    context.view_layer.objects.active = model.findArmature(context.active_object)

    # test japanese or english ("leg_R", "右足"), ("leg_L", "左足"),
    english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
    japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
    japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]

    keys = context.active_object.data.bones.keys()

    english_bones = all([e in keys for e in english])
    japanese_bones = all([j in keys for j in japanese])
    japanese_bones_L_R = all([j in keys for j in japanese_L_R])

    print("english_bones =", english_bones)
    print("japanese_bones =", japanese_bones)
    print("japanese_bones_L_R =", japanese_bones_L_R)
    print("\n\n")

    assert english_bones or japanese_bones or japanese_bones_L_R, "This is not an MMD armature. MMD bone names of knee, ankle and toe bones are required for this script to run."

    IK_BONE_NAMES = [
        "leg IK_L",
        "leg IK_R",
        "toe IK_L",
        "toe IK_R",
        "左足ＩＫ",
        "右足ＩＫ",
        "左つま先ＩＫ",
        "右つま先ＩＫ",
        "足ＩＫ.L",
        "足ＩＫ.R",
        "つま先ＩＫ.L",
        "つま先ＩＫ.R",
    ]
    ik_bones = any([ik in keys for ik in IK_BONE_NAMES])

    assert not ik_bones, "This armature already has MMD IK bone names."

    if english_bones:
        LEG_IK_LEFT_BONE = "leg IK_L"
        LEG_IK_RIGHT_BONE = "leg IK_R"
        TOE_IK_LEFT_BONE = "toe IK_L"
        TOE_IK_RIGHT_BONE = "toe IK_R"
        LEG_IK_LEFT_BONE_TIP = "leg IK_L_t"
        LEG_IK_RIGHT_BONE_TIP = "leg IK_R_t"
        TOE_IK_LEFT_BONE_TIP = "toe IK_L_t"
        TOE_IK_RIGHT_BONE_TIP = "toe IK_R_t"
        ROOT = "root"

    if japanese_bones or japanese_bones_L_R:
        LEG_IK_LEFT_BONE = "左足ＩＫ"
        LEG_IK_RIGHT_BONE = "右足ＩＫ"
        TOE_IK_LEFT_BONE = "左つま先ＩＫ"
        TOE_IK_RIGHT_BONE = "右つま先ＩＫ"
        LEG_IK_LEFT_BONE_TIP = "左足ＩＫ先"
        LEG_IK_RIGHT_BONE_TIP = "右足ＩＫ先"
        TOE_IK_LEFT_BONE_TIP = "左つま先ＩＫ先"
        TOE_IK_RIGHT_BONE_TIP = "右つま先ＩＫ先"
        ROOT = "全ての親"

        # Lists of possible names of knee, ankle and toe bones
    KNEE_LEFT_BONES = ["knee_L", "左ひざ", "ひざ.L"]
    KNEE_RIGHT_BONES = ["knee_R", "右ひざ", "ひざ.R"]
    ANKLE_LEFT_BONES = ["ankle_L", "左足首", "足首.L"]
    ANKLE_RIGHT_BONES = ["ankle_R", "右足首", "足首.R"]
    TOE_LEFT_BONES = ["toe_L", "左つま先", "つま先.L"]
    TOE_RIGHT_BONES = ["toe_R", "右つま先", "つま先.R"]

    print("\n")
    # Searches through the bones of the active armature and finds the knee, ankle and toe bones.
    for b in context.active_object.data.bones:
        if b.name in KNEE_LEFT_BONES:
            KNEE_LEFT = b.name
            print("KNEE_LEFT = ", KNEE_LEFT)
        if b.name in KNEE_RIGHT_BONES:
            KNEE_RIGHT = b.name
            print("KNEE_RIGHT = ", KNEE_RIGHT)
        if b.name in ANKLE_LEFT_BONES:
            ANKLE_LEFT = b.name
            print("ANKLE_LEFT = ", ANKLE_LEFT)
        if b.name in ANKLE_RIGHT_BONES:
            ANKLE_RIGHT = b.name
            print("ANKLE_RIGHT = ", ANKLE_RIGHT)
        if b.name in TOE_LEFT_BONES:
            TOE_LEFT = b.name
            print("TOE_LEFT = ", TOE_LEFT)
        if b.name in TOE_RIGHT_BONES:
            TOE_RIGHT = b.name
            print("TOE_RIGHT = ", TOE_RIGHT)

    bpy.ops.object.mode_set(mode="POSE")
    context.active_object.pose.bones[KNEE_LEFT].use_ik_limit_x = True
    context.active_object.pose.bones[KNEE_RIGHT].use_ik_limit_x = True

    # measurements of the length of the foot bone which will used to calculate the lengths of the IK bones.
    LENGTH_OF_FOOT_BONE = context.active_object.data.bones[ANKLE_LEFT].length
    HALF_LENGTH_OF_FOOT_BONE = context.active_object.data.bones[ANKLE_LEFT].length * 0.5
    TWENTIETH_LENGTH_OF_FOOT_BONE = context.active_object.data.bones[ANKLE_LEFT].length * 0.05

    bpy.ops.object.mode_set(mode="EDIT")

    # The IK bones are created
    bone = context.active_object.data.edit_bones.new(LEG_IK_LEFT_BONE)
    bone.head = context.active_object.data.edit_bones[ANKLE_LEFT].head
    bone.tail = context.active_object.data.edit_bones[ANKLE_LEFT].head
    bone.tail.y = context.active_object.data.edit_bones[ANKLE_LEFT].head.y + LENGTH_OF_FOOT_BONE
    if ROOT in context.active_object.data.edit_bones.keys():
        print(ROOT, ROOT in context.active_object.data.edit_bones.keys())
        bone.parent = context.active_object.data.edit_bones[ROOT]
        print(bone, bone.parent)

    bone = context.active_object.data.edit_bones.new(LEG_IK_RIGHT_BONE)
    bone.head = context.active_object.data.edit_bones[ANKLE_RIGHT].head
    bone.tail = context.active_object.data.edit_bones[ANKLE_RIGHT].head
    bone.tail.y = context.active_object.data.edit_bones[ANKLE_RIGHT].head.y + LENGTH_OF_FOOT_BONE
    if ROOT in context.active_object.data.edit_bones.keys():
        print(ROOT, ROOT in context.active_object.data.edit_bones.keys())
        bone.parent = context.active_object.data.edit_bones[ROOT]
        print(bone, bone.parent)

    bone = context.active_object.data.edit_bones.new(TOE_IK_LEFT_BONE)
    bone.head = context.active_object.data.edit_bones[TOE_LEFT].head
    bone.tail = context.active_object.data.edit_bones[TOE_LEFT].head
    bone.tail.z = context.active_object.data.edit_bones[TOE_LEFT].head.z - HALF_LENGTH_OF_FOOT_BONE
    print("bone = ", bone)
    bone.parent = context.active_object.data.edit_bones[LEG_IK_LEFT_BONE]
    bone.use_connect = False

    bone = context.active_object.data.edit_bones.new(TOE_IK_RIGHT_BONE)
    bone.head = context.active_object.data.edit_bones[TOE_RIGHT].head
    bone.tail = context.active_object.data.edit_bones[TOE_RIGHT].head
    bone.tail.z = context.active_object.data.edit_bones[TOE_RIGHT].head.z - HALF_LENGTH_OF_FOOT_BONE
    bone.parent = context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE]
    bone.use_connect = False

    bone = context.active_object.data.edit_bones.new(LEG_IK_LEFT_BONE_TIP)
    bone.head = context.active_object.data.edit_bones[LEG_IK_LEFT_BONE].head
    bone.tail = context.active_object.data.edit_bones[LEG_IK_LEFT_BONE].head
    bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_FOOT_BONE
    bone.parent = context.active_object.data.edit_bones[LEG_IK_LEFT_BONE]
    bone.use_connect = False
    bpy.ops.object.mode_set(mode="POSE")
    # if "leg IK_L_t" in context.active_object.pose.bones.keys():
    context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].bone.hide = True
    if hasattr(context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP], "mmd_bone"):
        context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].mmd_bone.is_visible = False
        context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].mmd_bone.is_controllable = False
        context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].mmd_bone.is_tip = True
    bpy.ops.object.mode_set(mode="EDIT")

    bone = context.active_object.data.edit_bones.new(LEG_IK_RIGHT_BONE_TIP)
    bone.head = context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE].head
    bone.tail = context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE].head
    bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_FOOT_BONE
    bone.parent = context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE]
    bone.use_connect = False
    bpy.ops.object.mode_set(mode="POSE")
    # if "leg IK_R_t" in context.active_object.pose.bones.keys():
    context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].bone.hide = True
    if hasattr(context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP], "mmd_bone"):
        context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].mmd_bone.is_visible = False
        context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].mmd_bone.is_controllable = False
        context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].mmd_bone.is_tip = True
    bpy.ops.object.mode_set(mode="EDIT")

    bone = context.active_object.data.edit_bones.new(TOE_IK_LEFT_BONE_TIP)
    bone.head = context.active_object.data.edit_bones[TOE_IK_LEFT_BONE].head
    bone.tail = context.active_object.data.edit_bones[TOE_IK_LEFT_BONE].head
    bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_FOOT_BONE
    bone.parent = context.active_object.data.edit_bones[TOE_IK_LEFT_BONE]
    bone.use_connect = False
    bpy.ops.object.mode_set(mode="POSE")
    # if "toe IK_L_t" in context.active_object.pose.bones.keys():
    context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].bone.hide = True
    if hasattr(context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP], "mmd_bone"):
        context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].mmd_bone.is_visible = False
        context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].mmd_bone.is_controllable = False
        context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].mmd_bone.is_tip = True
    bpy.ops.object.mode_set(mode="EDIT")

    bone = context.active_object.data.edit_bones.new(TOE_IK_RIGHT_BONE_TIP)
    bone.head = context.active_object.data.edit_bones[TOE_IK_RIGHT_BONE].head
    bone.tail = context.active_object.data.edit_bones[TOE_IK_RIGHT_BONE].head
    bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_FOOT_BONE
    bone.parent = context.active_object.data.edit_bones[TOE_IK_RIGHT_BONE]
    bone.use_connect = False
    bpy.ops.object.mode_set(mode="POSE")
    # if "toe IK_R_t" in context.active_object.pose.bones.keys():
    context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].bone.hide = True
    if hasattr(context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP], "mmd_bone"):
        context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].mmd_bone.is_visible = False
        context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].mmd_bone.is_controllable = False
        context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].mmd_bone.is_tip = True
    bpy.ops.object.mode_set(mode="EDIT")

    bpy.ops.object.mode_set(mode="POSE")

    # Adds IK constraints
    context.object.pose.bones[KNEE_LEFT].constraints.new("IK")
    context.object.pose.bones[KNEE_LEFT].constraints["IK"].target = context.active_object
    context.object.pose.bones[KNEE_LEFT].constraints["IK"].subtarget = LEG_IK_LEFT_BONE
    context.object.pose.bones[KNEE_LEFT].constraints["IK"].chain_count = 2
    context.object.pose.bones[KNEE_LEFT].constraints["IK"].use_tail = True
    context.object.pose.bones[KNEE_LEFT].constraints["IK"].iterations = 48

    context.object.pose.bones[KNEE_LEFT].constraints.new("LIMIT_ROTATION")
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_x = True
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_y = True
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_z = True
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_x = math.pi / 360  # radians = 0.5 degrees
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_x = math.pi  # radians = 180 degrees

    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_y = 0
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_y = 0
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_z = 0
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_z = 0

    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].owner_space = "POSE"
    context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

    context.object.pose.bones[KNEE_RIGHT].constraints.new("IK")
    context.object.pose.bones[KNEE_RIGHT].constraints["IK"].target = context.active_object
    context.object.pose.bones[KNEE_RIGHT].constraints["IK"].subtarget = LEG_IK_RIGHT_BONE
    context.object.pose.bones[KNEE_RIGHT].constraints["IK"].chain_count = 2
    context.object.pose.bones[KNEE_RIGHT].constraints["IK"].use_tail = True
    context.object.pose.bones[KNEE_RIGHT].constraints["IK"].iterations = 48

    context.object.pose.bones[KNEE_RIGHT].constraints.new("LIMIT_ROTATION")
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_x = True
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_y = True
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_z = True
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_x = math.pi / 360  # radians = 0.5 degrees
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_x = math.pi  # radians = 180 degrees

    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_y = 0
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_y = 0
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_z = 0
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_z = 0

    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].owner_space = "POSE"
    context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

    # context.object.pose.bones[ANKLE_LEFT].constraints.new("DAMPED_TRACK")
    # context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].target = context.active_object
    # context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].subtarget = KNEE_LEFT
    # context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].track_axis = 'TRACK_Y'
    # context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].name = "mmd_ik_target_override"

    context.object.pose.bones[ANKLE_LEFT].constraints.new("IK")
    context.object.pose.bones[ANKLE_LEFT].constraints["IK"].target = context.active_object
    context.object.pose.bones[ANKLE_LEFT].constraints["IK"].subtarget = TOE_IK_LEFT_BONE
    context.object.pose.bones[ANKLE_LEFT].constraints["IK"].chain_count = 1
    context.object.pose.bones[ANKLE_LEFT].constraints["IK"].use_tail = True
    context.object.pose.bones[ANKLE_LEFT].constraints["IK"].iterations = 6

    # context.object.pose.bones[ANKLE_RIGHT].constraints.new("DAMPED_TRACK")
    # context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].target = context.active_object
    # context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].subtarget = KNEE_LEFT
    # context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].track_axis = 'TRACK_Y'
    # context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].name = "mmd_ik_target_override"

    context.object.pose.bones[ANKLE_RIGHT].constraints.new("IK")
    context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].target = context.active_object
    context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].subtarget = TOE_IK_RIGHT_BONE
    context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].chain_count = 1
    context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].use_tail = True
    context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].iterations = 6

    if hasattr(context.object.pose.bones[KNEE_RIGHT], "mmd_bone"):
        context.object.pose.bones[KNEE_RIGHT].mmd_bone.ik_rotation_constraint = 2  # 180*2/math.pi
        context.object.pose.bones[KNEE_LEFT].mmd_bone.ik_rotation_constraint = 2  # 180*2/math.pi
        context.object.pose.bones[ANKLE_RIGHT].mmd_bone.ik_rotation_constraint = 4  # 180*4/math.pi
        context.object.pose.bones[ANKLE_LEFT].mmd_bone.ik_rotation_constraint = 4  # 180*4/math.pi

    # create an 'IK' bone collection and add the IK bones to it
    if "IK" not in context.active_object.data.collections.keys():
        context.active_object.data.collections.new(name="IK")

    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[LEG_IK_LEFT_BONE])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[LEG_IK_RIGHT_BONE])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[TOE_IK_LEFT_BONE])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[TOE_IK_RIGHT_BONE])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP])
    context.active_object.data.collections["IK"].assign(context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP])


@register_wrap
class AddMMDLegIK(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.add_leg_ik"
    bl_label = "Add leg IK to MMD model"
    bl_description = "Add foot and leg IK bones and constraints to active MMD model"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.mode not in {"OBJECT", "POSE"}:
            return False

        active_object = context.active_object

        if active_object is None:
            return False

        return model.findRoot(active_object) is not None

    def execute(self, context):
        previous_mode = context.mode

        try:
            clear_IK(context)
            main(context)
            self.report({"INFO"}, message="Successfully added leg IK")
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to add leg IK: {e}")
            return {"CANCELLED"}
        finally:
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
