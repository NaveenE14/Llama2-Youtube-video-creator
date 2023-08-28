import streamlit as st
from clarifai_utils.modules.css import ClarifaiStreamlitCSS

st.set_page_config(page_title="LLAMA 2 Video Creator", layout="wide")

ClarifaiStreamlitCSS.insert_default_css(st)

from dotenv import load_dotenv

load_dotenv()
import os

clarifai_pat = os.getenv('CLARIFAI_PAT')

PAT = clarifai_pat
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'meta'
APP_ID = 'Llama-2'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'llama2-70b-chat'
MODEL_VERSION_ID = '6c27e86364ba461d98de95cddc559cb3'


# Set page title
import streamlit as st

# Set page title


# Main Title
st.title("🎥LLamaScriptAI: Revolutionize Video Creation with AI Magic 🦙🎥")

# Description
st.markdown("""
Create captivating videos effortlessly with the YouTube Video Creator powered by LLAMA 2! ✨
🌟 **About LLamaScriptAI:**
Step into a realm of boundless creativity with LLamaScriptAI, your all-inclusive AI video generation platform. Imagine the power of crafting captivating videos with just one prompt. Scripting, imagery, and narration converge seamlessly to bring your visions to life.

📜 **Scripting Beyond Imagination:**
Witness the transformation as LLamaScriptAI's AI models convert your prompts into immersive scripts. Watch your ideas unfold into captivating narratives that resonate with your audience.

🖼️ **Image Prompts & Stable Diffusion XL:**
LLAMA 2 generates image prompts which are then processed by the powerful Stable Diffusion XL model. This collaboration results in captivating and lifelike images that seamlessly align with your content.

🗣️ **Narration with gTTS:**
For natural and expressive narration, we use Google Text-to-Speech (gTTS). Your scripts come to life with lifelike audio.

🎉 **Features:**
- AI-generated scripts and image prompts
- High-quality images from Stable Diffusion XL
- Natural voiceover using Google Text-to-Speech
- One-click video creation

🎭 **Create Stories of Any Genre:**
Craft stories of any genre you need, from drama to comedy, fantasy to documentary. LLamaScriptAI adapts to your creative vision, allowing you to explore limitless storytelling possibilities.

🚀 **AI Video Generation: Unveiling the Future:**
LLamaScriptAI introduces a paradigm shift in video creation. Harness the power of AI to create full videos from a single prompt. With LLamaScriptAI, your ideas are transformed into complete videos with just a single input.

🌟 **About LLAMA 2:**
LLAMA 2 is a cutting-edge large language model that empowers you to create stunning videos from scratch. It handles everything from generating scripts to crafting mesmerizing image prompts.

🎬 **Output:**
LLAMA 2 delivers your masterpiece as a full video, combining its AI-generated script content, mesmerizing images from Stable Diffusion XL, and natural narration.

Experience the future of video creation with YouTube Video Creator powered by LLAMA 2! 🚀

""")


storyname = st.text_input("Create a video about")

if (st.button("SUBMIT")):
    prompt = """
    Generate a full compelling video story script for youtube video about """ + storyname + """You choose video tone ,names and everthing in the video . For each sentence in the story, provide a related visual image scene description to enhance the storytelling. Remember to format the output as follows: Image Prompt: [Insert image description or scene here] Narrator: [Write the narration or dialogue for the sentence] Image Prompt: [Insert image description or scene here] Narrator: [Write the narration or dialogue for the sentence] and so on untill the end of the story"""

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    st.write("Completion:\n")
    st.write(output.data.text.raw)
    prompt_text = output.data.text.raw
    splitted_prompts = prompt_text.split('Image Prompt: ')
    print(splitted_prompts)
    image_prompt = []
    narrator_prompt = []
    for iter in splitted_prompts:
        values = iter.split('Narrator:')
        image_prompt_current = ((values[0]).split('.\\n\\n')[0])
        import requests

        response = requests.post("https://microsoft-promptist.hf.space/run/predict", json={
            "data": [
                image_prompt_current,
            ]}).json()

        image_prompt.append(response["data"][0])
        st.write(response['data'][0])
        try:
            narrator_prompt_text = (values[1]).split('.\\n\\n')
            narrator_prompt.append(narrator_prompt_text[0])
        except:
            pass
    st.title("IMAGES : ")
    for iter in image_prompt:
        st.write(iter)
    st.title("NARRATOR")
    for iter in narrator_prompt:
        st.write(iter)

    from gtts import gTTS

    count = 0

    for idx, para in enumerate(narrator_prompt):
        tts = gTTS(text=para, lang='en', slow=False)
        audio_filename = f"voiceover{idx}.mp3"  # Use index for unique filenames
        tts.save(audio_filename)
        print(f"Generated audio for prompt {idx}")
        count = count + 1

    USER_ID = 'stability-ai'
    APP_ID = 'stable-diffusion-2'
    MODEL_ID = 'stable-diffusion-xl'
    MODEL_VERSION_ID = '0c919cc1edfc455dbc96207753f178d7'
    TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    print("Created text to speech succesfully")
    for concept in output.data.concepts:
        print("%s %.2f" % (concept.name, concept.value))
    for idx, iter in enumerate(image_prompt):
        image_generate_prompt = iter
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=image_generate_prompt
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        print(f"Created {idx} stable diffusion image")
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))

        base64_image = output.data.image.base64
        image_filename = f"Clarifai_image_{idx}.jpg"  # Use index for unique filenames
        with open(image_filename, 'wb') as f:
            f.write(base64_image)

    from moviepy.editor import ImageClip, concatenate_videoclips
    from moviepy.audio.io.AudioFileClip import AudioFileClip

    # Replace these values with your actual counts and paths
    # Replace with the desired count
    output_video_filename = "output_video.mp4"

    image_filenames = [f"Clarifai_image_{idx}.jpg" for idx in range(count)]
    audio_filenames = [f"voiceover{idx}.mp3" for idx in range(count)]

    # Create audio clips
    audio_clips = [AudioFileClip(audio_filename) for audio_filename in audio_filenames]

    # Create image clips
    image_clips = [ImageClip(image_filename, duration=audio_clip.duration)
                   for image_filename, audio_clip in zip(image_filenames, audio_clips)]

    # Combine image and audio clips
    final_clips = [image_clip.set_audio(audio_clip)
                   for image_clip, audio_clip in zip(image_clips, audio_clips)]

    # Concatenate the clips to create the final video
    video = concatenate_videoclips(final_clips, method="compose")

    # Save the final video
    video.write_videofile(output_video_filename, codec='libx264', threads=4, audio_codec='aac',
                          fps=24)  # Adjust the frame rate as needed
    st.video("output_video.mp4")
    print("Video creation completed!")
