import os


class streaming:
    def __init__(self, name, fromtime="00:47", totime="00:57",
                 filename="bbb_sunflower_1080p_30fps_normal.mp4"):
        """
        Initialize general parameters to streaming video comparator
        :param name: Output video name
        :param fromtime: From what time you want to cut
        :param totime: To what time you want to cut
        :param filename: Filename of the original video
        """
        self.name = name
        self.filename = filename
        self.fromtime = fromtime
        self.totime = totime

    def get_streaming_videos(self):
        os.system("ffmpeg -ss %s -i %s -to %s -c copy h264.mp4" % (self.fromtime, self.filename, self.totime))
        os.system("ffmpeg -i %s -ss %s -to %s -c copy h264.mp4" % (self.filename, self.fromtime, self.totime))

        # VP8 ENCODER https://trac.ffmpeg.org/wiki/Encode/VP8
        # worst quality
        os.system("ffmpeg -i h264.mp4 -c:v libvpx -b:v 1M -c:a libvorbis vp8.webm")

        # VP9 ENCODER https://trac.ffmpeg.org/wiki/Encode/VP9
        # improve VP8 quality
        os.system("ffmpeg -i h264.mp4 -c:v libvpx-vp9 -b:v 2M vp9.webm")

        # AV1 ENCODER https://trac.ffmpeg.org/wiki/Encode/AV1
        # better dynamic range odf color
        os.system("ffmpeg -i h264.mp4 -c:v libaom-av1 -crf 30 -b:v 0 -strict experimental av1.mkv")

        # H265 ENCODER https://trac.ffmpeg.org/wiki/Encode/H.265
        # Middle quality, good using less performance than AV1
        os.system("ffmpeg -i h264.mp4 -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k h265.mp4")

    def get_streaming_comparator(self):
        self.get_streaming_videos()

        # MERGE VIDEOS #https://trac.ffmpeg.org/wiki/Create%20a%20mosaic%20out%20of%20several%20input%20videos
        os.system(
            "ffmpeg -i h265.mp4 -i av1.mkv -i vp9.webm -i vp8.webm -filter_complex 'nullsrc=size=1280x720 [base]; [0:v]"
            " setpts=PTS-STARTPTS, scale=640x360 [upperleft]; [1:v] setpts=PTS-STARTPTS, scale=640x360 ["
            "upperright]; [2:v] setpts=PTS-STARTPTS, scale=640x360 [lowerleft]; [3:v] setpts=PTS-STARTPTS, "
            "scale=640x360 [lowerright]; [base][upperleft] overlay=shortest=1 [tmp1]; [tmp1][upperright] "
            "overlay=shortest=1:x=640 [tmp2]; [tmp2][lowerleft] overlay=shortest=1:y=360 [tmp3]; [tmp3]["
            "lowerright] overlay=shortest=1:x=640:y=360' -c:v libx264 %s.mkv" % self.name)

    def make_broadcast(self):
        os.system("ffmpeg -i %s.mp4 -v 0 -vcodec mpeg4 -f mpegts udp://192.168.1.40:1234" % self.name)

def S3():
    while True:
        filename = input("Insert output video name: ")
        fromtime = input("Insert from what time you want to cut the original video (Example: 00:47) or skip with "
                         "enter to use default value: ")
        totime = input("Insert to what time you want to cut: ")
        if fromtime and totime:
            stream = streaming(filename, fromtime, totime)
        else:
            stream = streaming(filename)

        stream.get_streaming_comparator()

        yesNo = input("Do you want to make a broadcast of the video? [y/N]")
        if yesNo == "y":
            stream.make_broadcast()


if __name__ == '__main__':
    S3()
