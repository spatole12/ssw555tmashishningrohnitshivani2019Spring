import os,sys
import datetime
from prettytable import PrettyTable
filename="test01.ged"

ind={}
family={}

def normalize_gedcom(filename, ind, family):
    ged=open(filename,'r')
    a=ged.read()
    b=a.split("\n")
    #print(b)
    c=[]
    finalize=[]
    check={'0':["HEAD","NOTE","TRLR","INDI","FAM"],
    '1':["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV",],
    '2':["DATE"]}

    for i in range(0,len(b)):
        if b[i]=="":
            c.append(["","",""])
        else:
            space=b[i][2:].find(" ")
            #print(space)
            if space==-1:
                #print(b[i])
                #print("no space")
                c.append([b[i][0],b[i][2:],""])
            else:
                if b[i][space+3:].isspace():
                    #print(b[i])
                    #print("spaces removed")
                    c.append([b[i][0],b[i][2:2+space],""])
                else:
                    c.append([b[i][0],b[i][2:2+space],b[i][space+3:]])
    #print(c)

    for i in range(0,len(c)):
        if(c[i][0]=="" and c[i][1]=="" and c[i][2]==""):
            temporary="temporary"#used as a place holder
        else:
            #print("-->"+b[i])
            if c[i][0]=='0':
                if (c[i][1] in check[c[i][0]]) and (c[i][1]=="HEAD" or c[i][1]=="TRLR" or c[i][1]=="NOTE"):
                    if (c[i][1]=="HEAD" or c[i][1]=="TRLR") and (c[i][2]==""):
                        #print("valid\n")
                        #print("<--"+c[i][0]+"|"+c[i][1]+"|Y"+c[i][2]+"\n")
                        finalize.append(c[i])
                    elif c[i][1]=="NOTE" and c[i][2]!="":
                        #print("valid\n")
                        #print("<--"+c[i][0]+"|"+c[i][1]+"|Y|"+c[i][2]+"\n")
                        finalize.append(c[i])
                elif (c[i][2] in check[c[i][0]]) and (c[i][2]=="INDI" or c[i][2]=="FAM"):
                    #print("valid\n")
                    #print("<--"+c[i][0]+"|"+c[i][2]+"|Y|"+c[i][1]+"\n")
                    temp=[c[i][0],c[i][2],c[i][1]]
                    finalize.append(temp)
            elif (c[i][0]=='1') and (c[i][1] in check[c[i][0]]):
                if (c[i][1]=="BIRT" or c[i][1]=="DEAT" or c[i][1]=="MARR" or c[i][1]=="DIV" ) and (c[i][2]==""):
                    #print("valid\n")
                    #print("<--"+c[i][0]+"|"+c[i][1]+"|Y"+c[i][2]+"\n")
                    finalize.append(c[i])
                elif (c[i][1]!="BIRT" or c[i][1]!="DEAT" or c[i][1]!="MARR" or c[i][1]!="DIV" ):
                    if (c[i][1]=="SEX"):
                        if (c[i][2]=='M' or c[i][2]=='F'):
                            #print("valid\n")
                            #print("<--"+c[i][0]+"|"+c[i][1]+"|Y|"+c[i][2]+"\n")
                            finalize.append(c[i])
                    else:
                        #print("valid\n")
                        #print("<--"+c[i][0]+"|"+c[i][1]+"|Y|"+c[i][2]+"\n")
                        finalize.append(c[i])
            elif (c[i][0]=='2') and (c[i][1] in check[c[i][0]]):
                #print("valid\n")
                #print("<--"+c[i][0]+"|"+c[i][1]+"|Y|"+c[i][2]+"\n")
                finalize.append(c[i])
    # print(finalize)
    i=0
    while i<len(finalize):
        if finalize[i][0]=="0" and finalize[i][1]=="INDI":
            ind[finalize[i][2]]={}
            j=i+1
            while not(finalize[j][0]=="0" and (finalize[j][1]=="INDI" or finalize[j][1]=="FAM")) :
                if finalize[j][0]=='1' and (finalize[j][1] in check[finalize[j][0]]):
                    if (finalize[j][1]=="BIRT" or finalize[j][1]=="DEAT"):
                        ind[finalize[i][2]][finalize[j][1]+"_"+finalize[j+1][1]]=finalize[j+1][2]
                        #print(ind)
                        j=j+2
                    elif (finalize[j][1]=="FAMC" or finalize[j][1]=="FAMS"):
                        if finalize[j][1] in ind[finalize[i][2]]:
                            ind[finalize[i][2]][finalize[j][1]].append(finalize[j][2])
                        else:
                            ind[finalize[i][2]][finalize[j][1]]=[]
                            ind[finalize[i][2]][finalize[j][1]].append(finalize[j][2])
                        j=j+1
                    else:
                        ind[finalize[i][2]][finalize[j][1]]=finalize[j][2]
                        #print(ind)
                        j=j+1
                else:
                    j=j+1
                    if(j>=len(finalize)):
                        break
            if not("DEAT_DATE" in ind[finalize[i][2]]):
                ind[finalize[i][2]]["DEAT_DATE"]="NA"
                ind[finalize[i][2]]["ALIVE"]="True"
                dea_date=datetime.datetime.now()
            else:
                dea_date=datetime.datetime.strptime(ind[finalize[i][2]]["DEAT_DATE"],'%d %b %Y')
                ind[finalize[i][2]]["DEAT_DATE"]=dea_date.strftime('%Y-%m-%d')
                ind[finalize[i][2]]["ALIVE"]="False"

            if not("BIRT_DATE" in ind[finalize[i][2]]):
                ind[finalize[i][2]]["BIRT_DATE"]="NA"
                ind[finalize[i][2]]["AGE"]="NA"
            else:
                con_date=datetime.datetime.strptime(ind[finalize[i][2]]["BIRT_DATE"],'%d %b %Y')
                ind[finalize[i][2]]["BIRT_DATE"]=con_date.strftime('%Y-%m-%d')
                ind[finalize[i][2]]["AGE"]=int(((dea_date)-(con_date)).days/365)
            
            if not("FAMC" in ind[finalize[i][2]]):
                ind[finalize[i][2]]["FAMC"]="None"

            if not("FAMS" in ind[finalize[i][2]]):
                ind[finalize[i][2]]["FAMS"]="NA"

            i=j
        elif finalize[i][0]=="0" and finalize[i][1]=="FAM":
            family[finalize[i][2]]={}
            j=i+1
            while not(finalize[j][0]=="0" and (finalize[j][1]=="INDI" or finalize[j][1]=="FAM")):
                if finalize[j][0]=='1' and (finalize[j][1] in check[finalize[j][0]]):
                    if (finalize[j][1]=="MARR" or finalize[j][1]=="DIV"):
                        family[finalize[i][2]][finalize[j][1]+"_"+finalize[j+1][1]]=finalize[j+1][2]
                        #print(family)
                        j=j+2
                    elif (finalize[j][1]=="CHIL"):
                        if finalize[j][1] in family[finalize[i][2]]:
                            family[finalize[i][2]][finalize[j][1]].append(finalize[j][2])
                        else:
                            family[finalize[i][2]][finalize[j][1]]=[]
                            family[finalize[i][2]][finalize[j][1]].append(finalize[j][2])
                        j=j+1
                    else:
                        family[finalize[i][2]][finalize[j][1]]=finalize[j][2]
                        #print(family)
                        j=j+1
                else:
                    j=j+1
                    if(j>=len(finalize)):
                        break
            if not("MARR_DATE" in family[finalize[i][2]]):
                family[finalize[i][2]]["MARR_DATE"]="NA"
            else:
                con_date=datetime.datetime.strptime(family[finalize[i][2]]["MARR_DATE"],'%d %b %Y')
                family[finalize[i][2]]["MARR_DATE"]=con_date.strftime('%Y-%m-%d')
            if not("DIV_DATE" in family[finalize[i][2]]):
                family[finalize[i][2]]["DIV_DATE"]="NA"
            else:
                con_date=datetime.datetime.strptime(family[finalize[i][2]]["DIV_DATE"],'%d %b %Y')
                family[finalize[i][2]]["DIV_DATE"]=con_date.strftime('%Y-%m-%d')
            i=j
        else:
            i=i+1

