from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from flask import Flask, render_template
import io
import base64

app = Flask(__name__)

@app.route("/")
def root():
    # Set time period
    start = datetime(2022, 1, 1)
    end = datetime(2022, 12, 31)

    # Create Point for San Antonio, TX
    location = Point(29.4252, -98.4946, 28)

    # Get daily data for 2018
    data = Daily(location, start, end)
    data = data.fetch()

    # Plot line chart including average, minimum and maximum temperature
    plt.plot(data.index, data['tavg'], label='Average Temperature')
    plt.plot(data.index, data['tmin'], label='Minimum Temperature')
    plt.plot(data.index, data['tmax'], label='Maximum Temperature')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')

    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Encode the image in base64
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')

    return render_template("index.html", img_data=img_str)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
