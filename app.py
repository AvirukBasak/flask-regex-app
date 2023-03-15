from flask import Flask, request, render_template
import re

app = Flask(__name__)

def gen_response(resp, rgx, inp, rgxerr, inperr):
    return render_template('form.html',
        response      = resp,
        regex_val     = rgx,
        inputstr_val  = inp,
        regex_ierr    = rgxerr,
        inputstr_ierr = inperr
    )


# function to insert a string
def insert_str(s, i, ns):
    return s[:i] + ns + s[i:]


@app.route('/')
def index():
    response = False
    regex_val = ''
    inputstr_val = ''
    regex_ierr = ''
    inputstr_ierr = ''
    return gen_response(
        response,
        regex_val,
        inputstr_val,
        regex_ierr,
        inputstr_ierr
    )


@app.route('/parse', methods=['POST'])
def parse():
    response = False
    regex_val = ''
    inputstr_val = ''
    regex_ierr = ''
    inputstr_ierr = ''
    # function to evaluate parameters
    def evaluate_params():
        nonlocal response, regex_val, inputstr_val, regex_ierr, inputstr_ierr
        # get form data
        regex_val = request.form['regex'].strip() if 'regex' in request.form else False
        inputstr_val = request.form['inputstr'].strip() if 'inputstr' in request.form else False
        errflag = False
        # validate input
        if not regex_val or len(regex_val) == 0:
            regex_ierr = 'Malformed regex'
            errflag = True
        if not inputstr_val or len(inputstr_val) == 0:
            inputstr_ierr = 'Malformed input'
            errflag = True
        # return on error
        if errflag: return False
        # sanitize input
        regex_val = regex_val.replace(">", "&gt;")
        regex_val = regex_val.replace("<", "&lt;")
        inputstr_val = inputstr_val.replace(">", "&gt;")
        inputstr_val = inputstr_val.replace("<", "&lt;")
        return True
    # eval params and match pattern
    if not evaluate_params():
        return gen_response(
            response,
            regex_val,
            inputstr_val,
            regex_ierr,
            inputstr_ierr
        )
    # regex matching code
    try:
        matches = re.finditer(regex_val, inputstr_val)
    except Exception as e:
        regex_ierr = 'regex: %s' % e
        return gen_response(
            response,
            regex_val,
            inputstr_val,
            regex_ierr,
            inputstr_ierr
        )
    response = inputstr_val
    TAGOPEN = "<font class=\"ptrn-mark\">"
    TAGCLOSE = "</font>"
    for m in reversed(list(matches)):
        l, u = m.span()
        response = insert_str(response, u, TAGCLOSE)
        response = insert_str(response, l, TAGOPEN)
    return gen_response(
        response,
        regex_val,
        inputstr_val,
        regex_ierr,
        inputstr_ierr
    )


if __name__ == '__main__':
    app.run(debug=True)
