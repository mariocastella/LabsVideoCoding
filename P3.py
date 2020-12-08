import os


class Container:
    def __init__(self, name, vcodec="h264", acodec="aac", lowBR="45", filename="bbb_sunflower_1080p_30fps_normal.mp4",
                 fromtime="00:47", totime="00:57"):
        """
        Initialize general parameters to generate new container
        :param name: Name for the new container
        :param filename: Filename of the original video
        :param fromtime: From what time you want to cut
        :param totime: To what time you want to cut
        :param vcodec: Video codec for the new container
        :param acodec: Audio codec for the new container
        :param lowBR: Bit rate for the lower bit rate stream
        :param broadcast: Dictionary with compatibility codecs for each broadcast
        """
        self.filename = filename
        self.name = name
        self.fromtime = fromtime
        self.totime = totime
        self.vcodec = vcodec
        self.acodec = acodec
        self.lowBR = lowBR
        self.broadcast = {
            "dv3_video": ["mpeg", "h264"],
            "dv3_audio": ["aac", "ac3"],
            "isdb_video": ["mpeg", "h264"],
            "isdb_audio": ["aac"],
            "atsc_video": ["mpeg", "h264"],
            "atsc_audio": ["aac"],
            "dtmb_video": ["avs", "avs+", "mpeg", "h264"],
            "dtmb_audio": ["dra", "aac", "ac3", "mp2", "mp3"]
        }

    def createContainer(self, streams):
        """
        Function that creates a container from given streams
        :param streams: Dictionary contains video, audio, subtitle streams namefile and needed commands
        """
        command = "ffmpeg "
        if streams["video"]:
            for i in streams["video"]:
                command += "-i %s " % i

        if streams["audio"]:
            for i in streams["audio"]:
                command += "-i %s " % i

        if streams["subtitles"]:
            for i in streams["subtitles"]:
                command += "-i %s " % i

        command += streams["command"]
        command += " %s.mp4" % self.name
        os.system(command)

    def createMultiAudioContainer(self):
        """
        Function that creates streams of mono audio and given lower bit rate audio and execute createContainer of its streams
        """
        os.system("ffmpeg -ss %s -i %s -to %s -c copy cut.mp4" % (self.fromtime, self.filename, self.totime))
        os.system("ffmpeg -i %s -ss %s -to %s -c copy cut.mp4" % (self.filename, self.fromtime, self.totime))
        os.system("ffmpeg -i cut.mp4 -an -c:v %s original_video.mp4" % self.vcodec)
        os.system("ffmpeg -i cut.mp4 -vn -c:a %s original_audio.%s" % (self.acodec, self.acodec))
        os.system("ffmpeg -i original_audio.%s -ac 1 mono_audio.%s" % (self.acodec, self.acodec))
        os.system("ffmpeg -i original_audio.%s -ab %sk lowBR_audio.%s" % (self.acodec, self.lowBR, self.acodec))

        streams = {"video": ["original_video.mp4"],
                   "audio": ["original_audio.%s" % self.acodec, "mono_audio.%s" % self.acodec,
                             "lowBR_audio.%s" % self.acodec],
                   "subtitles": ["subtitles.srt"],
                   "command": "-map 0:v:0 -map 1:a:0 -map 2:a:0 -map 3:a:0 -map 4:s:0 -c:v copy -c:a copy -c:s mov_text"}

        self.createContainer(streams)

        os.remove("cut.mp4")
        os.remove("original_video.mp4")
        os.remove("original_audio.%s" % self.acodec)
        os.remove("mono_audio.%s" % self.acodec)
        os.remove("lowBR_audio.%s" % self.acodec)

    def createStandardContainer(self):
        """
        Function that creates streams of video and audio of given file with given video and audio codec and execute
        createContainer of its streams
        """
        os.system("ffmpeg -ss %s -i %s -to %s -c copy cut.mp4" % (self.fromtime, self.filename, self.totime))
        os.system("ffmpeg -i %s -ss %s -to %s -c copy cut.mp4" % (self.filename, self.fromtime, self.totime))
        os.system("ffmpeg -i cut.mp4 -an -c:v %s original_video.mp4" % self.vcodec)
        os.system("ffmpeg -i cut.mp4 -vn -c:a %s original_audio.%s" % (self.acodec, self.acodec))

        streams = {
            "video": ["original_video.mp4"],
            "audio": ["original_audio.%s" % self.acodec],
            "subtitles": False,
            "command": "-map 0:v:0 -map 1:a:0"
        }

        self.createContainer(streams)

        os.remove("cut.mp4")
        os.remove("original_video.mp4")
        os.remove("original_audio.%s" % self.acodec)

    def compatibility(self):
        """
        Reads audio and video mp4 container and check the compatibility using the broadcast dictionary
        """
        video_codec = os.popen("ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of "
                               "default=noprint_wrappers=1:nokey=1 %s.mp4" % self.name).read()

        audio_codec = os.popen("ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of "
                               "default=noprint_wrappers=1:nokey=1 %s.mp4" % self.name).read()

        self.vcodec = str(video_codec)[:len(video_codec) - 1]
        self.acodec = str(audio_codec)[:len(audio_codec) - 1]

        if self.vcodec in self.broadcast["dtmb_video"] and self.acodec in self.broadcast["dtmb_audio"]:
            print("Compatible with DTMB\n")
            if self.vcodec in self.broadcast["dv3_video"] and self.acodec in self.broadcast["dv3_audio"]:
                print("Compatible with DV3\n")
                if self.vcodec in self.broadcast["isdb_video"] and self.acodec in self.broadcast["isdb_audio"]:
                    print("Compatible with ISDB and ATSC!\n")
        else:
            print("No broadcast compatibility")


def P3():
    BBB_multiAudio = Container("BBB_multiAudio")
    BBB_mpg_ac3 = Container("BBB_multiAudio", vcodec="mpeg4", acodec="ac3")
    BBB_avs_dra = Container("BBB_multiAudio", vcodec="avs", acodec="dra")
    BBB_multiAudio.createMultiAudioContainer()
    BBB_mpg_ac3.createStandardContainer()
    BBB_avs_dra.createStandardContainer()
    BBB_mpg_ac3.compatibility()
    BBB_avs_dra.compatibility()


if __name__ == '__main__':
    P3()
