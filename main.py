from azuresentiment import analyze_sentiment
import streamlit as st
from azuresummarizer import generate_summary

st.set_page_config(page_title="SummarizeHub", page_icon="📝", layout="centered")

# Header styling
def gradient_text(text, color1, color2):
    gradient_css = f"""
        background: -webkit-linear-gradient(left, {color1}, {color2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 42px;
    """
    return f'<span style="{gradient_css}">{text}</span>'

color1 = "red"
color2 = "blue"
text = "SummarizeHub"

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("logo.png", width=200)
styled_text = gradient_text(text, color1, color2)
st.write(f"<div style='text-align: center;'>{styled_text}</div>", unsafe_allow_html=True)

# Input box from user
text = st.text_area("Input Text For Summary", height=200)

# Checkbox to allow user to analyze sentiment
sentimenter = st.checkbox("Analyze Sentiment")


col1,  col2, col3 = st.columns(3)
if col1.button('SUMMARIZE'):
    #try:
        # To check if the input is filled
        if bool(text)== False:
            st.error("Please enter some text to summarize")
        else:
            st.snow()
            st.success('Results Generating below ....!', icon="✅")
            # To generate text file
            textfile = open("content.txt","w")
            textfile.write(text)
            textfile.close()

            # To generate sentiment
            if sentimenter:
                sentiment = analyze_sentiment("content.txt")
                st.markdown("<h3> Sentiment : </h3>" ,  unsafe_allow_html=True)
                st.write(sentiment)

            # To generate summarize
            summary=generate_summary("content.txt")
            st.markdown("<h2> Your Summary : </h2>" ,  unsafe_allow_html=True)        
            st.markdown("<h3> > Summary : </h3>" ,  unsafe_allow_html=True)
            st.write(summary)

# Adding a footer
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ by <a style='display: inline; text-align: center;' href="https://www.linkedin.com/in/harshavardhan-bajoria/" target="_blank">Harshavardhan Bajoria</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
