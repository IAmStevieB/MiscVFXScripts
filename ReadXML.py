from xml.etree import ElementTree as et
import os, re

imgmagik = "S:\\net_exe\\ImageMagik\\ImageMagick-6.8.9-Q16_static\\"
sslate = None ## Path to slate file

## (A) ReadXML: Converts XML to python dictionary for easy manipulation when generating Generation project.
def ReadXML(xml):
    z = 0
    totalcount = 0
    actualcount = 0

    ## (A-1) Load xml using element tree module and parse.
    print "Reading XML file: " + str(xml)
    xmlD = et.parse(xml)
    root = xmlD.getroot()
    fpathnum = int((sum(1 for i in xmlD.iter("ITEM"))))
    projdir = (xml.rsplit("\\",2)[0])
    
    print "XML successfully loaded."

    ## (A-2) Begin building dictionary.
    print "Reading in XML..."
    projdict = {}
    try:
        projtype = (xmlD.find("TYPE").text).upper()
        projdict["TYPE"] = projtype
    except:
        projdict["TYPE"] = "EPISODIC"
    
    try:
        resx = (xmlD.find("PROJECTWIDTH").text)
    except:
        resx = "1920"
    try:
        resy = (xmlD.find("PROJECTHEIGHT").text)
    except:
        resy = "1080"

    try:
        projdict["RESOLUTION"] = resx + "x" + resy
    except:
        projdict["RESOLUTION"] = "1920x1080"
    projdict["PROJNAME"] = "Null"

    LUTlist = []
    
    oktypes = ["plate","element","composite", "precomp", "animatic", "slapcomp"] ## For Muse, we wanted to only allow certain types of shots to be used in Generation. Generation is a bit buggy on some filetypes and this was one of the better ways to handle that.
    
    ## (A-2.1) Iter through items to get a quick count of total items for use later. Would be better to have a tag in the XML for total items that can be added on creation of XML, but if not or until available, this will suffice.
    for show in root.iter('SHOW'):
        for episode in show.iter('EPISODE'):
            for shot in episode:
                for item in shot:
                    actualcount += 1

    ## (A-2.2) Iter through Shows, Episodes, Shots, and Items to build dictionary.
    for show in root.iter('SHOW'):
        showname = (show.text).strip().replace(" ","_") ## Get rid of all white spaces for cleanliness.
        showname = re.sub('[^a-zA-Z0-9 \n\.]', '_', showname) ## This is actually better to catch for when creating the XML, but provided as a catch here just in case its not possible. 
                                                               # Generation DOES NOT like the use of special characters at all when dealing with item names in their .genproj file. So to make the document play nice, every special character
                                                               # is changed into an underscore (_). The only characters it likes is the pound(#) and at(@), but only when denoting img sequences and frames not starting at one(1) respectively.
                                                               # This is shown when building the .genproj file.
        projdict[showname] = {}
        print showname
        for episode in show.iter('EPISODE'):
            epname = (episode.text).strip().replace(" ","_")
            epname = re.sub('[^a-zA-Z0-9 \n\.]', '_', epname)
            projdict[showname][epname] = {}
            print epname
            for shot in episode:
                shotname = (shot.text).strip().replace(" ","_")
                shotname = re.sub('[^a-zA-Z0-9 \n\.]', '_', shotname)
                print shotname
                projdict[showname][epname][shotname] = {}

                items = sum(1 for item in shotname)

                itemcount = 0
                errorcount = 0
                itemerror = []

                if shotname.find("ITEM") == None:
                    print "No items to add. " + shot + " not added..."
                    continue
                else:
                    pass

                for item in shot:
                    fpath = item.find("FILEPATH").text
                    approvedtypes = ["Plate","Composite"] ## This can be changed. Muse prefers CDL information to only be applied to the shot types Plates and Compositions when viewing in Generation.
                    if os.path.isfile(fpath) == True:
                        filetype = fpath.rsplit(".",1)[1]
                        i = (item.text).strip()
                        i = re.sub('[^a-zA-Z0-9 \n\.]', '_', i)
                        try:
                            ## If itemnames look similar to the ones in the Muse Exmaple XML (example: 1-v0034298), this will make sure that its readable by Generation.
                            itemnum = i.split("_",1)[0]
                            itemnumstr = '{num:0{width}}'.format(num = int(itemnum), width = len(str(actualcount)))
                            itemname = str(itemnumstr) + "_" + i.split("_",1)[1]
                        except:
                            itemname = i
                        projdict[showname][epname][shotname][itemname] = {}

                        try: 
                            ## Shot type is used for various things, like to know which item should have a CDL applied or not.
                            shottype = item.find("TYPE").text
                            if shottype == None:
                                shottype = ""
                        except:
                            shottype = ""

                        ## Generation has a fairly slow and poor proxy system. Custom NProxies (network proxies) and LProxes (local proxies) are used instead with Muse_ProxyExchange to quickly change between original and proxy files.
                        try:
                            nproxy = (item.find("FILEPATH_NPROXY").text)
                        except:
                            nproxy = ""
                        # try:
                        #     if os.path.exists(nproxy) == True:
                        #         fpath = nproxy
                        #     else:
                        #         nproxy = ""
                        # except:
                        #     nproxy = ""

                        try:
                            lproxy = (item.find("FILEPATH_LPROXY").text)
                        except:
                            lproxy = ""
                        # try:
                        #     if os.path.exists(lproxy) == True:
                        #         fpath = lproxy
                        #     else:
                        #         lproxy = ""
                        # except:
                        #     lproxy = ""

                        ## Notes get added in the .genmeta files along with statuses, submitting user information, and other misc information.
                        try:
                            note = item.find("NOTE").text
                            if note == None:
                                note = ""
                        except:
                            note = ""
                        
                        try:   
                            status = item.find("STATUS").text
                            if status == None:
                                status = ""
                        except:
                            status = ""
                         
                        try:   
                            version = item.find("VERSION").text
                            if version == None:
                                version = ""
                        except:
                            version = ""
                            
                        ## Submitting artist of item.
                        try:
                            submittingartist = item.find("SUBMITTINGARTIST").text
                            if submittingartist == None:
                                submittingartist = ""
                        except:
                            submittingartist = ""
                           
                        ## All artists associated with the particular item.
                        try:
                            allartists = item.find("ALLARTISTS").text
                            if allartists == None:
                                allartists = ""
                        except:
                            allartists = ""
                            
                        try:
                            gridlocator = item.find("GRIDLOCATOR").text
                            if gridlocator == None:
                                gridlocator = ""
                        except:
                            gridlocator = ""

                        ## Length of item
                        try:
                            length = str(item.find("LENGTH").text)
                            if length == None:
                                length = str(50)
                        except:
                            length = "50"
                            
                        ## Muse pulls their own plates. This is so that we know where the original plate came from for current item.
                        try:
                            origreel = item.find("ORIGREELNAME").text   
                            if origreel == None:
                                origreel = ""
                        except:
                            origreel = ""
                            
                        ## Sequence item is in.
                        try:
                            sequence = item.find("SEQUENCE").text
                            if sequence == None:
                                sequence = "SEQUENCE"
                        except:
                            sequence = ""

                        ## CDL information to use on item if proper CDL is given. If not, then the default is used. Numbers generally do not need to be adjusted.
                        try:
                            cdlpath = item.find("CDL").text
                            if cdlpath == None:
                                cdlpath = ""
                        except:
                            cdlpath = ""

                        cdlinfo = {}
                        cdlinfo['SLOPE'] = {'RED': '1.0000', 'GREEN': '1.0000', 'BLUE': '1.0000'}
                        cdlinfo['OFFSET'] = {'RED': '0.0000', 'GREEN': '0.0000', 'BLUE': '0.0000'}
                        cdlinfo['POWER'] = {'RED': '1.0000', 'GREEN': '1.0000', 'BLUE': '1.0000'}
                        cdlinfo['SATURATION'] = '1.0000'
                        try:
                            if filetype.lower() != "exr":
                                if shottype in approvedtypes:
                                    if cdlpath != "":
                                        cdlinfo = ReadCDL(cdlpath)
                            else:
                                cdlinfo['POWER'] = {'RED': '0.4545', 'GREEN': '0.4545', 'BLUE': '0.4545'}

                        except:
                            pass

                        ## Information for which LUT to use for item if provided.
                        try:
                            lutpath = item.find("LUT").text
                            if lutpath == None:
                                lutpath = ""
                            else:
                                if lutpath not in LUTlist:
                                    LUTlist.append(lutpath)
                        except:
                            lutpath = ""

                        try:
                            shotwidth = item.find("WIDTH").text
                            if shotwidth == None:
                                shotwidth = "1920"
                        except:
                            shotwidth = "1920"

                        try:
                            shotheight = item.find("HEIGHT").text
                            if shotheight == None:
                                shotheight = "1080"
                        except:
                            shotheight = "1080"

                        try:
                            hhandle = item.find("HEADHANDLE").text
                            if hhandle == None:
                                hhandle = "0"
                        except:
                            hhandle = "0"

                        try:
                            thandle = item.find("TAILHANDLE").text
                            if thandle == None:
                                thandle = "0"
                        except:
                            thandle = "0"

                        ## Generation creates .genmeta files anytime an item is adjusted. This makes sure that that file gets bypassed and returns all the files in the directory of the original file.
                        listoffiles = []
                        try:
                            for i in os.listdir(fpath.rsplit("\\",1)[0]):
                                if os.path.isfile(fpath.rsplit("\\",1)[0] + "\\" + i) == True:
                                    if "genmeta" not in i:
                                        if i not in listoffiles:
                                            listoffiles.append(i)
                        except:
                            pass

                        ## Generation sometimes needs a framebuffer for the shot or item being submitted. This tries to get it.
                        findfb0 = os.path.basename(fpath).rsplit(".",1)[0]
                        for i in reversed(findfb0):
                            if i.isdigit() == False:
                                if i.isalpha() == False:
                                    fbbreak = i
                                    break
                        try:
                            fbuffer = len(findfb0.rsplit(fbbreak,1)[1])
                        except:
                            fbuffer = 1
                        
                        ## Gets the first and last frames of the submitted item.
                        try:
                            firstframe0 = re.findall("(\d{%s}?.)" % fbuffer + os.path.basename(listoffiles[0]).rsplit(".",1)[1],os.path.basename(listoffiles[0]))
                            firstframe = int(firstframe0[0].split(".",1)[0])
                        except:
                            firstframe = 1
                        
                        try:
                            lastframe0 = re.findall("(\d{%s}?.)" % fbuffer + os.path.basename(listoffiles[-1]).rsplit(".",1)[1],os.path.basename(listoffiles[-1]))
                            lastframe = int(lastframe0[0].split(".",1)[0])
                        except:
                            lastframe = 1

                        ## Add all information for the current item to the dictionary.
                        shotitem = projdict[showname][epname][shotname][itemname]
                        shotitem["FILEPATH"] = fpath
                        shotitem["FILEPATH_LPROXY"] = lproxy
                        shotitem["FILEPATH_NPROXY"] = nproxy
                        shotitem["NOTE"] = note
                        shotitem["STATUS"] = status
                        shotitem["VERSION"] = version
                        shotitem["SUBMITTINGARTIST"] = submittingartist
                        shotitem["ALLARTISTS"] = allartists
                        shotitem["GRIDLOCATOR"] = gridlocator
                        shotitem["LENGTH"] = length
                        shotitem["ORIGREEL"] = origreel
                        shotitem["SEQUENCE"] = sequence
                        shotitem["SHOTTYPE"] = shottype
                        shotitem["CDL_PATH"] = cdlpath
                        shotitem["CDL_INFO"] = cdlinfo
                        shotitem["LUT_PATH"] = lutpath
                        shotitem["EPISODE"] = epname
                        shotitem["SHOW"] = showname
                        shotitem["SHOTNAME"] = shotname
                        shotitem["INAME"] = str("_" + shotname + "_" + version + "_" + itemname + "_").replace("-","_")
                        shotitem["FIRSTFRAME"] = firstframe
                        shotitem["LASTFRAME"] = lastframe
                        shotitem["FRAMEBUFFER"] = fbuffer
                        if showname == "Teen_Wolf":
                            shotitem["INPUT_LUT"] = lutpath
                            shotitem["OUTPUT_LUT"] = ""
                        else:
                            shotitem["INPUT_LUT"] = ""
                            shotitem["OUTPUT_LUT"] = lutpath
                        shotitem["HEADHANDLE"] = hhandle
                        shotitem["TAILHANDLE"] = thandle
                        shotitem["SHOTWIDTH"] = shotwidth
                        shotitem["SHOTHEIGHT"] = shotheight

                        totalcount += 1
                        print "Read item: " + str(itemname)

                ## Sometimes, when dealing with many shots, its difficult to see which shots you're looking at when viewing in column view. This will try to create and insert a placeholder at the top of the column with the shotname on it for easy viewing and finding.
                # try:
                #     pholderdir = projdir + "\\_placeholders\\" + showname + "_" + epname
                #     if os.path.isdir(pholderdir) == False:
                #         os.makedirs(pholderdir)
                #     pholder = os.path.abspath(pholderdir + "\\" + showname + "_" + shotname + "_placeholder.jpg")
                #     if os.path.exists(pholder) == False:
                #         CreatePlaceholder(pholder)
                #     projdict[showname][epname][shotname]["PLACEHOLDER"] = pholder
                # except Exception as e:
                #     print e
                #     print "Could not create placeholders for current item."
                #     pass

    ## (A-3) Finish the dictionary.
    ## Total items successfully able to be read in XML.
    projdict["TOTAL_ITEMS"] = str(totalcount)
    ## Sometimes the XML will contain multiple shows, episodes, and shots that utilize different LUTs. This gathers a list of them to be used later.
    projdict["LUT_LIST"] = LUTlist
    print "\n"

    return projdict

