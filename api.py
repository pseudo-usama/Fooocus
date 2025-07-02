import os
import sys
import time
import random

# Prevent Fooocus from launching the webui
os.environ['DONT_LAUNCH_WEBUI'] = 'True'

# Add the Fooocus directory to the path
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)

# Import necessary modules from Fooocus
import modules.async_worker as worker
import ldm_patched.modules.model_management as model_management


def call_fooocus(args):
    """Generate images using Fooocus"""
    def generate_clicked(task: worker.AsyncTask):
        with model_management.interrupt_processing_mutex:
            model_management.interrupt_processing = False

        if len(task.args) == 0:
            return

        finished = False
        worker.async_tasks.append(task)

        while not finished:
            time.sleep(0.01)
            if len(task.yields) > 0:
                flag, product = task.yields.pop(0)
                if flag == 'finish':
                    finished = True
                    return product

    currentTask = worker.AsyncTask(args=args)
    imgs_paths = generate_clicked(currentTask)
    
    return imgs_paths


def generate_img(
    prompt,
    negative_prompt="",
    style_names=["Fooocus V2"],
    performance="Speed",
    aspect_ratio="1152×896",
    num_images=1,
    seed=-1,
    output_dir=None
):
    if seed == -1:
        seed = random.randint(0, 2**32 - 1)
    
    # Default args template
    args = [False, prompt, negative_prompt, style_names, performance, '1152×896 <span style="color: grey;"> ∣ 9:7</span>', num_images, 'png', str(seed), False, 2, 4, 'juggernautXL_v8Rundiffusion.safetensors', 'None', 0.5, True, 'sd_xl_offset_example-lora_1.0.safetensors', 0.1, True, 'None', 1, True, 'None', 1, True, 'None', 1, True, 'None', 1, False, 'uov', 'Disabled', None, [], None, '', None, False, False, False, False, 1.5, 0.8, 0.3, 7, 2, 'dpmpp_2m_sde_gpu', 'karras', 'Default (model)', -1, -1, -1, -1, -1, -1, False, False, False, False, 64, 128, 'joint', 0.25, False, 1.01, 1.02, 0.99, 0.95, False, False, 'v2.6', 1, 0.618, False, False, 0, False, False, 'fooocus', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', False, 0, False, None, False, 'Disabled', 'Before First Enhancement', 'Original Prompts', False, '', '', '', 'sam', 'full', 'vit_b', 0.25, 0.3, 0, False, 'v2.6', 1, 0.618, 0, False, False, '', '', '', 'sam', 'full', 'vit_b', 0.25, 0.3, 0, False, 'v2.6', 1, 0.618, 0, False, False, '', '', '', 'sam', 'full', 'vit_b', 0.25, 0.3, 0, False, 'v2.6', 1, 0.618, 0, False]

    # Generate the images
    return call_fooocus(args)


if __name__ == "__main__":
    images = generate_img(
        prompt="a gril",
        negative_prompt="ugly, blurry, low quality",
        style_names=["Fooocus V2", "Fooocus Enhance"],
        performance="Quality",
        aspect_ratio="1024×1024",
    )
    
    print(f"Generated images: {images}")
