import os


def main():
    choose = input("Select using number tags what action do you want to apply \n[1] Play video with yuv "
                   "histograms\n[2] Generate copies with all qualities\n[3] Generate copy with acc audio codec\n["
                   "4] Generate copy with mono audio\n Selected: ")
    fromtime = "00:47"
    totime = "00:57"
    os.system("ffmpeg -ss " + fromtime + " -i bbb_sunflower_1080p_30fps_normal.mp4 -to " + totime + " -c copy "
                                                                                                    "bbb_1080.mp4")
    os.system("ffmpeg -i bbb_sunflower_1080p_30fps_normal.mp4 -ss " + fromtime + " -to " + totime + " -c copy "
                                                                                                    "bbb_1080.mp4")
    if choose == '1':
        os.system("ffplay bbb_1080.mp4 -vf \"split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay\"")

    if choose == '2':
        resize = ["1280:720", "720:480", "360:240", "160:120"]
        for i in resize:
            os.system("ffmpeg -i bbb_1080.mp4 -vf scale=" + i + " bbb_" + i + ".mp4")
    if choose == '3':
        os.system("ffmpeg -i bbb_1080.mp4 -acodec aac -vcodec copy bbb_acc.mp4")
    if choose == '4':
        os.system("ffmpeg -i bbb_1080.mp4 -ac 1 bbb_mono.mp4")


main()
