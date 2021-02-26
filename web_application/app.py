from utils import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 30

###################### Web ######################
@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        try:
            # open image
            file = Image.open(request.files['file'].stream)
            # remove alpha channel
            rgb_im = file.convert('RGB')
            rgb_im.save('file.jpg')
        # failure
        except:
            return redirect(request.url)

        result ,fin_img = detect(np.asarray(file))
        
        return render_template('result.html', img_name = fin_img) 
    cleanup()

    return render_template('index.html')

#########################API Requests###########################
@app.route('/api',methods=['POST'])
def upload_detect():
    if request.method == 'POST':
        try:
            file = Image.open(request.files['file'].stream)
            # remove alpha channel
            rgb_im = file.convert('RGB')
            rgb_im.save('file.jpg')
        except:
            pass

    result,fin_img = detect(np.asarray(file))
    return jsonify(result)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)