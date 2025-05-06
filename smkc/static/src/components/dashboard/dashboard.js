/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KpiCard } from "../kpi_card/kpi_card";
import { PropertyMapView } from "../google_map/property_map";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class OwlCrmDashboard extends Component {
    static components = { KpiCard, PropertyMapView };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            property_info: {},
            error: null
        });

        onWillStart(async () => {
            try {
                // Property status wise data
                const propertyDetails = await this.orm.call(
                    'smkc.property.info',
                    'get_dashboard_data',
                    [],
                    {}
                );
                
                console.log("propertyDetails - ", propertyDetails);
                if (propertyDetails && propertyDetails.length > 0) {
                    this.state.property_info = propertyDetails[0];
                } else {
                    console.log("No property details found.");
                }
            } catch (error) {
                console.error("Error in onWillStart:", error);
                this.state.error = error.message;
            }
        });
    }
}

// Define the template for the component
OwlCrmDashboard.template = 'smkc.OwlCrmTemplate';

// Register the component
registry.category("actions").add("smkc.crm_dashboard_tag", OwlCrmDashboard);
