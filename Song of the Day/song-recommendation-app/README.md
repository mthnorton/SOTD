# Song Recommendation App

This project is a song recommendation application that utilizes a Flask backend to provide song recommendations based on similarity metrics. The application reads song data from a CSV file and serves recommendations through a simple HTML frontend.

## Project Structure

```
song-recommendation-app
├── backend
│   ├── app.py               # Entry point for the Flask server
│   ├── recommender.py       # Contains recommendation logic
│   ├── requirements.txt      # Lists dependencies for the backend
│   └── data
│       └── songs.csv        # CSV file containing song data
├── frontend
│   ├── index.html           # Main HTML file for the frontend
│   ├── styles
│       └── style.css        # CSS styles for the frontend
│   └── scripts
│       └── app.js           # JavaScript for handling user interactions
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd song-recommendation-app
   ```

2. **Install backend dependencies:**
   Navigate to the `backend` directory and install the required packages:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the backend server:**
   Start the Flask server:
   ```
   python app.py
   ```

4. **Open the frontend:**
   Open `frontend/index.html` in your web browser to access the application.

## Usage

- Use the input fields in the frontend to select a song and receive recommendations based on similarity metrics.
- The backend processes the request and returns a list of recommended songs.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is open-source and available under the MIT License.