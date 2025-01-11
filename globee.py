from streamlit_globe import streamlit_globe

def calling_globe():
    pointsData = [
                {'lat': 28.7041, 'lng': 77.1025, 'size': 0.01, 'color': 'red'},  # Delhi
                {'lat': 19.0760, 'lng': 72.8777, 'size': 0.01, 'color': 'blue'},  # Mumbai
                {'lat': 13.0827, 'lng': 80.2707, 'size': 0.01, 'color': 'green'},  # Chennai
                {'lat': 22.5726, 'lng': 88.3639, 'size': 0.01, 'color': 'orange'},  # Kolkata
                {'lat': 12.9716, 'lng': 77.5946, 'size': 0.01, 'color': 'purple'},  # Bengaluru
                {'lat': 17.3850, 'lng': 78.4867, 'size': 0.01, 'color': 'yellow'},  # Hyderabad
                {'lat': 26.9124, 'lng': 75.7873, 'size': 0.01, 'color': 'pink'},  # Jaipur
                {'lat': 21.1702, 'lng': 72.8311, 'size': 0.01, 'color': 'cyan'},  # Surat
                {'lat': 18.5204, 'lng': 73.8567, 'size': 0.01, 'color': 'magenta'},  # Pune
                {'lat': 23.0225, 'lng': 72.5714, 'size': 0.01, 'color': 'lime'},  # Ahmedabad
                {'lat': 30.7333, 'lng': 76.7794, 'size': 0.01, 'color': 'teal'},  # Chandigarh
                {'lat': 11.0168, 'lng': 76.9558, 'size': 0.01, 'color': 'gold'},  # Coimbatore
                {'lat': 31.1048, 'lng': 77.1734, 'size': 0.01, 'color': 'brown'},  # Shimla
                {'lat': 25.5941, 'lng': 85.1376, 'size': 0.01, 'color': 'olive'},  # Patna
                {'lat': 19.9975, 'lng': 73.7898, 'size': 0.01, 'color': 'navy'},  # Nashik
                {'lat': 22.3072, 'lng': 73.1812, 'size': 0.01, 'color': 'violet'},  # Vadodara
                {'lat': 34.0837, 'lng': 74.7973, 'size': 0.01, 'color': 'coral'},  # Srinagar
                {'lat': 15.3173, 'lng': 75.7139, 'size': 0.01, 'color': 'maroon'},  # Hampi
                {'lat': 27.1767, 'lng': 78.0081, 'size': 0.01, 'color': 'crimson'},  # Agra
                {'lat': 24.5854, 'lng': 73.7125, 'size': 0.01, 'color': 'indigo'}   # Udaipur
            ]

            # Add labels with city name and AQI value
    labelsData = [
                {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'size': location['size'],
                    'color': location['color'],
                    'text': f"{name} (AQI: {location['size']:.2f})"
                } for location, name in zip(pointsData, [
                    'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bengaluru', 'Hyderabad', 'Jaipur', 'Surat', 'Pune', 'Ahmedabad',
                    'Chandigarh', 'Coimbatore', 'Shimla', 'Patna', 'Nashik', 'Vadodara', 'Srinagar', 'Hampi', 'Agra', 'Udaipur'
                ])
            ]

            # Render the globe
    streamlit_globe(pointsData=pointsData, labelsData=labelsData, daytime='day', width=600, height=480)