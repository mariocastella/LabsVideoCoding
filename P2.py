import os
import tempfile


def parse(filepath):
    tmpf = tempfile.NamedTemporaryFile()
    os.system("ffmpeg -i \"%s\" 2> %s" % (filepath, tmpf.name))
    lines = tmpf.readlines()
    tmpf.close()

    for l in lines:
        l = str(l.strip())
        if l.startswith('b\'Duration:'):
            start = l.find("D")
            Ginfo = l[start:-1]
        if l.startswith('b\'Stream #0:0'):
            start = l.find(")") + 3
            stream0 = l[start:-1]
        if l.startswith('b\'Stream #0:1'):
            start = l.find(")") + 3
            stream1 = l[start:-1]

    print(Ginfo + "\n" + stream0 + "\n" + stream1)


def cut(filename, fromtime, totime):
    os.system("ffmpeg -ss " + fromtime + " -i " + filename + " -to " + totime + " -c copy bbb_1080.mp4")
    os.system("ffmpeg -i " + filename + " -ss " + fromtime + " -to " + totime + " -c copy bbb_1080.mp4")


def allqualities():
    resize = ["1280:720", "720:480", "360:240", "160:120"]
    for i in resize:
        os.system("ffmpeg -i bbb_1080.mp4 -vf scale=" + i + " bbb_" + i + ".mp4")


def rename(name):
    os.rename("bbb_1080.mp4", name + "_original.mp4")
    os.rename("bbb_1280:720.mp4", name + "_720.mp4")
    os.rename("bbb_720:480.mp4", name + "_480.mp4")
    os.rename("bbb_360:240.mp4", name + "_240.mp4")
    os.rename("bbb_160:120.mp4", name + "_120.mp4")


def transcode(option, name):
    if option == 1:
        os.system("ffmpeg -i " + name + "_original.mp4 -vcodec vp9 " + name + "_transcode.mp4")
    elif option == 2:
        os.system("ffmpeg -i " + name + "_original.mp4 -acodec aac -vcodec copy " + name + "_transcode.mp4")
    elif option == 3:
        os.system("ffmpeg -i " + name + "_original.mp4 -vcodec vp9 " + name + "_transcode.mp4")
        os.system("ffmpeg -i " + name + "_transcode.mp4 -acodec aac -vcodec copy " + name + "_transcode.mp4")


def P2():
    while True:
        defaultfilename = "bbb_sunflower_1080p_30fps_normal.mp4"
        filename = str(input(
            "Put your video in the script directory and introduce here the name of it (skip with enter to use "
            "bbb_sunflower_1080p_30fps_normal.mp4): "))
        print("here you can see your video specifications")
        if filename:
            parse(filename)
        else:
            parse(defaultfilename)
        input("Press Enter to continue...")
        defaultfromtime = "00:47"
        defaulttotime = "00:57"
        fromtime = input("Insert from what time you want to cut the original video (Example: 00:47) or skip with "
                         "enter to use default value: ")
        totime = input("Insert to what time you want to cut: ")
        if fromtime and totime:
            if filename:
                cut(filename, fromtime, totime)
            else:
                cut(defaultfilename, fromtime, totime)
        else:
            cut(defaultfilename, defaultfromtime, defaulttotime)

        allqualities()

        name = input("Insert a name for files: ")
        rename(name)
        option = input("Select using number tags what action do you want to apply \n[Enter] Do not transcode \n[1] "
                       "Transcode video into vp9 codec\n[2] Transcode audio into acc codec\n[3] Transcode both video "
                       "and audio into vp9 and acc codecs\n Selected: ")
        if option:
            transcode(int(option), name)
            parse(name + "_transcode.mp4")


if __name__ == '__main__':
    P2()

