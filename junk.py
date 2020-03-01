#def for returning dummy sql data
import jsonify

def getSqlData():
    f=open("recipe.txt", "r")
    fileContents=f.readlines()
    f.close()
    returnData=[]
    for line in fileContents:
        line=line.split(",")
        temp=[]
        temp.append(int(line[0]))
        temp.append(line[1].strip())
        temp.append(line[2].strip())
        returnData.append(temp)
    for item in returnData:
        #print(item)
        ""
    global returnDataLength
    returnDataLength=len(returnData)

    return returnData

temp=getSqlData()
print(jsonify(temp))