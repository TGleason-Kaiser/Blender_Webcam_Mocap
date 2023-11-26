import streamlit as st
import cv2
import subprocess

video_data = st.file_uploader("Upload file", ['mp4','mov', 'avi'])

temp_file_to_save = './temp_file_1.mp4'
temp_file_result  = './temp_file_2.mp4'

# func to save BytesIO on a drive
def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

if video_data:
    # save uploaded video to disc
    write_bytesio_to_file(temp_file_to_save, video_data)

    # read it with cv2.VideoCapture(), 
    # so now we can process it with OpenCV functions
    cap = cv2.VideoCapture(temp_file_to_save)

    # grab some parameters of video to use them for writing a new, processed video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = cap.get(cv2.CAP_PROP_FPS)  ##<< No need for an int
    st.write(width, height, frame_fps)
    
    # specify a writer to write a processed video to a disk frame by frame
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    out_mp4 = cv2.VideoWriter(temp_file_result, fourcc_mp4, frame_fps, (width, height),isColor = False)
   
    while True:
        ret,frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ##<< Generates a grayscale (thus only one 2d-array)
        out_mp4.write(gray)
    
    ## Close video files
    out_mp4.release()
    cap.release()

    ## Reencodes video to H264 using ffmpeg
    ##  It calls ffmpeg back in a terminal so it fill fail without ffmpeg installed
    ##  ... and will probably fail in streamlit cloud
    convertedVideo = "./testh264.mp4"
    subprocess.call(args=f"ffmpeg -y -i {temp_file_result} -c:v libx264 {convertedVideo}".split(" "))
    
    ## Show results
    col1,col2 = st.columns(2)
    col1.header("Original Video")
    col1.video(temp_file_to_save)
    col2.header("Output from OpenCV (MPEG-4)")
    col2.video(temp_file_result)
    col2.header("After conversion to H264")
    col2.video(convertedVideo)

'''
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def save_uploadedfile(uploadedFile):
    with open(os.path.join("webui",uploadedFile.name),"wb") as f:
        f.write(uploadedFile.getbuffer())
    return st.success("Saved File: " + uploadedFile.name + " to webui folder")

def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

def analyzeVideo(uploadedFile):
    filename = uploadedFile.name
    saveFilename = os.path.join("webui",uploadedFile.name[0:len(uploadedFile.name)-4] + "_result.mp4")

    cap = cv2.VideoCapture(filename)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = cap.get(cv2.CAP_PROP_FPS)  ##<< No need for an int
    
    # specify a writer to write a processed video to a disk frame by frame
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'MP4V')
    out_mp4 = cv2.VideoWriter(saveFilename, fourcc_mp4, frame_fps, (width, height),isColor = True)

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Save annotated file
            out_mp4.write(image)
    out_mp4.release()
    cap.release()

    #convertedVideo = 'webui\h264Test.mp4'
    #subprocess.call(args=f"ffmpeg -y -i {saveFilename} -c:v libx264 {convertedVideo}".split(" "))

st.set_page_config(page_title="Pose Detection", layout="wide")

st.subheader("Upload Image or Video for Pose Detection")

uploaded_files = st.file_uploader("Choose an mp4 file", accept_multiple_files=True, type=['mp4'])

if(uploaded_files is not None):
    for uploaded_file in uploaded_files:
        if(uploaded_file.type[0:3] == "vid"):
            video_bytes = uploaded_file.read()
            st.video(video_bytes)
            write_bytesio_to_file(os.path.join("webui", uploaded_file.name), uploaded_file)
            analyzeVideo(uploaded_file)

            result_video = open(temp_file_result, "rb")
            st.video(result_video)
        else:
            image_bytes = uploaded_file.read()
            st.image(image_bytes)
        #save_uploadedfile(uploaded_file)
'''