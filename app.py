import openai
import os
from time import sleep
from progress.bar import ChargingBar
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv



app = Flask(__name__, static_folder='static')

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route("/", methods=["GET", "POST"])
def index():
    keywords = []  

    if request.method == "POST":
        user_input = request.form['job_role']
        prompt = f"Keywords to add to a {user_input} resume to get past the ATS."

        try:
        
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",  
                messages=[{"role": "user", "content": prompt}]
            )

            
            with ChargingBar("Gathering results...") as bar:
                for i in range(110):  
                    sleep(0.02)
                    bar.next()

    
            if "choices" in completion and len(completion["choices"]) > 0:
                response_content = completion["choices"][0].get("message", {}).get("content", "No content available")
                if response_content:
                    keywords = response_content.splitlines()
                else:
                    keywords = ["Sorry no response available"]
            else:
                keywords = ["Sorry no response available"]
        
        except Exception as e:
            print(f"Error occurred: {e}")
            keywords = ["An error occurred while processing your request"]

        return render_template("index.html", job_role=user_input, response=keywords)
    print(keywords)
    return render_template("index.html", job_role=None, response=[])

if __name__ == "__main__":
    app.run(debug=True)
