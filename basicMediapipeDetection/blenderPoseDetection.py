import bpy
import os

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

class OT_ReadPoseData(Operator, ImportHelper):

    bl_idname = "test.open_filebrowser"
    bl_label = "Open Data File"
    
    filter_glob: StringProperty(
        default='*.txt',
        options={'HIDDEN'}
    )

    def execute(self, context):
        bpy.data.scenes[bpy.context.scene.name].frame_set(1)
        
        i = 0
        while i < len(open(self.filepath).readlines()):
            readData(self.filepath)
            bpy.data.scenes[bpy.context.scene.name].frame_set(bpy.data.scenes[bpy.context.scene.name].frame_current + 1)
            i+=1
        bpy.data.scenes[bpy.context.scene.name].frame_end = i

        #readData(self.filepath)
        
        #filename, extension = os.path.splitext(self.filepath)
        #print('Selected file:', self.filepath)
        #print('File name:', filename)
        #print('File extension:', extension)
        
        return {'FINISHED'}

def readData(dataFile : str):
    with open(dataFile, 'r') as file:
        dataArray = file.readlines()
        #print(dataArray[bpy.data.scenes["Scene"].frame_current].rstrip('\n'))
        fullLine = dataArray[bpy.data.scenes[bpy.context.scene.name].frame_current - 1].rstrip('\n')

        landmarkNums = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
        landmarkNames = ['left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
        i = 0
        while i < len(landmarkNums):
            try:
                lineSegment = fullLine[fullLine.find(str(landmarkNums[i]) + ":") + 3:10000]
                xEnd = lineSegment.find(",")
                yEnd = xEnd + lineSegment[xEnd + 1:10000].find(",") + 1
                zEnd = yEnd + lineSegment[yEnd + 1:10000].find("|") + 1
                x = float(lineSegment[0:xEnd])
                y = float(lineSegment[xEnd + 1:yEnd])
                z = float(lineSegment[yEnd + 1:zEnd])
                print("landmark: ", landmarkNames[i], "\nx: ", x, "\ny: ", y, "\nz: ", z)
                
                if bpy.data.scenes[bpy.context.scene.name].frame_current == 1:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.ops.object.empty_add(location=(x,z,-y))
                    empty = bpy.context.object
                    empty.empty_display_size = 0.1
                    empty.name = landmarkNames[i]
                    bpy.data.objects[landmarkNames[i]].select_set(True)
                    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects[landmarkNames[i]].location = (x,z,-y)
                    bpy.data.objects[landmarkNames[i]].select_set(True)
                    bpy.ops.anim.keyframe_insert_by_name(type="Available")

            except Exception as e:
                print("y'all fucked up: ", e)
            i+=1

def register():
    bpy.utils.register_class(OT_ReadPoseData)


def unregister():
    bpy.utils.unregister_class(OT_ReadPoseData)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')

'''
#Set start frame
bpy.data.scenes['Scene'].frame_set(1)

#Create armature and enter edit mode
bpy.ops.object.armature_add(enter_editmode=False)

bonesEdit = bpy.data.objects["Armature"].data.bones
bonesEdit["Bone"].name = "root"

bpy.ops.object.editmode_toggle()

#extrude one bone straight up
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.724229)})

#enter pose mode
bpy.ops.object.posemode_toggle()   

#select all and insert keyframe
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
bpy.ops.pose.select_all(action='DESELECT')

#go to next frame
bpy.data.scenes['Scene'].frame_set(bpy.data.scenes['Scene'].frame_current + 1)

#select one bone and change pose
bones = bpy.data.objects["Armature"].pose.bones
secondBone = bones[1]
#bpy.ops.transform.translate(value=(-1.50728, 0, 0), orient_axis_ortho='X', orient_type='VIEW', orient_matrix=((-1, -0, -0), (-0, 1.34359e-07, 1), (-0, 1, 1.34359e-07)), orient_matrix_type='VIEW', mirror=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

#select all and insert keyframe
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
bpy.ops.pose.select_all(action='DESELECT')

#exit pose mode
bpy.ops.object.posemode_toggle()
'''