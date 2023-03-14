from flask import Flask, request, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    response = False
    regex_val = ''
    inputstr_val = ''

    regex_ierr = ''
    inputstr_ierr = ''

    return render_template('form.html',
        response=response,
        regex_val=regex_val,
        inputstr_val=inputstr_val,
        regex_ierr=regex_ierr,
        inputstr_ierr=inputstr_ierr
    )


@app.route('/parse', methods=['POST'])
def parse():
    response = False
    regex_val = ''
    inputstr_val = ''

    regex_ierr = ''
    inputstr_ierr = ''

    def evaluate_params():
        nonlocal response, regex_val, inputstr_val, regex_ierr, inputstr_ierr

        regex_val = request.form['regex'].strip() if 'regex' in request.form else False
        inputstr_val = request.form['inputstr'].strip() if 'inputstr' in request.form else False

        errflag = False

        if not regex_val or len(regex_val) == 0:
            regex_ierr = 'Malformed regex'
            errflag = True

        if not inputstr_val or len(inputstr_val) == 0:
            inputstr_ierr = 'Malformed input'
            errflag = True

        if errflag: return


    evaluate_params()

    return render_template('form.html',
        response=response,
        regex_val=regex_val,
        inputstr_val=inputstr_val,
        regex_ierr=regex_ierr,
        inputstr_ierr=inputstr_ierr
    )


if __name__ == '__main__':
    app.run(debug=True)
