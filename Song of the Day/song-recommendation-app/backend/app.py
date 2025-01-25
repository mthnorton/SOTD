from flask import Flask, jsonify, request
from recommender import file_reader, most_similar_songs, song_info, combined_similarity

app = Flask(__name__)

# Load songs data
songs = file_reader('data/songs.csv')

@app.route('/api/recommendations', methods=['POST'])
def recommend_songs():
    song_data = request.json
    input_song_number = song_data['song_number']
    similar_songs = most_similar_songs(input_song_number, songs)
    return jsonify([song._asdict() for song in similar_songs])

@app.route('/api/song_info', methods=['POST'])
def get_song_info():
    song_data = request.json
    input_song_number = song_data['song_number']
    song_details = next((song for song in songs if song.number == input_song_number), None)
    if song_details:
        return jsonify(song_details._asdict())
    else:
        return jsonify({'error': 'Song not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)