def print_gedcom(ind, family):
    indi = PrettyTable()
    indi.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    fam = PrettyTable()
    fam.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    for key, values in ind.items():
        arr = list()
        
        arr.append(key)
        if values.__contains__("NAME"):
            arr.append (ind[key]["NAME"])
        if values.__contains__("SEX"):
            arr.append (ind[key]["SEX"])
        if values.__contains__("BIRT_DATE"):
            arr.append (ind[key]["BIRT_DATE"])
        if values.__contains__("AGE"):
            arr.append (ind[key]["AGE"])
        if values.__contains__("ALIVE"):
            arr.append (ind[key]["ALIVE"])
        if values.__contains__("DEAT_DATE"):
            arr.append (ind[key]["DEAT_DATE"])
        
        if values.__contains__("FAMC"):
            arr.append (ind[key]["FAMC"])
        if values.__contains__("FAMS"):
            arr.append (ind[key]["FAMS"])
        indi.add_row(arr)

    for key, values  in family.items():
        arr = list()
        husID = ""
        wifeID = ""
        arr.append(key)
        if values.__contains__("MARR_DATE"):
            arr.append (family[key]["MARR_DATE"])
        if values.__contains__("DIV_DATE"):
            arr.append (family[key]["DIV_DATE"])
        if values.__contains__("HUSB"):
            arr.append (family[key]["HUSB"])
            husID = family[key]["HUSB"]
        arr.append(ind[husID]["NAME"])
        if values.__contains__("WIFE"):
            arr.append (family[key]["WIFE"])
            wifeID = family[key]["WIFE"]
        arr.append(ind[wifeID]["NAME"])
        if values.__contains__("CHIL"):
            arr.append (family[key]["CHIL"])
        fam.add_row(arr)
    #print(arr)

    print("Individuals")
    print(indi)
    print("Family")
    print(fam)

