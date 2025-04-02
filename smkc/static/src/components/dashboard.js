

// import { registry } from "@web/core/registry";
// import { KpiCard } from "./kpi_card/kpi_card";
// import { ChartRenderer } from "./ChartRenderer/ChartRenderer";

// import { loadJS } from "@web/core/assets";
// import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";  // Corrected import for `useRef`

// export class OwlCrmDashboard extends Component {
//     static components = { KpiCard, ChartRenderer };

//     setup() {
//         // Reference to the chart element
//         this.chartRef = useRef("chart");

//         // Load Chart.js library on component startup
//         onWillStart(async () => {
//             await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js");
//         });

//         // Initialize the chart after the component is mounted
//         onMounted(() => {
//             const data = [
//                 { year: 2010, count: 10 },
//                 { year: 2011, count: 20 },
//                 { year: 2012, count: 15 },
//                 { year: 2013, count: 25 },
//                 { year: 2014, count: 22 },
//                 { year: 2015, count: 30 },
//                 { year: 2016, count: 28 },
//             ];

//             // Ensure Chart.js is available before using it
//             if (typeof Chart !== 'undefined') {
//                 new Chart(
//                     this.chartRef.el,
//                     {
//                         type: 'doughnut',
//                         data: {
//                             labels: [
//                                 'Red',
//                                 'Blue',
//                                 'Yellow'
//                               ],
//                               datasets: [
//                                 {
//                                 label: 'My First Dataset',
//                                 data: [300, 50, 100],
//                                 backgroundColor: [
//                                   'rgb(255, 99, 132)',
//                                   'rgb(54, 162, 235)',
//                                   'rgb(255, 205, 86)'
//                                 ],
//                                 hoverOffset: 4
//                               },

//                               {
//                                 label: 'My Second Dataset',
//                                 data: [300, 70, 160],
//                                 backgroundColor: [
//                                   'red',
//                                   'green',
//                                   'orange'
//                                 ],
//                                 hoverOffset: 4
//                               }
//                             ]
//                         },
//                         options: {
//                             responsive: true,
//                             plugins: {
//                                 legends: {
//                                     position: 'bottom'
//                                 },
//                                 title: {
//                                     display: true,
//                                     text: 'Chart.js Doughnut Chart',
//                                     position: 'bottom'
//                                 }
//                             }
//                         },
//                     }
                    
//                 );
//             } else {
//                 console.error("Chart.js is not loaded.");
//             }
//         });
//     }
// }

// // Define the template for the component
// OwlCrmDashboard.template = 'smkc.OwlCrmTemplate';

// // Register the component
// registry.category("actions").add('smkc.crm_dashboard_tag', OwlCrmDashboard);


import { registry } from "@web/core/registry";
import { KpiCard } from "./kpi_card/kpi_card";
import { ChartRenderer } from "./chart_renderer/chart_renderer";  // Import the ChartRenderer
import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";


export class OwlCrmDashboard extends Component {
    static components = { KpiCard, ChartRenderer };  // Register ChartRenderer

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
OwlCrmDashboard.template = 'smkc.OwlCrmTemplate';

// Register the component
registry.category("actions").add('smkc.crm_dashboard_tag', OwlCrmDashboard);
