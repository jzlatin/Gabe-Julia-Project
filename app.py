from flask import Flask, render_template, request
import re
import string

app = Flask(__name__, template_folder='templates')

mf = 'static/masculinewords.txt'
ff = 'static/femininewords.txt'


def clean_word_list(reviews):
    "used to remove punctuation and seperates a string into seperate words and converting it to a list of words"
    res = re.sub('[' + string.punctuation + ']', '', reviews).split()

    return res


def file_to_list(txtfile):
    """return a list of words, from txt files containing masculine and feminine words"""
    words = []
    with open(txtfile) as f:
        for line in f.readlines():
            words.append(line.strip())
    return words


def detectfeminine(input, feminine):
    """Checks if there are feminine words in the user input."""
    length = len(feminine)
    list = []
    for i in range(length):
        if feminine[i] in input:
            list.append(feminine[i])
    return list


def detectmasculine(input, masculine):
    """Checks if there are masculine words in the user input."""
    length = len(masculine)
    list = []
    for i in range(length):
        if masculine[i] in input:
            list.append(masculine[i])

    return list


def checkoverall(mas, fem):
    """Checks for the masculine and feminine words."""
    if len(mas) == len(fem):
        return 1
    elif len(mas) > len(fem):
        return 2
    else:
        return 3


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        # Render the form to get input.
        return render_template('index.html')

    if request.method == 'POST':
        user_input = request.form.get('getdata')

        user_input = clean_word_list(user_input)

        masculine_file = file_to_list(mf)
        feminine_file = file_to_list(ff)

        print("Here are the list of feminine words:")
        print(detectfeminine(user_input, feminine_file))
        print("Here are the list of masculine words:")
        print(detectmasculine(user_input, masculine_file))

        overall = checkoverall(detectmasculine(user_input, masculine_file), detectfeminine(user_input, feminine_file))

        if overall == 1:
            temp = "This job description is gender neutral. There are an equal amount of masculine and feminine " \
                   "keywords in this job description. "
        elif overall == 2:
            temp = "There are more masculine keywords than feminine keywords " \
                   "in this job description. "

        elif overall == 3:
            temp = "There are more feminine keywords than masculine keywords " \
                   "in this job description. "

        ## Return our inputs, list if inputs, and prediction message back to index.html
        return render_template('index.html',
                               returned_pred=temp,
                               feminine= detectfeminine(user_input, feminine_file),
                               masculine= detectmasculine(user_input, masculine_file)
                               )


if __name__ == '__main__':
    app.run(debug=True)
