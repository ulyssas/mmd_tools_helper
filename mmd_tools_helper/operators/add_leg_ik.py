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
    def add_ik_limit(pbone: bpy.types.PoseBone):
        pbone.use_ik_limit_x = True
        pbone.use_ik_limit_y = True
        pbone.use_ik_limit_z = True
        pbone.ik_min_x = 0
        pbone.ik_max_x = math.pi
        pbone.ik_min_y = 0
        pbone.ik_max_y = 0
        pbone.ik_min_z = 0
        pbone.ik_max_z = 0

    def add_ik_constraint(
        pbone: bpy.types.PoseBone,
        subtarget: str,
        chain_count: int,
        iterations: int,
    ):
        constraint = pbone.constraints.new("IK")
        constraint.target = raw_object
        constraint.subtarget = subtarget
        constraint.chain_count = chain_count
        constraint.iterations = iterations

    def add_limit_rot(pbone: bpy.types.PoseBone):
        constraint = pbone.constraints.new("LIMIT_ROTATION")
        constraint.name = "mmd_ik_limit_override"
        constraint.use_limit_x = True
        constraint.use_limit_y = False
        constraint.use_limit_z = False
        constraint.min_x = math.pi / 360  # radians=0.5 degrees
        constraint.max_x = math.pi  # radians=180 degrees
        constraint.min_y = 0
        constraint.max_y = 0
        constraint.min_z = 0
        constraint.max_z = 0
        constraint.owner_space = "LOCAL"

    def create_ik_bone(name: str, target: str, parent: str) -> bpy.types.EditBone:
        bone = raw_armature.edit_bones.new(name)
        bone.head = raw_armature.edit_bones[target].head
        bone.tail = raw_armature.edit_bones[target].head
        bone.use_deform = False
        if parent in raw_armature.edit_bones.keys():
            print(parent, parent in raw_armature.edit_bones.keys())
            bone.parent = raw_armature.edit_bones[parent]
            print(bone, bone.parent)
        return bone

    context.view_layer.objects.active = model.findArmature(context.active_object)
    raw_object: bpy.types.Object = context.active_object
    raw_armature: bpy.types.Armature = context.active_object.data

    # test japanese or english ("leg_R", "右足"), ("leg_L", "左足"),
    english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
    japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
    japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]

    keys = raw_armature.bones.keys()

    english_bones = all(e in keys for e in english)
    japanese_bones = all(j in keys for j in japanese)
    japanese_bones_L_R = all(j in keys for j in japanese_L_R)

    print("english_bones =", english_bones)
    print("japanese_bones =", japanese_bones)
    print("japanese_bones_L_R =", japanese_bones_L_R)
    print("\n\n")

    assert english_bones or japanese_bones or japanese_bones_L_R, (
        "This is not an MMD armature. MMD bone names of knee, ankle and toe bones are required for this script to run."
    )

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
    ik_bones = any(ik in keys for ik in IK_BONE_NAMES)

    assert not ik_bones, "This armature already has MMD IK bone names."

    if english_bones:
        LEG_IK_L = "leg IK_L"
        LEG_IK_R = "leg IK_R"
        TOE_IK_L = "toe IK_L"
        TOE_IK_R = "toe IK_R"
        ROOT = "root"

    if japanese_bones or japanese_bones_L_R:
        LEG_IK_L = "左足ＩＫ"
        LEG_IK_R = "右足ＩＫ"
        TOE_IK_L = "左つま先ＩＫ"
        TOE_IK_R = "右つま先ＩＫ"
        ROOT = "全ての親"

        # Lists of possible names of knee, ankle and toe bones
    KNEE_L_LIST = ["knee_L", "左ひざ", "ひざ.L"]
    KNEE_R_LIST = ["knee_R", "右ひざ", "ひざ.R"]
    ANKLE_L_LIST = ["ankle_L", "左足首", "足首.L"]
    ANKLE_R_LIST = ["ankle_R", "右足首", "足首.R"]
    TOE_L_LIST = ["toe_L", "左つま先", "つま先.L"]
    TOE_R_LIST = ["toe_R", "右つま先", "つま先.R"]

    print("\n")
    # Searches through the bones of the active armature and finds the knee, ankle and toe bones.
    for b in raw_armature.bones:
        if b.name in KNEE_L_LIST:
            KNEE_L = b.name
            print("KNEE_L = ", KNEE_L)
        if b.name in KNEE_R_LIST:
            KNEE_R = b.name
            print("KNEE_R = ", KNEE_R)
        if b.name in ANKLE_L_LIST:
            ANKLE_L = b.name
            print("ANKLE_L = ", ANKLE_L)
        if b.name in ANKLE_R_LIST:
            ANKLE_R = b.name
            print("ANKLE_R = ", ANKLE_R)
        if b.name in TOE_L_LIST:
            TOE_L = b.name
            print("TOE_L = ", TOE_L)
        if b.name in TOE_R_LIST:
            TOE_R = b.name
            print("TOE_R = ", TOE_R)

    bpy.ops.object.mode_set(mode="POSE")

    add_ik_limit(raw_object.pose.bones[KNEE_L])
    add_ik_limit(raw_object.pose.bones[KNEE_R])

    # measurements of the length of the foot bone which will used to calculate the lengths of the IK bones.
    FOOT_LENGTH = raw_armature.bones[ANKLE_L].length

    bpy.ops.object.mode_set(mode="EDIT")

    # The IK bones are created
    bone = create_ik_bone(LEG_IK_L, ANKLE_L, ROOT)
    bone.tail.y = raw_armature.edit_bones[ANKLE_L].head.y + FOOT_LENGTH

    bone = create_ik_bone(LEG_IK_R, ANKLE_R, ROOT)
    bone.tail.y = raw_armature.edit_bones[ANKLE_R].head.y + FOOT_LENGTH

    bone = create_ik_bone(TOE_IK_L, TOE_L, LEG_IK_L)
    bone.tail.z = raw_armature.edit_bones[TOE_L].head.z - FOOT_LENGTH * 0.5

    bone = create_ik_bone(TOE_IK_R, TOE_R, LEG_IK_R)
    bone.tail.z = raw_armature.edit_bones[TOE_R].head.z - FOOT_LENGTH * 0.5

    bpy.ops.object.mode_set(mode="POSE")

    # Adds IK constraints
    add_ik_constraint(raw_object.pose.bones[KNEE_L], LEG_IK_L, 2, 200)
    add_ik_constraint(raw_object.pose.bones[KNEE_R], LEG_IK_R, 2, 200)
    add_ik_constraint(raw_object.pose.bones[ANKLE_L], TOE_IK_L, 1, 15)
    add_ik_constraint(raw_object.pose.bones[ANKLE_R], TOE_IK_R, 1, 15)

    add_limit_rot(raw_object.pose.bones[KNEE_L])
    add_limit_rot(raw_object.pose.bones[KNEE_R])

    if hasattr(raw_object.pose.bones[KNEE_L], "mmd_bone"):
        raw_object.pose.bones[KNEE_L].mmd_bone.ik_rotation_constraint = 2  # 180*2/math.pi
        raw_object.pose.bones[KNEE_R].mmd_bone.ik_rotation_constraint = 2  # 180*2/math.pi
        raw_object.pose.bones[ANKLE_L].mmd_bone.ik_rotation_constraint = 4  # 180*4/math.pi
        raw_object.pose.bones[ANKLE_R].mmd_bone.ik_rotation_constraint = 4  # 180*4/math.pi

    # create an 'IK' bone collection and add the IK bones to it
    if "IK" not in raw_armature.collections.keys():
        raw_armature.collections.new(name="IK")

    raw_armature.collections["IK"].assign(raw_object.pose.bones[LEG_IK_L])
    raw_armature.collections["IK"].assign(raw_object.pose.bones[LEG_IK_R])
    raw_armature.collections["IK"].assign(raw_object.pose.bones[TOE_IK_L])
    raw_armature.collections["IK"].assign(raw_object.pose.bones[TOE_IK_R])


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
