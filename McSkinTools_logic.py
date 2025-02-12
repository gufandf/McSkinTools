from PIL import Image, ImageEnhance
import os
import requests, json, base64
import numpy as np
from io import BytesIO


def find_data(source, target):
    """计算透视变换矩阵"""
    matrix = []
    for s, t in zip(source, target):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = np.matrix(matrix, dtype=float)
    B = np.array(source).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def perspectiveTrans(image: Image, target_points: list) -> Image:
    """透视变换"""
    # 定义源图像的四个顶点
    source_points = [
        (0, 0),
        (image.width, 0),
        (image.width, image.height),
        (0, image.height),
    ]
    # 计算透视变换矩阵
    coeffs = find_data(source_points, target_points)
    # 应用透视变换
    transformed_image = image.transform(
        image.size, Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC
    )
    # 显示或保存结果
    return transformed_image


def get_skin(username) -> Image:
    # 获取玩家的UUID
    uuid_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(uuid_url)
    if response.status_code != 200:
        print(f"无法找到玩家 {username}")
        return None
    uuid = response.json()["id"]

    # 获取玩家的皮肤信息
    skin_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(skin_url)
    if response.status_code != 200:
        print(f"无法获取皮肤信息 {username}")
        return None
    skin_data = response.json()

    # 提取皮肤URL
    skin_value = skin_data["properties"][0]["value"]
    skin_data_decoded = json.loads(base64.b64decode(skin_value))
    skin_url = skin_data_decoded["textures"]["SKIN"]["url"]

    # 下载皮肤
    response = requests.get(skin_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        return img
    else:
        print(f"无法获取皮肤{response.status_code} {username}")
        return None


def gen_headimg2D(skin: Image) -> Image:
    l1 = ImageEnhance.Brightness(skin.crop([8, 8, 16, 16]).convert("RGBA")).enhance(0.9)
    l2 = skin.crop([40, 8, 48, 16]).convert("RGBA")
    head = Image.new("RGBA", [256, 256], (0, 0, 0, 0))
    head.paste(l1.resize([224, 224], Image.NEAREST), [16, 16])
    l2_resized = l2.resize([256, 256], Image.NEAREST)
    head = Image.alpha_composite(head, l2_resized)
    return head


def gen_headimg3D(skin: Image) -> Image:
    head = Image.new("RGBA", [256, 256], (0, 0, 0, 0))

    head_l0 = Image.new("RGBA", [256, 256], (0, 0, 0, 0))
    l0_l = skin.crop([48, 8, 56, 16]).convert("RGBA")
    l0_n = skin.crop([56, 8, 64, 16]).convert("RGBA")
    l0_b = skin.crop([48, 0, 56, 8]).convert("RGBA")
    l0_l = perspectiveTrans(
        l0_l.resize([256, 256], Image.NEAREST),
        [(242, 58), (128, 2), (128, 141), (242, 197)],
    )
    l0_n = perspectiveTrans(
        l0_n.resize([256, 256], Image.NEAREST),
        [(14, 58), (128, 2), (128, 141), (14, 197)],
    )
    l0_b = perspectiveTrans(
        l0_b.resize([256, 256], Image.NEAREST),
        [(14, 197), (128, 141), (242, 197), (128, 254)],
    )
    head_l0 = Image.alpha_composite(head_l0, l0_l)
    head_l0 = Image.alpha_composite(head_l0, l0_n)
    head_l0 = Image.alpha_composite(head_l0, l0_b)

    head_l1 = Image.new("RGBA", [256, 256], (0, 0, 0, 0))
    l1_r = skin.crop([0, 8, 8, 16]).convert("RGBA")
    l1_f = skin.crop([8, 8, 16, 16]).convert("RGBA")
    l1_t = skin.crop([8, 0, 16, 8]).convert("RGBA")
    l1_r = perspectiveTrans(
        l1_r.resize([256, 256], Image.NEAREST),
        [(14, 58), (128, 115), (128, 254), (14, 197)],
    )
    l1_f = perspectiveTrans(
        l1_f.resize([256, 256], Image.NEAREST),
        [(242, 58), (128, 115), (128, 254), (242, 197)],
    )
    l1_t = perspectiveTrans(
        l1_t.resize([256, 256], Image.NEAREST),
        [(14, 58), (128, 2), (242, 58), (128, 115)],
    )
    head_l1 = Image.alpha_composite(head_l1, l1_r)
    head_l1 = Image.alpha_composite(head_l1, l1_f)
    head_l1 = Image.alpha_composite(head_l1, l1_t)

    head_l2 = Image.new("RGBA", [256, 256], (0, 0, 0, 0))
    l2_r = skin.crop([32, 8, 40, 16]).convert("RGBA")
    l2_f = skin.crop([40, 8, 48, 16]).convert("RGBA")
    l2_t = skin.crop([40, 0, 48, 8]).convert("RGBA")
    l2_r = perspectiveTrans(
        l2_r.resize([256, 256], Image.NEAREST),
        [(14, 58), (128, 115), (128, 254), (14, 197)],
    )
    l2_f = perspectiveTrans(
        l2_f.resize([256, 256], Image.NEAREST),
        [(242, 58), (128, 115), (128, 254), (242, 197)],
    )
    l2_t = perspectiveTrans(
        l2_t.resize([256, 256], Image.NEAREST),
        [(14, 58), (128, 2), (242, 58), (128, 115)],
    )

    head_l2 = Image.alpha_composite(head_l2, l2_r)
    head_l2 = Image.alpha_composite(head_l2, l2_f)
    head_l2 = Image.alpha_composite(head_l2, l2_t)

    head_l0 = ImageEnhance.Brightness(head_l0).enhance(0.9)
    head_l1 = head_l1.resize([224, 224], Image.NEAREST)
    head_l1 = ImageEnhance.Brightness(head_l1).enhance(0.95)
    head.paste(head_l1, [16, 16])
    head = Image.alpha_composite(head_l0, head)
    head = Image.alpha_composite(head, head_l2)
    return head


"""
head: Image,
head_o: Image,
body: Image,
body_o: Image,
left_hand: Image,
left_hand_o: Image,
right_hand: Image,
right_hand_o: Image,
left_leg: Image,
left_leg_o: Image,
right_leg: Image,
right_leg_o: Image,
"""


def crop_skin(skin: Image) -> Image:
    top_head = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    top_head.paste(skin.crop([32, 0, 64, 16]).convert("RGBA"), (32, 0))
    und_head = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    und_head.paste(skin.crop([0, 0, 32, 16]).convert("RGBA"), [0, 0])
    top_body = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    top_body.paste(skin.crop([16, 32, 40, 48]).convert("RGBA"), (16, 32))
    und_body = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    und_body.paste(skin.crop([16, 16, 40, 32]).convert("RGBA"), (16, 16))

    top_left_arm = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    top_left_arm.paste(skin.crop([48, 48, 64, 64]).convert("RGBA"), (48, 48))
    und_left_arm = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    und_left_arm.paste(skin.crop([32, 48, 48, 64]).convert("RGBA"), (32, 48))
    top_right_arm = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    top_right_arm.paste(skin.crop([40, 32, 56, 48]).convert("RGBA"), (40, 32))
    und_right_arm = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    und_right_arm.paste(skin.crop([40, 16, 56, 32]).convert("RGBA"), (40, 16))
    top_left_leg = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    top_left_leg.paste(skin.crop([0, 48, 16, 64]).convert("RGBA"), (0, 48))
    und_left_leg = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    und_left_leg.paste(skin.crop([16, 48, 32, 64]).convert("RGBA"), (16, 48))
    top_right_leg = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    top_right_leg.paste(skin.crop([0, 32, 16, 48]).convert("RGBA"), (0, 32))
    und_right_leg = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
    und_right_leg.paste(skin.crop([0, 16, 16, 32]).convert("RGBA"), (0, 16))

    return [
        top_head,
        und_head,
        top_body,
        und_body,
        top_left_arm,
        und_left_arm,
        top_right_arm,
        und_right_arm,
        top_left_leg,
        und_left_leg,
        top_right_leg,
        und_right_leg,
    ]


if "__main__" == __name__:
    crop_skin(Image.open("./skin/Gufandf_2.png"))[0].show()
