import customtkinter
import os, threading
from tkinter import filedialog
from PIL import Image
from McSkinTools_logic import *

skin_list = []
threads = []


class skin_skin_list(customtkinter.CTkFrame):
    def __init__(self, master, skin: Image, name: str):
        super().__init__(master)
        self.grid(sticky="ew", pady=(0, 5))
        self.img = customtkinter.CTkImage(
            light_image=skin, dark_image=skin, size=(64, 64)
        )
        self.image_label = customtkinter.CTkLabel(
            self, image=self.img, text=""
        )  # display image with a CTkLabel
        self.image_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.text = customtkinter.CTkLabel(self, text=name, wraplength=80)
        self.text.grid(row=0, column=1, padx=10, sticky="e")


class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Get Skin")
        self.add("Headimg")
        self.add("Tailor")
        self.DownloadSkin = DownloadSkin(self.tab("Get Skin"))
        self.DownloadSkin.grid(row=0, column=0, padx=5, pady=5)
        self.GenHeadimg = GenHeadimg(self.tab("Headimg"))
        self.GenHeadimg.grid(row=0, column=0, padx=5, pady=5)
        self.GenHeadimg.columnconfigure(0, weight=1)
        self.Tailorimg = Tailor(self.tab("Tailor"))
        self.Tailorimg.grid(row=0, column=0, padx=5, pady=5)

        # add widgets on tabs


