import streamlit as st
import openai
import os
from PIL import Image
import io

openai.api_key = "YOUR_API_KEY"

def analyze_image(image_data):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Summarize the data presented in this chart."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

st.title("Visual Chart Summarizer")

uploaded_file = st.file_uploader("Upload an image of a chart", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_column_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    image_data = buffered.getvalue()
    import base64
    image_data = base64.b64encode(image_data).decode('utf-8')

    summary = analyze_image(image_data)

    st.write("Summary:")
    st.write(summary)
