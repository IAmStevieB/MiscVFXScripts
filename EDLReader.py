import TimecodeConverter as tcc
from collections import OrderedDict
import math, re, pprint

edlitems = {}
def GatherEDL(edl):
	if (str(edl).rsplit(".",1)[1]).lower() != "edl":
		print "File is not an edl. Plese supply a properly formatted edl..."
		return
	else:
		pass

	e = open(edl,'r')
	
	edlline = e.read().splitlines()
	try:
		title = str.strip(edlline[0].split("TITLE:",1)[1])
		edlitems["Title"] = title
	except:
		pass
	try:
		fcm = str.strip(edlline[1].split("FCM:",1)[1])
		edlitems["FCM"] = fcm
		if fcm == "NON-DROP FRAME":
			framerate = 24
		else:
			framerate = 24
	except:
		pass
	edlitems["Items"] = {}
	for a in edlline[2:]:
		try:
			if ">>>" in a:
				continue
			elif " BL " in a:
				continue
			else:
				if str.isdigit(a[0]) == True:
					items = a.split(" ")
					myitems = []
					itemsnum = 0
					for b in items:
						if bool(b.strip()) == True:
							myitems.append(str(b))
						itemsnum += 1
					itemnumber = str("%03d"%int(myitems[0]))
					presourcename = myitems[1]
					timein = myitems[4]
					timeout = myitems[5]
					recordin = myitems[6]
					recordout = myitems[7].strip("'\n'")
					edlitems["Items"][itemnumber] = {}
					try:
						tx = tcc.TimecodeToFrames(timein, int(framerate))
						ty = tcc.TimecodeToFrames(timeout, int(framerate))
						t = float(ty) - float(tx)
						rx = tcc.TimecodeToFrames(recordin, int(framerate))
						ry = tcc.TimecodeToFrames(recordout, int(framerate))
						r = float(ry) - float(rx)
						speed = (t/r)
						if int(speed) > 5:
							speed = 5

					except:
						pass
					edlitems["Items"][itemnumber]['TimeIn'] = timein
					edlitems["Items"][itemnumber]['TimeOut'] = timeout
					edlitems["Items"][itemnumber]['RecordIn'] = recordin
					edlitems["Items"][itemnumber]['RecordOut'] = recordout
					edlitems["Items"][itemnumber]["SOP"] = ""
					edlitems["Items"][itemnumber]["SAT"] = ""
					edlitems["Items"][itemnumber]["ClipName"] = ""
					try:
						edlitems["Items"][itemnumber]['Speed'] = str(speed)
					except:
						edlitems["Items"][itemnumber]['Speed'] = "1.00"
					edlitems["Items"][itemnumber]['Vari'] = "False"
					edlitems["Items"][itemnumber]['SourceReelName'] = presourcename

				elif "M2" in a or "TIMEWARP" in a:
					edlitems["Items"][itemnumber]["TIMEWARP"] = "TRUE"

				# elif "TM:" in a:
				# 	edlitems["Items"][itemnumber]['TM'] = "1"

				elif "SOP" in a:
					mysops = a.strip("*").replace("ASC_SOP","").strip()
					edlitems["Items"][itemnumber]['SOP'] = mysops

				elif "SAT" in a:
					mysat = a.strip("*").replace("ASC_SAT","").strip()
					edlitems["Items"][itemnumber]['SAT'] = mysat

				elif "*" in a:
					if "FROM CLIP NAME:" in a:
						clipname = str(a.split(":", 1)[1]).strip()
						if a.count("-") >= 2:
							fps01 = (str.strip(a.split("-",2)[2]))[:7]
							z = re.sub("[^0-9.]","",fps01)
							if "(" in fps01:
								x = (str(fps01[fps01.find("(")+1:fps01.find(")")]).replace(" ",""))
								y = re.sub("[^0-9.]","",x)
								try:
									fps = int(round(float(y)))
								except:
									fps = y
								if fps == '':
									fps = framerate
							else:
								fps = re.sub("[^0-9.]","",fps01)
								if fps == '':
									fps = framerate
						else:
							fps = "24"
						edlitems["Items"][itemnumber]['FPS'] = str(fps)
						edlitems["Items"][itemnumber]['ClipName'] = clipname

					elif "VFX:" in a:
						vfxname01 = (str(a.split("VFX:",1)[1]).strip()).split(" ",1)[0]
						
						if "." in vfxname01:
							vfxname02 = vfxname01.split(".",1)[0]
						else:
							vfxname02 = vfxname01

						vfxname_fix = vfxname02.split("+",1)[0].replace(" ", "_")

						if bool(re.findall(r'[0-9][0-9]X[0-9][0-9]', vfxname_fix)) == True:
							shotnum = re.findall(r'[0-9][0-9]X[0-9][0-9]', vfxname_fix)[0]
							shotnumfix = shotnum.replace("X","x")
							vfxname = vfxname_fix.replace(shotnum, shotnumfix)
						else:
							vfxname = vfxname_fix
							

						edlitems["Items"][itemnumber]['VFXName'] = vfxname
						try:
							descriptor = str(a.split("VFX: ",1)[1]).split(" ",1)[1]
							edlitems["Items"][itemnumber]['Description'] = descriptor.strip()
						except:
							edlitems["Items"][itemnumber]['Description'] = ""
						if "+" in vfxname01:
							elename = vfxname01.split("+",1)[1]
							edlitems["Items"][itemnumber]['ElementName'] = elename
						else:
							edlitems["Items"][itemnumber]['ElementName'] = ""

					elif "SOURCE" in a:
						sourcereelname = str.strip(a.split(":",1)[1])
						edlitems["Items"][itemnumber]['SourceReelName'] = sourcereelname
						try:
							blah = edlitems["Items"][itemnumber]['ElementName']
							bleh = edlitems["Items"][itemnumber]['Description']
						except:
							edlitems["Items"][itemnumber]['ElementName'] = ""
							edlitems["Items"][itemnumber]['Description'] = ""

					elif "MSEC_" in a:
						vfxnames01 = a.split(" ")
						vfxnames = []
						for i in vfxnames01:
							if i != "":
								vfxnames.append(i)
						try:
							vfxname = vfxnames[3].split("-")[0]
						except:
							vfxname = ""
						edlitems["Items"][itemnumber]['VFXName'] = vfxname

						try:
							elename = vfxnames[3].split("-")[1]
						except:
							elename = ""
						edlitems["Items"][itemnumber]['ElementName'] = elename

						try:
							descriptor = a.split(str(vfxname+"-"+elename),"1")[1].strip()
						except:
							descriptor = ""
						edlitems["Items"][itemnumber]['Description'] = descriptor

					else:
						pass

		except Exception as ex:
			print ex
			pass

	for x, y in edlitems.iteritems():
		if x == "Items":
			for a, b in y.iteritems():
				try:
					if "TIMEWARP" in b:
						if (float(b["Speed"])).is_integer() == False:
							n = float(b["Speed"])
							nx = str(n)
							nd = float(nx.split(".",1)[0] + ".10")
							print nd
							if n > nd:
								b["Speed"] = "5.00"
								b["Vari"] = "True"
							else:
								b["Speed"] = str(int(n))+".00"
						else:
							pass
						del b["TIMEWARP"]
					else:
						if (float(b["Speed"])).is_integer() == False:
							sp = int(math.ceil(float(b["Speed"])))
							b["Speed"] = str(int(sp))+".00"
						pass
					if "VFXName" not in b:
						b["VFXName"] = b["SourceReelName"].rsplit(".",1)[0]
					else:
						for c, d in b.iteritems():
							if c == "VFXName":
								if d == "":
									b["VFXName"] = b["SourceReelName"]
					if int(b["Speed"]) > 5:
						b["Speed"] = "5.00"

					# if "Speed" in b:
					# 	myspeed = b["Speed"]
					# 	myfps = b["FPS"]
					# 	if myspeed == "1.0":
					# 		b["Speed"] = str("%.2f"%(float(myfps)/framerate))
					# 	else:
					# 		b["Speed"] = str("%.2f"%float(myspeed))
					# else:
					# 	pass

				except:
					pass
	# edlitems01 = {}
	# for x, y in OrderedDict(sorted(edlitems.iteritems())).iteritems():
	# 	if x == "Items":
	# 		edlitems01["Items"] = {}
	# 		itemnum = 1
	# 		for a, b in OrderedDict(sorted(y.iteritems())).iteritems():
	# 			if "TM" not in b:
	# 				edlitems01["Items"][str("%03d"%itemnum)] = b
	# 				itemnum += 1
	# 	else:
	# 		edlitems01[x] = y

	e.close()
	return edlitems