class Tailor(customtkinter.CTkFrame):
    def pick_cover_skin(self):
        file_path = filedialog.askopenfilename(
            title="choose a skin",
            filetypes=[("skin", "*.png")],
        )
        img = Image.open(file_path)
        if img.size == (64, 64):
            self.coverskin = img
        else:
            self.coverskin = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
        self.skintop.configure(
            image=customtkinter.CTkImage(light_image=self.coverskin, size=(64, 64))
        )

    def output(self):
        target_path = filedialog.askdirectory(
            title="pick up a position",  # 对话框标题
        )
        cover = [
            self.ct_head.get(),
            self.cu_head.get(),
            self.ct_body.get(),
            self.cu_body.get(),
            self.ct_left_arm.get(),
            self.cu_left_arm.get(),
            self.ct_right_arm.get(),
            self.cu_right_arm.get(),
            self.ct_left_leg.get(),
            self.cu_left_leg.get(),
            self.ct_right_leg.get(),
            self.cu_right_leg.get(),
        ]
        list = [
            self.lt_head.get(),
            self.lu_head.get(),
            self.lt_body.get(),
            self.lu_body.get(),
            self.lt_left_arm.get(),
            self.lu_left_arm.get(),
            self.lt_right_arm.get(),
            self.lu_right_arm.get(),
            self.lt_left_leg.get(),
            self.lu_left_leg.get(),
            self.lt_right_leg.get(),
            self.lu_right_leg.get(),
        ]
        for skin in skin_list:
            listSkinimg = skin[0]
            coverskin = self.coverskin
            
            croped_skin = crop_skin(listSkinimg)
            result_skin = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
            for i in range(12):
                if list[i]:
                    result_skin.alpha_composite(croped_skin[i])
            
            croped_coverskin = crop_skin(coverskin)
            result_coverskin = Image.new("RGBA", [64, 64], (0, 0, 0, 0))
            for i in range(12):
                if cover[i]:
                    result_coverskin.alpha_composite(croped_coverskin[i])
            
            result_skin.alpha_composite(result_coverskin)
            result_skin.save(
                    target_path
                    + "/"
                    + os.path.basename(skin[1]).split(".")[0]
                    + "-tailored.png"
                )
            

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.coverskin = Image.new("RGBA", [64, 64], (0, 0, 0, 0))

        self.skintop = customtkinter.CTkLabel(
            self,
            image=customtkinter.CTkImage(light_image=self.coverskin, size=(64, 64)),
            text="cover skin",
        )
        self.skintop.grid(row=1, column=0, padx=5, pady=5)
        self.skinbuttom = customtkinter.CTkLabel(
            self,
            image=customtkinter.CTkImage(
                light_image=Image.new("RGBA", [64, 64], (0, 0, 100, 255)), size=(64, 64)
            ),
            text="skin in list",
        )
        self.skinbuttom.grid(row=3, column=0, padx=5, pady=5)

        customtkinter.CTkButton(
            self, text="pick cover skin", command=self.pick_cover_skin, width=64
        ).grid(row=0, column=0)
        customtkinter.CTkButton(
            self, text="Output", command=self.output, width=64
        ).grid(row=8, column=0)

        customtkinter.CTkLabel(self, text="top layer").grid(row=1, column=1)
        customtkinter.CTkLabel(self, text="under layer").grid(row=2, column=1)
        customtkinter.CTkLabel(self, text="top layer").grid(row=3, column=1)
        customtkinter.CTkLabel(self, text="under layer").grid(row=4, column=1)

        customtkinter.CTkLabel(self, text="head").grid(row=0, column=2)
        customtkinter.CTkLabel(self, text="body").grid(row=0, column=3)
        customtkinter.CTkLabel(self, text="left arm").grid(row=0, column=4)
        customtkinter.CTkLabel(self, text="right arm").grid(row=0, column=5)
        customtkinter.CTkLabel(self, text="left leg").grid(row=0, column=6)
        customtkinter.CTkLabel(self, text="right leg").grid(row=0, column=7)

        self.ct_head = customtkinter.CTkSwitch(self, text="", width=50)
        self.ct_head.grid(row=1, column=2)
        self.ct_body = customtkinter.CTkSwitch(self, text="", width=50)
        self.ct_body.grid(row=1, column=3)
        self.ct_left_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.ct_left_arm.grid(row=1, column=4)
        self.ct_right_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.ct_right_arm.grid(row=1, column=5)
        self.ct_left_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.ct_left_leg.grid(row=1, column=6)
        self.ct_right_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.ct_right_leg.grid(row=1, column=7)

        self.cu_head = customtkinter.CTkSwitch(self, text="", width=50)
        self.cu_head.grid(row=2, column=2)
        self.cu_body = customtkinter.CTkSwitch(self, text="", width=50)
        self.cu_body.grid(row=2, column=3)
        self.cu_left_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.cu_left_arm.grid(row=2, column=4)
        self.cu_right_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.cu_right_arm.grid(row=2, column=5)
        self.cu_left_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.cu_left_leg.grid(row=2, column=6)
        self.cu_right_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.cu_right_leg.grid(row=2, column=7)

        self.lt_head = customtkinter.CTkSwitch(self, text="", width=50)
        self.lt_head.grid(row=3, column=2)
        self.lt_body = customtkinter.CTkSwitch(self, text="", width=50)
        self.lt_body.grid(row=3, column=3)
        self.lt_left_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.lt_left_arm.grid(row=3, column=4)
        self.lt_right_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.lt_right_arm.grid(row=3, column=5)
        self.lt_left_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.lt_left_leg.grid(row=3, column=6)
        self.lt_right_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.lt_right_leg.grid(row=3, column=7)

        self.lu_head = customtkinter.CTkSwitch(self, text="", width=50)
        self.lu_head.grid(row=4, column=2)
        self.lu_body = customtkinter.CTkSwitch(self, text="", width=50)
        self.lu_body.grid(row=4, column=3)
        self.lu_left_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.lu_left_arm.grid(row=4, column=4)
        self.lu_right_arm = customtkinter.CTkSwitch(self, text="", width=50)
        self.lu_right_arm.grid(row=4, column=5)
        self.lu_left_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.lu_left_leg.grid(row=4, column=6)
        self.lu_right_leg = customtkinter.CTkSwitch(self, text="", width=50)
        self.lu_right_leg.grid(row=4, column=7)


