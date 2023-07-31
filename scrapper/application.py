from flask import Flask
from flask import Flask,request,render_template,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

application = Flask(__name__)
app = application

@app.route("/",methods = ["GET"])
def home_page():
    return render_template("index.html")
    


@app.route("/review",methods = ["GET","POST"])
def hello():
    if request.method == "POST":
        try :
            reviews = []
            surl = "https://www.flipkart.com/search?q="
            search_word = request.form['content'].replace(" ","")
            flipkart_surl = surl+search_word
            uclient = uReq(flipkart_surl)
            flipkart_page = uclient.read()
            flipkart_html = bs(flipkart_page,"html.parser")
            bigboxes = flipkart_html.find_all("div",{"class":"_2kHMtA"})
            box = bigboxes[0]
            productlink = "https://www.flipkart.com" + box.a['href']
            product_req = requests.get(productlink)
            product_html = bs(product_req.text,"html.parser")
            comment_box = product_html.find_all("div",{"class":"_16PBlm"})

            file_name = search_word + ".csv"
            fw = open(file_name ,"w+")
            header = "Product, customer name, rating , heading, comment /n"
            fw.write(header)
            for i in comment_box[0 :10]:
                try :
                    name = i.div.div.find_all("p" ,{"class" : "_2sc7ZR _2V5EHH"})[0].text
                except:
                    name = "No Name"
                try:
                    rating  = i.div.div.div.div.text
                except:
                    rating = "No Rating"
                try:
                    comment_head = i.div.div.div.p.text
                except:
                    comment_head = "No Heading"
                try:
        
                    comment  = i.div.div.find_all("div" ,{"class" : ""})[0].div.text
                except:
                    comment = "No Comment"
                mydict = {"Product":search_word,"Name": name,"Rating":rating,"CommentHead":comment_head,"Comment":comment}
                reviews.append(mydict)
            return render_template("result.html",reviews = reviews[0: (len(reviews)-1)])
        except Exception as e:
            print(e)
    else:
        return render_template("index.html")


if __name__=="__main__":
    app.run(host="0.0.0.0",port =5002)