def us01_date_b4_now(ind, family):
    for key, values in ind.items():
        if (values.__contains__("BIRT_DATE") and ind[key]["BIRT_DATE"] != "NA"):
            isB4Now = us01_tsk01_is_b4_now(ind[key]["BIRT_DATE"])
            if (isB4Now == False):
                print('Error US01: Birth date of', ind[key]["NAME"], '(', key ,') occurs after current date.')
        if (values.__contains__("DEAT_DATE") and ind[key]["DEAT_DATE"] != "NA"):
            isB4Now = us01_tsk01_is_b4_now(ind[key]["DEAT_DATE"])
            if (isB4Now == False):
                print('Error US01: Death date of', ind[key]["NAME"], '(', key ,') occurs after current date.')

    for key, values in family.items():
        if (values.__contains__("MARR_DATE") and family[key]["MARR_DATE"] != "NA"):
            isB4Now = us01_tsk01_is_b4_now(family[key]["MARR_DATE"])
            if (isB4Now == False):
                husID = family[key]["HUSB"]
                wifeID = family[key]["WIFE"]
                print('Error US01: Marriage date of ', ind[husID]["NAME"],'(', husID, ') and', ind[wifeID]["NAME"],'(', wifeID,') in Family (', key,') occurs after current date.')
        if (values.__contains__("DIV_DATE") and family[key]["DIV_DATE"] != "NA"):
            isB4Now = us01_tsk01_is_b4_now(family[key]["DIV_DATE"])
            if (isB4Now == False):
                husID = family[key]["HUSB"]
                wifeID = family[key]["WIFE"]
                print('Error US01: Divorce date of ', ind[husID]["NAME"],'(', husID, ') and', ind[wifeID]["NAME"],'(', wifeID,') in Family (', key,') occurs after current date.')

def us01_tsk01_is_b4_now(dateString):
    if(dateString == "NA"):
        return True
    else:
        nowDate = datetime.datetime.now()
        subjectDate = datetime.datetime.strptime(dateString, '%Y-%m-%d')
        if(subjectDate < nowDate):
            return True
        else:
            return False

normalize_gedcom(filename, ind, family)
print_gedcom(ind, family)
us01_date_b4_now(ind, family)