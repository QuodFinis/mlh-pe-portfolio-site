const mapContainer = document.getElementById('travel-map');

if (mapContainer) {
  const map = L.map('travel-map').setView([40.7128, -74.0060], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
  }).addTo(map);

  const locations = [
    { lat: 40.7128, lon: -74.0060, label: "New York City, NY" },
    { lat: 24.555059, lon: -81.779984, label: "Key West, FL" },
    { lat: 28.538336, lon: -81.379234, label: "Orlando, FL" },
    { lat: 27.964157, lon: -82.452606, label: "Tampa, FL" },
    { lat: 32.08111, lon: -81.09111, label: "Savannah, GA" },
    { lat: 36.779591, lon: -76.288376, label: "Chesapeake, VA" },
    { lat: 38.25278, lon: -75.12778, label: "Assateague Island, MD" },
    { lat: 38.89500, lon: -77.03639, label: "Washington, D.C." },
    { lat: 41.66278, lon: -77.82306, label: "Cherry Springs, PA" },
    { lat: 43.096214, lon: -79.037739, label: "Niagara Falls, NY" },
    { lat: 42.382167, lon: -76.899238, label: "Watkins Glen, NY" },
    { lat: 43.830569, lon: -73.926059, label: "Whiteface Mountain, NY" },
    { lat: 44.112222, lon: -73.923333, label: "Mt. Marcy, NY" },
    { lat: 43.212278, lon: -75.455440, label: "Rome, NY" },
    { lat: 41.763710, lon: -72.685093, label: "Hartford, CT" },
    { lat: 45.501690, lon: -73.567253, label: "Montreal, Canada" },
    { lat: 41.059021, lon: -71.952450, label: "Montauk, NY" },
    { lat: 6.2355, lon: -75.5906, label: "Guatapé, Colombia" },
    { lat: 4.7110, lon: -74.0721, label: "Bogotá, Colombia" },
    { lat: 6.2442, lon: -75.5812, label: "Medellín, Colombia" },
    { lat: 21.3891, lon: 39.8579, label: "Mecca, Saudi Arabia" },
    { lat: 24.5247, lon: 39.5692, label: "Medina, Saudi Arabia" },
    { lat: 23.8103, lon: 90.4125, label: "Dhaka, Bangladesh" }
  ];

  locations.forEach(loc => {
      L.marker([loc.lat, loc.lon]).addTo(map).bindPopup(loc.label);
  });
}