class GenHeadimg(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.gen2DButton = customtkinter.CTkButton(
            self, text="Generate 2D headimg", command=self.gen2D
        )
        self.gen2DButton.grid(row=0, column=0, pady=(0, 5))
        self.gen3DButton = customtkinter.CTkButton(
            self, text="Generate 3D headimg", command=self.gen3D
        )
        self.gen3DButton.grid(row=1, column=0, pady=(0, 5))

    def gen2D(self):
        global skin_list
        target_path = filedialog.askdirectory(
            title="pick up a position",
        )
        if target_path:
            for skin in skin_list:
                img = gen_headimg2D(skin[0])
                img.save(
                    target_path
                    + "/"
                    + os.path.basename(skin[1]).split(".")[0]
                    + "-2D.png"
                )

    def gen3D(self):
        global skin_list
        target_path = filedialog.askdirectory(
            title="pick up a position",
        )
        if target_path:
            for skin in skin_list:
                img = gen_headimg3D(skin[0])
                img.save(
                    target_path
                    + "/"
                    + os.path.basename(skin[1]).split(".")[0]
                    + "-3D.png"
                )


class DownloadSkin(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(
            self, text="Input player id (one per line)："
        )
        self.label.grid(row=0, column=0, pady=(0, 5))
        self.textbox = customtkinter.CTkTextbox(self, width=200, height=300)
        self.textbox.grid(row=1, column=0, pady=(0, 5))
        self.label1 = customtkinter.CTkLabel(
            self, text="It takes some time to download all the skins."
        )
        self.label1.grid(row=2, column=0, pady=(0, 5))
        self.downloadButton = customtkinter.CTkButton(
            self, text="Download to Skin List", command=self.download
        )
        self.downloadButton.grid(row=3, column=0, pady=(0, 5))
        self.progressbar = customtkinter.CTkProgressBar(
            self, orientation="download progress"
        )
        self.progressbar.grid(row=4, column=0, pady=(0, 5))
        self.progressbar.set(1)

    def download(self):
        global totleTask, completeTask
        inputText = self.textbox.get("1.0", "end-1c")
        playerNames = inputText.split("\n")
        totleTask = len(playerNames)
        completeTask = 0
        for name in playerNames:
            thread = threading.Thread(target=downloadskin, args=(name,))
            thread.start()
        self.textbox.delete("1.0", "end")


totleTask = 0
completeTask = 0


def downloadskin(name):
    global completeTask
    skin = get_skin(name)
    if skin:
        skin_list.append((skin, name))
    else:
        pass
    completeTask += 1
    app.tab_view.DownloadSkin.progressbar.set(completeTask / totleTask)
    app.flash_list()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Minecraft Skin Tools")
        self.geometry("750x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.leftSide = customtkinter.CTkFrame(self, width=200)
        self.leftSide.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.leftSide.grid_rowconfigure(0, weight=1)

        self.leftSide.skinList = customtkinter.CTkScrollableFrame(self.leftSide)
        self.leftSide.skinList.grid(row=0, column=0, sticky="nsew")
        self.leftSide.skinList.columnconfigure(0, weight=1)

        self.leftSide.leftIO = customtkinter.CTkFrame(self.leftSide, height=30)
        self.leftSide.leftIO.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.leftSide.leftIO.Input = customtkinter.CTkButton(
            self.leftSide.leftIO,
            width=(222 - 5) / 2,
            text="Input",
            command=self.input_skin,
        )
        self.leftSide.leftIO.Input.grid(row=0, column=0, sticky="ew")
        self.leftSide.leftIO.Output = customtkinter.CTkButton(
            self.leftSide.leftIO,
            width=(222 - 5) / 2,
            text="Output",
            command=self.output,
        )
        self.leftSide.leftIO.Output.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        self.tab_view = TabView(master=self)
        self.tab_view.grid(row=0, column=1, padx=5, pady=(0, 5), sticky="nsew")

    def output(self):
        target_path = filedialog.askdirectory(
            title="pick up a position",  # 对话框标题
        )
        for skin in skin_list:
            skin[0].save(
                    target_path
                    + "/"
                    + os.path.basename(skin[1]).split(".")[0]
                    + ".png"
                )

    def flash_list(self):
        for widget in self.leftSide.skinList.winfo_children():
            widget.destroy()
        i = 0
        for skin in skin_list:
            self.leftSide.skinList.skin = skin_skin_list(
                self.leftSide.skinList, skin=skin[0], name=skin[1]
            )
            self.leftSide.skinList.skin.grid(row=i, column=0)
            i += 1

    def input_skin(self):
        file_paths = filedialog.askopenfilenames(
            title="input skins",
            filetypes=[("skin", "*.png")],
        )
        for file in file_paths:
            img = Image.open(file)
            if img.size == (64, 64):
                skin_list.append((img, os.path.basename(file).split(".")[0]))
        # print(skin_list)
        self.flash_list()


app = App()
app.mainloop()
