from dotenv import load_dotenv
load_dotenv()

import os
import sys
import time
import json
import cv2

os.environ['DONT_LAUNCH_WEBUI'] = 'True'
from launch import *
import modules.async_worker as worker

submodule_path = os.path.join(os.path.dirname(__file__), "prompter")
sys.path.append(submodule_path)
from prompter.plan_photoshoot import get_photoshoot_plan



def readtheimg(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def writetheimg(img, path):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, img)


def generate(args):
    def generate_clicked(task: worker.AsyncTask):
        import ldm_patched.modules.model_management as model_management

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
    imgs = [readtheimg(im) for im in imgs_paths]

    return imgs


def simple_generate(prompt, quality, size, num_of_imgs):
    args = [False, 'a girl', '', ['Fooocus V2', 'Fooocus Enhance', 'Fooocus Sharp'], 'Speed', '1152×896 <span style="color: grey;"> ∣ 9:7</span>', 2, 'png', '8710412579712811529', False, 2, 4, 'juggernautXL_v8Rundiffusion.safetensors', 'None', 0.5, True, 'sd_xl_offset_example-lora_1.0.safetensors', 0.1, True, 'None', 1, True, 'None', 1, True, 'None', 1, True, 'None', 1, False, 'uov', 'Disabled', None, [], None, '', None, False, False, False, False, 1.5, 0.8, 0.3, 7, 2, 'dpmpp_2m_sde_gpu', 'karras', 'Default (model)', -1, -1, -1, -1, -1, -1, False, False, False, False, 64, 128, 'joint', 0.25, False, 1.01, 1.02, 0.99, 0.95, False, False, 'v2.6', 1, 0.618, False, False, 0, False, False, 'fooocus', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', False, 0, False, None, False, 'Disabled', 'Before First Enhancement', 'Original Prompts', False, '', '', '', 'sam', 'full', 'vit_b', 0.25, 0.3, 0, False, 'v2.6', 1, 0.618, 0, False, False, '', '', '', 'sam', 'full', 'vit_b', 0.25, 0.3, 0, False, 'v2.6', 1, 0.618, 0, False, False, '', '', '', 'sam', 'full', 'vit_b', 0.25, 0.3, 0, False, 'v2.6', 1, 0.618, 0, False]

    if size == [1080, 1350]:
        size = '1080×1350 <span style="color: grey;"> ∣ 4:5</span>'
    elif size == [1024, 1024]:
        size = '1024×1024 <span style="color: grey;"> ∣ 1:1</span>'
    elif size == [1080, 566]:
        size = '1080×566 <span style="color: grey;"> ∣ 1.91:1</span>'
    else:
        raise ValueError(f'Unsupported image size "{size}"')

    args[1] = prompt
    args[4] = quality
    args[5] = size
    args[6] = num_of_imgs

    imgs = generate(args)
    return imgs


def generate_in_batch(photoshoot_plans, parent_dir="batch_generation", test=False):
    for i, plan in enumerate(photoshoot_plans, start=1):
        quality = 'Speed' if test else 'Quality'
        size = plan["aspect_ratio"]
        n = 5 if test else 10
        dir_path = f"{parent_dir}/{i}. {plan['theme']}"

        try:
            os.makedirs(dir_path)
        except:
            dir_path = f"{parent_dir}/{i}"
            os.makedirs(dir_path)

        def generate(prompt, start_index=1):
            imgs = simple_generate(prompt, quality, size, n)

            for j, im in enumerate(imgs, start=start_index):
                writetheimg(im, f'{dir_path}/{j}.png')

        with open(f'{dir_path}/prompt.txt', 'w') as f:
            json.dump(plan, f, indent=2)

        generate(plan["model_focus_prompt"], start_index=1)
        generate(plan["background_focus_prompt"], start_index=n+1)
        generate(plan["scene_only_prompt"], start_index=2*n+1)


if __name__ == "__main__":
    photoshoot_plans = [{'theme': 'Golden Tranquility: Embracing the Warmth of Diversity', 'location': 'A secluded tropical beach in Bali, Indonesia, known for its golden sands, swaying palm trees, and crystal-clear waters. This location provides a serene and picturesque backdrop that exudes warmth and tranquility.', 'outfit': 'A flowing, golden maxi dress made from lightweight, breathable fabric to complement the beach setting. The dress will have intricate batik patterns, a nod to traditional Indonesian craftsmanship, blending modern style with cultural heritage. Accessories will include delicate gold jewelry, such as hoop earrings and bangles, to enhance the overall elegance and harmony with the natural sunlight.', 'model_ethnicity': 'Asian', 'aspect_ratio': (1080, 1350), 'reason_for_aspect_ratio': 'This aspect ratio is ideal for emphasizing the vertical flow of the golden maxi dress and capturing the intricate batik patterns that are a nod to traditional Indonesian craftsmanship. The portrait orientation will also effectively showcase the model\'s elegance and the delicate gold jewelry, enhancing the overall harmony with the natural sunlight. Additionally, this framing will allow the serene and picturesque backdrop of the tropical beach in Bali, with its golden sands and swaying palm trees, to complement the theme of "Golden Tranquility: Embracing the Warmth of Diversity." The 4:5 ratio provides an intimate and immersive view that highlights the model\'s cultural representation and the stylist\'s vision in unison with the location\'s natural beauty.', 'model_focus_prompt': 'A serene scene on a secluded tropical beach in Bali, Indonesia, captures an Asian model gracefully posing in a flowing golden maxi dress adorned with intricate batik patterns, complemented by delicate gold hoop earrings and bangles, all harmonizing with the golden sands, swaying palm trees, and crystal-clear waters, embodying the theme of "Golden Tranquility: Embracing the Warmth of Diversity" in a visually evocative composition that aligns perfectly with an aspect ratio of (1080, 1350).', 'background_focus_prompt': 'A serene tropical beach in Bali sets the stage for a captivating scene where an Asian model, draped in a flowing, golden maxi dress adorned with intricate batik patterns, stands gracefully on the golden sands, her look perfectly accentuated by delicate gold jewelry, as the warm sunlight and swaying palm trees frame the essence of Golden Tranquility: Embracing the Warmth of Diversity.', 'scene_only_prompt': 'Immerse in the serene embrace of a secluded tropical beach in Bali, where an Asian model gracefully poses in a flowing, golden maxi dress adorned with intricate batik patterns, harmoniously blending modern style with Indonesian cultural heritage, as delicate gold jewelry catches the sunlight amidst the golden sands, swaying palm trees, and crystal-clear waters, embodying the theme of Golden Tranquility: Embracing the Warmth of Diversity.'}]

    photoshoot_plans = get_photoshoot_plan(10)
    generate_in_batch(photoshoot_plans, 'batch_generation24', test=False)
