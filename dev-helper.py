from helperkit import *


# region DevKit Table
class TableDevKit(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('VPT Dev Kit')
        self.geometry('420x320+40+40')
        self.resizable(width=False, height=False)
        
        self.nameflash_click1 = tk.StringVar(self, value="Choose")
        self.autorun = tk.BooleanVar(self, value=False)
        self.numpoints = []
        
        self.pickflashBtn = ttk.Combobox(self, textvariable=self.nameflash_click1, values=self.fetchWindowlist())
        self.pickflashBtn.place(x=5,y=12, width=110)
        self.label_pid = ttk.Label(self, text="PID:")
        self.label_pid.place(x=120, y=13)
        self.button_inject = ttk.Button(self, text="Inject", command=self.checkInjected, state=tk.NORMAL)
        self.button_inject.place(x=210, y=10)
        
        self.button_BUGBAY = ttk.Button(self, text="Bug Bay", command=self.bug_bay, state=tk.DISABLED)
        self.button_BUGBAY.place(x=300, y=10)
        
        self.addpoint("Get Toạ Độ: ")
        
        self.refPt = []
        self.zoomed = tk.StringVar()
        self.zoomed.set("1")
        self.min_zoom = 1
        self.max_zoom = 150
        
        self.button_crop = ttk.Button(self, text="Crop IMG", command=self.crop_image, state=tk.DISABLED)
        self.button_crop.place(x=20, y=70)

        self.button_checkimg = ttk.Button(self, text="Find IMG", command=self.find_image, state=tk.DISABLED)
        self.button_checkimg.place(x=115, y=70)
        
        self.text_croped = tk.Text(self, width=46, height=7, state=tk.NORMAL)
        self.text_croped.place(x=20, y=100)
        
    def bug_bay(self):
        print(self.nameflash_click1.get())
        try:
            if not HelperKit(self.nameflash_click1.get()).isfly():
                HelperKit(self.nameflash_click1.get()).setfly(True)
                # HelperKit(self.nameflash_click1.get()).setfly1(3)
            else:
                messagebox.showinfo(title="Adu lỗi", message="Đang bay thì ko thể bug bay được", parent=self)
        except Exception as e:
            print(e)
            messagebox.showinfo(title="Adu lỗi", message="Lỗi Ko bug được", parent=self)

    def crop_image(self):
        try:
            getcordtit = "baodeptrai_crop_" + self.nameflash_click1.get()
            image = HelperKit(self.nameflash_click1.get()).capture()
            clone = image.copy()
            cv2.imshow(getcordtit, image)
            
            def click_and_crop(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.refPt = [(x, y)]
                    self.text_croped.delete("1.0", "end-1c")
                    cv2.destroyWindow("roi")
                    self.button_checkimg.configure(state=tk.DISABLED)
                elif event == cv2.EVENT_LBUTTONUP:
                    self.refPt.append((x, y))
                    if len(self.refPt) == 2:
                        img = image.copy()
                        cv2.rectangle(img, self.refPt[0], self.refPt[1], (0, 255, 0), 1)
                        cv2.imshow(getcordtit, img)
                        roi = clone[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
                        self.text_croped.insert(tk.END, Convert(roi).img_to_b64())
                        cv2.imshow("roi", roi)
                        self.button_checkimg.configure(state=tk.NORMAL)
            cv2.setMouseCallback(getcordtit, click_and_crop)
        except Exception as e: 
            print(e)
            messagebox.showinfo(title="Lỗi Flash", message="Vui lòng chọn flash cần auto")
    
    def find_image(self):
        founded_img = HelperKit(self.nameflash_click1.get()).ImgSearchB64(self.text_croped.get(1.0, "end-1c"), 0.7, version=2)
        messagebox.showinfo(title="info img", message=f"cord: ({founded_img[0]}, {founded_img[1]})")
        
    def show_getcord(self, index):
        try:
            getcordtit = "baodeptrai_kq2_" + self.nameflash_click1.get()
            cv2.imshow(getcordtit, HelperKit(self.nameflash_click1.get()).capture())
            def onMouse(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.numpoints[index-1]["cords"] = {
                        "x" : x,
                        "y" : y,
                    }
                    self.numpoints[index-1]["var"]["x"].configure(text=x)
                    self.numpoints[index-1]["var"]["y"].configure(text=y)
                    cv2.destroyWindow(getcordtit) 

            cv2.setMouseCallback(getcordtit, onMouse)
        except: 
            messagebox.showinfo(title="Lỗi Flash", message="Vui lòng chọn flash cần auto")

    def addpoint(self, title=""):
        if len(self.numpoints) >= 18:
            return
        cX = ttk.Label(self, text=0)
        cY = ttk.Label(self, text=0)
        numclick1 = tk.IntVar()
        data = {
            "index": len(self.numpoints) + 1,
            "cords": {
                "x" : 0,
                "y" : 0,
            },
            "var": {
                "x" : cX,
                "y" : cY,
            },
            "type" : numclick1,
        }
        self.numpoints.append(data)

        if len(title) > 0:
            ttk.Label(self, text=title).place(x=5, y=10+data["index"]*30)

        ttk.Label(self, text="X" + str(data["index"])).place(x=5 + len(title)*7, y=10+data["index"]*30)
        
        cX.place(x=30 + len(title)*7, y=10 + data["index"] * 30)
        ttk.Label(self, text="Y"+ str(data["index"])).place(x=70 + len(title)*7, y=10+data["index"]*30)
        
        cY.place(x=100 + len(title)*7, y=10 + data["index"] * 30)
        ttk.Button(self, text="GET", command=lambda: self.show_getcord(data["index"])).place(x=135 + len(title)*7, y=10 + data["index"] * 30 - 2)

    def checkInjected(self):
        if self.nameflash_click1.get() != "Choose":
            self.label_pid.configure(text=f"PID: {HelperKit(title=self.nameflash_click1.get()).pid}")
            self.button_BUGBAY.configure( state=tk.NORMAL)
            self.button_crop.configure( state=tk.NORMAL)
        else:
            messagebox.showinfo(title="DEV KIT", message="Chọn flash", parent=self)
            
    def fetchWindowlist(self):
        titles = []
        t = []
        pidList = [(p.pid, p.name()) for p in psutil.process_iter()]

        def enumWindowsProc(hwnd, lParam):
            """ append window titles which match a pid """
            if (lParam is None) or ((lParam is not None) and (win32process.GetWindowThreadProcessId(hwnd)[1] == lParam)):
                text = win32gui.GetWindowText(hwnd)
                if text:
                    wStyle = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
                    if wStyle & win32con.WS_VISIBLE:
                        t.append("%s" % (text))
                        return

        def enumProcWnds(pid=None):
            win32gui.EnumWindows(enumWindowsProc, pid)
        
        try:
            for pid, pName in pidList:
                enumProcWnds(pid)
                if t:
                    for title in t:
                        if pName == "flash.exe":
                            a = []
                            a.append(pName)
                            a.append(title)
                            a.append(pid)
                            titles.append(a)
                    t = []
            titles = sorted(titles, key=lambda x: x[0].lower())
            return [x[1] for x in titles]
        except: return []

        
# endregion DevKit Table

if __name__ == "__main__":
    mainform = TableDevKit()
    mainform.mainloop()
    os._exit(0)