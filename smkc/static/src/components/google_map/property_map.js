import { registry } from "@web/core/registry";
import { Component, onMounted, useRef } from "@odoo/owl";

export class PropertyMapView extends Component {
    static template = "property_map_template";

    setup() {
        this.mapRef = useRef("map");

        onMounted(async () => {
            console.log("Mounted: Loading Google Maps...");
            await this.loadGoogleMaps();
            this.initMap();
        });
    }

    async loadGoogleMaps() {
        return new Promise((resolve, reject) => {
            if (window.google && window.google.maps) {
                console.log("Google Maps already loaded.");
                return resolve();
            }

            const script = document.createElement("script");
            script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyCPulC96ujry-V0F29TagPf3wN6lnsmZhQ&callback=initMap";
            script.async = true;
            script.defer = true;

            window.initMap = () => {
                console.log("Google Maps script loaded.");
                resolve();
            };

            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    initMap() {
        const mapContainer = this.mapRef.el;
        if (!mapContainer) {
            console.error("Map container not found!");
            return;
        }

        const location = { lat: 27.7172, lng: 85.3240 }; // Kathmandu
        const map = new google.maps.Map(mapContainer, {
            center: location,
            zoom: 12,
        });

        new google.maps.Marker({
            position: location,
            map: map,
            title: "Kathmandu",
        });

        console.log("Map initialized.");
    }
}
// PropertyMapView.template = 'smkc.property_map_template';
registry.category("actions").add("property_map_view", PropertyMapView);
