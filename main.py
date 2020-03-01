from flask import Flask, flash, redirect, render_template, request, session, abort
import os,time,math
app = Flask(__name__)

scrollAmount=10
listStartIndex=0
listEndIndex=scrollAmount
returnData=[]
returnDataLength=0
pageNum=1
pageMax=1

#def for returning dummy sql data
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
    global pageMax
    pageMax=math.ceil(float(returnDataLength)/scrollAmount)


    return returnData

#if not session.get('logged_in'):   useful snippet.

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        global returnData
        returnData = getSqlData()
        trimmedData = returnData[listStartIndex:listEndIndex]
        return render_template('table.html', dataArray=trimmedData,pageNum=pageNum,pageMax=pageMax)
    else:
        return render_template('login.html',wrongLogin=1)

@app.route('/scrollPage',methods=['POST'])
def scrollPage():
    global scrollAmount
    global listStartIndex
    global listEndIndex
    global returnDataLength
    if((request.form['direction']=='forward')and(listEndIndex<returnDataLength)):
        listStartIndex = listStartIndex + scrollAmount
        listEndIndex = listEndIndex + scrollAmount
        global pageNum
        pageNum=pageNum+1

    if ((request.form['direction'] == 'backward')and(listStartIndex!=0)):
        listStartIndex = listStartIndex - scrollAmount
        listEndIndex = listEndIndex - scrollAmount
        global pageNum
        pageNum=pageNum-1

    #returnData = getSqlData()
    global returnData
    trimmedData = returnData[listStartIndex:listEndIndex]
    return render_template('table.html', dataArray=trimmedData,pageNum=pageNum,pageMax=pageMax)

@app.route('/refreshPage')
def refreshPage():
    if not session.get('logged_in'):
        return "NOT LOGGED IN"

    global returnData
    returnData = getSqlData()
    trimmedData = returnData[listStartIndex:listEndIndex]
    return render_template('table.html', dataArray=trimmedData,pageNum=pageNum,pageMax=pageMax)

@app.route('/postRefreshPage',methods=['POST'])
def postRefreshPage():
    global returnData
    returnData = getSqlData()
    trimmedData = returnData[listStartIndex:listEndIndex]
    return render_template('table.html', dataArray=trimmedData,pageNum=pageNum,pageMax=pageMax)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
    #getSqlData()