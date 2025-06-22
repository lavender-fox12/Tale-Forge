import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS 

app = Flask(__name__, static_folder='..frontend/build', static_url_path='/')
CORS(app) # enable CORS for developement and remove/configure for production if needed

# Define the paths for actual story links
STORY_LINKS_DIR = os.path.join(os.path.dirname(__file__), '../docs/story_links')

# --- API Endpoint to get the story links
@app.route('/api/stories', methods=['GET'])
def get_stories():
    """
    Reads story details (title, description, link) from text files in the 'docs/story_links' directory. Each file is expected to have the description on the first line and the URL on teh seconf line.
    """
    stories = []
    try:
        # Ensure the directory exists 
        if not os.path.exists(STORY_LINKS_DIR):
            print(f"Warning: Story links directory not found at {STORY_LINKS_DIR}")
            return jsonify({"error": "Story links directory not found"}), 404
            for filename in os.listdir(STORY_LINKS_DIR):
                if filename.endswith(".txt"):
                    filepath = os.path.join(STORY_LINKS_DIR, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            if len(lines) >= 2:
                                description = lines[0].strip()
                                link = lines[1].strip()
                                # Generate a cutesy and nice title from the filename like storu_1.txt becomes Story 1
                                title = filename.replace('_', '').replace('.txt', '').capitalize()
                                stories.append({
                                    'id': filename.replace('.txt', ''), 
                                    'title': title, 
                                    'description': description,
                                    'link': link
                                })
                                else:
                                    print(f"Warning: Skipping {filename} - not enough lines (expected 2: description, link)")
                    except Exception as e:
                        print(f"Error reading file {filepath}: {e}")  
    except Exception as e:
        print(f"Error listing story files: {e}")        
        return jsonify({"error": f"Failed to retrieve stories: {e}"}), 500
    #stories are sorted by title to be organized
    stories.sort(key=lamda x: x['title'])
    return jsonify(stories)

# --- Serve the Frontend Static Files ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serves the static files (HTML, CSS, JS) from the React build directory. If a file is not found, it serves index.html, allowing React Router to handle client-side routing (though for this app and it's a single page).
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')  

if __name__ == '__main__':
    # port 5000
    app.run(debug=True) # debug=True enables auto reloading and better error messages
          