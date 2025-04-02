// import { Component } from "@odoo/owl";

// export class KpiCard extends Component {}

// KpiCard.template = 'smkc.KpiCard'

// registry.category("actions").add('smkc.crm_dashboard_tag', KpiCard)

import { Component } from "@odoo/owl";

export class KpiCard extends Component {}

KpiCard.template = 'smkc.KpiCardTemplate';  // Ensure this matches the template name in kpi_card.xml
