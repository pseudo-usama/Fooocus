def improve_img_from_mask(prompt, quality, size, num_of_imgs, img_to_improve, mask, improvement_prompt):
    args = [None, 'a girl', '', ['Fooocus V2', 'Fooocus Enhance', 'Fooocus Sharp'], 'Speed', '1152×896 <span style="color: grey;"> ∣ 9:7</span>', 2, 'png', '5255450403419049086', False, 2, 4, 'juggernautXL_v8Rundiffusion.safetensors', 'None', 0.5, True, 'sd_xl_offset_example-lora_1.0.safetensors', 0.1, True, 'None', 1, True, 'None', 1, True, 'None', 1, True, 'None', 1, True, 'inpaint', 'Disabled', None, [],
     {'image': None, 'mask': None}, 'improve this necklace', None, False, False, False, False, 1.5, 0.8, 0.3, 7, 2, 'dpmpp_2m_sde_gpu', 'karras', 'Default (model)', -1, -1, -1, -1, -1, -1, False, False, False, False, 64, 128, 'joint', 0.25, False, 1.01, 1.02, 0.99, 0.95, False, False, 'None', 0.5, 0, False, False, 0, False, 'fooocus', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt']

    args[1] = prompt
    args[4] = quality
    args[5] = f'{size[0]}×{size[1]} <span style="color: grey;"> ∣ 4:5</span>'
    args[6] = 1 # num_of_imgs

    args[35]['image'] = img_to_improve
    args[35]['mask'] = mask
    args[36] = ''

    improved_img = generate(args)

    return improved_img[0]


def improve_img(prompt, quality, size, num_of_imgs, img_to_improve, improvement_prompt):
    def get_masks():
        height, width = img_to_improve.shape[:2]
        masks = []

        MASK_WIDTH = 400
        STRIDE = 400
        OVERLAP = 50
        step = STRIDE - OVERLAP

        for y in range(0, height, step):
            for x in range(0, width, step):
                # Adjust x and y if the remaining part of the image is smaller than mask_width
                if x + MASK_WIDTH > width:
                    x = width - MASK_WIDTH
                if y + MASK_WIDTH > height:
                    y = height - MASK_WIDTH

                mask = np.zeros_like(img_to_improve)
                mask[y:y+MASK_WIDTH, x:x+MASK_WIDTH] = 255
                masks.append(mask)

        return masks

    args = [None, 'a girl', '', ['Fooocus V2', 'Fooocus Enhance', 'Fooocus Sharp'], 'Speed', '1152×896 <span style="color: grey;"> ∣ 9:7</span>', 2, 'png', '5255450403419049086', False, 2, 4, 'juggernautXL_v8Rundiffusion.safetensors', 'None', 0.5, True, 'sd_xl_offset_example-lora_1.0.safetensors', 0.1, True, 'None', 1, True, 'None', 1, True, 'None', 1, True, 'None', 1, True, 'inpaint', 'Disabled', None, [],
     {'image': None, 'mask': None}, 'improve this necklace', None, False, False, False, False, 1.5, 0.8, 0.3, 7, 2, 'dpmpp_2m_sde_gpu', 'karras', 'Default (model)', -1, -1, -1, -1, -1, -1, False, False, False, False, 64, 128, 'joint', 0.25, False, 1.01, 1.02, 0.99, 0.95, False, False, 'None', 0.5, 0, False, False, 0, False, 'fooocus', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt', None, 0.5, 0.6, 'ImagePrompt']


    args[1] = prompt
    args[4] = quality
    args[5] = f'{size[0]}×{size[1]} <span style="color: grey;"> ∣ 4:5</span>'
    args[6] = 1 # num_of_imgs

    args[35]['image'] = img_to_improve
    args[36] = ''


    masks = get_masks()
    for mask in tqdm(masks):
        args[35]['mask'] = mask
        improved_img = generate(deepcopy(args))
        im = readtheimg(improved_img[0])
        writetheimg(im, 'img.jpg')
        args[35]['image'] = im


    return args[35]['image']


def fn(dir_path, prompt):
    dir_path = Path(dir_path)
    imgs = dir_path.glob('img_*.*')

    for im in imgs:
        im = str(im)
        img_number = re.search(r"_(\d+)\.", im).group(1)
        masks = dir_path.glob(f"mask_{img_number}_*.*")

        improv_img_path = f'{dir_path}/improv{img_number}.jpg'
        for i, mask in enumerate(masks):
            if i > 0:
                im = improv_img_path

            print(im, mask)

            mask = readtheimg(str(mask))
            mask[mask > 128] = 255
            mask[mask <= 128] = 0

            img = readtheimg(im)
            improved_img = improve_img_from_mask(prompt, 'Quality',
                                                 (1080, 1350), 1, img,
                                                 mask, '')
            writetheimg(improved_img, improv_img_path)




if __name__ == "__main__":
    # for i in range(1, 5):
    #     mask = readtheimg(f'mask{i}.jpg')
    #     mask[mask > 128] = 255
    #     mask[mask <= 128] = 0

    #     img = readtheimg(f'new.jpg')
    #     improved_img = improve_img_from_mask('Generate an image of a Polynesian model, styled with minimal makeup and adorned with simple, earthy accessories, wearing a lightweight, flowy summer maxi dress in various shades of blue with a high slit and deep v-neck, standing in a lush tropical forest where natural sunlight filters through the foliage creating a serene, dramatic, and ethereal atmosphere.',
    #             'Quality',
    #             (1080, 1350),
    #             1,
    #             img,
    #             mask,
    #             '')
    #     writetheimg(readtheimg(improved_img), f'new.jpg')
