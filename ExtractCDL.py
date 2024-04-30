import EDLReader as edlr
import sys
from collections import OrderedDict


def ExtractCDL(myedl):
    newedlitems = OrderedDict(sorted((edlr.GatherEDL(myedl)).iteritems()))
    pprint.pprint(newedlitems)
    for x,y in newedlitems.iteritems():
        if x == "Items":
            for a, b in y.iteritems():
                givenitemnumber = a
                try:
                    sop = str(newedlitems["Items"][str(givenitemnumber)]["SOP"])
                    sat = str(newedlitems["Items"][str(givenitemnumber)]["SAT"])
                except:
                    sop = ""
                    sat = ""
                soplist = sop.split(")")

            mycdlshotfile = myedl.rsplit("\\",1)[0] + "\\" + str(a) + ".cdl"
            try:
                with open(mycdlshotfile,'w') as cdls:
                    cdls.write('<?xml version="1.0" ?>\n')
                    cdls.write('<ColorCorrection>\n')
                    cdls.write('   <SOPNode>\n')
                    try:
                        cdls.write('      <Slope>\n')
                        cdls.write('         ' + str(soplist[0].strip("(")) + '\n')
                        cdls.write('      </Slope>\n')
                        cdls.write('      <Offset>\n')
                        cdls.write('         ' + str(soplist[1].strip("(")) + '\n')
                        cdls.write('      </Offset>\n')
                        cdls.write('      <Power>\n')
                        cdls.write('         ' + str(soplist[2].strip("(")) + '\n')
                        cdls.write('      </Power>\n')
                    except:
                        pass
                    cdls.write('   </SOPNode>\n')
                    cdls.write('   <SatNode>\n')
                    try:
                        cdls.write('      <Saturation>\n')
                        cdls.write('         ' + str(sat) + '\n')
                        cdls.write('      </Saturation>\n')
                    except:
                        pass
                    cdls.write('   </SatNode>\n')
                    cdls.write('</ColorCorrection>')
                    cdls.close()
            except:
                pass

ExtractCDL(sys.argv[1])