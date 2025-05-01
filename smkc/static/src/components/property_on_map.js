

import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
import { PropertyMapView } from "./google_map/property_map";
import { ChartRenderer } from "./chart_renderer/chart_renderer";  // Import the ChartRenderer
import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";


export class OwlPropertyOnMap extends Component {
    static components = { KpiCard, ChartRenderer, PropertyMapView};  // Register ChartRenderer

    setup() {
        // You can set up any other logic for this dashboard component here if necessary
        // Reference to the chart element
        this.chartRef = useRef("chart");
        this.orm = useService("orm");

        this.state = useState({
            property_info: [],
        })

        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");

            // Property status wise data
            try {
                this.state.property_info = {};
                const propertyDetails = await this.orm.call('smkc.property.info', 'get_dashboard_data', []);
                console.log("propertyDetails - ", propertyDetails);
                if (propertyDetails && propertyDetails.length > 0) {
                    this.state.property_info = propertyDetails[0];
                } else {
                    console.log("No employee details found.");
                }
            } catch (error) {
                console.error("Error in onWillStart:", error);
                if (error instanceof Error) {
                    console.error("Error message: ", error.message);
                }
            }

            // Chart Render Data
        });
    }
}

// Define the template for the component
OwlPropertyOnMap.template = 'smkc.OwlPropertyOnGoogleMapTemplate';

// Register the component
registry.category("actions").add('smkc.action_property_map_sjdfkjad', OwlPropertyOnMap);
