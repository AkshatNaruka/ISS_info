import json
import urllib.request
import time
import webbrowser
import geocoder
import streamlit as st
import folium
import streamlit.components.v1 as components

def fetch_iss_data():
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    st.write(f"There are currently {result['number']} astronauts on the ISS:")
    people = result["people"]
    for p in people:
        st.write(f"{p['name']} - on board")

    # Print user's current lat/long
    g = geocoder.ip('me')
    st.write(f"\nYour current lat/long is: {g.latlng}")

def display_iss_location():
    m = folium.Map(location=[0, 0], zoom_start=2)  # Initialize map with a default location

    # Create a text element to display ISS location dynamically
    iss_location_text = st.empty()

    while True:
        url = "http://api.open-notify.org/iss-now.json"
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())

        location = result["iss_position"]
        lat = float(location['latitude'])
        lon = float(location['longitude'])

        # Update the text dynamically
        iss_location_text.text(f"ISS Current Location: Latitude {lat}, Longitude {lon}")

        # Add ISS marker to the map
        folium.Marker([lat, lon], popup='ISS').add_to(m)

        # Convert the folium map to HTML
        m.save("index.html")

        # Rerun the script to update the Streamlit app
        st.experimental_rerun()

        # Refresh every 5 seconds
        time.sleep(5)

def isslocation():
    # Use components.iframe to embed the HTML file directly
    components.iframe("index.html", width=800, height=600)

    if st.button('Open Browser'):
        webbrowser.open_new_tab("index.html")

def main():
    st.title("ISS Tracker App")
    fetch_iss_data()

    # Run display_iss_location in a separate thread to allow dynamic updates
    display_iss_location()

    isslocation()

if __name__ == "__main__":
    main()
