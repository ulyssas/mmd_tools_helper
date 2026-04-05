"""Module for finding MMD model components in Blender objects."""

import bpy


def findRoot(obj: bpy.types.Object) -> bpy.types.Object:
    if obj is not None:
        if obj.mmd_type == "ROOT":
            return obj
        else:
            return findRoot(obj.parent)
    else:
        return None


def findCamera(obj: bpy.types.Object) -> bpy.types.Object:
    if obj is not None:
        if obj.mmd_type == "CAMERA":
            return obj
        else:
            return findCamera(obj.parent)
    else:
        return None


def armature(root: bpy.types.Object) -> bpy.types.Object:
    armatures = []
    for c in root.children:
        if c.type == "ARMATURE":
            c.hide = False
            armatures.append(c)
    if len(armatures) == 1:
        return armatures[0]
    if len(armatures) == 0:
        return None
    if len(armatures) > 1:
        print("Error. More than 1 armature found", armatures)


def __allObjects(obj: bpy.types.Object) -> list[bpy.types.Object]:
    r = []
    for i in obj.children:
        r.append(i)
        r += __allObjects(i)
    return r


def allObjects(obj: bpy.types.Object, root: bpy.types.Object) -> list[bpy.types.Object]:
    if obj is None:
        obj = root
    return [obj] + __allObjects(obj)


def meshes(root: bpy.types.Object) -> list[bpy.types.Object]:
    arm = armature(root)
    if arm is None:
        return []
    else:
        return list(
            filter(lambda x: x.type == "MESH" and x.mmd_type == "NONE", allObjects(arm, root))
        )


def find_MMD_Armature(obj: bpy.types.Object) -> bpy.types.Object:
    root = findRoot(obj)
    if root is None:
        print("No MMD model is selected")
    else:
        return armature(root)


def findArmature(obj: bpy.types.Object) -> bpy.types.Object:
    if obj.type == "ARMATURE":
        obj.hide = False
        return obj
    if obj.parent is not None and obj.parent.type == "ARMATURE":
        obj.parent.hide = False
        return obj.parent
    if hasattr(obj, "mmd_type") and obj.mmd_type == "ROOT":
        return armature(obj)
    if obj.type == "EMPTY":
        return armature(obj)


def find_MMD_MeshesList(obj: bpy.types.Object) -> list[bpy.types.Object]:
    root = findRoot(obj)
    if root is None:
        print("No MMD model is selected")
    else:
        return meshes(root)


def findMeshesList(obj: bpy.types.Object) -> list[bpy.types.Object]:
    mesheslist = []
    if obj.type == "ARMATURE":
        for c in obj.children:
            if c.type == "MESH":
                mesheslist.append(c)
        return mesheslist
    if obj.type == "MESH":
        if obj.parent is not None and obj.parent.type == "ARMATURE":
            for c in obj.parent.children:
                if c.type == "MESH":
                    mesheslist.append(c)
            return mesheslist
        if obj.parent is None or obj.parent.type != "ARMATURE":
            return [obj]
    if hasattr(obj, "mmd_type") and obj.mmd_type == "ROOT":
        return meshes(obj)
    if obj.type == "EMPTY":
        return meshes(obj)


def find_mmd_rigid_bodies_list(root: bpy.types.Object):
    for c in root.children:
        if c.type == "EMPTY" and c.name == "rigidbodies":
            rigidbodies = c
    return list(rigidbodies.children)


def find_mmd_joints_list(root: bpy.types.Object):
    for c in root.children:
        if c.type == "EMPTY" and c.name == "joints":
            joints = c
    return list(joints.children)


def test():
    if hasattr(bpy.context, "active_object"):
        if bpy.context.active_object is not None:
            print("Active Object Type = ", bpy.context.active_object.type)
            Root = findRoot(bpy.context.active_object)
            print("root = ", Root)
            Meshes = find_MMD_MeshesList(bpy.context.active_object)
            print("mmd_meshes = ", Meshes)
            Armature = find_MMD_Armature(bpy.context.active_object)
            print("mmd_armature = ", Armature, "\n")
            Meshes = findMeshesList(bpy.context.active_object)
            print("meshes = ", Meshes)
            Armature = findArmature(bpy.context.active_object)
            print("armature = ", Armature)
            print("\n")
            Rigid_Bodies = find_mmd_rigid_bodies_list(Root)
            print("rigid bodies = ", Rigid_Bodies)
            print("\n")
            Joints = find_mmd_joints_list(Root)
            print("joints = ", Joints)
            print("\n")
            print()


# test()
