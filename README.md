# 🌦️ Weather Intelligence App

A modern weather dashboard built with **Python + Streamlit**, integrating real-time meteorological data and **LLM-powered insights via Ollama**.

The application allows users to search any city worldwide and receive:

- Current weather conditions
- Hourly temperature forecast
- Daily forecast
- Meteorological warnings
- AI-generated travel suggestions

<br><br>
---

# 📷 Application Preview

## Main Dashboard
![Dashboard](https://github.com/GuiCRG/weather_project/blob/main/assets/3.jpeg)

## City Search Example
![City Example](https://github.com/GuiCRG/weather_project/blob/main/assets/4.jpeg)

---



# 🚀 Features
- Real-time weather data  
- Hourly forecast visualization  
- 7-day forecast chart  
- Meteorological warning alerts  
- AI-generated suggestions using **Ollama LLM**  
- Smart city search with normalization  
- Clean and responsive UI
- Robust Error Handling



<br><br>


# 🧠 AI / LLM Integration

The application integrates with **Ollama** to generate contextual weather insights.

Examples of generated insights include:

- Interpreting weather conditions
- Providing contextual explanations
- Generating suggestions based on temperature, humidity, or weather alerts

This allows the application to move beyond raw weather data and provide **natural language insights**.
![LLM1](https://github.com/GuiCRG/weather_project/blob/main/assets/5.1.jpeg)
![LLM1](https://github.com/GuiCRG/weather_project/blob/main/assets/6.1.jpeg)

<br><br>





# 📊Data Source

- City data is based on the OpenWeather city list dataset, which contains thousands of cities worldwide with geographic coordinates.
- This dataset enables fast location lookup for weather queries.

  
<br><br>



  



# 🛠️Error Handling

- The project includes structured error handling to ensure reliability and maintainability.
- User-Friendly Errors
- Errors are displayed with clear and understandable messages in the Streamlit interface, avoiding raw exception traces for users.
- Graceful Failures
- External integrations such as:
- Weather API requests
   Local dataset loading
- LLM responses are protected with error handling to prevent application crashes.
- Maintainable Architecture
- Error handling is organized into logical layers:
    - UI layer (Streamlit interface)
    - Data / API layer
    - Utility functions
    - This separation improves maintainability and simplifies debugging.
    - Defensive Programming
-The application includes safeguards such as:
    - Try/except blocks for API calls
    - Validation of API responses
    - Verification of file paths
    - Controlled fallback behavior
    - Logging Ready

- The architecture is designed to allow easy integration with logging and monitoring systems in future versions.

<br><br>





# 🗂️ Project Structure

```
weather_project
│
├── App
│ └── web_app_weather.py # Main Streamlit application
│
├── tools
│ ├── init.py
│ └── functions.py # Utility and processing functions
│
├── data
│ └── city.list.json # Dataset with global cities
│
├── requirements.txt
└── README.md

```


<br><br>

---

# ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/weather-project.git
cd weather-project

python -m venv venv

Windows(venv\Scripts\activate)

Linux(source venv/bin/activate)

pip install -r requirements.txt

streamlit run App/web_app_weather.py

```


# 🔮 Future Improvements

Planned improvements include:

- Autocomplete city search

- Historical weather data visualization

- Interactive weather maps

- More advanced AI-generated weather insights

- Docker support for deployment

<br><br>


# Technologies Used

- Python
- Streamlit
- Pandas
- OpenWeather API
- Ollama (Local LLM)
- Ploty Express
- Dotenv
- Htlm
- Css


<br><br>



# Contributing

- Contributions are welcome.

- Fork the repository


<br><br>

#📄 License

``` This project is licensed under the MIT License. ```