def CreatePlaceholder(myfile): ## Creates placeholders. NOTE: Uses ImageMagik
    shot = os.path.basename(myfile).split("placeholder")[0]
    os.chdir(imgmagik)
    newplaceholder = myfile.rsplit("\\",1)[0] + "\\" + shot + "placeholder.jpg"
    ## 'sslate' refers to a custom blank slate for Img Magick to use. You could also just have ImgMagik create a black frame instead by changing the 'command'
    command = ('convert -size 1920x1080 canvas:black ' + sslate + ' -composite -pointsize 200 -fill white -annotate +100+790 "' + shot + '" ' + newplaceholder)
    os.system(command)
    return

def ReadCDL(cdlpath):
    cdlD = et.parse(cdlpath)
    cdlroot = cdlD.getroot()
    cdlinfo = {}
    for cc in cdlroot.iter("ColorCorrection"):
        for sopnode in cc.iter("SOPNode"):
            slope = sopnode.find("Slope").text.strip()
            cdlinfo["SLOPE"] = {'RED':slope.split(" ")[0], 'GREEN':slope.split(" ")[1], 'BLUE':slope.split(" ")[2]}
            offset = sopnode.find("Offset").text.strip()
            cdlinfo["OFFSET"] = {'RED':offset.split(" ")[0], 'GREEN':offset.split(" ")[1], 'BLUE':offset.split(" ")[2]}
            power = sopnode.find("Power").text.strip()
            cdlinfo["POWER"] = {'RED':power.split(" ")[0], 'GREEN':power.split(" ")[1], 'BLUE':power.split(" ")[2]}
        for satnode in cc.iter("SatNode"):
            sat = satnode.find("Saturation").text.strip()
            cdlinfo["SATURATION"] = sat
    return cdlinfo