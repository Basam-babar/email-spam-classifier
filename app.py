from flask import Flask, render_template, request
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)

model = pickle.load(open('models/model.pkl', 'rb'))
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    # Keep only alphanumeric tokens
    text = [word for word in text if word.isalnum()]

    # Remove stopwords and punctuation
    text = [word for word in text if word not in stop_words and word not in string.punctuation]

    # Stem each word
    text = [ps.stem(word) for word in text]

    return " ".join(text)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    email_text = ""

    if request.method == 'POST':
        email_text = request.form['email_text']

        # Process the input
        transformed = transform_text(email_text)
        vectorized = vectorizer.transform([transformed])
        prediction = model.predict(vectorized)[0]
        probability = model.predict_proba(vectorized)[0]

        if prediction == 1:
            result = {
                'label': 'SPAM',
                'confidence': round(probability[1] * 100, 1),
                'color': 'red'
            }
        else:
            result = {
                'label': 'NOT SPAM',
                'confidence': round(probability[0] * 100, 1),
                'color': 'green'
            }

    return render_template('index.html', result=result, email_text=email_text)


if __name__ == '__main__':
    app.run(debug=True)