from flask import Flask, request, render_template
import re

app = Flask(__name__)

def gen_response(resp, rgx, inp, rgxerr, inperr, count=-1):
    return render_template('form.html',
        response      = resp,
        regex_val     = rgx,
        inputstr_val  = inp,
        regex_ierr    = rgxerr,
        inputstr_ierr = inperr,
        matches_cnt   = count
    )


# function to insert a string
def insert_str(s, i, ns):
    return s[:i] + ns + s[i:]


@app.route('/')
def index():
    return gen_response(
        False,
        '',
        '',
        '',
        ''
    )


@app.route('/parse', methods=['POST'])
def parse():
    response = False
    regex_val = ''
    regex_flags = 0
    inputstr_val = ''
    regex_ierr = ''
    inputstr_ierr = ''
    # function to evaluate parameters
    def evaluate_params():
        nonlocal response
        nonlocal regex_val, regex_flags
        nonlocal inputstr_val
        nonlocal regex_ierr, inputstr_ierr
        # get form data
        regex_val = request.form['regex'].strip() if 'regex' in request.form else False
        inputstr_val = request.form['inputstr'].strip() if 'inputstr' in request.form else False
        for key in request.form:
            if 're.I' == key: regex_flags |= re.I
            if 're.M' == key: regex_flags |= re.M
            if 're.A' == key: regex_flags |= re.A
            if 're.S' == key: regex_flags |= re.S
            if 're.L' == key: regex_flags |= re.L
        errflag = False
        # validate input
        if not regex_val or len(regex_val) == 0:
            regex_ierr = 'regex: malformed input'
            errflag = True
        if not inputstr_val or len(inputstr_val) == 0:
            inputstr_ierr = 'text: malformed input'
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
        matches = re.finditer(regex_val, inputstr_val, regex_flags)
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
    matches = list(matches)
    TAGOPEN = "<font class=\"ptrn-mark\">"
    TAGCLOSE = "</font>"
    for m in reversed(matches):
        l, u = m.span()
        response = insert_str(response, u, TAGCLOSE)
        response = insert_str(response, l, TAGOPEN)
    return gen_response(
        response,
        regex_val,
        inputstr_val,
        regex_ierr,
        inputstr_ierr,
        len(matches)
    )


if __name__ == '__main__':
    app.run(debug=True)
