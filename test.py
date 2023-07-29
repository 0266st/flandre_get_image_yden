import aiohttp
import asyncio
import json

url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
data = {
            "restore_faces": False,
            "face_restorer": "CodeFormer",
            "codeformer_weight": 0.5,
            "prompt": "erotic, nsfw, pussy, tits, 8k, very cute girl",
            "negative_prompt": "horror, icon, lbad anatomy, long_neck, long_body, longbody, deformed mutated disfigured, missing arms, extra_arms, mutated hands, extra_legs, bad hands, poorly_drawn_hands, malformed_hands, missing_limb, floating_limbs, disconnected_limbs, extra_fingers, bad fingers, liquid fingers, poorly drawn fingers, missing fingers, extra digit, fewer digits, ugly face, deformed eyes, partial face, partial head, bad face, inaccurate limb, cropped, low quality, worst quality, out of focus, ugly, error, jpeg artifacts, lowers, blurry, bokeh",
            "seed": -1,
            "seed_enable_extras": False,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": 0,
            "seed_resize_from_w": 0,
            "sampler_name": "Euler a",
            "steps": 30,
            "cfg_scale": 7.5,
            "denoising_strength": 0.35,
            "batch_count": 1,
            "batch_size": 1,
            "base_size": 512,
            "max_size": 768,
            "tiling": False,
            "highres_fix": False,
            "firstphase_height": 512,
            "firstphase_width": 512,
            "upscaler_name": "None",
            "filter_nsfw": False,
            "include_grid": False,
            "sample_path": "outputs/krita-out",
            "orig_width": 512,
            "orig_height": 512
}


async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

# 非同期コードを実行するため、イベントループを作成して実行します
loop = asyncio.get_event_loop()
result = loop.run_until_complete(post_data(url=url, data=data))
print(result['images'])


