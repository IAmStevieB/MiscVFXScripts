ffprobe = "" ##Replace with your location of FFProbe
ffmpeg = "" ##Replace with your location of FFMpeg

import os, subprocess, re, sys

def TimecodeChange(timecode, oldframerate, newframerate):
    try:
        x = TimecodeToFrames(timecode,oldframerate)
        y = FramesToTimecode(x, newframerate)
        return y
    except:
        print("TimecodeToFrames Error: Given object needs to be in standard timecode format (00:00:00:00) and given framerate needs to be an integer")
        return

def TimecodeToFrames(timecode, framerate):
    try:
        a,b,c = timecode.split(":")
        if "." in str(c):
            cd = c.split(".")
            c = cd[0]
            d = "%02d"%(int(float(cd[1])/4.166667))
            framerate = 24
        else:
            cd = c.split(":")
            c = cd[0]
            d = cd[1]
        # print(a, b, c, d)
        frames = float(d) + (int(c)*float(framerate)) + (int(b)*(float(framerate)*60)) + (int(a)*(float(framerate)*3600))
        # print(int(round(frames)))
        return int(round(frames))
    except Exception as e:
        print("TimecodeToFrames Error: Given object needs to be in standard timecode format (00:00:00:00) and given framerate needs to be an integer")
        print(e)
        return (-1)

def FramesToTimecode(frames, framerate):
    try:
        hrs = "%02d"%(int(frames/framerate/60/60))
        mins = "%02d"%(int(frames/framerate/60%60))
        secs = "%02d"%(int(frames/framerate%60))
        frs = "%02d"%(round(frames%framerate))
        timecode = str(hrs) + ":" + str(mins) + ":" + str(secs) + ":" + str(frs)
        return timecode
    except:
        print("FramesToTimecode Error: Given object or framerate need to be integers")
        return False

def TimecodeMath(operation, timecodeX, frameratex, timecodeY, frameratey, framerate):
    try:
        x = int(TimecodeToFrames(timecodeX, frameratex))
        y = int(TimecodeToFrames(timecodeY,frameratey))
        # print x, y
        if str.lower(operation) == "add" or str.lower(operation) == "addition" or operation == "+":
            newframes = x + y
        elif str.lower(operation) == "subtract" or str.lower(operation) == "sub" or operation == "-":
            newframes = x - y
        else:
            print("Please give operation: 'add' ('+') or 'subtract' ('-') (In quotes)")
            return
        newtimecode = FramesToTimecode(newframes,framerate)
        return newtimecode
    except:
        print("TimecodeMath Error: Given objects need to be in standard timecode format (00:00:00:00) and given framerate needs to be an integer")
        return

def GetFrameCount(mov):
    try:
        command = [ ffmpeg,
                    '-i', mov,
                    '-vcodec', 'copy',
                    '-acodec', 'copy',
                    '-f', 'null', '-']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        frames = 0
        items=re.findall("frame.*$",err,re.MULTILINE)
        for x in items:
            mycount = -1
            y = x.split()
            for i in y:
                mycount += 1
                if i == "frame=":
                    frames = int(y[mycount + 1]) - 1
        return str(frames)
    except:
        print("GetFrameCount Error: Make sure that path to FFMpeg exists and given file is a proper .mov")
        return

def GetBeginTimecode(mov):
    try:
        command = [ffprobe, mov]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        # print out, err
        timecode01 = err.split("timecode",1)[1]
        timecode02 = timecode01.split(": ",1)[1]
        timecode = timecode02.split(" ",1)[0]
        return timecode.strip()
    except Exception as e:
        print(e)
        print("GetBeginTimecode Error: Make sure that path to FFProbe exists and given file is a proper .mov")

def GetEndTimecode(mov):
    try:
        totalframes = GetFrameCount(mov)
        begintimecode = GetBeginTimecode(mov)
        beginframes = TimecodeToFrames(begintimecode,24)
        endframes = int(beginframes) + int(totalframes) - 1
        endtimecode = FramesToTimecode(endframes,24)
        return endtimecode
    except:
        print("GetEndTimecode Error: Make sure that paths to FFMpeg and FFProbe exist and given file is a proper .mov")
        return

def ProbeFile(mov):
    try:
        command = [ffprobe, mov]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        probestring01 = err.split("Video: ",1)[1]

        r = re.compile(r'(?:[^,(]|\([^)]*\))+')
        probestring = r.findall(probestring01)
        codec = (probestring[0].split(" ",1)[0]).strip()
        colorspace = (probestring[1].split("(",1)[0]).strip()
        res = probestring[2].strip()
        fps = probestring01.split("fps",1)[0].rsplit(",",1)[1].strip()
        return codec,colorspace,res,fps
        
    except:
        print("ProbeFile: Make sure that path to FFProbe exists and given file is a proper .mov")
        return
